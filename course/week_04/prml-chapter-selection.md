# PRML Chapter Selection For Abstractive Summarization

Date: 2026-06-27

## Goal

Choose two PRML chapters for the Week 04 abstractive summarization and retrieval experiment.

The experiment will use real textbook material to test derived retrieval artifacts:

- raw chunks
- abstractive summaries
- factoids
- QA pairs
- source-grounded evidence pointers

## Selected Chapters

### Chapter 2: Probability Distributions

Approximate range:

- Book pages: 67-136
- PDF pages: 86-155

Why this chapter is useful:

Chapter 2 introduces the probability distributions that become building blocks for later machine learning models. It is concept dense and suitable for summary-based indexing because the chapter contains many related but distinct ideas.

Important topics:

- Bernoulli distribution
- beta distribution
- multinomial variables
- Dirichlet distribution
- Gaussian distribution
- conditional and marginal Gaussian distributions
- Bayes' theorem for Gaussian variables
- maximum likelihood
- Bayesian inference
- Student's t-distribution
- mixtures of Gaussians
- exponential family
- conjugate priors
- nonparametric methods
- kernel density estimators
- nearest-neighbour methods

High-level summary target:

> Chapter 2 explains how probability distributions represent uncertainty, how their parameters can be estimated from data, and how conjugacy, Gaussian structure, mixture models, and nonparametric methods provide reusable tools for pattern recognition.

### Chapter 3: Linear Models For Regression

Approximate range:

- Book pages: 137-177
- PDF pages: 156-196

Why this chapter is useful:

Chapter 3 turns probability and estimation ideas into supervised prediction. It is a good pair with Chapter 2 because it shows how distributions and likelihoods become regression models.

Important topics:

- linear basis function models
- maximum likelihood and least squares
- geometry of least squares
- sequential learning
- regularized least squares
- multiple outputs
- bias-variance decomposition
- Bayesian linear regression
- predictive distribution
- equivalent kernel
- evidence approximation

High-level summary target:

> Chapter 3 explains linear regression as a supervised learning problem, showing how basis functions, least squares, regularization, Bayesian inference, and evidence optimization produce predictive models for continuous targets.

## Why Not Chapter 1 First

Chapter 1 is useful as an overview, but it mixes many introductory themes:

- curve fitting
- probability theory
- model selection
- curse of dimensionality
- decision theory
- information theory

For the Week 04 experiment, Chapter 2 and Chapter 3 are better because they form a tighter technical sequence:

```text
Chapter 2: probability distributions and uncertainty
-> Chapter 3: regression models and prediction
```

This makes the abstractive summaries easier to evaluate.

## Planned Retrieval Artifacts

For each selected chapter, create multiple artifact types:

```text
PRML chapter text
-> section chunks
-> chapter-level abstractive summary
-> section-level abstractive summaries
-> key concepts
-> factoids
-> QA pairs
-> embeddings
-> local JSON index or Qdrant later
```

Each synthetic artifact should keep a pointer back to the source evidence:

```json
{
  "artifact_type": "abstractive_summary",
  "source_doc": "PRML.pdf",
  "chapter": 2,
  "source_pages": [86, 155],
  "source_chunk_ids": ["prml_ch2_001", "prml_ch2_002"]
}
```

## Demo Direction

Build a Week 04 UI that compares:

1. Raw chunk retrieval
2. QA-pair retrieval
3. Abstractive-summary retrieval

Example questions:

- What is the role of the Gaussian distribution in PRML?
- How does Bayesian inference appear in Chapter 2?
- What is the relationship between least squares and maximum likelihood?
- Why are basis functions useful in linear regression?
- What is the bias-variance decomposition?

Expected lesson:

> Raw chunks are useful for local evidence, QA pairs are useful for query-shaped retrieval, and abstractive summaries are useful for high-level conceptual questions. A good RAG system may index all three while grounding final answers in the original source text.

