# Enterprise RAG Architecture Visual Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a LinkedIn-ready Enterprise RAG architecture diagram, editable source, browser preview, and synchronized three-minute narration.

**Architecture:** Use one self-contained SVG as the source of truth for the visual. Wrap that SVG in a lightweight HTML preview and render it to a 1600 x 900 PNG with the workspace browser runtime. Keep the narration in Markdown and verify its terminology against labels in the SVG.

**Tech Stack:** SVG, HTML/CSS, Node.js browser rendering, Markdown, shell verification

---

### Task 1: Create The Editable Architecture Source

**Files:**
- Create: `reviews/enterprise-rag-agent-architecture.svg`

- [x] **Step 1: Build the 1600 x 900 SVG canvas**

Create a self-contained SVG with a deep navy background, editorial title area, four
layered architecture bands, arrows, and a compact legend. Do not use external fonts or
images.

- [x] **Step 2: Add the approved system labels**

Include:

```text
Experience Layer
Agent Control Plane
Enterprise Data & Action Plane
Observability & Improvement
Intent + Identity
Authorize + Scope
Retrieval Plan
Decide Next Step
Generate Response
Verify + Guard
Document Pipeline
Permitted Retrieval
Authoritative Sources
Approved Tools
Trace
Evaluate
Human Review
Improve
```

- [x] **Step 3: Confirm the trust boundaries**

The primary flow must show authorization before retrieval. The observability layer must
span the full architecture. The diagram must not label GraphRAG, RAPTOR, or learned
reranking as implemented capabilities.

### Task 2: Create The Browser Preview

**Files:**
- Create: `reviews/enterprise-rag-agent-architecture.html`

- [x] **Step 1: Create an accessible preview wrapper**

Embed the SVG in a responsive page with a dark presentation background and explanatory
metadata.

- [x] **Step 2: Add LinkedIn posting guidance**

Below the visual, include the suggested image title and a concise post caption.

- [x] **Step 3: Verify the file is self-contained**

Run:

```bash
rg -n 'https?://|src=' reviews/enterprise-rag-agent-architecture.html
```

Expected: no external asset dependency.

### Task 3: Write The Three-Minute Narration

**Files:**
- Create: `reviews/enterprise-rag-three-minute-video-script.md`

- [x] **Step 1: Write a timed English narration**

Use six sections:

```text
0:00-0:25
0:25-1:00
1:00-1:35
1:35-2:10
2:10-2:40
2:40-3:00
```

- [x] **Step 2: Add recording directions**

Include what to point at on the diagram and where to pause.

- [x] **Step 3: Verify word count**

Run:

```bash
sed '/^#/d;/^>/d;/^-/d;/^$/d' reviews/enterprise-rag-three-minute-video-script.md | wc -w
```

Expected: approximately 380 to 420 spoken words.

### Task 4: Render And Inspect The LinkedIn PNG

**Files:**
- Create: `reviews/enterprise-rag-agent-architecture.png`

- [x] **Step 1: Render the HTML at 1600 x 900**

Use the workspace browser runtime to open the local preview and capture the diagram
canvas at 1600 x 900.

- [x] **Step 2: Verify file dimensions**

Run an image metadata check.

Expected:

```text
width: 1600
height: 900
```

- [x] **Step 3: Inspect full-size and thumbnail views**

Confirm that the title, six control-plane steps, three data-plane components, and four
observability labels remain readable. Confirm there is no clipping or overlap.

### Task 5: Record The Deliverables

**Files:**
- Modify: `tasks/T010-ai-career-positioning-cv-linkedin.md`

- [x] **Step 1: Add all four deliverables**

Record the SVG, PNG, HTML preview, and narration paths.

- [x] **Step 2: Add verification evidence**

Record PNG dimensions, visual inspection, and narration word count.

- [x] **Step 3: Check decision logging**

Confirm this visual communication artifact does not change project architecture,
evaluation policy, scope, memory policy, or folder structure. No decision-log update is
required.
