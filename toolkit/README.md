# Enterprise RAG Method Toolkit

This directory turns the bootcamp's course notes and lab code into a reusable,
project-independent method library.

The toolkit is deliberately implementation-neutral. It does not require Avaloka,
SupportVectors infrastructure, one model vendor, one vector database, or a fixed
clone location. Original course code remains the evidence and worked-example
layer; these documents explain how to select, adapt, trace, and evaluate each
method in another project.

## Start Here

1. Use [method-catalog.md](method-catalog.md) to find methods by problem.
2. Copy [project-adoption-template.md](project-adoption-template.md) into the
   target project's planning or decisions folder.
3. Select the smallest baseline that can expose the failure.
4. Record the baseline, metric, cost, safety boundary, and removal criterion.
5. Link the adopted implementation back to its method ID.

## Method Families

| IDs | Family | Typical question |
|---|---|---|
| F01-F04 | Foundations | How do tokens, probabilities, embeddings, and attention behave? |
| R01-R07 | Representation | What should become a retrievable unit? |
| I01-I06 | Indexing and retrieval | How should candidates be stored and recalled? |
| Q01-Q04 | Query processing | How should the user's intent become a retrieval query? |
| G01-G04 | Graph retrieval | When does graph-shaped memory help? |
| S01-S07 | Safety and grounding | What may enter, be retrieved, or leave the system? |
| E01-E09 | Evaluation | Which stage failed, and did a change really help? |
| A01-A04 | Agent and learning loops | How does retrieval support a bounded decision loop? |

## Reuse Contract

Every adoption should preserve:

- a named user or system failure
- a transparent baseline
- inputs, outputs, and provenance
- permission and privacy boundaries
- at least one measurable success criterion
- latency, token, compute, and maintenance costs
- an observable trace
- an exit or removal criterion

Do not copy a technique merely because it is newer or more complex. Dense
retrieval, reranking, late chunking, GraphRAG, fine-tuning, and agent memory are
interventions whose value must be demonstrated against a simpler baseline.

## Portability Rules

- Use repository-relative paths in committed files.
- Put secrets and machine-specific values in ignored environment files.
- Keep provider, model, database, and endpoint choices configurable.
- Save generated artifacts separately from source methods.
- Do not copy SupportVectors-restricted source into another repository unless
  its license permits it; reimplement from the method description instead.
- Preserve citations to papers, notes, or original code when adapting a method.

## Relationship To Existing Material

- `resources/notebook-methods-kb.md` is the detailed notebook-derived knowledge
  base.
- `course/` preserves weekly learning history and equations.
- `labs/` and runnable files under `course/` provide implementations and
  experiments.
- `toolkit/` is the stable cross-project selection and adoption interface.

## Maintenance

When adding a method:

1. Assign a stable family ID.
2. Add a catalog entry with selection and evaluation guidance.
3. Link evidence from `course/`, `labs/`, `resources/`, or a paper.
4. Mark maturity as `concept`, `demo`, `integrated`, or `validated`.
5. Add a task if validation or portability remains incomplete.
6. Record a decision if the addition changes architecture, evaluation, safety,
   memory policy, or the toolkit structure.
