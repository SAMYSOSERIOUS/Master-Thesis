# XR Knee Quant JSW — Quantitative Joint Space Width

Computer-assisted **quantitative joint space width (JSW)** measurements of the OAI knee radiographs (Duryea reading project): absolute width in millimetres at fixed locations along the joint, per visit, plus test–retest reliability files.

> **Role in the thesis.** Not used by the final pipeline. The thesis's joint-space-narrowing concept is the semi-quantitative OARSI grade from [`../XR Knee Semi-Quant/`](../XR%20Knee%20Semi-Quant/), not the continuous JSW measurement; the quantitative readings are retained as documentation and as a candidate for future work on continuous severity targets.

## What is in this folder

| File pattern | Content |
|---|---|
| `kxr_qjsw_duryea00.txt` … `kxr_qjsw_duryea10.txt` | Quantitative JSW per visit (`00` baseline, then 12, 36, 60, 72, 96, 120 months) |
| `kxr_qjsw_rel_duryea00.txt` … `_05.txt` | Test–retest reliability measurements (Project 20) |
| `*_Contents.pdf` / `*_Stats.pdf` | Data dictionary and summary statistics for the matching `.txt` |
| `kXR_QJSW_Duryea*_Comments.pdf` | Reader comments per visit |
| `kXR_QJSW_Duryea_Descrip.pdf` | Methods: *Central Assessment of Longitudinal Knee X-rays for Quantitative JSW* |
| `kXR_QJSW_Rel_Duryea_Descrip.pdf` | Methods: *Test-Retest Reliability of Joint Space Width Measurements* |
| `ImageAssessmentDataOverview.pdf` | OAI overview of all image-assessment datasets |

Read-only source files; derived data belong on Google Drive.
