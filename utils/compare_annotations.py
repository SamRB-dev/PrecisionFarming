"""
Compare two annotators' segmentation masks against the original images.

Layout:
    Top:    Original image
    Bottom: SamRB-dev annotation | Azefty annotation

Expected directories:
    data/initial_inspection_samples/
    data/mutual_annotated_samples/annot_list_1/
    data/mutual_annotated_samples/annot_list_2/

Output:
    experiments/annotation_comparisons/

Run:
    python utils/compare_annotations.py

Run for one image:
    python utils/compare_annotations.py --image-id DJI_0000
"""

import argparse
import io
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


# ============================================================
# GLOBAL CONFIGURATION
# CHANGE SETTINGS HERE; THE REST OF THE SCRIPT USES THESE.
# ============================================================

# ----------------------------
# FONT SETTINGS
# ----------------------------

FONT_SIZE = 85
FONT_BOLD = True
FONT_NAME = "arial"

# Other font sizes are derived automatically from FONT_SIZE.
# Change FONT_SIZE above rather than editing these individually.
HEADER_FONT_SIZE = FONT_SIZE
LEGEND_FONT_SIZE = max(12, int(FONT_SIZE * 0.55))
INFO_FONT_SIZE = max(10, int(FONT_SIZE * 0.40))

# ----------------------------
# LAYOUT SETTINGS
# ----------------------------

# Image display width. Set to None to retain the original width.
DISPLAY_WIDTH = 1600

# Dimensions scale with FONT_SIZE.
HEADER_HEIGHT = int(FONT_SIZE * 2.4)
HEADER_PADDING = int(FONT_SIZE * 0.45)
LEGEND_HEIGHT = int(FONT_SIZE * 2.0)
PANEL_GAP = max(8, int(FONT_SIZE * 0.25))
OUTER_PADDING = max(10, int(FONT_SIZE * 0.35))

# ----------------------------
# OVERLAY SETTINGS
# ----------------------------

# Transparency of annotation overlays.
# 0 = completely transparent; 255 = completely opaque.
OVERLAY_ALPHA = 145

# Annotation colours, specified as RGB.
SUGAR_BEET_COLOR = (25, 77, 28)
WEED_COLOR = (250, 50, 83)
IGNORE_COLOR = (115, 51, 128)

# Background colour for headers, legends, and gaps.
CANVAS_BACKGROUND = (30, 30, 30)

# Header and legend text colour.
TEXT_COLOR = (255, 255, 255)

# ----------------------------
# ANNOTATION LABEL SETTINGS
# ----------------------------

SUGAR_BEET_LABEL = "Sugar beet"
WEED_LABEL = "Weed"
IGNORE_LABEL = "Ignore / uncertain"

# Annotation IDs.
SUGAR_BEET_ID = 1
WEED_ID = 2
IGNORE_ID = 255

# ----------------------------
# DIRECTORY SETTINGS
# ----------------------------

ORIGINALS_DIR = Path("data/initial_inspection_samples")

ANNOTATOR_1_DIR = Path(
    "data/mutual_annotated_samples/annot_list_1"
)

ANNOTATOR_2_DIR = Path(
    "data/mutual_annotated_samples/annot_list_2"
)

OUTPUT_DIR = Path("experiments/annotation_comparisons")

# Display names for the two annotators.
ANNOTATOR_1_NAME = "SamRB-dev"
ANNOTATOR_2_NAME = "Azefty"

# Supported original image extensions.
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff",
    ".bmp",
    ".webp",
}

# Supported image formats inside annotation ZIP files.
MASK_EXTENSIONS = {
    ".png",
    ".tif",
    ".tiff",
    ".bmp",
    ".jpg",
    ".jpeg",
}


# ============================================================
# FONT HELPERS
# ============================================================

