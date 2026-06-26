# Evaluation — Post-hoc Result Analysis (no training)

Inference-free evaluation notebooks that re-analyze the **predictions already
saved** by the fold experiments. Neither notebook trains a model; both reuse
stored probability vectors, so every result here is reproducible in minutes and
cannot introduce optimistic bias.

## Scientific rationale

Once the experiments have produced predictions, several questions can be answered
without retraining: *How much of the accuracy difference from prior work is an
artifact of the grading scheme rather than the harder multi-dataset setting?* and
*Does averaging independent seeds give a small, free accuracy gain?* Answering
these from saved predictions keeps the analysis honest (the model is fixed) and
cheap (no GPU training).

## Notebooks

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `scheme_comparison.ipynb` | Re-bins the saved 5-class predictions under three grading schemes — original 5-class, prior-work 4-category (KL-3/4 merged), and 4-category with the ambiguous boundary removed (KL-0/1 merged) — and recomputes accuracy, weighted F1, and QWK for each held-out dataset. | Prior work reported a 4-category result on a single dataset; re-grading both labels and predictions identically makes the comparison **fair** and isolates how much difference is due to scheme vs the harder LODO setting. |
| `seed_ensemble.ipynb` | Averages the three per-seed validation probability vectors per fold, takes the argmax, and recomputes in-domain 5-class accuracy and QWK against the single-seed mean. | Averaging independent seeds reduces variance and typically yields a small, free accuracy gain; showing the single-seed mean alongside makes the **ensemble gain directly visible**. |

## Method notes

- **Prediction-level re-analysis** — the model is frozen; only the scoring changes, so results are unbiased and instantly reproducible.
- **Consistent re-binning** — class merges are applied to truth and predictions together, otherwise the comparison would be invalid.
- **Seed ensembling** — variance reduction by averaging independent runs, the standard low-cost robustness technique.
- **Metrics** — accuracy, weighted F1, and quadratic weighted kappa (QWK), the latter respecting the ordinal nature of KL grades.
