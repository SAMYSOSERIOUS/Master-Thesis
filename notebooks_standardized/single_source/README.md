# single_source — Single-Dataset SOTA Baseline

A single-source experiment: train one strong model on **OAI alone** and evaluate
how well it transfers to the other three datasets in the same run.

## Scientific rationale

The thesis argues that **multi-source** training improves generalization. To prove
that, a fair single-source baseline is needed: maximise accuracy on one
well-curated dataset, then honestly report how much accuracy is lost on unseen
cohorts. OAI is chosen as the training source because it has the cleanest,
expert-graded labels. The internal→external gap measured here is the **honest cost
of training on a single source**, and it is the number the multi-dataset method
(studied in `pipeline_v1`) must beat.

## Notebook

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `single_dataset_sota.ipynb` | Trains the full-accuracy model on OAI's training split only, holding NHANES III, MRKR and Mendeley entirely out, then evaluates on all three external sets in the same run. The multi-dataset mechanisms (curriculum, domain-adversarial) are **switched off**. Reports in-domain OAI accuracy/QWK and external transfer, saved to JSON. | Disabling the multi-source mechanisms is required for a clean baseline — they have no role with one source, so leaving them on would confound the comparison. Combining the three external sets into one tagged test set returns external metrics directly, with no checkpoint reload. |

## Method notes

- **Patient-level split** — OAI is split into train/validation by patient, so all images from one patient (both knees, every visit) stay on the same side. A random row-level split would leak the same patient into both splits and inflate accuracy.
- **Strict hold-out** — the other three datasets are never seen during training; their accuracy is pure out-of-distribution transfer.
- **Same model family as the multi-source runs** — keeps the single-source vs multi-source comparison fair (only the training data differs).
- **Metrics** — accuracy, quadratic weighted kappa (QWK), and AUC, reported for both in-domain and external evaluation.
