#!/usr/bin/env python3
"""
Build dataset.zip for PrecisionFarming.

Baseline:
    data/images.zip                 (contains images/ and masks/, 97 baseline pairs)

Annotation sources:
    data/individual_annotation_samples/**

Output:
    final_dataset/
        images/
        masks/
        dataset.zip
        manifest.csv
        build_report.txt

Semantic mask IDs:
    background=0, sugar beet=1, weed=2, ignore=255

The script preserves the baseline image inventory, replaces baseline masks when a
matching semantic annotation is found, and appends DJI_0104 samples when it can
find original images and matching semantic masks.

Source files and source ZIPs are never modified.
Requires: pip install pillow numpy
"""

from pathlib import Path
from zipfile import ZipFile, BadZipFile
from PIL import Image
import numpy as np
import tempfile
import shutil
import json
import csv
import re
import io
import sys
import time


def log(message):
    print(message, flush=True)


def progress(current, total, label, start_time=None):
    pct = (100.0 * current / total) if total else 100.0
    elapsed = f" | {time.time() - start_time:.1f}s" if start_time else ""
    log(f"\r[{current:>4}/{total:<4} {pct:5.1f}%] {label}{elapsed}")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BASELINE_ZIP = DATA_DIR / "images.zip"
INDIVIDUAL_DIR = DATA_DIR / "individual_annotation_samples"
OUTPUT_DIR = PROJECT_ROOT / "final_dataset"
OUTPUT_ZIP = OUTPUT_DIR / "dataset.zip"
REPORT_PATH = OUTPUT_DIR / "build_report.txt"
MANIFEST_PATH = OUTPUT_DIR / "manifest.csv"

CLASS_RGB = {
    (0, 0, 0): 0,
    (25, 77, 28): 1,
    (250, 50, 83): 2,
    (115, 51, 128): 255,
}
VALID_IDS = {0, 1, 2, 255}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}


def normalize_stem(stem):
    return re.sub(r"[^a-z0-9]", "", stem.lower())


def group_from_name(name):
    m = re.search(r"(DJI[_-]?\d{4})", name, re.IGNORECASE)
    if m:
        return m.group(1).upper().replace("-", "_")
    return None


def image_id_from_path(path):
    # Consolidated names such as DJI_0099__DJI_0000 are kept as-is.
    return Path(path).stem


def read_image_bytes(data):
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
        return im
    except Exception:
        return None


def decode_semantic_mask(data, mapping=None):
    im = read_image_bytes(data)
    if im is None:
        return None, "unreadable image"

    mapping = mapping or CLASS_RGB
    if im.mode in ("L", "I", "I;16", "1"):
        arr = np.asarray(im)
        values = set(np.unique(arr).tolist())
        if values.issubset(VALID_IDS):
            return arr.astype(np.uint8), None
        return None, f"grayscale mask has unexpected values: {sorted(values)[:20]}"

    arr = np.asarray(im.convert("RGB"))
    out = np.full(arr.shape[:2], 255, dtype=np.uint8)
    seen = set()
    for rgb, class_id in mapping.items():
        rgb_arr = np.array(rgb, dtype=np.uint8)
        hit = np.all(arr == rgb_arr, axis=2)
        out[hit] = class_id
        seen.add(rgb)
    unique_colors = np.unique(arr.reshape(-1, 3), axis=0)
    unknown = [tuple(int(x) for x in c) for c in unique_colors if tuple(c.tolist()) not in mapping]
    if unknown:
        return None, f"RGB mask has unknown colors: {unknown[:10]}"
    return out, None


def parse_mapping_text(data):
    """Parse lines like '115 51 128 ignore' or '25 77 28 sugar beet'."""
    try:
        text = data.decode("utf-8", errors="replace")
    except Exception:
        return None
    mapping = {}
    names_to_ids = {
        "background": 0, "bg": 0,
        "sugar beet": 1, "sugarbeet": 1, "beet": 1,
        "weed": 2,
        "ignore": 255, "ignored": 255, "void": 255,
    }
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s+(.+?)\s*$", line)
        if not m:
            continue
        r, g, b, label = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4).lower()
        label = label.replace("_", " ")
        class_id = names_to_ids.get(label)
        if class_id is not None:
            mapping[(r, g, b)] = class_id
    return mapping if mapping else None


