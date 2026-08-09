# SOTA - Historical Dataset-Specific Benchmark Context

This folder holds dataset-specific comparison notebooks used to place exploratory
models alongside previously reported or reference benchmark settings. They are
contextual analyses, not the canonical final evaluation sequence.

## Notebooks

| Notebook | Scope |
| --- | --- |
| `oai_beat_sota.ipynb` | OAI-focused benchmark and reference-result comparison. |
| `nhanes_benchmark.ipynb` | NHANES III-focused benchmark comparison. |
| `mrkr_benchmark.ipynb` | MRKR-focused benchmark comparison with its pseudo-label caveat. |

## Interpretation Boundary

Benchmark definitions, preprocessing, label schemes, and split policies can
differ across prior studies. Read the notebook-specific source citations and
protocol notes before comparing metrics. Final protected claims are reported by
[`../../Final Notebook/`](../../Final%20Notebook/); store regenerated tables and
figures on Google Drive.
