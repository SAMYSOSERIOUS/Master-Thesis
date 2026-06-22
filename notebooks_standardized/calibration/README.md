# calibration — Stabilization, Multi-Seed and Calibration

The final "within-one" push: stabilizing the distance-weighted trainer, repeating
it across seeds for a variance estimate, and combining seeds into a calibrated
ensemble. No new data is introduced here — these notebooks make the *existing*
method reliable and well-calibrated.

## Scientific rationale

A good point estimate is not enough for a thesis claim; the result must be
**stable** (not seed luck), **calibrated** (predicted probabilities mean what they
say), and **robust** at the decision boundary. These three notebooks address those
in order: fix the optimization, measure variance over seeds, then ensemble +
calibrate to extract the final defensible number.

## Notebooks

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `w1_v2_stabilized.ipynb` | Re-engineers the within-one trainer with three fixes: **gentle capped distance weighting**, a **class-balance penalty**, and a **divergence detector** with checkpoint reversion. | The first attempt diverged on NHANES and collapsed KL1 on OAI; each fix targets one observed failure mode — diagnosing and correcting, not retrying blindly. |
| `w1_day2_v2_three_seeds.ipynb` | Repeats the stabilized trainer for seeds 1 and 2 (seed 0 already exists) on OAI and NHANES; skips any seed already computed. | Multiple seeds turn a single number into a mean ± spread, the minimum standard for a credible deep-learning result. Skip-if-exists makes the run idempotent. |
| `w1_day3_v2_ensemble_calibration.ipynb` | Combines the three seeds per fold into an ensemble with **test-time augmentation**, then fits a **per-dataset decision-threshold calibration** on validation and applies it once to test. No training. | Ensembling + TTA reduce variance; validation-only threshold fitting corrects systematic bias without touching the test set — the definitive, leakage-free within-one score. |

## Method notes

- **Divergence detection + checkpoint reversion** — treats training stability as a measurable, controllable part of the method.
- **Multi-seed protocol** — the standard defense against cherry-picked runs.
- **Validation-fit, test-apply calibration** — strict separation so calibration never sees the test labels.
- **Test-time augmentation** — averages predictions over input transforms to lower variance at inference.