def get_font(size=None, bold=None):
    """Load a font using the global configuration."""

    if size is None:
        size = FONT_SIZE

    if bold is None:
        bold = FONT_BOLD

    font_name = FONT_NAME.lower()

    if font_name == "arial":
        if bold:
            candidates = [
                "C:/Windows/Fonts/arialbd.ttf",
                "C:/Windows/Fonts/segoeuib.ttf",
            ]
        else:
            candidates = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/segoeui.ttf",
            ]

    elif font_name == "segoe":
        if bold:
            candidates = [
                "C:/Windows/Fonts/segoeuib.ttf",
                "C:/Windows/Fonts/arialbd.ttf",
            ]
        else:
            candidates = [
                "C:/Windows/Fonts/segoeui.ttf",
                "C:/Windows/Fonts/arial.ttf",
            ]

    else:
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf"
            if bold
            else "C:/Windows/Fonts/arial.ttf"
        ]

    for font_path in candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            continue

    # Pillow's default font is a fallback, not an exact equivalent
    # to the configured TrueType font.
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


# ============================================================
# FILE DISCOVERY
# ============================================================

def find_original(image_id, originals_dir):
    """Find the original image matching an image ID."""

    if not originals_dir.exists():
        raise FileNotFoundError(
            f"Original image directory does not exist: {originals_dir}"
        )

    for path in originals_dir.iterdir():
        if (
            path.is_file()
            and path.suffix.lower() in IMAGE_EXTENSIONS
            and path.stem.lower() == image_id.lower()
        ):
            return path

    return None


def get_image_id_from_zip(zip_path):
    """Use the ZIP filename stem as the image ID."""

    return zip_path.stem


def find_zip_files(directory):
    """Return ZIP files from an annotator directory."""

    if not directory.exists():
        raise FileNotFoundError(
            f"Annotation directory does not exist: {directory}"
        )

    return sorted(
        directory.glob("*.zip"),
        key=lambda path: path.name.lower(),
    )


def image_members_in_zip(zip_file):
    """List supported image files inside a ZIP archive."""

    return [
        name
        for name in zip_file.namelist()
        if (
            Path(name).suffix.lower() in MASK_EXTENSIONS
            and not name.endswith("/")
            and "__MACOSX" not in name
        )
    ]


def choose_mask_member(zip_file, image_id):
    """
    Select the most likely annotation image inside a ZIP.

    Selection order:
        1. Exact image ID filename.
        2. Filename containing the image ID.
        3. A filename containing mask/label/annot/seg.
        4. The only image in the archive.

    Raises an error if the archive remains ambiguous.
    """

    members = image_members_in_zip(zip_file)

    if not members:
        raise ValueError(
            f"No supported image files found in {zip_file.filename}"
        )

    # Ignore unrelated images outside defaultannot when possible.
    defaultannot_members = [
        name
        for name in members
        if "defaultannot" in name.lower().replace("\\", "/").split("/")
    ]

    if defaultannot_members:
        members = defaultannot_members

    # First choice: exact filename stem.
    exact_matches = [
        name
        for name in members
        if Path(name).stem.lower() == image_id.lower()
    ]

    if len(exact_matches) == 1:
        return exact_matches[0]

    # Second choice: filename contains the image ID.
    id_matches = [
        name
        for name in members
        if image_id.lower() in Path(name).stem.lower()
    ]

    if len(id_matches) == 1:
        return id_matches[0]

    # Third choice: likely annotation filename.
    keyword_matches = [
        name
        for name in members
        if re.search(
            r"(mask|label|annot|seg)",
            Path(name).stem,
            re.IGNORECASE,
        )
    ]

    if len(keyword_matches) == 1:
        return keyword_matches[0]

    # If there is only one image, use it.
    if len(members) == 1:
        return members[0]

    # Do not silently choose the wrong mask.
    raise ValueError(
        f"Could not uniquely identify the mask in "
        f"{zip_file.filename}.\n"
        f"Candidate images:\n"
        + "\n".join(f"  - {name}" for name in members)
    )


# ============================================================
# MASK DECODING
# ============================================================

