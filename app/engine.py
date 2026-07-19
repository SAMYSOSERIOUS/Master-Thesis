"""
Reliability engine + model service for the Knee-OA transparent grader.

Layers 1-3 are the SAME deterministic code validated in the thesis notebook.
The model service (Layer 2) is pluggable:
  KNEE_MODEL_MODE=real  -> loads the trained PyTorch checkpoint (needs torch + training_lib + Drive/model files)
  KNEE_MODEL_MODE=stub  -> a deterministic stand-in (no torch) so the API/frontend can be tested anywhere
"""
import os, io, base64
import numpy as np
import cv2
from PIL import Image, ImageDraw

# ----------------------------------------------------------------------------- config
IMG_SIZE, CLAHE_CLIP, CLAHE_TILE = 224, 2.0, (8, 8)
VARIANTS  = ["ref_order", "alt_order", "double_clahe", "no_clahe"]
REFERENCE = "ref_order"
VARIANT_LABEL = {"ref_order": "CLAHE then resize (reference)", "alt_order": "resize then CLAHE",
                 "double_clahe": "double CLAHE", "no_clahe": "no CLAHE"}
SEVERITY_WORD = {0: "none", 1: "mild", 2: "moderate", 3: "severe", 4: "severe"}
FINDING_NAMES = ["osteophyte", "jsn", "sclerosis"]
MODEL_MODE = os.environ.get("KNEE_MODEL_MODE", "stub")
RUN_NAME   = os.environ.get("KNEE_RUN_NAME", "mt_mendeley_seed0")

_clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=CLAHE_TILE)

# ----------------------------------------------------------------------------- Layer 1
def _resize(a):
    return np.array(Image.fromarray(a, "L").resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS))

def to_gray(image):
    a = np.asarray(image)
    if a.ndim == 3:
        a = a[..., :3].mean(axis=2)
    if a.dtype != np.uint8:
        mn, mx = float(a.min()), float(a.max())
        a = np.zeros_like(a, np.uint8) if mx - mn < 1e-6 else ((a - mn) / (mx - mn) * 255.0).astype(np.uint8)
    return a

def preprocess_variant(gray, v):
    g = gray.astype(np.uint8)
    if v == "ref_order":    return _resize(_clahe.apply(g))
    if v == "alt_order":    return _clahe.apply(cv2.resize(g, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LANCZOS4))
    if v == "double_clahe": return _clahe.apply(_resize(_clahe.apply(g)))
    if v == "no_clahe":     return _resize(g)
    raise ValueError(v)

# ----------------------------------------------------------------------------- Layer 2 (pluggable)
class _StubModel:
    """Deterministic stand-in: grade tracks brightness, so preprocessing variants can disagree (like the real effect)."""
    def predict(self, img224):
        m = float(img224.mean())
        kl = int(np.clip(m / 52, 0, 4))
        findings = {"osteophyte": int(np.clip(m / 70, 0, 3)),
                    "jsn": int(np.clip(m / 60, 0, 3)),
                    "sclerosis": int(np.clip(m / 80, 0, 3))}
        kl_probs = np.zeros(5, np.float32); kl_probs[kl] = 0.7
        return kl, findings, kl_probs

class _RealModel:
    """Loads the trained checkpoint. Imported lazily so the API can run in stub mode without torch."""
    def __init__(self):
        import torch, torch.nn as nn, importlib, sys
        from pathlib import Path
        sys.path.insert(0, os.environ.get("KNEE_LIB_PATH", "/content/drive/MyDrive/Master Thesis/scope3"))
        import config; importlib.reload(config)
        import training_lib_max as TM
        self.torch, self.nn, self.TM, self.config = torch, nn, TM, config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        SUBK = 4
        class MultiTaskNet(nn.Module):
            def __init__(self, n_sub):
                super().__init__()
                self.core = TM.OrdinalNet(config.NUM_CLASSES, 4, use_hierarchical=True)
                feat = self.core.feat_dim
                self.sub_heads = nn.ModuleList([nn.Sequential(nn.Flatten(1), nn.LayerNorm(feat), nn.Dropout(0.3),
                                                              nn.Linear(feat, SUBK - 1)) for _ in range(n_sub)])
            def forward(self, x, grl_lambda=0.0):
                f = self.core.backbone(x)
                if f.dim() == 4: f = f.mean(dim=[-2, -1])
                kl = self.core.corn(f)
                dom = self.core.domain_head(TM.grad_reverse(f, grl_lambda))
                return kl, None, None, dom, [h(f) for h in self.sub_heads]
        ckpt = os.environ.get("KNEE_CKPT_PATH",
                              f"/content/drive/MyDrive/Master Thesis/scope3_mt/checkpoints/{RUN_NAME}_best.pt")
        self.model = MultiTaskNet(len(FINDING_NAMES)).to(self.device)
        TM.load_ckpt(ckpt, self.model, None); self.model.eval()

    def predict(self, img224):
        torch, TM = self.torch, self.TM
        with torch.no_grad():
            a = TM._resize(TM.joint_crop(img224))
            x = torch.from_numpy(a.astype(np.float32) / 255.0); x = (x - 0.485) / 0.229
            xb = x.unsqueeze(0).repeat(3, 1, 1).unsqueeze(0).to(self.device)
            kl, _, _, _, subs = self.model(xb, grl_lambda=0.0)
            kl_probs = TM.corn_probs(kl)[0].cpu().numpy()
            findings = {name: int(TM.corn_probs(subs[k])[0].cpu().numpy().argmax())
                        for k, name in enumerate(FINDING_NAMES)}
        return int(kl_probs.argmax()), findings, kl_probs

