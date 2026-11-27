# Cross-Scenario Integration Review and Requirements Traceability

**Project:** Autonomous Agricultural Weed-Management System  
**Date:** 27 November 2026  
**Status:** Review completed; the models still need to be connected and tested together

## 1. What this review is about

We developed three scenarios separately, so I checked how they are supposed to work together and whether our requirements can be traced to the diagrams and UPPAAL models.

The main question was: **If we put the three scenarios together, do they already exchange the information they need?**

This is a review of the current models. It is **not** a claim that we have already built or verified one integrated UPPAAL model.

## 2. Files used for the review

I used the scenario guide, the three use case diagrams, the available UPPAAL models and the project Gantt chart.

- **Scenario 1:** `scenario_01.xml` on the main branch (`DroneSurvey`).
- **Scenario 2:** the Scenario 2 UPPAAL model (`ControlStation` and `Tractorr`), including `WaitingForClearPath` and 11 queries with saved successful results.
- **Scenario 3:** `scenario_03_communication_recovery.xml` on the main branch (`Tractor` and `ExternalEvents`).

The Scenario 2 XML was checked using the file shared for this review. The saved verification results were **not rerun independently**. All results described here apply to the standalone models.

## 3. How the scenarios should work together

The expected flow is straightforward:

1. The **drone (Scenario 1)** surveys the field and sends weed locations.
2. The **Control Station (Scenario 2)** uses that information to create and assign a removal task.
3. The **tractor (Scenario 2)** navigates to the target, checks it, removes the weed if it is valid, and reports the result.
4. If communication fails, **Scenario 3** should stop unsafe activity and manage reconnection and recovery before the tractor continues.

This flow makes sense in our diagrams. The main remaining problem is connecting the separate UPPAAL models so they actually behave this way.

## 4. What is connected and what is missing?

| Connection | What I found | What we still need |
|---|---|---|
| **Scenario 1 → Scenario 2** | Scenario 1 has a `send_weed_geolocation` state. Scenario 2 creates a task, but starts this on its own. | An event or shared information so a weed observation can trigger task creation. |
| **Control Station ↔ tractor (Scenario 2)** | `assign_task` and `report_result` already connect the two templates. | Keep these connections when we integrate the models. |
| **Scenario 2 ↔ Scenario 3** | Both models describe tractor behaviour, but use different templates and movement/tool variables. | Agree on how a communication failure stops the tractor that is executing the task. |
| **Task information** | Task creation and reporting are shown, but there is no shared task ID across the models. | Agree on a small set of task details and statuses needed for assignment and recovery. |

One important point: **putting the three templates into one XML file is not enough.** They also need to share the correct events and state. Otherwise, each scenario would still run separately.

## 5. Requirements traceability

I checked all **20 requirements** from the scenario guide: FR-01 to FR-09 and SR-01 to SR-11. The separate file `PrecisionFarming_Traceability_Matrix.csv` contains the requirement-by-requirement details.

The main results are:

| Area | What is covered | What is still limited |
|---|---|---|
| **Scenario 1 (FR-01–FR-03)** | Field validation, surveying and weed detection/location are represented. | The weed observation is not yet passed to Scenario 2 in UPPAAL. |
| **Scenario 2 (FR-04–FR-07)** | Assignment, navigation, target verification, removal and result reporting are modelled. | There is no shared task ID, duplicate-assignment check or partial-result outcome in the current XML. |
| **Scenario 2 safety (SR-01–SR-07)** | Obstacle stopping, tool interlock and target verification have modelled behaviour and saved successful queries. | Emergency stop, unreliable localization, unavailable safety data and invalid/expired commands are not fully modelled in Scenario 2. |
| **Scenario 3 (FR-08–FR-09, SR-08–SR-11)** | Communication loss, safe stopping, timeout and recovery checks are modelled. | The recovery behaviour is not yet connected to the Scenario 2 tractor/task state. |

**Important:** A function appearing in a use case diagram is not the same as it being verified in UPPAAL. I have kept that distinction in the traceability matrix.

## 6. Findings to follow up

| ID | Finding | Suggested next step | Status |
|---|---|---|---|
| **INT-01** | Scenario 1 does not send an event that Scenario 2 can receive. | Agree on a weed-observation handover. | Open |
| **INT-02** | Scenario 2 and 3 use different variables for tractor movement and tool activity. | Decide how both models will control the same tractor safely. | Open |
| **INT-03** | Task identity and status are not shared across scenarios. | Agree on the minimum task information needed. | Open |
| **INT-04** | Scenario 1 has a saved failed query for `A<> Process.end_survey`. | Check whether the project requires the survey to end on every possible path; adjust and rerun if needed. | Open |
| **INT-05** | Several detailed requirements are not implemented in the standalone Scenario 2 model. | Review which requirements still need implementation or verification in the integrated model. | Open — team decision needed |
| **UC-01** | Scenario 1 associates task generation with the drone instead of the Control Station. | Scenario 1 owner updates the use case diagram. | Pending |

### Note on the Scenario 1 query

In the Scenario 1 XML, `E<> Process.end_survey` has a saved successful result, but `A<> Process.end_survey` has a saved failed result. This means the model **can** reach the end of the survey, but it does not guarantee that it will do so on every path. Whether that needs fixing depends on what we want to prove.

## 7. A simple plan for integration

Before editing the models, the team should agree on a few shared signals and variables:

| Between | Possible approach | Why |
|---|---|---|
| **S1 → S2** | Weed-observation event and target/location information | So the Control Station knows when to create a task. |
| **Control Station → tractor** | Keep `assign_task`, with an agreed task status | So a task can be assigned only when appropriate. |
| **Tractor → Control Station** | Keep `report_result` and agree on result codes | So the Control Station can record the outcome. |
| **S3 → S2** | Shared communication status or loss/recovery event | So communication failure affects the tractor that is actually moving/removing weeds. |
| **Recovery → task execution** | Shared safety checks and permission to resume | So communication coming back does not automatically restart the tractor. |

These are **suggestions**, not changes already made. We should agree on the exact names and behaviour together before combining the XML files. In UPPAAL, normal channels need matching sender and receiver transitions, so the choice of communication method matters.

## 8. Conclusion and next steps

The integration and traceability **review is complete**. We know how the scenarios are meant to fit together, have checked the requirements against the existing evidence, and have listed the main gaps.

What is **not complete yet** is the actual integration of all three UPPAAL models. The team still needs to agree on the interfaces, connect the models, run simulations and verify the combined system.

For the next stage:

- **Scenario 1 owner:** correct UC-01, help define the weed-observation handover and review the failed survey-completion query.
- **Scenario 2 owner:** help define the task status and tractor safety signals.
- **Scenario 3 owner:** connect communication-loss and recovery behaviour to the Scenario 2 tractor.
- **Whole team:** agree on the shared interface, integrate the models and run new verification queries.

**Milestone note:** Cross-scenario integration review and traceability completed; implementation and combined verification still pending.
