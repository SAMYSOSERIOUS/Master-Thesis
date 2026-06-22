# diagnostics — Why Does the External Gap Exist?

Read-only diagnostic notebooks that ask a single causal question: when the model
loses accuracy on an external dataset (notably Mendeley), is the gap caused by
**labels** (different grading conventions, recoverable by re-fitting boundaries) or
by **images** (a genuine feature-level domain shift, irreducible)?

## Scientific rationale

An external accuracy drop is ambiguous — it could be fixed cheaply (relabel /
recalibrate) or be a hard limit of the data. Distinguishing the two changes what
the thesis should conclude and what future work should attempt. The diagnostic is
deliberately **read-only** (no training, no fitting on the target) so it cannot
itself create the effect it measures. It uses the trained maximum model purely as
a frozen **feature extractor** and tests whether two datasets share a common
"severity axis" in feature space.

## Method (shared across all three notebooks)

1. Load the OAI-fold maximum checkpoint as a frozen backbone (fair severity representation — it never saw these as test data in-run).
2. Extract penultimate features for a bounded random sample from each dataset.
3. Learn a **severity direction** on OAI (LDA / logistic direction along which KL increases) and project both datasets onto it.
4. Test two things: does the OAI direction **order the other dataset's grades correctly** (Spearman), and do the per-grade severity distributions **overlap and increase monotonically**?

> If the axis is shared, the gap is largely *label/threshold* level (recoverable).
> If the other dataset sits apart or its grades don't separate, the gap is
> *feature* level (irreducible).

## Notebooks

| Notebook | Comparison | Why |
|----------|-----------|-----|
| `phase1_diagnostic.ipynb` | OAI vs **Mendeley** | The headline external set — is its gap labels or images? |
| `phase1_diag_oai_vs_nhanes.ipynb` | OAI vs **NHANES III** | Cross-checks the diagnostic on an expert-labelled cohort where the answer should be "shared axis". |
| `phase1_diag_oai_vs_mrkr.ipynb` | OAI vs **MRKR** | Tests the pseudo-labelled cohort, separating its label noise from any image-level shift. |

## Method notes

- **Frozen feature extractor** — isolates representation quality from any new optimization.
- **Linear severity axis (LDA/logistic)** — a single, interpretable direction makes the "shared axis?" question testable.
- **Spearman rank correlation** — checks ordering without assuming linear spacing of grades.
- **Read-only by design** — guarantees the diagnostic measures, rather than manufactures, the effect.
