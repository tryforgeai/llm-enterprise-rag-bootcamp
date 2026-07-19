# T020 Week 06 Class Capture

Status: doing

Date: 2026-07-18

## Goal

Capture Week 06 material on request-side guardrails (the gatehouse), response-side grounding (the conscience), and refusal/humility (the honest "no" and the honest partial), and connect it to Avaloka's access control, grounding, and abstention needs.

## Working File

`course/week-06.zh.md`

## Source

`summer-week-6-lesson-plan.pdf` (local Downloads copy of the Week 6 lesson plan, *The Two Gates of the Gatehouse*, Asif Qamar / SupportVectors)

## Done Criteria

- [x] Lesson-plan PDF is read in full (52 pages) and summarized.
- [x] Two-gates / two-virtues frame (security vs integrity) is recorded precisely.
- [x] Four request-side threat families and their detectors are recorded.
- [x] Indirect prompt injection (PoisonedRAG, spotlighting) is distinguished from direct injection.
- [x] RAGAS triad, assertion-evidence bipartite graph, and judge pathologies are recorded.
- [x] Escalation ladder economics and the false-positive tax are recorded.
- [x] Three doors of refusal and graded humility (verbalized uncertainty, conformal abstention) are recorded.
- [x] Eight labs are summarized.
- [x] Essential and optional readings are recorded.
- [x] Connection to Weeks 01-05 and to Avaloka is drafted.
- [x] Live classroom screenshots for Act IV, Coda, and three beyond-the-deck supplements (governance/policy/guardrails/security/trust terminology, guardrailed-RAG and guardrailed-agent reference architectures, "examples by gate" controls ①-②) are transcribed and integrated into `course/week-06.zh.md`.
- [ ] Live classroom discussion / instructor's spoken commentary on the above screenshots is still missing — only the slide content itself has been captured.
- [x] Act IV (Landscape) and Coda (The Honest Machine) are captured — these appear on the live "Map of the Day" slide but are not in the source PDF's table of contents; content now sourced entirely from live screenshots (guardrail-framework landscape, Phoenix observability, fundamental asymmetry, base-rate curse, defense-in-depth product, worked latency budget, pattern language, four verbs, five crafts, journey map).
- [ ] "Examples by gate" controls ④-㉔ (RAG) and A-H (agent) still lack concrete worked scenarios — only controls ①②③ (format/secret gate, input-quality/anti-abuse, PII detection & redaction) have scenario-level detail so far. However, both the Gate-1 (request rails) AND Gate-2 (response rails) tools-and-frameworks tables are now captured, covering all 18 request+response gate controls at the tool-selection level even without individual worked scenarios for ④-⑰.
- [x] A runnable end-to-end pipeline demo now exists: `course/week_06/guardrailed_rag_pipeline_demo.py` implements the "Project Atlas" reference-architecture gates 1-4, 7 (gates 5/6/8 stubbed), 9-10, mocked generation, and response-rails gates 11-17 (including a real conformal-abstention threshold), composing the two prior demo files. This is not one of the 8 formally-scoped labs but does satisfy the spirit of "at least one lab implemented" for the request+response gate mechanics — Lab 6/7's actual precision/recall ablation numbers on a real eval set are still open.
- [ ] At least one of the 8 formally-scoped labs (Lab 6 or Lab 7 preferred) is implemented against a real eval set with measurable precision/recall numbers — the new pipeline demo is a mocked architecture walkthrough, not an ablation study.
- [ ] A Week 06 eval artifact is created (e.g. request-side guardrail ablation table or grounding faithfulness score on an existing demo).
- [ ] Avaloka application section is revised from "initial mapping" to a concrete design.

## 2026-07-18 Update

Created the first Week 06 record from the lesson-plan PDF:

- two-gates / two-virtues framing (request-side security vs response-side integrity) and why RAG is more exposed than a bare chatbot on three axes
- Act I: Swiss-cheese cost-ordered gatehouse, four threat families (malformed/evasive, adversarial intent, access/identity, abuse/economics), indirect injection via PoisonedRAG as the RAG-native threat, spotlighting as the cheapest effective defense, RBAC as a pre-retrieval filter, the confused-deputy pattern, the false-positive tax (0.99^16 ≈ 85%)
- Act II: groundedness/faithfulness formal definition, RAGAS triad, assertion-evidence bipartite graph algorithm, NLI vs LLM-judge cascade and judge pathologies (self-preference, verbosity, position bias), the four-tier escalation ladder economics, citation faithfulness (ALCE), and the four remedies for a caught hallucination
- Act III: three doors of refusal (security/permission/grounding) and their asymmetric disclosure rules, refusal (binary/values) vs humility (graded/epistemic), verbalized uncertainty, four uncertainty signal sources, conformal abstention's distribution-free coverage guarantee, and the base-rate trap under calibration
- summarized all 8 labs and the required/optional reading list
- drafted an initial Avaloka mapping (RBAC pre-filter for memory retrieval, assertion-evidence grounding for advice, graded refusal/humility for uncertain or out-of-scope memory questions) — flagged as needing course-day refinement

