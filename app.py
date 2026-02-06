# ==============================================================================
# FILE: app.py
# PROJECT: MINDCHECK AI (LIQUID GLASS ENTERPRISE EDITION)
# VERSION: 5.0.1-STABLE
# DATE: February 2026
# AUTHOR: Gemini (AI Architecture) & Mubashir Mohsin
# ==============================================================================
#
# [ SYSTEM ARCHITECTURE DOCUMENTATION ]
#
# 1.0 CORE INFRASTRUCTURE
#     - Imports & Environment Setup
#     - Streamlit Page Configuration
#     - Session State Initialization
#
# 2.0 DATA LAYER
#     - Asset Configuration (Logos, Models)
#     - ML Model Loading (Joblib/Cache)
#     - Generative AI Interface (Gemini API)
#
# 3.0 VISUAL DESIGN SYSTEM (LUMINA GLASS v5)
#     - Theme Token Definitions (Light/Dark)
#     - CSS Variable Injection
#     - Keyframe Animation Physics
#     - Component Styling (Cards, Inputs, Buttons)
#
# 4.0 COMPONENT LIBRARY
#     - AssetLibrary (SVG Icon Repository)
#     - UI Elements (Navbar, Loaders, Modals)
#     - ContentManager (Static Text & Legal)
#
# 5.0 BUSINESS LOGIC
#     - Routing Engine
#     - Interview Logic
#     - Scoring Algorithms
#
# 6.0 EXECUTION ENTRY POINT
#     - Main Render Loop
#
# ==============================================================================

import streamlit as st
import pandas as pd
import joblib
import json
import time
import requests
import numpy as np
import base64
import random
import os
from datetime import datetime

# ==============================================================================
# 1.0 CORE INFRASTRUCTURE
# ==============================================================================

# 1.1 CONFIGURATION CONSTANTS
# ------------------------------------------------------------------------------
# Defines the structural assets required for the application to function.
FAVICON_FILENAME = "Gemini_Generated_Image_5b19745b19745b19.jpg"
LOGO_FILENAME = "Gemini_Generated_Image_fq49a6fq49a6fq49.jpg"
MODEL_FILE = 'mental_health_model.joblib'
GEMINI_MODEL = 'gemini-2.5-flash'

# 1.2 SECURITY & CREDENTIALS
# ------------------------------------------------------------------------------
# Securely fetch the Google Gemini API key from Streamlit secrets.
# Ensure .streamlit/secrets.toml is configured in your deployment environment.
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# 1.3 PAGE METADATA SETUP
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="MindCheck AI",
    page_icon=FAVICON_FILENAME,
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.mentalhealth.gov',
        'Report a bug': "mailto:support@mindcheck.ai",
        'About': "MindCheck AI v5.0\nEnterprise Mental Health Analytics"
    }
)

# ==============================================================================
# 2.0 DATA LAYER & STATE MANAGEMENT
# ==============================================================================

def init_session_state():
    """
    Initializes the session state dictionary to persist user data,
    navigation history, and theme settings across re-runs.
    """
    # Navigation State
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Theme State (Default: Light Mode)
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Light"

    # AI Analysis Cache
    if "ai_results" not in st.session_state:
        st.session_state.ai_results = {}

    # Scoring Engine State
    if "score" not in st.session_state:
        st.session_state.score = None

    # Form Input Persistence
    if "inputs" not in st.session_state:
        st.session_state.inputs = {}

    # Animation Seed (For stochastic visual effects)
    if "anim_seed" not in st.session_state:
        st.session_state.anim_seed = random.random()

    # System Diagnostics (Simulated)
    if "system_status" not in st.session_state:
        st.session_state.system_status = "ONLINE"

# Execute State Initialization
init_session_state()

# 2.1 MACHINE LEARNING INTERFACE
# ------------------------------------------------------------------------------
@st.cache_resource
def load_ml_model():
    """
    Loads the predictive model from the disk.
    Uses caching to prevent I/O blocking on main thread.
    
    Returns:
        model: The loaded joblib model object or None.
    """
    try:
        if os.path.exists(MODEL_FILE):
            return joblib.load(MODEL_FILE)
        else:
            return None
    except Exception as e:
        # Log error in production environment
        return None

# Load model globally
model = load_ml_model()

