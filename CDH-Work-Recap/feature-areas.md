# Feature Areas: What I Built (Pega Customer Decision Hub)

[← Back to index](README.md)

Each section below covers one feature area: the **user stories (features)** I delivered, the main **bug and hotfix themes**, and the **skills** the work used. See [timeline-by-year.md](timeline-by-year.md) for every item.

---

## 1. Email Authoring: BeeFree Editor & Templates (2024 – 2026)
My main area in recent years. I brought a drag-and-drop email editor (BeeFree) into CDH and built the template experience on top of it.

**Features**
- US-650070: Build an email from selected templates
- US-650074: Browse saved templates (CDH and 1:1 Ops Manager)
- US-662392: Template selection when acting as a template editor
- US-659520: Plan-stage users can select and plan an email template
- US-674682: BeeFree Pega component that can include section rules
- US-657618: Preview and test email treatments (part II)
- ENHANCEMENT-2114 / HFIX-D3455: **Plain-text and multipart email** generation and preview. This included BeeFree content-conversion endpoints, an email content processor, error-stream handling, connection cleanup and read-timeout settings, written in **Java (mktcodesets)** with JUnit tests and Playwright automation
- Synced-fragment support in BeeFree authoring; BeeFree authentication changes for staging
- ENHANCEMENT-1995: Dark-mode email preview (PR open)

**Bug / hotfix themes:** CTA and fields missing in the Enhanced Email Authoring tool (HFIX-D2352), issue/group defaulting to "ALL" (HFIX-D1493), RV generation for update change requests, the subject line not matching its preview, editor not shown inline on always-on actions, Content Landing Page template issues, and email-account validation.

**Skills:** Pega UI and sections, REST connectors, Java HTTP clients, JavaScript editor callbacks, third-party SaaS integration.

---

## 2. Brand Voice & GenAI (2024 – 2026)
Features that use generative AI to create marketing content in a company's brand voice.

**Features**
- US-582566: "Create Brand Voice" case flow
- US-582567: Voice analysis of sample content (including reading .docx files)
- US-609779: Deleting a brand voice and its global directive
- US-613182: **Generating treatments using a brand voice**
- US-614750 / TASK-1618537: Brand Voice UI/UX improvements and the brand voice tile
- US-650088: Actions that contain a GenAI-enabled marketing message
- ENHANCEMENT-15218: Nightly trigger for the Orchestrator Agent (PR open)

**Bug / hotfix themes:** GenAI connection failures (HFIX-B2462), support for Bedrock models, adopting platform Connect-GenAI rules, archiving brand voices through change requests, ruleset mismatches, CDH Assistant and SDE AI Assistant fixes.

**Skills:** GenAI prompt integration, Pega Connect-GenAI, case design, the Pega change-request lifecycle.

---

## 3. Treatments & Channels (2022 – 2026)
The largest area by item count. It covers creating, editing, versioning and importing email, SMS and custom-channel treatments.

**Features**
- US-471810: Revert to a previous version of a treatment
- US-476973: Dynamic SMS messages
- US-527176: **Lock & Roll** of treatments on edit
- US-533194: Treatment lever weighting
- US-503308: Treatments Landing Page support for custom channels
- US-710364: Refined treatment case from an Update Action change request
- US-704721: Treatment Sets data model extended to other Ops change requests

**Bug / hotfix themes:** bulk import/export, treatment joins lost after upgrade (HFIX-C2691), treatments removed from actions (HFIX-C3035), treatment eligibility and property filters, language values not kept on import, validation (dates, business weight, names), and internal/external email previews.

---

## 4. Customer Profile Viewer (CPV) & Personas (2021 – 2026)
The tool marketers use to simulate and explain next-best-action decisions for a customer or persona.

**Features**
- US-477041: CPV support for Customer Journey decisions
- US-515727: CPV support for Channel Context
- US-610564: Better Make Decision experience
- US-651452: Refactored progress bar in CPV tabs
- US-501811: Default summary view on the Persona landing page
- US-525167: Refresh persona details to match an existing customer
- US-559917: Mark whether a persona is in or out of specific tests
- US-523320: API to retrieve system data sources from context
- US-573262 / US-573300: Data model, infrastructure, UI and automations for customer data and base count

**Bug / hotfix themes:** wrong eligibility/engagement-policy explanations (HFIX-C4616), IH/DH (Interaction History / Decision History) not loading for personas and external IDs, propensity and priority columns, channel-context placements, and the default Prioritization view.

---

## 5. Contact Policies & Emergency Exclusions (2023 – 2026)
Rules that limit how often customers are contacted.

**Features**
- US-513683: Contact policies support placement type
- US-522200: BehavioralLimits strategy uses GOS
- US-566735: **Redesigned** contact-policy association and action delete
- US-600440: Adopted the new contact-policy architecture in Ops Manager
- US-626087: **Multi-level contact policies** that limit the tracking context
- US-608928: **Managing emergency exclusions in production**

**Bug / hotfix themes:** placement-type creation (HFIX-C1292), ContactPolicyJoins DDR in revisions, invalid policies showing up in search, and missing tracking/suppression context.

---

## 6. Ops Manager, Change Requests & Revisions (2022 – 2026)
The 1:1 Operations Manager portal that business users use to ship changes safely.

**Features**
- US-460665: Action landing page supports withdrawn actions
- US-507127: Migrated the shipped CDH DDRs (data-driven rules) to the new architecture
- US-506723: Merge activity for ActionInsights2
- US-674286: Option to disable DDR import/export

**Bug / hotfix themes:** change requests failing in the Plan stage (HFIX-B187), IndexOutOfBounds after the 8.8 upgrade (HFIX-B244), a customer-reported automated CR failure (INC-B4669), dependency checks for withdraw, bulk archival (HFIX-C2511), and automated insights.

---

## 7. App Overview, Localization & Platform Alignment
- Hardening of the App Overview (style, Pega Cloud values, performance and impression metrics)
- Localization fixes for CDH 8.23 and 8.24 (for example, Dutch)
- Aligned access groups with Infinity Studio and removed App Studio
- HFIX-D28: Enabled holdout experiments; fixed pxPriority in container responses
- Local dev tooling: created missing operators, access groups and applications

---

## 8. Test Automation & Quality
- **Selenium / Cucumber** (2022 – 2025): kept the PMFramework/PMTests suites stable (xpaths, waits, bulk-import and CPV flows)
- **Playwright** (2026): Infinity Studio setup steps and plain-text preview automation
- **PegaUnit**: fixed suites that were blocking merges and removed redundant tests
- **Karate API tests**: DX API update-action scripts
- T-47965: Aligned Raptors test tags across master, 25.1 and 26.1
- Used **Spec-Kit** (spec → plan → tasks) and AI coding agents for the plain-text preview work