## 2026-07-18 Update (later in the day — live-class screenshots)

Added Act IV, Coda, and three beyond-the-deck supplements to `course/week-06.zh.md`, transcribed from live Zoom screenshots shared during class (not present in the source lesson-plan PDF):

- Act IV: guardrail-framework landscape (programmable rails/NeMo, validator libraries/Guardrails.ai, classifier models/Llama Guard+Prompt Guard, managed services/Azure+Bedrock) organized by detection philosophy not vendor; Phoenix/OpenTelemetry observability; the fundamental AND/OR asymmetry between defense and attack plus GCG adversarial suffixes; "security is a garden, not a wall" and red-teaming tooling (HarmBench, JailbreakBench, PyRIT, garak); the base-rate curse precision formula; defense-in-depth as a product of independent miss-probabilities and why correlated holes break it; the full guardrailed-RAG pipeline diagram; a worked P50 latency budget table
- Coda: a 10-pattern/5-anti-pattern wheel keyed to "the two gates"; the four verbs (defend/ground/refuse/confess); "never wrong in the dark" as the redefinition of trust; the five-crafts-one-discipline diagram (skill/memory/prompt/harness/guardrail all routing through context) and why guardrails come last but are not least important; the closing journey-recap curve
- Beyond the deck: a governance/policy/guardrails/security/trust terminology table and concentric-circle diagram (with an HR-assistant worked example); where explainability fits relative to observability, governance, and trust; a fully numbered (24-control) guardrailed-RAG reference architecture; an extended guardrailed-AI-agent reference architecture (gates A-H covering tool selection, MCP provenance, sandboxing, human-in-the-loop, loop budget control, memory poisoning); the first two entries (controls ①② — format/secret-pattern gate, input-quality/anti-abuse) of an "examples by gate" specification document
- Updated the concept table, the "still missing" list, and the review-question list in `course/week-06.zh.md` to reflect the new material; controls ③-㉔ of the examples-by-gate document and the agent gates A-H remain uncaptured with concrete scenarios and should be backfilled if shown again in class

## 2026-07-18 Update (control ③ + tools table)

Added two more live screenshots to `course/week-06.zh.md`:

- "Examples by gate" control ③ — PII detection & redaction (SSN-in-query and support-agent-PII scenarios; Presidio/AWS Comprehend PII/Google Cloud DLP/Nightfall) — the pattern across ①②③ is now recorded as regex-pattern → statistical-feature → NER-entity, three escalating detection sophistication levels
- A consolidated "Request rails — tools & frameworks" table covering all 9 request-side gate controls with named tools per control (format/secret gate, input quality, PII, prompt-injection/jailbreak, multi-turn/long-context jailbreak, toxicity, intent/topic, deobfuscate-then-inspect, spotlighting, ACL/RBAC-at-retrieval) — notably multi-turn/long-context jailbreak has no named product (self-build territory) and spotlighting is explicitly flagged as an architectural pattern, not a product
- Controls ④-㉔ (RAG) and gates A-H (agent) still lack concrete worked scenarios; the tools table gives partial coverage for the remaining request-side controls but response-side (⑨-⑰) and agent-loop (B-G) controls have neither scenarios nor a tools table yet

## 2026-07-18 Update (tool glossary)

Added a "工具清单速查" (tool glossary) subsection right after the Gate-1 tools table, explaining what each named tool actually is (vendor, open-source vs. commercial vs. managed-cloud-service) for every product named in the request-rails table — Guardrails.ai, Protect AI LLM Guard, Rebuff, Presidio, AWS Comprehend PII, Google Cloud DLP, Nightfall, Protecto, Llama Prompt Guard 2, Azure AI Prompt Shields, Lakera Guard, Vigil, NeMo Guardrails, Llama Guard 3, OpenAI Moderation API, Azure AI Content Safety, Bedrock Guardrails, Detoxify, Perspective API, Pinecone/Weaviate/Milvus, Azure AI Search. Closes with a three-way vendor taxonomy (managed cloud service / open-source self-hosted / dedicated security startup) to guide future tool selection.

## 2026-07-18 Update (Gate 2 tools table + Colang mechanics)

