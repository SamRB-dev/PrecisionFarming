# ADAS Lab 02 --- Three-Scenario SysML and UPPAAL Guide

**System:** Autonomous Agricultural Weed-Management System\
**Team:** Three-person team\
**Purpose:** Define three complementary scenarios, model each in SysML,
and verify their timed behaviour in UPPAAL.

> **Scope note:** The three scenarios below are the team's working
> decomposition of the autonomous weed-management system. They are
> proposed modelling scenarios, not a claim that the course handout
> mandates these exact scenarios or diagram types. Confirm final scope
> with the instructor/team.

------------------------------------------------------------------------

# 1. Shared system baseline

## 1.1 System overview and actors

The system surveys an assigned agricultural field, detects and
geolocates suspected weeds, creates and assigns removal tasks to an
autonomous tractor, performs weed removal, and handles communication
failures safely.

Principal actors/components:

-   **Operator:** selects a registered field and monitors the mission.
-   **Drone:** surveys the assigned field and captures observations.
-   **AI Detector:** analyses observations and identifies suspected weed
    targets.
-   **Control Station:** validates field data, creates and assigns
    tasks, tracks task outcomes, and coordinates recovery.
-   **Autonomous Tractor:** validates assigned tasks, navigates to
    targets, verifies treatment areas, and operates its configured
    weed-removal mechanism.
-   **Safety/Localization functions:** provide obstacle, localization,
    command-validity, and emergency-stop information.

The physical weed-removal technology is not fixed. The models use the
term **configured weed-removal mechanism** and do not assume a specific
mechanical or spraying implementation.

## 1.2 Functional requirements baseline

These are the current system-level Functional Requirements. Scenario
models should trace to the applicable IDs rather than redefine the same
system requirement under new IDs.

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

## 1.3 Functional requirements diagram

The hierarchy below is embedded in the guide as Mermaid source. It uses
the final requirement IDs and parent/child grouping from the team's
Functional Requirements diagram.

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

**Relationship note:** The Mermaid arrows show the requirement hierarchy
visually. In the formal SysML model, use the relationship type that
matches the modelling intent and course convention. `«deriveReqt»` means
one requirement is derived from another through analysis; it is not a
generic label for every parent/child connector.

## 1.4 Safety requirements baseline

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

## 1.5 Shared communication recovery behaviour

Use the following behaviour consistently in scenarios where tractor
communication is in scope:

1.  **Normal operation:** tractor performs a valid assigned task.
2.  **Communication loss:** tractor detects lost or unreliable
    communication.
3.  **Reconnect State:** tractor stops movement, disables the
    weed-removal mechanism, and attempts to reconnect.
4.  **Recovery check:** when communication returns, synchronize task
    status and verify that the task/command remains valid and safety
    conditions pass.
5.  **Resume:** resume only after those checks pass.
6.  **Timeout State:** if the defined reconnection timeout/retry limit
    is reached, remain stopped, keep the mechanism disabled, and store
    the failure event locally.
7.  **Failure report:** transmit the stored failure event when
    communication becomes available again.

Communication restoration alone must **not** cause immediate resumption.
It enables recovery checks; it does not itself authorize movement or
tool activation.

The timeout duration, retry policy, and whether an operator must
authorize recovery are design parameters to agree and document. Do not
invent numeric values without an agreed source.

## 1.6 Shared state vocabulary

  -----------------------------------------------------------------------
  State                               Meaning
  ----------------------------------- -----------------------------------
  `Idle`                              No active task; ready or waiting.

  `Monitoring`                        Drone is collecting observations.

  `DetectionPending`                  Observation is being analysed.

  `TargetReported`                    Weed observation and field/location
                                      information have been sent to the
                                      Control Station.

  `TaskCreated`                       Control Station has created a task
                                      ID and target.

  `WaitingForAck`                     Sender is waiting for task
                                      acknowledgement.

  `Navigating`                        Tractor is moving toward a target.

  `ObstacleDetected`                  Obstacle/person condition has been
                                      detected.

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

# 2. Scenario 1 --- Drone field survey and weed detection

**Scenario focus:** field selection, drone survey, weed identification,
geolocation, and delivery of weed observations to the Control Station.

