import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import cv2
import json
import os
import base64
from PIL import Image

from core.detector import ProfileForensicEngine
from core.presets import PRESET_PROFILES

st.set_page_config(
    page_title="VeriProfile AI — Forensic Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Engine
@st.cache_resource
def get_forensic_engine():
    return ProfileForensicEngine()

engine = get_forensic_engine()

# Inject Pixel-Perfect Cyberpunk Glassmorphism CSS matching the Web Dashboard
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    /* Hide Default Streamlit Clutter */
    #MainMenu, footer, header { visibility: hidden; height: 0; }
    [data-testid="stSidebar"] { display: none; }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1540px !important;
    }

    /* Core Theme */
    .stApp {
        background-color: #070a12;
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    }

    /* Top Navigation Header */
    .cyber-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 24px;
        background: rgba(13, 19, 34, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 14px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-icon {
        width: 38px;
        height: 38px;
        border-radius: 8px;
        background: rgba(0, 242, 254, 0.15);
        border: 1px solid #00f2fe;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #00f2fe;
        font-size: 1.2rem;
        box-shadow: 0 0 12px rgba(0,242,254,0.3);
    }
    .brand-name {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin: 0;
        color: #fff;
    }
    .brand-name span {
        color: #00f2fe;
    }
    .brand-desc {
        font-size: 0.72rem;
        color: #94a3b8;
        margin: 0;
    }
    .status-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #10b981;
        font-weight: 700;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    /* Glass Cards */
    .vp-card {
        background: rgba(16, 24, 43, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s;
    }
    .vp-card:hover {
        border-color: rgba(0, 242, 254, 0.4);
    }
    .vp-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 10px;
        margin-bottom: 14px;
    }
    .vp-card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .vp-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        background: rgba(0, 242, 254, 0.1);
        border: 1px solid rgba(0, 242, 254, 0.3);
        color: #00f2fe;
    }

    /* Speedometer Gauge */
    .gauge-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 10px 0;
    }
    .threat-tag {
        margin-top: 8px;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-align: center;
    }

    /* Biometric Box */
    .bio-viewport {
        position: relative;
        background: #050811;
        border: 1px solid rgba(0, 242, 254, 0.25);
        border-radius: 10px;
        height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .bio-stats-row {
        display: flex;
        gap: 8px;
        margin-top: 10px;
    }
    .bio-pill {
        flex: 1;
        background: rgba(9, 14, 26, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 6px;
        padding: 5px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
    }

    /* Metric Grid Tiles */
    .metrics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }
    .m-tile {
        background: rgba(9, 14, 26, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid #00f2fe;
        border-radius: 8px;
        padding: 10px 12px;
    }
    .m-tile-lbl {
        font-size: 0.68rem;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 600;
    }
    .m-tile-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.15rem;
        font-weight: 700;
        color: #fff;
        margin-top: 3px;
    }

    /* Streamlit Form Element Styling */
    div.stTextInput > div > div > input,
    div.stNumberInput > div > div > input,
    div.stTextArea > div > div > textarea,
    div.stSelectbox > div > div > div {
        background-color: rgba(9, 14, 26, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }
    div.stTextInput > div > div > input:focus,
    div.stNumberInput > div > div > input:focus,
    div.stTextArea > div > div > textarea:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.3) !important;
    }

    /* Submit Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00f2fe, #0284c7) !important;
        color: #030712 !important;
        font-weight: 800 !important;
        font-size: 0.88rem !important;
        border: none !important;
        border-radius: 8px !important;
        height: 46px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(0, 242, 254, 0.6) !important;
    }

    /* Diagnostic Reasoning Boxes */
    .reasons-box {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-top: 14px;
    }
    .flagged-list, .verified-list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .flagged-list li {
        font-size: 0.78rem;
        line-height: 1.4;
        padding: 6px 10px;
        border-radius: 6px;
        background: rgba(239, 68, 68, 0.08);
        border-left: 3px solid #ef4444;
        color: #fca5a5;
    }
    .verified-list li {
        font-size: 0.78rem;
        line-height: 1.4;
        padding: 6px 10px;
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.08);
        border-left: 3px solid #10b981;
        color: #86efac;
    }
