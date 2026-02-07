# ==============================================================================
# MINDCHECK AI - MENTAL HEALTH & SOCIAL IMPACT DASHBOARD (ENTERPRISE EDITION)
# ==============================================================================
# AUTHOR: Mubashir Mohsin and Gemini (AI Assistant)
# DATE: 2-5-2026
# PURPOSE: A Streamlit application to calculate Mental Health scores based on
#          digital habits and lifestyle metrics.
# ==============================================================================

import streamlit as st
import pandas as pd
import joblib
import json
import time
import requests
import numpy as np
import base64
from PIL import Image
import os

# ==============================================================================
# 1. FILE & ASSET CONFIGURATION
# ==============================================================================
FAVICON_FILENAME = "Gemini_Generated_Image_g704tpg704tpg704.png"
LOGO_FILENAME = "Gemini_Generated_Image_g704tpg704tpg704.png"
MODEL_FILE = 'mental_health_model.joblib' 
GEMINI_MODEL = 'gemini-2.5-flash'

# Securely fetch API Key
API_KEY = st.secrets.get("GEMINI_API_KEY", None)


# ==============================================================================
# 2. PAGE SETUP & INITIALIZATION
# ==============================================================================
st.set_page_config(
    page_title="MindCheck AI",
    page_icon=FAVICON_FILENAME,
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==============================================================================
# 3. GLOBAL STATE MANAGEMENT
# ==============================================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

if "ai_results" not in st.session_state:
    st.session_state.ai_results = {} 

if "score" not in st.session_state:
    st.session_state.score = None

if "inputs" not in st.session_state:
    st.session_state.inputs = {}


# ==============================================================================
# 4. CORE FUNCTIONS (LOGIC LAYER)
# ==============================================================================

def toggle_theme():
    """Switches the session state between 'Light' and 'Dark' modes."""
    if st.session_state.theme_toggle:
        st.session_state.theme_mode = "Dark"
    else:
        st.session_state.theme_mode = "Light"

def go_to_page(page_name):
    """Updates the session state to navigate to a specific page."""
    st.session_state.page = page_name

def reset_interview():
    """Clears all interview data to allow the user to start fresh."""
    st.session_state.page = "interview"
    st.session_state.ai_results = {}
    st.session_state.score = None
    st.session_state.inputs = {}

@st.cache_resource
def load_ml_model():
    """Loads the machine learning model from the .joblib file."""
    try:
        return joblib.load(MODEL_FILE)
    except Exception as e:
        return None

def call_gemini(prompt, is_json=True):
    """Handles API calls to Google's Gemini Model."""
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

# Load the model once at startup
model = load_ml_model()

# Define the columns expected by the ML model
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
# 5. ADVANCED DESIGN SYSTEM (CSS & THEME CONFIGURATION)
# ==============================================================================

# 5.1 THEME PALETTES
themes = {
    "Dark": {
        "bg_image": "linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e1b4b 100%)",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "accent_primary": "#8b5cf6", # Violet
        "accent_secondary": "#6366f1", # Indigo
        "card_bg": "rgba(30, 41, 59, 0.4)",
        "card_border": "rgba(148, 163, 184, 0.1)",
        "card_shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.3)",
        "input_bg": "rgba(255, 255, 255, 0.95)",
        "input_text": "#0f172a",
        "input_border": "#e2e8f0",
        "btn_gradient": "linear-gradient(90deg, #6366f1, #a855f7)",
        "btn_text": "#ffffff",
        "btn_shadow": "0 4px 15px rgba(99, 102, 241, 0.4)",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "highlight": "#c084fc"
    },
    "Light": {
        "bg_image": "linear-gradient(120deg, #f0f9ff 0%, #e0f2fe 50%, #dbeafe 100%)",
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "accent_primary": "#0ea5e9", # Sky Blue
        "accent_secondary": "#3b82f6", # Blue
        "card_bg": "rgba(255, 255, 255, 0.65)",
        "card_border": "rgba(255, 255, 255, 0.9)",
        "card_shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.07)",
        "input_bg": "#ffffff",
        "input_text": "#0f172a",
        "input_border": "#cbd5e1",
        "btn_gradient": "linear-gradient(90deg, #3b82f6, #06b6d4)",
        "btn_text": "#ffffff",
        "btn_shadow": "0 4px 15px rgba(59, 130, 246, 0.3)",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "highlight": "#0ea5e9"
    }
}

current = themes[st.session_state.theme_mode]

# 5.2 DYNAMIC BACKGROUND GENERATOR
def get_background_style(mode, score):
    base = current['bg_image']
    if st.session_state.page != "results" or score is None:
        return base
    
    emoji = "🌟" if score >= 6 else "🌧️"
    svg = f"""
    <svg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'>
        <text x='50%' y='50%' font-size='35' text-anchor='middle' dominant-baseline='middle' opacity='0.1'>{emoji}</text>
    </svg>
    """
    b64_svg = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"url('data:image/svg+xml;base64,{b64_svg}'), {base}"

final_bg = get_background_style(st.session_state.theme_mode, st.session_state.score)

# 5.3 COMPREHENSIVE CSS INJECTION
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;600&display=swap');

    :root {{
        --font-primary: 'Poppins', sans-serif;
        --font-secondary: 'Inter', sans-serif;
    }}

    .stApp {{
        background: {final_bg};
        background-attachment: fixed;
        background-size: cover;
        color: {current['text_primary']};
        font-family: var(--font-primary);
    }}
    
    /* Global Reset */
    .block-container {{ padding-top: 2rem; padding-bottom: 5rem; max-width: 1000px; }}
    h1, h2, h3, h4, h5, h6 {{ color: {current['text_primary']} !important; font-family: var(--font-primary); font-weight: 700; }}
    p, label, span, div, li {{ color: {current['text_primary']}; font-family: var(--font-secondary); }}

    /* Custom Headers */
    .section-header {{
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: {current['highlight']} !important;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {current['highlight']}33;
        display: block;
        width: 100%;
    }}

    /* Inputs - Enhanced Visibility */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        background-color: {current['input_bg']} !important;
        color: {current['input_text']} !important;
        border: 1px solid {current['input_border']} !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
    }}
    
    .stSelectbox > div > div > div {{
        background-color: {current['input_bg']} !important;
        color: {current['input_text']} !important;
        border: 1px solid {current['input_border']} !important;
        border-radius: 12px !important;
    }}

    div[data-baseweb="popover"], div[data-baseweb="menu"] {{ background-color: {current['input_bg']} !important; }}
    div[role="option"] {{ color: {current['input_text']} !important; }}
    
    /* Buttons */
    .stButton > button {{
        background: {current['btn_gradient']} !important;
        color: {current['btn_text']} !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        box-shadow: {current['btn_shadow']} !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }}
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.2) !important;
    }}

    /* Glass Cards */
    .glass-card {{
        background: {current['card_bg']};
        border: 1px solid {current['card_border']};
        border-radius: 24px;
        padding: 2.5rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: {current['card_shadow']};
        margin-bottom: 2rem;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }}
    .glass-card:hover {{
        transform: translateY(-5px);
        border-color: {current['highlight']};
    }}

    /* Navbar */
    .nav-container-wrapper {{
        background: {current['card_bg']};
        border: 1px solid {current['card_border']};
        backdrop-filter: blur(15px);
        padding: 15px 30px;
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: {current['card_shadow']};
    }}

    /* Custom Lists */
    ul.custom-list {{ list-style: none; padding: 0; }}
    ul.custom-list li {{ padding-left: 25px; position: relative; margin-bottom: 12px; line-height: 1.5; }}
    ul.custom-list li::before {{
        content: "•"; color: {current['highlight']}; font-weight: bold; font-size: 1.5rem;
        position: absolute; left: 0; top: -5px;
    }}

    /* Animations */
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .animate-enter {{ animation: fadeIn 0.6s ease-out forwards; }}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 6. UI COMPONENT FUNCTIONS
# ==============================================================================

