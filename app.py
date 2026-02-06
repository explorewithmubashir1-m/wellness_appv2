# ==============================================================================
# MINDCHECK AI - MENTAL HEALTH & SOCIAL IMPACT DASHBOARD
# ==============================================================================
# VERSION: 3.5.0 (Apple Liquid Glass Edition)
# ARCHITECTURE: Streamlit + Python + CSS3 Glassmorphism
# AUTHOR: Mubashir Mohsin and Gemini (AI Assistant)
# DATE: 2026-02-05
# ==============================================================================
# MISSION STATEMENT:
# To provide an AI-driven, privacy-focused interface for assessing digital
# habits and their impact on mental wellness, wrapped in a high-fidelity
# "Liquid Glass" user interface inspired by modern iOS aesthetics.
# ==============================================================================

# ==============================================================================
# [SECTION 1] LIBRARY IMPORTS & DEPENDENCIES
# ==============================================================================
# Standard Library Imports
import os
import time
import json
import base64

# Third-Party Library Imports
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
from PIL import Image

# ==============================================================================
# [SECTION 2] ASSET & CONSTANT CONFIGURATION
# ==============================================================================
# NOTE: Ensure these specific image files are located in the root directory.
# The app relies on them for branding continuity.
# ==============================================================================

FAVICON_FILENAME = "Gemini_Generated_Image_g704tpg704tpg704.png"
LOGO_FILENAME = "Gemini_Generated_Image_g704tpg704tpg704.png"

# Machine Learning Model Configuration
MODEL_FILE = 'mental_health_model.joblib' 

# Generative AI Configuration
GEMINI_MODEL = 'gemini-2.5-flash'

# API Key Retrieval (Secure Access)
# ------------------------------------------------------------------------------
# We use st.secrets for production safety. Ensure .streamlit/secrets.toml exists.
API_KEY = st.secrets.get("GEMINI_API_KEY", None)


# ==============================================================================
# [SECTION 3] PAGE SETUP & INITIALIZATION
# ==============================================================================
# Configure the Streamlit page metadata, layout, and browser tab appearance.
# ==============================================================================

