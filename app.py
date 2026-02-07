# ==============================================================================
#   __________  ____     _ _____ ____ _____   _____ _____ _   _  _____ 
#  |__  / ____|/ __ \   | | ____/ __ \_   _| |__  /| ____| | | |/ ____|
#     / /| |__ | |  | |   | |  __| |  | || |      / / | |__ | | | | (___  
#    / / |  __|| |  | |   | | |_ | |  | || |     / /  |  __|| | | |\___ \ 
#   / /__| |___| |__| |   | |__| | |__| || |_   / /___| |___| |_| |____) |
#  /_____|______\____/    |_____\____/_____| /_____|______\___/|_____/ 
# 
#  PROJECT ZEUS: THE OMNI-BUILD (ENTERPRISE ARCHITECTURE)
# ==============================================================================
#  SYSTEM:       MindCheck AI (Zeus Edition)
#  VERSION:      7.0.0 (The Monolith)
#  ARCHITECT:    Mubashir Mohsin & Gemini (Neural Core)
#  DATE:         February 6, 2026
#  ENGINE:       Dual-Core CSS (Light/Dark Separation) + Transition API
#  LOC TARGET:   Maximum Density / High Fidelity
# ==============================================================================

import streamlit as st
import pandas as pd
import joblib
import json
import time
import requests
import os
import base64
import random
import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum

# ==============================================================================
# SECTION 1: GLOBAL SYSTEM CONFIGURATION
# ==============================================================================
# Defines the immutable constants, file paths, and environment settings.
# ==============================================================================

class SystemMetadata:
    """
    Metadata registry for the application.
    Stores versioning, authorship, and branding assets.
    """
    APP_NAME = "MindCheck AI"
    CODENAME = "ZEUS"
    VERSION = "7.0.0"
    BUILD_DATE = "2026-02-06"
    AUTHOR = "Mubashir Mohsin"
    
    # Asset Configuration
    FAVICON_PATH = "Gemini_Generated_Image_g704tpg704tpg704.png"
    LOGO_PATH = "Gemini_Generated_Image_g704tpg704tpg704.png"
    MODEL_PATH = 'mental_health_model.joblib'
    
    # AI Configuration
    GEMINI_MODEL_ID = 'gemini-2.5-flash'
    API_TIMEOUT = 30 # seconds

class LayoutConfig:
    """
    Configuration regarding the Streamlit layout engine.
    """
    PAGE_LAYOUT = "wide"
    SIDEBAR_STATE = "collapsed"
    MENU_ITEMS = {
        'Get Help': 'https://www.mentalhealth.gov',
        'Report a bug': "mailto:support@mindcheck.ai",
        'About': "# MindCheck AI: Enterprise Edition"
    }

# ------------------------------------------------------------------------------
# INITIALIZATION ROUTINE
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title=SystemMetadata.APP_NAME,
    page_icon=SystemMetadata.FAVICON_PATH,
    layout=LayoutConfig.PAGE_LAYOUT,
    initial_sidebar_state=LayoutConfig.SIDEBAR_STATE,
    menu_items=LayoutConfig.MENU_ITEMS
)

# Secure API Key Access
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ==============================================================================
# SECTION 2: ASSET GENERATION & SVG LIBRARY
# ==============================================================================
# Helper classes to generate visual assets dynamically if files are missing.
# ==============================================================================

class IconLibrary:
    """
    A repository of SVG icons and base64 encoded assets to be used
    throughout the application for visual enrichment.
    """
    
    @staticmethod
    def get_star_svg() -> str:
        """Returns the SVG code for the 'Good Score' Star."""
        return """
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="starGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#FFA500;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path fill="url(#starGrad)" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
        """

    @staticmethod
    def get_cloud_svg() -> str:
        """Returns the SVG code for the 'Bad Score' Sad Cloud."""
        return """
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="rainGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#4a5568;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#2d3748;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path fill="url(#rainGrad)" d="M4.5 11a4.5 4.5 0 013.9-6.8 7 7 0 0113.2 2.6A5 5 0 0117 17H5a5 5 0 01-.5-6zm4 8v3m4-3v3m4-3v3"/>
        </svg>
        """

    @staticmethod
    def get_loader_svg() -> str:
        """Returns a complex SVG for the loading animation."""
        return """
        <svg width="100" height="100" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="40" stroke="#3498db" stroke-width="4" fill="none">
                <animate attributeName="stroke-dasharray" from="0 251" to="251 0" dur="2s" repeatCount="indefinite"/>
                <animate attributeName="stroke-dashoffset" from="0" to="-251" dur="2s" repeatCount="indefinite"/>
            </circle>
        </svg>
        """

