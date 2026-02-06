# ==============================================================================
# SOCIAL IMPACT & WELLNESS AI DASHBOARD - V2.0 (ENTERPRISE EDITION)
# ==============================================================================
# AUTHOR: Mubashir Mohsin and Gemini 3 Pro
# DATE: 2-5-2026
# PURPOSE: A Streamlit application to analyze digital habits and mental wellness.
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
# These are the exact filenames provided for the visual identity of the app.
# Ensure these files exist in the root directory.
# ==============================================================================
FAVICON_FILENAME = "Gemini_Generated_Image_5b19745b19745b19.jpg"
LOGO_FILENAME = "Gemini_Generated_Image_fq49a6fq49a6fq49.jpg"
MODEL_FILE = 'mental_health_model.joblib' 
GEMINI_MODEL = 'gemini-2.5-flash'

# Securely fetch API Key
API_KEY = st.secrets.get("GEMINI_API_KEY", None)


# ==============================================================================
# 2. PAGE SETUP & INITIALIZATION
# ==============================================================================
st.set_page_config(
    page_title="Wellness V2",
    page_icon=FAVICON_FILENAME,
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==============================================================================
# 3. GLOBAL STATE MANAGEMENT
# ==============================================================================
# Initialize session state variables to handle navigation, themes, and data persistence.
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
# These functions handle the business logic, theme toggling, and navigation.
# ==============================================================================

def toggle_theme():
    """
    Switches the session state between 'Light' and 'Dark' modes.
    Triggered by the toggle switch in the UI.
    """
    if st.session_state.theme_toggle:
        st.session_state.theme_mode = "Dark"
    else:
        st.session_state.theme_mode = "Light"

def go_to_page(page_name):
    """
    Updates the session state to navigate to a specific page.
    Args:
        page_name (str): The key for the page ('home', 'interview', 'results', etc.)
    """
    st.session_state.page = page_name

def reset_interview():
    """
    Clears all interview data to allow the user to start fresh.
    """
    st.session_state.page = "interview"
    st.session_state.ai_results = {}
    st.session_state.score = None
    st.session_state.inputs = {}

@st.cache_resource
def load_ml_model():
    """
    Loads the machine learning model from the .joblib file.
    Cached to prevent reloading on every interaction.
    """
    try:
        return joblib.load(MODEL_FILE)
    except Exception as e:
        return None

def call_gemini(prompt, is_json=True):
    """
    Handles API calls to Google's Gemini Model.
    Args:
        prompt (str): The text prompt to send.
        is_json (bool): Whether to request JSON output.
    Returns:
        str or None: The AI's response text.
    """
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
# This section defines the visual identity of the app.
# It includes a massive CSS injection that overrides Streamlit's defaults
# to create a truly custom, app-like experience.
# ==============================================================================

# 5.1 THEME PALETTES
# ------------------------------------------------------------------------------
# Detailed color tokens for both modes.
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
        "input_bg": "#ffffff",
        "input_text": "#000000",
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
        "card_bg": "rgba(255, 255, 255, 0.7)",
        "card_border": "rgba(255, 255, 255, 0.8)",
        "card_shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.07)",
        "input_bg": "#ffffff",
        "input_text": "#000000",
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

# Select current theme based on session state
current = themes[st.session_state.theme_mode]

# 5.2 DYNAMIC BACKGROUND GENERATOR
# ------------------------------------------------------------------------------
# Adds SVG patterns (emojis) to the background if a score is present.
def get_background_style(mode, score):
    base = current['bg_image']
    if st.session_state.page != "results" or score is None:
        return base
    
    # Determine Emoji
    emoji = "🌟" if score >= 6 else "🌧️"
    
    # Generate SVG
    svg = f"""
    <svg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'>
        <text x='50%' y='50%' font-size='35' text-anchor='middle' dominant-baseline='middle' opacity='0.15'>{emoji}</text>
    </svg>
    """
    b64_svg = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"url('data:image/svg+xml;base64,{b64_svg}'), {base}"

final_bg = get_background_style(st.session_state.theme_mode, st.session_state.score)

# 5.3 COMPREHENSIVE CSS INJECTION
# ------------------------------------------------------------------------------
st.markdown(f"""
<style>
    /* =========================================
       IMPORT EXTERNAL FONTS
       ========================================= */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;600&display=swap');

    /* =========================================
       ROOT VARIABLES & RESET
       ========================================= */
    :root {{
        --font-primary: 'Poppins', sans-serif;
        --font-secondary: 'Inter', sans-serif;
        --transition-speed: 0.3s;
    }}

    /* =========================================
       MAIN CONTAINER STYLING
       ========================================= */
    .stApp {{
        background: {final_bg};
        background-attachment: fixed;
        background-size: cover;
        color: {current['text_primary']};
        font-family: var(--font-primary);
        transition: background 0.5s ease-in-out;
    }}
    
    /* Remove top padding constraint from Streamlit */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }}

    /* =========================================
       TYPOGRAPHY
       ========================================= */
    h1, h2, h3, h4, h5, h6 {{
        color: {current['text_primary']} !important;
        font-family: var(--font-primary);
        font-weight: 800;
        letter-spacing: -0.5px;
    }}
    
    p, label, span, div {{
        color: {current['text_primary']};
        font-family: var(--font-secondary);
    }}
    
    .section-header {{
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: {current['highlight']} !important;
        font-weight: 700;
        margin-bottom: 1rem;
        border-bottom: 2px solid {current['highlight']};
        padding-bottom: 0.5rem;
        display: inline-block;
    }}

    /* =========================================
       INPUT ELEMENTS (TEXTBOXES, SELECTS)
       ========================================= */
    /* CRITICAL REQUIREMENT: 
       Inputs must be WHITE background with BLACK text 
       regardless of the theme mode.
    */
    
    /* Text Inputs & Number Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid {current['input_border']} !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {current['accent_primary']} !important;
        box-shadow: 0 0 0 3px {current['accent_primary']}33 !important;
        outline: none !important;
    }}

    /* Select Boxes (Dropdowns) */
    .stSelectbox > div > div > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid {current['input_border']} !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
    }}
    
    /* Dropdown Menu Items */
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 12px !important;
    }}
    
    div[data-baseweb="popover"],
    div[data-baseweb="menu"] {{
        background-color: #ffffff !important;
    }}
    
    div[role="option"] {{
        color: #000000 !important;
    }}
    
    /* Selected Value Text */
    div[data-testid="stSelectbox"] div[class*="st-"] {{
        color: #000000 !important;
    }}
    
    /* Sliders */
    .stSlider > div > div > div > div {{
        background-color: {current['accent_primary']} !important;
    }}

    /* =========================================
       BUTTONS
       ========================================= */
    .stButton > button {{
        background: {current['btn_gradient']} !important;
        color: {current['btn_text']} !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        box-shadow: {current['btn_shadow']} !important;
        transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
        width: 100%;
        text-transform: uppercase;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(1px) scale(0.98);
    }}

    /* =========================================
       CARDS & CONTAINERS (Glassmorphism)
       ========================================= */
    .glass-card {{
        background: {current['card_bg']};
        border: 1px solid {current['card_border']};
        border-radius: 24px;
        padding: 2.5rem;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: {current['card_shadow']};
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        border-color: {current['highlight']};
    }}

    /* =========================================
       NAVBAR STYLING
       ========================================= */
    .nav-container {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: {current['card_bg']};
        border: 1px solid {current['card_border']};
        backdrop-filter: blur(12px);
        padding: 10px 30px;
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: {current['card_shadow']};
    }}
    
    .nav-item {{
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* =========================================
       CUSTOM LISTS
       ========================================= */
    ul.custom-list {{
        list-style: none;
        padding: 0;
    }}
    
    ul.custom-list li {{
        padding-left: 20px;
        position: relative;
        margin-bottom: 10px;
        color: {current['text_primary']};
    }}
    
    ul.custom-list li::before {{
        content: "•";
        color: {current['highlight']};
        font-weight: bold;
        font-size: 1.5rem;
        position: absolute;
        left: 0;
        top: -5px;
    }}

    /* =========================================
       ANIMATIONS
       ========================================= */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animate-enter {{
        animation: fadeIn 0.6s ease-out forwards;
    }}
    
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 6. UI COMPONENT FUNCTIONS
# ==============================================================================

def render_navbar():
    """
    Renders the TOP NAVIGATION BAR.
    Layout: [LOGO] ----- [HOME BUTTON] ----- [THEME TOGGLE]
    This satisfies the constraint of keeping the home button in between.
    """
    # Create a container styled like a pill/bar
    st.markdown('<div class="nav-container-wrapper">', unsafe_allow_html=True)
    
    # We use Streamlit columns to layout the items horizontally
    col_logo, col_spacer1, col_home, col_spacer2, col_toggle = st.columns([1.5, 0.5, 2, 0.5, 1.5])
    
    # 1. LOGO (Left)
    with col_logo:
        if os.path.exists(LOGO_FILENAME):
            st.image(LOGO_FILENAME, width=110)
        else:
            st.markdown(f"<h3 style='margin:0; color:{current['highlight']}'>Wellness AI</h3>", unsafe_allow_html=True)

    # 2. HOME BUTTON (Center - In between)
    with col_home:
        st.markdown('<div style="display: flex; justify-content: center; height: 100%; align-items: center;">', unsafe_allow_html=True)
        # Use a secondary button style for navigation to differentiate from main actions
        if st.button("🏠 DASHBOARD HOME", key="nav_home_btn", use_container_width=True):
            go_to_page("home")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. DARK MODE TOGGLE (Right)
    with col_toggle:
        st.markdown('<div style="display: flex; justify-content: flex-end; height: 100%; align-items: center;">', unsafe_allow_html=True)
        # Theme toggle logic
        is_dark = (st.session_state.theme_mode == "Dark")
        st.toggle("Night Mode", value=is_dark, key="theme_toggle", on_change=toggle_theme)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    # Add a visual divider
    st.markdown(f"<hr style='border: 0; height: 1px; background: {current['card_border']}; margin-bottom: 2rem;'>", unsafe_allow_html=True)

def show_loader(duration=4):
    """
    Displays the custom 'Synthesizing Information' full-screen overlay.
    """
    # HTML/CSS for the loader
    loader_html = """
    <style>
        .loader-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.95); z-index: 999999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            backdrop-filter: blur(10px);
        }
        .loader-box { position: relative; width: 150px; height: 150px; }
        
        /* Ring Animation */
        .cyber-ring {
            position: absolute; border-radius: 50%; border: 4px solid transparent;
        }
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
        
        /* Heartbeat Core */
        .core {
            position: absolute; top: 50%; left: 50%; width: 20px; height: 20px;
            background: #ec4899; border-radius: 50%;
            transform: translate(-50%, -50%);
            animation: pulse 1s ease-in-out infinite;
            box-shadow: 0 0 30px #ec4899;
        }

        @keyframes spin { 0% {transform: rotate(0deg);} 100% {transform: rotate(360deg);} }
        @keyframes spin-rev { 0% {transform: rotate(360deg);} 100% {transform: rotate(-360deg);} }
        @keyframes pulse { 0% {transform: translate(-50%, -50%) scale(1);} 50% {transform: translate(-50%, -50%) scale(1.5);} 100% {transform: translate(-50%, -50%) scale(1);} }
        
        .txt {
            margin-top: 40px; color: #fff; font-family: 'Courier New', monospace;
            font-size: 1.2rem; letter-spacing: 3px; font-weight: bold;
        }
    </style>
    <div class="loader-overlay">
        <div class="loader-box">
            <div class="cyber-ring cr-1"></div>
            <div class="cyber-ring cr-2"></div>
            <div class="core"></div>
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
# This section directs the user to the correct page based on session state.
# ==============================================================================

