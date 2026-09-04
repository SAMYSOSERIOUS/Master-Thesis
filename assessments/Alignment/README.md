# Alignment — Knee Alignment and Femoro-Tibial Angle Readings

Central measurements of lower-limb alignment from OAI radiographs: the **KneeAlign** anatomic-axis readings (Cooke and Duryea reading projects) and the **FTA** (femoro-tibial angle) measurements (Duryea), across baseline and follow-up visits.

> **Role in the thesis.** Not used by the final pipeline. Alignment is retained as part of the complete OAI image-assessment documentation set; the thesis's three radiographic concepts are osteophytes, joint space narrowing and sclerosis, all of which come from [`../XR Knee Semi-Quant/`](../XR%20Knee%20Semi-Quant/).

## What is in this folder

| File pattern | Content |
|---|---|
| `flxr_kneealign_cooke01.txt`, `FLXR_KneeAlign_Duryea01/03/05/06.txt` | Full-limb alignment readings per visit and reading project |
| `KXR_FTA_DURYEA00/08/12.txt` | Femoro-tibial angle measured on the knee films |
| `*_Contents.pdf` / `*_Stats.pdf` | Data dictionary and summary statistics for the matching `.txt` |
| `*_Comments.pdf` | Reader comments per visit and project |
| `flXR_KneeAlign_Descrip.pdf` | Methods description of the alignment reading protocol |
| `ImageAssessmentDataOverview.pdf` | OAI overview of all image-assessment datasets |

## Notes

- The visit code in each filename (`01`, `03`, `05`, `06`, `08`, `12`) follows the OAI convention; `00` is baseline.
- Two reading projects (Cooke, Duryea) measured alignment with different protocols; consult the `_Descrip` and `_Comments` PDFs before combining them.
- Read-only source files; derived data belong on Google Drive.