# 2.2 GENERATIVE AI INTERFACE
# ------------------------------------------------------------------------------
def call_gemini_api(prompt_text, expect_json=True):
    """
    Wrapper for Google Gemini API interactions.
    Handles JSON parsing and error management.
    
    Args:
        prompt_text (str): The instruction to send to the LLM.
        expect_json (bool): Whether to enforce JSON output formatting.
        
    Returns:
        str: The parsed response text or None if failed.
    """
    if not API_KEY:
        return None

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    
    if expect_json:
        payload["generationConfig"] = {"responseMimeType": "application/json"}

    try:
        # Set a reasonable timeout for AI generation
        response = requests.post(
            endpoint,
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return None
    except Exception:
        return None

# 2.3 DATA MODEL DEFINITIONS
# ------------------------------------------------------------------------------
MODEL_COLUMNS = [
    'Age', 'Gender', 'Academic_Level', 'Avg_Daily_Usage_Hours', 
    'Affects_Academic_Performance', 'Sleep_Hours_Per_Night', 
    'Conflicts_Over_Social_Media', 'Addicted_Score', 
    'Most_Used_Platform_Facebook', 'Most_Used_Platform_Instagram', 
    'Most_Used_Platform_KakaoTalk', 'Most_Used_Platform_LINE', 
    'Most_Used_Platform_LinkedIn', 'Most_Used_Platform_Snapchat', 
    'Most_Used_Platform_TikTok', 'Most_Used_Platform_Twitter', 
    'Most_Used_Platform_VKontakte', 'Most_Used_Platform_WeChat', 
    'Most_Used_Platform_WhatsApp', 'Most_Used_Platform_YouTube', 
    'Relationship_Status_Complicated', 
    'Relationship_Status_In Relationship', 'Relationship_Status_Single'
]

# ==============================================================================
# 3.0 VISUAL DESIGN SYSTEM (LUMINA GLASS v5)
# ==============================================================================

# 3.1 THEME TOKENS
# ------------------------------------------------------------------------------
# Defines the color palette and physics constants for the UI.
# FIX APPLIED: Added 'accent' key to map to 'accent_primary' to prevent KeyError.
themes = {
    "Dark": {
        "bg_image": "radial-gradient(circle at 20% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%)",
        "glass_bg": "rgba(20, 20, 25, 0.4)",
        "glass_border": "rgba(255, 255, 255, 0.08)",
        "glass_shine": "rgba(255, 255, 255, 0.03)",
        "text_main": "#f8fafc",
        "text_sub": "#94a3b8",
        # KEYS FIXED HERE
        "accent": "#a855f7", # Alias for backward compatibility
        "accent_primary": "#a855f7",
        "accent_secondary": "#7c3aed",
        "btn_grad": "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
        "shadow": "rgba(0, 0, 0, 0.6)",
        "highlight": "#c084fc",
        "card_blur": "40px",
        "saturation": "180%",
        "brightness": "1.1",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444"
    },
    "Light": {
        "bg_image": "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #ffffff 100%)",
        "glass_bg": "rgba(255, 255, 255, 0.65)",
        "glass_border": "rgba(255, 255, 255, 0.8)",
        "glass_shine": "rgba(255, 255, 255, 0.4)",
        "text_main": "#0f172a",
        "text_sub": "#475569",
        # KEYS FIXED HERE
        "accent": "#0ea5e9", # Alias for backward compatibility
        "accent_primary": "#0ea5e9",
        "accent_secondary": "#0284c7",
        "btn_grad": "linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)",
        "shadow": "rgba(14, 165, 233, 0.15)",
        "highlight": "#0ea5e9",
        "card_blur": "25px",
        "saturation": "160%",
        "brightness": "1.05",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444"
    }
}

current = themes[st.session_state.theme_mode]

# 3.2 DYNAMIC BACKGROUND GENERATOR
# ------------------------------------------------------------------------------
def generate_background_css():
    """
    Constructs the CSS for the main background.
    Injects a subtle particle layer if the results page is active.
    """
    base_bg = current['bg_image']
    
    if st.session_state.page != "results" or st.session_state.score is None:
        return base_bg
    
    emoji = "🌟" if st.session_state.score >= 6 else "🌧️"
    
    # Create optimized SVG pattern
    svg_pattern = f"""
    <svg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'>
        <style>
            .anim {{ animation: float 5s infinite ease-in-out; }}
            @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
        </style>
        <text x='50' y='50' class='anim' font-size='35' text-anchor='middle' dominant-baseline='middle' opacity='0.08'>{emoji}</text>
    </svg>
    """
    b64_svg = base64.b64encode(svg_pattern.encode('utf-8')).decode('utf-8')
    return f"url('data:image/svg+xml;base64,{b64_svg}'), {base_bg}"

final_bg_css = generate_background_css()

# 3.3 CSS ENGINE INJECTION
# ------------------------------------------------------------------------------
# This function injects the massive CSS block required for the Liquid Glass effect.
# It is separated into functional blocks for clarity and maintainability.
# ------------------------------------------------------------------------------
def inject_css_engine():
    st.markdown(f"""
    <style>
        /* ========================================================================
           LUMINA GLASS ENGINE v5.0 - CORE VARIABLES
           ======================================================================== */
        :root {{
            --font-stack: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Poppins', sans-serif;
            --bg-layer: {current['bg_image']};
            --glass-surface: {current['glass_bg']};
            --glass-border: {current['glass_border']};
            --glass-specular: {current['glass_shine']};
            --glass-shadow: {current['shadow']};
            --accent: {current['accent']};
            --text-main: {current['text_main']};
            --text-sub: {current['text_sub']};
            --blur-strength: {current['card_blur']};
            --saturation: {current['saturation']};
            --brightness: {current['brightness']};
            
            /* Animation Physics */
            --ease-elastic: cubic-bezier(0.175, 0.885, 0.32, 1.275);
            --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
            
            /* Geometry */
            --radius-sm: 12px;
            --radius-md: 20px;
            --radius-lg: 32px;
            --radius-pill: 100px;
        }}

        /* ========================================================================
           GLOBAL RESET & LAYOUT
           ======================================================================== */
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@100;300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');

        .stApp {{
            background: {final_bg_css};
            background-attachment: fixed;
            background-size: cover;
            font-family: var(--font-stack);
            color: var(--text-main);
            transition: background 0.8s var(--ease-smooth);
            overflow-x: hidden;
        }}

        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
            max-width: 1200px;
        }}

        /* ========================================================================
           COMPONENT: LIQUID GLASS CARD
           ======================================================================== */
        /*
           The core container for content. Uses layered shadows and filters
           to simulate a thick, refractive glass surface floating above the background.
        */
        .glass-card {{
            position: relative;
            background: var(--glass-surface);
            
            /* Optical Physics */
            backdrop-filter: blur(var(--blur-strength)) saturate(var(--saturation)) brightness(var(--brightness));
            -webkit-backdrop-filter: blur(var(--blur-strength)) saturate(var(--saturation)) brightness(var(--brightness));
            
            /* Border & Highlights */
            border: 1px solid var(--glass-border);
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            border-left: 1px solid rgba(255, 255, 255, 0.1);
            
            border-radius: var(--radius-lg);
            padding: 35px;
            margin-bottom: 30px;
            
            /* Depth Shadowing */
            box-shadow: 
                0 20px 40px -10px var(--glass-shadow),
                inset 0 0 0 1px var(--glass-specular);
                
            transform-style: preserve-3d;
            transition: transform 0.4s var(--ease-elastic), box-shadow 0.4s ease;
            overflow: hidden;
        }}

        /* Interactive Hover State - The "Lift" Effect */
        .glass-card:hover {{
            transform: translateY(-6px) scale(1.005);
            box-shadow: 
                0 30px 60px -12px var(--glass-shadow),
                inset 0 0 0 1px var(--accent);
            z-index: 10;
        }}

        /* The "Sheen" Animation */
        .glass-card::after {{
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 50%; height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.1),
                transparent
            );
            transform: skewX(-25deg);
            pointer-events: none;
            transition: 0.5s;
        }}

        .glass-card:hover::after {{
            animation: sheen-slide 1s forwards;
        }}

        @keyframes sheen-slide {{
            100% {{ left: 150%; }}
        }}

        /* ========================================================================
           COMPONENT: NAVIGATION PILL
           ======================================================================== */
        .nav-pill-container {{
            width: 100%;
            display: flex;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 50px;
            position: sticky;
            top: 20px;
            z-index: 999;
        }}

        .nav-pill {{
            background: var(--glass-surface);
            backdrop-filter: blur(30px) saturate(180%);
            -webkit-backdrop-filter: blur(30px) saturate(180%);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-pill);
            padding: 10px 30px;
            width: 95%;
            max-width: 900px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 15px 35px -10px var(--glass-shadow);
            transition: width 0.3s ease;
        }}

        /* ========================================================================
           COMPONENT: BUTTONS (HAPTIC STYLE)
           ======================================================================== */
        /* Overriding Streamlit's default buttons */
        .stButton > button {{
            background: {current['btn_grad']} !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 14px 28px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            
            /* Initial Shadow */
            box-shadow: 0 10px 20px -5px {current['accent']}55 !important;
            
            transition: all 0.4s var(--ease-elastic) !important;
            width: 100%;
            position: relative;
            overflow: hidden;
        }}

        /* Button Hover Physics */
        .stButton > button:hover {{
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 20px 35px -10px {current['accent']}88 !important;
            filter: brightness(1.1);
        }}

        /* Button Active/Click Physics */
        .stButton > button:active {{
            transform: scale(0.95);
            box-shadow: 0 5px 10px -5px {current['accent']}55 !important;
        }}

        /* ========================================================================
           COMPONENT: INPUT FIELDS (FORCED WHITE)
           ======================================================================== */
        /* Crucial Requirement: Inputs must always have white backgrounds 
           and black text for readability, regardless of the theme.
        */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            border-radius: var(--radius-sm) !important;
            padding: 12px 15px !important;
            font-family: var(--font-stack) !important;
            font-weight: 500 !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
            transition: border 0.3s ease, box-shadow 0.3s ease;
        }}

        /* Focus States */
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 4px {current['accent']}22 !important;
        }}

        /* Dropdown Menu Internals */
        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: var(--radius-sm) !important;
        }}
        div[data-testid="stSelectbox"] div[class*="st-"] {{
            color: #000000 !important;
        }}
        div[data-baseweb="popover"] {{
            background-color: #ffffff !important;
            border-radius: var(--radius-sm) !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15) !important;
        }}
        div[role="option"] {{
            color: #000000 !important;
            background-color: #ffffff !important;
            padding: 10px 15px !important;
        }}
        div[role="option"]:hover {{
            background-color: #f5f5f7 !important;
        }}

        /* ========================================================================
           TYPOGRAPHY & DECORATION
           ======================================================================== */
        h1, .hero-text {{
            font-family: var(--font-stack);
            font-weight: 800;
            letter-spacing: -0.03em;
            background: {current['btn_grad']};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}

        .section-header {{
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 0.85rem;
            font-weight: 800;
            color: var(--accent);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-header::after {{
            content: "";
            flex-grow: 1;
            height: 2px;
            background: linear-gradient(90deg, var(--accent), transparent);
            opacity: 0.4;
        }}

        /* ========================================================================
           ANIMATION KEYFRAMES
           ======================================================================== */
        
        /* 1. Slide Up Entrance */
        .animate-enter {{
            animation: slideUpFade 0.8s var(--ease-elastic) forwards;
            opacity: 0;
            transform: translateY(40px);
        }}
        
        @keyframes slideUpFade {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* 2. Floating Objects */
        .float-anim {{
            animation: float 6s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-12px); }}
            100% {{ transform: translateY(0px); }}
        }}

        /* ========================================================================
           LOADER: THE CYBER HEART
           ======================================================================== */
        .loader-backdrop {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(5, 5, 10, 0.85);
            backdrop-filter: blur(30px) saturate(0%);
            z-index: 999999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        .cyber-spinner-container {{
            position: relative;
            width: 140px; height: 140px;
        }}

        .spin-ring-1 {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            border-radius: 50%; border: 4px solid transparent;
            border-top-color: #0ea5e9; border-right-color: #a855f7;
            animation: spin 1.5s linear infinite;
            filter: drop-shadow(0 0 10px #0ea5e9);
        }}

        .spin-ring-2 {{
            position: absolute; top: 20%; left: 20%; width: 60%; height: 60%;
            border-radius: 50%; border: 4px solid transparent;
            border-bottom-color: #ec4899; border-left-color: #6366f1;
            animation: spin-rev 2.5s linear infinite;
            filter: drop-shadow(0 0 10px #ec4899);
        }}

        .heart-core-pulse {{
            position: absolute; top: 50%; left: 50%; width: 30px; height: 30px;
            background: #a855f7;
            transform: translate(-50%, -50%) rotate(45deg);
            animation: heart-beat 1s ease-in-out infinite;
            box-shadow: 0 0 30px #a855f7;
        }}
        
        .heart-core-pulse::before, .heart-core-pulse::after {{
            content: ""; position: absolute; width: 30px; height: 30px;
            background: #a855f7; border-radius: 50%;
        }}
        .heart-core-pulse::before {{ left: -15px; }}
        .heart-core-pulse::after {{ top: -15px; }}

        @keyframes spin {{ 0% {{transform: rotate(0deg);}} 100% {{transform: rotate(360deg);}} }}
        @keyframes spin-rev {{ 0% {{transform: rotate(360deg);}} 100% {{transform: rotate(-360deg);}} }}
        @keyframes heart-beat {{ 0% {{transform: translate(-50%,-50%) rotate(45deg) scale(0.8); opacity:0.8;}} 50% {{transform: translate(-50%,-50%) rotate(45deg) scale(1.2); opacity:1;}} 100% {{transform: translate(-50%,-50%) rotate(45deg) scale(0.8); opacity:0.8;}} }}

        .loader-text-glitch {{
            margin-top: 50px;
            font-family: 'Courier New', monospace;
            color: white;
            font-size: 1.2rem;
            letter-spacing: 0.3em;
            font-weight: 700;
            text-transform: uppercase;
            animation: pulse-text 2s infinite;
        }}
        @keyframes pulse-text {{ 0% {{opacity: 0.5;}} 50% {{opacity: 1;}} 100% {{opacity: 0.5;}} }}

        /* ========================================================================
           UTILITIES & OVERRIDES
           ======================================================================== */
        /* Scrollbar */
        ::-webkit-scrollbar {{ width: 10px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{
            background-color: var(--glass-border);
            border-radius: 20px;
            border: 2px solid transparent;
            background-clip: content-box;
        }}
        ::-webkit-scrollbar-thumb:hover {{ background-color: var(--accent); }}

        /* Hide Streamlit Footer */
        footer {{ visibility: hidden; }}
        #MainMenu {{ visibility: hidden; }}

    </style>
    """, unsafe_allow_html=True)

inject_css_engine()

# ==============================================================================
# 4.0 COMPONENT LIBRARY
# ==============================================================================

# 4.1 ASSET LIBRARY (SVG ICONS)
# ------------------------------------------------------------------------------
# Storing SVGs as code reduces file dependencies and allows dynamic coloring.
class AssetLibrary:
    @staticmethod
    def get_icon(name, size="2rem"):
        # Placeholder for future SVG expansion
        pass

# 4.2 NAVIGATION BAR
# ------------------------------------------------------------------------------
def render_navbar():
    """
    Renders the floating "Pill" navigation.
    """
    st.markdown('<div class="nav-pill-container"><div class="nav-pill">', unsafe_allow_html=True)
    
    # Grid Layout
    col_left, col_center, col_right = st.columns([1.5, 3, 1.5])
    
    # Left: Logo
    with col_left:
        if os.path.exists(LOGO_FILENAME):
            st.image(LOGO_FILENAME, width=120)
        else:
            st.markdown(f"<h3 style='margin:0; color:{current['accent']}'>MindCheck</h3>", unsafe_allow_html=True)
            
    # Center: Home Button
    with col_center:
        st.markdown("<div style='display:flex; justify-content:center; width:100%;'>", unsafe_allow_html=True)
        if st.button("🏠 HOME", key="nav_home_btn"):
            st.session_state.page = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Right: Theme Toggle
    with col_right:
        st.markdown("<div style='display:flex; justify-content:flex-end; width:100%; align-items:center;'>", unsafe_allow_html=True)
        def toggle_theme():
            if st.session_state.theme_toggle:
                st.session_state.theme_mode = "Dark"
            else:
                st.session_state.theme_mode = "Light"
        
        is_dark = (st.session_state.theme_mode == "Dark")
        st.toggle("Night Mode", value=is_dark, key="theme_toggle", on_change=toggle_theme)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown('</div></div>', unsafe_allow_html=True)

# 4.3 LOADING OVERLAY
# ------------------------------------------------------------------------------
def show_loader(duration=4):
    """
    Displays the blocking 'Synthesizing' overlay.
    """
    loader_html = """
    <div class="loader-backdrop">
        <div class="cyber-spinner-container">
            <div class="spin-ring-1"></div>
            <div class="spin-ring-2"></div>
            <div class="heart-core-pulse"></div>
        </div>
        <div class="loader-text-glitch">SYNTHESIZING...</div>
    </div>
    """
    placeholder = st.empty()
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    time.sleep(duration)
    placeholder.empty()

# 4.4 CONTENT MANAGER (STATIC TEXT)
# ------------------------------------------------------------------------------
class ContentManager:
    LEGAL_DISCLAIMER = """
    <div style='font-size:0.7rem; opacity:0.5; margin-top:20px; text-align:center;'>
    **LEGAL DISCLAIMER:**<br>
    MindCheck AI is a demonstration tool powered by artificial intelligence. 
    It is NOT a medical device and should NOT be used to diagnose, treat, or cure any mental health condition.
    The scores and insights generated are for educational and entertainment purposes only.
    If you or someone you know is in crisis, please contact your local emergency services or a mental health professional immediately.
    Data processed by this application is transient and not stored permanently on our servers.
    </div>
    """

# ==============================================================================
# 5.0 BUSINESS LOGIC (ROUTING ENGINE)
# ==============================================================================

# Always render the navigation pill at the top
render_navbar()

# 5.1 HOME PAGE
# ------------------------------------------------------------------------------
if st.session_state.page == "home":
    # Hero Section
    st.markdown(f"""
    <div class="animate-enter" style="text-align: center; padding: 80px 0 60px 0;">
        <h1 style="font-size: 5rem; margin-bottom: 20px; 
                   background: {current['btn_grad']}; 
                   -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;
                   filter: drop-shadow(0 10px 20px {current['accent']}44);">
            MindCheck AI
        </h1>
        <p style="font-size: 1.6rem; opacity: 0.8; font-weight: 300; max-width: 700px; margin: 0 auto; letter-spacing: 0.5px;">
            An AI that helps improve mental health through digital analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Cards
    c1, c2, c3 = st.columns(3, gap="medium")
    
    # Card 1: About
    with c1:
        st.markdown('<div class="glass-card animate-enter" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size: 4rem; margin-bottom: 20px;">👤</div>', unsafe_allow_html=True)
        st.markdown('<h3>Profile</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:30px;">Meet the developer.</p>', unsafe_allow_html=True)
        
        if st.button("About Me!", key="home_btn_about", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Card 2: Interview (Featured)
    with c2:
        # Featured Styling
        border_style = f"border: 2px solid {current['accent']}; box-shadow: 0 0 30px {current['accent']}33;"
        st.markdown(f'<div class="glass-card animate-enter" style="text-align:center; height:100%; {border_style}">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size: 4rem; margin-bottom: 20px;">🧠</div>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:{current["accent"]} !important;">MindCheck AI</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:30px;">Start your assessment.</p>', unsafe_allow_html=True)
        
        if st.button("START CHECK-IN", type="primary", key="home_btn_start", use_container_width=True):
            st.session_state.page = "interview"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Card 3: Updates
    with c3:
        st.markdown('<div class="glass-card animate-enter" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size: 4rem; margin-bottom: 20px;">📢</div>', unsafe_allow_html=True)
        st.markdown('<h3>News</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:30px;">Latest version info.</p>', unsafe_allow_html=True)
        
        if st.button("Latest Update", key="home_btn_update", use_container_width=True):
            st.session_state.page = "updates"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 5.2 ABOUT PAGE
# ------------------------------------------------------------------------------
elif st.session_state.page == "about":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 40px;">About Me</h1>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; max-width: 600px; margin: 0 auto; padding: 80px 40px;">
        <h2 style="font-weight: 300; font-size: 4rem; background: {current['btn_grad']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Hi.</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 5.3 UPDATES PAGE
# ------------------------------------------------------------------------------
elif st.session_state.page == "updates":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 40px;">Latest Updates</h1>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; max-width: 600px; margin: 0 auto; padding: 80px 40px;">
        <h2 style="font-weight: 300; font-size: 4rem; background: {current['btn_grad']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Hello</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 5.4 INTERVIEW PAGE (INPUT FORM)
# ------------------------------------------------------------------------------
elif st.session_state.page == "interview":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    
    st.markdown(f'<h1 style="text-align:center; margin-bottom: 10px;">📝 Mental Health Check-In</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; opacity:0.7; margin-bottom: 50px;">Complete the assessment below to unlock your insights.</p>', unsafe_allow_html=True)
    
    with st.form("interview_form"):
        left_col, right_col = st.columns(2, gap="large")
        
        # Left: Profile
        with left_col:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">👤 Profile Details</div>', unsafe_allow_html=True)
            
            age = st.number_input("How old are you?", 10, 100, 15)
            gender = st.selectbox("Gender Identity", ["Male", "Female"])
            academic_level = st.selectbox("Current School Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
            
            st.markdown('<br><div class="section-header">❤️ Health Metrics</div>', unsafe_allow_html=True)
            sleep = st.number_input("Average Sleep (Hours/Night)", 0.0, 24.0, 8.0, 0.5)
            rel_status = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced"])
            st.markdown('</div>', unsafe_allow_html=True)

        # Right: Digital Habits
        with right_col:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📱 Digital Footprint</div>', unsafe_allow_html=True)
            
            avg_daily_usage = st.number_input("Daily Screen Time (Hours)", 0.0, 24.0, 4.0, 0.5)
            platform = st.selectbox("Dominant Platform", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
            
            st.markdown("<br><label style='font-weight:600;'>Self-Perceived Addiction Level (1-10)</label>", unsafe_allow_html=True)
            addiction = st.slider("", 1, 10, 5)
            
            st.markdown('<br><div class="section-header">⚠️ Impact Assessment</div>', unsafe_allow_html=True)
            affects_perf = st.radio("Does usage affect your grades/work?", ["No", "Yes"], horizontal=True)
            conflicts = st.number_input("Weekly conflicts caused by social media?", 0, 10, 0)
            st.markdown('</div>', unsafe_allow_html=True)

        # Submit
        st.markdown("<br>", unsafe_allow_html=True)
        col_dummy1, col_btn, col_dummy2 = st.columns([1, 2, 1])
        with col_btn:
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
            
            # Prediction Logic
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
                    wellness_score = max(1.0, min(10.0, base))

                st.session_state.score = wellness_score
                st.session_state.page = "results"
                st.rerun()
            except Exception as e:
                st.error(f"Computation Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 5.5 RESULTS PAGE
# ------------------------------------------------------------------------------
elif st.session_state.page == "results":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    score = st.session_state.score
    data = st.session_state.inputs
    
    # Recap Bar
    st.markdown(f"""
    <div class="glass-card" style="padding: 1.2rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; border-left: 6px solid {current['accent']};">
        <div>
            <strong style="color:{current['accent']}; font-size: 0.85rem; letter-spacing: 1.5px; text-transform:uppercase;">ANALYSIS PARAMETERS:</strong>&nbsp;&nbsp;
            <span style="font-size: 0.95rem; font-family: 'SF Pro Display'; opacity:0.8;">
                <b>{data.get('Age')}y/o {data.get('Gender')}</b> • 
                <b>{data.get('Platform')}</b> ({data.get('Avg_Daily_Usage_Hours')}h/day) • 
                Sleep: <b>{data.get('Sleep')}h</b>
            </span>
        </div>
        <div style="font-size:1.5rem;">✅</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header
    col_head_1, col_head_2 = st.columns([4, 1.2])
    with col_head_1:
        st.markdown(f'<h1 style="text-align:left; font-size: 3rem; margin:0;">Mental Health Scorecard</h1>', unsafe_allow_html=True)
    with col_head_2:
        if st.button("🔄 Restart?", use_container_width=True):
            show_loader(duration=2)
            st.session_state.page = "interview"
            st.session_state.ai_results = {}
            st.session_state.score = None
            st.rerun()
    
    # Score Card
    if score < 4:
        score_color = current['danger']
        message = "Immediate Action Recommended"
    elif score < 7:
        score_color = current['warning']
        message = "Moderate Impact Detected"
    else:
        score_color = current['success']
        message = "Excellent Mental Balance"

    st.markdown(f"""
    <div class="glass-card" style="text-align: center; border: 2px solid {score_color}; position:relative; overflow:hidden;">
        <div style="position:absolute; top:0; left:0; width:100%; height:8px; background:{score_color}; opacity:0.8;"></div>
        <h3 style="margin-top:20px; opacity:0.6; letter-spacing:4px; font-size:1rem; font-weight:700;">MENTAL HEALTH INDEX</h3>
        <h1 style="font-size: 9rem; font-weight: 900; margin: 10px 0; color: {score_color} !important; text-shadow: 0 0 40px {score_color}44; line-height:1;">
            {score:.1f}<span style="font-size:2.5rem; opacity:0.5; color:{current['text_main']};">/10</span>
        </h1>
        <div style="background:{score_color}22; display:inline-block; padding:10px 25px; border-radius:100px; margin-bottom:20px;">
            <p style="margin:0; color:{score_color} !important; font-weight:700; letter-spacing:0.5px;">{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI Insights
    st.markdown(f'<h3 style="text-align:center; color:{current["accent"]}; margin-bottom:30px; margin-top:50px;">✨ Generative AI Insights</h3>', unsafe_allow_html=True)
    col_ai_1, col_ai_2, col_ai_3 = st.columns(3, gap="medium")
    
    with col_ai_1:
        st.markdown('<div class="glass-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size:2.5rem;">📊</div>', unsafe_allow_html=True)
        st.markdown('<h4>My Persona</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">Deep behavioral analysis.</p>', unsafe_allow_html=True)
        if st.button("Generate", key="btn_persona", use_container_width=True):
            show_loader(4)
            with st.spinner("Processing..."):
                prompt = f"Based on: {json.dumps(data)}. Return JSON: {{'persona': 'Fun Title', 'analysis': 'Short analysis', 'tips': ['Tip 1', 'Tip 2']}}"
                res = call_gemini_api(prompt)
                if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ai_2:
        st.markdown('<div class="glass-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size:2.5rem;">🕰️</div>', unsafe_allow_html=True)
        st.markdown('<h4>Future Self</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">A message from 2029.</p>', unsafe_allow_html=True)
        if st.button("Warp Time", key="btn_future", use_container_width=True):
            show_loader(4)
            with st.spinner("Connecting..."):
                prompt = f"Write a note from future 2029 self based on habits: {json.dumps(data)}. Max 50 words."
                res = call_gemini_api(prompt, expect_json=False)
                if res: st.session_state.ai_results['future'] = res; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ai_3:
        st.markdown('<div class="glass-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size:2.5rem;">🍃</div>', unsafe_allow_html=True)
        st.markdown('<h4>Detox Plan</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">3-Day cleansing protocol.</p>', unsafe_allow_html=True)
        if st.button("Build Plan", key="btn_detox", use_container_width=True):
            show_loader(4)
            with st.spinner("Planning..."):
                prompt = f"3-day detox for {data['Platform']} user. JSON: {{'days': [{{'day': 'Day 1', 'theme': 'Theme', 'tasks': ['Task 1']}}]}}"
                res = call_gemini_api(prompt)
                if res: st.session_state.ai_results['detox'] = json.loads(res); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Dynamic Results Rendering
    if st.session_state.get('ai_results'):
        st.markdown("<br><hr style='opacity:0.2; margin: 3rem 0;'><br>", unsafe_allow_html=True)
        results = st.session_state.ai_results
        
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="glass-card animate-enter" style="border-left: 5px solid {current['accent']};">
                <h3 style="color:{current['accent']} !important; margin:0;">📊 {r.get('persona', 'User')}</h3>
                <p style="font-style:italic; font-size:1.15rem; opacity:0.9; margin-top:15px;">"{r.get('analysis', '')}"</p>
                <div style="margin-top:25px; padding-top:20px; border-top:1px solid {current['glass_border']};">
                    <strong style="text-transform:uppercase; font-size:0.8rem; letter-spacing:1px; opacity:0.7;">Key Recommendations:</strong>
                    <ul style="margin-top:15px; list-style-type:none; padding:0;">
                        {"".join([f"<li style='margin-bottom:10px; padding-left:20px; position:relative;'><span style='position:absolute; left:0; color:{current['accent']};'>➤</span> {t}</li>" for t in r.get('tips', [])])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if 'future' in results:
            st.markdown(f"""
            <div class="glass-card animate-enter" style="border-left: 5px solid {current['warning']};">
                <h3 style="color:{current['warning']} !important; margin:0;">🕰️ Incoming Transmission (2029)</h3>
                <p style="font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.7; margin-top:15px;">
                    {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        if 'detox' in results:
            r = results['detox']
            days_html = ""
            for d in r.get('days', []):
                tasks = "".join([f"<li style='margin-bottom:5px; opacity:0.9;'>• {t}</li>" for t in d.get('tasks', [])])
                days_html += f"""
                <div style='background:rgba(255,255,255,0.03); padding:1.5rem; margin-bottom:15px; border-radius:20px; border:1px solid {current['glass_border']}'>
                    <strong style="color:{current['success']}; font-size:1.2rem; display:block; margin-bottom:10px;">{d.get('day')}: {d.get('theme')}</strong>
                    <ul style="list-style-type:none; padding-left:10px;">{tasks}</ul>
                </div>
                """
            st.markdown(f"""
            <div class="glass-card animate-enter" style="border-left: 5px solid {current['success']};">
                <h3 style="color:{current['success']} !important; margin:0;">🍃 Detox Challenge</h3>
                {days_html}
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# 6.0 FOOTER
# ------------------------------------------------------------------------------
st.markdown(ContentManager.LEGAL_DISCLAIMER, unsafe_allow_html=True)
st.markdown(f"""
<br><br>
<div style="text-align: center; margin-top: 2rem; opacity: 0.4; font-size: 0.8rem; font-family: 'SF Pro Display'; letter-spacing: 1px;">
    <p>MindCheck AI v5.0.1 • Powered by Gemini • 2026</p>
    <p style="font-size: 0.7rem;">Lumina Glass Engine Active</p>
</div>
<br>
""", unsafe_allow_html=True)

# ==============================================================================
# END OF SCRIPT
# ==============================================================================
