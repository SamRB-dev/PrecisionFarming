# System modelling

## Directory convention

- `Requirements/`: system-level requirements diagrams. Preserve requirement IDs across scenario models.
- `scenario_01_field_survey_and_weed_detection/`: field survey and detection models.
- `scenario_02_task_coordination_and_weed_removal/`: tractor task coordination and treatment models.
- `scenario_03_communication_failure/`: communication-loss and recovery models.
- `uppaal/`: timed automata models and simulation traces.

## Scenario artefacts

| Scenario | Directory |
|---|---|
| SC-01 — Field survey and weed detection | [scenario_01_field_survey_and_weed_detection](scenario_01_field_survey_and_weed_detection/) |
| SC-02 — Task coordination and weed removal | [scenario_02_task_coordination_and_weed_removal](scenario_02_task_coordination_and_weed_removal/) |
| SC-03 — Communication failure | [scenario_03_communication_failure](scenario_03_communication_failure/) |

Each scenario directory should contain its activity diagram, use-case diagram, and scenario-specific requirement artefacts where available. Editable source files should be retained alongside rendered exports.

## Naming convention

Use lowercase snake_case, scenario prefix `scenario_01`, `scenario_02`, or `scenario_03`, and descriptive artifact suffixes such as `activity_diagram`, `use_case_diagram`, or `requirements_diagram`. Keep editable files (`.drawio`, JSON/model source) and rendered previews (`.png`) paired.
