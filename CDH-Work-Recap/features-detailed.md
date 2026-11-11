# Features in Detail (from Agile Studio)

[← Back to index](README.md)

Each story and enhancement I worked on, with the description, acceptance criteria, epic and story points pulled from the Agile Studio MCP. Grouped by release.

## Customer Decision Hub 8.8

### US-460665: Action Landing Page Supports Withdrawn Actions

**Epic:** Advanced Configuration of Actions · **Story points:** 5 · **Status:** Resolved-Rejected

> As a NBA designer, I want to be able to optionally view withdrawn actions so I can re-enable them

**Acceptance criteria:**
- The Action landing page will continue to show rule resolved actions by default
- The Actions landing page shows an option to display Withdrawn and Not available
- Actions that are available should continue to use the OpenByKey method
- Actions that are Withdrawn or Not available should use the OpenByHandle method
- The landing page should display the status of the rule on the landing page so users can distinguish between withdran and available actions

### US-471810: Reverting to a Previous Version of Treatment

**Epic:** Improved Treatment Authoring experience · **Story points:** 5 · **Status:** Resolved-Completed

> As a NBA designer, I want to rollback to the previous version of a treatment after deleting an action so the behavior is consistent with the action rule

**Acceptance criteria:**
- When deleting the current version of an action in an unlocked ruleset version, the treatment join DDR entries should update to the previous version
- This behavior should be consistent with the action rule
- Existing functionality should not be impacted by this change

### US-476973: Adopt Support for Dynamic SMS Messages

**Epic:** Support Personalization for Email & SMS treatments · **Story points:** 3 · **Status:** Resolved-Rejected

> As a NBA designer, I want to adopt support for personalizing external SMS treatments so I can send personalized messages to my customers

**Acceptance criteria:**
- Review changes made by Champions to support personalization of external treatments
- Refactor any existing code for SMS to support this personalization

### US-477041: CPV Supports Customer Journey Decisions

**Epic:** Additional Explain Results & Data for Customer Profile Viewer · **Story points:** 3 · **Status:** Resolved-Completed

> As a NBA designer, I want decisions and responses captured in CPV to write to JourneyStages dataset so I can properly test how customers advance through journeys

**Acceptance criteria:**
- The generated ArbitrationTest dataflow includes the WriteToJourneyStages dataflow if the "Show only decision results that will be delivered" option is selected

## Customer Decision Hub '23

### US-501811: Persona Landing Page - Default Summary View

**Epic:** CPV Supports Explain results and better Persona management · **Story points:** 5 · **Status:** Resolved-Completed

> As a NBA designer/specialist, I want to see all of my personas in a landing page, so that I can manage my library of personas

**Acceptance criteria:**
- See all active personas on grid
- Ability to filter/sort personas and define new filters
- Ability to search for persona
- Only display data transforms that are personas
- Available and visible in CDH
- Available and visible in Ops Manager
- Persona landing page can be accessed from new menu item

### US-503308: Treatments Landing Page Supports Custom Channels

**Epic:** Manage Next-Best-Action Designer Business Configurations · **Story points:** 8 · **Status:** Resolved-Rejected

> As a NBA Designer, I want to be able to create/edit treatments for custom channels so I can manage treatments for these channels

**Acceptance criteria:**
- Each treatment grid should display a new column 'TreatmentType' which displays this property from the Treatment DDR. A blank or null value should display as "Any" in the ui only.
- Each Treatment section should adopt the new Channel datapage. Channels are now defined as being inbound or outbound so the Direction dropdown should be removed from the treatment sections. Each treatment section, both internal and external, should al…
- Create menu on treatment landing page should allow creation of custom channel treatments and be sourced from new channel datapage.
- If there is only 1 channel defined for the current ChannelGroup, the TreatmentType dropdown should display that channel. If there are multiple, then "Any treatment in the group" option should be added to the dropdown.

### US-506723: [CDH] Merge Activity for ActionInsights2

**Epic:** Adopt Profile Merge for Identity Stitching · **Story points:** 3 · **Status:** Resolved-Completed

> As a NBA Designer, I want to merge ActionInsights data for a customer between a known and unknown identity so I can decision on combined behavioral data Implementation details: Implementation details: Information on the required parameters for this activity is described in the design doc: https://techdocs.rpega.com/pages/viewpage.action?pageId=66847845

