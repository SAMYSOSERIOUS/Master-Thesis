# mrkr — Emory Knee Radiograph Dataset (MRKR)

Acquisition and preprocessing of the **MRKR** (Emory) knee radiographs — the
largest source in the study, but with **model-predicted (pseudo) KL labels**
rather than expert annotations.

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
