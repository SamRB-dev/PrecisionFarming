# Utilities

Helper scripts for inspecting and comparing project annotations.

## Annotation comparison

`compare_annotations.py` creates a visual comparison of two annotators' segmentation masks against the original image. The output places the original image above the two annotation overlays.

### Requirements

Install dependencies from the repository root:

```bash
python -m pip install -r utils/requirements.txt
```

### Run

From the repository root:

```bash
python utils/compare_annotations.py
```

To compare one image ID:

```bash
python utils/compare_annotations.py --image-id DJI_0000
```

To specify a different project root:

```bash
python utils/compare_annotations.py --root /path/to/PrecisionFarming
```

### Inputs and output

| Path | Role |
| --- | --- |
| `data/initial_inspection_samples/` | Original images, matched by filename stem (image ID). |
| `data/mutual_annotated_samples/annot_list_1/` | First annotator's ZIP mask exports. |
| `data/mutual_annotated_samples/annot_list_2/` | Second annotator's ZIP mask exports. |
| `experiments/annotation_comparisons/` | Generated comparison PNGs. |

The script processes image IDs with a ZIP archive in both annotator directories and a matching original image. ZIPs must contain a supported image mask. The mask decoder recognises the configured RGB colours in `compare_annotations.py`; grayscale or indexed masks are interpreted as class-ID masks.

### Configuration

The global configuration section in `compare_annotations.py` contains annotator display names, class colours, font/layout settings, and input/output directories.

Unknown RGB colours are treated as background by the current decoder.

### Errors

The script reports missing input directories, missing original images, unmatched annotation ZIPs, and ambiguous mask files.

## Quantitative inter-annotator agreement (IoU)

`evaluate_annotations.py` calculates the class-wise Intersection over Union (IoU)
required by Work Package C of the lab notebook. It compares the independent
annotations **before adjudication**.

From the repository root:

```bash
python utils/evaluate_annotations.py
```

To evaluate one image pair:

```bash
python utils/evaluate_annotations.py --image-id DJI_0000
```

To use a different project root:

```bash
python utils/evaluate_annotations.py --root /path/to/PrecisionFarming
```

The script matches ZIP exports by filename stem in the two annotator directories
listed above. It supports single-channel/indexed masks containing IDs
`0`, `1`, `2`, and `255`, and RGB masks using the palette configured in
`compare_annotations.py`:

| ID | Class | RGB |
| ---: | --- | --- |
| 0 | Background | (0, 0, 0) |
| 1 | Sugar beet | (25, 77, 28) |
| 2 | Weed | (250, 50, 83) |
| 255 | Ignore | (115, 51, 128) |

For quantitative evaluation, the evaluator uses the agreed project palette
strictly. If either annotator's mask in an image pair contains an unknown RGB
colour, an invalid class ID, or dimensions that do not match, the entire image
pair is skipped. No pixels from a skipped pair contribute to IoU or ignore
statistics. Skipped image IDs and reasons are recorded in
`skipped_images.csv`. The evaluator does not resize masks.

### Metric and ignore handling

For each class (c):

```
IoU_c = intersection_c / union_c
```

Pixels are excluded from **all** class calculations if either annotator marks
the pixel as `255`. The excluded fraction is reported separately. Intersections
and unions are summed across all matched images first, and aggregate IoU is
then calculated from those pooled counts. Per-image IoUs are also reported for
inspection, but are not averaged to obtain the aggregate result. A zero union
is reported as `N/A`.

### Outputs

The results are written to `experiments/annotation_evaluation/`:

| File | Contents |
| --- | --- |
| `per_image_iou.csv` | Per-image IoU for each class, plus total/excluded pixel counts and excluded fraction. |
| `aggregate_iou.csv` | Pooled intersection, union and aggregate IoU for Background, Sugar beet and Weed. |
| `ignore_statistics.csv` | Dataset-level total, valid and excluded pixel counts and excluded fraction. |
| `iou_summary.txt` | Human-readable summary of evaluated/skipped pair counts, pooled results and method. |
| `skipped_images.csv` | Image IDs and reasons for image pairs excluded due to unknown colours, invalid class IDs, or dimension mismatches. |

The aggregate class-wise scores—not a mean of per-image scores and not overall
pixel accuracy—are the primary agreement results to report in the notebook.