**Primary requirement traceability:** FR-01, FR-02, FR-03.\
**Related safety considerations:** SR-04 and SR-05 where
boundary/localization or unreliable data affect the survey.

## 2.1 Goal and actors

Model how an operator assigns a registered field to the drone, the drone
surveys it, and the AI Detector identifies and reports suspected weeds
with their geographic locations.

Actors/components: Operator, Control Station, Drone, AI Detector.

## 2.2 Preconditions and assumptions

-   The field is registered in the system.
-   The field boundary can be validated and supplied to the drone.
-   The drone is available and has sufficient resources to perform the
    assigned survey.
-   The detector returns a suspected-weed result and associated
    location; image-processing accuracy is abstracted.
-   Localization and observation quality are assumed to be available
    unless an exception is explicitly modelled.

## 2.3 Normal flow

1.  Operator selects a registered field.
2.  Control Station validates the field record and boundary.
3.  Control Station assigns the field and boundary to the drone.
4.  Drone begins surveying the assigned field.
5.  Drone captures observations with geographic/location metadata.
6.  AI Detector analyses each observation.
7.  If a suspected weed is detected, the detector records the field ID
    and geographic location.
8.  AI Detector sends the weed observation to the Control Station.
9.  Control Station stores the observation for task generation.
10. Drone continues surveying until the assigned field coverage is
    complete.
11. Control Station records the survey outcome.

## 2.4 Exception flows

-   **Invalid field/boundary:** reject the survey assignment and report
    the validation failure.
-   **No weed detected:** store the observation/negative result as
    appropriate and continue surveying; do not create a weed-removal
    target from a negative detection.
-   **Unreliable localization or observation data:** do not publish an
    untrusted target as a valid weed location; record/raise the
    data-quality condition.
-   **Survey interrupted:** record the incomplete survey state so it is
    not incorrectly reported as fully completed.

## 2.5 SysML activity diagram

Suggested flow:

`Select registered field` → `Validate field and boundary` → decision
`Field valid?`

-   **No:** `Reject survey assignment` → `Report validation failure`.
-   **Yes:** `Assign field to drone` → `Survey field` →
    `Capture observation` → `Analyse observation` → decision
    `Suspected weed detected?`
    -   **No:** continue survey.
    -   **Yes:** `Record field ID and geographic location` →
        `Send weed observation to Control Station` →
        `Store target observation`.

After coverage is complete: `Report survey outcome` → final.

Use swimlanes for Operator, Control Station, Drone, and AI Detector. Add
a loop for repeated observations and a decision for field coverage
complete.

## 2.6 SysML sequence diagram

Suggested lifelines: `Operator`, `ControlStation`, `Drone`,
`AI_Detector`.

Suggested messages:

-   `Operator -> ControlStation: selectField(fieldId)`
-   `ControlStation -> ControlStation: validateFieldBoundary(fieldId)`
-   `ControlStation -> Drone: assignSurvey(fieldId, boundary)`
-   `Drone -> AI_Detector: observation(image, location, fieldId)`
-   `AI_Detector -> AI_Detector: analyseObservation()`
-   `AI_Detector -> ControlStation: weedDetected(fieldId, location, confidence)`
-   `ControlStation -> ControlStation: storeWeedObservation()`
-   `Drone -> ControlStation: surveyStatus(fieldId, coverageStatus)`
-   `ControlStation -> Operator: surveyOutcome(status)`

Use `loop` for repeated observations and `alt` for weed detected/no weed
detected and valid/invalid field. Do not imply that confidence
thresholds or detection accuracy have been specified unless the team
defines them.

## 2.7 Scenario-specific requirement candidates

Use the system-level IDs as the baseline. Add scenario-specific
requirements only if additional detail is required, for example:

-   `S1-REQ-01`: The Control Station shall provide the drone with the
    validated boundary of the selected registered field.
-   `S1-REQ-02`: Each reported suspected weed observation shall include
    its field identifier and geographic location.
-   `S1-REQ-03`: The system shall not treat an observation with invalid
    localization as a valid removal target.

Map these to FR-01 to FR-03 and applicable safety requirements. Avoid
duplicating system requirements verbatim.

## 2.8 UPPAAL model

Suggested templates:

