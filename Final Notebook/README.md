Final Thesis Pipeline

This folder contains the nine notebooks that implement the final, auditable
analysis pipeline for cross-cohort knee osteoarthritis grading.

The core scientific pipeline, N00–N05, is a post-exploratory freeze, not a
preregistration. Each stage has an explicit input contract, writes an acceptance
status, and prevents downstream analysis when its required checks fail.

N06A and N06B are explicitly exploratory, post-hoc performance extensions.
They do not replace, modify, or reinterpret the locked N00–N05 scientific
pipeline. Their purpose is to test how much OAI-to-NHANES III KL-grading
performance can be recovered with a stronger direct model and subsequent
source-only ordinal refinement.

The notebooks are the pipeline specification. Generated tables, figures,
predictions, checkpoints, certificates, manifests, configuration locks, and logs
are written to Google Drive under:

/content/drive/MyDrive/MasterThesis/Final Pipeline/

They are not treated as authoritative when stored only in local runtime storage.

Execution Order

Run the notebooks in this order:

flowchart LR
    N00[N00: Measurement validation] --> N01[N01: Cohorts and protected splits]
    N01 --> N02A[N02A: OAI-only primary CBM]
    N02A --> N02B[N02B: Locked OAI-to-NHANES transfer]
    N02B --> N03[N03: Failure decomposition]
    N03 --> N04[N04: Concept-layer reliability]

    N01 --> N05[N05: Adaptation strategies]
    N02A --> N05
    N02B --> N05
    N03 --> N05
    N04 --> N05

    N05 --> N06A[N06A: Performance ceiling and external benchmark]
    N01 --> N06A
    N06A --> N06B[N06B: Ordinal refinement and paired benchmark]

Do not bypass a failed status gate. A downstream notebook assumes that all
required upstream cohorts, checkpoints, predictions, manifests, and acceptance
artifacts passed their checks.

N06A and N06B should be executed only after the locked N00–N05 pipeline has
been completed and preserved. N06B additionally requires the exact locked N06A
artifacts and refuses to proceed if their hashes, source universe, or patient
split no longer match.

Notebook Catalogue

Stage

Notebook

Role

Primary inputs

Key products

N00

N00_Measurement_Validation.ipynb

Validates the metrics and statistical procedures used throughout the pipeline using synthetic data only.

No patient data.

Shared measurement_tools.py, frozen measurement protocol, validation tables and figures, status, certificate, output manifest.

N01

N01_Cohorts_Labels_Protected_Splits.ipynb

Reconstructs OAI and NHANES III cohorts, validates labels and concepts, and freezes participant-level splits.

Original OAI and NHANES source data; N00 status.

Frozen cohort files, source registry, label and concept tables, Discovery/Confirmation manifests, cohort figures, status, certificate.

N02A

N02A_OAI_Only_Primary_CBM.ipynb

Develops and freezes a three-seed ConvNeXt-Tiny concept-bottleneck ensemble using OAI only.

Frozen OAI cohort and split from N01.

Checkpoints, validation temperatures, OAI test predictions, model and checkpoint manifests, status, certificate.

N02B

N02B_Transfer_Compile_Clean.ipynb

Performs locked evaluation of the frozen OAI ensemble on OAI test and NHANES Confirmation.

N02A checkpoints and temperatures; N01 cohorts.

OAI and NHANES predictions, transfer metrics, generalization-loss tables, participant-bootstrap intervals, figures, status, certificate.

N03

N03_Failure_Decomposition.ipynb

Separates image-to-concept perception failure from concept-to-grade mapping failure.

N02B prediction tables; N01 cohort data.

Four-condition decomposition predictions, effect intervals, concept-grade analyses, scientific verdict, figures, status, certificate.

N04

N04_Concept_Layer_Reliability.ipynb

Tests whether concept-layer uncertainty identifies grading errors better than maximum-softmax response.

N02B predictions; N03 status.

Reliability scores, risk-coverage curves, selected threshold and transfer tables, scientific verdict, figures, status, certificate.

N05

N05_Adaptation_Strategies.ipynb

Compares the frozen baseline and five adaptation strategies on target performance, mechanism repair, and source retention.