# RENDER THE NAVIGATION BAR ON EVERY PAGE
render_navbar()

# ------------------------------------------------------------------------------
# PAGE: HOME
# ------------------------------------------------------------------------------
if st.session_state.page == "home":
    # Hero Section
    st.markdown(f"""
    <div class="animate-enter" style="text-align: center; padding: 4rem 0;">
        <h1 style="font-size: 4.5rem; margin-bottom: 1rem; background: {current['btn_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Wellness V2
        </h1>
        <p style="font-size: 1.4rem; color: {current['text_secondary']}; max-width: 700px; margin: 0 auto 3rem auto;">
            Your personal AI-powered companion for tracking digital habits and improving mental resilience.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Main Navigation Grid (3 Large Buttons)
    grid_c1, grid_c2, grid_c3 = st.columns(3, gap="large")
    
    with grid_c1:
        st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
        # Using cards for visual weight
        st.markdown(f"""
        <div style="background:{current['card_bg']}; padding:20px; border-radius:20px; text-align:center; height:100%;">
            <div style="font-size:3rem; margin-bottom:10px;">👤</div>
            <h3 style="margin-bottom:15px;">Profile</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("About Me!", use_container_width=True):
            go_to_page("about")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with grid_c2:
        st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{current['card_bg']}; padding:20px; border-radius:20px; text-align:center; height:100%; border: 2px solid {current['accent_primary']};">
            <div style="font-size:3rem; margin-bottom:10px;">🧠</div>
            <h3 style="margin-bottom:15px; color:{current['accent_primary']} !important;">MindCheck AI</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("START CHECK-IN", type="primary", use_container_width=True):
            go_to_page("interview")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with grid_c3:
        st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{current['card_bg']}; padding:20px; border-radius:20px; text-align:center; height:100%;">
            <div style="font-size:3rem; margin-bottom:10px;">📢</div>
            <h3 style="margin-bottom:15px;">News</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Latest Update", use_container_width=True):
            go_to_page("updates")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: ABOUT ME
# ------------------------------------------------------------------------------
elif st.session_state.page == "about":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 2rem;">About Me</h1>', unsafe_allow_html=True)
    
    # Simple card as requested
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; max-width: 600px; margin: 0 auto;">
        <h2 style="font-weight: 400; font-size: 2rem;">Hi.</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: LATEST UPDATES
# ------------------------------------------------------------------------------
elif st.session_state.page == "updates":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 2rem;">Latest Updates</h1>', unsafe_allow_html=True)
    
    # Simple card as requested
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; max-width: 600px; margin: 0 auto;">
        <h2 style="font-weight: 400; font-size: 2rem;">Hello</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: INTERVIEW (INPUT FORM)
# ------------------------------------------------------------------------------
elif st.session_state.page == "interview":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align:center; margin-bottom: 0.5rem;">📝 Wellness Check-In</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:{current["text_secondary"]}; margin-bottom: 3rem;">Complete the assessment below to unlock your insights.</p>', unsafe_allow_html=True)
    
    # Using a Form for better UX
    with st.form("interview_form"):
        # Create two columns for the form layout
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            st.markdown('<div class="glass-card" style="padding: 1.5rem;">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">👤 Profile Details</div>', unsafe_allow_html=True)
            
            age = st.number_input("How old are you?", 10, 100, 15, help="Your age helps us benchmark against peer groups.")
            gender = st.selectbox("Gender Identity", ["Male", "Female"])
            academic_level = st.selectbox("Education Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
            
            st.markdown('<br><div class="section-header">❤️ Health Metrics</div>', unsafe_allow_html=True)
            sleep = st.number_input("Average Sleep (Hours/Night)", 0.0, 24.0, 8.0, 0.5)
            rel_status = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced"])
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="glass-card" style="padding: 1.5rem;">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📱 Digital Footprint</div>', unsafe_allow_html=True)
            
            avg_daily_usage = st.number_input("Daily Screen Time (Hours)", 0.0, 24.0, 4.0, 0.5)
            platform = st.selectbox("Dominant Platform", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
            
            st.markdown("<br><label>Self-Perceived Addiction Level</label>", unsafe_allow_html=True)
            addiction = st.slider("", 1, 10, 5)
            
            st.markdown('<br><div class="section-header">⚠️ Impact Assessment</div>', unsafe_allow_html=True)
            affects_perf = st.radio("Does usage affect your grades/work?", ["No", "Yes"], horizontal=True)
            conflicts = st.number_input("Weekly conflicts caused by social media?", 0, 10, 0)
            st.markdown('</div>', unsafe_allow_html=True)

        # Submit Action
        st.markdown("<br>", unsafe_allow_html=True)
        col_spacer_l, col_submit, col_spacer_r = st.columns([1, 2, 1])
        with col_submit:
            submitted = st.form_submit_button("🏁 ANALYZE MY DATA")
            
        if submitted:
            # 1. Show the cool loading animation (4 seconds)
            show_loader(duration=4)
            
            # 2. Save Inputs to Session State
            st.session_state.inputs = {
                "Age": age, "Gender": gender, "Academic_Level": academic_level,
                "Avg_Daily_Usage_Hours": avg_daily_usage, "Platform": platform,
                "Addiction": addiction, "Sleep": sleep, "Relationship": rel_status,
                "Affects_Performance": affects_perf, "Conflicts": conflicts
            }
            
            # 3. Prepare Data for Model
            input_df = pd.DataFrame(0, index=[0], columns=MODEL_COLUMNS)
            try:
                # Map inputs to model format
                input_df['Gender'] = 1 if gender == "Female" else 0 
                input_df['Age'] = age
                input_df['Academic_Level'] = 1 # Simplified mapping for demo
                input_df['Avg_Daily_Usage_Hours'] = avg_daily_usage
                input_df['Addicted_Score'] = addiction
                input_df['Conflicts_Over_Social_Media'] = conflicts
                input_df['Affects_Academic_Performance'] = 1 if affects_perf == "Yes" else 0
                
                # One-hot encoding handling
                if model:
                    plat_col = f"Most_Used_Platform_{platform}"
                    if plat_col in MODEL_COLUMNS: input_df[plat_col] = 1
                    wellness_score = model.predict(input_df)[0]
                else:
                    # Fallback logic if model fails/missing
                    base = 10 - (avg_daily_usage * 0.3) - (addiction * 0.2) + (sleep * 0.2)
                    wellness_score = max(1, min(10, base))

                # 4. Update State and Navigate
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
    
    # 1. Header & Recap Section
    # -----------------------------------------
    st.markdown(f"""
    <div class="glass-card" style="padding: 1.5rem; display: flex; align-items: center; justify-content: space-between; border-left: 6px solid {current['highlight']};">
        <div>
            <span style="font-weight: 800; color: {current['highlight']}; letter-spacing: 1px;">ANALYSIS COMPLETE</span><br>
            <span style="font-size: 0.95rem; opacity: 0.8;">
                User: <b>{data.get('Age')}y {data.get('Gender')}</b> | 
                Focus: <b>{data.get('Platform')}</b> | 
                Sleep: <b>{data.get('Sleep')}h</b>
            </span>
        </div>
        <div style="font-size: 2rem;">✅</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Main Title & Restart Button
    # -----------------------------------------
    col_res_header, col_res_btn = st.columns([4, 1.2])
    with col_res_header:
        st.markdown(f'<h1 style="margin:0;">Wellness Scorecard</h1>', unsafe_allow_html=True)
    with col_res_btn:
        if st.button("🔄 RESTART?", use_container_width=True):
            show_loader(duration=2)
            reset_interview()
            st.rerun()

    # 3. Big Score Display
    # -----------------------------------------
    # Color logic for score
    if score < 4:
        s_color = current['danger']
        msg = "Immediate Detox Recommended"
    elif score < 7:
        s_color = current['warning']
        msg = "Moderate Impact Detected"
    else:
        s_color = current['success']
        msg = "Healthy Digital Balance"

    st.markdown(f"""
    <div style="text-align: center; padding: 3rem; background: {current['card_bg']}; border-radius: 30px; margin: 2rem 0; box-shadow: {current['card_shadow']}; backdrop-filter: blur(10px); border: 1px solid {current['card_border']};">
        <h4 style="margin:0; opacity:0.6; letter-spacing: 3px;">COMPOSITE WELLNESS INDEX</h4>
        <h1 style="font-size: 7rem; font-weight: 900; margin: 0; color: {s_color} !important; text-shadow: 0 0 30px {s_color}40;">
            {score:.1f}<span style="font-size: 2.5rem; opacity: 0.4; color: {current['text_primary']};">/10</span>
        </h1>
        <div style="display:inline-block; padding: 0.5rem 1.5rem; border-radius: 20px; background: {s_color}20; color: {s_color}; font-weight: bold; margin-top: 1rem;">
            {msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. AI Insights Grid
    # -----------------------------------------
    st.markdown(f'<h3 style="text-align:center; margin-bottom: 2rem; color:{current["highlight"]} !important;">✨ Generative AI Insights</h3>', unsafe_allow_html=True)
    
    col_ai_1, col_ai_2, col_ai_3 = st.columns(3, gap="medium")
    
    # Feature 1: Persona Analysis
    with col_ai_1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 2rem; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
            <h4>Profile Analysis</h4>
            <p style="font-size: 0.9rem;">Deep dive into your behavioral archetype.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Persona", key="btn_persona", use_container_width=True):
            show_loader(duration=4)
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
            <p style="font-size: 0.9rem;">Receive a message from your future self.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Connect to 2029", key="btn_future", use_container_width=True):
            show_loader(duration=4)
            with st.spinner("Establishing temporal link..."):
                prompt = f"Write a dramatic but helpful note from this user's future self in 2029 based on their current habits: {json.dumps(data)}. Max 50 words. Be encouraging but real."
                res = call_gemini(prompt, is_json=False)
                if res: 
                    st.session_state.ai_results['future'] = res
                    st.rerun()

    # Feature 3: Detox Plan
    with col_ai_3:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 2rem; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🍃</div>
            <h4>Detox Protocol</h4>
            <p style="font-size: 0.9rem;">Get a custom 3-day cleansing schedule.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Plan", key="btn_detox", use_container_width=True):
            show_loader(duration=4)
            with st.spinner("Drafting protocol..."):
                prompt = f"Create a 3-day social media detox plan for a {data['Platform']} user. Return JSON: {{'days': [{{'day': 'Day 1', 'theme': 'Theme Name', 'tasks': ['Task 1', 'Task 2']}}]}}"
                res = call_gemini(prompt)
                if res: 
                    st.session_state.ai_results['detox'] = json.loads(res)
                    st.rerun()

    # 5. Display AI Results
    # -----------------------------------------
    results = st.session_state.get('ai_results', {})
    
    if results:
        st.markdown("<hr style='margin: 3rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        st.markdown("### 🧬 Generated Insights")
        
        # Display Analysis
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {current['accent_primary']};">
                <h3 style="color:{current['accent_primary']} !important; margin-top:0;">{r.get('persona', 'User')}</h3>
                <p style="font-style: italic; font-size: 1.1rem; opacity: 0.9;">"{r.get('analysis', '')}"</p>
                <div style="margin-top: 1.5rem;">
                    <strong style="text-transform:uppercase; font-size:0.85rem; letter-spacing:1px; color:{current['text_secondary']};">Recommendations</strong>
                    <ul class="custom-list" style="margin-top: 0.5rem;">
                        {''.join([f'<li>{t}</li>' for t in r.get('tips', [])])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Display Future Message
        if 'future' in results:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {current['warning']}; background: {current['card_bg']};">
                <h3 style="color:{current['warning']} !important; margin-top:0;">📨 Incoming Transmission (2029)</h3>
                <p style="font-family: 'Courier New', monospace; font-size: 1.05rem; line-height: 1.6;">
                    {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Display Detox Plan
        if 'detox' in results:
            r = results['detox']
            days_html = ""
            for d in r.get('days', []):
                tasks = "".join([f"<li>{t}</li>" for t in d.get('tasks', [])])
                days_html += f"""
                <div style="background:rgba(255,255,255,0.05); border:1px solid {current['card_border']}; padding:1rem; border-radius:12px; margin-bottom:1rem;">
                    <strong style="color:{current['success']}; font-size:1.1rem;">{d.get('day')}: {d.get('theme')}</strong>
                    <ul class="custom-list" style="margin-top:0.5rem;">{tasks}</ul>
                </div>
                """
            
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {current['success']};">
                <h3 style="color:{current['success']} !important; margin-top:0;">🌱 Digital Detox Protocol</h3>
                {days_html}
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------------
st.markdown(f"""
<div style="text-align: center; margin-top: 5rem; opacity: 0.5; font-size: 0.8rem;">
    <p>Social Impact & Mental Health AI v2.0 • Powered by MindCheck AI • 2026</p>
</div>
""", unsafe_allow_html=True)

# End of Script