-   `Operator` --- selects a field (can be abstracted as an initial
    input).
-   `ControlStation` --- validates field and starts/stores the survey.
-   `Drone` --- surveys and sends observations.
-   `Detector` --- abstracts detection/no-detection outcomes.

Suggested Drone locations:

`Idle` → `SurveyAssigned` → `Surveying` → (`ObservationCaptured` →
`WaitingForAnalysis` → `Surveying`) → `SurveyComplete`.

Suggested Detector locations:

`Idle` → `Analysing` → (`WeedDetected` or `NoWeedDetected`) → `Idle`.

Suggested variables: `fieldValid`, `coverageComplete`,
`localizationValid`, `weedDetected`, `observationStored`.

Candidate properties (adapt template names/syntax):

-   `A[] (ControlStation.ValidTarget imply localizationValid)` --- a
    valid target is only accepted with valid localization.
-   `A[] (Drone.SurveyComplete imply coverageComplete)` --- survey
    completion requires the coverage condition.
-   `E<> ControlStation.SurveyRecorded` --- at least one path reaches a
    recorded survey outcome.

UPPAAL verifies the abstract workflow and guards, not real drone
coverage, image recognition accuracy, or GPS performance.

------------------------------------------------------------------------

# 3. Scenario 2 --- Tractor task coordination and safe weed removal

**Scenario focus:** converting a detected weed observation into a task,
assigning it to the tractor, navigating to the target, safely removing
the weed, and reporting the outcome.

**Primary requirement traceability:** FR-04, FR-05, FR-06, FR-07.\
**Related safety requirements:** SR-01 to SR-07.

## 3.1 Goal and actors

Model how the Control Station creates a unique task from a stored weed
observation, assigns it to an available tractor, and how the tractor
safely performs and reports the removal task.

Actors/components: Control Station, Autonomous Tractor, obstacle/person
detection, localization/safety functions, optional Operator.

## 3.2 Preconditions and assumptions

-   A valid weed observation exists with field ID and geographic
    location.
-   The target lies within the authorized field boundary.
-   The tractor is registered, available, and configured for the
    assigned task.
-   The configured weed-removal mechanism is operational.
-   Obstacle and localization signals are abstracted as model inputs.
-   The exact physical removal technology is not specified by this
    scenario.

## 3.3 Normal flow

1.  Control Station retrieves a valid weed observation.
2.  Control Station creates a unique task ID and target.
3.  Control Station checks tractor availability and checks that the
    target is not already assigned concurrently.
4.  Control Station assigns the task to the available tractor.
5.  Tractor receives and validates the task and command.
6.  Tractor accepts the task and acknowledges it to the Control Station.
7.  Tractor navigates toward the target while remaining inside the
    authorized field.
8.  Tractor checks for obstacles/persons during navigation.
9.  On reaching the target, tractor verifies the target and treatment
    area.
10. Tractor confirms it is stationary.
11. Tractor activates the configured weed-removal mechanism.
12. Tractor completes the operation and disables the mechanism.
13. Tractor reports `completed`, `partial`, or `failed`.
14. Control Station records the task outcome and updates mission
    progress.
15. The mission is complete only when all generated tasks have terminal
    outcomes.

## 3.4 Exception and safety flows

-   **Invalid/expired/unauthorized task:** reject the command; do not
    start navigation or tool operation.
-   **Duplicate assignment:** Control Station prevents a concurrent
    duplicate task assignment.
-   **Obstacle/person detected:** tractor stops; it resumes navigation
    only when the path is considered safe.
-   **Target/treatment area not verified:** do not activate the
    weed-removal mechanism.
-   **Tractor moving:** tool interlock prevents mechanism activation.
-   **Localization unreliable or boundary risk:** stop and enter the
    defined safe state.
-   **Emergency stop:** halt tractor motion and disable the weed-removal
    mechanism.
-   **Safety-critical data unavailable:** remain in a defined safe state
    until required checks pass.
-   **Task incomplete:** report partial or failed; do not report
    completed without a valid completion outcome.

## 3.5 SysML activity diagram

Suggested flow:

`Receive task` → `Validate task and command` → decision
`Valid and accepted?`

