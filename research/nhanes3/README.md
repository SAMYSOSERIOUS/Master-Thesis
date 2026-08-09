# nhanes3 — NHANES III Cohort

Acquisition, processing and labelling of the **NHANES III** knee radiographs — a
population-representative US survey cohort used as a second expert-labelled
training/generalization source.

> **Role in the final thesis:** NHANES III is the independently acquired,
> expert-labelled target cohort for the protected OAI-to-NHANES evaluation. The
> final pipeline reconstructs its cohort and freezes participant-level splits in
> [`../../Final Notebook/`](../../Final%20Notebook/).

## Scientific rationale

NHANES III was acquired with different equipment and on a broader, community-based
population than OAI. Including it tests whether models transfer across **population
and acquisition shift**, not just across random splits of one cohort. Processing
it into the *same* 224×224 grayscale format as OAI guarantees that any performance
difference is biological/demographic rather than format-driven.

## Notebooks

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `nhanes3_batch_process.ipynb` | Downloads every bilateral knee X-ray from the CDC FTP and processes each to a 224×224 PNG; long-running, checkpointed, background-safe. | Reproducible bulk acquisition; checkpointing after each image makes a ~9-hour job interruptible and resumable without re-downloading. |
| `nhanes3_labels.ipynb` | Extracts KL grades for both knees, cross-references against the processed PNGs, and writes **stratified** train/val/test CSVs. | Cross-referencing guarantees every label has a matching image; stratification preserves the KL-grade distribution across splits so evaluation is unbiased. |

## Method notes

- **Identical preprocessing to OAI** — same resize/CLAHE target so cohorts are directly comparable.
- **Stratified splitting** — KL grades are imbalanced (most knees are grade 0–1);
  stratifying prevents rare severe grades from landing entirely in one split.
- **Image–label cross-reference** — protects against silent misalignment between
  the CDC data file and the processed images.

## Reproducibility Boundary

The acquisition notebook is network-dependent and may be long-running. Preserve
source identifiers, image-label joins, and participant-level grouping when
rerunning it. Store downloaded images, manifests, and generated reports on
Google Drive rather than local Colab storage.
