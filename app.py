# ==============================================================================
# MINDCHECK AI - TITANIUM EDITION (ENTERPRISE BUILD v3.0)
# ==============================================================================
# AUTHOR: Mubashir Mohsin & Gemini
# ENGINE: Titanium UI / CSS 4.0
# DATE: 2026-02-06
# ==============================================================================

import streamlit as st
import pandas as pd
import joblib
import json
import time
import requests
import os
import base64

# ==============================================================================
# 1. SYSTEM CONFIGURATION & CONSTANTS
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
# 2. STATE MANAGEMENT & INITIALIZATION
# ==============================================================================
# We use a dictionary-based approach for cleaner state handling
DEFAULTS = {
    "page": "home",
    "theme_mode": "Light",
    "score": None,
    "inputs": {},
    "ai_results": {},
    "loading": False
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==============================================================================
# 3. THE TITANIUM CSS ENGINE (MASSIVE STYLING CORE)
# ==============================================================================
# This engine handles all visual transformations, animations, and responsive logic.
# ==============================================================================

def inject_titanium_engine():
    # Define Dynamic Color Palettes based on state
    if st.session_state.theme_mode == "Dark":
        # Cyberpunk / Deep Space Theme
        primary = "#8B5CF6"        # Vivid Violet
        secondary = "#EC4899"      # Neon Pink
        bg_grad = "linear-gradient(135deg, #0F172A 0%, #020617 100%)"
        surface = "rgba(30, 41, 59, 0.4)"
        surface_hover = "rgba(30, 41, 59, 0.7)"
        border = "rgba(139, 92, 246, 0.2)"
        text_main = "#F8FAFC"
        text_sub = "#94A3B8"
        shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.5)"
        input_bg = "rgba(15, 23, 42, 0.8)"
    else:
        # Aurora / Clean Tech Theme
        primary = "#0EA5E9"        # Sky Blue
        secondary = "#6366F1"      # Indigo
        bg_grad = "linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%)"
        surface = "rgba(255, 255, 255, 0.65)"
        surface_hover = "rgba(255, 255, 255, 0.85)"
        border = "rgba(255, 255, 255, 0.8)"
        text_main = "#0F172A"
        text_sub = "#475569"
        shadow = "0 8px 32px 0 rgba(31, 38, 135, 0.07)"
        input_bg = "#FFFFFF"

    css_code = f"""
    <style>
        /* ---------------------------------------------------------------------
           1. FONT IMPORT & GLOBAL RESET
           --------------------------------------------------------------------- */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

        :root {{
            --primary: {primary};
            --secondary: {secondary};
            --bg-grad: {bg_grad};
            --surface: {surface};
            --surface-hover: {surface_hover};
            --border: {border};
            --text-main: {text_main};
            --text-sub: {text_sub};
            --shadow: {shadow};
            --input-bg: {input_bg};
            --radius-sm: 8px;
            --radius-md: 16px;
            --radius-lg: 24px;
            --radius-full: 9999px;
            --trans-speed: 0.3s;
        }}

        html, body, [class*="css"] {{
            font-family: 'Outfit', sans-serif;
            color: var(--text-main);
        }}

        .stApp {{
            background: var(--bg-grad);
            background-attachment: fixed;
            background-size: cover;
        }}

        /* Hide Streamlit Default Elements for cleanliness */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .stDeployButton {{display:none;}}

        /* ---------------------------------------------------------------------
           2. TYPOGRAPHY SYSTEM
           --------------------------------------------------------------------- */
        h1 {{
            font-weight: 800;
            letter-spacing: -1.5px;
            line-height: 1.1;
        }}
        
        h2 {{
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        
        h3, h4 {{
            font-weight: 600;
            opacity: 0.9;
        }}

        p, label, span, div {{
            font-weight: 400;
            line-height: 1.6;
        }}

        code {{
            font-family: 'JetBrains Mono', monospace;
            background: rgba(0,0,0,0.1);
            padding: 2px 6px;
            border-radius: 4px;
        }}

        /* ---------------------------------------------------------------------
           3. TITANIUM CARD ENGINE (The core container style)
           --------------------------------------------------------------------- */
        .titan-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 2.5rem;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
            transition: all var(--trans-speed) cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .titan-card:hover {{
            transform: translateY(-5px) scale(1.005);
            border-color: var(--primary);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            background: var(--surface-hover);
        }}

        /* Ambient Glow Effect behind cards */
        .titan-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .titan-card:hover::before {{
            opacity: 1;
        }}

        /* ---------------------------------------------------------------------
           4. INTERACTIVE INPUT FIELD STYLING
           --------------------------------------------------------------------- */
        /* Text Inputs & Numbers */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {{
            background-color: var(--input-bg) !important;
            color: var(--text-main) !important;
            border: 2px solid transparent !important;
            border-radius: var(--radius-md) !important;
            padding: 12px 15px !important;
            font-family: 'Outfit', sans-serif !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2) !important;
            transform: translateY(-1px);
        }}

        /* Select Boxes */
        .stSelectbox > div > div > div {{
            background-color: var(--input-bg) !important;
            color: var(--text-main) !important;
            border-radius: var(--radius-md) !important;
            border: 1px solid var(--border) !important;
            font-weight: 500 !important;
        }}

        /* Dropdown Menus */
        div[data-baseweb="popover"], div[data-baseweb="menu"] {{
            background-color: var(--input-bg) !important;
            border: 1px solid var(--border) !important;
            backdrop-filter: blur(20px);
        }}
        
        div[role="option"] {{
            color: var(--text-main) !important;
        }}
        
        div[role="option"]:hover {{
            background-color: var(--primary) !important;
            color: #fff !important;
        }}

        /* Sliders */
        .stSlider > div > div > div > div {{
            background-color: var(--primary) !important;
        }}

        /* Radio Buttons */
        .stRadio > div {{
            background: transparent !important;
        }}

        /* ---------------------------------------------------------------------
           5. BUTTON ARCHITECTURE
           --------------------------------------------------------------------- */
        .stButton > button {{
            width: 100%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: var(--radius-full) !important;
            padding: 0.8rem 2rem !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
            position: relative;
            overflow: hidden;
        }}

        .stButton > button:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 30px rgba(0,0,0,0.2) !important;
            filter: brightness(1.1);
        }}

        .stButton > button:active {{
            transform: translateY(1px) !important;
            box-shadow: 0 5px 10px rgba(0,0,0,0.1) !important;
        }}

        /* Secondary Button Variation (Ghost) */
        button[kind="secondary"] {{
            background: transparent !important;
            border: 2px solid var(--text-sub) !important;
            color: var(--text-sub) !important;
        }}

        /* ---------------------------------------------------------------------
           6. NAVIGATION BAR STYLING
           --------------------------------------------------------------------- */
        .nav-container {{
            background: var(--surface);
            border: 1px solid var(--border);
            backdrop-filter: blur(15px);
            padding: 15px 30px;
            border-radius: var(--radius-full);
            margin-bottom: 40px;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .nav-brand {{
            font-weight: 800;
            font-size: 1.2rem;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* ---------------------------------------------------------------------
           7. ANIMATION KEYFRAMES
           --------------------------------------------------------------------- */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.4); }}
            70% {{ box-shadow: 0 0 0 15px rgba(139, 92, 246, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }}
        }}

        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .animate-enter {{
            animation: fadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }}
        
        .animate-float {{
            animation: float 6s ease-in-out infinite;
        }}

        /* ---------------------------------------------------------------------
           8. CUSTOM UTILITY CLASSES
           --------------------------------------------------------------------- */
        .text-gradient {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .section-label {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--secondary);
            font-weight: 700;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
            display: block;
        }}

        .stat-value {{
            font-size: 4rem;
            font-weight: 800;
            color: var(--primary);
            line-height: 1;
        }}

        .footer-container {{
            margin-top: 5rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--text-sub);
            font-size: 0.9rem;
            opacity: 0.7;
        }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# ==============================================================================
# 4. LOGIC LAYER (BACKEND FUNCTIONS)
# ==============================================================================

def toggle_theme():
    """Toggles dark/light mode and forces a rerun."""
    if st.session_state.theme_toggle:
        st.session_state.theme_mode = "Dark"
    else:
        st.session_state.theme_mode = "Light"

def go_to_page(page_name):
    """Router function to switch pages."""
    st.session_state.page = page_name

def reset_interview():
    """Resets all session data for a new assessment."""
    st.session_state.page = "interview"
    st.session_state.ai_results = {}
    st.session_state.score = None
    st.session_state.inputs = {}

@st.cache_resource
def load_ml_model():
    """Attempts to load the ML model, handles failure gracefully."""
    try:
        return joblib.load(MODEL_FILE)
    except:
        return None

def call_gemini(prompt, is_json=True):
    """
    Robust API caller for Google Gemini.
    Includes timeout handling and JSON parsing support.
    """
    if not API_KEY: return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    if is_json:
        payload["generationConfig"] = {"responseMimeType": "application/json"}
    
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=20)
        if response.status_code == 200:
            result = response.json()
            return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
    except Exception as e:
        st.error(f"AI Connection Error: {e}")
        return None
    return None

# ==============================================================================
# 5. UI COMPONENT LIBRARY (Reusable Widgets)
# ==============================================================================

def render_navbar():
    """Renders the custom Glassmorphism Navbar."""
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3, 5, 2], gap="small")
    
    with c1:
        st.markdown('<div class="nav-brand">MindCheck AI</div>', unsafe_allow_html=True)
    
    with c2:
        # Centered Home Action
        st.markdown('<div style="display:flex; justify-content:center; width:100%">', unsafe_allow_html=True)
        if st.button("🏠 DASHBOARD", key="nav_home"):
            go_to_page("home")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        # Theme Toggle
        st.markdown('<div style="display:flex; justify-content:flex-end">', unsafe_allow_html=True)
        is_dark = (st.session_state.theme_mode == "Dark")
        st.toggle("Night Mode", value=is_dark, key="theme_toggle", on_change=toggle_theme)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_loader(duration=3):
    """
    Displays a CSS-only complex loader animation.
    This replaces the standard Streamlit spinner with something 'Titanium'.
    """
    loader_css = """
    <style>
        .titan-loader-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); z-index: 9999;
            backdrop-filter: blur(15px);
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
        }
        .scanner {
            position: relative; width: 200px; height: 4px; background: #333;
            border-radius: 4px; overflow: hidden;
        }
        .scanner::after {
            content: ''; position: absolute; top: 0; left: 0; width: 40%; height: 100%;
            background: linear-gradient(90deg, transparent, #8B5CF6, transparent);
            animation: scan 1s infinite ease-in-out alternate;
        }
        @keyframes scan { from { left: 0; } to { left: 60%; } }
        .loader-text {
            color: white; font-family: 'JetBrains Mono'; margin-top: 20px;
            letter-spacing: 2px; font-size: 0.9rem;
        }
    </style>
    <div class="titan-loader-overlay">
        <div class="scanner"></div>
        <div class="loader-text">PROCESSING NEURAL DATA...</div>
    </div>
    """
    placeholder = st.empty()
    placeholder.markdown(loader_css, unsafe_allow_html=True)
    time.sleep(duration)
    placeholder.empty()

# ==============================================================================
# 6. APPLICATION EXECUTION START
# ==============================================================================

# Inject the Massive CSS Engine
inject_titanium_engine()

# Render Global Navigation
render_navbar()

# Load Model
model = load_ml_model()
MODEL_COLUMNS = [
    'Age', 'Gender', 'Academic_Level', 'Avg_Daily_Usage_Hours', 
    'Affects_Academic_Performance', 'Sleep_Hours_Per_Night', 
    'Conflicts_Over_Social_Media', 'Addicted_Score', 
    'Most_Used_Platform_Facebook', 'Most_Used_Platform_Instagram', 
    'Most_Used_Platform_KakaoTalk', 'Most_Used_Platform_LINE', 
    'Most_Used_Platform_LinkedIn', 'Most_Used_Platform_Snapchat', 
    'Most_Used_Platform_TikTok', 'Most_Used_Platform_Twitter', 
    'Most_Used_Platform_VKontakte', 'Most_Used_Platform_WeChat', 
    'Most_Used_Platform_WhatsApp', 'Most_Used_Platform_YouTube', 'Relationship_Status_Complicated', 
    'Relationship_Status_In Relationship', 'Relationship_Status_Single'
]

# ==============================================================================
# 7. PAGE ROUTING & LAYOUTS
# ==============================================================================

# ------------------------------------------------------------------------------
# PAGE: HOME DASHBOARD
# ------------------------------------------------------------------------------
if st.session_state.page == "home":
    
    # Hero Text Logic (Handles Night Mode Contrast Issue)
    title_classes = "animate-enter"
    title_style = "font-size: 5.5rem; text-align: center; margin-bottom: 0.5rem;"
    
    if st.session_state.theme_mode == "Light":
        # Apply Gradient only in light mode
        inner_html = '<span class="text-gradient">MindCheck AI</span>'
    else:
        # Solid white in dark mode for accessibility
        inner_html = '<span style="color: #fff;">MindCheck AI</span>'

    st.markdown(f"""
    <div class="{title_classes}" style="padding: 4rem 0; text-align: center;">
        <h1 style="{title_style}">{inner_html}</h1>
        <p style="font-size: 1.4rem; max-width: 650px; margin: 0 auto; opacity: 0.8;">
            The enterprise-grade digital wellness companion powered by advanced generative AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2-Column Grid Layout (No News Feed)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="animate-enter" style="animation-delay: 0.1s; height: 100%;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="titan-card" style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;" class="animate-float">👨‍💻</div>
            <h3>About the Creator</h3>
            <p style="margin-bottom: 2rem;">Discover the story of Mubashir Mohsin and the origin of MindCheck.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Read Profile", use_container_width=True):
            go_to_page("about")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="animate-enter" style="animation-delay: 0.2s; height: 100%;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="titan-card" style="text-align: center; border-color: var(--primary);">
            <div style="font-size: 4rem; margin-bottom: 1rem;" class="animate-float">🧠</div>
            <h3 style="color: var(--primary);">Start Check-In</h3>
            <p style="margin-bottom: 2rem;">Initialize the comprehensive mental health assessment protocol.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH SYSTEM", type="primary", use_container_width=True):
            go_to_page("interview")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: ABOUT THE CREATOR
# ------------------------------------------------------------------------------
elif st.session_state.page == "about":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 3rem;">Origin Story</h1>', unsafe_allow_html=True)
    
    # Layout constraint for better readability
    c_spacer_l, c_content, c_spacer_r = st.columns([1, 4, 1])
    
    with c_content:
        st.markdown(f"""
        <div class="titan-card" style="text-align: center; padding: 4rem;">
            <div style="font-size: 5rem; margin-bottom: 2rem;">🚀</div>
            <p style="font-size: 1.25rem; line-height: 2; margin-bottom: 2rem; font-weight: 300;">
                "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
            </p>
            <div style="height: 1px; width: 50px; background: var(--primary); margin: 0 auto 1rem auto;"></div>
            <p style="font-family: 'JetBrains Mono'; font-size: 0.9rem; opacity: 0.6;">
                LOG TIMESTAMP: FEBRUARY 6, 2026
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: ASSESSMENT INTERVIEW
# ------------------------------------------------------------------------------
elif st.session_state.page == "interview":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align:center;">Assessment Protocol</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; margin-bottom: 3rem; opacity: 0.7;">Please input your biometrics and digital habits below.</p>', unsafe_allow_html=True)
    
    with st.form("interview_form"):
        col1, col2 = st.columns(2, gap="large")
        
        # Left Column: Bio Data
        with col1:
            st.markdown(f"""
            <div class="titan-card" style="height: 100%;">
                <span class="section-label">01 // BIOMETRICS</span>
            """, unsafe_allow_html=True)
            
            age = st.number_input("Age", 10, 100, 15)
            gender = st.selectbox("Gender Identity", ["Male", "Female"])
            academic_level = st.selectbox("Education Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
            
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            st.markdown('<span class="section-label">02 // HEALTH</span>', unsafe_allow_html=True)
            
            sleep = st.number_input("Avg Sleep (Hours)", 0.0, 24.0, 8.0, 0.5)
            rel_status = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced"])
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Right Column: Digital Data
        with col2:
            st.markdown(f"""
            <div class="titan-card" style="height: 100%;">
                <span class="section-label">03 // DIGITAL FOOTPRINT</span>
            """, unsafe_allow_html=True)
            
            avg_daily_usage = st.number_input("Screen Time (Daily Hrs)", 0.0, 24.0, 4.0, 0.5)
            platform = st.selectbox("Dominant Platform", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
            
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            
            st.markdown('<label>Self-Perceived Addiction (1-10)</label>', unsafe_allow_html=True)
            addiction = st.slider("", 1, 10, 5)
            
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            
            st.markdown('<span class="section-label">04 // IMPACT ANALYSIS</span>', unsafe_allow_html=True)
            affects_perf = st.radio("Impacts Academic Performance?", ["No", "Yes"], horizontal=True)
            conflicts = st.number_input("Weekly Offline Conflicts", 0, 10, 0)
            
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit Logic
        c_sub_1, c_sub_2, c_sub_3 = st.columns([1, 2, 1])
        with c_sub_2:
            submitted = st.form_submit_button("INITIATE ANALYSIS")
            
        if submitted:
            show_loader(duration=3)
            
            # 1. State Update
            st.session_state.inputs = {
                "Age": age, "Gender": gender, "Academic_Level": academic_level,
                "Avg_Daily_Usage_Hours": avg_daily_usage, "Platform": platform,
                "Addiction": addiction, "Sleep": sleep, "Relationship": rel_status,
                "Affects_Performance": affects_perf, "Conflicts": conflicts
            }
            
            # 2. Score Calculation
            input_df = pd.DataFrame(0, index=[0], columns=MODEL_COLUMNS)
            try:
                # Basic mapping logic
                input_df['Gender'] = 1 if gender == "Female" else 0 
                input_df['Age'] = age
                input_df['Avg_Daily_Usage_Hours'] = avg_daily_usage
                input_df['Addicted_Score'] = addiction
                
                # ML Prediction or Fallback
                if model:
                    plat_col = f"Most_Used_Platform_{platform}"
                    if plat_col in MODEL_COLUMNS: input_df[plat_col] = 1
                    wellness_score = model.predict(input_df)[0]
                else:
                    # Fallback Algorithm
                    base = 10 - (avg_daily_usage * 0.35) - (addiction * 0.25) + (sleep * 0.15)
                    wellness_score = max(1, min(10, base))

                st.session_state.score = wellness_score
                go_to_page("results")
                st.rerun()
            except Exception as e:
                st.error(f"System Failure: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: RESULTS ANALYTICS
# ------------------------------------------------------------------------------
elif st.session_state.page == "results":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    score = st.session_state.score
    data = st.session_state.inputs
    
    # Context Header
    st.markdown(f"""
    <div class="titan-card" style="padding: 1.5rem; display: flex; align-items: center; justify-content: space-between; border-left: 6px solid var(--primary); margin-bottom: 2rem;">
        <div>
            <span style="font-weight: 800; color: var(--primary); letter-spacing: 1px; font-size: 0.9rem;">STATUS: COMPLETE</span><br>
            <span style="font-size: 1.1rem; font-weight: 600;">Subject: {data.get('Age')}y / {data.get('Gender')}</span>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.9rem; opacity: 0.7;">Focus Vector</span><br>
            <b>{data.get('Platform')}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Title & Restart
    c_head, c_btn = st.columns([4, 1.5])
    with c_head:
        st.markdown(f'<h2 style="margin:0;">Wellness Diagnostics</h2>', unsafe_allow_html=True)
    with c_btn:
        if st.button("🔄 RE-CALIBRATE", use_container_width=True):
            show_loader(duration=2)
            reset_interview()
            st.rerun()

    # Score Logic
    if score < 4:
        s_color = "#EF4444" # Red
        msg = "CRITICAL: Immediate Digital Detox Required"
    elif score < 7:
        s_color = "#F59E0B" # Orange
        msg = "WARNING: Moderate Lifestyle Adjustment Needed"
    else:
        s_color = "#10B981" # Green
        msg = "OPTIMAL: Sustainable Digital Habits Detected"

    # Big Score Card
    st.markdown(f"""
    <div class="titan-card" style="text-align: center; padding: 4rem 2rem; position: relative; overflow: hidden;">
        <div style="position: absolute; top:0; left:0; width:100%; height:10px; background: {s_color};"></div>
        <h4 style="margin:0; opacity:0.6; letter-spacing: 3px; font-size: 0.9rem; margin-bottom: 1rem;">COMPOSITE INDEX</h4>
        <h1 style="font-size: 8rem; line-height: 1; margin: 0; color: {s_color} !important; text-shadow: 0 0 50px {s_color}44;">
            {score:.1f}
        </h1>
        <p style="font-size: 1.5rem; opacity: 0.5; margin-top: -10px;">/ 10.0</p>
        <div style="display:inline-block; padding: 0.75rem 2rem; border-radius: 50px; background: {s_color}22; color: {s_color}; font-weight: 700; margin-top: 2rem; border: 1px solid {s_color};">
            {msg}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(score / 10)

    # AI Feature Grid - Only 2 Features as requested
    st.markdown(f'<h3 style="text-align:center; margin: 4rem 0 2rem 0;">Generative Insights</h3>', unsafe_allow_html=True)
    
    col_ai_1, col_ai_2 = st.columns(2, gap="medium")
    
    # Feature 1: Persona
    with col_ai_1:
        st.markdown(f"""
        <div class="titan-card" style="text-align:center; padding: 2rem; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
            <h4>Psychometric Persona</h4>
            <p style="font-size: 0.9rem; margin-bottom: 1.5rem;">Generate a behavioral archetype based on your input vectors.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Persona", key="btn_persona", use_container_width=True):
            show_loader(duration=3)
            with st.spinner("Accessing Gemini Neural Net..."):
                prompt = f"Based on this user data: {json.dumps(data)}. Return JSON with keys: 'persona' (Creative 2-3 word title), 'analysis' (1 sentence summary), 'tips' (Array of 2 short actionable tips)."
                res = call_gemini(prompt)
                if res: 
                    st.session_state.ai_results['analysis'] = json.loads(res)
                    st.rerun()

    # Feature 2: Time Travel
    with col_ai_2:
        st.markdown(f"""
        <div class="titan-card" style="text-align:center; padding: 2rem; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🕰️</div>
            <h4>Temporal Bridge</h4>
            <p style="font-size: 0.9rem; margin-bottom: 1.5rem;">Receive a quantum transmission from your 2029 self.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Connect to 2029", key="btn_future", use_container_width=True):
            show_loader(duration=3)
            with st.spinner("Establishing Timeline Link..."):
                prompt = f"Write a dramatic but helpful note from this user's future self in 2029 based on their current habits: {json.dumps(data)}. Max 50 words. Be encouraging but real."
                res = call_gemini(prompt, is_json=False)
                if res: 
                    st.session_state.ai_results['future'] = res
                    st.rerun()

    # Display Results
    results = st.session_state.get('ai_results', {})
    if results:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        
        # Persona Result
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="titan-card" style="border-left: 5px solid var(--primary);">
                <span class="section-label">ANALYSIS VECTOR 01</span>
                <h3 style="color: var(--primary) !important; margin-top:0;">{r.get('persona', 'User')}</h3>
                <p style="font-style: italic; font-size: 1.1rem; opacity: 0.9; margin-bottom: 1.5rem;">"{r.get('analysis', '')}"</p>
                <div style="background: rgba(0,0,0,0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border);">
                    <strong style="text-transform:uppercase; font-size:0.8rem; letter-spacing:1px; color: var(--text-sub);">Optimization Strategy</strong>
                    <ul class="custom-list" style="margin-top: 0.5rem;">
                        {''.join([f'<li>{t}</li>' for t in r.get('tips', [])])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Future Message Result
        if 'future' in results:
            st.markdown(f"""
            <div class="titan-card" style="border-left: 5px solid #F59E0B; background: var(--surface);">
                <div style="display:flex; align-items:center; margin-bottom:1rem;">
                    <span style="background:#F59E0B; color:#000; padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:bold; margin-right:10px;">ENCRYPTED</span>
                    <h3 style="color:#F59E0B !important; margin:0;">Incoming Transmission</h3>
                </div>
                <p style="font-family: 'JetBrains Mono', monospace; font-size: 1rem; line-height: 1.6; color: var(--text-main);">
                    > {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 8. SYSTEM FOOTER
# ------------------------------------------------------------------------------
st.markdown(f"""
<div class="footer-container">
    <p>MINDCHECK AI v3.0 // TITANIUM ENGINE ACTIVE // 2026</p>
</div>
""", unsafe_allow_html=True)
