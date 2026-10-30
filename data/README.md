# Data

This directory contains selected field-image samples and annotation archives used by the project. The complete course dataset may be hosted separately; use the designated course storage location as the source of truth.

**Dataset access:** [Course Sciebo folder](https://hshl.sciebo.de/s/g2QCsQzRqABPYmd)

## Directory contents

| Path | Contents |
| --- | --- |
| `initial_inspection_samples/` | Selected original field images for initial inspection, plus `Initial_inspection_samples_manifest.xlsx`. |
| `individual_annotation_samples/` | Per-image examples containing original image archives and annotated batch archives. |
| `mutual_annotated_samples/` | Shared image annotation exports grouped by annotator list (`annot_list_1/` and `annot_list_2/`). |

## Data handling

- Preserve original recordings; perform annotation and processing on working copies.
- Keep image filenames/IDs consistent across originals, exports, manifests, and comparison outputs.
- Record provenance and any transformations applied to an image or mask.
- Do not commit the full dataset or restricted course material unless redistribution is explicitly permitted.
- Avoid committing credentials or private configuration.

See the README files in the individual sample directories for their local structure and the annotation class configuration.