**Acceptance criteria:**
- On request, this process will take in the From and To SubjectID's and copy all ActionInsight records
- TTL entries should be recalculated and set on the copied ActionInsights
- The original ActionInsight records remain as they were
- This merge activity can be called from another process

### US-513683: Contact Policies Support PlacementType

**Epic:** Manage Next-Best-Action Designer Business Configurations · **Story points:** 5 · **Status:** Resolved-Completed

> As a NBA Designer, I want to define a threshold for outcomes for a placement type (Hero, Tile, etc) so I can limit the number of times a specific placement type is displayed across issues and groups

**Acceptance criteria:**
- BehavioralLimits and CheckOutcomeLimits strategies are regenerated in 8.9 regardless if they have been modified
- PlacementType property was added to IH channel dimension by of Guardians work, ensure this new IH property is added on upgrade
- ProcessSuppressions dataflow was updated to add PlacementType as ActionInsight2 property and as Identifier. Ensure this dataflow is regenerated on upgrade
- Upgrade Contact policies continue to work as expected

### US-515727: Update CPV to support Channel Context

**Epic:** CPV Supports Explain results and better Persona management · **Story points:** 5 · **Status:** Resolved-Completed

> As a NBA Designer I want to select a Channel context in the Next-Best-Action tab so I can test my decision results

**Acceptance criteria:**
- User can select a Channel context in the NBA tab
- Selecting a Channel context shows the context values as read-only

### US-522200: BehavioralLimits Strategy uses GOS

**Epic:** Adopt Profile Merge for Identity Stitching · **Story points:** 3 · **Status:** Resolved-Completed

> As a system architect, I want the ProcessInteractionHistory dataflow to use the GOS version of BehavioralLimits so response execution is efficient and performant

**Acceptance criteria:**
- New implementations should use GOS version of BehavorialLimits strategy
- On Save of Context dictionary, the BehavioralLimits strategy should get replaced with GOS version in ProcessInteractionHistory DF
- Ship the GOS version of BehavioralLimits strategy

### US-523320: [CDH] API for Retrieving System Data Sources from Context Dict

**Epic:** Adopt Profile Merge for Identity Stitching · **Story points:** 1 · **Status:** Resolved-Rejected

> As a CPD data admin, I want an API to retrieve the list of internal data sources so I can merge all CDH data sources To work correctly, the platform data definition will need the list of internal data sources. So that CPD can provide these platform data sources to the platform profile the context dictionary will need to be updated to provide this data source list to CPD

**Acceptance criteria:**
- Platform provides an API which can be implemented in the CDH layer
- CDH layer identifies the internal sources for Journey stages and ActionInsights

### US-525167: Ability to refresh persona details to match existing customer

**Epic:** CPV Supports Explain results and better Persona management · **Story points:** 5 · **Status:** Resolved-Completed

> As an NBA Specialist, I want to refresh my Persona to match the existing customer it is based off of, so that my Persona is up to date.

**Acceptance criteria:**
- Update all information other than 'General' section of a persona (by skipping the following) - Name - Description - Tags

### US-527176: Lock & Roll of Treatments on Edit

**Epic:** CPV Supports Explain results and better Persona management · **Story points:** 5 · **Status:** Resolved-Rejected

> As a NBA designer, I want the <treatments>DDR to lock & roll on create or update of treatments so this roll doesn't happen when viewing the landing page

**Acceptance criteria:**
- Remove Lock & Roll logic on the treatments landing pages
- Add Lock & Roll logic to the creation of treatments
- Add Lock & Roll logic to the update of existing treatments
- Confirm this doesn't cause issues in 1:1 Operation manager
- Ensure this continues to work in RM context

### US-533194: Support for Treatment Lever Weighting

**Epic:** Enrich Treatments with External Metadata for Better AI Insights · **Story points:** 8 · **Status:** Resolved-Completed

> As a NBA Designer, I want to upweight a specific treatment, not all treatments on the action, so I can lever up and be sure the treatment is presented for a specific inbound placement