Added the Gate-2 (response rails / "the conscience") tools-and-frameworks table, covering all 9 response-side controls: atomic-claim decomposition (FActScore, RAGAS, custom LLM decomposer), groundedness/faithfulness (RAGAS, TruLens groundedness triad, DeepEval, Vectara HHEM, Azure Groundedness detection, DeBERTa-based NLI), hallucination detection (SelfCheckGPT, Semantic Entropy, Vectara HHEM leaderboard), uncertainty/conformal abstention (custom only), citation/attribution (ALCE, Vectara, LlamaIndex/LangChain), trichotomy routing (custom + NeMo output rails), templated hedging (custom only), output safety/PII/toxicity (same tools as Gate 1's input-side moderation, reused on output), and helpful-refusal templates (custom only). Flagged the key finding: roughly half of Gate 2's rows are "custom" with no named product, unlike Gate 1 where nearly every row has 4-7 options — response-side/conscience tooling is markedly less commoditized than request-side/gatehouse tooling, confirming the Act IV "guardrail landscape mostly covers request-side" observation and marking this as the area needing the most in-house build effort.

Also recorded (in chat only, not yet in the .md file) a detailed explanation of Colang's actual runtime mechanics — canonical-form matching via embeddings before any LLM call, deterministic flow-graph state transitions requiring no LLM when a flow matches exactly, direct Python action execution with no LLM involvement, and few-shot LLM prompts assembled dynamically from Colang-defined examples only at genuinely ambiguous decision points. Consider folding this into the NeMo Guardrails / Colang section of week-06.zh.md if it proves durably useful, since it clarifies "how Colang actually talks to the LLM" — currently the file names Colang as a tool but doesn't explain its invocation mechanism.

## 2026-07-18 Update (Gate 2 tool glossary + jailbreak-vs-injection distinction)

Added a "工具清单速查（Gate 2 / 响应侧）" subsection mirroring the Gate 1 glossary — standalone vendor/open-source/academic-method descriptions for every tool in the Gate 2 table (FActScore, RAGAS, TruLens, DeepEval, Vectara HHEM + leaderboard, Azure Groundedness detection, DeBERTa-based NLI models, SelfCheckGPT, Semantic Entropy, ALCE, Vectara's enterprise RAG product, LlamaIndex, LangChain, NeMo output rails, and the reused Gate-1 output-safety tools). Explicitly requested by the user to be reusable reference material for other projects, not just this course.

Also discussed in chat (not yet folded into the .md) the conceptual distinction between prompt injection (control-flow hijacking — exploits the lack of a syntactic boundary between data and instructions; direct vs. indirect subtypes) and jailbreaking (safety-alignment bypass — exploits gaps in RLHF-trained refusal generalization; DAN persona, Crescendo, many-shot, GCG suffixes, translation jailbreaks). Noted that "ignore previous instructions" style DAN attacks sit at the intersection of both, while indirect injection (PoisonedRAG) is usually pure injection with no jailbreak goal, and Crescendo/many-shot are usually pure jailbreak with no injection mechanic. The current Family B section of week-06.zh.md blurs these together under "对抗意图" without drawing this distinction explicitly — worth a dedicated clarifying paragraph if revisited.

## 2026-07-18 Update (Project Atlas diagram + runnable pipeline demo)

Captured a live screenshot of "Project Atlas — end-to-end guardrail flow" (a Word doc shown in class) — a unified diagram merging the RAG (24-control) and Agent (A-H) reference architectures into one renumbered scheme (1-17 + B-G), applied to a named example system, with an explicit API-gateway/WAF infrastructure layer and a dedicated "early refuse / short-circuit" diagram node not present in the earlier abstract architectures. Recorded in `course/week-06.zh.md` under the "Project Atlas" subsection.

Also wrote and validated a new runnable demo, `course/week_06/guardrailed_rag_pipeline_demo.py`, implementing Project Atlas gates 1-4/7 (request rails, cost-ordered, short-circuiting), 9-10 (ACL-bound retrieval + spotlighting), mocked generation, and 11-17 (response rails, including a working conformal-abstention threshold using the exact formula from Act III). It composes the two pre-existing demo files (`pii_redaction_demo.redact`, `indirect_injection_defense_demo.spotlight_*`). Four scenarios all verified working: a clean query where the planted PoisonedRAG-style document (hr-03) organically ranks #1 by lexical relevance yet is neutralized by spotlighting regardless of rank; a direct-injection attempt short-circuiting at gate 4; an out-of-clearance query where ACL excludes the confidential doc as a candidate (not a post-hoc hide); and a leaked-credential query short-circuiting at gate 1. This is a mocked architecture walkthrough (no real LLM/ML calls), not one of the 8 formally-scoped labs — see the updated "still missing" checklist above for what real Lab 6/7 work would still require.