def render_navbar():
    """Renders the TOP NAVIGATION BAR."""
    st.markdown('<div class="nav-container-wrapper">', unsafe_allow_html=True)
    col_logo, col_home, col_toggle = st.columns([2, 6, 2], gap="small")
    
    with col_logo:
        if os.path.exists(LOGO_FILENAME):
            st.image(LOGO_FILENAME, width=100)
        else:
            st.markdown(f"<h3 style='margin:0; color:{current['highlight']}'>MindCheck AI</h3>", unsafe_allow_html=True)

    with col_home:
        # Centered Home Button
        st.markdown('<div style="display: flex; justify-content: center; width: 100%;">', unsafe_allow_html=True)
        if st.button("🏠 DASHBOARD HOME", key="nav_home_btn"):
            go_to_page("home")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_toggle:
        st.markdown('<div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">', unsafe_allow_html=True)
        is_dark = (st.session_state.theme_mode == "Dark")
        st.toggle("Night Mode", value=is_dark, key="theme_toggle", on_change=toggle_theme)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def show_loader(duration=4):
    """Displays the custom 'Synthesizing Information' full-screen overlay."""
    loader_html = """
    <style>
        .loader-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.95); z-index: 999999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            backdrop-filter: blur(10px);
        }
        .loader-box { position: relative; width: 120px; height: 120px; }
        .cyber-ring { position: absolute; border-radius: 50%; border: 3px solid transparent; }
        .cr-1 {
            top: 0; left: 0; width: 100%; height: 100%;
            border-top-color: #0ea5e9; border-right-color: #0ea5e9;
            animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
            box-shadow: 0 0 15px rgba(14, 165, 233, 0.5);
        }
        .cr-2 {
            top: 20%; left: 20%; width: 60%; height: 60%;
            border-bottom-color: #a855f7; border-left-color: #a855f7;
            animation: spin-rev 2s linear infinite;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.5);
        }
        @keyframes spin { 0% {transform: rotate(0deg);} 100% {transform: rotate(360deg);} }
        @keyframes spin-rev { 0% {transform: rotate(360deg);} 100% {transform: rotate(-360deg);} }
        .txt { margin-top: 30px; color: #fff; font-family: monospace; font-size: 1.1rem; letter-spacing: 3px; }
    </style>
    <div class="loader-overlay">
        <div class="loader-box">
            <div class="cyber-ring cr-1"></div>
            <div class="cyber-ring cr-2"></div>
        </div>
        <div class="txt">SYNTHESIZING...</div>
    </div>
    """
    placeholder = st.empty()
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    time.sleep(duration)
    placeholder.empty()