**Acceptance criteria:**
- Users can set the TreatmentWeight on the treatment ruleform. This includes both internal and external treatments. Note: use the slider control from action ruleform
- TreatmentWeight property is seamlessly added to Treatment DDRs on upgrade
- Add a Treatment upweighting toggle to the Arbitration tab of NBA Designer in the Business levers section. Present this option below the existing Action weighting toggle. it should follow same pattern
- Add Treatment weighting property to Total weighting overlay in Prioritization view
- Add Treatment weighting property to Weighting view in CPV grid
- On upgrade, add the "Treatment weighting" row to the BusinessControlSettings DDR. (This row exists in Engine version of DDR)

## Pega Infinity '23

### US-507127: [Adoption] Migrate shipped pega CDH DDRs to new architecture

**Epic:** pyEditElement re-architecture and Dec Data performance updates · **Story points:** 3 · **Status:** Resolved-Completed

> Migrate all the shipped pega CDH DDRs to new edit element architecture Following are the rules that needs to be migrated

**Acceptance criteria:**
- when shipped DDRs are opened , new edit element should be in place of pyEditElement

## Customer Decision Hub '24.1

### US-559917: Ability to designate whether Persona is in/out specific test

**Epic:** Close Personas Gaps in Operations Manager · **Story points:** 3 · **Status:** Resolved-Completed

> As an NBA Specialist, I'd like to be able to designate whether Persona is always in or out of a specified Impact Analyzer test so that I can test my use cases with a known outcome.

**Acceptance criteria:**
- Should be incorporated into UI
- User can indicate whether this persona should participate in an impact analyzer test or not (Boolean)
- If a user has indicated that they want to participate in an impact analyzer test they can optionally indicate the specific Impact analyzer test
- This selector needs to be included anywhere a persona is created: - Create from scratch - Create from file - Create from existing customer

### US-566735: Redesign the contact policy association and action delete logic

**Epic:** Release Improvements · **Story points:** 8 · **Status:** Resolved-Completed

> As a developer, I want to refactor the Contact policy associated codebase so I can improve its performance, readability and extensibility

**Acceptance criteria:**
- Remove the dependencies of the contact policy requestor level data page while the action is in the edit state
- Remove the dependency of “pzOriginalInsKey” on action delete and identify a different approach to handle the delete more efficiently.
- The new design approach for action deletion should be compatible with RM, Ops, and Customer Decision Hub

### US-573262: Data model, Underlying Infra and UI

**Epic:** Provide an Application Overview · **Story points:** 3 · **Status:** Resolved-Completed

> As an NBA designer, I want a data model to collect and store usage and key configuration info so I can make this info available to automations and activities that request it

**Acceptance criteria:**
- Provide a reliable and extensible Data model to support the Application overview
- Overview data can be refreshed at a specified interval and stored for later use
- User has a dedicated landing page to see the current overview of their application
- The App Overview job scheduler should run on every environment
- Expose an API to retrieve data only available on Production which will be called from BOE
- The API is secured and requires proper authentication

### US-573300: Collect Data for Customer Data & Base Count

**Epic:** Provide an Application Overview · **Story points:** 2 · **Status:** Resolved-Completed

> As a NBA designer, I want an automation to retrieve specific information about the Customer Profile definition and counts as well as customer attributes so I can include this in the Application Overview

**Acceptance criteria:**
- Automation to get Context and associated data in context dictionary.
- Automation to get the aggregated customer Attributes.
- Automation to get the Customer/Prospect counts in an application.
- Make sure all modules should be independent and can be utilized as part of Autopilot

## Customer Decision Hub '24.2

### US-582566: Case Flow - 'Create Brand Voice'

**Epic:** Analyze Content to formulate the Brand Voice · **Story points:** 8 · **Status:** Resolved-Rejected

> As a marketer, I want to create my Brand Voice, so that I can generate more consistent content to my organizations mission.

**Acceptance criteria:**
- Case Intialaization: - Name Case - Describe reason for New Global Directive - Completion Date - Attachments
- Voice Details - Name Voice - Describe objective of voice - Language - Issue/Group - Icon - How would you like to formulate? (GenAI vs. Manual Input)
- Formulate with Gen AI - Example Treatment Upload Stage (Internal & External) - Treatment Analysis Stage - Finalize Voice Stage
- Manually Input - Finalize Voice Stage

### US-582567: Sample Content Voice Analyses

**Epic:** Analyze Content to formulate the Brand Voice · **Story points:** 8 · **Status:** Resolved-Completed

> As a marketer, I want to use my organizations existing content to inspire my Brand Voice, so that consistency is maintained across the content I make.

