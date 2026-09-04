# XR Knee Semi-Quant — Central KL and OARSI Readings of Knee Radiographs

**The one assessment set the thesis actually uses.** These are the Boston University (BU) central readings of the OAI knee radiographs: the Kellgren–Lawrence grade and the individual OARSI-style features — osteophytes, joint space narrowing and sclerosis — per compartment, per knee, per visit.

> **Role in the thesis.** The final pipeline derives every OAI label from the baseline file `KXR_SQ_BU00.txt`: the KL grade (`V00XRKL`) and the three concepts as the per-knee maximum across compartments (`V00XROS*` → osteophytes, `V00XRJS*` → joint space narrowing, `V00XRSC*` → sclerosis). See [`../../Final Notebook/`](../../Final%20Notebook/) (`N01`) and [`../../research/oai/`](../../research/oai/) (`oai_labels.ipynb`), and the OARSI extraction in [`../../research/oarsi/`](../../research/oarsi/).

## What is in this folder

| File pattern | Content |
|---|---|
| `KXR_SQ_BU00.txt`, `kxr_sq_bu01.txt` … `KXR_SQ_BU12.txt` | Absolute readings per follow-up visit (`00` = baseline, then months 12, 24, 36, 48, 72, 96, 120…), one row per subject, side and reading project |
| `kxr_sq_rel_bu00.txt` … `kxr_sq_rel_bu06.txt` | Reliability re-reads (paired duplicate readings) used to estimate reader agreement |
| `*_Contents.pdf` | Variable-by-variable data dictionary for the matching `.txt` file |
| `*_Stats.pdf` | Frequency tables and summary statistics for the matching `.txt` file |
| `*_Comments.pdf` | Reader notes per visit |
| `kXR_SQ_BU_Descrip.pdf` | Methods: *Central Reading of Knee X-rays for Kellgren & Lawrence Grade and Individual Radiographic Features of Tibiofemoral Knee OA* |
| `kXR_SQ_Rel_BU_Descrip.pdf` | Methods for the reliability re-reads |
| `ImageAssessmentDataOverview.pdf` | OAI overview of all image-assessment datasets |

## Variable naming

`V{visit}XR{feature}{compartment}` — for example `V00XROSFM` = visit 00, X-ray, **os**teophyte, **f**emur **m**edial; `V00XRJSL` = joint space narrowing, lateral; `V00XRSCTL` = sclerosis, tibia lateral; `V00XRKL` = KL grade. Missing-value codes follow OAI conventions (`.M` missing, `.T` poor image quality, `.J` excluded for medical reasons).

## Notes

- Not every knee with a KL grade has feature readings; the thesis's concept-complete OAI cohort (5,252 knees) is the subset with all three features present, whereas the KL-only universe used by the exploratory `N06A` extension is larger (8,547 knees).
- Do not edit these files. Derived tables belong in the Google Drive artifact tree documented by the final pipeline.
