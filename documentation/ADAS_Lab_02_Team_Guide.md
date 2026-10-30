# ADAS Lab 02 --- Team Working Guide

**Purpose:** A practical checklist for a three-person team to plan,
implement, review, and document the work described in
`ASB_lab_ADAS_02.pdf`.

**Source basis:** ADAS 02, page 2. The PDF defines the required work
packages and milestones, but does **not** prescribe a programming
language, AI architecture, annotation platform, UML notation, hardware
platform, or exact GitHub folder structure. Those items are marked below
as recommendations rather than course requirements.

------------------------------------------------------------------------

## 1. What ADAS 02 asks the team to do

The PDF sets out these requirements:

1.  **Identify and specify agricultural use cases in detail** for:
    -   tasks monitored by drones;
    -   autonomously driving agricultural vehicles;
    -   agricultural areas that cannot be monitored by a drone alone;
    -   external devices for monitoring and controlling the holistic
        system.
2.  **Model, validate, and verify** the use cases.
3.  Work on **automated labelling and learning** for different types of
    plants, weeds, parasites, and diseases.
4.  Complete **all subtasks by the end of November 2026**. Each team
    manages its own work and should use a **Gantt chart**.
5.  Produce an **integrated overall solution** that includes coordinated
    autonomous vehicles and a deep-learning (DL) approach, and prepare
    for the competition **before Christmas 2026**.

