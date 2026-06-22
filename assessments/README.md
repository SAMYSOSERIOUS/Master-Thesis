# Assessments

This folder contains radiographic assessment datasets and their accompanying
documentation from the Osteoarthritis Initiative (OAI). Each subfolder holds a
specific category of knee or hip X-ray readings, provided as comma-separated
`.txt` data files together with PDF descriptors (variable contents, statistics,
and reader comments).

## File types

- `*.txt` — tabular data (CSV format) with subject IDs, reading project/version,
  side, follow-up visit grades, and cohort information.
- `*_Contents.pdf` — variable/column descriptions for the corresponding dataset.
- `*_Stats.pdf` — summary statistics for the corresponding dataset.
- `*_Comments.pdf` / `*_Descrip.pdf` — reader notes and methodology descriptions.

## Subfolders

| Folder | Files | Description |
| --- | --- | --- |
| `Alignment/` | 67 | Knee alignment readings (KneeAlign and FTA — femoro-tibial angle) from the Cooke and Duryea reading projects across multiple follow-up visits. |
| `XR Hip Semi-Quant/` | 16 | Semi-quantitative hip OA status gradings (UCSF reading project) at baseline and follow-up visits, per hip side. |
| `XR Knee Quant JSW/` | 43 | Quantitative knee joint space width (JSW) measurements (Duryea reading project), including absolute and relative/change values across visits. |
| `XR Knee SC Bone/` | 10 | Knee subchondral bone texture / bone-trabecular-integrity readings (FNIH BTI, Duke reading project). |
| `XR Knee Semi-Quant/` | 50 | Semi-quantitative knee OA gradings (KXR_SQ, Boston University reading project), including absolute grades and reliability/relative re-read datasets. |

## Notes

- Filenames encode the reading project and the follow-up visit number
  (e.g. `00` = baseline, `01`, `03`, `05`, `06`, `08`, `10`, `12` = later visits).
- Missing or non-readable values use OAI conventions such as `.M:missing`,
  `.T:poor quality`, and `.J:excluded for medical reasons`.
- The `_rel_` files contain reliability re-reads or relative (change-from-baseline) measures.
