# Precision Farming — Autonomous Systems B

Team repository for the **Autonomous Systems B (ASB)** precision-farming project at Hochschule Hamm-Lippstadt.

The repository currently contains field-image samples, crop/weed annotation exports, annotation comparisons, course notebooks, and project documentation.

## Project at a glance

| Area | Contents |
| --- | --- |
| Data | Sample field images, manifests, and annotation archives |
| Annotation | CVAT and Label Studio exports |
| Analysis | Annotation comparison images and a Python comparison utility |
| Documentation | Lab guide, task log, and research paper |
| Notebooks | Course notebook and project record |

## Repository layout

| Path | Contents |
| --- | --- |
| `data/` | Image samples, individual annotation examples, and shared annotation sets. See [data/README.md](data/README.md). |
| `documentation/` | ADAS Lab 02 team guide, task log, and research paper. See [documentation/README.md](documentation/README.md). |
| `experiments/` | Selected CVAT and Label Studio exports, plus annotation comparison images. |
| `notebooks/` | Updated ADAS Lab 01 notebook and notebook documentation. |
| `utils/` | Python utility for comparing annotation masks and its dependencies. |
| `contribution.md` | Git branching, commit, and pull-request workflow. |
| `LICENSE` | Repository licensing information. |

## Annotation comparison utility

Install the dependencies from the repository root:

```bash
python -m pip install -r utils/requirements.txt
```

Run comparisons:

```bash
python utils/compare_annotations.py
```

To process one image:

```bash
python utils/compare_annotations.py --image-id DJI_0000
```

The script reads original images and matching annotator ZIP exports from the paths configured in `utils/compare_annotations.py`. It writes comparison images to `experiments/annotation_comparisons/`. See [utils/README.md](utils/README.md).

## Project documentation

- [ADAS Lab 02 Team Working Guide](documentation/ADAS_Lab_02_Team_Guide.md)
- [Task Log](documentation/TASK_LOG.md)
- [Notebook documentation](notebooks/Readme.md)
- [Contribution guide](contribution.md)

## Data

The repository contains selected samples and annotation artefacts; it may not contain the complete source dataset. The [data guide](data/README.md) links to the course storage location.

Some course data may be subject to access or redistribution restrictions.