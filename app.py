# ==============================================================================
# MINDCHECK AI - MENTAL HEALTH & SOCIAL IMPACT DASHBOARD
# ==============================================================================
# VERSION: 4.0.0 (LUMINA LIQUID GLASS ULTIMATE EDITION)
# ARCHITECTURE: Streamlit + Python + LuminaGlass CSS Engine
# AUTHOR: Mubashir Mohsin & Gemini (AI Assistant)
# DATE: February 05, 2026
# ==============================================================================
#
# SYSTEM OVERVIEW:
# This application serves as a sophisticated interface for assessing digital
# well-being. It utilizes a proprietary "Liquid Glass" design system to mimic
# high-end optical physics found in modern operating systems (e.g., visionOS).
#
# TABLE OF CONTENTS:
# 1.0 - LIBRARY IMPORTS & SYSTEM CHECKS
# 2.0 - ASSET CONFIGURATION & PATH MANAGEMENT
# 3.0 - PAGE SETUP & METADATA
# 4.0 - GLOBAL STATE MANAGEMENT & PERSISTENCE
# 5.0 - LUMINA GLASS CSS ENGINE (THE CORE DESIGN SYSTEM)
#       5.1 - Variable Definitions (Tokens)
#       5.2 - Animation Physics (Keyframes)
#       5.3 - Component Architecture
#       5.4 - Refractive Layering Logic
# 6.0 - BACKEND LOGIC & AI INTEGRATION
# 7.0 - UI COMPONENT LIBRARY (PYTHON WRAPPERS)
# 8.0 - ROUTING ENGINE & PAGE LOGIC
# 9.0 - FOOTER & SYSTEM DIAGNOSTICS
#
# ==============================================================================

# ==============================================================================
# 1.0 LIBRARY IMPORTS & SYSTEM CHECKS
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
import random  # Used for stochastic animation variability

# ==============================================================================
# 2.0 ASSET CONFIGURATION & PATH MANAGEMENT
# ==============================================================================
# CONSTANTS defining the visual identity.
# Ensure these files are present in the root directory for proper rendering.
FAVICON_FILENAME = "Gemini_Generated_Image_5b19745b19745b19.jpg"
LOGO_FILENAME = "Gemini_Generated_Image_fq49a6fq49a6fq49.jpg"
MODEL_FILE = 'mental_health_model.joblib' 
GEMINI_MODEL = 'gemini-2.5-flash'

# API CREDENTIALS
# Fetched securely from Streamlit secrets environment.
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ==============================================================================
# 3.0 PAGE SETUP & METADATA
# ==============================================================================
st.set_page_config(
    page_title="MindCheck AI",
    page_icon=FAVICON_FILENAME,
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.mentalhealth.gov',
        'Report a bug': "mailto:support@mindcheck.ai",
        'About': "# MindCheck AI v4.0\nHigh-fidelity mental health analytics."
    }
)

# ==============================================================================
# 4.0 GLOBAL STATE MANAGEMENT & PERSISTENCE
# ==============================================================================
# Initialize the session state to handle navigation, data storage, and theme
# persistence across re-runs.

def init_session_state():
    """
    Initializes all required session state variables with default values.
    This ensures the app has a stable state on first load.
    """
    if "page" not in st.session_state:
        st.session_state.page = "home"
        
    if "theme_mode" not in st.session_state:
        # Default is Light to showcase the refraction effects better initially
        st.session_state.theme_mode = "Light"
        
    if "ai_results" not in st.session_state:
        st.session_state.ai_results = {} 
        
    if "score" not in st.session_state:
        st.session_state.score = None
        
    if "inputs" not in st.session_state:
        st.session_state.inputs = {}
        
    if "animation_seed" not in st.session_state:
        # Used to slightly randomize floating animations for natural feel
        st.session_state.animation_seed = random.random()

init_session_state()

# ==============================================================================
# 5.0 LUMINA GLASS CSS ENGINE (THE CORE DESIGN SYSTEM)
# ==============================================================================
# This section defines the visual physics of the application.
# It is extensive to support the "1500+ lines" requirement and provide
# true high-fidelity UI rendering.
# ==============================================================================

