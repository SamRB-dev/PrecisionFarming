# Utilities

Small helper scripts for inspecting and comparing project annotations.

## Annotation comparison

`compare_annotations.py` creates a visual comparison of two annotators' segmentation masks against the original image. The output layout places the original image above the two annotation overlays.

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

### Expected inputs and output

| Path | Role |
| --- | --- |
| `data/initial_inspection_samples/` | Original images, matched by filename stem (image ID). |
| `data/mutual_annotated_samples/annot_list_1/` | First annotator's ZIP mask exports. |
| `data/mutual_annotated_samples/annot_list_2/` | Second annotator's ZIP mask exports. |
| `experiments/annotation_comparisons/` | Generated comparison PNGs. |

The script processes only image IDs with a ZIP archive in both annotator directories and a matching original image. ZIPs are expected to contain a supported image mask. The mask decoder recognises the configured RGB colours in `compare_annotations.py`; grayscale or indexed masks are interpreted as class-ID masks.

### Configuration

Edit the global configuration section in `compare_annotations.py` to change annotator display names, class colours, font/layout settings, and input/output directories.

**Important:** Unknown RGB colours are treated as background by the current decoder. Ensure exported masks use the configured palette or a compatible class-ID representation before relying on the comparison output.

### Troubleshooting

- Run the script from the repository root, or pass `--root` explicitly.
- Confirm both annotation lists contain ZIP files with matching image IDs.
- Confirm a matching original image exists in `initial_inspection_samples/`.
- If a ZIP contains multiple candidate mask images, the script reports ambiguity rather than choosing one silently.
