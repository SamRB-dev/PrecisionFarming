# Precision Farming — Autonomous Systems B

Repository for the **Autonomous Systems B (ASB)** precision-farming project. The current work focuses on Task 1: gathering and preparing field images, defining a consistent semantic-segmentation annotation protocol, reviewing annotations, and validating a documented dataset release.

## Task 1 objectives

- Inspect the assigned field-image recordings and document their properties.
- Select a representative subset and maintain a source-linked manifest.
- Define annotation rules for the four mask values: background (0), sugar beet (1), weed (2), and ignore/uncertain (255).
- Compare two annotation tools using a common image sample.
- Independently annotate a pilot, review the main annotations, and assess agreement using class-wise Intersection over Union (IoU).
- Validate the image-mask pairs and document the dataset and limitations.

## Repository layout

| Path | Purpose |
| --- | --- |
| `data/` | Data-location instructions and dataset organization notes. Follow course rules for restricted files; do not commit source images or annotations unless explicitly permitted. |
| `documentation/` | Annotation protocol, dataset description, findings, validation evidence, and task log. |
| `notebooks/` | Course notebook and reproducible exploratory or analysis notebooks. |
| `LICENSE` | Repository license information. |

## Task tracking

See [the Task Log](documentation/TASK_LOG.md) for task owners, dates, deadlines, and completion dates.

## Working principles

1. Keep the original source recordings unchanged.
2. Record unknown metadata as unknown; do not invent it.
3. Use the agreed class IDs consistently in all exported masks.
4. Keep a record of annotators, reviewers, guideline versions, and tool versions.
5. Do not report planned work as completed work. Update the task log when work is actually finished.
6. Follow the instructor's data-sharing and repository-access requirements.

## Current status

This repository is being organized for Task 1. Update this section as the team produces verified results; do not treat the checklist above as evidence that the work is complete.