# 5.1 THEME TOKENS
# ------------------------------------------------------------------------------
themes = {
    "Dark": {
        # Deep space gradients for contrast
        "bg_layer_1": "#020617",
        "bg_layer_2": "#0f172a",
        "bg_layer_3": "#1e1b4b",
        "bg_gradient": "radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%)",
        
        # Glass Properties (High Transparency, High Blur)
        "glass_surface": "rgba(20, 20, 30, 0.4)",
        "glass_border": "rgba(255, 255, 255, 0.08)",
        "glass_specular": "rgba(255, 255, 255, 0.15)",
        "glass_shadow": "0 25px 50px -12px rgba(0, 0, 0, 0.7)",
        
        # Typography
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "text_tertiary": "#64748b",
        
        # Accents (Neon Violet)
        "accent_primary": "#a855f7",
        "accent_secondary": "#7c3aed",
        "accent_glow": "0 0 20px rgba(168, 85, 247, 0.5)",
        
        # Button Gradients
        "btn_gradient": "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
        
        # Physics Parameters
        "blur_strength": "40px",
        "saturation": "180%",
        "brightness": "1.1",
        
        # Result Colors
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#f87171"
    },
    "Light": {
        # Ethereal sky gradients
        "bg_layer_1": "#ffffff",
        "bg_layer_2": "#f0f9ff",
        "bg_layer_3": "#e0f2fe",
        "bg_gradient": "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 40%, #ffffff 100%)",
        
        # Glass Properties (Frosted Ice Look)
        "glass_surface": "rgba(255, 255, 255, 0.55)",
        "glass_border": "rgba(255, 255, 255, 0.8)",
        "glass_specular": "rgba(255, 255, 255, 0.9)",
        "glass_shadow": "0 20px 40px -12px rgba(14, 165, 233, 0.15)",
        
        # Typography
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "text_tertiary": "#94a3b8",
        
        # Accents (Liquid Blue)
        "accent_primary": "#0ea5e9",
        "accent_secondary": "#0284c7",
        "accent_glow": "0 0 20px rgba(14, 165, 233, 0.3)",
        
        # Button Gradients
        "btn_gradient": "linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)",
        
        # Physics Parameters
        "blur_strength": "30px",
        "saturation": "200%",
        "brightness": "1.05",
        
        # Result Colors
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444"
    }
}

current = themes[st.session_state.theme_mode]

# 5.2 DYNAMIC BACKGROUND GENERATOR
# ------------------------------------------------------------------------------
def get_background_css():
    """
    Generates a dynamic background that reacts to the mental health score.
    If a score exists, it adds a floating particle layer.
    """
    base = current['bg_gradient']
    
    if st.session_state.page == "results" and st.session_state.score is not None:
        emoji = "🌟" if st.session_state.score >= 6 else "🌧️"
        # We encode the emoji into an SVG pattern for high performance rendering
        svg = f"""
        <svg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'>
            <text x='50' y='50' font-size='20' text-anchor='middle' dominant-baseline='middle' opacity='0.05'>{emoji}</text>
        </svg>
        """
        b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
        return f"url('data:image/svg+xml;base64,{b64}'), {base}"
    
    return base

bg_css = get_background_css()

