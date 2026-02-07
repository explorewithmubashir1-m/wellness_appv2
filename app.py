# ==============================================================================
# MINDCHECK AI - QUANTUM EDITION (v4.0)
# ==============================================================================
# AUTHOR: Mubashir Mohsin & Gemini
# ENGINE: Quantum CSS / Wizard Logic
# DATE: 2026-02-06
# ==============================================================================

import streamlit as st
import pandas as pd
import joblib
import json
import time
import requests
import os

# ==============================================================================
# 1. SYSTEM CONFIGURATION
# ==============================================================================
PAGE_TITLE = "MindCheck AI"
PAGE_ICON = "🧠"
MODEL_FILE = 'mental_health_model.joblib' 
GEMINI_MODEL = 'gemini-2.5-flash'
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. STATE MANAGEMENT & WIZARD LOGIC
# ==============================================================================
# We need to track the current question index for the wizard flow.
DEFAULTS = {
    "page": "home",
    "theme_mode": "Light",
    "score": None,
    "inputs": {},
    "ai_results": {},
    "wizard_step": 0, # Tracks which question we are on
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==============================================================================
# 3. QUANTUM CSS ENGINE (MASSIVE VISUAL CORE)
# ==============================================================================
def inject_quantum_engine():
    # Define Dynamic Color Palettes
    if st.session_state.theme_mode == "Dark":
        # Quantum Dark
        primary = "#00f2ff"        # Cyan Neon
        secondary = "#7000ff"      # Violet Neon
        bg_grad = "linear-gradient(135deg, #050505 0%, #1a1a2e 100%)"
        surface = "rgba(20, 20, 35, 0.6)"
        surface_hover = "rgba(30, 30, 50, 0.8)"
        border = "rgba(0, 242, 255, 0.15)"
        text_main = "#ffffff"
        text_sub = "#a0a0a0"
        glow = "0 0 20px rgba(0, 242, 255, 0.2)"
        input_bg = "rgba(0,0,0,0.5)"
    else:
        # Quantum Light
        primary = "#2563eb"        # Royal Blue
        secondary = "#9333ea"      # Purple
        bg_grad = "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)"
        surface = "rgba(255, 255, 255, 0.7)"
        surface_hover = "rgba(255, 255, 255, 0.95)"
        border = "rgba(37, 99, 235, 0.15)"
        text_main = "#0f172a"
        text_sub = "#64748b"
        glow = "0 0 20px rgba(37, 99, 235, 0.1)"
        input_bg = "#ffffff"

    css_code = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

        :root {{
            --primary: {primary};
            --secondary: {secondary};
            --bg-grad: {bg_grad};
            --surface: {surface};
            --surface-hover: {surface_hover};
            --border: {border};
            --text-main: {text_main};
            --text-sub: {text_sub};
            --glow: {glow};
            --input-bg: {input_bg};
        }}

        html, body, [class*="css"] {{
            font-family: 'Space Grotesk', sans-serif;
            color: var(--text-main);
        }}

        .stApp {{
            background: var(--bg-grad);
            background-attachment: fixed;
            background-size: cover;
        }}
        
        /* Hide Default Elements */
        #MainMenu, footer, header {{visibility: hidden;}}
        
        /* ---------------------------------------------------------------------
           QUANTUM CARD (3D TILT EFFECT & GLASS)
           --------------------------------------------------------------------- */
        .quantum-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 3rem;
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            box-shadow: var(--glow), 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }}
        
        .quantum-card:hover {{
            transform: translateY(-5px) scale(1.01);
            border-color: var(--primary);
            box-shadow: 0 0 40px rgba(var(--primary), 0.3);
        }}

        /* Neon Line Animation */
        .quantum-card::after {{
            content: '';
            position: absolute;
            bottom: 0; left: 0; width: 0%; height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            transition: width 0.5s ease;
        }}
        
        .quantum-card:hover::after {{
            width: 100%;
        }}

        /* ---------------------------------------------------------------------
           INPUT FIELDS (NEON GLOW)
           --------------------------------------------------------------------- */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {{
            background-color: var(--input-bg) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            transition: all 0.3s ease !important;
        }}

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 15px var(--primary) !important;
            transform: scale(1.02);
        }}
        
        .stSelectbox > div > div > div {{
            background-color: var(--input-bg) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }}

        /* ---------------------------------------------------------------------
           BUTTONS (HOLOGRAPHIC)
           --------------------------------------------------------------------- */
        .stButton > button {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 1rem 3rem !important;
            font-weight: 700 !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
            width: 100%;
        }}

        .stButton > button:hover {{
            transform: translateY(-5px) !important;
            box-shadow: 0 0 30px var(--primary) !important;
            filter: brightness(1.2);
        }}

        /* ---------------------------------------------------------------------
           WIZARD PROGRESS BAR
           --------------------------------------------------------------------- */
        .wizard-progress {{
            width: 100%;
            height: 6px;
            background: rgba(128,128,128,0.2);
            border-radius: 10px;
            margin-bottom: 2rem;
            overflow: hidden;
        }}
        
        .wizard-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* ---------------------------------------------------------------------
           UTILITIES
           --------------------------------------------------------------------- */
        .nav-bar {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px 30px; background: var(--surface); border: 1px solid var(--border);
            border-radius: 50px; margin-bottom: 40px; backdrop-filter: blur(20px);
        }}
        
        .nav-title {{ font-weight: 800; letter-spacing: 1px; color: var(--primary); }}

        @keyframes float {{
            0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} 100% {{ transform: translateY(0px); }}
        }}
        .float-anim {{ animation: float 6s ease-in-out infinite; }}
        
        .animate-slide {{ animation: slideIn 0.5s ease-out forwards; }}
        @keyframes slideIn {{ from {{ opacity: 0; transform: translateX(20px); }} to {{ opacity: 1; transform: translateX(0); }} }}

    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# ==============================================================================
