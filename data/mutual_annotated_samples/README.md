# Shared Annotation Samples

This directory contains annotation ZIP exports for images annotated by two team members. The exports are grouped by annotator list.

## Contents

| Path | Contents |
| --- | --- |
| `annot_list_1/` | Annotation ZIP files for the shared image IDs. |
| `annot_list_2/` | Corresponding annotation ZIP files from the second annotation set. |

The image IDs currently represented in both lists are `DJI_0000`, `DJI_0004`, `DJI_0005`, `DJI_0008`, `DJI_0012`, `DJI_0021`, `DJI_0026`, `DJI_0030`, and `DJI_0033`.

## CVAT label colours

The following are the current class display colours. They are not, by themselves, a complete pixel-mask encoding specification.

| Label | Display colour | Intended class |
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