def is_mapping_file(name, data):
    # Some source mapping text files have misleading .png extensions.
    if len(data) > 4096:
        return False
    mapping = parse_mapping_text(data)
    return bool(mapping)


def zip_image_entries(zf):
    entries = []
    for name in zf.namelist():
        if name.endswith("/") or Path(name).suffix.lower() not in IMAGE_EXTS:
            continue
        try:
            data = zf.read(name)
        except Exception:
            continue
        if is_mapping_file(name, data):
            continue
        im = read_image_bytes(data)
        if im is not None:
            entries.append((name, data, im))
    return entries


def identify_semantic_mask_path(name):
    p = name.lower().replace("\\", "/")
    if "segmentationobject" in p:
        return False
    if "segmentationclass" in p:
        return True
    # Flat annotation batches: image-like PNGs outside object folders.
    return Path(name).suffix.lower() in {".png", ".tif", ".tiff", ".bmp"}


def find_mapping_in_zip(zf):
    mapping = dict(CLASS_RGB)
    for name in zf.namelist():
        low = name.lower()
        if low.endswith((".txt", ".png")) and ("labelmap" in low or "color" in low or "map" in low):
            try:
                data = zf.read(name)
            except Exception:
                continue
            parsed = parse_mapping_text(data)
            if parsed:
                # Source label maps often omit black/background. Preserve the
                # canonical background mapping and overlay source definitions.
                mapping = dict(CLASS_RGB)
                mapping.update(parsed)
                break
    # Also discover misnamed mapping text in small PNG entries.
    for name in zf.namelist():
        if Path(name).suffix.lower() != ".png":
            continue
        try:
            data = zf.read(name)
        except Exception:
            continue
        parsed = parse_mapping_text(data)
        if parsed:
            mapping = dict(CLASS_RGB)
            mapping.update(parsed)
            break
    return mapping


def candidate_annotation_entries(zf):
    mapping = find_mapping_in_zip(zf)
    candidates = []
    for name in zf.namelist():
        p = name.lower().replace("\\", "/")
        if name.endswith("/") or Path(name).suffix.lower() not in {".png", ".tif", ".tiff", ".bmp"}:
            continue
        if "segmentationobject" in p or "object" in Path(p).parent.name.lower():
            continue
        try:
            data = zf.read(name)
        except Exception:
            continue
        if is_mapping_file(name, data):
            continue
        im = read_image_bytes(data)
        if im is None:
            continue
        if "segmentationclass" in p or not any(x in p for x in ("original", "images", "image/")):
            arr, err = decode_semantic_mask(data, mapping)
            if arr is not None:
                candidates.append((name, data, arr))
    return candidates


def stem_key(stem):
    return normalize_stem(Path(stem).stem)


def pair_key(group, stem):
    return (normalize_stem(group or ""), stem_key(stem))


def group_from_archive_path(path):
    # Group is the first directory under individual_annotation_samples.
    try:
        relative = Path(path).relative_to(INDIVIDUAL_DIR)
        first = relative.parts[0]
        return group_from_name(first) or first.upper()
    except Exception:
        return group_from_name(str(path))


def is_original_archive(path):
    return normalize_stem(Path(path).stem) in {"original", "origial", "originial", "origional", "originalimages"}


def load_original_images_from_archive(archive_path):
    result = {}
    try:
        with ZipFile(archive_path, "r") as zf:
            for name, data, im in zip_image_entries(zf):
                if Path(name).suffix.lower() not in {".jpg", ".jpeg"}:
                    continue
                if any(x in name.lower().replace("\\\\", "/") for x in ("segmentationclass", "segmentationobject", "mask", "annotation")):
                    continue
                result[stem_key(Path(name).name)] = (name, data)
    except Exception as e:
        log(f"  Could not read originals archive {archive_path}: {e}")
    return result


def make_lookup(entries):
    lookup = {}
    for name, data, arr in entries:
        key = stem_key(Path(name).name)
        lookup.setdefault(key, []).append((name, data, arr))
    return lookup


