# mendeley - Acquisition and Provenance Audit Input

This folder contains acquisition and preparation work for the Mendeley/Kaggle
knee osteoarthritis resource. It belongs to the exploratory multi-source
pipeline, not the canonical final OAI-to-NHANES evaluation.

## Current Interpretation

The provenance work in [`../novel/`](../novel/) found that the Mendeley resource
is OAI-derived for the overlapping knees examined. It must therefore not be
described as an independent external validation cohort when OAI is in the
training source. Historical leave-one-dataset-out results involving Mendeley are
useful for tracing preprocessing and data-lineage effects, but they are not
independent OAI-to-Mendeley transfer estimates.

The derived relationship is scientifically useful: paired OAI and Mendeley
representations of the same knee support a controlled analysis of how image
processing can change predicted findings and KL grade without changing anatomy
or the reference label.

## Notebook

| Notebook | Role | Main products |
| --- | --- | --- |
| `mendeley_download.ipynb` | Downloads and prepares the Mendeley/Kaggle images for the historical multi-source pipeline. | Processed images, `mendeley_holdout.csv`, and a KL-distribution summary. |

## Use Boundaries

- Do not use this folder's outputs as evidence of independent external
	performance for OAI-trained models.
- Do not combine Mendeley and OAI as independent cohorts in a final statistical
	analysis.
- Use the canonical final pipeline in [`../../Final Notebook/`](../../Final%20Notebook/)
	for protected OAI-to-NHANES evaluation.
- Use [`../novel/`](../novel/) for the provenance and paired-preprocessing
	analyses that explain the audit finding.
