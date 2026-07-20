# oarsi — OARSI Sub-Feature Multi-Task Learning

Extraction of **OARSI sub-feature gradings** (osteophytes, joint-space narrowing,
sclerosis) and multi-task training that predicts these features *alongside* the KL
grade.

## Scientific rationale

The KL grade is a single ordinal summary of several distinct radiographic
findings. If a model is taught to also predict the underlying OARSI sub-features,
it is forced to learn the **clinically meaningful structures** that define a grade,
rather than shortcut correlations. This is auxiliary-task regularization: extra
supervision that should improve the main task and its transfer. Sub-feature labels
exist **only on OAI** and only where each feature was actually read, so the method
must learn from *partial* supervision — handled with per-feature masking.

## Notebooks

| Notebook | What it does | Why (method & justification) |
|----------|--------------|------------------------------|
| `oai_oarsi_subgrades.ipynb` | Auto-detects and parses the `V00XR*` OARSI columns from `KXR_SQ_BU00.txt` (OST/JSN/SC families) and computes per-knee composite maxima. | Pattern-matching the variable names makes extraction robust to schema changes; the composite maximum across compartments is the cleanest objective target per feature. |
| `mt1_merge_subgrades.ipynb` | Attaches OAI sub-grades to manifest rows by subject+side and builds a **per-feature mask**. | A separate mask per feature lets a knee contribute the features it has and skip the ones it lacks — no knee or KL label is wasted. |
| `mt2_multitask_trainer.ipynb` | Reference multi-task trainer: shared CORN backbone + KL head + one small ordinal head per sub-feature, with a **masked** sub-feature loss. | Sharing the backbone is what transfers knowledge between tasks; masking ensures missing readings contribute zero gradient instead of fake-zero targets. |
| `mt2_multitask_oai.ipynb` | Runs the multi-task trainer on the OAI fold. | OAI is where sub-feature supervision is dense, so it is the primary test of the auxiliary-task benefit. |
| `mt2_multitask_nhanes_v2.ipynb` | NHANES fold re-run with a **divergence detector** (reverts to last good checkpoint on a loss spike). | The first run diverged at epoch 8; the guard makes training robust and the result trustworthy. |

## Method notes

- **Multi-task learning** — auxiliary OARSI heads regularize the shared representation toward genuine pathology.
- **Masked loss** — the principled way to train on partially labelled data.
- **Ordinal (CORN) heads** — each sub-feature (0–3) is ordered, so ordinal modelling, not flat classification, is used.
- **Divergence guard** — an explicit stability mechanism, treated as part of the experimental method rather than an afterthought.