def add_image_and_mask(out_images, out_masks, image_name, image_data, mask_array, output_stem, manifest_rows, source):
    im = read_image_bytes(image_data)
    if im is None:
        return False, "image unreadable"
    if im.size != (mask_array.shape[1], mask_array.shape[0]):
        return False, f"dimension mismatch: image {im.size}, mask {(mask_array.shape[1], mask_array.shape[0])}"
    image_ext = Path(image_name).suffix.lower()
    if image_ext not in {".jpg", ".jpeg"}:
        image_ext = ".jpg"
        # Keep source bytes only if already JPEG; otherwise re-encode.
        buffer = io.BytesIO()
        im.convert("RGB").save(buffer, format="JPEG", quality=95)
        image_data = buffer.getvalue()
    image_out = output_stem + image_ext
    mask_out = output_stem + ".png"
    out_images[image_out] = image_data
    mask_buffer = io.BytesIO()
    Image.fromarray(mask_array, mode="L").save(mask_buffer, format="PNG")
    out_masks[mask_out] = mask_buffer.getvalue()
    values = sorted(int(x) for x in np.unique(mask_array))
    manifest_rows.append({
        "sample_id": output_stem,
        "image": f"images/{image_out}",
        "mask": f"masks/{mask_out}",
        "width": im.width,
        "height": im.height,
        "mask_values": ";".join(map(str, values)),
        "annotation_source": source,
    })
    return True, None