# 4. BACKEND LOGIC
# ==============================================================================
def toggle_theme():
    st.session_state.theme_mode = "Dark" if st.session_state.theme_toggle else "Light"

def go_to_page(page_name):
    st.session_state.page = page_name
    st.session_state.wizard_step = 0 # Reset wizard on navigation

def reset_interview():
    st.session_state.page = "interview"
    st.session_state.ai_results = {}
    st.session_state.score = None
    st.session_state.inputs = {}
    st.session_state.wizard_step = 0

def next_step():
    st.session_state.wizard_step += 1

def prev_step():
    st.session_state.wizard_step -= 1

@st.cache_resource
def load_ml_model():
    try: return joblib.load(MODEL_FILE)
    except: return None

def call_gemini(prompt, is_json=True):
    if not API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    if is_json: payload["generationConfig"] = {"responseMimeType": "application/json"}
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
    except: pass
    return None

# ==============================================================================
# 5. UI COMPONENTS
# ==============================================================================
def render_navbar():
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2,6,2])
    with c1: st.markdown('<div class="nav-title">MINDCHECK AI</div>', unsafe_allow_html=True)
    with c2: 
        if st.button("DASHBOARD HOME", key="nav_home"): go_to_page("home"); st.rerun()
    with c3:
        st.toggle("Night Mode", value=(st.session_state.theme_mode=="Dark"), key="theme_toggle", on_change=toggle_theme)
    st.markdown('</div>', unsafe_allow_html=True)

def show_loader(duration=3):
    loader_html = """
    <style>
        .loader-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9); z-index: 9999;
            display: flex; justify-content: center; align-items: center; flex-direction: column;
            backdrop-filter: blur(20px);
        }
        .quantum-spinner {
            width: 80px; height: 80px; border: 5px solid transparent;
            border-top-color: #00f2ff; border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% {transform: rotate(0deg);} 100% {transform: rotate(360deg);} }
    </style>
    <div class="loader-overlay">
        <div class="quantum-spinner"></div>
        <h3 style="color:white; margin-top:20px; font-family:'Space Grotesk';">QUANTUM ANALYSIS INITIATED...</h3>
    </div>
    """
    placeholder = st.empty()
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    time.sleep(duration)
    placeholder.empty()

