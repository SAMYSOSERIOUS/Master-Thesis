# Knee OA — Transparent Reliability Grader (production app)

A knee-OA KL grader that **shows its work**: every prediction returns the grade, the four-pipeline evidence
behind a preprocessing-stability trust flag, a deterministic plain-language explanation, and the model's
provenance. No LLM, no agent — the reliability core is pure, reproducible code.

## Run locally

```bash
cd app
python -m pip install -r requirements.txt
set KNEE_MODEL_MODE=stub
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000/ to use the UI, or /healthz for the API health check.

## Deploy online

### Render / Railway / Fly.io
1. Connect this folder as the app source.
2. Use the start command:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. Set `KNEE_MODEL_MODE=stub` for the first deployment.

### Docker
```bash
docker build -t knee-oa-api .
docker run -p 8000:8000 -e KNEE_MODEL_MODE=stub knee-oa-api
```

## Endpoints

| method | path | returns |
|---|---|---|
| POST | `/assess` (multipart `file`) | grade, softmax, verdict, spread, per-pipeline grades, findings, montage PNG (base64), deterministic explanation |
| GET | `/modelcard` | model provenance, measured performance, limitations, trust-flag validation, disclaimer |
| GET | `/healthz` | status + model mode |

## Trust-flag validation — keep it honest

`validation.json` holds the measured result (STABLE-flagged 80% accurate vs UNSTABLE 61%, failure-detection
AUC 0.60 on OAI, n=1444). **These numbers are tied to the checkpoint.** If you change the model, regenerate them
(rerun the preprocessing-variant validation) and update the file — otherwise the model card lies. If the file is
absent, the card honestly reports "not yet validated on this deployment".

## Important

**Research/educational use only. Not a medical device; not for clinical decision-making.** Clinical deployment
would trigger CE/MDR (EU) or FDA (US) regulation — a different process entirely. Never store patient images;
this service processes in memory and discards.