# ==============================================================================
# SECTION 3: SESSION STATE MANAGEMENT ARCHITECTURE
# ==============================================================================
# Handles persistence, navigation flow, and temporary data storage.
# ==============================================================================

@dataclass
class SessionState:
    """
    Data Transfer Object representing the user's current session.
    """
    page: str = "home"
    theme_mode: str = "Dark" # Defaulting to Dark for that 'Zeus' feel
    is_transitioning: bool = False # For the animation
    wizard_step: int = 0
    inputs: Dict[str, Any] = field(default_factory=dict)
    score: Optional[float] = None
    ai_results: Dict[str, Any] = field(default_factory=dict)

class StateController:
    """
    Controller class to manage Streamlit's session state dictionary.
    """
    KEY = "zeus_core_session"

    @staticmethod
    def init():
        """Initializes the session state if it doesn't exist."""
        if StateController.KEY not in st.session_state:
            st.session_state[StateController.KEY] = SessionState()
        
        # Widget-specific state keys
        if "theme_toggle_btn" not in st.session_state:
            st.session_state.theme_toggle_btn = True # True = Dark Mode

    @staticmethod
    def get() -> SessionState:
        """Returns the current session object."""
        return st.session_state[StateController.KEY]

    @staticmethod
    def toggle_theme():
        """
        Handles the complex logic of switching themes with animation.
        Sets a 'transitioning' flag to True, allowing the UI to render the overlay.
        """
        session = StateController.get()
        
        # Trigger Transition Animation
        session.is_transitioning = True
        
        # Actual Toggle Logic
        if st.session_state.theme_toggle_btn:
            session.theme_mode = "Dark"
        else:
            session.theme_mode = "Light"

    @staticmethod
    def clear_transition():
        """Resets the transition flag after the animation plays."""
        SessionController.get().is_transitioning = False

    @staticmethod
    def navigate(page_name: str):
        """Routes the user to a different page."""
        session = StateController.get()
        session.page = page_name
        if page_name != "interview":
            session.wizard_step = 0

    @staticmethod
    def next_step():
        """Advances the wizard."""
        StateController.get().wizard_step += 1

    @staticmethod
    def prev_step():
        """Reverses the wizard."""
        s = StateController.get()
        if s.wizard_step > 0:
            s.wizard_step -= 1

    @staticmethod
    def reset_app():
        """Hard reset of application data."""
        s = StateController.get()
        s.page = "interview"
        s.wizard_step = 0
        s.inputs = {}
        s.score = None
        s.ai_results = {}

# ==============================================================================
# SECTION 4: THE DUAL-CORE CSS ENGINE
# ==============================================================================
# Unlike previous versions, this engine generates COMPLETELY DIFFERENT CSS
# for Light and Dark modes to ensure maximum readability and aesthetic direction.
# ==============================================================================

