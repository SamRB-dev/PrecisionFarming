# ADAS Lab 02 --- Updated SysML and UPPAAL Scenario Guide

**System:** Autonomous Agricultural Weed-Management System\
**Team:** Three-person team; scenario ownership is agreed by the team.\
**Purpose:** Define the shared system baseline, model each assigned
scenario in SysML, and verify its timed behaviour in UPPAAL.

> **Scope note:** This guide is the team's working model baseline. The
> scenario split and proposed requirement wording are team design
> decisions, not claims that the course handout mandates these exact
> scenarios or requirement IDs. Confirm the final scope with the
> instructor/team.

------------------------------------------------------------------------

## 1. How to use this guide

Work on each scenario independently first, then integrate the models.
Each scenario owner should produce:

1.  Scenario description: purpose, actors, assumptions, preconditions,
    normal flow, and exception flow.
2.  SysML activity diagram: workflow, decisions, parallel actions, and
    exception paths.
3.  SysML sequence diagram: lifelines and time-ordered messages.
4.  SysML requirement diagram: scenario requirements and applicable
    relationships.
5.  UPPAAL model: timed automata, channels, shared variables, and
    clocks.
6.  Verification notes: exact queries, results, assumptions, and
    unresolved limitations.

Keep requirement IDs, message names, task identifiers, and state
meanings consistent across the team.

## 2. Shared system baseline

The system comprises these principal elements:

-   **Operator:** selects a registered field and authorizes/monitors the
    mission.
-   **Drone:** surveys the assigned field and captures observations.
-   **AI Detector:** analyses observations and identifies suspected weed
    targets.
-   **Control Station:** stores field/task information, creates and
    assigns tasks, tracks outcomes, and coordinates recovery.
-   **Autonomous Tractor:** receives tasks, navigates to targets,
    verifies the treatment area, and operates its configured
    weed-removal mechanism.
-   **Safety/Localization functions:** provide obstacle, localization,
    command-validity, and emergency-stop information.

The exact weed-removal technology is deliberately left open: the
requirement says "configured weed-removal mechanism" and does not assume
a particular mechanical or spraying implementation.

### 2.1 Functional requirements baseline

The following functional requirements are the shared system-level
baseline. Scenario owners should allocate the applicable requirements to
their own models rather than copy every requirement into every scenario.

  -----------------------------------------------------------------------
  ID                      Requirement             Summary
  ----------------------- ----------------------- -----------------------
  FR-01                   Select and validate     Select a registered
                          field                   field and provide its
                                                  validated boundary to
                                                  the drone.

  FR-02                   Survey assigned field   Drone surveys the
                                                  assigned field and
                                                  collects observations.

  FR-03                   Identify and geolocate  Identify suspected
                          weeds                   weeds and record field
                                                  ID and geographic
                                                  location.

  FR-04                   Create and assign task  Control Station creates
                                                  a task ID/target from
                                                  an observation and
                                                  assigns it to an
                                                  available tractor.

  FR-05                   Navigate and remove     Tractor validates the
                          weed                    task, navigates to the
                                                  target, verifies the
                                                  treatment area, and
                                                  performs weed removal.

  FR-06                   Report task outcome     Tractor reports
                                                  completed, partial, or
                                                  failed; Control Station
                                                  records the status.

  FR-07                   Prevent duplicate       Prevent concurrent
                          assignment              duplicate assignment;
                                                  mission completes only
                                                  when all tasks have
                                                  terminal outcomes.

  FR-08                   Detect communication    Detect and record loss
                          loss                    of communication
                                                  between Control Station
                                                  and tractor.

  FR-09                   Reconcile after         After recovery,
                          recovery                reconcile task status
                                                  and require valid
                                                  current commands and
                                                  safety checks before
                                                  resuming.
  -----------------------------------------------------------------------

### 2.2 Functional requirements diagram

The diagram below is embedded as Mermaid source so it can be rendered in
Markdown viewers that support Mermaid. It represents the same
requirement hierarchy and IDs as the team's Functional Requirements
diagram.