Frozen model, cohorts, predictions, and diagnostics from N01 through N04.

Per-method metrics, concept recovery and reliability analyses, participant-bootstrap intervals, trade-off tables, scientific verdict, status, certificate.

N06A

N06A_Performance_Ceiling_and_External_Benchmark.ipynb

Tests an exploratory direct ConvNeXt-Base performance ceiling using the expanded OAI KL-labelled cohort. Screens baseline CE, ordinal/ranking, and hybrid-concept variants using OAI validation only, then performs locked zero-shot NHANES evaluation.

Original OAI KL labels and processed images; N01 NHANES cohort for external evaluation only.

Frozen three-seed checkpoints, OAI source and split manifests, validation-selected variant, OAI-only cut-points, external-evaluation lock, OAI/NHANES predictions, participant-bootstrap intervals, benchmark figures, status/certificate artifacts.

N06B

N06B_Ordinal_Refinement_and_Paired_Benchmark.ipynb

Refines the locked N06A model with source-only ordinal and continuous-severity supervision and tests whether this improves transfer without changing the OAI cohort, split, backbone, or using NHANES labels for training or selection.

Exact locked N06A checkpoints, lock/hash contracts and patient split; N01 NHANES cohort loaded only after the N06B external lock.

Three refined checkpoints, OAI-only blend and cut-points, N06B external-evaluation lock, OAI/NHANES predictions, participant-bootstrap intervals, paired N06A-vs-N06B ΔQWK analysis, grade-level diagnostics, certificate, editorial recommendation.

Data Protection and Evaluation Rules

N02A is OAI-only. It must not access NHANES data while training or selecting
the primary concept-bottleneck model.

NHANES is split into Discovery and Confirmation at the participant level in
N01. Discovery supports adaptation development; Confirmation is retained for
final evaluation within the locked N00–N05 pipeline.

N02B is evaluation-only. It loads the frozen N02A ensemble and does not train,
select, or modify checkpoints.

N03 separates failure mechanisms using only concepts shared across the two
cohorts rather than treating all concept labels as universally comparable.

N04 compares reliability measures on the same frozen ensemble outputs. It does
not perform inference, retraining, checkpoint selection, or recalibration.

N05 reports adaptation as a trade-off among target performance, mechanism
repair, and OAI source retention rather than as a single accuracy number.

N06A is an exploratory direct-model performance extension. OAI alone is used
for training, candidate selection, threshold fitting, and model development.
NHANES is loaded only after the external-evaluation lock is written.

N06A uses a fresh participant-level OAI split because its direct KL objective
can use a larger KL-labelled OAI universe than the concept-complete N02A
cohort. The OAI test set is not used for candidate selection.

N06B must reuse the exact N06A OAI universe and participant split. It may
not create a new cohort or resplit participants.

N06B initializes from the corresponding locked N06A EMA checkpoints and uses
OAI validation only for epoch selection, blend selection, and ordinal
cut-point fitting.

N06B loads NHANES only after its own external-evaluation lock has been
written. No NHANES label may alter weights, epoch choices, blend weights, or
cut-points.

Because N06A NHANES results were already observed before N06B was designed,
N06B is an exploratory repeated external benchmark, not a fresh untouched
confirmatory external validation.

N06A/N06B benchmark comparisons to published external results are contextual
unless cohort construction, quality-control rules, and evaluation protocols
are demonstrably aligned.

Reproducibility and Audit Trail

Every applicable stage records the information needed to audit its products:

deterministic seeds and environment information;

participant-level, rather than image-level, bootstrap procedures;

schema, leakage, identity, and input-integrity checks;

status JSON gates and acceptance certificates;

output manifests with file paths and hashes;

configuration and/or evaluation locks where required;

checkpoint hashes and source/split hashes for model stages;

Google Drive-safe output handling and save audits.

The exploratory N06 stages add stricter model-provenance controls:

N06A writes its external-evaluation lock before any NHANES labels are read;

N06B verifies the exact N06A parent lock, source-manifest hash, split hash,
and checkpoint hashes before refinement;

N06B writes to a separate namespace and does not modify N06A artifacts;

paired N06A-vs-N06B comparison uses participant-level resampling.