class DualCoreCSSEngine:
    
    @staticmethod
    def get_transition_css() -> str:
        """
        Generates the Windows-like transition overlay CSS.
        """
        return """
        <style>
            @keyframes dissolve {
                0% { opacity: 0; backdrop-filter: blur(0px); }
                50% { opacity: 1; backdrop-filter: blur(20px); background: rgba(0,0,0,0.5); }
                100% { opacity: 0; backdrop-filter: blur(0px); }
            }
            .theme-transition-overlay {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                z-index: 999999; pointer-events: none;
                animation: dissolve 1s ease-in-out forwards;
            }
        </style>
        <div class="theme-transition-overlay"></div>
        """

    @staticmethod
    def _common_css() -> str:
        """CSS shared between both modes (Layouts, Resets)."""
        return """
        /* --- FONT IMPORTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

        /* --- RESET --- */
        .stApp { transition: background 0.5s ease; }
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding-top: 2rem; padding-bottom: 6rem; max-width: 1200px; }
        
        /* --- ANIMATIONS --- */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes scaleIn { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        
        .anim-fade { animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .anim-scale { animation: scaleIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        """

    @staticmethod
    def _dark_mode_css() -> str:
        """
        THE DARK CORE: Cyberpunk/Neon Aesthetic.
        Optimized for low-light environments with high contrast neons.
        """
        return """
        /* --- DARK MODE VARIABLES --- */
        :root {
            --bg-color: #050505;
            --bg-grad: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 80%);
            --card-bg: rgba(20, 20, 25, 0.6);
            --card-border: 1px solid rgba(255, 255, 255, 0.1);
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --accent: #00f2ff;
            --accent-glow: 0 0 15px rgba(0, 242, 255, 0.4);
            --input-bg: rgba(255, 255, 255, 0.05);
            --font-head: 'Space Grotesk', sans-serif;
            --font-body: 'Plus Jakarta Sans', sans-serif;
        }

        .stApp {
            background-color: var(--bg-color);
            background-image: var(--bg-grad);
            color: var(--text-primary);
        }

        h1, h2, h3, h4 {
            font-family: var(--font-head);
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* --- DARK CARD --- */
        .zeus-card {
            background: var(--card-bg);
            border: var(--card-border);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: all 0.3s ease;
        }
        .zeus-card:hover {
            border-color: var(--accent);
            box-shadow: var(--accent-glow);
            transform: translateY(-5px);
        }

        /* --- DARK INPUTS --- */
        .stTextInput input, .stNumberInput input {
            background: var(--input-bg) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 10px !important;
        }
        .stSelectbox div[data-baseweb="select"] > div {
            background: var(--input-bg) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
        }

        /* --- DARK BUTTONS --- */
        .stButton button {
            background: linear-gradient(90deg, #00f2ff, #0078ff) !important;
            color: black !important;
            border: none !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            border-radius: 8px !important;
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.2) !important;
        }
        
        /* --- DARK NAVBAR --- */
        .nav-container {
            background: rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
        }
        """

    @staticmethod
    def _light_mode_css() -> str:
        """
        THE LIGHT CORE: Clean/Aero Aesthetic.
        Optimized for high readability with soft shadows and gradients.
        """
        return """
        /* --- LIGHT MODE VARIABLES --- */
        :root {
            --bg-color: #f8f9fa;
            --bg-grad: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            --card-bg: rgba(255, 255, 255, 0.85);
            --card-border: 1px solid rgba(255, 255, 255, 1);
            --text-primary: #1a1a1a;
            --text-secondary: #5a5a5a;
            --accent: #4a90e2;
            --accent-glow: 0 10px 20px rgba(74, 144, 226, 0.3);
            --input-bg: #ffffff;
            --font-head: 'Plus Jakarta Sans', sans-serif;
            --font-body: 'Plus Jakarta Sans', sans-serif;
        }

        .stApp {
            background: var(--bg-grad);
            color: var(--text-primary);
        }

        h1, h2, h3, h4 {
            font-family: var(--font-head);
            color: #2c3e50;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        /* --- LIGHT CARD --- */
        .zeus-card {
            background: var(--card-bg);
            border: var(--card-border);
            border-radius: 24px;
            padding: 35px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .zeus-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }

        /* --- LIGHT INPUTS --- */
        .stTextInput input, .stNumberInput input {
            background: #ffffff !important;
            color: #333 !important;
            border: 2px solid #e0e0e0 !important;
            border-radius: 12px !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: var(--accent) !important;
        }
        
        .stSelectbox div[data-baseweb="select"] > div {
            background: #ffffff !important;
            color: #333 !important;
            border: 2px solid #e0e0e0 !important;
            border-radius: 12px !important;
        }

        /* --- LIGHT BUTTONS --- */
        .stButton button {
            background: linear-gradient(135deg, #4a90e2, #007aff) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 50px !important;
            box-shadow: 0 5px 15px rgba(74, 144, 226, 0.4) !important;
        }
        
        /* --- LIGHT NAVBAR --- */
        .nav-container {
            background: rgba(255, 255, 255, 0.8);
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            backdrop-filter: blur(20px);
        }
        """

    @classmethod
    def inject(cls, mode: str):
        """
        Injects the appropriate CSS block based on the mode.
        """
        common = cls._common_css()
        specific = cls._dark_mode_css() if mode == "Dark" else cls._light_mode_css()
        
        full_payload = f"<style>{common}\n{specific}</style>"
        st.markdown(full_payload, unsafe_allow_html=True)