def main():
    if not BASELINE_ZIP.exists():
        sys.exit(f"Baseline ZIP not found: {BASELINE_ZIP}")
    if not INDIVIDUAL_DIR.exists():
        sys.exit(f"Annotation directory not found: {INDIVIDUAL_DIR}")

    build_start = time.time()
    log("=" * 72)
    log("PRECISION FARMING DATASET BUILDER")
    log(f"Baseline: {BASELINE_ZIP}")
    log(f"Annotations: {INDIVIDUAL_DIR}")
    log(f"Output: {OUTPUT_ZIP}")
    log("=" * 72)

    report = {
        "baseline_zip": str(BASELINE_ZIP),
        "individual_annotations": str(INDIVIDUAL_DIR),
        "warnings": [],
        "errors": [],
        "baseline_pairs": 0,
        "replaced_masks": 0,
        "appended_samples": 0,
        "unmatched_baseline_images": [],
        "unmatched_annotations": [],
        "bad_masks": [],
        "dimension_errors": [],
        "source_archives": [],
    }

    with tempfile.TemporaryDirectory(prefix="precisionfarming_build_") as td:
        td = Path(td)
        baseline_images = {}
        baseline_masks = {}
        log("[1/5] Reading baseline ZIP and indexing images/masks...")
        with ZipFile(BASELINE_ZIP, "r") as base:
            bad = base.testzip()
            if bad:
                sys.exit(f"Baseline ZIP integrity failed at {bad}")
            for name in base.namelist():
                p = Path(name)
                if p.suffix.lower() not in IMAGE_EXTS:
                    continue
                data = base.read(name)
                im = read_image_bytes(data)
                if im is None:
                    continue
                if "/images/" in name.lower() or name.lower().startswith("images/"):
                    baseline_images[p.name] = data
                elif "/masks/" in name.lower() or name.lower().startswith("masks/"):
                    baseline_masks[p.name] = data

        # Pair baseline images to their existing masks.
        baseline_pairs = {}
        mask_by_stem = {stem_key(n): (n, d) for n, d in baseline_masks.items()}
        for image_name, image_data in baseline_images.items():
            k = stem_key(image_name)
            existing = mask_by_stem.get(k)
            if existing:
                baseline_pairs[image_name] = (image_data, existing[1], existing[0])
        report["baseline_pairs"] = len(baseline_pairs)
        if not baseline_pairs:
            sys.exit("No baseline image/mask pairs were found inside data/images.zip. Check ZIP folder layout.")

        log(f"Baseline inventory: {len(baseline_images)} images, {len(baseline_masks)} masks, {len(baseline_pairs)} matched pairs")
        log("[2/5] Scanning annotation ZIP archives (this can take time)...")
        semantic_lookup = {}
        original_images_0104 = {}
        archive_paths = [p for p in INDIVIDUAL_DIR.rglob("*.zip") if not is_original_archive(p)]
        log(f"Found {len(archive_paths)} annotation ZIP archives (original-image ZIPs skipped).")
        scan_start = time.time()
        for archive_idx, archive_path in enumerate(archive_paths, 1):
            group = group_from_archive_path(archive_path)
            log(f"\\nArchive [{archive_idx}/{len(archive_paths)}]: {archive_path.relative_to(INDIVIDUAL_DIR)}")
            try:
                with ZipFile(archive_path, "r") as zf:
                    report["source_archives"].append(str(archive_path.relative_to(DATA_DIR)))
                    candidates = candidate_annotation_entries(zf)
                    log(f"  Semantic masks decoded: {len(candidates)}")
                    for name, data, arr in candidates:
                        semantic_lookup.setdefault(pair_key(group, Path(name).name), []).append((name, arr, str(archive_path)))
            except BadZipFile:
                report["warnings"].append(f"Bad ZIP skipped: {archive_path}")
                log("  WARNING: invalid ZIP, skipped")
            except Exception as e:
                report["warnings"].append(f"Archive scan issue {archive_path}: {e}")
                log(f"  WARNING: {e}")

        # Read DJI_0104 original images separately, without decoding them as masks.
        original_zip_paths = [p for p in INDIVIDUAL_DIR.rglob("*.zip") if is_original_archive(p) and "DJI_0104" in str(p).upper()]
        for orig_path in original_zip_paths:
            log(f"Reading DJI_0104 original images: {orig_path.relative_to(INDIVIDUAL_DIR)}")
            original_images_0104.update(load_original_images_from_archive(orig_path))

        log(f"\nArchive scan finished in {time.time()-scan_start:.1f}s; annotation stem keys indexed: {len(semantic_lookup)}")
        log("[3/5] Matching baseline images and preparing masks...")
        out_images = {}
        out_masks = {}
        manifest_rows = []
        baseline_keys = set()
        baseline_total = len(baseline_pairs)
        for baseline_idx, (image_name, (image_data, old_mask_data, old_mask_name)) in enumerate(baseline_pairs.items(), 1):
            progress(baseline_idx, baseline_total, f"Matching baseline {image_name}", build_start)
            sample_stem = Path(image_name).stem
            k = stem_key(image_name)
            group = group_from_name(image_name)
            match_key = pair_key(group, image_name)
            baseline_keys.add(match_key)
            candidates = semantic_lookup.get(match_key, [])
            chosen = candidates[0] if candidates else None
            if chosen:
                source_name, arr, archive = chosen
                if len(candidates) > 1:
                    report["warnings"].append(f"Multiple annotation matches for {sample_stem}; using first: {source_name}")
                ok, err = add_image_and_mask(out_images, out_masks, image_name, image_data, arr, sample_stem, manifest_rows, archive + "::" + source_name)
                if ok:
                    report["replaced_masks"] += 1
                else:
                    report["dimension_errors"].append({"sample": sample_stem, "error": err, "source": source_name})
                    # Use the baseline mask if its contents can be decoded.
                    old_arr, old_err = decode_semantic_mask(old_mask_data)
                    if old_arr is not None:
                        add_image_and_mask(out_images, out_masks, image_name, image_data, old_arr, sample_stem, manifest_rows, "baseline images.zip")
                    else:
                        report["errors"].append(f"{sample_stem}: source and baseline mask invalid")
            else:
                old_arr, old_err = decode_semantic_mask(old_mask_data)
                if old_arr is None:
                    report["bad_masks"].append({"sample": sample_stem, "error": old_err})
                    report["unmatched_baseline_images"].append(image_name)
                    continue
                ok, err = add_image_and_mask(out_images, out_masks, image_name, image_data, old_arr, sample_stem, manifest_rows, "baseline images.zip")
                if not ok:
                    report["dimension_errors"].append({"sample": sample_stem, "error": err})
        log(f"\nBaseline matching done: {len(out_images)} pairs currently prepared.")
        log("[4/5] Checking DJI_0104 supplemental originals and annotations...")
        supplemental_total = len(original_images_0104)
        for supplemental_idx, (k, (image_name, image_data)) in enumerate(original_images_0104.items(), 1):
            progress(supplemental_idx, supplemental_total, f"DJI_0104 {image_name}", build_start)
            supplemental_key = pair_key("DJI_0104", image_name)
            if supplemental_key in baseline_keys:
                continue
            candidates = semantic_lookup.get(supplemental_key, [])
            if not candidates:
                report["unmatched_baseline_images"].append(f"DJI_0104::{image_name} (no semantic mask)")
                continue
            source_name, arr, archive = candidates[0]
            stem = "DJI_0104__" + Path(image_name).stem
            ok, err = add_image_and_mask(out_images, out_masks, image_name, image_data, arr, stem, manifest_rows, archive + "::" + source_name)
            if ok:
                report["appended_samples"] += 1
            else:
                report["dimension_errors"].append({"sample": stem, "error": err})

        log("\n[5/5] Validating output pairs and writing ZIP/report...")
        # Record annotation files that weren't matched to a baseline or supplemental image.
        for k, candidates in semantic_lookup.items():
            if k not in baseline_keys and k not in {pair_key("DJI_0104", stem) for stem in original_images_0104}:
                report["unmatched_annotations"].extend([c[0] for c in candidates])

        if len(out_images) != len(out_masks):
            report["errors"].append(f"Output image/mask count mismatch: {len(out_images)} images vs {len(out_masks)} masks")
        if not out_images:
            sys.exit("No valid output pairs produced.")

        # Materialize the self-contained final_dataset directory.
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        images_dir, masks_dir = OUTPUT_DIR / "images", OUTPUT_DIR / "masks"
        images_dir.mkdir(exist_ok=True); masks_dir.mkdir(exist_ok=True)
        for folder in (images_dir, masks_dir):
            for existing in folder.iterdir():
                if existing.is_file():
                    existing.unlink()
        for name, data in out_images.items():
            (images_dir / name).write_bytes(data)
        for name, data in out_masks.items():
            (masks_dir / name).write_bytes(data)

        with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as f:
            fields = ["sample_id", "image", "mask", "width", "height", "mask_values", "annotation_source"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader(); writer.writerows(manifest_rows)

        report["output_images"] = len(out_images)
        report["output_masks"] = len(out_masks)
        report["total_pairs"] = len(manifest_rows)
        report["manifest"] = "manifest.csv"
        report["output_directory"] = str(OUTPUT_DIR)

        report_lines = [
            "PRECISION FARMING DATASET BUILD REPORT", "=" * 40,
            f"Baseline pairs: {report['baseline_pairs']}",
            f"Masks replaced: {report['replaced_masks']}",
            f"DJI_0104 appended: {report['appended_samples']}",
            f"Output pairs: {report['total_pairs']}",
            f"Unmatched annotations: {len(report['unmatched_annotations'])}",
            f"Dimension errors: {len(report['dimension_errors'])}",
            f"Bad masks: {len(report['bad_masks'])}",
            "", "Warnings:", *(f"- {w}" for w in report["warnings"]),
            "", "Unmatched baseline samples:", *(f"- {x}" for x in report["unmatched_baseline_images"]),
            "", "Unmatched annotation files:", *(f"- {x}" for x in report["unmatched_annotations"]),
            "", "Dimension errors:", *(f"- {x}" for x in report["dimension_errors"]),
            "", "Bad masks:", *(f"- {x}" for x in report["bad_masks"]),
        ]
        REPORT_PATH.write_text("\\n".join(report_lines), encoding="utf-8")

        if OUTPUT_ZIP.exists():
            backup = OUTPUT_ZIP.with_suffix(".zip.bak")
            shutil.copy2(OUTPUT_ZIP, backup)
            report["warnings"].append(f"Previous output backed up to {backup.name}")
        with ZipFile(OUTPUT_ZIP, "w") as out:
            for name, data in out_images.items(): out.writestr(f"images/{name}", data)
            for name, data in out_masks.items(): out.writestr(f"masks/{name}", data)
            out.write(MANIFEST_PATH, "manifest.csv")
            out.writestr("build_report.txt", REPORT_PATH.read_text(encoding="utf-8"))

    print("\nDataset build complete")
    print("-" * 60)
    log(f"Baseline pairs:          {report['baseline_pairs']}")
    log(f"Masks replaced:         {report['replaced_masks']}")
    log(f"DJI_0104 appended:      {report['appended_samples']}")
    log(f"Output pairs:           {report['total_pairs']}")
    log(f"Unmatched annotations:   {len(report['unmatched_annotations'])}")
    log(f"Dimension errors:        {len(report['dimension_errors'])}")
    log(f"Bad masks:              {len(report['bad_masks'])}")
    log(f"Output ZIP:              {OUTPUT_ZIP}")
    log(f"Report:                  {REPORT_PATH}")
    log(f"Total elapsed:            {time.time()-build_start:.1f}s")


if __name__ == "__main__":
    main()