-   **No:** `Reject task` → `Report rejection`.
-   **Yes:** `Acknowledge task` → `Navigate to target` → decision
    `Obstacle/person detected?`
    -   **Yes:** `Stop tractor` → `Wait until path safe` → return to
        navigation.
    -   **No:** continue navigation. → decision `Target reached?` →
        `Verify target and treatment area` → decision
        `Target verified and tractor stationary?`
    -   **No:** `Remain stopped / report failure or request review`.
    -   **Yes:** `Activate weed-removal mechanism` → `Perform removal` →
        `Deactivate mechanism` → `Report task outcome` →
        `Update task status`.

Add guards for authorized field boundary, valid localization, emergency
stop, and safety-critical data. The tool activation action must only be
reachable when the tractor is stationary and target verification has
passed.

## 3.6 SysML sequence diagram

Suggested lifelines: `ControlStation`, `Tractor`, `ObstacleSensor`,
`Localization/Safety`.

Suggested messages:

-   `ControlStation -> ControlStation: createTask(taskId, target)`
-   `ControlStation -> Tractor: assignTask(taskId, target, commandValidity)`
-   `Tractor -> Tractor: validateTaskAndCommand()`
-   `Tractor -> ControlStation: taskAck(taskId, accepted/rejected)`
-   `ObstacleSensor -> Tractor: obstacleStatus(clear/detected)`
-   `Localization/Safety -> Tractor: localizationStatus(valid/invalid)`
-   `Tractor -> Tractor: verifyTargetAndTreatmentArea()`
-   `Tractor -> Tractor: activateRemovalMechanism()`
-   `Tractor -> ControlStation: taskResult(taskId, completed/partial/failed)`
-   `ControlStation -> ControlStation: updateTaskStatus(taskId, outcome)`

Use `alt` fragments for accepted/rejected, obstacle/no-obstacle,
verified/not-verified, and completed/partial/failed. Use `loop` if the
tractor handles multiple targets. Ensure the sequence shows the tool
being activated only after target verification and stationary
confirmation.

## 3.7 Scenario-specific requirement candidates

Possible additional detail, if needed:

-   `S2-REQ-01`: The Control Station shall assign a target only to an
    available tractor and shall prevent concurrent duplicate assignment
    of that target.
-   `S2-REQ-02`: The tractor shall acknowledge acceptance or rejection
    of each assigned task.
-   `S2-REQ-03`: The tractor shall report a terminal task outcome as
    completed, partial, or failed.

Trace these to FR-04 to FR-07 and SR-01 to SR-07. Do not create
duplicate IDs for requirements already fully covered by the system
baseline.

## 3.8 UPPAAL model

Suggested templates:

-   `ControlStation` --- creates, validates, assigns, and tracks task
    IDs.
-   `Tractor` --- accepts/rejects, navigates, verifies target, removes
    weed, and reports.
-   `SafetyEnvironment` --- abstracts obstacle, localization, and
    emergency-stop signals.

Suggested Tractor locations:

`Idle` → `ValidatingTask` → (`Rejected` or `Navigating`) →
`VerifyingTarget` → `ExecutingTask` → `Reporting` → `Completed`.

Add branches:

-   obstacle detected: `Navigating` → `Stopped` → `Navigating` after
    `pathClear`;
-   invalid localization: `Navigating` → `SafeState`;
-   unverified target: `VerifyingTarget` → `SafeState` or `Failed`;
-   emergency stop: active location → `EmergencyStopped`.

Suggested variables: `taskValid`, `taskAssigned`, `duplicateAssignment`,
`obstacle`, `pathClear`, `moving`, `actuatorOn`, `targetVerified`,
`localizationValid`, `emergencyStop`.

Candidate properties:

-   `A[] not (moving && actuatorOn)` --- tractor never moves while the
    mechanism is active.
-   `A[] (Tractor.ExecutingTask imply targetVerified)` --- removal only
    occurs after target verification.
-   `A[] (Tractor.ExecutingTask imply !moving)` --- tractor is
    stationary while removing weeds.
-   `A[] (Tractor.EmergencyStopped imply (!moving && !actuatorOn))` ---
    emergency stop disables movement and tool.
-   `A[] not duplicateAssignment` --- no concurrent duplicate
    assignment, if represented by a suitable variable/invariant.