``` mermaid
flowchart TB
    SYS["«requirement» SYS-REQ-01<br/><b>Autonomous agricultural weed-management system</b><br/>Survey the field, identify weeds, dispatch a tractor for removal, and report mission outcomes."]

    SC1["«requirement» SC-01<br/><b>Field survey &amp; weed detection</b><br/>Survey the assigned field and generate geolocated weed observations."]
    SC2["«requirement» SC-02<br/><b>Task coordination &amp; weed removal</b><br/>Assign weed targets to a tractor and execute removal tasks."]
    SC3["«requirement» SC-03<br/><b>Communication &amp; recovery</b><br/>Detect communication loss, preserve task state, and coordinate safe recovery."]

    FR01["FR-01<br/>Select and validate field"]
    FR02["FR-02<br/>Survey assigned field"]
    FR03["FR-03<br/>Identify and geolocate weeds"]
    FR04["FR-04<br/>Create and assign task"]
    FR05["FR-05<br/>Navigate and remove weed"]
    FR06["FR-06<br/>Report task outcome"]
    FR07["FR-07<br/>Prevent duplicate assignment"]
    FR08["FR-08<br/>Detect communication loss"]
    FR09["FR-09<br/>Reconcile after recovery"]

    SYS --> SC1
    SYS --> SC2
    SYS --> SC3
    SC1 --> FR01
    SC1 --> FR02
    SC1 --> FR03
    SC2 --> FR04
    SC2 --> FR05
    SC2 --> FR06
    SC2 --> FR07
    SC3 --> FR08
    SC3 --> FR09

    classDef root fill:#dceaf4,stroke:#173f5f,color:#102a43,stroke-width:2px;
    classDef parent fill:#eaf2f8,stroke:#315a78,color:#17324d,stroke-width:1.5px;
    classDef child fill:#ffffff,stroke:#526575,color:#172b3a;
    class SYS root;
    class SC1,SC2,SC3 parent;
    class FR01,FR02,FR03,FR04,FR05,FR06,FR07,FR08,FR09 child;
```

**Relationship note:** The arrows above communicate the visual
parent/child decomposition used in the requirements hierarchy. In the
SysML model, choose the relationship type that matches the modelling
intent and your course convention. Do not label every decomposition
connector `«deriveReqt»` automatically: `«deriveReqt»` means the client
requirement is derived from the supplier requirement through analysis;
it is not simply a generic tree connector.

## 3. Safety requirements baseline

These are the current agreed safety requirements. The communication
branch uses the team's **Reconnect State** and **Timeout State**
concept.

  -----------------------------------------------------------------------
  ID                      Requirement             Summary
  ----------------------- ----------------------- -----------------------
  SR-01                   Obstacle/person         Stop when an obstacle
                          protection              or person is detected
                                                  within the defined
                                                  safety zone.

  SR-02                   Tool interlock          Weed-removal mechanism
                                                  shall not activate
                                                  while the tractor is
                                                  moving.

  SR-03                   Target verification     Activate the mechanism
                                                  only after the target
                                                  and treatment area are
                                                  verified.

  SR-04                   Field-boundary          Remain within the
                          containment             authorized field and
                                                  stop if localization
                                                  becomes unreliable.

  SR-05                   Safe state on           Enter a defined safe
                          unavailable data        state when
                                                  safety-critical data
                                                  are unavailable or
                                                  unreliable.

  SR-06                   Emergency stop          Emergency stop shall
                                                  halt tractor motion and
                                                  disable the
                                                  weed-removal mechanism.

  SR-07                   Command validation      Reject invalid,
                                                  expired, or
                                                  unauthorized commands.

  SR-08                   Communication-loss      Detect when
                          detection               communication with the
                                                  Control Station is lost
                                                  or unreliable.

  SR-09                   Reconnect State         On communication loss,
                                                  stop movement,
                                                  deactivate the weeding
                                                  mechanism, and attempt
                                                  reconnection.

  SR-10                   Timeout State           If reconnection fails
                                                  within the defined
                                                  timeout, remain stopped
                                                  and store the failure
                                                  event.

  SR-11                   Safe operation          After communication
                          resumption              returns, synchronize
                                                  task status and verify
                                                  safety conditions
                                                  before resuming.
  -----------------------------------------------------------------------

### 3.1 Communication recovery behaviour

Use this as the agreed behavioural interpretation when creating
activity, sequence, state-machine, and UPPAAL models:

1.  **Normal operation:** tractor performs a valid assigned task.
2.  **Communication loss:** tractor detects lost or unreliable
    communication.
3.  **Reconnect State:** tractor stops movement, disables the
    weed-removal mechanism, and attempts reconnection.
4.  **Recovery check:** once communication returns, the system
    synchronizes task status and checks that the task/command is still
    valid and safety conditions are satisfied.
5.  **Resume:** the tractor resumes only after those checks pass.
6.  **Timeout State:** if the defined reconnection timeout/retry limit
    is reached, the tractor remains stopped, keeps the mechanism
    disabled, and stores the failure event locally.
7.  **Failure reporting:** because the link is unavailable during the
    timeout, the event is transmitted to the Control Station when
    communication becomes available again.