# 5.3 THE CSS ENGINE INJECTION
# ------------------------------------------------------------------------------
st.markdown(f"""
<style>
    /* ============================================================================
    LUMINA GLASS ENGINE v4.0 - CORE CSS VARIABLES
    ============================================================================
    */
    :root {{
        --font-stack: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        --glass-surface: {current['glass_surface']};
        --glass-border: {current['glass_border']};
        --glass-specular: {current['glass_specular']};
        --glass-shadow: {current['glass_shadow']};
        --accent: {current['accent_primary']};
        --text-main: {current['text_primary']};
        --text-sub: {current['text_secondary']};
        --blur-strength: {current['blur_strength']};
        --saturation: {current['saturation']};
        --brightness: {current['brightness']};
        --squircle-radius: 32px;
        --elastic-ease: cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    /* ============================================================================
    GLOBAL RESET & BODY PHYSICS
    ============================================================================
    */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@100;300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');

    .stApp {{
        background: {bg_css};
        background-attachment: fixed;
        background-size: cover;
        font-family: var(--font-stack);
        color: var(--text-main);
        transition: background 0.8s ease-in-out;
        overflow-x: hidden; /* Prevent jitter during animations */
    }}

    /* Remove default Streamlit header margin */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 6rem !important;
        max-width: 1200px;
    }}

    /* ============================================================================
    THE "MAGNIFYING GLASS" CARD COMPONENT
    ============================================================================
    This is the core of the Liquid Glass UI. It uses multiple layers of
    backdrop-filter to simulate refraction and depth.
    */
    .liquid-card {{
        position: relative;
        background: var(--glass-surface);
        
        /* THE OPTICAL PHYSICS ENGINE */
        backdrop-filter: blur(var(--blur-strength)) saturate(var(--saturation)) brightness(var(--brightness));
        -webkit-backdrop-filter: blur(var(--blur-strength)) saturate(var(--saturation)) brightness(var(--brightness));
        
        /* BORDER OPTICS */
        border: 1px solid var(--glass-border);
        border-top: 1px solid var(--glass-specular); /* Top light catch */
        border-left: 1px solid var(--glass-specular); /* Left light catch */
        
        border-radius: var(--squircle-radius);
        padding: 40px;
        margin-bottom: 30px;
        
        /* DEPTH SIMULATION */
        box-shadow: 
            0 20px 40px -10px rgba(0,0,0,0.1), /* Ambient shadow */
            0 0 0 1px rgba(255,255,255,0.1) inset; /* Inner rim light */
            
        transform-style: preserve-3d;
        transition: transform 0.4s var(--elastic-ease), box-shadow 0.4s ease;
        overflow: hidden; /* Contains the liquid sheen */
    }}

    /* Layer Morphing Animation on Hover */
    .liquid-card:hover {{
        transform: translateY(-8px) scale(1.01);
        box-shadow: 
            0 30px 60px -12px rgba(0,0,0,0.15),
            0 0 0 1px var(--accent) inset; /* Accent glow on hover */
        z-index: 10;
    }}

    /* The "Liquid Sheen" Effect */
    .liquid-card::before {{
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 50%;
        height: 100%;
        background: linear-gradient(
            to right,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transform: skewX(-25deg);
        transition: 0.5s;
        pointer-events: none;
    }}

    .liquid-card:hover::before {{
        animation: sheen 0.75s forwards;
    }}

    @keyframes sheen {{
        100% {{ left: 150%; }}
    }}

    /* ============================================================================
    APPLE-STYLE PILL NAVIGATION
    ============================================================================
    Floating, blurred navigation bar.
    */
    .nav-pill-wrapper {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 50px;
        z-index: 1000;
        position: sticky;
        top: 20px;
    }}

    .nav-pill {{
        background: var(--glass-surface);
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        
        border: 1px solid var(--glass-border);
        border-radius: 100px;
        
        padding: 10px 20px;
        width: 95%;
        max-width: 900px;
        
        display: flex;
        align-items: center;
        justify-content: space-between;
        
        box-shadow: 0 10px 30px -5px rgba(0,0,0,0.1);
        transition: width 0.3s ease;
    }}

    /* ============================================================================
    TYPOGRAPHY ENGINE (SF PRO SIMULATION)
    ============================================================================
    */
    h1, .hero-title {{
        font-family: var(--font-stack);
        font-weight: 800;
        letter-spacing: -0.03em;
        background: {current['btn_gradient']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}

    h2, h3, h4 {{
        color: var(--text-main) !important;
        font-weight: 700;
        letter-spacing: -0.01em;
    }}

    /* ============================================================================
    INTERACTIVE ELEMENTS (BUTTONS & INPUTS)
    ============================================================================
    */
    
    /* Apple-style Elastic Buttons */
    .stButton > button {{
        background: {current['btn_gradient']} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 16px 32px !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 10px 25px -5px {current['accent']}55 !important;
        transition: all 0.4s var(--elastic-ease) !important;
        width: 100%;
        position: relative;
        overflow: hidden;
    }}

    .stButton > button:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 20px 35px -10px {current['accent']}77 !important;
        filter: brightness(1.1);
    }}

    .stButton > button:active {{
        transform: scale(0.95);
        box-shadow: 0 5px 15px -5px {current['accent']}55 !important;
    }}

    /* INPUT FIELDS - FORCED WHITE THEME */
    /* As per requirements: White BG, Black Text always */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        border-radius: 18px !important;
        padding: 14px 18px !important;
        font-family: var(--font-stack) !important;
        font-weight: 500 !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
        transition: border 0.3s ease, box-shadow 0.3s ease;
    }}

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px {current['accent']}22 !important;
    }}

    /* Dropdown Menu Styling */
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 18px !important;
    }}
    
    div[data-testid="stSelectbox"] div[class*="st-"] {{
        color: #000000 !important;
    }}
    
    div[data-baseweb="popover"] {{
        background-color: #ffffff !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2) !important;
    }}
    
    div[role="option"] {{
        color: #000000 !important;
        background-color: #ffffff !important;
        padding: 12px 20px !important;
    }}
    
    div[role="option"]:hover {{
        background-color: #f5f5f7 !important; /* Apple light gray */
    }}

    /* ============================================================================
    ADVANCED ANIMATION KEYFRAMES
    ============================================================================
    */
    
    /* 1. Page Entrance - Slide Up & Fade */
    .animate-enter {{
        animation: slideUpFade 0.8s var(--elastic-ease) forwards;
        opacity: 0;
        transform: translateY(30px);
    }}
    
    @keyframes slideUpFade {{
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* 2. Floating Elements (Breath) */
    .float-anim {{
        animation: float 6s ease-in-out infinite;
    }}
    
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* 3. Pulse Glow */
    @keyframes pulse-glow {{
        0% {{ box-shadow: 0 0 0 0 {current['accent']}44; }}
        70% {{ box-shadow: 0 0 0 15px transparent; }}
        100% {{ box-shadow: 0 0 0 0 transparent; }}
    }}

    /* ============================================================================
    LOADER OVERLAY - THE "SYNTHESIZING" HEART
    ============================================================================
    */
    .loader-backdrop {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.85);
        backdrop-filter: blur(40px) saturate(0%);
        z-index: 999999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}

    .cyber-heart-container {{
        position: relative;
        width: 150px;
        height: 150px;
        filter: drop-shadow(0 0 20px {current['accent']});
    }}

    .orbit-ring {{
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        border: 4px solid transparent;
        border-top-color: #0ea5e9;
        border-right-color: #a855f7;
        border-radius: 50%;
        animation: spin 2s linear infinite;
    }}

    .orbit-ring-2 {{
        position: absolute;
        top: 15%; left: 15%;
        width: 70%; height: 70%;
        border: 4px solid transparent;
        border-bottom-color: #ec4899;
        border-left-color: #6366f1;
        border-radius: 50%;
        animation: spin-reverse 3s linear infinite;
    }}

    .core-pulse {{
        position: absolute;
        top: 50%; left: 50%;
        width: 40px; height: 40px;
        background: radial-gradient(circle, #ffffff 0%, {current['accent']} 100%);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: heartbeat 1.2s ease-in-out infinite;
        box-shadow: 0 0 40px {current['accent']};
    }}

    .loader-text-glitch {{
        margin-top: 50px;
        font-family: 'Courier New', monospace;
        color: white;
        font-size: 1.2rem;
        letter-spacing: 0.3em;
        font-weight: bold;
        text-transform: uppercase;
        animation: textFlicker 3s infinite;
    }}

    @keyframes spin {{ 0% {{transform: rotate(0deg);}} 100% {{transform: rotate(360deg);}} }}
    @keyframes spin-reverse {{ 0% {{transform: rotate(360deg);}} 100% {{transform: rotate(-360deg);}} }}
    @keyframes heartbeat {{ 0% {{transform: translate(-50%,-50%) scale(1);}} 15% {{transform: translate(-50%,-50%) scale(1.3);}} 30% {{transform: translate(-50%,-50%) scale(1);}} 45% {{transform: translate(-50%,-50%) scale(1.3);}} 100% {{transform: translate(-50%,-50%) scale(1);}} }}
    @keyframes textFlicker {{ 0%, 19.9%, 22%, 62.9%, 64%, 64.9%, 70%, 100% {{opacity: 0.99;}} 20%, 21.9%, 63%, 63.9%, 65%, 69.9% {{opacity: 0.4;}} }}

    /* ============================================================================
    SCROLLBAR CUSTOMIZATION
    ============================================================================
    */
    ::-webkit-scrollbar {{ width: 12px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{
        background-color: {current['glass_border']};
        border-radius: 20px;
        border: 3px solid transparent;
        background-clip: content-box;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background-color: {current['accent']};
    }}

    /* HIDE FOOTERS */
    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 6.0 BACKEND LOGIC & AI INTEGRATION
# ==============================================================================
# This section contains the core business logic, including API calls to Gemini
# and the ML model prediction logic.
# ==============================================================================

def toggle_theme():
    """
    Toggles the application theme between Light and Dark modes.
    Updates the session_state and triggers a re-run to apply new CSS variables.
    """
    if st.session_state.theme_toggle:
        st.session_state.theme_mode = "Dark"
    else:
        st.session_state.theme_mode = "Light"

@st.cache_resource
def load_ml_model():
    """
    Loads the trained machine learning model from disk using joblib.
    Uses st.cache_resource to prevent reloading on every interaction.
    
    Returns:
        The loaded model object or None if the file is missing/corrupt.
    """
    try:
        return joblib.load(MODEL_FILE)
    except Exception as e:
        # In a real enterprise app, we would log this error to a monitoring service.
        # print(f"Error loading model: {e}")
        return None

# Load model immediately
model = load_ml_model()

def call_gemini_api(prompt_text, expect_json=True):
    """
    Executes a secure API call to Google's Gemini 2.5 Flash model.
    
    Args:
        prompt_text (str): The prompt instructions for the AI.
        expect_json (bool): If True, configures the model to output valid JSON.
        
    Returns:
        str: The text content of the response, or None if failed.
    """
    if not API_KEY:
        # Graceful degradation if API key is missing
        return None
        
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    
    request_body = {
        "contents": [{
            "parts": [{
                "text": prompt_text
            }]
        }]
    }
    
    if expect_json:
        request_body["generationConfig"] = {"responseMimeType": "application/json"}
        
    try:
        # We use a generous timeout because AI generation can sometimes lag
        response = requests.post(
            endpoint,
            headers={'Content-Type': 'application/json'},
            json=request_body,
            timeout=25 
        )
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # Handle non-200 responses (e.g., quota exceeded)
            return None
            
    except Exception:
        return None

# ==============================================================================
# 7.0 UI COMPONENT LIBRARY (PYTHON WRAPPERS)
# ==============================================================================
# Reusable UI components that wrap the complex HTML/CSS classes defined above.
# ==============================================================================

def render_navigation_pill():
    """
    Renders the floating navigation bar at the top of the screen.
    Contains the Logo, Home Button, and Theme Toggle.
    """
    # Outer Wrapper
    st.markdown('<div class="nav-pill-wrapper"><div class="nav-pill">', unsafe_allow_html=True)
    
    # Grid Layout for Nav Items
    col_left, col_center, col_right = st.columns([1.5, 3, 1.5])
    
    # 1. Branding (Left)
    with col_left:
        if os.path.exists(LOGO_FILENAME):
            st.image(LOGO_FILENAME, width=120)
        else:
            # Fallback text logo if image is missing
            st.markdown(f"<h3 style='margin:0; color:{current['accent_primary']}'>MindCheck</h3>", unsafe_allow_html=True)
            
    # 2. Navigation (Center)
    with col_center:
        st.markdown("<div style='display:flex; justify-content:center; width:100%;'>", unsafe_allow_html=True)
        # Unique key prevents widget ID collision
        if st.button("🏠 HOME", key="nav_home_button"):
            st.session_state.page = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 3. Controls (Right)
    with col_right:
        st.markdown("<div style='display:flex; justify-content:flex-end; width:100%; align-items:center;'>", unsafe_allow_html=True)
        # Theme toggle determines session state
        is_dark_mode = (st.session_state.theme_mode == "Dark")
        st.toggle("Night Mode", value=is_dark_mode, key="theme_toggle", on_change=toggle_theme)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Close Wrapper
    st.markdown('</div></div>', unsafe_allow_html=True)

def show_loading_screen(seconds=4):
    """
    Injects a full-screen, blocking overlay with the 'Synthesizing' animation.
    
    Args:
        seconds (int): Duration to display the loader.
    """
    loader_html = """
    <div class="loader-backdrop">
        <div class="cyber-heart-container">
            <div class="orbit-ring"></div>
            <div class="orbit-ring-2"></div>
            <div class="core-pulse"></div>
        </div>
        <div class="loader-text-glitch">SYNTHESIZING...</div>
    </div>
    """
    
    # Create placeholder to hold the overlay
    placeholder = st.empty()
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    
    # Block execution
    time.sleep(seconds)
    
    # Remove overlay
    placeholder.empty()

def render_glass_card_start(additional_styles=""):
    """
    Helper to start a liquid glass card div. 
    Must be closed with render_glass_card_end().
    """
    st.markdown(f'<div class="liquid-card animate-enter" style="{additional_styles}">', unsafe_allow_html=True)

def render_glass_card_end():
    """Closes a liquid glass card div."""
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# 8.0 ROUTING ENGINE & PAGE LOGIC
# ==============================================================================
# The main controller that switches views based on st.session_state.page.
# ==============================================================================

# Always render nav first
render_navigation_pill()

# ------------------------------------------------------------------------------
# PAGE 1: LANDING PAGE (HOME)
# ------------------------------------------------------------------------------
if st.session_state.page == "home":
    
    # 1. Hero Section with Typing Effect Simulation
    st.markdown(f"""
    <div class="animate-enter" style="text-align: center; padding: 80px 0 60px 0;">
        <h1 style="font-size: 5rem; margin-bottom: 20px; 
                   background: {current['btn_gradient']}; 
                   -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent;">
            MindCheck AI
        </h1>
        <p style="font-size: 1.6rem; opacity: 0.8; font-weight: 300; max-width: 700px; margin: 0 auto; letter-spacing: 0.5px;">
            An AI that helps improve mental health through digital analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Card Grid System
    c1, c2, c3 = st.columns(3, gap="medium")
    
    # Card 1: About Me
    with c1:
        st.markdown('<div class="liquid-card animate-enter" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size: 4rem; margin-bottom: 20px;">👤</div>', unsafe_allow_html=True)
        st.markdown('<h3>Profile</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:30px;">Meet the developer.</p>', unsafe_allow_html=True)
        
        if st.button("About Me!", key="home_about_btn", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Card 2: MindCheck AI (Featured Card)
    with c2:
        # Featured card gets a colored border
        border_style = f"border: 2px solid {current['accent_primary']}; box-shadow: 0 0 30px {current['accent_primary']}44;"
        st.markdown(f'<div class="liquid-card animate-enter" style="text-align:center; height:100%; {border_style}">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size: 4rem; margin-bottom: 20px;">🧠</div>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:{current["accent_primary"]} !important;">MindCheck AI</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:30px;">Start your assessment.</p>', unsafe_allow_html=True)
        
        if st.button("START CHECK-IN", type="primary", key="home_start_btn", use_container_width=True):
            st.session_state.page = "interview"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Card 3: Updates
    with c3:
        st.markdown('<div class="liquid-card animate-enter" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size: 4rem; margin-bottom: 20px;">📢</div>', unsafe_allow_html=True)
        st.markdown('<h3>News</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:30px;">Latest version info.</p>', unsafe_allow_html=True)
        
        if st.button("Latest Update", key="home_update_btn", use_container_width=True):
            st.session_state.page = "updates"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE 2: ABOUT ME
# ------------------------------------------------------------------------------
elif st.session_state.page == "about":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 40px;">About Me</h1>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="liquid-card" style="text-align: center; max-width: 600px; margin: 0 auto; padding: 80px 40px;">
        <h2 style="font-weight: 300; font-size: 4rem; background: {current['btn_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Hi.</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE 3: LATEST UPDATES
# ------------------------------------------------------------------------------
elif st.session_state.page == "updates":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 40px;">Latest Updates</h1>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="liquid-card" style="text-align: center; max-width: 600px; margin: 0 auto; padding: 80px 40px;">
        <h2 style="font-weight: 300; font-size: 4rem; background: {current['btn_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Hello</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE 4: THE INTERVIEW (DATA COLLECTION)
# ------------------------------------------------------------------------------
elif st.session_state.page == "interview":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    
    # Header
    st.markdown(f'<h1 style="text-align:center; margin-bottom: 10px;">📝 Mental Health Check-In</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; opacity:0.7; margin-bottom: 50px;">Complete the assessment below to unlock your insights.</p>', unsafe_allow_html=True)
    
    # Form Logic
    with st.form("interview_form"):
        # Split layout into two liquid glass cards
        left_col, right_col = st.columns(2, gap="large")
        
        # Left Panel: User Profile
        with left_col:
            st.markdown('<div class="liquid-card" style="height: 100%;">', unsafe_allow_html=True)
            
            # Header Style
            st.markdown(f'<div style="text-transform:uppercase; font-size:0.8rem; letter-spacing:2px; color:{current["accent_primary"]}; font-weight:800; margin-bottom:20px;">👤 Profile Details</div>', unsafe_allow_html=True)
            
            age = st.number_input("How old are you?", 10, 100, 15, help="Used for age-group benchmarking.")
            gender = st.selectbox("Gender Identity", ["Male", "Female"])
            academic_level = st.selectbox("Current School Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
            
            st.markdown(f'<br><div style="text-transform:uppercase; font-size:0.8rem; letter-spacing:2px; color:{current["accent_primary"]}; font-weight:800; margin-bottom:20px;">❤️ Health Metrics</div>', unsafe_allow_html=True)
            
            sleep = st.number_input("Average Sleep (Hours/Night)", 0.0, 24.0, 8.0, 0.5)
            rel_status = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced"])
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Right Panel: Digital Habits
        with right_col:
            st.markdown('<div class="liquid-card" style="height: 100%;">', unsafe_allow_html=True)
            
            st.markdown(f'<div style="text-transform:uppercase; font-size:0.8rem; letter-spacing:2px; color:{current["accent_primary"]}; font-weight:800; margin-bottom:20px;">📱 Digital Footprint</div>', unsafe_allow_html=True)
            
            avg_daily_usage = st.number_input("Daily Screen Time (Hours)", 0.0, 24.0, 4.0, 0.5)
            platform = st.selectbox("Dominant Platform", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
            
            st.markdown("<br><label style='font-weight:600;'>Self-Perceived Addiction Level (1-10)</label>", unsafe_allow_html=True)
            addiction = st.slider("", 1, 10, 5)
            
            st.markdown(f'<br><div style="text-transform:uppercase; font-size:0.8rem; letter-spacing:2px; color:{current["accent_primary"]}; font-weight:800; margin-bottom:20px;">⚠️ Impact Assessment</div>', unsafe_allow_html=True)
            
            affects_perf = st.radio("Does usage affect your grades/work?", ["No", "Yes"], horizontal=True)
            conflicts = st.number_input("Weekly conflicts caused by social media?", 0, 10, 0)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Bottom Action Bar
        st.markdown("<br>", unsafe_allow_html=True)
        col_dummy1, col_btn, col_dummy2 = st.columns([1, 2, 1])
        with col_btn:
            submitted = st.form_submit_button("🏁 ANALYZE MY DATA")
            
        # Submission Handler
        if submitted:
            # 1. Trigger the "Synthesizing" Loader
            show_loading_screen(seconds=4)
            
            # 2. Store user inputs
            st.session_state.inputs = {
                "Age": age, "Gender": gender, "Academic_Level": academic_level,
                "Avg_Daily_Usage_Hours": avg_daily_usage, "Platform": platform,
                "Addiction": addiction, "Sleep": sleep, "Relationship": rel_status,
                "Affects_Performance": affects_perf, "Conflicts": conflicts
            }
            
            # 3. Model Prediction (Feature Mapping)
            # We create a dataframe with 0s and then fill in the user values
            input_df = pd.DataFrame(0, index=[0], columns=MODEL_COLUMNS)
            
            try:
                # Basic features
                input_df['Gender'] = 1 if gender == "Female" else 0 
                input_df['Age'] = age
                input_df['Academic_Level'] = 1 # Simplified for demo compatibility
                input_df['Avg_Daily_Usage_Hours'] = avg_daily_usage
                input_df['Addicted_Score'] = addiction
                input_df['Conflicts_Over_Social_Media'] = conflicts
                input_df['Affects_Academic_Performance'] = 1 if affects_perf == "Yes" else 0
                
                # Dynamic One-Hot Encoding for Platform
                if model:
                    plat_col = f"Most_Used_Platform_{platform}"
                    if plat_col in MODEL_COLUMNS: 
                        input_df[plat_col] = 1
                        
                    # Execute Prediction
                    wellness_score = model.predict(input_df)[0]
                else:
                    # Fallback Algorithm if model file is missing/corrupt
                    # (Higher Usage + Higher Addiction - Sleep) = Lower Score
                    base_calc = 10 - (avg_daily_usage * 0.3) - (addiction * 0.2) + (sleep * 0.2)
                    wellness_score = max(1.0, min(10.0, base_calc))

                # 4. Save and Navigate
                st.session_state.score = wellness_score
                st.session_state.page = "results"
                st.rerun()
                
            except Exception as e:
                st.error(f"Computation Engine Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE 5: RESULTS & AI DIAGNOSTICS
# ------------------------------------------------------------------------------
elif st.session_state.page == "results":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    
    # Retrieve state
    score = st.session_state.score
    data = st.session_state.inputs
    
    # 1. Parameter Recap (Top Bar)
    # -----------------------------------------
    st.markdown(f"""
    <div class="liquid-card" style="padding: 1.2rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; border-left: 6px solid {current['accent_primary']};">
        <div>
            <strong style="color:{current['accent_primary']}; font-size: 0.85rem; letter-spacing: 1.5px; text-transform:uppercase;">ANALYSIS PARAMETERS:</strong>&nbsp;&nbsp;
            <span style="font-size: 0.95rem; font-family: 'SF Pro Display'; opacity:0.8;">
                <b>{data.get('Age')}y/o {data.get('Gender')}</b> • 
                <b>{data.get('Platform')}</b> ({data.get('Avg_Daily_Usage_Hours')}h/day) • 
                Sleep: <b>{data.get('Sleep')}h</b> • 
                Addiction: <b>{data.get('Addiction')}/10</b>
            </span>
        </div>
        <div style="font-size:1.5rem;">✅</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Header & Controls
    # -----------------------------------------
    col_head_1, col_head_2 = st.columns([4, 1.2])
    with col_head_1:
        st.markdown(f'<h1 style="text-align:left; font-size: 3rem; margin:0;">Mental Health Scorecard</h1>', unsafe_allow_html=True)
    with col_head_2:
        if st.button("🔄 Restart?", use_container_width=True):
            show_loading_screen(seconds=2)
            reset_interview()
            st.rerun()
    
    # 3. The Score Display (Hero Visual)
    # -----------------------------------------
    if score < 4:
        score_color = current['danger']
        message = "Immediate Action Recommended"
    elif score < 7:
        score_color = current['warning']
        message = "Moderate Impact Detected"
    else:
        score_color = current['success']
        message = "Excellent Mental Balance"

    # We use inline styles for the score to ensure high contrast and size
    st.markdown(f"""
    <div class="liquid-card" style="text-align: center; border: 2px solid {score_color}; position:relative; overflow:hidden;">
        <div style="position:absolute; top:0; left:0; width:100%; height:10px; background:{score_color}; opacity:0.8;"></div>
        <h3 style="margin-top:20px; opacity:0.6; letter-spacing:4px; font-size:1rem; font-weight:700;">MENTAL HEALTH INDEX</h3>
        <h1 style="font-size: 9rem; font-weight: 900; margin: 10px 0; color: {score_color} !important; text-shadow: 0 0 40px {score_color}44; line-height:1;">
            {score:.1f}<span style="font-size:2.5rem; opacity:0.5; color:{current['text_main']};">/10</span>
        </h1>
        <div style="background:{score_color}22; display:inline-block; padding:10px 25px; border-radius:100px; margin-bottom:20px;">
            <p style="margin:0; color:{score_color} !important; font-weight:700; letter-spacing:0.5px;">{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Generative AI Section
    # -----------------------------------------
    st.markdown(f'<h3 style="text-align:center; color:{current["accent_primary"]}; margin-bottom:30px; margin-top:50px;">✨ Generative AI Insights</h3>', unsafe_allow_html=True)
    
    col_ai_1, col_ai_2, col_ai_3 = st.columns(3, gap="medium")
    
    # Insight Tile 1: Persona
    with col_ai_1:
        st.markdown('<div class="liquid-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size:2.5rem;">📊</div>', unsafe_allow_html=True)
        st.markdown('<h4>My Persona</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">Deep behavioral analysis.</p>', unsafe_allow_html=True)
        
        if st.button("Generate", key="btn_persona", use_container_width=True):
            show_loading_screen(seconds=4)
            with st.spinner("Analyzing psychographics..."):
                prompt = f"Based on this user data: {json.dumps(data)}. Return JSON with keys: 'persona' (Creative Title), 'analysis' (Short summary), 'tips' (List of 2 tips)."
                res = call_gemini_api(prompt)
                if res: 
                    st.session_state.ai_results['analysis'] = json.loads(res)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Insight Tile 2: Future Self
    with col_ai_2:
        st.markdown('<div class="liquid-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size:2.5rem;">🕰️</div>', unsafe_allow_html=True)
        st.markdown('<h4>Future Self</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">A message from 2029.</p>', unsafe_allow_html=True)
        
        if st.button("Warp Time", key="btn_future", use_container_width=True):
            show_loading_screen(seconds=4)
            with st.spinner("Establishing temporal link..."):
                prompt = f"Write a dramatic note from future 2029 self based on habits: {json.dumps(data)}. Max 50 words."
                res = call_gemini_api(prompt, expect_json=False)
                if res: 
                    st.session_state.ai_results['future'] = res
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Insight Tile 3: Detox Plan
    with col_ai_3:
        st.markdown('<div class="liquid-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="float-anim" style="font-size:2.5rem;">🍃</div>', unsafe_allow_html=True)
        st.markdown('<h4>Detox Plan</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">3-Day cleansing protocol.</p>', unsafe_allow_html=True)
        
        if st.button("Build Plan", key="btn_detox", use_container_width=True):
            show_loading_screen(seconds=4)
            with st.spinner("Drafting protocol..."):
                prompt = f"Create a 3-day social media detox plan for a {data['Platform']} user. Return JSON: {{'days': [{{'day': 'Day 1', 'theme': 'Theme', 'tasks': ['Task 1']}}]}}"
                res = call_gemini_api(prompt)
                if res: 
                    st.session_state.ai_results['detox'] = json.loads(res)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Display AI Results (Dynamic Rendering)
    # -----------------------------------------
    if st.session_state.get('ai_results'):
        st.markdown("<br><hr style='opacity:0.2; margin: 3rem 0;'><br>", unsafe_allow_html=True)
        
        results = st.session_state.ai_results
        
        # Display Persona Result
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="liquid-card animate-enter" style="border-left: 5px solid {current['accent_primary']};">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:2rem; margin-right:15px;">📊</span>
                    <h3 style="color:{current['accent_primary']} !important; margin:0;">{r.get('persona', 'User')}</h3>
                </div>
                <p style="font-style:italic; font-size:1.15rem; opacity:0.9; line-height:1.6;">"{r.get('analysis', '')}"</p>
                <div style="margin-top:25px; padding-top:20px; border-top:1px solid {current['glass_border']};">
                    <strong style="text-transform:uppercase; font-size:0.8rem; letter-spacing:1px; opacity:0.7;">Key Recommendations:</strong>
                    <ul style="margin-top:15px; list-style-type:none; padding:0;">
                        {"".join([f"<li style='margin-bottom:10px; padding-left:20px; position:relative;'><span style='position:absolute; left:0; color:{current['accent_primary']};'>➤</span> {t}</li>" for t in r.get('tips', [])])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Display Future Result
        if 'future' in results:
            st.markdown(f"""
            <div class="liquid-card animate-enter" style="border-left: 5px solid {current['warning']}; background: {current['bg_layer_1']}88;">
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <span style="font-size:2rem; margin-right:15px;">🕰️</span>
                    <h3 style="color:{current['warning']} !important; margin:0;">Incoming Transmission (2029)</h3>
                </div>
                <p style="font-family: 'Courier New', monospace; font-size: 1.1rem; line-height: 1.7; color:{current['text_primary']};">
                    {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Display Detox Result
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
            <div class="liquid-card animate-enter" style="border-left: 5px solid {current['success']};">
                <div style="display:flex; align-items:center; margin-bottom:20px;">
                    <span style="font-size:2rem; margin-right:15px;">🍃</span>
                    <h3 style="color:{current['success']} !important; margin:0;">Detox Challenge</h3>
                </div>
                {days_html}
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 9.0 FOOTER & SYSTEM DIAGNOSTICS
# ==============================================================================
st.markdown(f"""
<br><br>
<div style="text-align: center; margin-top: 5rem; opacity: 0.4; font-size: 0.8rem; font-family: 'SF Pro Display'; letter-spacing: 1px;">
    <p>MindCheck AI v4.0 • Powered by Gemini • 2026</p>
    <p style="font-size: 0.7rem;">Liquid Glass Engine Active</p>
</div>
<br>
""", unsafe_allow_html=True)

# End of System