st.set_page_config(
    page_title="MindCheck AI",
    page_icon=FAVICON_FILENAME,
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==============================================================================
# [SECTION 4] GLOBAL STATE MANAGEMENT
# ==============================================================================
# We utilize Streamlit's session_state to persist user data, navigation status,
# and interface themes across re-runs.
# ==============================================================================

# 4.1 Navigation State
# ------------------------------------------------------------------------------
if "page" not in st.session_state:
    # Default landing page is 'home'
    st.session_state.page = "home"

# 4.2 Theme State
# ------------------------------------------------------------------------------
if "theme_mode" not in st.session_state:
    # Default theme is Light mode
    st.session_state.theme_mode = "Light"

# 4.3 AI Analysis Results Storage
# ------------------------------------------------------------------------------
if "ai_results" not in st.session_state:
    # Dictionary to hold JSON responses from Gemini
    st.session_state.ai_results = {} 

# 4.4 Scoring Engine Storage
# ------------------------------------------------------------------------------
if "score" not in st.session_state:
    # Float value for the calculated mental health score
    st.session_state.score = None

# 4.5 User Input Persistence
# ------------------------------------------------------------------------------
if "inputs" not in st.session_state:
    # Dictionary to store raw form inputs for recap display
    st.session_state.inputs = {}


# ==============================================================================
# [SECTION 5] CORE LOGIC FUNCTIONS
# ==============================================================================
# These functions handle the business logic, state transitions, and API calls.
# ==============================================================================

def toggle_theme():
    """
    Switches the interface theme between 'Light' and 'Dark'.
    Triggered by the toggle switch in the sidebar/navbar.
    """
    if st.session_state.theme_toggle:
        st.session_state.theme_mode = "Dark"
    else:
        st.session_state.theme_mode = "Light"

def go_to_page(page_name):
    """
    Navigates the user to a specific page within the single-page application structure.
    
    Args:
        page_name (str): The identifier of the target page (e.g., 'home', 'about').
    """
    st.session_state.page = page_name

def reset_interview():
    """
    Resets the interview process, clearing all scores, inputs, and results.
    Returns the user to the interview start page.
    """
    st.session_state.page = "interview"
    st.session_state.ai_results = {}
    st.session_state.score = None
    st.session_state.inputs = {}

@st.cache_resource
def load_ml_model():
    """
    Loads the pre-trained Random Forest/XGBoost model from the disk.
    Cached to prevent IO bottlenecks on every script rerun.
    
    Returns:
        object: The loaded joblib model or None if loading fails.
    """
    try:
        return joblib.load(MODEL_FILE)
    except Exception as e:
        # In production, we might log this error.
        return None

# Load the model immediately upon script execution
model = load_ml_model()

def call_gemini(prompt, is_json=True):
    """
    Interface for the Google Gemini 2.5 Flash API.
    
    Args:
        prompt (str): The text prompt to send to the AI.
        is_json (bool): If True, requests the response in JSON format.
        
    Returns:
        str: The content text from the AI response.
        None: If the API key is missing or the call fails.
    """
    # Safety Check: Ensure API Key exists
    if not API_KEY: 
        return None
        
    # Construct the API Endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    
    # Construct Payload
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    # Add Generation Config if JSON is required
    if is_json: 
        payload["generationConfig"] = {"responseMimeType": "application/json"}
        
    try:
        # Execute POST Request
        response = requests.post(
            url, 
            headers={'Content-Type': 'application/json'}, 
            json=payload, 
            timeout=20 # 20 second timeout for stability
        )
        
        # Parse Response
        if response.status_code == 200:
            data = response.json()
            return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
            
    except Exception as e:
        # Silently handle errors to prevent app crashes
        pass
        
    return None

# Define the Feature Columns expected by the ML Model
# These must match the training data structure exactly.
MODEL_COLUMNS = [
    'Age', 
    'Gender', 
    'Academic_Level', 
    'Avg_Daily_Usage_Hours',
    'Affects_Academic_Performance', 
    'Sleep_Hours_Per_Night',
    'Conflicts_Over_Social_Media', 
    'Addicted_Score',
    'Most_Used_Platform_Facebook', 
    'Most_Used_Platform_Instagram',
    'Most_Used_Platform_KakaoTalk', 
    'Most_Used_Platform_LINE',
    'Most_Used_Platform_LinkedIn', 
    'Most_Used_Platform_Snapchat',
    'Most_Used_Platform_TikTok', 
    'Most_Used_Platform_Twitter',
    'Most_Used_Platform_VKontakte', 
    'Most_Used_Platform_WeChat',
    'Most_Used_Platform_WhatsApp', 
    'Most_Used_Platform_YouTube', 
    'Relationship_Status_Complicated',
    'Relationship_Status_In Relationship', 
    'Relationship_Status_Single'
]


# ==============================================================================
# [SECTION 6] LIQUID GLASS DESIGN SYSTEM (CSS ARCHITECTURE)
# ==============================================================================
# This section contains the aesthetic logic for the application.
# We define color tokens for Dark and Light modes, and then inject a massive
# CSS block to override Streamlit's defaults with "Apple-style" aesthetics.
# ==============================================================================

# 6.1 Color Token Definitions
# ------------------------------------------------------------------------------
themes = {
    "Dark": {
        "bg_image": "radial-gradient(circle at 20% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%)",
        # High transparency for dark mode glass
        "glass_bg": "rgba(20, 20, 25, 0.4)",
        "glass_border": "rgba(255, 255, 255, 0.08)",
        "glass_shine": "rgba(255, 255, 255, 0.03)",
        "text_main": "#f8fafc",
        "text_sub": "#94a3b8",
        # Neon Violet Accent
        "accent": "#a855f7",
        "btn_grad": "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
        # Deep shadows for depth
        "shadow": "rgba(0, 0, 0, 0.6)",
        "highlight": "#c084fc",
        "card_blur": "40px",
        "saturation": "180%"
    },
    "Light": {
        "bg_image": "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #ffffff 100%)",
        # Frosted ice look for light mode
        "glass_bg": "rgba(255, 255, 255, 0.65)",
        "glass_border": "rgba(255, 255, 255, 0.8)",
        "glass_shine": "rgba(255, 255, 255, 0.4)",
        "text_main": "#0f172a",
        "text_sub": "#475569",
        # Sky Blue Accent
        "accent": "#0ea5e9",
        "btn_grad": "linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)",
        # Soft ambient shadows
        "shadow": "rgba(14, 165, 233, 0.15)",
        "highlight": "#0ea5e9",
        "card_blur": "25px",
        "saturation": "160%"
    }
}

# Determine current theme configuration based on session state
current = themes[st.session_state.theme_mode]

# 6.2 Dynamic Background Logic
# ------------------------------------------------------------------------------
def get_dynamic_bg(score):
    """
    Generates the CSS background string.
    If results are active, overlays a subtle pattern of emojis (Happy/Sad)
    based on the mental health score.
    """
    base_bg = current['bg_image']
    
    # Only show emoji pattern on results page
    if st.session_state.page != "results" or score is None:
        return base_bg
        
    # Choose emoji based on score threshold
    emoji = "🌟" if score >= 6 else "🌧️"
    
    # Create an SVG data URI for the background pattern
    svg_pattern = f"""
    <svg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'>
        <text x='50%' y='50%' font-size='35' text-anchor='middle' dominant-baseline='middle' opacity='0.1'>{emoji}</text>
    </svg>
    """
    # Encode SVG to Base64
    b64_svg = base64.b64encode(svg_pattern.encode('utf-8')).decode('utf-8')
    
    # Combine the SVG pattern with the gradient background
    return f"url('data:image/svg+xml;base64,{b64_svg}'), {base_bg}"

# Get the final background CSS
final_background_css = get_dynamic_bg(st.session_state.score)

# 6.3 CSS Injection (The Design System)
# ------------------------------------------------------------------------------
# This block injects the visual rules for the app.
# It uses CSS3 features like backdrop-filter, linear-gradients, 
# and complex box-shadows to achieve the "Liquid Glass" effect.
# ------------------------------------------------------------------------------

st.markdown(f"""
<style>
    /* =========================================================================
       1. GLOBAL RESET & TYPOGRAPHY
       ========================================================================= */
    /* Import modern sans-serif fonts to mimic Apple's SF Pro */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=Poppins:wght@300;400;600;800&display=swap');

    /* Apply background and fonts to main container */
    .stApp {{
        background: {final_background_css};
        background-attachment: fixed;
        background-size: cover;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Poppins', sans-serif;
        color: {current['text_main']};
        /* Smooth transition for theme switching */
        transition: background 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }}

    /* Global Text Colors */
    h1, h2, h3, h4, h5, h6 {{
        color: {current['text_main']} !important;
        letter-spacing: -0.02em;
        font-weight: 700;
    }}
    
    p, label, li, span {{
        color: {current['text_main']} !important;
        letter-spacing: 0.01em;
    }}

    /* Fix Streamlit's default padding */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 1100px;
    }}

    /* =========================================================================
       2. LIQUID GLASS CARD ENGINE
       ========================================================================= */
    /* This class creates the frosted glass effect.
       - backdrop-filter: blurs everything behind the card.
       - saturate: boosts colors behind the card for vibrancy.
       - border: adds a subtle highlight to mimic glass edges.
       - box-shadow: creates depth and elevation.
    */
    .glass-card {{
        background: {current['glass_bg']};
        /* The Secret Sauce for Apple-like Glass */
        backdrop-filter: blur({current['card_blur']}) saturate({current['saturation']});
        -webkit-backdrop-filter: blur({current['card_blur']}) saturate({current['saturation']});
        
        border: 1px solid {current['glass_border']};
        /* Squircle-like border radius */
        border-radius: 32px; 
        
        padding: 35px;
        margin-bottom: 30px;
        
        /* Deep, soft shadows for floating effect */
        box-shadow: 
            0 20px 40px -10px {current['shadow']},
            inset 0 0 0 1px {current['glass_shine']};
            
        /* Animation properties */
        transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), 
                    box-shadow 0.3s ease;
    }}
    
    /* Hover effect for interactivity */
    .glass-card:hover {{
        transform: translateY(-6px) scale(1.005);
        box-shadow: 
            0 30px 60px -12px {current['shadow']},
            inset 0 0 0 1px rgba(255,255,255,0.3);
    }}

    /* =========================================================================
       3. NAVIGATION BAR (THE "FLOATING PILL")
       ========================================================================= */
    .nav-pill-container {{
        width: 100%;
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
        margin-top: 10px;
        z-index: 100;
    }}
    
    .nav-pill {{
        background: {current['glass_bg']};
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid {current['glass_border']};
        
        /* Fully rounded pill shape */
        border-radius: 100px;
        
        padding: 12px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        
        box-shadow: 0 10px 30px -5px {current['shadow']};
    }}

    /* =========================================================================
       4. BUTTON SYSTEM (APPLE STYLE)
       ========================================================================= */
    /* Target Streamlit buttons */
    .stButton > button {{
        background: {current['btn_grad']} !important;
        color: #ffffff !important;
        border: none !important;
        
        /* Apple style rounding */
        border-radius: 18px !important;
        
        padding: 14px 28px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        
        /* Shadow for lift */
        box-shadow: 0 8px 20px -6px {current['shadow']} !important;
        
        /* Smooth elastic transition */
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 15px 30px -8px {current['shadow']} !important;
        filter: brightness(1.1);
    }}
    
    .stButton > button:active {{
        transform: scale(0.96);
    }}

    /* =========================================================================
       5. INPUT FIELDS (CRITICAL REQUIREMENT)
       ========================================================================= */
    /* Requirement: Inputs must have WHITE background and BLACK text
       in both Dark and Light modes.
    */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important;
    }}
    
    /* Fix for Dropdown Menus */
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
    }}
    div[data-testid="stSelectbox"] div[class*="st-"] {{
        color: #000000 !important;
    }}
    /* Dropdown options container */
    div[data-baseweb="popover"] {{
        background-color: #ffffff !important;
    }}
    div[role="option"] {{
        color: #000000 !important;
        background-color: #ffffff !important;
    }}
    div[role="option"]:hover {{
        background-color: #f0f9ff !important;
    }}

    /* =========================================================================
       6. HEADERS & DECORATIONS
       ========================================================================= */
    .section-title {{
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
        font-weight: 800;
        color: {current['accent']} !important;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .section-title::after {{
        content: "";
        flex-grow: 1;
        height: 2px;
        background: linear-gradient(90deg, {current['accent']}, transparent);
        margin-left: 10px;
        opacity: 0.5;
    }}

    .hero-title {{
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -2px;
        background: {current['btn_grad']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 0 10px 30px {current['shadow']};
    }}

    /* =========================================================================
       7. LOADER ANIMATION (CYBER HEART)
       ========================================================================= */
    .loader-overlay {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(5, 5, 10, 0.9);
        z-index: 99999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        backdrop-filter: blur(25px);
    }}
    
    .cyber-spinner {{
        width: 120px; height: 120px; position: relative;
    }}
    
    .spinner-ring {{
        position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 4px solid transparent;
        border-top-color: #0ea5e9; border-right-color: #0ea5e9;
        animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
        filter: drop-shadow(0 0 10px #0ea5e9);
    }}
    
    .spinner-ring-inner {{
        position: absolute; width: 60%; height: 60%; top: 20%; left: 20%;
        border-radius: 50%; border: 4px solid transparent;
        border-bottom-color: #ec4899; border-left-color: #ec4899;
        animation: spin-rev 2s linear infinite;
        filter: drop-shadow(0 0 10px #ec4899);
    }}
    
    .heart-core {{
        position: absolute; top: 50%; left: 50%; width: 20px; height: 20px;
        background: #a855f7; transform: translate(-50%, -50%) rotate(45deg);
        animation: heartbeat 1s ease-in-out infinite;
        box-shadow: 0 0 20px #a855f7;
    }}
    .heart-core:before, .heart-core:after {{
        content: ""; position: absolute; width: 20px; height: 20px;
        background: #a855f7; border-radius: 50%;
    }}
    .heart-core:before {{ left: -10px; }}
    .heart-core:after {{ top: -10px; }}

    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    @keyframes spin-rev {{ 0% {{ transform: rotate(360deg); }} 100% {{ transform: rotate(-360deg); }} }}
    @keyframes heartbeat {{
        0% {{ transform: translate(-50%, -50%) rotate(45deg) scale(0.8); opacity: 0.8; }}
        50% {{ transform: translate(-50%, -50%) rotate(45deg) scale(1.2); opacity: 1; }}
        100% {{ transform: translate(-50%, -50%) rotate(45deg) scale(0.8); opacity: 0.8; }}
    }}
    
    .loader-text {{
        margin-top: 40px; color: white; font-family: 'SF Pro Display';
        font-size: 1.2rem; letter-spacing: 4px; font-weight: 700;
        text-transform: uppercase; 
        animation: textPulse 2s infinite;
    }}
    @keyframes textPulse {{ 0%, 100% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} }}

    /* =========================================================================
       8. ANIMATION UTILITIES
       ========================================================================= */
    .animate-enter {{
        animation: slideUpFade 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        opacity: 0;
    }}
    
    @keyframes slideUpFade {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* =========================================================================
       9. RESPONSIVE ADJUSTMENTS
       ========================================================================= */
    /* Hide default footer */
    footer {{ visibility: hidden; }}
    #MainMenu {{ visibility: hidden; }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{ width: 10px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: {current['accent']}; border-radius: 10px; }}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# [SECTION 7] UTILITY & HELPER FUNCTIONS
# ==============================================================================

def render_top_nav():
    """
    Renders the Apple-style Navigation Pill.
    Layout: [Logo] <-> [Home Button] <-> [Theme Toggle]
    """
    # Container start
    st.markdown('<div class="nav-pill-container"><div class="nav-pill">', unsafe_allow_html=True)
    
    # We use columns inside the main container to layout the interactive elements
    # Since we can't put st.button inside HTML strings directly, we rely on layout order.
    # NOTE: To create the "Pill" visual, we use the CSS class on a wrapper div above,
    # and then place Streamlit columns "inside" that visual space conceptually.
    
    # However, Streamlit columns break out of HTML divs. 
    # So we apply the style to a wrapper and use columns for layout.
    
    col1, col2, col3 = st.columns([1.5, 3, 1.5])
    
    with col1:
        # LOGO DISPLAY
        if os.path.exists(LOGO_FILENAME):
            st.image(LOGO_FILENAME, width=120)
        else:
            st.markdown(f"<h3 style='margin:0; color:{current['highlight']}'>MindCheck</h3>", unsafe_allow_html=True)
            
    with col2:
        # HOME BUTTON
        # Centered in the navbar
        st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
        if st.button("🏠 HOME", key="nav_home_btn"):
            go_to_page("home")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        # THEME TOGGLE
        # Right aligned
        st.markdown("<div style='display:flex; justify-content:flex-end;'>", unsafe_allow_html=True)
        st.toggle("Night Mode", value=(st.session_state.theme_mode == "Dark"), key="theme_toggle", on_change=toggle_theme)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Container end
    st.markdown('</div></div>', unsafe_allow_html=True)

def show_custom_loader(duration=4):
    """
    Displays the full-screen 'Synthesizing Information' loader.
    """
    # HTML structure for the loader
    loader_html = """
    <div class="loader-overlay">
        <div class="cyber-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring-inner"></div>
            <div class="heart-core"></div>
        </div>
        <div class="loader-text">SYNTHESIZING INFORMATION</div>
    </div>
    """
    
    # Create an empty container to hold the loader
    placeholder = st.empty()
    
    # Render the HTML
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    
    # Wait for the specified duration
    time.sleep(duration)
    
    # clear the loader
    placeholder.empty()


# ==============================================================================
# [SECTION 8] MAIN APPLICATION ROUTING LOGIC
# ==============================================================================
# This section handles which "Page" is displayed based on session_state.page
# ==============================================================================

# 1. Always render the navigation bar first
render_top_nav()

# ------------------------------------------------------------------------------
# PAGE 1: HOME (Landing Page)
# ------------------------------------------------------------------------------
if st.session_state.page == "home":
    # 1. Hero Section
    st.markdown(f"""
    <div class="animate-enter" style="text-align: center; padding: 60px 0;">
        <h1 class="hero-title">MindCheck AI</h1>
        <p style="font-size: 1.5rem; opacity: 0.8; font-weight: 400; max-width: 600px; margin: 0 auto;">
            An AI that helps improve mental health.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Main Action Buttons (3 Columns)
    c1, c2, c3 = st.columns(3, gap="large")
    
    # Column 1: About Me
    with c1:
        st.markdown('<div class="glass-card animate-enter" style="text-align:center; height: 100%;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 3rem; margin-bottom: 10px;">👤</div>', unsafe_allow_html=True)
        st.markdown('<h3>Profile</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:20px;">Learn more about the developer.</p>', unsafe_allow_html=True)
        
        if st.button("About Me!", use_container_width=True):
            go_to_page("about")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Column 2: MindCheck AI (The Main Tool)
    with c2:
        # We give this card a special border color to highlight it
        st.markdown(f'<div class="glass-card animate-enter" style="text-align:center; height: 100%; border: 2px solid {current["accent"]};">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 3rem; margin-bottom: 10px;">🧠</div>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:{current["accent"]} !important;">MindCheck AI</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:20px;">Start your mental wellness assessment.</p>', unsafe_allow_html=True)
        
        if st.button("START CHECK-IN", type="primary", use_container_width=True):
            go_to_page("interview")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Column 3: Latest Updates
    with c3:
        st.markdown('<div class="glass-card animate-enter" style="text-align:center; height: 100%;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 3rem; margin-bottom: 10px;">📢</div>', unsafe_allow_html=True)
        st.markdown('<h3>News</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.9rem; opacity:0.7; margin-bottom:20px;">See what is new in version 2.0.</p>', unsafe_allow_html=True)
        
        if st.button("Latest Update", use_container_width=True):
            go_to_page("updates")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE 2: ABOUT ME
# ------------------------------------------------------------------------------
elif st.session_state.page == "about":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 40px;">About Me</h1>', unsafe_allow_html=True)
    
    # Simple card with "Hi." as requested
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; max-width: 600px; margin: 0 auto; padding: 60px;">
        <h2 style="font-weight: 400; font-size: 3rem;">Hi.</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE 3: LATEST UPDATES
# ------------------------------------------------------------------------------
elif st.session_state.page == "updates":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 40px;">Latest Updates</h1>', unsafe_allow_html=True)
    
    # Simple card with "Hello" as requested
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; max-width: 600px; margin: 0 auto; padding: 60px;">
        <h2 style="font-weight: 400; font-size: 3rem;">Hello</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE 4: INTERVIEW (MINDCHECK AI FORM)
# ------------------------------------------------------------------------------
elif st.session_state.page == "interview":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    
    # Header
    st.markdown(f'<h1 style="text-align:center; margin-bottom: 10px;">📝 Mental Health Check-In</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; opacity:0.7; margin-bottom: 40px;">Complete the assessment below to unlock your insights.</p>', unsafe_allow_html=True)
    
    # Form Container
    with st.form("interview_form"):
        # We split the form into two glass cards side-by-side using columns
        c1, c2 = st.columns(2, gap="large")
        
        # Left Column: Profile & Health
        with c1:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">👤 Profile Details</div>', unsafe_allow_html=True)
            
            age = st.number_input("How old are you?", 10, 100, 15, help="Used for demographic benchmarking.")
            gender = st.selectbox("Gender Identity", ["Male", "Female"])
            academic_level = st.selectbox("Current School Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
            
            st.markdown('<br><div class="section-title">❤️ Health Metrics</div>', unsafe_allow_html=True)
            sleep = st.number_input("Average Sleep (Hours/Night)", 0.0, 24.0, 8.0, 0.5)
            rel_status = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced"])
            st.markdown('</div>', unsafe_allow_html=True)

        # Right Column: Digital Habits
        with c2:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📱 Digital Footprint</div>', unsafe_allow_html=True)
            
            avg_daily_usage = st.number_input("Daily Screen Time (Hours)", 0.0, 24.0, 4.0, 0.5)
            platform = st.selectbox("Dominant Platform", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
            
            st.markdown("<br><label style='font-weight:600;'>Self-Perceived Addiction Level (1-10)</label>", unsafe_allow_html=True)
            addiction = st.slider("", 1, 10, 5)
            
            st.markdown('<br><div class="section-title">⚠️ Impact Assessment</div>', unsafe_allow_html=True)
            affects_perf = st.radio("Does usage affect your grades/work?", ["No", "Yes"], horizontal=True)
            conflicts = st.number_input("Weekly conflicts caused by social media?", 0, 10, 0)
            st.markdown('</div>', unsafe_allow_html=True)

        # Submit Button Area
        st.markdown("<br>", unsafe_allow_html=True)
        col_dummy1, col_btn, col_dummy2 = st.columns([1, 2, 1])
        with col_btn:
            submitted = st.form_submit_button("🏁 ANALYZE MY DATA")
            
        # Logic executed when button is clicked
        if submitted:
            # 1. Trigger the Loading Animation (4 seconds as requested)
            show_custom_loader(duration=4)
            
            # 2. Store Inputs in Session State
            st.session_state.inputs = {
                "Age": age, "Gender": gender, "Academic_Level": academic_level,
                "Avg_Daily_Usage_Hours": avg_daily_usage, "Platform": platform,
                "Addiction": addiction, "Sleep": sleep, "Relationship": rel_status,
                "Affects_Performance": affects_perf, "Conflicts": conflicts
            }
            
            # 3. Create DataFrame for Model Prediction
            input_df = pd.DataFrame(0, index=[0], columns=MODEL_COLUMNS)
            try:
                # Map inputs
                input_df['Gender'] = 1 if gender == "Female" else 0 
                input_df['Age'] = age
                input_df['Academic_Level'] = 1 # Simplified
                input_df['Avg_Daily_Usage_Hours'] = avg_daily_usage
                input_df['Addicted_Score'] = addiction
                input_df['Conflicts_Over_Social_Media'] = conflicts
                input_df['Affects_Academic_Performance'] = 1 if affects_perf == "Yes" else 0
                
                # Handle Platform One-Hot Encoding
                if model:
                    plat_col = f"Most_Used_Platform_{platform}"
                    if plat_col in MODEL_COLUMNS: input_df[plat_col] = 1
                    # Get Prediction
                    wellness_score = model.predict(input_df)[0]
                else:
                    # Fallback logic if model fails
                    base = 10 - (avg_daily_usage * 0.3) - (addiction * 0.2) + (sleep * 0.2)
                    wellness_score = max(1, min(10, base))

                # 4. Save Score and Navigate to Results
                st.session_state.score = wellness_score
                go_to_page("results")
                st.rerun()
            except Exception as e:
                st.error(f"Calculation Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE 5: RESULTS DASHBOARD
# ------------------------------------------------------------------------------
elif st.session_state.page == "results":
    st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
    
    # Retrieve data
    score = st.session_state.score
    data = st.session_state.inputs
    
    # 1. Parameter Recap Section (Top)
    # This shows the user what they entered
    st.markdown(f"""
    <div class="glass-card" style="padding: 1rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; border-left: 5px solid {current['highlight']};">
        <div>
            <strong style="color:{current['highlight']}; font-size: 0.9rem; letter-spacing: 1px;">ANALYSIS PARAMETERS:</strong>&nbsp;&nbsp;
            <span style="font-size: 0.9rem; font-family: 'SF Pro Display';">
                <b>{data.get('Age')}y/o {data.get('Gender')}</b> • 
                <b>{data.get('Platform')}</b> ({data.get('Avg_Daily_Usage_Hours')}h/day) • 
                Sleep: <b>{data.get('Sleep')}h</b> • 
                Addiction: <b>{data.get('Addiction')}/10</b>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Results Header with Restart Button
    col_head_1, col_head_2 = st.columns([4, 1.2])
    with col_head_1:
        st.markdown(f'<h1 style="text-align:left; font-size: 3rem;">Mental Health Scorecard</h1>', unsafe_allow_html=True)
    with col_head_2:
        if st.button("🔄 Restart?", use_container_width=True):
            show_custom_loader(duration=2) # 2 Second loader for restart
            reset_interview()
            st.rerun()
    
    # 3. Score Display Logic
    # Determine color and message based on score
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
    <div class="score-container glass-card" style="text-align: center; border: 2px solid {score_color};">
        <h3 style="margin:0; opacity:0.7; letter-spacing:4px; font-size:1rem; font-weight:600;">MENTAL HEALTH INDEX</h3>
        <h1 style="font-size: 8rem; font-weight: 900; margin: 10px 0; color: {score_color} !important; text-shadow: 0 0 30px {score_color}44;">
            {score:.1f}<span style="font-size:2.5rem; opacity:0.5; color:{current['text_main']};">/10</span>
        </h1>
        <div style="background:{score_color}22; display:inline-block; padding:8px 20px; border-radius:20px;">
            <p style="margin:0; color:{score_color} !important; font-weight:700;">{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. AI Insight Tiles
    st.markdown(f'<h3 style="text-align:center; color:{current["highlight"]}; margin-bottom:20px; margin-top:40px;">✨ Generative AI Insights</h3>', unsafe_allow_html=True)
    
    col_ai_1, col_ai_2, col_ai_3 = st.columns(3, gap="medium")
    
    # Tile 1: Persona
    with col_ai_1:
        st.markdown('<div class="glass-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:2.5rem;">📊</div>', unsafe_allow_html=True)
        st.markdown('<h4>My Persona</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">Deep behavioral analysis.</p>', unsafe_allow_html=True)
        
        if st.button("Generate", key="btn_persona", use_container_width=True):
            show_custom_loader(duration=4)
            with st.spinner("Analyzing psychographics..."):
                prompt = f"Based on: {json.dumps(data)}. Return JSON: {{'persona': 'Fun Title', 'analysis': 'Short analysis', 'tips': ['Tip 1', 'Tip 2']}}"
                res = call_gemini(prompt)
                if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Tile 2: Future Self
    with col_ai_2:
        st.markdown('<div class="glass-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:2.5rem;">🕰️</div>', unsafe_allow_html=True)
        st.markdown('<h4>Future Self</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">A message from 2029.</p>', unsafe_allow_html=True)
        
        if st.button("Warp Time", key="btn_future", use_container_width=True):
            show_custom_loader(duration=4)
            with st.spinner("Establishing temporal link..."):
                prompt = f"Write a note from future 2029 self based on habits: {json.dumps(data)}. Max 50 words."
                res = call_gemini(prompt, is_json=False)
                if res: st.session_state.ai_results['future'] = res; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Tile 3: Detox Plan
    with col_ai_3:
        st.markdown('<div class="glass-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:2.5rem;">🍃</div>', unsafe_allow_html=True)
        st.markdown('<h4>Detox Plan</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">3-Day cleansing protocol.</p>', unsafe_allow_html=True)
        
        if st.button("Build Plan", key="btn_detox", use_container_width=True):
            show_custom_loader(duration=4)
            with st.spinner("Drafting protocol..."):
                prompt = f"3-day detox for {data['Platform']} user. JSON: {{'days': [{{'day': 'Day 1', 'theme': 'Theme', 'tasks': ['Task 1', 'Task 2']}}]}}"
                res = call_gemini(prompt)
                if res: st.session_state.ai_results['detox'] = json.loads(res); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Display AI Results (Dynamic Rendering)
    if st.session_state.get('ai_results'):
        st.markdown("<br><hr style='opacity:0.2;'><br>", unsafe_allow_html=True)
        results = st.session_state.ai_results
        
        # Persona Result
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="glass-card animate-enter" style="border-left: 5px solid {current['accent']};">
                <h3 style="color:{current['accent']} !important; margin-top:0;">📊 {r.get('persona', 'User')}</h3>
                <p style="font-style:italic; font-size:1.1rem; opacity:0.9;">"{r.get('analysis', '')}"</p>
                <div style="margin-top:20px;">
                    <strong style="text-transform:uppercase; font-size:0.8rem; letter-spacing:1px;">Key Recommendations:</strong>
                    <ul class="apple-list" style="margin-top:10px;">
                        {"".join([f"<li>{t}</li>" for t in r.get('tips', [])])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Future Result
        if 'future' in results:
            st.markdown(f"""
            <div class="glass-card animate-enter" style="border-left: 5px solid {current['warning']}; background: {current['card_bg']};">
                <h3 style="color:{current['warning']} !important; margin-top:0;">🕰️ Incoming Transmission (2029)</h3>
                <p style="font-family: 'Courier New', monospace; font-size: 1.05rem; line-height: 1.6;">
                    {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Detox Result
        if 'detox' in results:
            r = results['detox']
            days_html = ""
            for d in r.get('days', []):
                tasks = "".join([f"<li>{t}</li>" for t in d.get('tasks', [])])
                days_html += f"""
                <div style='background:rgba(255,255,255,0.05); padding:1rem; margin-bottom:10px; border-radius:16px; border:1px solid {current['glass_border']}'>
                    <strong style="color:{current['success']}; font-size:1.1rem;">{d.get('day')}: {d.get('theme')}</strong>
                    <ul class="apple-list" style="margin-top:5px;">{tasks}</ul>
                </div>
                """
            st.markdown(f"""
            <div class="glass-card animate-enter" style="border-left: 5px solid {current['success']};">
                <h3 style="color:{current['success']} !important; margin-top:0;">🍃 Detox Challenge</h3>
                {days_html}
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# [SECTION 9] FOOTER
# ==============================================================================
st.markdown(f"""
<div style="text-align: center; margin-top: 5rem; opacity: 0.5; font-size: 0.8rem; font-family: 'SF Pro Display';">
    <p>MindCheck AI v3.0 • Powered by Gemini • 2026</p>
</div>
""", unsafe_allow_html=True)

# End of Script
