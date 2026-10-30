# Precision Farming — Autonomous Systems B

Team repository for the **Autonomous Systems B (ASB)** precision-farming project at Hochschule Hamm-Lippstadt.

The project currently covers field-image inspection, crop/weed annotation, annotation-tool evaluation, and the broader ADAS Lab 02 work on agricultural use cases, automated labelling/learning, and an integrated autonomous-system solution.

## Project at a glance

| Area | What is here |
| --- | --- |
| Data preparation | Sample field images, image manifests, and annotation archives |
| Annotation | CVAT and Label Studio exports for selected images |
| Analysis | Annotation comparison visualisations and a Python comparison utility |
| Documentation | Lab guidance, task tracking, and the PhenoBench reference paper |
| Notebooks | Course notebook and project analysis record |

## Repository layout

| Path | Contents |
| --- | --- |
| `data/` | Image samples, individual annotation examples, and shared annotation sets. See [data/README.md](data/README.md). |
| `documentation/` | ADAS Lab 02 team guide, task log, and research paper. See [documentation/README.md](documentation/README.md). |
| `experiments/` | Selected CVAT and Label Studio exports, plus visual comparisons of annotations. |
| `notebooks/` | The updated ADAS Lab 01 notebook and notebook-specific guidance. |
| `utils/` | Python utility for comparing annotation masks and its dependencies. |
| `contribution.md` | Branching, commit, and pull-request workflow. |
| `LICENSE` | Repository licensing information. |

## Getting started

1. Read the [contribution guide](contribution.md) and work on a feature/task branch rather than committing directly to `main`.
2. Review the [data guide](data/README.md) before accessing or adding image files.
3. Check the [notebook guide](notebooks/Readme.md) for the course notebook.
4. Use the [task log](documentation/TASK_LOG.md) to see the current work allocation and deadlines.

### Compare annotation exports

From the repository root, install the utility dependencies and run the comparison script:

```bash
python -m pip install -r utils/requirements.txt
python utils/compare_annotations.py
```

To process one image only:

```bash
python utils/compare_annotations.py --image-id DJI_0000
```

The script expects the original images and both annotators' ZIP exports in the paths configured in `utils/compare_annotations.py`. It writes comparison images to `experiments/annotation_comparisons/`. See [utils/README.md](utils/README.md) for details.

## Project documentation

- [ADAS Lab 02 Team Working Guide](documentation/ADAS_Lab_02_Team_Guide.md) — requirements, recommended work packages, and review checklists.
- [Task Log](documentation/TASK_LOG.md) — owners, work packages, and deadlines.
- [Notebook documentation](notebooks/Readme.md) — scope and handling of the course notebook.
- [Contribution guide](contribution.md) — Git workflow and pull-request process.

## Data and reproducibility

The repository contains selected samples and annotation artefacts, not necessarily the complete source dataset. Check the data guide and the designated course storage location for the authoritative dataset. Do not add restricted data, credentials, or large source recordings without approval.

Keep image IDs and source provenance traceable. Document annotation conventions, tool/export settings, and any processing steps needed to reproduce an analysis.

## Status

Work is tracked in [documentation/TASK_LOG.md](documentation/TASK_LOG.md). Update the task log and relevant documentation as work is completed; do not treat planned work as completed.