**Do not model "communication restored" as an immediate restart
trigger.** Restoration permits recovery checks; it does not by itself
authorize movement or tool activation.

The timeout duration, retry policy, and whether an operator must
authorize recovery are design parameters to agree and document. Do not
invent numeric values without an agreed source.

## 4. Shared state vocabulary

Use the following meanings consistently. Add scenario-specific states
when needed.

  -----------------------------------------------------------------------
  State                               Meaning
  ----------------------------------- -----------------------------------
  `Idle`                              No active task; ready or waiting.

  `Monitoring`                        Drone is collecting observations.

  `DetectionPending`                  Observation is being analysed.

  `TargetReported`                    Weed observation with
                                      field/location information has been
                                      sent to the Control Station.

  `TaskCreated`                       Control Station has created a task
                                      ID and target.

  `WaitingForAck`                     Sender is waiting for task
                                      acknowledgement.

  `Navigating`                        Tractor is moving toward a target.

  `ObstacleDetected`                  An obstacle/person condition has
                                      been detected.

  `Stopped`                           Tractor motion is halted pending
                                      safe conditions or instruction.

  `VerifyingTarget`                   Tractor is checking the target and
                                      treatment area.

  `ExecutingTask`                     Tractor is performing weed removal.

  `Reporting`                         Tractor is sending a task outcome.

  `Reconnect`                         Communication is
                                      unavailable/unreliable; tractor is
                                      stopped, tool disabled, and
                                      reconnection is attempted.

  `Timeout`                           Reconnection deadline/retry limit
                                      was reached; tractor remains
                                      stopped and failure is stored
                                      locally.

  `RecoveryCheck`                     Communication is back; task state
                                      and safety conditions are being
                                      checked.

  `Completed`                         Task is complete and its outcome
                                      has been reported/recorded.

  `Failed`                            Task cannot continue or a defined
                                      timeout/failure outcome has been
                                      reached.
  -----------------------------------------------------------------------

In UPPAAL, locations are states; transitions carry events, guards,
synchronisations, and updates. Use clocks for defined time bounds. Every
timeout must have an explicit outcome.

------------------------------------------------------------------------

## 5. Scenario 1 --- Drone survey, weed detection, and tractor removal

**Owner:** Team member working on the weed-management scenario.

### Goal and actors

Model the end-to-end workflow from field selection and drone survey
through weed target generation, tractor task assignment, weed removal,
and task reporting. Include the agreed communication-loss recovery
behaviour where it affects the scenario boundary.

**Actors/components:** Operator, Drone, AI Detector, Control Station,
Autonomous Tractor, obstacle/localization and safety functions.

### Assumptions to document

-   The field is registered and its boundary can be validated.
-   The drone and tractor are available and have the required
    permissions/resources.
-   Weed detection produces a suspected target with a field identifier
    and geographic location; the model abstracts image-processing
    accuracy.
-   The tractor's removal mechanism is configured, but its physical
    implementation is outside this behavioural model unless the team
    chooses to model it.
-   Safety-zone dimensions, localization thresholds, communication
    timeout, and retry count are parameters to be agreed rather than
    guessed.

### Normal flow

1.  Operator selects a registered field.
2.  System validates the field boundary and assigns the field to the
    drone.
3.  Drone surveys the field and collects observations.
4.  AI Detector analyses observations.
5.  For each suspected weed, the system records the field ID and
    geographic location.
6.  Control Station creates a unique task ID and target.
7.  Control Station checks tractor availability and assigns the task
    without creating a concurrent duplicate assignment.
8.  Tractor validates the task and navigates to the target.
9.  Tractor verifies the target and treatment area.
10. Tractor performs weed removal using its configured mechanism.
11. Tractor reports `completed`, `partial`, or `failed`.
12. Control Station records the outcome and updates mission status.
13. Mission is complete only when all generated tasks have terminal
    outcomes.

### Exception and safety flows

-   **No weed detected:** no removal task is created for that
    observation; survey continues or ends according to mission policy.
-   **Invalid/unavailable task:** tractor rejects the task and reports
    the reason.
-   **Obstacle/person detected:** tractor stops; it resumes navigation
    only when the path is safe.
-   **Unreliable localization or safety-critical data:** tractor enters
    the defined safe state.
-   **Communication loss:** follow `Reconnect` → `RecoveryCheck` →
    resume, or `Timeout`. On loss, motion stops and the mechanism is
    disabled.
-   **Timeout:** tractor remains stopped, stores the failure event, and
    reports it when communication returns.
-   **Task outcome missing:** Control Station must not mark the task
    complete without a valid report.

### SysML activity diagram

Suggested action flow:

`Select field` → `Validate boundary` → `Assign field to drone` →
`Survey field` → `Analyse observation` → decision `Suspected weed?`

-   **No:** continue survey or finish survey.
-   **Yes:** `Record field ID and location` → `Create task ID/target` →
    `Assign tractor` → `Validate task` → decision `Task accepted?`
    -   **No:** `Record rejection/failure`.
    -   **Yes:** `Navigate to target` → decision
        `Obstacle/person detected?`
        -   **Yes:** `Stop` → `Wait until path safe` → return to
            navigation.
        -   **No:** continue. → `Verify target/treatment area` →
            `Perform weed removal` → `Report outcome` →
            `Update task status`.

Add an interrupt/exception path for communication loss:
`Communication lost` → `Stop and disable mechanism` → `Reconnect State`
→ decision `Reconnected before timeout?` - **Yes:**
`Synchronize task status` → `Validate task and safety conditions` →
decision `Safe to resume?` → resume only if yes. - **No:**
`Timeout State` → `Remain stopped and store failure` → report failure
when communication is restored.

Use swimlanes for Operator, Drone, AI Detector, Control Station, and
Tractor. Safety functions can be a separate lane or represented as
signals/guards.

### SysML sequence diagram

Suggested lifelines: `Operator`, `Drone`, `AI_Detector`,
`ControlStation`, `Tractor`, and optionally `Safety/Localization`.

Suggested messages:

-   `Operator -> ControlStation: selectField(fieldId)`
-   `ControlStation -> Drone: assignSurvey(fieldId, boundary)`
-   `Drone -> AI_Detector: observation(image, location, fieldId)`
-   `AI_Detector -> ControlStation: weedDetected(fieldId, location, confidence)`
-   `ControlStation -> Tractor: assignTask(taskId, target)`
-   `Tractor -> ControlStation: taskAck(taskId, accepted/rejected)`
-   `Tractor -> Safety/Localization: requestTargetAndSafetyCheck`
-   `Tractor -> ControlStation: taskStatus(taskId, status)`
-   `Tractor -> ControlStation: taskResult(taskId, completed/partial/failed)`
-   `ControlStation -> Operator: missionStatus(status)`

Use `alt` fragments for weed/no-weed, task accepted/rejected,
obstacle/no-obstacle, and communication restored/timeout. Use `loop` for
repeated observations/targets. Use an `alt` or interruptible fragment
for communication loss during tractor operation. Exact message payloads
are implementation-level choices; keep message names and directions
consistent with UPPAAL channels.

### Scenario requirements and traceability

Use the system requirement IDs above as the baseline. Create
scenario-specific requirements only where the scenario needs detail not
already captured by FR/SR requirements. Avoid duplicate requirements
with different IDs. For each requirement, identify: - the
activity/sequence/state-machine element that realises it; - the UPPAAL
property or test that checks it, where applicable; - any assumption
needed for the property.

### UPPAAL model

Suggested templates:

-   `Operator` (optional if field selection is abstracted as an initial
    input).
-   `Drone` --- survey/observation.
-   `Detector` --- abstract issue/no-issue result.
-   `ControlStation` --- field assignment, target/task creation, task
    tracking.
-   `Tractor` --- task validation, navigation, obstacle response,
    weeding, communication recovery.

Suggested Tractor locations:

`Idle` → `ValidatingTask` → `Navigating` → `VerifyingTarget` →
`ExecutingTask` → `Reporting` → `Completed`.

Include branches: - invalid task → `Failed`; - obstacle → `Stopped` →
`Navigating` after safe-path condition; - communication loss →
`Reconnect` → (`RecoveryCheck` → resume appropriate prior activity) or
`Timeout`; - timeout → remain stopped, tool disabled, failure
stored/reported later.

Suggested variables include `taskValid`, `obstacle`, `moving`,
`actuatorOn`, `commUp`, `taskStatusValid`, `localizationValid`,
`targetVerified`, and `failureStored`. Use a clock such as `tReconnect`
for the agreed communication timeout.

Candidate properties (adapt names and syntax to the actual UPPAAL
templates):

-   `A[] not (moving && actuatorOn)` --- tractor never moves while the
    weeding mechanism is active.
-   `A[] (Tractor.ExecutingTask imply targetVerified)` --- weed removal
    only occurs after target verification.
-   `A[] (Tractor.Timeout imply (!moving && !actuatorOn))` --- timeout
    state is stopped with mechanism disabled.
-   `A[] (Tractor.Reconnect imply (!moving && !actuatorOn))` ---
    reconnect state is stopped with mechanism disabled.