def decode_rgb_mask(rgb_array):
    """
    Convert an RGB annotation image into integer class IDs.

    Expected colours:
        Green  = sugar beet
        Red    = weed
        Purple = ignore / uncertain
        Black  = background

    Unknown colours are treated as background.
    """

    mask = np.zeros(rgb_array.shape[:2], dtype=np.uint8)

    sugar_beet = np.all(
        rgb_array[:, :, :3] == SUGAR_BEET_COLOR,
        axis=2,
    )

    weed = np.all(
        rgb_array[:, :, :3] == WEED_COLOR,
        axis=2,
    )

    ignore = np.all(
        rgb_array[:, :, :3] == IGNORE_COLOR,
        axis=2,
    )

    mask[sugar_beet] = SUGAR_BEET_ID
    mask[weed] = WEED_ID
    mask[ignore] = IGNORE_ID

    return mask


def convert_image_to_mask(image):
    """
    Convert an annotation image to a 2D integer mask.

    Indexed or grayscale images are preserved as class IDs.
    RGB images are decoded using the configured annotation colours.
    """

    image.load()

    # Preserve indexed masks and grayscale masks.
    if image.mode in ("L", "P", "1", "I", "I;16"):
        array = np.asarray(image)

        if array.ndim == 2:
            return array.astype(np.uint8)

    # Decode RGB colour masks.
    rgb = np.asarray(image.convert("RGB"))

    return decode_rgb_mask(rgb)


def load_mask_from_zip(zip_path, image_id):
    """Load the selected annotation mask from a ZIP archive."""

    with zipfile.ZipFile(zip_path, "r") as archive:
        member = choose_mask_member(archive, image_id)
        image_bytes = archive.read(member)

    with Image.open(io.BytesIO(image_bytes)) as image:
        mask = convert_image_to_mask(image)

    return mask


# ============================================================
# ANNOTATION OVERLAYS
# ============================================================

def make_overlay(original, mask):
    """
    Overlay the annotation mask on the original image.

    The original image remains visible through the coloured regions.
    Background pixels are left unchanged.
    """

    original = original.convert("RGBA")

    if mask.shape != (original.height, original.width):
        mask_image = Image.fromarray(mask.astype(np.uint8))
        mask_image = mask_image.resize(
            original.size,
            Image.Resampling.NEAREST,
        )
        mask = np.asarray(mask_image)

    overlay_array = np.zeros(
        (original.height, original.width, 4),
        dtype=np.uint8,
    )

    overlay_array[mask == SUGAR_BEET_ID] = (
        *SUGAR_BEET_COLOR,
        OVERLAY_ALPHA,
    )

    overlay_array[mask == WEED_ID] = (
        *WEED_COLOR,
        OVERLAY_ALPHA,
    )

    overlay_array[mask == IGNORE_ID] = (
        *IGNORE_COLOR,
        OVERLAY_ALPHA,
    )

    overlay = Image.fromarray(overlay_array, mode="RGBA")

    return Image.alpha_composite(original, overlay).convert("RGB")


# ============================================================
# HEADER AND LEGEND
# ============================================================

def add_header(image, title):
    """Add a title header using globally configured font settings."""

    image = image.convert("RGB")

    header = Image.new(
        "RGB",
        (image.width, HEADER_HEIGHT),
        CANVAS_BACKGROUND,
    )

    draw = ImageDraw.Draw(header)
    font = get_font(HEADER_FONT_SIZE)

    draw.text(
        (HEADER_PADDING, HEADER_PADDING),
        title,
        fill=TEXT_COLOR,
        font=font,
    )

    result = Image.new(
        "RGB",
        (image.width, image.height + HEADER_HEIGHT),
        CANVAS_BACKGROUND,
    )

    result.paste(header, (0, 0))
    result.paste(image, (0, HEADER_HEIGHT))

    return result


