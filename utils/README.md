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