-   `A[] (Tractor.Operating imply commUp && taskStatusValid)` ---
    operation only occurs with valid communication/task state, if this
    is the agreed operational policy.
-   Check that an accepted task reaches `Completed` or a defined
    `Failed` outcome under stated fairness/environment assumptions.

Do not claim UPPAAL verifies physical sensor accuracy,
weed-classification accuracy, or real-world braking performance. It
verifies the abstract model and its stated timing/logic assumptions.

------------------------------------------------------------------------

## 6. Scenario 2 --- Friend's assigned agricultural task

**Owner:** Team member handling the separate task.

Keep this scenario independent until its actual objective and scope are
agreed. Do not assume it is identical to Scenario 1 or copy Scenario 1's
workflow.

The owner should fill in:

-   **Scenario title and goal**
-   **Actors/components**
-   **Preconditions and assumptions**
-   **Normal flow**
-   **Exception/timeout flow**
-   **Relevant FR/SR IDs**
-   **SysML activity diagram**
-   **SysML sequence diagram**
-   **Scenario-specific requirements**
-   **UPPAAL templates, locations, clocks, channels, and properties**

Reuse shared system vocabulary and interfaces where appropriate. If the
friend's scenario uses a ground vehicle, align meanings of `Stopped`,
`Completed`, `Failed`, `Reconnect`, and `Timeout` with this guide.

------------------------------------------------------------------------

## 7. Optional coordinated pause/resume scenario

If the team still needs a third scenario, a separate coordination
scenario can model an Operator pausing and resuming two vehicles.

Core rule: the Control Station must not report the overall system as
`Paused` until both vehicles have confirmed a safe stop. A missing
acknowledgement must lead to an explicit timeout/failure outcome. A
vehicle must not resume without a valid resume command.

This scenario is optional until the team confirms that it is still part
of the agreed scope.

------------------------------------------------------------------------

## 8. UPPAAL modelling checklist

For each scenario:

-   [ ] List each automaton and what it represents.
-   [ ] Draw locations before adding transitions.
-   [ ] Declare shared variables and channels consistently.
-   [ ] Label transitions with events, guards, synchronisations, and
    updates.
-   [ ] Add clocks only for meaningful time bounds.
-   [ ] Include normal, exception, and timeout paths.
-   [ ] Define the outcome of every timeout.
-   [ ] State assumptions needed for liveness (for example, that a path
    eventually becomes clear).
-   [ ] Run verification and record exact properties/results.
-   [ ] Inspect counterexamples when a property fails; revise the model
    or explain the assumption/property issue.

Query examples are patterns, not guaranteed copy-paste queries. Adapt
them to actual template/location/variable names and the UPPAAL version:

-   `A[] not (moving && actuatorOn)` --- no simultaneous motion and tool
    activation.
-   `A[] not deadlock` --- no reachable deadlock, if terminal deadlock
    is not intended.
-   `E<> ControlStation.Completed` --- there exists a path to
    completion; this does not prove all executions complete.
-   `A<> (Completed || Failed)` --- every execution eventually reaches a
    terminal outcome; use only when model assumptions support it.

------------------------------------------------------------------------

## 9. Suggested project structure

``` text
docs/
  ADAS_Lab02_Updated_Scenario_Guide.md
  scenario-1-weed-detection-removal.md
  scenario-2-friends-task.md
sysml/
  scenario-1/
    activity.*
    sequence.*
    requirements.*
  scenario-2/
    activity.*
    sequence.*
    requirements.*
uppaal/
  scenario-1.xml
  scenario-2.xml
  integrated-system.xml
```

Each scenario document should include purpose, actors, assumptions,
normal/exception flows, state definitions, diagram references, UPPAAL
properties/results, and open questions.

## 10. Team integration review

Before integrating:

1.  Do all scenarios use the same meaning for `Stopped`, `Completed`,
    and `Failed`?
2.  Are `Reconnect`, `Timeout`, and recovery rules represented
    consistently wherever communication recovery applies?
3.  Are message names and task/request IDs consistent?
4.  Does each requirement map to model elements and a verification check
    where applicable?
5.  Are timeouts and recovery paths explicit?
6.  Can a teammate understand each diagram without verbal explanation?
7.  Are assumptions and unverified physical behaviours documented?

### Integration sequence

1.  Complete and verify each scenario independently.
2.  Compare interfaces, state meanings, requirement IDs, and
    assumptions.
3.  Connect one interaction at a time in the integrated UPPAAL model.
4.  Verify after each integration step.
5.  Preserve individual scenario models for debugging.
6.  Commit the integrated model, verification results, and a short note
    describing assumptions and limitations.
