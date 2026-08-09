# Research Notebooks and Exploratory Studies

This directory contains the acquisition, multi-source, calibration, diagnostic,
benchmark, and forensic work that informed the thesis. It is the canonical home
for research notebooks, but it is not the canonical final analysis sequence.
For the protected OAI-to-NHANES thesis workflow, start with
[`../Final Notebook/README.md`](../Final%20Notebook/README.md).

## How to Read This Directory

- **Final claims and protected evaluation:** use `Final Notebook/`.
- **Forensic provenance and preprocessing evidence:** use `novel/`.
- **Historical multi-source experimentation:** use `pipeline_v1/` and its
	supporting folders. Treat Mendeley-related external-validation results as
	retrospective evidence only, because the provenance audit identifies an
	OAI-derived relationship.

## Areas

| Location | Purpose | Status in thesis narrative |
| --- | --- | --- |
| [`calibration/`](calibration/) | Stabilization, multi-seed, and calibration studies. | Exploratory support. |
| [`diagnostics/`](diagnostics/) | Frozen-feature and generalization-gap diagnostics. | Historical diagnostic evidence. |
| [`docs/`](docs/) | Written reports and generated metadata. | Supporting records. |
| [`Evaluation/`](Evaluation/) | Prediction-level re-analysis and seed ensembles. | Historical re-scoring. |
| [`experiments/`](experiments/) | Ablations and maximum-configuration studies. | Exploratory upper-bound work. |
| [`mendeley/`](mendeley/) | Mendeley acquisition and lineage inputs. | Provenance/preprocessing control, not independent OAI validation. |
| [`mrkr/`](mrkr/) | MRKR acquisition and preprocessing. | Ancillary pseudo-label source. |
| [`mt3/`](mt3/) | Fused multi-task and cascade architecture study. | Exploratory model study. |
| [`nhanes3/`](nhanes3/) | NHANES III acquisition and labels. | Supports independent final target evaluation. |
| [`novel/`](novel/) | Provenance, paired preprocessing, and concept-policy studies. | Core forensic contribution. |
| [`oai/`](oai/) | OAI acquisition, labels, preprocessing, and QC. | Primary source-cohort preparation. |
| [`oarsi/`](oarsi/) | OARSI sub-feature extraction and multi-task studies. | Exploratory concept supervision. |
| [`pipeline_v1/`](pipeline_v1/) | Earlier multi-source LODO sequence. | Historical; interpret Mendeley folds cautiously. |
| [`single_source/`](single_source/) | OAI-only comparison baseline. | Historical baseline. |
| [`SOTA/`](SOTA/) | Dataset-specific benchmark notebooks. | Contextual comparisons. |

## Top-Level Notebook

`dataset_status.ipynb` records dataset availability and processing status for
the exploratory research workspace.