-   Check that an accepted task reaches `Completed` or a defined
    `Failed` outcome under stated environment assumptions.

------------------------------------------------------------------------

# 4. Scenario 3 --- Communication failure, reconnection, and timeout recovery

**Scenario focus:** safe tractor behaviour when communication with the
Control Station is lost, automatic reconnection attempts, timeout
handling, failure reporting, and safe resumption.

**Primary requirement traceability:** FR-08, FR-09.\
**Primary safety requirement traceability:** SR-08, SR-09, SR-10,
SR-11.\
**Related safety requirements:** SR-02, SR-05, SR-06, SR-07.

## 4.1 Goal and actors

Model how the tractor responds to lost or unreliable communication while
performing a task. The tractor must stop safely, disable the
weed-removal mechanism, attempt to reconnect, enter Timeout State if the
reconnection limit is reached, and only resume after task
synchronization and safety checks.

Actors/components: Control Station, Autonomous Tractor, communication
link, optional Operator.

## 4.2 Preconditions and assumptions

-   Tractor has received and accepted a valid task.
-   Tractor is operating or navigating under that task.
-   A communication-health mechanism can detect loss or unacceptable
    degradation.
-   A reconnection timeout or retry limit is defined as a model
    parameter.
-   The link may recover before the timeout or remain unavailable until
    after timeout.
-   Failure reporting cannot be transmitted while the communication link
    is unavailable; the tractor stores the event locally.

## 4.3 Normal recovery flow

1.  Tractor is performing its assigned task with communication
    established.
2.  Tractor detects that communication is lost or unreliable.
3.  Tractor immediately stops movement and disables the weed-removal
    mechanism.
4.  Tractor enters `Reconnect` state.
5.  Tractor starts/restarts the reconnection timer according to the
    chosen retry policy.
6.  Tractor attempts to re-establish communication.
7.  If communication returns before timeout, tractor enters
    `RecoveryCheck`.
8.  Tractor and Control Station synchronize the current task ID, task
    status, and latest valid command.
9.  Tractor verifies command validity, localization, obstacle status,
    and other required safety conditions.
10. If all checks pass, the tractor resumes the appropriate task
    activity.
11. Control Station and tractor continue normal task reporting.

## 4.4 Timeout flow

1.  Reconnection attempts do not succeed before the defined
    timeout/retry limit.
2.  Tractor enters `Timeout` state.
3.  Tractor remains stopped and the weed-removal mechanism remains
    disabled.
4.  Tractor stores the communication-failure event and relevant task
    status locally.
5.  The tractor does not resume autonomously merely because a link later
    becomes available.
6.  When communication becomes available, the tractor reports the stored
    failure event and synchronizes task status.
7.  Resumption requires the defined recovery checks and a valid current
    command; include operator authorization if that is the team's chosen
    policy.

## 4.5 SysML activity diagram

Suggested flow:

`Operating with communication` → decision `Communication healthy?`

-   **Yes:** continue task.
-   **No:** `Stop tractor` → `Disable weed-removal mechanism` →
    `Enter Reconnect State` → `Start timeout clock` →
    `Attempt reconnection` → decision
    `Communication restored before timeout?`
    -   **Yes:** `Synchronize task status` → `Validate current command`
        → `Check localization and safety conditions` → decision
        `Recovery checks pass?`
        -   **Yes:** `Resume appropriate task activity`.
        -   **No:** `Remain stopped / request intervention`.
    -   **No:** `Enter Timeout State` →
        `Remain stopped and mechanism disabled` →
        `Store failure event locally` → wait for communication →
        `Report stored failure` → `Synchronize task status` →
        `Recovery checks` → resume only if authorized and safe.

Use a timer/timeout event for the timeout branch. Make the safe-state
actions explicit on entry to Reconnect and Timeout.

## 4.6 SysML sequence diagram

Suggested lifelines: `ControlStation`, `Tractor`, `CommunicationLink`,
`Safety/Localization`, optional `Operator`.

Suggested messages/events:

-   `CommunicationLink -> Tractor: communicationLost()`
-   `Tractor -> Tractor: stopMotion()`
-   `Tractor -> Tractor: disableRemovalMechanism()`
-   `Tractor -> Tractor: enterReconnectState()`
-   `Tractor -> CommunicationLink: reconnectAttempt()`
-   `CommunicationLink -> Tractor: connectionRestored()` (if restored
    before timeout)
-   `Tractor -> ControlStation: synchronizeTaskStatus(taskId, status)`
-   `ControlStation -> Tractor: currentTaskAndCommand(taskId, commandVersion)`
-   `Tractor -> Safety/Localization: requestSafetyStatus()`
-   `Safety/Localization -> Tractor: safetyStatus(localization, obstacle, interlocks)`
-   `Tractor -> ControlStation: recoveryReady()` or
    `recoveryBlocked(reason)`

For timeout:

-   `Tractor -> Tractor: reconnectTimeout()`
-   `Tractor -> Tractor: enterTimeoutState()`
-   `Tractor -> Tractor: storeFailureEvent(taskId, reason)`
-   after link recovery:
    `Tractor -> ControlStation: reportStoredFailure(taskId, reason)`

Use `alt` for connection restored before timeout vs timeout reached. Use
another `alt` for safety checks passed vs failed. The sequence should
not show immediate task resumption on `connectionRestored()`.

## 4.7 Scenario-specific requirement candidates

The system baseline already contains the core requirements. Add detail
only if necessary:

-   `S3-REQ-01`: On communication loss, the tractor shall stop movement
    and disable the weed-removal mechanism before attempting
    reconnection.
-   `S3-REQ-02`: If the reconnection timeout expires, the tractor shall
    remain in Timeout State and store the failure event locally.
-   `S3-REQ-03`: Communication restoration shall not by itself authorize
    task resumption; task synchronization and safety checks shall pass
    first.

Trace these to FR-08, FR-09 and SR-08 to SR-11. These scenario-level
statements refine the system baseline; they do not replace it.

## 4.8 UPPAAL model

Suggested templates:

-   `Tractor` --- operating, reconnecting, timing out, recovery
    checking, and resuming.
-   `ControlStation` --- maintains task state and supplies the current
    task/command after reconnection.
-   `CommunicationLink` --- abstracts link up/down and recovery.
-   `SafetyEnvironment` --- abstracts localization, obstacle, and
    safety-check outcomes.

Suggested Tractor locations:

`Operating` → `Reconnect` → (`RecoveryCheck` → `Operating` if checks
pass) or (`Timeout` → `WaitingForLink` → `RecoveryCheck` after link
returns).

The `Reconnect` and `Timeout` locations must enforce `moving == false`
and `actuatorOn == false`.

Suggested variables:

-   `commUp`
-   `moving`
-   `actuatorOn`
-   `taskStatusValid`
-   `commandValid`
-   `localizationValid`
-   `obstacleClear`
-   `failureStored`
-   `reconnectAttempts`

Suggested clock: `tReconnect`, reset on entry to `Reconnect`. Define a
guard for the agreed timeout value `T_RECONNECT`; do not select a
numeric value until agreed by the team.

Candidate properties:

-   `A[] (Tractor.Reconnect imply (!moving && !actuatorOn))`
-   `A[] (Tractor.Timeout imply (!moving && !actuatorOn))`
-   `A[] (Tractor.Operating imply commUp && taskStatusValid && commandValid)`
    if the operational policy requires a live link for all operation.
-   `A[] (Tractor.Operating imply !emergencyStop)`
-   `A[] (Tractor.RecoveryCheck imply !moving && !actuatorOn)`
-   `A[] (Tractor.Timeout imply failureStored)`

Check that: - timeout is reachable when the link remains down beyond the
configured limit; - the tractor cannot move or activate the mechanism in
Reconnect or Timeout; - communication restoration alone cannot
transition directly to Operating; - resumption requires valid task
synchronization and safety checks; - the stored failure event is
reported when communication is available again.

UPPAAL verifies the abstract state/timeout logic. It does not validate
real radio coverage, reconnect performance, or physical safety hardware.

------------------------------------------------------------------------

# 5. Relationship between the three scenarios