_MODEL = None
def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = _RealModel() if MODEL_MODE == "real" else _StubModel()
    return _MODEL

# ----------------------------------------------------------------------------- Layer 3 (pure)
def reliability_verdict(grades_by_variant, reference_grade):
    vals = list(grades_by_variant.values())
    spread = int(max(vals) - min(vals))
    agree = sum(1 for v in vals if v == reference_grade) / len(vals)
    verdict = "STABLE" if spread == 0 else ("CAUTION" if spread == 1 else "UNSTABLE")
    return verdict, spread, agree

def assess(gray):
    model = get_model()
    per = {}
    for v in VARIANTS:
        kl, findings, kl_probs = model.predict(preprocess_variant(gray, v))
        per[v] = dict(kl=kl, findings=findings, kl_probs=kl_probs)
    grades = {v: per[v]["kl"] for v in VARIANTS}
    ref_kl = grades[REFERENCE]
    verdict, spread, agree = reliability_verdict(grades, ref_kl)
    finding_spreads = {}
    for f in FINDING_NAMES:
        vv = [per[v]["findings"][f] for v in VARIANTS]
        finding_spreads[f] = int(max(vv) - min(vv))
    worst = max(finding_spreads, key=finding_spreads.get) if finding_spreads else None
    unstable_finding = worst if worst and finding_spreads[worst] > 0 else None
    return dict(reference_grade=ref_kl, reference_findings=per[REFERENCE]["findings"],
                softmax=float(per[REFERENCE]["kl_probs"].max()), grades_by_variant=grades,
                per_variant={v: {"kl": per[v]["kl"], "findings": per[v]["findings"]} for v in VARIANTS},
                verdict=verdict, spread=spread, agreement=agree,
                finding_spreads=finding_spreads, unstable_finding=unstable_finding)

# ----------------------------------------------------------------------------- transparency helpers
def build_montage_png_b64(gray):
    tiles = []
    model = get_model()
    for v in VARIANTS:
        img = preprocess_variant(gray, v)
        kl, _, _ = model.predict(img)
        tiles.append((v, np.stack([img] * 3, -1).astype(np.uint8), kl))
    pad, label_h = 8, 40
    W = len(tiles) * IMG_SIZE + (len(tiles) + 1) * pad
    H = IMG_SIZE + label_h + 2 * pad
    canvas = Image.new("RGB", (W, H), (255, 255, 255)); draw = ImageDraw.Draw(canvas)
    x = pad
    for v, rgb, kl in tiles:
        canvas.paste(Image.fromarray(rgb), (x, pad))
        draw.text((x + 3, pad + IMG_SIZE + 4), VARIANT_LABEL[v][:26], fill=(0, 0, 0))
        draw.text((x + 3, pad + IMG_SIZE + 20), "-> KL %d" % kl, fill=(180, 30, 30))
        x += IMG_SIZE + pad
    buf = io.BytesIO(); canvas.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")

def explanation_sections(r):
    """DETERMINISTIC templated explanation -> list of {heading, body}. Identical every call. No LLM."""
    grades = list(r["grades_by_variant"].values()); lo, hi = min(grades), max(grades)
    S = []
    S.append(("How this was produced",
              "Your image was run through 4 standard preprocessing pipelines and graded by the same model each time. "
              "This checks whether the grade depends on preprocessing choices that should not change a clinical reading. "
              "The grade shown is from the reference pipeline (CLAHE then resize)."))
    if r["spread"] == 0:
        S.append(("What happened", "All 4 pipelines produced the same grade (KL %d). The reading does not depend on preprocessing." % r["reference_grade"]))
    else:
        S.append(("What happened", "The pipelines produced grades ranging KL %d to KL %d (%s). Preprocessing alone changed the grade by %d."
                  % (lo, hi, ", ".join("KL %d" % g for g in grades), r["spread"])))
    if r["verdict"] == "STABLE":
        S.append(("What the verdict means", "STABLE - the grade is robust to preprocessing. This is the model's consistent read (necessary for trust; see the limit below)."))
    elif r["verdict"] == "CAUTION":
        S.append(("What the verdict means", "CAUTION - the grade shifts by one depending on preprocessing. Treat this knee as borderline between KL %d and KL %d." % (lo, hi)))
    else:
        S.append(("What the verdict means", "UNSTABLE - the grade shifts by %d depending on preprocessing alone. The model's read is not robust for this image; manual review is recommended." % r["spread"]))
    if r["unstable_finding"]:
        f = r["unstable_finding"]; vals = [r["per_variant"][v]["findings"][f] for v in VARIANTS]
        S.append(("Which finding drives it",
                  "The instability is driven mainly by the %s finding, scored inconsistently across pipelines (%s on a 0-3 scale) - the model could not settle on one severity for it."
                  % (f, ", ".join(str(x) for x in vals))))
    S.append(("What this does NOT tell you",
              "This verdict measures consistency, not correctness. A stable grade can still be wrong if the case is genuinely ambiguous - expert radiologists agree on only ~60-66% of exact KL grades. Consistency is necessary but not sufficient for a correct grade."))
    return S
