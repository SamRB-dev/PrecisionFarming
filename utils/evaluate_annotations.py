"""Evaluate agreement between two independently produced semantic masks.

Implements the Work Package C protocol in the ASB Lab 01 notebook:
- class-wise IoU for background, sugar beet, and weed;
- aggregate intersections/unions over all matched images before division;
- ignore a pixel when either annotator marks it as 255;
- report the excluded-pixel fraction separately;
- report IoU as N/A when the class union is zero.

Run from the repository root:
    python utils/evaluate_annotations.py
    python utils/evaluate_annotations.py --image-id DJI_0000

The ZIP/mask discovery and decoding are shared with compare_annotations.py.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

try:
    from compare_annotations import find_zip_files, load_mask_from_zip
except ImportError:  # pragma: no cover
    from utils.compare_annotations import find_zip_files, load_mask_from_zip


CLASS_NAMES = {0: "Background", 1: "Sugar beet", 2: "Weed"}
IGNORE_ID = 255
ANNOTATOR_1_DIR = Path("data/mutual_annotated_samples/annot_list_1")
ANNOTATOR_2_DIR = Path("data/mutual_annotated_samples/annot_list_2")
OUTPUT_DIR = Path("experiments/annotation_evaluation")


def calculate_image_counts(mask_a: np.ndarray, mask_b: np.ndarray) -> dict:
    """Return valid-pixel and per-class intersection/union counts for one image."""
    if mask_a.shape != mask_b.shape:
        raise ValueError(
            "Mask dimensions differ: "
            f"annotator 1 {mask_a.shape}, annotator 2 {mask_b.shape}. "
            "No resizing is performed for quantitative evaluation."
        )

    allowed = set(CLASS_NAMES) | {IGNORE_ID}
    values_a = set(np.unique(mask_a).tolist())
    values_b = set(np.unique(mask_b).tolist())
    invalid_a = values_a - allowed
    invalid_b = values_b - allowed
    if invalid_a or invalid_b:
        raise ValueError(
            f"Unexpected class IDs: annotator 1={sorted(invalid_a)}, "
            f"annotator 2={sorted(invalid_b)}; expected only {sorted(allowed)}."
        )

    ignored = (mask_a == IGNORE_ID) | (mask_b == IGNORE_ID)
    valid = ~ignored
    counts = {
        "total_pixels": int(mask_a.size),
        "excluded_pixels": int(np.count_nonzero(ignored)),
        "valid_pixels": int(np.count_nonzero(valid)),
        "classes": {},
    }

    for class_id, class_name in CLASS_NAMES.items():
        a_class = (mask_a == class_id) & valid
        b_class = (mask_b == class_id) & valid
        intersection = int(np.count_nonzero(a_class & b_class))
        union = int(np.count_nonzero(a_class | b_class))
        counts["classes"][class_id] = {
            "class_name": class_name,
            "intersection": intersection,
            "union": union,
            "iou": intersection / union if union else None,
        }

    return counts


def _zip_map(directory: Path) -> dict[str, Path]:
    return {path.stem.lower(): path for path in find_zip_files(directory)}


def evaluate_dataset(
    annotator_1_dir: Path,
    annotator_2_dir: Path,
    image_id: str | None = None,
) -> tuple[list[dict], dict]:
    """Evaluate shared ZIP IDs and aggregate counts before calculating IoU."""
    zips_a = _zip_map(annotator_1_dir)
    zips_b = _zip_map(annotator_2_dir)
    shared_ids = sorted(set(zips_a) & set(zips_b))
    if image_id:
        shared_ids = [item for item in shared_ids if item == image_id.lower()]
    if not shared_ids:
        raise RuntimeError("No matching annotation ZIP pairs were found.")

    per_image = []
    aggregate = {
        "image_count": 0,
        "total_pixels": 0,
        "excluded_pixels": 0,
        "valid_pixels": 0,
        "classes": {
            class_id: {"class_name": name, "intersection": 0, "union": 0}
            for class_id, name in CLASS_NAMES.items()
        },
    }

    for key in shared_ids:
        display_id = zips_a[key].stem
        mask_a = load_mask_from_zip(zips_a[key], display_id)
        mask_b = load_mask_from_zip(zips_b[key], display_id)
        counts = calculate_image_counts(mask_a, mask_b)

        row = {
            "image_id": display_id,
            "total_pixels": counts["total_pixels"],
            "excluded_pixels": counts["excluded_pixels"],
            "excluded_fraction": (
                counts["excluded_pixels"] / counts["total_pixels"]
                if counts["total_pixels"] else 0.0
            ),
        }
        for class_id, result in counts["classes"].items():
            column = f"{CLASS_NAMES[class_id].lower().replace(' ', '_')}_iou"
            row[column] = result["iou"]
            aggregate["classes"][class_id]["intersection"] += result["intersection"]
            aggregate["classes"][class_id]["union"] += result["union"]

        per_image.append(row)
        aggregate["image_count"] += 1
        for key_name in ("total_pixels", "excluded_pixels", "valid_pixels"):
            aggregate[key_name] += counts[key_name]

    # Pool counts across images first; do not average per-image IoU values.
    for result in aggregate["classes"].values():
        union = result["union"]
        result["iou"] = result["intersection"] / union if union else None

    aggregate["excluded_fraction"] = (
        aggregate["excluded_pixels"] / aggregate["total_pixels"]
        if aggregate["total_pixels"] else 0.0
    )
    return per_image, aggregate


def write_outputs(per_image: list[dict], aggregate: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    per_image_path = output_dir / "per_image_iou.csv"
    with per_image_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(per_image[0].keys()))
        writer.writeheader()
        writer.writerows(per_image)

    summary_path = output_dir / "aggregate_iou.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["class_id", "class_name", "intersection", "union", "iou"]
        )
        writer.writeheader()
        for class_id, result in aggregate["classes"].items():
            writer.writerow({"class_id": class_id, **result})

    excluded_path = output_dir / "ignore_statistics.csv"
    with excluded_path.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "image_count", "total_pixels", "excluded_pixels",
            "valid_pixels", "excluded_fraction",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({key: aggregate[key] for key in fields})

    print(f"Evaluated image pairs: {aggregate['image_count']}")
    print(
        "Pixels excluded (ignore in either mask): "
        f"{aggregate['excluded_pixels']:,} / {aggregate['total_pixels']:,} "
        f"({aggregate['excluded_fraction']:.2%})"
    )
    print("\nAggregate class-wise IoU (pooled across images):")
    for class_id, result in aggregate["classes"].items():
        score = (
            "N/A (zero union)" if result["iou"] is None
            else f"{result['iou']:.4f} ({result['iou']:.2%})"
        )
        print(f"  {class_id} {result['class_name']}: {score}")
    print(f"\nCSV outputs written to: {output_dir}")
    print(f"  - {per_image_path.name}")
    print(f"  - {summary_path.name}")
    print(f"  - {excluded_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate class-wise IoU between two annotators' semantic masks."
    )
    parser.add_argument("--image-id", help="Evaluate one image ID, e.g. DJI_0000.")
    parser.add_argument(
        "--root", type=Path, default=Path("."),
        help="Project root (default: current directory).",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    try:
        per_image, aggregate = evaluate_dataset(
            root / ANNOTATOR_1_DIR,
            root / ANNOTATOR_2_DIR,
            args.image_id,
        )
        write_outputs(per_image, aggregate, root / OUTPUT_DIR)
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