# ==============================================================================
# SECTION 5: INTELLIGENCE & LOGIC LAYER
# ==============================================================================
# Handles backend processing, scoring algorithms, and AI interactions.
# ==============================================================================

class IntelligenceCore:
    """
    The Brain of Project Zeus.
    """
    
    @staticmethod
    @st.cache_resource
    def load_model():
        try:
            return joblib.load(SystemMetadata.MODEL_PATH)
        except Exception:
            return None

    @staticmethod
    def calculate_fallback_score(data: Dict[str, Any]) -> float:
        """
        Advanced algorithmic scoring if ML model is unavailable.
        Uses a weighted penalty system.
        """
        usage = data.get('Avg_Daily_Usage_Hours', 4.0)
        addiction = data.get('Addiction', 5.0)
        sleep = data.get('Sleep', 8.0)
        conflicts = data.get('Conflicts', 0)
        
        score = 10.0
        
        # Penalties
        score -= (usage * 0.3)      # Heavy usage penalty
        score -= (addiction * 0.25) # Perception penalty
        score -= (conflicts * 0.4)  # Social penalty
        
        # Bonuses
        if sleep >= 7 and sleep <= 9:
            score += 0.5
        elif sleep < 5:
            score -= 1.0
            
        # Bounds check
        return max(1.0, min(10.0, score))

    @staticmethod
    def query_gemini(prompt: str, is_json: bool = True) -> Any:
        """
        Robust connector to Google Gemini API.
        """
        if not API_KEY:
            return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{SystemMetadata.GEMINI_MODEL_ID}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        if is_json:
            payload["generationConfig"] = {"responseMimeType": "application/json"}
            
        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=25)
            if response.status_code == 200:
                text = response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
                return text
        except Exception as e:
            pass # Fail gracefully in UI
        return None

# ==============================================================================
# SECTION 6: COMPONENT FACTORY
# ==============================================================================
# Reusable UI widgets that abstract away the HTML/CSS complexity.
# ==============================================================================