def draw_legend(image):
    """Add a colour legend using globally configured font settings."""

    image = image.convert("RGB")

    legend = Image.new(
        "RGB",
        (image.width, LEGEND_HEIGHT),
        CANVAS_BACKGROUND,
    )

    draw = ImageDraw.Draw(legend)
    font = get_font(LEGEND_FONT_SIZE)

    items = [
        (SUGAR_BEET_LABEL, SUGAR_BEET_COLOR),
        (WEED_LABEL, WEED_COLOR),
        (IGNORE_LABEL, IGNORE_COLOR),
    ]

    x = HEADER_PADDING

    # Vertically center the legend items.
    y = max(
        0,
        (LEGEND_HEIGHT - LEGEND_FONT_SIZE) // 2,
    )

    for label, color in items:
        box_size = LEGEND_FONT_SIZE

        draw.rectangle(
            (
                x,
                y,
                x + box_size,
                y + box_size,
            ),
            fill=color,
        )

        x += box_size + HEADER_PADDING // 2

        draw.text(
            (x, y - 2),
            label,
            fill=TEXT_COLOR,
            font=font,
        )

        text_width = draw.textbbox(
            (0, 0),
            label,
            font=font,
        )[2]

        x += text_width + HEADER_PADDING * 2

    result = Image.new(
        "RGB",
        (image.width, image.height + LEGEND_HEIGHT),
        CANVAS_BACKGROUND,
    )

    result.paste(image, (0, 0))
    result.paste(legend, (0, image.height))

    return result


# ============================================================
# IMAGE RESIZING
# ============================================================

def resize_to_width(image, width):
    """Resize an image while preserving its aspect ratio."""

    if width is None or width <= 0 or image.width <= width:
        return image

    new_height = round(image.height * width / image.width)

    return image.resize(
        (width, new_height),
        Image.Resampling.LANCZOS,
    )


# ============================================================
# COMPARISON IMAGE CREATION
# ============================================================