# ==============================================================================
# 7. MAIN APPLICATION ROUTER
# ==============================================================================

render_navbar()

# ------------------------------------------------------------------------------
# PAGE: HOME
# ------------------------------------------------------------------------------
if st.session_state.page == "home":
    # Hero Section Title Styling
    # Fix: Ensure title is solid white in Dark Mode to prevent "blocking"/low visibility
    title_style = f"font-size: 5rem; line-height: 1.1; margin-bottom: 1rem; color: {current['text_primary']};"
    
    # Only apply gradient text effect in Light Mode where contrast is sufficient
    if st.session_state.theme_mode == "Light":
        title_style += f" background: {current['btn_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;"

    st.markdown(f"""
    <div class="animate-enter" style="text-align: center; padding: 3rem 0;">
        <h1 style="{title_style}">
            MindCheck AI
        </h1>
        <p style="font-size: 1.3rem; color: {current['text_secondary']}; max-width: 700px; margin: 0 auto 4rem auto; line-height: 1.6;">
            A next-generation AI companion dedicated to analyzing digital habits and improving mental well-being.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Main Navigation Grid - Two Columns Only
    grid_c1, grid_c2 = st.columns(2, gap="large")
    
    with grid_c1:
        st.markdown('<div class="animate-enter" style="animation-delay: 0.1s;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 2rem; border-bottom: 4px solid {current['accent_secondary']}; height: 100%;">
            <div style="font-size:3.5rem; margin-bottom:15px;">👨‍💻</div>
            <h3 style="margin-bottom:10px;">About the Creator</h3>
            <p style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 20px;">Meet Mubashir Mohsin and the story behind the app.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Read Story", use_container_width=True):
            go_to_page("about")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with grid_c2:
        st.markdown('<div class="animate-enter" style="animation-delay: 0.2s;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 2rem; border: 2px solid {current['accent_primary']}; box-shadow: 0 0 20px {current['accent_primary']}33; height: 100%;">
            <div style="font-size:3.5rem; margin-bottom:15px;">🧠</div>
            <h3 style="margin-bottom:10px; color:{current['accent_primary']} !important;">Start Check-In</h3>
            <p style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 20px;">Begin your comprehensive mental health assessment.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH ASSESSMENT", type="primary", use_container_width=True):
            go_to_page("interview")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: ABOUT THE CREATOR
# ------------------------------------------------------------------------------
elif st.session_state.page == "about":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 3rem;">About the Creator</h1>', unsafe_allow_html=True)
    
    col_centered = st.columns([1, 4, 1])[1]
    with col_centered:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🚀</div>
            <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
                "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
            </p>
            <p style="opacity: 0.6; font-style: italic;">- February 6, 2026</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: INTERVIEW (INPUT FORM)
# ------------------------------------------------------------------------------
elif st.session_state.page == "interview":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align:center; margin-bottom: 0.5rem;">Mental Health Check-In</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:{current["text_secondary"]}; margin-bottom: 3rem;">Complete the assessment below to unlock your insights.</p>', unsafe_allow_html=True)
    
    with st.form("interview_form"):
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            st.markdown(f'<div class="glass-card" style="height: 100%;"><div class="section-header">👤 Profile Details</div>', unsafe_allow_html=True)
            age = st.number_input("How old are you?", 10, 100, 15)
            gender = st.selectbox("Gender Identity", ["Male", "Female"])
            academic_level = st.selectbox("Education Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
            
            st.markdown('<br><div class="section-header">❤️ Health Metrics</div>', unsafe_allow_html=True)
            sleep = st.number_input("Average Sleep (Hours/Night)", 0.0, 24.0, 8.0, 0.5)
            rel_status = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced"])
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown(f'<div class="glass-card" style="height: 100%;"><div class="section-header">📱 Digital Footprint</div>', unsafe_allow_html=True)
            avg_daily_usage = st.number_input("Daily Screen Time (Hours)", 0.0, 24.0, 4.0, 0.5)
            platform = st.selectbox("Dominant Platform", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
            
            st.markdown("<br><label style='font-size:0.9rem; font-weight:600;'>Self-Perceived Addiction Level (1-10)</label>", unsafe_allow_html=True)
            addiction = st.slider("", 1, 10, 5)
            
            st.markdown('<br><div class="section-header">⚠️ Impact Assessment</div>', unsafe_allow_html=True)
            affects_perf = st.radio("Does usage affect your grades/work?", ["No", "Yes"], horizontal=True)
            conflicts = st.number_input("Weekly conflicts caused by social media?", 0, 10, 0)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_spacer_l, col_submit, col_spacer_r = st.columns([1, 2, 1])
        with col_submit:
            submitted = st.form_submit_button("🏁 ANALYZE MY DATA")
            
        if submitted:
            show_loader(duration=4)
            
            # Save Inputs
            st.session_state.inputs = {
                "Age": age, "Gender": gender, "Academic_Level": academic_level,
                "Avg_Daily_Usage_Hours": avg_daily_usage, "Platform": platform,
                "Addiction": addiction, "Sleep": sleep, "Relationship": rel_status,
                "Affects_Performance": affects_perf, "Conflicts": conflicts
            }
            
            # Model Logic
            input_df = pd.DataFrame(0, index=[0], columns=MODEL_COLUMNS)
            try:
                input_df['Gender'] = 1 if gender == "Female" else 0 
                input_df['Age'] = age
                input_df['Academic_Level'] = 1 
                input_df['Avg_Daily_Usage_Hours'] = avg_daily_usage
                input_df['Addicted_Score'] = addiction
                input_df['Conflicts_Over_Social_Media'] = conflicts
                input_df['Affects_Academic_Performance'] = 1 if affects_perf == "Yes" else 0
                
                if model:
                    plat_col = f"Most_Used_Platform_{platform}"
                    if plat_col in MODEL_COLUMNS: input_df[plat_col] = 1
                    wellness_score = model.predict(input_df)[0]
                else:
                    base = 10 - (avg_daily_usage * 0.3) - (addiction * 0.2) + (sleep * 0.2)
                    wellness_score = max(1, min(10, base))

                st.session_state.score = wellness_score
                go_to_page("results")
                st.rerun()
            except Exception as e:
                st.error(f"Calculation Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: RESULTS DASHBOARD
# ------------------------------------------------------------------------------
elif st.session_state.page == "results":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    score = st.session_state.score
    data = st.session_state.inputs
    
    # Header & Context
    st.markdown(f"""
    <div class="glass-card" style="padding: 1.5rem; display: flex; align-items: center; justify-content: space-between; border-left: 6px solid {current['highlight']}; margin-bottom: 2rem;">
        <div>
            <span style="font-weight: 800; color: {current['highlight']}; letter-spacing: 1px; font-size: 0.9rem;">ANALYSIS COMPLETE</span><br>
            <span style="font-size: 1.1rem; font-weight: 600;">Evaluation for {data.get('Age')}y Old {data.get('Gender')}</span>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.9rem; opacity: 0.7;">Dominant Platform</span><br>
            <b>{data.get('Platform')}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_res_header, col_res_btn = st.columns([4, 1.2])
    with col_res_header:
        st.markdown(f'<h2 style="margin:0;">Mental Health Scorecard</h2>', unsafe_allow_html=True)
    with col_res_btn:
        if st.button("🔄 START OVER", use_container_width=True):
            show_loader(duration=2)
            reset_interview()
            st.rerun()

    # Score Display Logic
    if score < 4:
        s_color = current['danger']
        msg = "High Risk: Immediate Detox Recommended"
    elif score < 7:
        s_color = current['warning']
        msg = "Moderate Risk: Lifestyle Changes Needed"
    else:
        s_color = current['success']
        msg = "Healthy: Good Digital Balance"

    st.markdown(f"""
    <div style="text-align: center; padding: 4rem 2rem; background: {current['card_bg']}; border-radius: 30px; margin: 2rem 0; box-shadow: {current['card_shadow']}; backdrop-filter: blur(20px); border: 1px solid {current['card_border']};">
        <h4 style="margin:0; opacity:0.6; letter-spacing: 3px; font-size: 0.9rem; margin-bottom: 1rem;">WELLNESS INDEX</h4>
        <h1 style="font-size: 8rem; line-height: 1; font-weight: 800; margin: 0; color: {s_color} !important; text-shadow: 0 0 40px {s_color}40;">
            {score:.1f}
        </h1>
        <p style="font-size: 1.5rem; opacity: 0.5; margin-top: -10px;">out of 10</p>
        <div style="display:inline-block; padding: 0.75rem 2rem; border-radius: 50px; background: {s_color}15; color: {s_color}; font-weight: 700; margin-top: 2rem; border: 1px solid {s_color}44;">
            {msg}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Visual Progress Bar
    st.progress(score / 10)

    # AI Grid - TWO Features Only
    st.markdown(f'<h3 style="text-align:center; margin: 4rem 0 2rem 0; color:{current["highlight"]} !important;">✨ Generative AI Insights</h3>', unsafe_allow_html=True)
    
    col_ai_1, col_ai_2 = st.columns(2, gap="medium")
    
    # Feature 1: Persona
    with col_ai_1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 2rem; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
            <h4>Profile Analysis</h4>
            <p style="font-size: 0.9rem; margin-bottom: 1.5rem;">Deep dive into your behavioral archetype.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Persona", key="btn_persona", use_container_width=True):
            show_loader(duration=3)
            with st.spinner("Analyzing behavioral patterns..."):
                prompt = f"Based on this user data: {json.dumps(data)}. Return JSON with keys: 'persona' (Creative 2-3 word title), 'analysis' (1 sentence summary), 'tips' (Array of 2 short actionable tips)."
                res = call_gemini(prompt)
                if res: 
                    st.session_state.ai_results['analysis'] = json.loads(res)
                    st.rerun()

    # Feature 2: Time Travel
    with col_ai_2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 2rem; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🕰️</div>
            <h4>Time Travel</h4>
            <p style="font-size: 0.9rem; margin-bottom: 1.5rem;">Receive a message from your future self.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Connect to 2029", key="btn_future", use_container_width=True):
            show_loader(duration=3)
            with st.spinner("Establishing temporal link..."):
                prompt = f"Write a dramatic but helpful note from this user's future self in 2029 based on their current habits: {json.dumps(data)}. Max 50 words. Be encouraging but real."
                res = call_gemini(prompt, is_json=False)
                if res: 
                    st.session_state.ai_results['future'] = res
                    st.rerun()

    # Results Display Area
    results = st.session_state.get('ai_results', {})
    if results:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {current['accent_primary']};">
                <h3 style="color:{current['accent_primary']} !important; margin-top:0;">{r.get('persona', 'User')}</h3>
                <p style="font-style: italic; font-size: 1.1rem; opacity: 0.9; margin-bottom: 1.5rem;">"{r.get('analysis', '')}"</p>
                <div style="background: rgba(0,0,0,0.05); padding: 1.5rem; border-radius: 12px;">
                    <strong style="text-transform:uppercase; font-size:0.8rem; letter-spacing:1px; color:{current['text_secondary']};">Key Recommendations</strong>
                    <ul class="custom-list" style="margin-top: 0.5rem;">
                        {''.join([f'<li>{t}</li>' for t in r.get('tips', [])])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if 'future' in results:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {current['warning']}; background: {current['card_bg']};">
                <div style="display:flex; align-items:center; margin-bottom:1rem;">
                    <span style="background:{current['warning']}; color:#fff; padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:bold; margin-right:10px;">INCOMING</span>
                    <h3 style="color:{current['warning']} !important; margin:0;">Transmission from 2029</h3>
                </div>
                <p style="font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.6;">
                    {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------------
st.markdown(f"""
<div style="text-align: center; margin-top: 5rem; padding-top: 2rem; border-top: 1px solid {current['card_border']}; opacity: 0.6; font-size: 0.85rem;">
    <p>MindCheck AI v2.0 &nbsp;•&nbsp; Empowered by Gemini Models &nbsp;•&nbsp; 2026</p>
</div>
""", unsafe_allow_html=True)
