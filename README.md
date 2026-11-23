# Precision Farming — Autonomous Systems B

Team repository for the **Autonomous Systems B (ASB)** precision-farming project at Hochschule Hamm-Lippstadt.

The project explores autonomous systems in precision agriculture, with a focus on field observation, weed detection, task coordination, autonomous treatment, and safe recovery.

## Project status and timeline

The timeline below is the high-level project plan. The [detailed Gantt](documentation/project_management/GANTT.md) includes task owners, dates, status and evidence notes and is automatically refreshed by GitHub Actions.

```mermaid
gantt
    title Autonomous Systems B
    dateFormat YYYY-MM-DD
    axisFormat %d %b
    Task 1 dataset and annotation :done, 2026-10-27, 2026-11-06
    Scenario 3 modelling :done, 2026-11-09, 2026-11-12
    Scenario 2 modelling and UPPAAL :done, 2026-11-12, 2026-11-20
    Scenario 1 modelling and UPPAAL :done, 2026-11-23, 2026-11-23
    Integration and verification :2026-11-24, 2026-11-30
    Automated labeling and learning :2026-11-24, 2026-12-11
    Integrated autonomous vehicles and DL :2026-12-01, 2026-12-18
    Demo and competition preparation :2026-12-07, 2026-12-23
    Final documentation :2026-12-14, 2027-01-15
    Final review and submission :2027-01-21, 2027-01-25
```

<details>
<summary>Project tracking links</summary>

- [Detailed Gantt chart](documentation/project_management/GANTT.md)
- [Task log](documentation/TASK_LOG.md)
- [Milestone schedule source](documentation/project_management/milestones.csv)
- [Documentation index](documentation/README.md)

</details>

## Repository structure

| Directory | Contents |
|---|---|
| `data/` | Field data, samples, and annotation datasets |
| `documentation/` | Requirements, scenario models, UPPAAL models, task log, papers, project tracking |
| `experiments/` | Annotation exports, comparison artefacts and evaluation |
| `notebooks/` | Coursework and analysis notebooks |
| `utils/` | Reusable utilities |

## Contribution

See [contribution.md](contribution.md).