def create_comparison(
    image_id,
    original_path,
    annotator_1_zip,
    annotator_2_zip,
    output_dir,
):
    """
    Create one comparison image.

    Layout:
        Original image at the top.
        SamRB-dev overlay at the bottom-left.
        Azefty overlay at the bottom-right.
    """

    print(f"Processing {image_id}...")

    with Image.open(original_path) as image:
        original = image.convert("RGB")

    # Load both annotation masks.
    mask_1 = load_mask_from_zip(
        annotator_1_zip,
        image_id,
    )

    mask_2 = load_mask_from_zip(
        annotator_2_zip,
        image_id,
    )

    # Generate the overlays.
    overlay_1 = make_overlay(original, mask_1)
    overlay_2 = make_overlay(original, mask_2)

    # Resize all panels consistently.
    original = resize_to_width(original, DISPLAY_WIDTH)
    overlay_1 = resize_to_width(overlay_1, DISPLAY_WIDTH)
    overlay_2 = resize_to_width(overlay_2, DISPLAY_WIDTH)

    # Add titles to the two annotation panels.
    panel_1 = add_header(
        overlay_1,
        f"{ANNOTATOR_1_NAME}",
    )

    panel_2 = add_header(
        overlay_2,
        f"{ANNOTATOR_2_NAME}",
    )

    # Add a title to the original image.
    original_panel = add_header(
        original,
        f"ORIGINAL IMAGE | {image_id}",
    )

    # Each comparison panel has the same width.
    panel_width = max(
        original_panel.width,
        panel_1.width,
        panel_2.width,
    )

    # Add the legend to the bottom.
    content_height = max(panel_1.height, panel_2.height)

    canvas_width = (
        panel_width * 2
        + PANEL_GAP
        + OUTER_PADDING * 2
    )

    canvas_height = (
        original_panel.height
        + PANEL_GAP
        + content_height
        + LEGEND_HEIGHT
        + OUTER_PADDING * 2
    )

    canvas = Image.new(
        "RGB",
        (canvas_width, canvas_height),
        CANVAS_BACKGROUND,
    )

    # Center the original image across the top.
    original_x = (canvas_width - original_panel.width) // 2

    canvas.paste(
        original_panel,
        (original_x, OUTER_PADDING),
    )

    # Place annotation panels side by side.
    annotation_y = (
        OUTER_PADDING
        + original_panel.height
        + PANEL_GAP
    )

    left_x = OUTER_PADDING
    right_x = OUTER_PADDING + panel_width + PANEL_GAP

    canvas.paste(
        panel_1,
        (left_x, annotation_y),
    )

    canvas.paste(
        panel_2,
        (right_x, annotation_y),
    )

    # Add the legend underneath both annotations.
    legend = draw_legend(
        Image.new(
            "RGB",
            (canvas_width - OUTER_PADDING * 2, 1),
            CANVAS_BACKGROUND,
        )
    )

    legend_x = OUTER_PADDING
    legend_y = annotation_y + content_height

    canvas.paste(
        legend,
        (legend_x, legend_y),
    )

    # Save comparison.
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / f"{image_id}_comparison.png"

    canvas.save(output_path)

    print(f"  Saved: {output_path}")

    return output_path


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Compare two annotators' masks against original images."
        )
    )

    parser.add_argument(
        "--image-id",
        type=str,
        default=None,
        help="Process only one image ID, e.g. DJI_0000.",
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Project root directory. Defaults to the current directory.",
    )

    args = parser.parse_args()

    root = args.root.resolve()

    originals_dir = root / ORIGINALS_DIR
    annotator_1_dir = root / ANNOTATOR_1_DIR
    annotator_2_dir = root / ANNOTATOR_2_DIR
    output_dir = root / OUTPUT_DIR

    # Find annotation ZIP files.
    try:
        annotator_1_zips = find_zip_files(annotator_1_dir)
        annotator_2_zips = find_zip_files(annotator_2_dir)

    except FileNotFoundError as error:
        print(f"ERROR: {error}")
        sys.exit(1)

    # Match ZIP files using image IDs.
    annotator_1_by_id = {
        get_image_id_from_zip(path).lower(): path
        for path in annotator_1_zips
    }

    annotator_2_by_id = {
        get_image_id_from_zip(path).lower(): path
        for path in annotator_2_zips
    }

    shared_ids = sorted(
        set(annotator_1_by_id)
        & set(annotator_2_by_id)
    )

    if args.image_id:
        requested_id = args.image_id.lower()

        shared_ids = [
            image_id
            for image_id in shared_ids
            if image_id == requested_id
        ]

    if not shared_ids:
        print("No shared annotation ZIP files were found.")
        print(f"Annotator 1 ZIPs: {annotator_1_dir}")
        print(f"Annotator 2 ZIPs: {annotator_2_dir}")
        sys.exit(1)

    print(f"Found {len(shared_ids)} shared annotation ZIP(s).")
    print(f"Font size: {FONT_SIZE}px")
    print(f"Output directory: {output_dir}")
    print()

    successful = 0
    failed = 0

    for image_id in shared_ids:
        zip_1 = annotator_1_by_id[image_id]
        zip_2 = annotator_2_by_id[image_id]

        # Recover the original ID's original filename casing.
        actual_image_id = zip_1.stem

        original_path = find_original(
            actual_image_id,
            originals_dir,
        )

        if original_path is None:
            print(
                f"ERROR: No original image found for {actual_image_id}"
            )
            failed += 1
            continue

        try:
            create_comparison(
                image_id=actual_image_id,
                original_path=original_path,
                annotator_1_zip=zip_1,
                annotator_2_zip=zip_2,
                output_dir=output_dir,
            )

            successful += 1

        except Exception as error:
            print(f"ERROR processing {actual_image_id}: {error}")
            failed += 1

    print()
    print("=" * 50)
    print("COMPARISON COMPLETE")
    print("=" * 50)
    print(f"Successful: {successful}")
    print(f"Failed:     {failed}")
    print(f"Output:     {output_dir}")


if __name__ == "__main__":
    main()