**Acceptance criteria:**
- GPT Analyzes Sample Content Subject Line and Body Separately as two individual portions of a piece of content
- Analyze the two portions of a piece of content for: - Syntatics - Semantics - Sentiment
- Breakdown language of each individual section within the two portions for: - Intent and use - Emotions - Narrative Style - Keywords - Urgency

### US-600440: Tech debt - Adopt Contact Policy architecture in Ops Mgr

**Epic:** 24.2 Technical Debt · **Story points:** 8 · **Status:** Resolved-Rejected

> As a developer, I want Operations Manager to adopt the new Contact Policy architecture so it's using the latest code base

**Acceptance criteria:**
- Adopting CP new architecture in OpsMgr

### US-609779: Deleting a Brand Voice & Global Directive

**Epic:** Analyze Content to formulate the Brand Voice · **Story points:** 5 · **Status:** Resolved-Rejected

> As a Team Lead, I want the ability to delete a Brand Voice and Global Directive so I can remove inactive or Voice that are no longer needed

**Acceptance criteria:**
- Users have the ability to Archive a Brand Voice and Global Directive
- On deployment the brand voice & Global Directive will be withdrawn and no longer appear for selection
- Users can view archived Brand voices & Global Directive and bring them back
- Users can make an archived brand voice & Global Directive active again

### US-610564: Improve Make Decision Experience in CPV

**Epic:** Arbitration & Action Level Testing in BAU · **Story points:** 5 · **Status:** Resolved-Rejected

> As a NBA designer, I want to refactor the Make decision tab of CPV so the user experience is improved and more capabilities fit into this compact space

**Acceptance criteria:**
- Refactor the Context area to include a light box and the Make decision button is anchored to the right side of this box
- Capture interaction area is refactor to support additional functions such as clear IH and behavioral data
- Refactor the Filter by Feature results grid to display PASSED or FILTERED badges to make interpretation of column easier
- Refactor the column headers to be easier to understand

### US-613182: Treatment generation using brand voice

**Epic:** Smarter Content Generation with GenAI · **Story points:** 5 · **Status:** Resolved-Completed

> As a marketer, I want be able to select a Brand Voice to use for treatment generation, so I can create consistent treatments

**Acceptance criteria:**
- Tone will be replaced with brand voice drop down
- Brand voice drop down will be first and then cialdini principal
- User is able to preview prompt used to generate their content: Display in the prompt the complete brand voice summary and the global directives applied alongside any other information passed to gpt to generate the treatment

### US-614750: MISC Brand Voice UI/UX Updates

**Epic:** Analyze Content to formulate the Brand Voice · **Story points:** 8 · **Status:** Resolved-Rejected

> As a marketer, I want to create brand voices, so I can use them to create smarter content.

**Acceptance criteria:**
- Remove default selection of voice from all flows and locations (Create brand voice, Update brand voice, Tile view, etc.)
- Remove select usage step all together in Create brand voice, update brand voice flows.
- Move active/inactive selection & issue and group selection into additional configurations section at the bottom of define attributes step (Create brand voice flow, update brand voice flow)
- Add rank to all cases - follow customer journeys layout
- Remove issue and group keys on backend

### US-626087: Multi-Level Contact Policies: Limit Tracking Context

**Epic:** Improved flexibility of Contact policies & IH · **Story points:** 3 · **Status:** Resolved-Completed

> As a NBA Designer, I want the ability to track Contact policies at the Primary context level or below so I can suppress Actions at different context levels

**Acceptance criteria:**
- Users can track contact policies at the primary context or below
- Users can suppress actions for any context, including above primary

## Customer Decision Hub '25.1

### US-650070: Build email from selected templates

**Epic:** Basic Email Authoring in CDH Portal · **Story points:** 5 · **Status:** Resolved-Completed

> As a marketer, I want to select a template when creating an email so I can be sure my email conforms to brand guidelines and format

**Acceptance criteria:**
- New email treatments display a placeholder with button in Content tab allowing a user to select an email template
- Users can select from the library of templates
- Upon selecting a template, the Content tab will switch to the email building plugin
- Define data model and rule type for templates

### US-650074: Browse through saved templates (CDH & 1:1 Ops)

**Epic:** Basic Email Authoring in CDH Portal · **Story points:** 5 · **Status:** Resolved-Rejected