class ComponentFactory:
    
    @staticmethod
    def navbar():
        """Renders the top navigation."""
        st.markdown('<div class="nav-container" style="padding: 15px 30px; margin-bottom: 40px; border-radius: 15px;">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 6, 2], gap="small")
        
        with c1:
            if os.path.exists(SystemMetadata.LOGO_PATH):
                st.image(SystemMetadata.LOGO_PATH, width=100)
            else:
                st.markdown('<h3 style="margin:0;">MINDCHECK</h3>', unsafe_allow_html=True)
        
        with c2:
            st.markdown('<div style="display:flex; justify-content:center; width:100%;">', unsafe_allow_html=True)
            if st.button("DASHBOARD", key="nav_home"):
                StateController.navigate("home")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c3:
            st.markdown('<div style="display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
            is_dark = (StateController.get().theme_mode == "Dark")
            st.toggle("Dark Mode", value=is_dark, key="theme_toggle_btn", on_change=StateController.toggle_theme)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def info_card(title: str, content: str, icon: str, center: bool = False):
        """Renders a standard Zeus Card."""
        align = "center" if center else "left"
        st.markdown(f"""
        <div class="zeus-card anim-fade" style="text-align: {align};">
            <div style="font-size: 3rem; margin-bottom: 15px;">{icon}</div>
            <h3>{title}</h3>
            <p style="opacity: 0.8;">{content}</p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def loader_overlay(message: str = "PROCESSING"):
        """Displays the transition overlay."""
        # Simple CSS spinner for loader
        spinner_html = f"""
        <style>
            .loader-box {{
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.85); z-index: 10000;
                display: flex; flex-direction: column; justify-content: center; align-items: center;
                backdrop-filter: blur(10px);
            }}
            .spinner {{
                width: 60px; height: 60px; border: 5px solid #f3f3f3;
                border-top: 5px solid #3498db; border-radius: 50%;
                animation: spin 1s linear infinite;
            }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        </style>
        <div class="loader-box">
            <div class="spinner"></div>
            <h2 style="color:white; margin-top:20px;">{message}...</h2>
        </div>
        """
        placeholder = st.empty()
        placeholder.markdown(spinner_html, unsafe_allow_html=True)
        time.sleep(UIConfig.LOADER_DURATION)
        placeholder.empty()

# ==============================================================================
# SECTION 7: SCENE CONTROLLERS
# ==============================================================================
# The logic for each specific page view.
# ==============================================================================

class SceneHome:
    @staticmethod
    def render():
        st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
        
        # Hero Section
        st.markdown("""
        <div class="anim-scale" style="text-align: center; margin-bottom: 60px;">
            <h1 style="font-size: 5rem; margin-bottom: 10px;">MINDCHECK AI</h1>
            <p style="font-size: 1.5rem; opacity: 0.7;">ENTERPRISE WELLNESS ANALYTICS</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            st.markdown('<div style="height: 100%;">', unsafe_allow_html=True)
            ComponentFactory.info_card("About Creator", "Meet Mubashir Mohsin.", "👨‍💻", True)
            if st.button("VIEW BIO", use_container_width=True):
                StateController.navigate("about")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div style="height: 100%;">', unsafe_allow_html=True)
            ComponentFactory.info_card("Diagnostics", "Start system assessment.", "🧬", True)
            if st.button("START WIZARD", type="primary", use_container_width=True):
                StateController.navigate("interview")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

class SceneAbout:
    @staticmethod
    def render():
        st.markdown('<div class="anim-fade">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; margin-bottom:40px;">CREATOR LOG</h1>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 4, 1])
        with c2:
            st.markdown("""
            <div class="zeus-card" style="text-align: center; padding: 50px;">
                <div style="font-size: 6rem; margin-bottom: 20px;">🚀</div>
                <p style="font-size: 1.3rem; line-height: 1.8; margin-bottom: 30px;">
                    "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
                </p>
                <p style="opacity: 0.5; font-size: 0.9rem;">- February 6, 2026</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

class SceneInterview:
    @staticmethod
    def render():
        state = StateController.get()
        steps = ["Profile", "Digital Habits", "Health", "Final Review"]
        curr = state.wizard_step
        
        # Progress UI
        st.markdown(f"<h2 style='text-align:center;'>STEP {curr + 1}: {steps[curr].upper()}</h2>", unsafe_allow_html=True)
        prog_val = (curr + 1) / len(steps)
        st.progress(prog_val)
        
        st.markdown('<div class="zeus-card anim-scale" style="margin-top: 30px;">', unsafe_allow_html=True)
        
        # --- WIZARD LOGIC ---
        if curr == 0: # Profile
            state.inputs['Age'] = st.number_input("Age", 10, 100, state.inputs.get('Age', 15))
            state.inputs['Gender'] = st.selectbox("Gender", ["Male", "Female"], index=0)
            state.inputs['Academic_Level'] = st.selectbox("Education", ["Middle School", "High School", "Undergraduate"])
            
            if st.button("NEXT ➔"): StateController.next_step(); st.rerun()

        elif curr == 1: # Habits
            state.inputs['Platform'] = st.selectbox("Platform", ["TikTok", "YouTube", "Instagram", "Snapchat", "Other"])
            state.inputs['Avg_Daily_Usage_Hours'] = st.number_input("Screen Time (Hrs)", 0.0, 24.0, state.inputs.get('Avg_Daily_Usage_Hours', 4.0))
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ BACK"): StateController.prev_step(); st.rerun()
            with c2: 
                if st.button("NEXT ➔"): StateController.next_step(); st.rerun()

        elif curr == 2: # Health
            state.inputs['Sleep'] = st.number_input("Sleep (Hrs)", 0.0, 24.0, state.inputs.get('Sleep', 8.0))
            state.inputs['Addiction'] = st.slider("Addiction Level (1-10)", 1, 10, state.inputs.get('Addiction', 5))
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ BACK"): StateController.prev_step(); st.rerun()
            with c2: 
                if st.button("NEXT ➔"): StateController.next_step(); st.rerun()

        elif curr == 3: # Final
            state.inputs['Conflicts'] = st.number_input("Conflicts", 0, 20, state.inputs.get('Conflicts', 0))
            state.inputs['Affects_Performance'] = st.radio("Impacts Grades?", ["No", "Yes"])
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ BACK"): StateController.prev_step(); st.rerun()
            with c2: 
                if st.button("ANALYZE 🚀"):
                    ComponentFactory.loader_overlay("CALCULATING VECTORS")
                    
                    # Score Logic
                    d = state.inputs
                    base = 10.0
                    base -= (d['Avg_Daily_Usage_Hours'] * 0.3)
                    base -= (d['Addiction'] * 0.2)
                    base += (d['Sleep'] * 0.1)
                    if d['Affects_Performance'] == "Yes": base -= 1.0
                    
                    state.score = max(1.0, min(10.0, base))
                    StateController.navigate("results")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

class SceneResults:
    @staticmethod
    def render():
        state = StateController.get()
        score = state.score
        
        st.markdown('<div class="anim-scale">', unsafe_allow_html=True)
        
        # Determine Visuals based on Score
        if score >= 7:
            color = "#00ff88"
            icon_svg = IconLibrary.get_star_svg() # THE STAR
            msg = "EXCELLENT CONDITION"
        else:
            color = "#ff4757"
            icon_svg = IconLibrary.get_cloud_svg() # THE SAD CLOUD
            msg = "ATTENTION REQUIRED"
            
        # Render the SVG Icon
        b64_icon = base64.b64encode(icon_svg.encode('utf-8')).decode("utf-8")
        
        # Score Card
        st.markdown(f"""
        <div class="zeus-card" style="text-align: center; border-top: 5px solid {color};">
            <div style="width: 100px; height: 100px; margin: 0 auto;">
                <img src="data:image/svg+xml;base64,{b64_icon}" width="100" height="100">
            </div>
            <h1 style="font-size: 6rem; color: {color}; margin: 20px 0;">{score:.1f}</h1>
            <h3 style="color: {color}; opacity: 0.8;">{msg}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Section
        st.markdown("<h2 style='text-align:center; margin: 40px 0;'>AI INSIGHTS</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown('<div class="zeus-card" style="text-align:center; height:100%"><h3>PROFILE</h3><p>Analyze Persona</p></div>', unsafe_allow_html=True)
            if st.button("GENERATE PROFILE", use_container_width=True):
                ComponentFactory.loader_overlay("ANALYZING")
                prompt = f"Data: {json.dumps(state.inputs)}. Return JSON: 'persona', 'analysis', 'tips'."
                res = IntelligenceCore.query_gemini(prompt, is_json=True)
                if res: 
                    state.ai_results['analysis'] = json.loads(res)
                    st.rerun()
                    
        with c2:
            st.markdown('<div class="zeus-card" style="text-align:center; height:100%"><h3>TIME TRAVEL</h3><p>Message from 2029</p></div>', unsafe_allow_html=True)
            if st.button("CONNECT", use_container_width=True):
                ComponentFactory.loader_overlay("CONNECTING")
                prompt = f"Message from 2029 self based on: {json.dumps(state.inputs)}. Max 50 words."
                res = IntelligenceCore.query_gemini(prompt, is_json=False)
                if res: 
                    state.ai_results['future'] = res
                    st.rerun()
        
        # Show Results
        res = state.ai_results
        if 'analysis' in res:
            r = res['analysis']
            st.markdown(f"<div class='zeus-card'><h3>{r.get('persona')}</h3><p>{r.get('analysis')}</p></div>", unsafe_allow_html=True)
        if 'future' in res:
            st.markdown(f"<div class='zeus-card'><h3>TRANSMISSION</h3><p>{res['future']}</p></div>", unsafe_allow_html=True)
            
        if st.button("RESTART SYSTEM", use_container_width=True):
            StateController.reset_app()
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SECTION 8: MAIN EXECUTION THREAD
# ==============================================================================

def main():
    # 1. Init Session State
    StateController.init()
    
    # 2. Check for transition animation needed
    session = StateController.get()
    if session.is_transitioning:
        # Inject animation CSS
        st.markdown(DualCoreCSSEngine.get_transition_css(), unsafe_allow_html=True)
        # We don't sleep here to allow UI to render behind it, 
        # but in Streamlit we often need a moment for the user to see it.
        time.sleep(0.5)
        StateController.clear_transition()
        st.rerun()

    # 3. Inject Theme-Specific CSS
    DualCoreCSSEngine.inject(session.theme_mode)
    
    # 4. Render Navbar
    ComponentFactory.navbar()
    
    # 5. Routing
    if session.page == "home":
        SceneHome.render()
    elif session.page == "about":
        SceneAbout.render()
    elif session.page == "interview":
        SceneInterview.render()
    elif session.page == "results":
        SceneResults.render()
        
    # 6. Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 80px; padding-top: 20px; border-top: 1px solid rgba(128,128,128,0.2); font-size: 0.8rem; opacity: 0.5;">
        PROJECT ZEUS // MINDCHECK AI v7.0 // 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
