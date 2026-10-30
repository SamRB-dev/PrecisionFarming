# Shared Annotation Samples

This directory contains annotation ZIP exports for images annotated by two team members. The current sets are grouped by annotator list.

## Contents

| Path | Contents |
| --- | --- |
| `annot_list_1/` | Annotation ZIP files for the shared image IDs. |
| `annot_list_2/` | The corresponding annotation ZIP files from the second annotation set. |

The image IDs currently represented in both lists are `DJI_0000`, `DJI_0004`, `DJI_0005`, `DJI_0008`, `DJI_0012`, `DJI_0021`, `DJI_0026`, `DJI_0030`, and `DJI_0033`.

## CVAT label colour configuration

Use the following label names and colours when configuring the corresponding CVAT project. The colour values are the current class display colours; they are not, by themselves, a complete pixel-mask encoding specification.

| Label | Display colour | Intended use |
| --- | --- | --- |
| Sugar beet | `#194d1c` | Sugar beet crop |
| Weed | `#fa3253` | Weed vegetation |
| Ignore | `#733380` | Uncertain or excluded region |

```json
[
  { "name": "sugar beet", "color": "#194d1c", "type": "any", "attributes": [] },
  { "name": "weed", "color": "#fa3253", "type": "any", "attributes": [] },
  { "name": "ignore", "color": "#733380", "type": "any", "attributes": [] }
]
```

Retain each export with its source image ID and annotator-list directory so that comparisons remain traceable.
