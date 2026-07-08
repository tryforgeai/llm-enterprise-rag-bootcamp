# 2026-06-06 Afternoon Transformer And LARQL Record

Status: Captured

Captured on: 2026-06-06

Source:

- User-provided afternoon course and terminal notes
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- [LARQL](https://github.com/chrishayuk/larql)

Canonical synthesized notes:

- [Week 01](../week-01.md)

Related research note:

- [LARQL Learning Note](../../resources/tools/larql-learning-note.md)

## Coverage

This record captures:

- Hugging Face authentication and gated-model access
- a local Python SSL certificate failure involving a corporate proxy certificate
- Gemma access approval requirements
- The Illustrated Transformer as a visual foundation
- the flow through a modern decoder-only Transformer block
- the connection between attention, the residual stream, MLP/FFN features, and LARQL

## Hugging Face Setup Record

The terminal flow began with:

```bash
hf auth login
```

The CLI requested a token from:

- [Hugging Face access tokens](https://huggingface.co/settings/tokens)

A read token is sufficient for downloading models that the account is authorized to access. The token should be entered only in the terminal and must not be copied into course notes, source control, or chat.

After token validation, the prompt:

```text
Add token as git credential? [y/N]:
```

can be answered with the default `N` when the token is only needed by the Hugging Face CLI.

Verification command:

```bash
hf auth whoami
```

### SSL Failure

The first login attempt failed with:

```text
SSL: CERTIFICATE_VERIFY_FAILED
unable to get local issuer certificate
```

The accompanying troubleshooting record attributes this to a corporate Zscaler certificate that was not trusted by the Python environment's certificate chain. The record says Python was subsequently configured to use the macOS system certificate chain and an HTTPS connection test returned `200`.

This fix was reported in the supplied terminal record; it has not been independently reproduced inside this bootcamp project.

### Gated Gemma Access

The model download command was:

```bash
hf download google/gemma-3-4b-it
```

Authentication succeeded, but the download returned:

```text
Access denied. This repository requires approval.
```

This means the CLI token was valid, while the Hugging Face account had not yet accepted or received access to the gated Gemma repository.

Required next step:

1. Open the `google/gemma-3-4b-it` model page with the same account.
2. Request access or accept the Gemma license terms.
3. Confirm the CLI account with `hf auth whoami`.
4. Retry the download.

This is an account-level repository authorization issue, not necessarily a token-scope failure.

## The Illustrated Transformer

[The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) by Jay Alammar is a visual tutorial rather than a standalone book.

Recommended reading order:

```text
high-level Transformer view
-> self-attention intuition
-> self-attention in detail
-> multi-head attention
-> positional encoding
-> decoder
-> linear and softmax output
-> training and loss
```

Its main value for this course is building visual intuition before reading the equations in *Attention Is All You Need*.

## Decoder-Only Transformer Block

The screenshot discussed in class shows a token representation moving through a modern decoder-only Transformer block.

### Query, Key, And Value

Each token representation is projected into:

- **Query**: what the current token is looking for
- **Key**: what each available token offers for matching
- **Value**: the information that can be retrieved from each token

Attention weights are conceptually:

```text
attention weights = softmax(QK^T / sqrt(d_k))
```

The resulting contextual representation is:

```text
attention output = attention weights x V
```

### Causal Masking

In an autoregressive decoder, the current token can attend only to itself and earlier tokens. It cannot inspect future tokens.

```text
current position
-> current and previous positions visible
-> future positions masked
```

### Multi-Head Attention

Multiple attention heads use different learned projections. Each head can model different relationships or operate in a different representational subspace.

Conceptually:

```text
head 1 ... head N
-> concatenate
-> output projection
```

### Residual Stream

Attention does not replace the token representation. Its contribution is added to the residual stream:

```text
x' = x + Attention(x)
```

The MLP/FFN contribution is then also added:

```text
x'' = x' + MLP(x')
```

The residual stream is therefore the evolving shared representation that carries accumulated information across layers.

### MLP / FFN

The MLP or feed-forward network acts on each token position independently after attention has moved information between token positions.

A useful first approximation is:

```text
attention -> exchange or retrieve information across tokens
MLP / FFN -> transform, combine, and write learned features
residual stream -> preserve and accumulate both contributions
```

This is a simplification, but it is a productive mental model for beginning mechanistic interpretation.

## Connection To LARQL

LARQL becomes easier to understand once this block-level flow is clear:

```text
prompt tokens
-> attention contributions
-> FFN feature contributions
-> residual stream changes across layers
-> output-token preference
```

LARQL's relevant learning surfaces include:

- browsing model features and learned associations
- inspecting FFN-related feature neighborhoods
- tracing when a candidate answer rises in rank
- decomposing attention and FFN contributions
- experimenting with reversible patches only after read-only validation

The key boundary remains:

> An internal feature association or trace is evidence about model behavior, not externally grounded evidence that the claim is true.

## Agent-First Interpretation

This material strengthens the `trace` part of the project loop:

```text
intent -> retrieve -> decide -> respond -> trace -> evaluate
```

For ordinary RAG, a trace records retrieved evidence and decisions. For model-internals research, a trace may additionally record:

- token trajectory by layer
- attention versus FFN contribution
- when an answer becomes dominant
- changes caused by ablation, steering, or a patch
- whether the final answer remains grounded in external evidence

The model's internal trajectory can explain behavior, but it does not replace provenance, citations, or safety evaluation.