</style>
""", unsafe_allow_html=True)

# 1. Header Bar (Matching Picture 1)
st.markdown("""
<div class="cyber-header">
    <div class="brand-group">
        <div class="brand-icon">🛡️</div>
        <div>
            <h1 class="brand-name">VERIPROFILE<span>.AI</span></h1>
            <p class="brand-desc">Autonomous Profile Authenticity & Deepfake Forensic Engine</p>
        </div>
    </div>
    <div class="status-pill">
        <div class="status-dot"></div>
        ENSEMBLE ONLINE (v2.4)
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Top Quick Presets Ribbon (Matching Picture 1)
st.markdown("<p style='font-size:0.8rem; font-weight:700; color:#00f2fe; margin-bottom:6px;'>⚡ Quick Presets:</p>", unsafe_allow_html=True)
preset_cols = st.columns(len(PRESET_PROFILES))
for idx, p in enumerate(PRESET_PROFILES):
    with preset_cols[idx]:
        if st.button(p["name"], key=f"top_preset_{p['id']}", use_container_width=True):
            st.session_state["active_preset"] = p

# Read current preset or fallback
current_p = st.session_state.get("active_preset", PRESET_PROFILES[0])

# 3. Main Grid Layout (Matching Picture 1 40% / 60% split)
left_col, right_col = st.columns([1, 1.35], gap="medium")

with left_col:
    # Target Profile Metrics Card
    st.markdown("""
    <div class="vp-card-header" style="margin-bottom:8px;">
        <div class="vp-card-title">👤 Target Profile Metrics</div>
        <span class="vp-badge">INPUT TELEMETRY</span>
    </div>
    """, unsafe_allow_html=True)

    with st.form("main_forensic_form"):
        username = st.text_input("Username / Handle", value=current_p["username"])
        
        row1_c1, row1_c2 = st.columns(2)
        with row1_c1:
            followers = st.number_input("Followers", min_value=0, value=current_p["followers"], step=10)
            posts = st.number_input("Total Posts", min_value=0, value=current_p["posts"], step=1)
        with row1_c2:
            following = st.number_input("Following", min_value=0, value=current_p["following"], step=10)
            acc_type = st.selectbox("Account Type", ["Public Account", "Private Account"], index=1 if current_p["is_private"] else 0)

        bio = st.text_area("Biography (Bio)", value=current_p["bio"], height=75)
        uploaded_image = st.file_uploader("Profile Photo (Biometric CV Scan)", type=["jpg", "png", "jpeg", "webp"])
        
        submit = st.form_submit_button("🔍 SCAN & ANALYZE PROFILE", use_container_width=True)

