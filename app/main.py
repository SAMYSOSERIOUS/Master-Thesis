"""FastAPI backend for the Knee-OA transparent reliability grader."""
import io
import json
import os
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image

import engine

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app = FastAPI(
    title="Knee OA Reliability Grader",
    version="1.0",
    description="Transparent, deterministic knee-OA KL grader with a validated preprocessing-stability trust flag.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_BYTES = 20 * 1024 * 1024  # 20 MB upload cap

def _load_validation():
    p = Path(os.environ.get("KNEE_VALIDATION_JSON", Path(__file__).parent / "validation.json"))
    try:
        return json.loads(p.read_text())
    except Exception:
        return None

@app.get("/healthz")
def healthz():
    return {"status": "ok", "model_mode": engine.MODEL_MODE, "run_name": engine.RUN_NAME}

@app.get("/modelcard")
def modelcard():
    v = _load_validation()
    return {
        "model": "multi-task ConvNeXt-Large concept-bottleneck (KL grade + osteophyte/JSN/sclerosis)",
        "checkpoint": engine.RUN_NAME,
        "trained_on": ["OAI", "NHANES", "MRKR"],
        "measured_performance": {
            "binary_OA_AUC_crosscohort": "0.77-0.85 (~0.88 this interpretable model)",
            "exact_5class_crosscohort": 0.46,
            "within_1_grade": 0.72,
            "findings_extractor": {"jsn": {"exact": 0.80, "qwk": 0.85},
                                   "osteophyte": {"exact": 0.66}, "sclerosis": {"exact": 0.76}},
        },
        "known_limitations": [
            "osteophyte/sclerosis findings noisier than JSN; their per-finding stability inherits that noise",
            "MRKR training labels are machine-generated",
            "exact 5-class grading sits near the ~60-66% expert-agreement ceiling",
        ],
        "trust_flag_validation": v,   # null if not validated on this deployment
        "disclaimer": "Research/educational use only. Not a medical device; not for clinical decision-making.",
    }

@app.post("/assess")
async def assess(file: UploadFile = File(...)):
    raw = await file.read()
    if not raw:
        raise HTTPException(400, "Empty upload.")
    if len(raw) > MAX_BYTES:
        raise HTTPException(413, "File too large (max 20 MB).")
    try:
        img = Image.open(io.BytesIO(raw))
        img.load()
    except Exception:
        raise HTTPException(415, "Could not read image. Upload a PNG/JPG/DICOM-exported X-ray.")
    try:
        gray = engine.to_gray(img)
        r = engine.assess(gray)
        montage = engine.build_montage_png_b64(gray)
        sections = engine.explanation_sections(r)
    except Exception as e:
        raise HTTPException(500, "Processing failed: %s" % str(e))

    findings_out = {f: {"severity": r["reference_findings"][f],
                        "word": engine.SEVERITY_WORD[r["reference_findings"][f]],
                        "stability_spread": r["finding_spreads"][f]} for f in engine.FINDING_NAMES}
    variant_out = [{"variant": v, "label": engine.VARIANT_LABEL[v], "grade": g}
                   for v, g in r["grades_by_variant"].items()]
    # NOTE: image processed in memory and discarded; nothing is stored.
    return JSONResponse({
        "grade": r["reference_grade"],
        "softmax": round(r["softmax"], 3),
        "verdict": r["verdict"],
        "spread": r["spread"],
        "agreement": round(r["agreement"], 3),
        "grades_by_variant": variant_out,
        "findings": findings_out,
        "unstable_finding": r["unstable_finding"],
        "montage_png_base64": montage,
        "explanation": [{"heading": h, "body": b} for h, b in sections],
        "model": {"checkpoint": engine.RUN_NAME, "mode": engine.MODEL_MODE},
    })

@app.get("/", response_class=HTMLResponse)
def root():
    html_path = Path(__file__).with_name("index.html")
    return html_path.read_text(encoding="utf-8")

@app.get("/assess", response_class=HTMLResponse)
def assessment_page():
    html_path = Path(__file__).with_name("assessment.html")
    return html_path.read_text(encoding="utf-8")

@app.get("/about", response_class=HTMLResponse)
def about_page():
    html_path = Path(__file__).with_name("about.html")
    return html_path.read_text(encoding="utf-8")
