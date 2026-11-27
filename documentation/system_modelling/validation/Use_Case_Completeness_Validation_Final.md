# Use-Case Completeness Check

**Project:** Autonomous Agricultural Weed-Management System  
**Date:** 27 November 2026  
**Status:** Review completed; one point still needs to be corrected

## 1. What I checked

I looked at the use case diagrams for all three scenarios and compared them with the functional and safety requirements in our scenario guide. I mainly wanted to see whether the important functions are shown, whether the right components are responsible for them, and whether the three scenarios make sense together.

## 2. Results

| Scenario | Requirements checked | What I found | Result |
|---|---|---|---|
| **1 — Drone survey and weed detection** | FR-01 to FR-03 | Field configuration, surveying, image capture and finding weed locations are shown. There is one issue with who generates removal tasks. | Complete at a high level; one correction pending |
| **2 — Task coordination and weed removal** | FR-04 to FR-07; SR-01 to SR-07 | The diagram covers task assignment, validation, navigation, weed removal, reporting, obstacle handling and emergency stopping. | No change needed for this review |
| **3 — Communication failure and recovery** | FR-08 to FR-09; SR-08 to SR-11 | Communication loss, stopping, reconnection, timeout, recovery checks, resuming and operator intervention are shown. | No change needed for this review |

## 3. Issue found in Scenario 1

**UC-01 — Who creates the removal task?**

In the Scenario 1 diagram, **Generate Removal Tasks** is connected to the **Survey Drone**. However, **FR-04** says that the **Control Station** creates and assigns removal tasks. This is also how we have divided the work between Scenarios 1 and 2.

The Scenario 1 teammate should correct this. One option is to show **Send Weed Observation to Control Station** in Scenario 1 and leave task creation to Scenario 2. If the diagram is intended to show the whole system, the task-generation use case could instead be connected to the Control Station.

**Status:** Pending — to be checked again after the diagram is updated.

## 4. Do the scenarios fit together?

At the use-case level, the overall workflow makes sense:

**Scenario 1** finds weeds and provides their locations → **Scenario 2** creates and carries out removal tasks → **Scenario 3** handles communication interruptions and safe recovery when needed.

The only responsibility conflict found in the diagrams is UC-01. The technical connections between the UPPAAL models are checked separately in the integration review.

## 5. Conclusion

I have completed the use-case review for all three scenarios. The main functions are covered, and I do not see a reason to make the diagrams more complicated at this stage.

**One correction is still open:** the Scenario 1 diagram should show the correct responsibility for generating removal tasks. Once that is changed, I will check it again and close UC-01.

**Milestone note:** Use-case review completed; Scenario 1 correction pending.
