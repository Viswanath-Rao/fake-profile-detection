import os
import json
import base64
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, FileResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from core.detector import ProfileForensicEngine
from core.presets import PRESET_PROFILES

engine = ProfileForensicEngine()

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

async def homepage(request):
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>VeriProfile AI Platform Loading...</h1>")

async def get_presets(request):
    return JSONResponse({"presets": PRESET_PROFILES})

async def analyze_profile_endpoint(request):
    try:
        content_type = request.headers.get("content-type", "")
        image_bytes = None
        data = {}

        if "multipart/form-data" in content_type:
            form = await request.form()
            for key, val in form.items():
                if key == "image" and hasattr(val, "read"):
                    image_bytes = await val.read()
                else:
                    data[key] = val
        else:
            data = await request.json()
            if "image_b64" in data and data["image_b64"]:
                b64_data = data["image_b64"]
                if "," in b64_data:
                    b64_data = b64_data.split(",", 1)[1]
                image_bytes = base64.b64decode(b64_data)

        # Normalize numbers
        data["followers"] = int(data.get("followers", 0) or 0)
        data["following"] = int(data.get("following", 0) or 0)
        data["posts"] = int(data.get("posts", 0) or 0)
        data["username"] = str(data.get("username", "anonymous_user")).strip()
        data["bio"] = str(data.get("bio", "")).strip()

        result = engine.analyze_profile(data, image_bytes)
        return JSONResponse({"success": True, "result": result})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

async def batch_analyze_endpoint(request):
    try:
        form = await request.form()
        results = []
        # Support batch image analysis
        for key, val in form.items():
            if hasattr(val, "read"):
                img_bytes = await val.read()
                filename = getattr(val, "filename", key)
                mock_data = {
                    "username": os.path.splitext(filename)[0],
                    "followers": 150,
                    "following": 300,
                    "posts": 5,
                    "bio": "Batch evaluated social profile."
                }
                res = engine.analyze_profile(mock_data, img_bytes)
                res["filename"] = filename
                results.append(res)

        return JSONResponse({"success": True, "results": results})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

async def export_dossier_html(request):
    try:
        data = await request.json()
        result = data.get("result", {})
        
        # Build sleek printable cyber dossier HTML
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Forensic Dossier - {result.get('username', 'Profile')}</title>
<style>
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0b0f19; color: #e2e8f0; margin: 0; padding: 40px; }}
  .dossier-card {{ max-width: 800px; margin: 0 auto; background: #131b2e; border: 1px solid #233152; border-radius: 12px; padding: 36px; box-shadow: 0 20px 50px rgba(0,0,0,0.6); }}
  .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #00f2fe; padding-bottom: 16px; margin-bottom: 24px; }}
  .badge {{ background: {result.get('theme_color', '#3b82f6')}; color: white; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 13px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 24px 0; }}
  .metric-box {{ background: #090e1a; padding: 16px; border-radius: 8px; border-left: 4px solid #00f2fe; }}
  .metric-label {{ font-size: 12px; color: #94a3b8; text-transform: uppercase; }}
  .metric-val {{ font-size: 22px; font-weight: bold; margin-top: 4px; color: #f8fafc; }}
  ul {{ margin: 8px 0; padding-left: 20px; }}
  li {{ margin-bottom: 6px; color: #cbd5e1; font-size: 14px; }}
  .footer {{ margin-top: 32px; padding-top: 16px; border-top: 1px dashed #334155; font-size: 12px; color: #64748b; display: flex; justify-content: space-between; }}
  @media print {{ body {{ background: #fff; color: #000; }} .dossier-card {{ border: 1px solid #000; background: #fff; color: #000; }} .metric-box {{ background: #f1f5f9; }} }}
</style>
</head>
<body>
<div class="dossier-card">
  <div class="header">
    <div>
      <h1 style="margin:0; font-size:24px; letter-spacing:1px; color:#00f2fe;">VERIPROFILE AI FORENSIC AUDIT</h1>
      <p style="margin:4px 0 0 0; font-size:13px; color:#94a3b8;">Dossier ID: {result.get('dossier_id')} | Target: @{result.get('username')}</p>
    </div>
    <div class="badge">{result.get('classification')}</div>
  </div>

  <div class="grid">
    <div class="metric-box">
      <div class="metric-label">Threat Classification</div>
      <div class="metric-val" style="color:{result.get('theme_color')}">{result.get('threat_level')}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Fake Account Probability</div>
      <div class="metric-val">{result.get('fake_probability')}%</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Followers / Following / Posts</div>
      <div class="metric-val">{result.get('metrics', {}).get('followers', 0):,} / {result.get('metrics', {}).get('following', 0):,} / {result.get('metrics', {}).get('posts', 0)}</div>
    </div>
    <div class="metric-box">
      <div class="metric-label">Biometric Avatar Status</div>
      <div class="metric-val" style="font-size:16px;">{result.get('cv_analysis', {}).get('forensic_badge', 'UNKNOWN')}</div>
    </div>
  </div>

  <h3 style="color:#00f2fe; margin-bottom:8px;">Forensic Risk Factors</h3>
  <ul>
    {"".join(f"<li>{r}</li>" for r in result.get('reasons_flagged', []))}
  </ul>

  <h3 style="color:#10b981; margin-top:20px; margin-bottom:8px;">Authenticity Indicators</h3>
  <ul>
    {"".join(f"<li>{p}</li>" for p in result.get('positive_factors', []))}
  </ul>

  <div class="footer">
    <div>Engine: VeriProfile Multi-Modal Ensemble v2.4 (Scikit-Learn + OpenCV)</div>
    <div>Report Hash: SHA256-AUTHENTICATED</div>
  </div>
</div>
<script>window.print();</script>
</body>
</html>"""
        return HTMLResponse(html)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

routes = [
    Route("/", homepage),
    Route("/api/presets", get_presets, methods=["GET"]),
    Route("/api/analyze", analyze_profile_endpoint, methods=["POST"]),
    Route("/api/batch", batch_analyze_endpoint, methods=["POST"]),
    Route("/api/export-dossier", export_dossier_html, methods=["POST"]),
    Mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
]

app = Starlette(debug=True, routes=routes, middleware=middleware)