The scenarios are separate views of one system, not three unrelated
systems.

  --------------------------------------------------------------------------------
  Scenario          Main focus        Main output                Main requirements
  ----------------- ----------------- -------------------------- -----------------
  Scenario 1        Drone survey and  Geolocated weed            FR-01 to FR-03
                    weed detection    observations               

  Scenario 2        Task assignment   Task outcome:              FR-04 to FR-07;
                    and tractor weed  completed/partial/failed   SR-01 to SR-07
                    removal                                      

  Scenario 3        Communication     Safe recovery or           FR-08 to FR-09;
                    failure and       timeout/failure report     SR-08 to SR-11
                    recovery                                     
  --------------------------------------------------------------------------------

**End-to-end dependency:** Scenario 1 produces weed observations.
Scenario 2 consumes those observations as removal tasks. Scenario 3
applies when communication between the tractor and Control Station is
lost during task operation or recovery. Scenario 3 can interrupt
Scenario 2 and must return control only through the defined recovery
checks.

------------------------------------------------------------------------

# 6. UPPAAL modelling checklist

For each scenario:

-   [ ] List each automaton and what it represents.
-   [ ] Draw locations before adding transitions.
-   [ ] Declare shared variables and channels consistently.
-   [ ] Label transitions with events, guards, synchronisations, and
    updates.
-   [ ] Add clocks only for meaningful time bounds.
-   [ ] Include normal, exception, and timeout paths relevant to the
    scenario.
-   [ ] Define the outcome of every timeout.
-   [ ] State assumptions needed for liveness (for example, that a path
    eventually becomes clear or a link eventually returns).
-   [ ] Run verification and record exact properties/results.
-   [ ] Inspect counterexamples when a property fails; revise the model
    or explain the assumption/property issue.

Query examples are patterns, not guaranteed copy-paste queries. Adapt
them to actual template/location/variable names and the UPPAAL version:

-   `A[] not (moving && actuatorOn)` --- no simultaneous tractor motion
    and tool activation.
-   `A[] not deadlock` --- no reachable deadlock, if terminal deadlock
    is not intended.
-   `E<> Completed` --- at least one path reaches completion; this does
    not prove all executions complete.
-   `A<> (Completed || Failed)` --- every execution eventually reaches a
    terminal outcome; use only when assumptions support it.
-   `A[] (Tractor.Timeout imply (!moving && !actuatorOn))` --- timeout
    always means stopped with tool disabled.

Record the exact query, result, and model assumptions. Do not claim a
reachability query proves all executions complete.

------------------------------------------------------------------------

# 7. Suggested project structure

``` text
docs/
  ADAS_Lab02_Three_Scenario_Guide.md
  scenario-1-drone-survey-weed-detection.md
  scenario-2-tractor-task-and-weed-removal.md
  scenario-3-communication-recovery.md
sysml/
  scenario-1/
    activity.*
    sequence.*
    requirements.*
  scenario-2/
    activity.*
    sequence.*
    requirements.*
  scenario-3/
    activity.*
    sequence.*
    requirements.*
uppaal/
  scenario-1.xml
  scenario-2.xml
  scenario-3.xml
  integrated-system.xml
```

Each scenario document should include purpose, actors, assumptions,
normal/exception flows, state definitions, diagram references, UPPAAL
properties/results, and open questions.

------------------------------------------------------------------------

# 8. Team integration review

Before integrating:

1.  Do all scenarios use the same meaning for `Stopped`, `Completed`,
    and `Failed`?
2.  Are `Reconnect`, `Timeout`, and recovery rules represented
    consistently wherever communication recovery applies?
3.  Are message names and task IDs consistent?
4.  Does each requirement map to model elements and a verification check
    where applicable?
5.  Are timeouts and recovery paths explicit?
6.  Can a teammate understand each diagram without verbal explanation?
7.  Are assumptions and unverified physical behaviours documented?

## Integration sequence

1.  Complete and verify each scenario independently.
2.  Compare interfaces, state meanings, requirement IDs, and
    assumptions.
3.  Connect Scenario 1 observation reporting to Scenario 2 task
    creation.
4.  Connect Scenario 2 tractor operation to Scenario 3 communication
    recovery.
5.  Verify after each integration step.
6.  Preserve the individual scenario models for debugging.
7.  Commit the integrated model, verification results, and a short note
    describing assumptions and limitations.