> As a marketer, I want to be be able to browse and filter templates, so I can quickly find the most appropriate template

**Acceptance criteria:**
- Show hover preview
- Search templates
- Filter through template

### US-651452: Refactor Progress bar in CPV tabs

**Epic:** Planned '25 Technical Debt · **Story points:** 5 · **Status:** Resolved-Completed

> As a developer I want to refactor the progress bar in the Decision and Interaction history tabs So it better reflects the current progress

**Acceptance criteria:**
- In certain scenarios, the data flow can enter an infinite loop, which lacks proper error handling and can lead to severe performance issues.
- The system displays generic error messages for all error types, offering no specific information to assist in troubleshooting.
- The progress bar does not show the actual loading progress for DH and IH tabs, leading to a confusing user experience.

### US-657618: Preview & Test Email Treatments - II

**Epic:** Basic Email Authoring in CDH Portal · **Story points:** 3 · **Status:** Resolved-Rejected

> As a NBA Designer I want to preview and test the email I just created So I can be sure they look as I intended

**Acceptance criteria:**
- The Test Subject Line is automatically prefixed with [Test] so users know this is a test email
- Validate the use cases related to Send test email (positive and negative). Take care of error handling.
- Finalize UX(desktop and mobile views,element to adjust the email preview size e.g., zoom in/out)
- Pega Unit coverage

### US-659520: Plan Stage Users select & plan an Email Template

**Epic:** Basic Email Authoring in Ops Manager · **Story points:** 8 · **Status:** Resolved-Rejected

> As a Business User I want to plan an internal email treatment So I can pass the details to the content builder

**Acceptance criteria:**
- While adding a treatment to an Action, Users select Internal email and New option
- Users select a Template to be used in email building
- Template is read-only, no changes can be made
- Users can add Details of the treatment in the Details tab. All details are optional

### US-662392: Template Selection as a Template Editor

**Epic:** Basic Email Authoring in CDH Portal · **Story points:** 5 · **Status:** Resolved-Rejected

> As a Template editor I want the option to see both organizational and Pega curated templates when creating emails So I can pick the appropriate template when creating emails

**Acceptance criteria:**
- A Content specialist persona only sees organizational templates when selecting a template for email creation
- A Template editor can switch between organizational templates which is the default view or Pega curated templates by toggling between these options
- There are separate set of Categories for organizational and Pega curated templates which are displayed accordingly
- Handle review comments: 1. Templates having blank category. 2. Spacing issues. 3. Clear and selected text should get cleared off 4. Any additional review comments captured.

### US-674286: Adopt Ability to Disable DDR Import/Export

**Epic:** Raptors Technical Debt for '25 · **Story points:** 3 · **Status:** Resolved-Completed

> As a product I want to disable the ability to import/export rows from select DDRs So I can prevent customers getting into trouble (out of sync with rules)

**Acceptance criteria:**
- Identify list of DDRs to prevent import/export
- Collaborate with Dragons and other CDH teams (Champions may be) on disabling the bulk import of DDR.

### US-674682: BeeFree Pega Component to Include Section Rules

**Epic:** Basic Email Authoring in Ops Manager · **Story points:** 5 · **Status:** Resolved-Completed

> As a Content Editor I want to add a Pega component to my email So I can reuse existing Pega section rules in my emails

**Acceptance criteria:**
- Pega Component available in BeeFree component panel
- Once placed in the email, user can click on it to select the Pega section rule
- Include section rules in PegaMKT-Work which are available

## Customer Decision Hub '26.1

### US-650088: Actions contain a Marketing Message - GenAI enabled

**Epic:** Better Treatment Planning and Building using GenAI · **Story points:** 5 · **Status:** Resolved-Completed

> As a Business User, I want to define a Marketing Message for an Action So I can have a consistent set of features provided to GenAI to generate consistent treatments

**Acceptance criteria:**
- Users can optionally define a Marketing Message on the Create & Update Action CRs in the Plan stage
- Users can manually copy/enter a marketing message into the text area
- Users can use GenAI to analyze existing pdf, file or url to have a marketing message automatically generated
- Ensure backwards compatibility.
- This property should appear whether GenAI is turned ON
- When analyzing text,file or url marketing brief. the following should be output by the LLM and used as the Marketing message Product Name If Product association is checked, include name. Otherwise assume it's part of the marketing message Product Cat…