# ==============================================================================
# 6. APP EXECUTION
# ==============================================================================
inject_quantum_engine()
render_navbar()
model = load_ml_model()
MODEL_COLUMNS = ['Age', 'Gender', 'Academic_Level', 'Avg_Daily_Usage_Hours', 'Affects_Academic_Performance', 'Sleep_Hours_Per_Night', 'Conflicts_Over_Social_Media', 'Addicted_Score', 'Most_Used_Platform_Facebook', 'Most_Used_Platform_Instagram', 'Most_Used_Platform_KakaoTalk', 'Most_Used_Platform_LINE', 'Most_Used_Platform_LinkedIn', 'Most_Used_Platform_Snapchat', 'Most_Used_Platform_TikTok', 'Most_Used_Platform_Twitter', 'Most_Used_Platform_VKontakte', 'Most_Used_Platform_WeChat', 'Most_Used_Platform_WhatsApp', 'Most_Used_Platform_YouTube', 'Relationship_Status_Complicated', 'Relationship_Status_In Relationship', 'Relationship_Status_Single']

# ==============================================================================
# 7. PAGE ROUTING
# ==============================================================================

# --- HOME PAGE ---
if st.session_state.page == "home":
    title_color = "#ffffff" if st.session_state.theme_mode == "Dark" else "#0f172a"
    st.markdown(f"""
    <div style="text-align:center; padding: 4rem 0;">
        <h1 style="font-size: 6rem; line-height:1; margin-bottom: 1rem; color:{title_color};">MindCheck AI</h1>
        <p style="font-size: 1.5rem; opacity: 0.8;">Quantum-Enhanced Mental Wellness Calculator</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(f"""
        <div class="quantum-card" style="text-align:center;">
            <div style="font-size:4rem; margin-bottom:1rem;" class="float-anim">🚀</div>
            <h3>About the Creator</h3>
            <p>Meet Mubashir Mohsin.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("READ STORY", use_container_width=True): go_to_page("about"); st.rerun()
    with col2:
        st.markdown(f"""
        <div class="quantum-card" style="text-align:center;">
            <div style="font-size:4rem; margin-bottom:1rem;" class="float-anim">🔮</div>
            <h3>Start Check-In</h3>
            <p>Begin the interactive assessment.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH WIZARD", type="primary", use_container_width=True): go_to_page("interview"); st.rerun()

# --- ABOUT PAGE ---
elif st.session_state.page == "about":
    st.markdown('<div class="quantum-card" style="text-align:center; padding: 4rem;"><h1>About the Creator</h1><p style="font-size:1.2rem; line-height:2;">"My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"</p><br><p style="opacity:0.5">- February 6, 2026</p></div>', unsafe_allow_html=True)

# --- INTERVIEW WIZARD (STEP-BY-STEP) ---
elif st.session_state.page == "interview":
    # 1. Wizard Configuration
    steps = [
        {"title": "Profile", "fields": ["Age", "Gender", "Education"]},
        {"title": "Habits", "fields": ["Platform", "Usage"]},
        {"title": "Wellness", "fields": ["Sleep", "Addiction"]},
        {"title": "Impact", "fields": ["Conflicts", "Performance"]}
    ]
    current_step_idx = st.session_state.wizard_step
    
    # 2. Progress Bar
    progress = (current_step_idx / len(steps)) * 100
    st.markdown(f"""
    <div class="wizard-progress">
        <div class="wizard-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Wizard Container
    st.markdown(f'<div class="animate-slide"><h2 style="text-align:center; margin-bottom:20px;">Step {current_step_idx + 1}: {steps[current_step_idx]["title"]}</h2>', unsafe_allow_html=True)
    
    # Use a container for the card to ensure variables persist
    with st.container():
        st.markdown('<div class="quantum-card">', unsafe_allow_html=True)
        
        # --- STEP 0: PROFILE ---
        if current_step_idx == 0:
            st.session_state.inputs['Age'] = st.number_input("How old are you?", 10, 100, st.session_state.inputs.get('Age', 15))
            st.session_state.inputs['Gender'] = st.selectbox("Gender Identity", ["Male", "Female"], index=0 if st.session_state.inputs.get('Gender') == "Male" else 1)
            st.session_state.inputs['Academic_Level'] = st.selectbox("Education Level", ["High School", "Middle School", "Undergraduate", "Graduate"])
            
            if st.button("Next Step ➔"): next_step(); st.rerun()

        # --- STEP 1: HABITS ---
        elif current_step_idx == 1:
            st.session_state.inputs['Platform'] = st.selectbox("Dominant Platform", ["TikTok", "YouTube", "Instagram", "Snapchat", "Other"])
            st.session_state.inputs['Avg_Daily_Usage_Hours'] = st.number_input("Daily Screen Time (Hours)", 0.0, 24.0, st.session_state.inputs.get('Avg_Daily_Usage_Hours', 4.0))
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ Back"): prev_step(); st.rerun()
            with c2: 
                if st.button("Next Step ➔"): next_step(); st.rerun()

        # --- STEP 2: WELLNESS ---
        elif current_step_idx == 2:
            st.session_state.inputs['Sleep'] = st.number_input("Average Sleep (Hours)", 0.0, 24.0, st.session_state.inputs.get('Sleep', 8.0))
            st.session_state.inputs['Addiction'] = st.slider("Self-Perceived Addiction (1-10)", 1, 10, st.session_state.inputs.get('Addiction', 5))
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ Back"): prev_step(); st.rerun()
            with c2: 
                if st.button("Next Step ➔"): next_step(); st.rerun()

        # --- STEP 3: IMPACT (FINAL) ---
        elif current_step_idx == 3:
            st.session_state.inputs['Conflicts'] = st.number_input("Weekly Offline Conflicts", 0, 20, st.session_state.inputs.get('Conflicts', 0))
            st.session_state.inputs['Affects_Performance'] = st.radio("Impacts Grades?", ["No", "Yes"])
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ Back"): prev_step(); st.rerun()
            with c2: 
                if st.button("🚀 FINALIZE ANALYSIS"):
                    show_loader(4)
                    # Calculate Score
                    data = st.session_state.inputs
                    base = 10 - (data['Avg_Daily_Usage_Hours'] * 0.35) - (data['Addiction'] * 0.25) + (data['Sleep'] * 0.15)
                    st.session_state.score = max(1, min(10, base))
                    go_to_page("results")
                    st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)

# --- RESULTS PAGE ---
elif st.session_state.page == "results":
    score = st.session_state.score
    data = st.session_state.inputs
    
    # Color Logic
    if score < 5: color = "#ff0055"
    elif score < 8: color = "#ffaa00"
    else: color = "#00ffaa"
    
    st.markdown(f"""
    <div class="quantum-card" style="text-align: center; border-color: {color};">
        <h4 style="letter-spacing:4px; opacity:0.7;">QUANTUM WELLNESS INDEX</h4>
        <h1 style="font-size: 8rem; color: {color}; text-shadow: 0 0 50px {color}; margin: 0;">{score:.1f}</h1>
        <p style="font-size: 1.2rem;">/ 10.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; margin: 40px 0;'>Generative Insights</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="quantum-card" style="text-align:center;"><h3>👤 Persona Analysis</h3></div>', unsafe_allow_html=True)
        if st.button("Generate Persona", use_container_width=True):
             show_loader(3)
             prompt = f"Data: {json.dumps(data)}. Return JSON: 'persona', 'analysis', 'tips'."
             res = call_gemini(prompt)
             if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
             
    with c2:
        st.markdown('<div class="quantum-card" style="text-align:center;"><h3>⏳ Time Travel</h3></div>', unsafe_allow_html=True)
        if st.button("Connect to 2029", use_container_width=True):
             show_loader(3)
             prompt = f"Message from 2029 for user: {json.dumps(data)}. Max 50 words."
             res = call_gemini(prompt, is_json=False)
             if res: st.session_state.ai_results['future'] = res; st.rerun()

    results = st.session_state.ai_results
    if results:
        if 'analysis' in results:
             r = results['analysis']
             st.markdown(f"<div class='quantum-card'><h3>{r.get('persona')}</h3><p>{r.get('analysis')}</p></div>", unsafe_allow_html=True)
        if 'future' in results:
             st.markdown(f"<div class='quantum-card'><h3>Transmission Received</h3><p style='font-family:monospace'>{results['future']}</p></div>", unsafe_allow_html=True)
             
    if st.button("RESTART SYSTEM", use_container_width=True): reset_interview(); st.rerun()

# ------------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------------
st.markdown(f"<div style='text-align:center; margin-top:50px; opacity:0.5;'><p>MindCheck AI v4.0 • Quantum Edition • 2026</p></div>", unsafe_allow_html=True)
