# oai — Osteoarthritis Initiative (Primary Source)

Acquisition, preprocessing and labelling of the **OAI** knee radiographs — the
highest-quality, expert-graded cohort in the study and the reference against
which the other datasets are harmonized.

## Scientific rationale

OAI provides standardized bilateral knee X-rays with expert semi-quantitative
readings. Because its labels are trustworthy, OAI defines the **canonical image
format** (224×224 grayscale, CLAHE-enhanced) and the **reference KL scale** that
every other dataset is aligned to. Establishing a clean, leakage-free OAI base is
a precondition for any valid cross-dataset comparison.

## Notebooks

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `oai_download.ipynb` | Downloads OAIScreeningImages from the NIMH Data Archive via `nda-tools`, extracts, and keeps only the X-ray images. | Reproducible, authenticated access to the source-of-truth cohort; discarding non-X-ray content controls storage and scope. |
| `oai_preprocess.ipynb` | Reads bilateral DICOMs, splits each into left/right knee crops, applies **CLAHE** + resize to 224×224 PNG, checkpointed. | CLAHE equalizes local contrast so the joint space is visible across exposure conditions; a fixed size/format makes all cohorts comparable. Checkpointing makes a multi-hour job restartable. |
| `oai_labels.ipynb` | Extracts Kellgren–Lawrence grades from `KXR_SQ_BU00.txt` into `oai_labels.csv` (`subject_id, side, kl_grade`). | KL is the clinical gold-standard severity scale; tidy per-knee labels are the supervision signal for the whole project. |
| `oai_pipeline.ipynb` | Quality-control pipeline (S1 inventory match, S2 image integrity, ... ) with **check → fix → verify** stages. | Defensive data engineering: each check has an auto-fix and a re-verification, so the dataset is provably consistent before training. |

## Method notes

- **CLAHE (Contrast-Limited Adaptive Histogram Equalization)** — chosen over global
  equalization because it enhances the local joint-space region without amplifying noise.
- **Bilateral split + left-flip** — the left knee is mirrored to the right-knee
  orientation so the model sees a single consistent anatomy.
- **Check→Fix→Verify** — every QC step is idempotent and auditable, the engineering
  analogue of a controlled measurement.
