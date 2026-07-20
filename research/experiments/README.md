# experiments — Ablations and Maximum-Configuration Studies

Exploratory and "maximum-effort" notebooks that extend the primary pipeline:
adjacency-tolerant evaluation, a self-contained ordinal training library, and a
single-fold **maximum model** tested on each dataset.

## Scientific rationale

The main pipeline answers the core research questions; these notebooks probe the
*ceiling* and the *interpretation* of the results. Part of the work asks "how good
can one fold get if every technique is stacked?" (the MAX configuration), and part
asks "are the remaining errors clinically meaningful?" (adjacency metrics). Both
are needed to argue the method's results are both strong and sensible.

## Notebooks

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `20_bonus_adjacent_softlabel.ipynb` | Part A: adjacency-tolerant metrics (exact vs within-±1 accuracy, off-by-one rate) from saved predictions. Part B: retrains on the Mendeley fold with **soft ordinal labels**. | A single-grade KL error rarely changes management, so within-±1 accuracy is the clinically honest metric; soft labels stop penalizing the model for placing mass on adjacent (and plausibly correct) grades. |
| `max2_ordinal_lib.ipynb` | Self-contained 5-class **CORN** ordinal training library with all max-config settings baked in (resolution, freeze level, LR, MRKR trust, curriculum). | Encapsulating the full stack in one library makes the maximum-model runs reproducible and decoupled from the main config. |
| `max3_max_single_fold.ipynb` (+ `_oai`, `_mrkr`, `_nhanes`) | Trains the maximum configuration (CORN head, full fine-tune, 384×384, soft targets, reliability weighting, sampling, curriculum, domain-adversarial) on each fold and compares to baseline H. | One variant per held-out dataset shows the ceiling is consistent across cohorts, not a one-fold artifact; the baseline comparison quantifies the stacked gain. |

## Method notes

- **Adjacency-tolerant metrics** — match the ordinal, clinical nature of KL; a large within-1 − exact gap means errors are boundary confusions, not gross misclassifications.
- **Soft / ordinal labels (CORN)** — respect grade ordering and label uncertainty.
- **Higher resolution (384²) + full fine-tune** — the "spare no expense" upper bound, deliberately separated from the efficient main pipeline.