### US-704721: Extend Treatment Sets data model to Other Ops CRs

**Epic:** Enhanced Collaboration & HTML Editing · **Story points:** 5 · **Status:** Resolved-Rejected

> As a Business User In plan stage, I can create/update a new/existing treatment as part of updating an Action in a Treatment Set (tabbed layout) So I can make multiple updates to the Action all at once

**Acceptance criteria:**
- Extend tabbed layout capability, available in Create Action flow, to Update Action flow
- This new capability can be controlled via Toggle in the Operations Manager Settings LP
- Create Action and Update Action features continue to work with no regressions.

### US-710364: Refine Treatment case from Update Action Change Request

**Epic:** Enhanced Collaboration & HTML Editing · **Story points:** 5 · **Status:** Resolved-Rejected

> As a NBA Specialist I can create a new email treatment or Update an existing email treatment as part of updating an Action So I can make multiple updates to the Action all at once

**Acceptance criteria:**
- Users can create/Update a new email treatment as part of the Update Action CR
- Handle Review task, In plan stage of Update Action, for new Internal email treatment
- System shows difference (Edited and Original value) for IE in plan stage
- Stabilizing Update Action > Update internal treatment

### US-745323: Manage email treatment details

**Epic:** Email Authoring in AMO · **Story points:** 3 · **Status:** Resolved-Completed

> As a marketer, I want the AMO agent to allow me to manage email treatment details, such as language, eligibility, and UTM parameters, so I can ensure the email is targeted and trackable.

**Acceptance criteria:**
- User can set the language for the email
- User can define the eligibility criteria for the email
- User can set the UTM parameters for the email
- User can preview the email with the applied treatment details

## RLS-38673

### ENHANCEMENT-15218: Nightly Trigger for Orchestrator Agent

**Feature:** Email Outreach Product · **Status:** Open-InProgress

> As a system administrator, I want the Orchestrator Agent to be triggered automatically on a nightly schedule, So that seller engagement data is analyzed and emails are pre-drafted before sellers begin their workday. Criteria The Orchestrator Agent initiates automatically at a configurable nightly time (default: 11:00 PM local time per seller's timezone). The trigger is idempotent — if a run fails, it can be safely re-triggered without duplicate output. A system log entry is created for each nightly run with start time, completion time, and status (Success / Partial / Failed). No manual intervention is required to initiate a standard nightly run.

## RLS-37112

### ENHANCEMENT-1995: Support Dark Mode Preview for Emails

**Feature:** Email Treatments · **Status:** Pending-Blocked

> Intent : Deliver an in-editor dark mode preview that gives content leads and content specialists a fast, reliable first-pass check before external validation. The enhancement should fit directly into normal authoring flow so teams can preview, adjust, and recheck without leaving the editor. Problem : Teams currently rely on test-send and external review loops to evaluate dark mode rendering, which slows iteration and increases rework. The lack of in-editor visibility creates uncertainty about contrast, logo treatment, button visibility, and image behavior until late in QA. That friction is especially costly for high-volume campaign teams balancing speed, compliance, and brand consistency. Wh…

### ENHANCEMENT-2114: Plain Text Email Generation / Preview

**Feature:** Email Treatments · **Status:** Resolved-Completed

> We are adding an in-editor plain text email preview and edit ability so content leads and content specialists can quickly verify readability, formatting, and link clarity for text-only recipients before test send. This should reduce QA rework, improve accessibility and deliverability confidence, and catch text-version issues earlier in authoring

## -

### TASK-1618537: Ui suggestions for brand voice tile

**Status:** Resolved-Completed

> Ui suggestions for brand voice tile. To have a fixed height of tile and show ellipsis for extra trimmed characters

### US-608928: Manage Emergency Exclusions in Production

**Epic:** Raptors Technical Debt for '26 · **Story points:** 8 · **Status:** Resolved-Completed

> As a NBA Designer, I want the ability to add an Emergency Exclusion to my production environment so I can immediately remove an Action or Treatment from being decisioned

**Acceptance criteria:**
- Emergency Exclusion landing page is available on the runtime Production env as a left menu item. This page is not available on any env other than production
- User can add an Action level exclusion
- User can add a Treatment level exclusion
- These exclusions are written to the EmergencyExclusions DDR in open/unlocked production ruleset
- EmergencyExclusions DDR is locked & rolled if required