with right_col:
    # Prepare image bytes
    img_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    
    # Process through Engine
    profile_data = {
        "username": username,
        "followers": int(followers),
        "following": int(following),
        "posts": int(posts),
        "bio": bio,
        "is_private": (acc_type == "Private Account")
    }
    result = engine.analyze_profile(profile_data, img_bytes)
    cv = result["cv_analysis"]

    # Top Right: Threat Gauge + Biometric Viewport Row (Matching Picture 1)
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        # SVG Animated Speedometer Gauge
        prob = result["fake_probability"]
        circumference = 2 * 3.14159 * 65 # ~408.4
        offset = circumference - (prob / 100.0) * circumference
        color = result["theme_color"]

        gauge_html = f"""
        <div style="background:rgba(16,24,43,0.75); border:1px solid rgba(56,189,248,0.2); border-radius:14px; padding:16px; text-align:center;">
            <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:700; color:#94a3b8; margin-bottom:6px;">
                <span>🎯 Threat Evaluation</span>
                <span style="font-family:'JetBrains Mono'; color:#00f2fe;">#{result['dossier_id']}</span>
            </div>
            <div style="position:relative; width:150px; height:150px; margin:0 auto;">
                <svg viewBox="0 0 160 160" style="width:100%; height:100%; transform:rotate(-90deg);">
                    <circle cx="80" cy="80" r="65" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="12"></circle>
                    <circle cx="80" cy="80" r="65" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round"
                            stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"></circle>
                </svg>
                <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center;">
                    <div style="font-family:'JetBrains Mono'; font-size:1.8rem; font-weight:800; color:{color}; line-height:1;">{prob}%</div>
                    <div style="font-size:0.6rem; font-weight:700; color:#64748b; letter-spacing:1px; margin-top:2px;">FAKE PROBABILITY</div>
                </div>
            </div>
            <div style="margin-top:8px; padding:6px 14px; border-radius:20px; font-size:0.75rem; font-weight:800; background:{color}18; border:1px solid {color}66; color:{color};">
                {result['classification']}
            </div>
        </div>
        """
        st.markdown(gauge_html, unsafe_allow_html=True)

    with g_col2:
        # Biometric HUD Scanner Box
        badge_text = cv["forensic_badge"] if cv["has_image"] else "NO AVATAR"
        hud_b64 = cv["annotated_image_base64"]
        
        hud_content = f"""<img src="{hud_b64}" style="max-width:100%; max-height:100%; object-fit:contain;" />""" if hud_b64 else """
        <div style="text-align:center; color:#64748b; padding:15px;">
            <div style="font-size:2rem; margin-bottom:4px;">👁️</div>
            <p style="font-size:0.75rem; margin:0;">Upload profile avatar to engage facial landmark & compression analysis</p>
        </div>
        """

        hud_card = f"""
        <div style="background:rgba(16,24,43,0.75); border:1px solid rgba(56,189,248,0.2); border-radius:14px; padding:16px;">
            <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:700; color:#94a3b8; margin-bottom:6px;">
                <span>🎯 Biometric HUD Scanner</span>
                <span style="font-family:'JetBrains Mono'; font-size:0.68rem; font-weight:700; color:{color}; border:1px solid {color}; padding:2px 6px; border-radius:4px;">{badge_text}</span>
            </div>
            <div class="bio-viewport" style="height:150px;">
                {hud_content}
            </div>
            <div class="bio-stats-row">
                <div class="bio-pill"><span style="color:#64748b;">Faces:</span> <span style="color:#00f2fe; font-weight:700;">{max(0, cv['face_count'])}</span></div>
                <div class="bio-pill"><span style="color:#64748b;">Ratio:</span> <span style="color:#00f2fe; font-weight:700;">{cv['face_ratio']*100:.1f}%</span></div>
                <div class="bio-pill"><span style="color:#64748b;">Sharp:</span> <span style="color:#00f2fe; font-weight:700;">{cv['sharpness']}</span></div>
            </div>
        </div>
        """
        st.markdown(hud_card, unsafe_allow_html=True)

    # Middle Right: Forensic Dimension Breakdown + Chart.js Radar (Matching Picture 1)
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    
    r_scores = result["radar_scores"]
    radar_labels = list(r_scores.keys())
    radar_vals = list(r_scores.values())

    radar_component_html = f"""
    <div style="background:rgba(16,24,43,0.75); border:1px solid rgba(56,189,248,0.2); border-radius:14px; padding:16px; font-family:'Plus Jakarta Sans', sans-serif;">
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:700; color:#fff; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:12px;">
            <span>🎯 Forensic Dimension Breakdown</span>
            <span style="font-family:'JetBrains Mono'; font-size:0.68rem; color:#00f2fe; background:rgba(0,242,254,0.1); padding:2px 8px; border-radius:4px; border:1px solid rgba(0,242,254,0.3);">MULTI-FACTOR ANALYSIS</span>
        </div>
        <div style="display:grid; grid-template-columns: 240px 1fr; gap:16px; align-items:center;">
            <div style="width:240px; height:200px;">
                <canvas id="appRadarChart"></canvas>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <div style="background:rgba(9,14,26,0.8); border-left:3px solid #00f2fe; border-radius:6px; padding:8px 10px;">
                    <div style="font-size:0.65rem; color:#94a3b8; text-transform:uppercase;">Follower/Following Ratio</div>
                    <div style="font-family:'JetBrains Mono'; font-size:1.1rem; font-weight:700; color:#fff;">{result['metrics']['ff_ratio']}</div>
                </div>
                <div style="background:rgba(9,14,26,0.8); border-left:3px solid #00f2fe; border-radius:6px; padding:8px 10px;">
                    <div style="font-size:0.65rem; color:#94a3b8; text-transform:uppercase;">Activity Density Score</div>
                    <div style="font-family:'JetBrains Mono'; font-size:1.1rem; font-weight:700; color:#fff;">{result['metrics']['activity_density']}</div>
                </div>
                <div style="background:rgba(9,14,26,0.8); border-left:3px solid #00f2fe; border-radius:6px; padding:8px 10px;">
                    <div style="font-size:0.65rem; color:#94a3b8; text-transform:uppercase;">Handle Digit Concentration</div>
                    <div style="font-family:'JetBrains Mono'; font-size:1.1rem; font-weight:700; color:#fff;">{result['metrics']['digit_ratio']}%</div>
                </div>
                <div style="background:rgba(9,14,26,0.8); border-left:3px solid {'#10b981' if result['authenticity_score']>50 else '#ef4444'}; border-radius:6px; padding:8px 10px;">
                    <div style="font-size:0.65rem; color:#94a3b8; text-transform:uppercase;">Overall Authenticity Index</div>
                    <div style="font-family:'JetBrains Mono'; font-size:1.1rem; font-weight:700; color:{'#10b981' if result['authenticity_score']>50 else '#ef4444'};">{result['authenticity_score']}%</div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const ctx = document.getElementById('appRadarChart').getContext('2d');
        new Chart(ctx, {{
            type: 'radar',
            data: {{
                labels: {json.dumps(radar_labels)},
                datasets: [{{
                    data: {json.dumps(radar_vals)},
                    backgroundColor: 'rgba(0, 242, 254, 0.2)',
                    borderColor: '#00f2fe',
                    borderWidth: 2,
                    pointBackgroundColor: '#00f2fe',
                    pointRadius: 3
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    r: {{
                        angleLines: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                        grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                        pointLabels: {{ color: '#94a3b8', font: {{ size: 9 }} }},
                        suggestedMin: 0,
                        suggestedMax: 100,
                        ticks: {{ display: false }}
                    }}
                }},
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});
    </script>
    """
    components.html(radar_component_html, height=240)

    # Bottom Right: Diagnostic Reasoning Breakdown (Matching Picture 1)
    reasons_html = f"""
    <div style="background:rgba(16,24,43,0.75); border:1px solid rgba(56,189,248,0.2); border-radius:14px; padding:16px; margin-top:14px;">
        <div style="font-size:0.85rem; font-weight:700; color:#fff; margin-bottom:10px;">📋 AI Forensic Telemetry Reasoning</div>
        <div class="reasons-box">
            <div>
                <h5 style="color:#ef4444; font-size:0.78rem; margin:0 0 6px 0;">⚠️ Anomalies & Risk Flags</h5>
                <ul class="flagged-list">
                    {"".join(f"<li>{r}</li>" for r in result['reasons_flagged'])}
                </ul>
            </div>
            <div>
                <h5 style="color:#10b981; font-size:0.78rem; margin:0 0 6px 0;">✅ Authenticity Indicators</h5>
                <ul class="verified-list">
                    {"".join(f"<li>{p}</li>" for p in result['positive_factors'])}
                </ul>
            </div>
        </div>
    </div>
    """
    st.markdown(reasons_html, unsafe_allow_html=True)