### Two milestones

  ------------------------------------------------------------------------------------
  Milestone               Required outcome stated in ADAS 02   Target
  ----------------------- ------------------------------------ -----------------------
  M1 --- Subtasks         All subtasks completed: use cases,   **30 November 2026**
                          modelling/validation/verification,   (PDF says "end of
                          and automated labelling and learning November")

  M2 --- Integrated       Integrated overall solution          **Before Christmas
  solution                including coordinated autonomous     2026**
                          vehicles and a DL approach;          
                          competition preparation              
  ------------------------------------------------------------------------------------

> **Important:** The PDF does not define how many use cases, which
> crop/disease classes, which model, or which vehicle/drone platform
> must be used. Agree these with the supervisor/team before treating
> them as fixed requirements.

------------------------------------------------------------------------

## 2. Task checklist: what to do and what to put in GitHub

The "GitHub deliverables" column below is a **recommended evidence
package**. ADAS 02 does not explicitly prescribe individual GitHub files
for each subtask.

  -----------------------------------------------------------------------------------------------------------------------------------------
  ID             Subtask           What the team should   Recommended GitHub deliverables / evidence                  Done when...
                                   do                                                                                 
  -------------- ----------------- ---------------------- ----------------------------------------------------------- ---------------------
  UC-01          Drone-monitored   List agricultural      `docs/use-cases/drone-monitoring.md`; relevant use-case     Each drone use case
                 agricultural      monitoring tasks       diagram source and exported image in `docs/diagrams/`.      is described clearly
                 tasks             suitable for a drone.                                                              enough that another
                                   For each, define the                                                               team member can
                                   goal, actors, inputs,                                                              understand its
                                   main steps, outputs,                                                               workflow and expected
                                   assumptions, and                                                                   result.
                                   failure/exception                                                                  
                                   cases.                                                                             

  UC-02          Autonomous        Identify tasks         `docs/use-cases/autonomous-vehicle.md`; vehicle use-case    Vehicle
                 agricultural      performed by an        diagram/source.                                             responsibilities and
                 vehicle tasks     autonomously driving                                                               interactions are
                                   agricultural vehicle.                                                              explicit; assumptions
                                   Describe its role,                                                                 and limitations are
                                   inputs, actions,                                                                   recorded.
                                   outputs, operating                                                                 
                                   conditions, and                                                                    
                                   interaction with other                                                             
                                   system components.                                                                 

  UC-03          Areas not         Identify agricultural  `docs/use-cases/coverage-gaps.md`; a table of               The uncovered cases
                 monitored by a    areas or situations    area/situation, limitation, and proposed monitoring         and the reason
                 drone alone       that cannot be         approach.                                                   drone-only monitoring
                                   adequately monitored                                                               is insufficient are
                                   by a drone alone.                                                                  documented.
                                   Explain the monitoring                                                             
                                   gap and what                                                                       
                                   additional coverage or                                                             
                                   system component is                                                                
                                   needed. Do not assume                                                              
                                   the solution before                                                                
                                   identifying the gap.                                                               

  UC-04          External          Identify external      `docs/use-cases/external-monitoring-control.md`; interface  Monitoring and
                 monitoring and    devices/interfaces     sketch or system-context diagram.                           control
                 control devices   used to monitor and                                                                responsibilities,
                                   control the holistic                                                               users, inputs, and
                                   system. Define who                                                                 outputs are clear.
                                   uses them, what                                                                    
                                   status/data they show,                                                             
                                   and what control                                                                   
                                   actions they support.                                                              

  MOD-01         Detailed use-case Turn the identified    `docs/use-cases/` specifications;                           Every selected use
                 specification     use cases into         `docs/templates/use-case-template.md`.                      case has a complete,
                                   consistent                                                                         consistent
                                   specifications. Use a                                                              specification.
                                   common template:                                                                   
                                   ID/name, objective,                                                                
                                   actors, preconditions,                                                             
                                   trigger, main flow,                                                                
                                   alternative/error                                                                  
                                   flows, inputs,                                                                     
                                   outputs, and                                                                       
                                   postconditions.                                                                    

  MOD-02         Model the use     Create models that     Editable diagram source (e.g. PlantUML/draw.io) plus        Diagrams are
                 cases             show actors, system    exported PNG/SVG in `docs/diagrams/`.                       readable,
                                   boundaries,                                                                        version-controlled,
                                   components, and                                                                    and agree with the
                                   interactions. Keep                                                                 written use cases.
                                   diagrams consistent                                                                
                                   with the written                                                                   
                                   specifications.                                                                    

  MOD-03         Validate the use  Check whether each use `docs/verification-validation/validation-plan.md`;          Each use case has a
                 cases             case represents a real `validation-results.md`; review/decision log.               recorded validation
                                   and useful                                                                         result and unresolved
                                   agricultural task and                                                              issues are visible.
                                   whether the proposed                                                               
                                   workflow addresses its                                                             
                                   intended purpose.                                                                  
                                   Record review                                                                      
                                   questions, feedback,                                                               
                                   and decisions.                                                                     

  MOD-04         Verify the use    Check that each        `docs/verification-validation/verification-checklist.md`;   Each agreed
                 cases             specification and      `verification-results.md`; links to evidence/issues.        requirement has a
                                   model is complete,                                                                 check and a recorded
                                   consistent, and                                                                    result or an
                                   conforms to the agreed                                                             explicitly open
                                   requirements. Define                                                               status.
                                   checks and record                                                                  
                                   pass/fail plus                                                                     
                                   evidence.                                                                          

  AL-01          Automated         Investigate and define `docs/ai/annotation-workflow.md`; annotation instructions;  The labelling
                 labelling         a repeatable workflow  small reviewed example/export if permitted;                 workflow,
                                   for automated or       tool/configuration notes.                                   quality-control
                                   assisted annotation of                                                             method, and
                                   the agricultural                                                                   limitations are
                                   images. State what is                                                              documented.
                                   automated, what                                                                    
                                   requires human review,                                                             
                                   and how annotation                                                                 
                                   quality is checked.                                                                

  AL-02          Plant types       Define the plant       `docs/ai/classes-and-label-schema.md`; example annotations  Plant classes and
                                   categories/classes to  and class definitions.                                      annotation rules are
                                   be considered and how                                                              unambiguous and
                                   they will be labelled.                                                             agreed by the team.
                                   The PDF does not                                                                   
                                   specify the exact                                                                  
                                   classes.                                                                           

  AL-03          Weed types        Define the weed        Same class schema plus weed examples and review notes.      Weed labels are
                                   categories/classes and                                                             consistent and
                                   annotation rules;                                                                  representative
                                   connect them to the                                                                examples are checked.
                                   automated                                                                          
                                   labelling/learning                                                                 
                                   workflow.                                                                          

  AL-04          Parasites         Define which parasite  Class/schema updates, example annotations if available, and Scope is explicit;
                                   categories are in      a note on data coverage/limitations.                        missing image
                                   scope and how they                                                                 coverage is recorded
                                   will be                                                                            rather than guessed.
                                   represented/labeled in                                                             
                                   the data. Confirm                                                                  
                                   feasibility against                                                                
                                   available images.                                                                  

  AL-05          Diseases          Define which disease   Class/schema updates, example annotations if available, and Scope is explicit;
                                   categories are in      data coverage/limitations.                                  missing image
                                   scope and how they                                                                 coverage is recorded
                                   will be                                                                            rather than guessed.
                                   represented/labeled.                                                               
                                   Confirm feasibility                                                                
                                   against available                                                                  
                                   images.                                                                            

  INT-01         Integrated        Define how the use     `docs/integration/system-architecture.md`; architecture     The team can explain
                 overall solution  cases, monitoring      diagram source/export; interface/data-flow notes.           the complete system
                                   components,                                                                        flow and how each
                                   vehicle(s), and DL                                                                 component connects.
                                   approach fit into one                                                              
                                   end-to-end system.                                                                 
                                   Identify component                                                                 
                                   interfaces and                                                                     
                                   information exchanged.                                                             

  INT-02         Coordinated       Specify and integrate  `docs/integration/vehicle-coordination.md`; relevant        A repeatable
                 autonomous        how autonomous         code/configuration; test scenario and results.              coordination scenario
                 vehicles          vehicles coordinate as                                                             is demonstrated or
                                   part of the overall                                                                any unimplemented
                                   solution. Document the                                                             part is clearly
                                   coordination behaviour                                                             documented.
                                   that is actually                                                                   
                                   implemented or                                                                     
                                   demonstrated.                                                                      

  INT-03         DL approach       Connect the            `docs/ai/model-card.md`; inference code/configuration;      The DL component's
                 integration       deep-learning approach sample input/output; integration notes and test results.    interface and role in
                                   to the integrated                                                                  the integrated
                                   system. Document the                                                               workflow are
                                   model's input/output                                                               demonstrated or
                                   and how downstream                                                                 limitations are
                                   components use its                                                                 recorded.
                                   output.                                                                            

  COMP-01        Competition       Prepare and rehearse a `docs/competition/demo-plan.md`; setup/run instructions;    The team can set up
                 preparation       demonstration of the   demo checklist; results/issues log.                         and run the agreed
                                   integrated solution.                                                               demonstration
                                   Define the scenario,                                                               reliably before the
                                   setup, expected                                                                    competition.
                                   behaviour, and                                                                     
                                   fallback plan.                                                                     
  -----------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 3. Suggested ownership for three members

This is a **team recommendation**, not a role allocation stated in ADAS
02. Assign one owner per workstream, but review and integrate the work
together.

  --------------------------------------------------------------------------
  Owner                   Primary workstream      Suggested responsibilities
  ----------------------- ----------------------- --------------------------
  Member 1                Drone and agricultural  UC-01, UC-03; contribute
                          monitoring use cases    to use-case specifications
                                                  and models; support
                                                  monitoring-related
                                                  integration.

  Member 2                Autonomous agricultural UC-02; contribute to
                          vehicles                use-case
                                                  specifications/models;
                                                  lead vehicle coordination
                                                  work for integration.

  Member 3                Automated labelling,    UC-04, AL-01 to AL-05;
                          learning, and external  contribute to
                          monitoring/control      validation/verification;
                                                  lead DL integration.

  All three               Shared system           Agree scope and
                          engineering             interfaces; review all use
                                                  cases; model, validate,
                                                  and verify the complete
                                                  set; integrate and
                                                  rehearse the final
                                                  demonstration; review
                                                  final documentation.
  --------------------------------------------------------------------------

**Working rule:** An owner is responsible for keeping a task moving and
uploading its evidence. The other members should review it. Do not let a
task become known only to its owner.

------------------------------------------------------------------------

## 4. Recommended GitHub repository structure

Use a simple structure that makes the team's work and evidence easy to
review.

``` text
adas-lab/
├── README.md
├── .gitignore
├── docs/
│   ├── project-plan/
│   │   ├── gantt-chart.md
│   │   └── task-assignments.md
│   ├── use-cases/
│   │   ├── drone-monitoring.md
│   │   ├── autonomous-vehicle.md
│   │   ├── coverage-gaps.md
│   │   ├── external-monitoring-control.md
│   │   └── use-case-template.md
│   ├── diagrams/
│   │   ├── source/
│   │   └── exports/
│   ├── verification-validation/
│   │   ├── validation-plan.md
│   │   ├── validation-results.md
│   │   ├── verification-checklist.md
│   │   └── verification-results.md
│   ├── ai/
│   │   ├── annotation-workflow.md
│   │   ├── classes-and-label-schema.md
│   │   ├── model-card.md
│   │   └── experiments/
│   ├── integration/
│   │   ├── system-architecture.md
│   │   └── vehicle-coordination.md
│   └── competition/
│       └── demo-plan.md
├── src/
│   ├── annotation/
│   ├── model/
│   └── integration/
├── notebooks/
├── tests/
├── examples/
└── results/
```

Adapt this structure to the actual code and work. Do not create empty
folders just to match the example.

### What should go into the repository?

-   **Documents:** Markdown specifications, plans, decisions, test
    plans, and results.
-   **Diagrams:** Editable source files and exported images
    (PNG/SVG/PDF).
-   **Code:** Scripts, notebooks, configuration, and integration code
    needed to reproduce the work.
-   **Evidence:** Small representative examples, test outputs, and links
    to larger approved artefacts.
-   **Instructions:** How to install dependencies, run
    notebooks/scripts, reproduce tests, and launch the demonstration.

**Dataset caution:** Do not commit large datasets, private data, or
externally shared images unless the team has permission and the
repository policy allows it. Add dataset acquisition instructions,
source/provenance, class information, and expected folder layout
instead. Keep credentials, tokens, and private configuration out of
GitHub.

------------------------------------------------------------------------

## 5. Tools to consider

ADAS 02 does not mandate any of these tools. Choose tools that solve a
real project need and that all three members can use.

  -----------------------------------------------------------------------
  Work area               Tools to consider       Why they may help
  ----------------------- ----------------------- -----------------------
  Version control and     **Git, GitHub**         Track changes, review
  collaboration                                   each other's work,
                                                  manage issues, and
                                                  maintain weekly
                                                  progress.

  Planning                **GitHub Projects**,    Assign owners, track
                          Gantt chart in          status, and manage the
                          Excel/LibreOffice, or a end-of-November
                          simple Markdown table   milestone.

  Use-case and            **diagrams.net          Create editable
  architecture diagrams   (draw.io)** or          use-case,
                          **PlantUML**            system-context, and
                                                  architecture diagrams.

  Data inspection and     **Python, Jupyter       Inspect image data, run
  experiments             Notebook**              experiments, and
                                                  document reproducible
                                                  steps.

  Image annotation        **CVAT**, **Label       Compare annotation
                          Studio**, or            workflows and assess
                          **Roboflow**            whether
                                                  automated/assisted
                                                  labelling is suitable.

  Deep learning           **PyTorch** or          Implement and evaluate
                          **TensorFlow**          a DL approach if model
                                                  development is part of
                                                  the agreed scope.

  Testing                 **pytest** (for Python  Make software checks
                          code) and documented    repeatable and record
                          manual test cases       test outcomes.
  -----------------------------------------------------------------------

### Keep the toolchain manageable

1.  Use GitHub as the single source of truth for code and project
    documentation.
2.  Select **one** diagramming tool and **one** annotation workflow
    initially.
3.  Do not choose a DL model until you understand the image data, target
    classes, and task.
4.  Record tool versions, settings, and steps needed to reproduce
    results.
5.  A tool being used does not itself prove that a task is complete;
    upload the resulting artefact and evidence.

------------------------------------------------------------------------

## 6. How to write a useful use-case specification

Use the same template for every use case.

  -----------------------------------------------------------------------
  Field                               What to write
  ----------------------------------- -----------------------------------
  ID and name                         Unique identifier and short
                                      descriptive name.

  Objective                           What agricultural task or problem
                                      does it address?

  Actors                              Drone, autonomous vehicle,
                                      operator, external device, or other
                                      system component.

  Preconditions                       What must be true before the use
                                      case starts?

  Trigger                             What event starts it?

  Main flow                           Ordered steps from start to
                                      successful completion.

  Alternative/error flows             What happens if data is missing,
                                      communication fails, or the task
                                      cannot be completed?

  Inputs                              Images, sensor readings, commands,
                                      locations, or other required
                                      information.

  Outputs                             Detection result, status, location,
                                      command, report, or other result.

  Postconditions                      What state or result should exist
                                      when it finishes?

  Assumptions/limitations             What is not yet known, available,
                                      or implemented?

  Validation/verification             How will the team judge usefulness
                                      and check conformance?
  -----------------------------------------------------------------------

Keep the written specification and its diagram consistent. If the
workflow changes, update both and record the change in Git.

------------------------------------------------------------------------

## 7. Validation and verification: practical checklist

The PDF requires both, but does not prescribe a test method. The
following is a recommended way to make the work auditable.

### Validation --- are these the right use cases?

-   [ ] The agricultural need or monitoring task is clearly stated.
-   [ ] The intended user/system actor is identified.
-   [ ] The workflow addresses the stated need.
-   [ ] Drone-only monitoring limitations are considered where relevant.
-   [ ] External monitoring/control needs are considered.
-   [ ] Assumptions and unresolved questions are recorded.
-   [ ] Review feedback and decisions are saved.

### Verification --- are the use cases specified and modelled correctly?

-   [ ] Every use case has a unique ID and complete specification.
-   [ ] Actors, triggers, inputs, outputs, and main flows are defined.
-   [ ] Alternative and failure flows are considered.
-   [ ] Diagrams agree with the written specifications.
-   [ ] Each agreed requirement has a check.
-   [ ] Pass/fail, evidence, date, and reviewer are recorded.
-   [ ] Open issues are listed rather than silently treated as complete.

------------------------------------------------------------------------

## 8. Automated labelling and learning: practical checklist

The PDF names plants, weeds, parasites, and diseases, but does not
define exact classes or annotation formats. Agree the scope using the
actual available images.

-   [ ] Inspect the available images and record their source and
    coverage.
-   [ ] Agree which plant, weed, parasite, and disease classes are in
    scope.
-   [ ] Define the annotation type needed for the task (for example,
    image-level class, bounding box, or segmentation mask); confirm this
    choice with the supervisor.
-   [ ] Write clear labelling rules and examples.
-   [ ] Decide which annotation steps are automated and which require
    human review.
-   [ ] Review a sample of labels for consistency and errors.
-   [ ] Record class counts, missing classes, and data limitations.
-   [ ] Document the learning approach and experiments performed.
-   [ ] Record evaluation method and results if a model is trained.
-   [ ] Keep a reproducible record of data preparation, configuration,
    and model version.

Do not claim a class is supported if the available images do not contain
suitable examples.

------------------------------------------------------------------------

## 9. Weekly GitHub workflow

ADAS 02 asks the team to manage its subtasks with a Gantt chart. ADAS 01
additionally says the team should configure a GitHub repository and make
**at least weekly updates from each member**. Use this lightweight
routine:

1.  **Plan:** Create GitHub Issues for the subtasks. Assign one owner
    and a due date.
2.  **Work:** Keep documents, diagrams, notebooks, code, and test
    evidence in the repository.
3.  **Update:** Each member makes a meaningful weekly commit or pull
    request showing their contribution.
4.  **Review:** At least one teammate reviews important specifications,
    diagrams, and code.
5.  **Track:** Update the issue status and Gantt chart; record blockers
    and decisions.
6.  **Integrate:** Merge reviewed work into the main branch and keep the
    README current.

Suggested issue labels: `use-case`, `modelling`, `validation`,
`verification`, `data`, `labelling`, `deep-learning`, `integration`,
`competition`, `documentation`.

A commit should describe the change, for example:
`docs: add drone monitoring use-case specification`.

------------------------------------------------------------------------

## 10. Final readiness checklist

### By the end of November 2026 --- all subtasks

-   [ ] The four use-case areas in ADAS 02 have been addressed.
-   [ ] Selected use cases are specified in detail.
-   [ ] Use cases have been modelled.
-   [ ] Validation has been performed and documented.
-   [ ] Verification has been performed and documented.
-   [ ] Automated labelling and learning work addresses plants, weeds,
    parasites, and diseases, with scope and limitations recorded.
-   [ ] The team Gantt chart is up to date.
-   [ ] The GitHub repository contains the work and evidence completed
    so far.

### Before Christmas 2026 --- integrated solution and competition preparation

-   [ ] The overall system architecture is documented.
-   [ ] The deep-learning approach is integrated into the overall
    solution.
-   [ ] Coordinated autonomous vehicles are included in the integrated
    solution.
-   [ ] The end-to-end workflow has been tested or demonstrated to the
    extent possible.
-   [ ] Competition demonstration steps and setup are documented.
-   [ ] Known limitations and incomplete features are clearly stated.

------------------------------------------------------------------------

## 11. Source boundary: what is required and what is recommended

  -----------------------------------------------------------------------
  Item                                Status
  ----------------------------------- -----------------------------------
  Four agricultural use-case areas    **Explicit ADAS 02 requirement**
  listed in Section 1                 

  Model, validate, and verify the use **Explicit ADAS 02 requirement**
  cases                               

  Automated labelling and learning    **Explicit ADAS 02 requirement**
  for plants, weeds, parasites, and   
  diseases                            

  Team-managed Gantt chart            **Explicit ADAS 02 instruction**

  Integrated solution with            **Explicit ADAS 02 requirement**
  coordinated autonomous vehicles and 
  DL approach                         

  Competition preparation before      **Explicit ADAS 02 milestone**
  Christmas                           

  Specific Markdown filenames and     **Team recommendation**
  repository structure                

  Specific UML notation or            **Team recommendation; not
  diagramming tool                    specified in ADAS 02**

  Specific annotation platform or DL  **Team recommendation; not
  framework                           specified in ADAS 02**

  Exact number of use cases, data     **Not specified in ADAS 02; clarify
  classes, model, or hardware         with supervisor**
  -----------------------------------------------------------------------

**Primary reference:** `ASB_lab_ADAS_02.pdf`, page 2 --- "Overall task"
(dated 30.10.26).

**Related organizational guidance:** `ASB_lab_ADAS_01.pdf`, page 2 (team
leader, GitHub repository, weekly member updates); page 7 (10-minute
presentation plus 2-minute discussion, balanced individual
contributions); page 8 (final documentation deadline 25.01.2027,
scientific descriptions, Git upload statistics, and member-to-task
mapping).