Environment and Outputs

Run the pipeline in Google Colab with Google Drive mounted.

GPU execution is required for:

N02A model development;

the training components of N05;

N06A performance-ceiling training;

N06B ordinal refinement.

The source cohort files, processed images, frozen checkpoints, and required
upstream Drive artifacts must already exist at the locations checked by each
notebook.

All generated artifacts belong under:

/content/drive/MyDrive/MasterThesis/Final Pipeline/

This includes, where applicable:

src/
data/
tables/
figures/
results/
predictions/
checkpoints/
logs/
config/
certificates/
manifests/

Artifacts are organized by notebook stage or provenance namespace.

Reading Guide

For the locked thesis analysis, start with N00 and N01 to establish what is
measured and which participants are protected. Read N02A and N02B together to
see the separation between model development and locked external evaluation.
N03 then decomposes the transfer gap, N04 evaluates whether concept-layer
uncertainty identifies grading failure, and N05 tests whether adaptation repairs
the diagnosed mechanism without sacrificing OAI source performance.

Then read the exploratory performance extension separately:

N06A asks how high OAI-to-NHANES III KL-grading performance can go when
the model is optimized directly for ordinal predictive performance rather
than constrained to the original concept-bottleneck pathway.

N06B asks whether source-only ordinal refinement of the already-trained
N06A model provides an additional transfer gain and evaluates that change
with a paired participant bootstrap.

The notebooks include reader-guide markdown blocks for this route. These blocks
are presentation aids only; they do not alter model code, configuration, data
access, or analysis logic.

Scientific Interpretation of N06A and N06B

N06A and N06B must remain clearly separated from the locked N00–N05 pipeline in
the thesis narrative.

N06A is a post-hoc performance-ceiling experiment. Candidate models are
selected using OAI validation only, and the final three-seed ensemble is locked
before NHANES evaluation. Its external result is a zero-shot benchmark on the
N01 NHANES cohort, but comparison with published systems is not automatically a
head-to-head replication because external cohort and quality-control protocols
may differ.

N06B is a post-hoc ordinal-refinement experiment designed after the N06A
NHANES result had already been observed. Its development remains target-label
free, but its NHANES evaluation must be described as an exploratory repeated
external benchmark rather than a pristine new external validation. The paired
participant-bootstrap comparison against N06A is the primary way to judge
whether the refinement added value.

A PASS status for either exploratory stage means that the specified protocol
and engineering checks completed successfully. It does not require a
particular performance threshold or require N06B to outperform N06A.

Relationship to Exploratory Research

The notebooks in ../research/ record the acquisition,
multi-source, calibration, and diagnostic work that informed the final pipeline.
They remain valuable for reproducibility and methodological context, but claims
from the locked thesis analysis should be traced to the protected cohorts,
frozen artifacts, and acceptance certificates produced by N00–N05.

The provenance and preprocessing studies in
../research/novel/ explain why Mendeley is not treated
as an independent OAI external-validation cohort in the final workflow.

N06A and N06B are later exploratory extensions and should be reported as such,
with their own locks, manifests, predictions, and certificates.

Artifact Naming Notes

N02A provenance identifiers

N02A is the presented stage name for primary OAI-only concept-bottleneck model
development. Some frozen checkpoints, tables, and manifests retain an N03
identifier because they originate from the earlier executed checkpoint protocol.
Treat that identifier as an immutable provenance label, not as an additional
pipeline stage. Do not rename these artifacts after a run because downstream
integrity checks refer to their recorded paths and hashes.

N06A artifact namespace

The notebook is presented as N06A, but its executed artifact namespace is
intentionally retained as:

N06

For example, N06A writes to locations such as:

results/N06/
tables/N06/
figures/N06/
predictions/N06/
checkpoints/N06/
manifests/N06/
config/N06/

N06B treats this N06 namespace as its immutable parent experiment and verifies
the parent lock and hashes before running.

N06B artifact namespace

N06B writes independently under:

N06B

and does not overwrite or rename N06A/N06 artifacts.

Do not rename provenance-bearing artifacts after execution. Downstream integrity
checks depend on their recorded paths, hashes, and lock contents.
