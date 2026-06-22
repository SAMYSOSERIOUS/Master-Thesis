# mt3 — Fused Multi-Task + Cascade Model

A single notebook that **fuses the two strongest modelling ideas** from the thesis
into one architecture and trains it on the OAI fold.

## Scientific rationale

Two independent improvements were found earlier: (1) the OARSI **sub-feature** heads
(`oarsi/`), which ground the representation in real pathology, and (2) a **binary
cascade** (KL≥1 screening, then KL≥3 severity), which mirrors how a clinician first
detects disease and then judges its severity. The scientific question is whether
these gains are **complementary** — i.e. whether combining them yields more than
either alone. Fusing them in one model is the direct experimental test.

## Notebook

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `mt3_fused_cascade_oai.ipynb` | Shared CORN backbone + KL head + masked OARSI sub-feature heads (osteophyte/JSN/sclerosis) + binary cascade heads (KL≥1, KL≥3); guarded single-fold training on OAI. | Tests whether sub-feature supervision and the screen-then-grade cascade stack additively; OAI is chosen because it carries the dense sub-feature labels both ideas need. |

## Method notes

- **Cascade decomposition** — splitting an ordinal task into ordered binary decisions follows clinical reasoning and can sharpen the hardest boundaries.
- **Masked multi-task heads** — reused from `oarsi/`, so missing sub-grades contribute no gradient.
- **Guarded training** — divergence detection / checkpoint reversion keeps the more complex fused model stable.
