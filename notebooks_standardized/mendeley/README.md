# mendeley — External Hold-Out Set

Acquisition and preparation of the **Mendeley/Kaggle Knee Osteoarthritis** dataset.

> **Role: hold-out only.** This dataset is *never* trained on. It is the external
> benchmark used to measure true out-of-distribution generalization.

## Scientific rationale

The strongest test of generalization is a dataset the model has never seen in any
form — different institution, scanner and labelling pipeline. Mendeley serves as
that independent yardstick (the "leave-one-dataset-out" target in several folds).
Keeping it strictly hold-out prevents any optimistic bias: every number reported
on Mendeley is honest external performance.

## Notebooks

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `mendeley_download.ipynb` | Downloads the Mendeley/Kaggle KL-graded dataset, processes images to the project format, and writes `mendeley_holdout.csv` plus a KL-distribution plot. | Establishes a clean, format-matched external benchmark; the distribution plot documents class balance so external results can be interpreted in context. |

## Method notes

- **Strict train/test hygiene** — hold-out status is enforced by convention and by the LODO protocol; leakage here would invalidate the headline generalization claim.
- **Format harmonization** — images are normalized to the same intensity/size as training data (see `pipeline_v1/03_mendeley_harmonize.ipynb`) so an external accuracy drop reflects domain shift in content, not preprocessing mismatch.
