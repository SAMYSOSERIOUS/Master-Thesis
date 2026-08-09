# mrkr - Emory Knee Radiograph Dataset (MRKR)

Acquisition and preprocessing of the **MRKR** (Emory) knee radiographs — the
large historical source in the exploratory pipeline, but with **model-predicted
(pseudo) KL labels** rather than expert annotations.

> **Status:** ancillary exploratory source. MRKR is not the independently
> expert-labelled target cohort for the final OAI-to-NHANES thesis evaluation.

## Scientific rationale

MRKR adds scale and diversity, but its labels are produced by a model, so they are
noisy. The scientific value is twofold: (1) more data and a third acquisition
domain for generalization, and (2) a realistic test of **learning from weak
supervision** — the labels are treated as noisy and handled downstream by
confident-learning quality scores and curriculum weighting (see `pipeline_v1`).
Matching MRKR images to the exact OAI/NHANES format keeps the only difference the
label quality, not the pixels.

## Notebooks

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `mrkr_download.ipynb` | Connects to the HITI S3 store, downloads the 210 MB metadata index of 503,261 images, filters to thesis-relevant studies, then downloads only those DICOMs. | Filtering from the index first avoids wasting bandwidth/storage on images that will never be used — measure before you fetch. |
| `mrkr_preprocess_part1.ipynb` | DICOM → 224×224 **CLAHE** PNG, splitting bilateral films into per-knee crops with correct left/right orientation; retry logic for Drive FUSE indexing. | Produces pixels in the same format as OAI/NHANES so MRKR is a drop-in source; orientation handling matches the OAI convention; retries absorb cloud-storage latency. |

## Method notes

- **Pseudo-labels = noisy supervision** — explicitly acknowledged and managed, not assumed clean.
- **Index-first filtering** — the 210 MB CSV is the cheap proxy used to plan an expensive download.
- **Format parity with OAI/NHANES** — identical CLAHE + 224×224 so cross-dataset effects are isolated to content and labels.

## Reproducibility Boundary

MRKR's pseudo-labels make it appropriate for weak-supervision and data-quality
experiments, not a substitute for expert-held-out validation. The acquisition
notebooks can be expensive and require authorized S3 access; keep downloaded and
generated artifacts on Google Drive. The final protected evaluation is documented
in [`../../Final Notebook/`](../../Final%20Notebook/).
