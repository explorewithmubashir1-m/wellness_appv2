# ==============================================================================
#   ____  _____   ___       _ ______ _____ _______   ____  _  __     ____  __  __ _____  _    _  _____ 
#  |  _ \|  __ \ / _ \     | |  ____/ ____|__   __| / __ \| | \ \   / /  \/  |  __ \| |  | |/ ____|
#  | |_) | |__) | | | |_   | | |__ | |       | |   | |  | | |  \ \_/ /| \  / | |__) | |  | | (___  
#  |  _ <|  _  /| | | | |  | |  __|| |       | |   | |  | | |   \   / | |\/| |  ___/| |  | |\___ \ 
#  | |_) | | \ \| |_| | |__| | |___| |____   | |   | |__| | |____| |  | |  | | |    | |__| |____) |
#  |____/|_|  \_\\___/ \____/|______\_____|  |_|    \____/|______|_|  |_|  |_|_|     \____/|_____/ 
# 
#  PROJECT OLYMPUS: THE APEX BUILD (ENTERPRISE ARCHITECTURE v8.0)
# ==============================================================================
#  SYSTEM:       MindCheck AI (Olympus Edition)
#  VERSION:      8.0.0 (Stable Release)
#  ARCHITECT:    Mubashir Mohsin & Gemini (Neural Core)
#  DATE:         February 6, 2026
#  ENGINE:       Triple-Core Nebula CSS + Procedural SVG Generation
#  LOC TARGET:   Maximum Density / Ultra-High Fidelity
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
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum

# ==============================================================================
# MODULE 1: GLOBAL CONFIGURATION & CONSTANTS
# ==============================================================================
# Defines immutable system parameters, file paths, and environment settings.
# ==============================================================================

class SystemMetadata:
    """
    Registry for static application metadata.
    Acts as the single source of truth for versioning and authorship.
    """
    APP_NAME = "MindCheck AI"
    CODENAME = "OLYMPUS"
    VERSION = "8.0.0"
    BUILD_DATE = "2026-02-06"
    AUTHOR = "Mubashir Mohsin"
    
    # Asset Configuration (Procedural Fallbacks Enabled)
    FAVICON_EMOJI = "🧠"
    MODEL_FILENAME = 'mental_health_model.joblib'
    
    # AI Configuration
    GEMINI_MODEL_ID = 'gemini-2.5-flash'
    API_TIMEOUT_SECONDS = 45

class UIConfig:
    """
    Configuration regarding the Streamlit layout engine and visual constraints.
    """
    PAGE_LAYOUT = "wide"
    SIDEBAR_STATE = "collapsed"
    ANIMATION_SPEED_MS = 400
    LOADER_DURATION_SEC = 3.5
    
    MENU_ITEMS = {
        'Get Help': 'https://www.mentalhealth.gov',
        'Report a bug': "mailto:support@mindcheck.ai",
        'About': f"### MindCheck AI v{SystemMetadata.VERSION}\nPowered by Project Olympus Architecture."
    }

# Initialize Streamlit Page Configuration
st.set_page_config(
    page_title=SystemMetadata.APP_NAME,
    page_icon=SystemMetadata.FAVICON_EMOJI,
    layout=UIConfig.PAGE_LAYOUT,
    initial_sidebar_state=UIConfig.SIDEBAR_STATE,
    menu_items=UIConfig.MENU_ITEMS
)

# Secure API Key Access
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ==============================================================================
# MODULE 2: PROCEDURAL ASSET GENERATOR
# ==============================================================================
# Instead of relying on external files that might break, this module generates
# high-quality SVG assets (logos, icons, backgrounds) on the fly using code.
# ==============================================================================

class ProceduralAssets:
    """
    Generates SVG graphics programmatically to ensure the app looks beautiful
    even without external image files.
    """
    
    @staticmethod
    def get_logo_svg(theme: str) -> str:
        """Generates the main application logo."""
        color1 = "#00f2ff" if theme == "Dark" else "#2563eb"
        color2 = "#bd00ff" if theme == "Dark" else "#7c3aed"
        
        svg = f"""
        <svg width="300" height="80" viewBox="0 0 300 80" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
                </linearGradient>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <g filter="url(#glow)">
                <path fill="url(#logoGrad)" d="M40,20 Q50,5 60,20 T80,20 T100,20" stroke="url(#logoGrad)" stroke-width="4" fill="none"/>
                <circle cx="50" cy="40" r="5" fill="{color1}" />
                <circle cx="70" cy="40" r="5" fill="{color2}" />
                <text x="90" y="55" font-family="sans-serif" font-weight="900" font-size="40" fill="url(#logoGrad)">MINDCHECK</text>
            </g>
        </svg>
        """
        return base64.b64encode(svg.encode('utf-8')).decode("utf-8")

    @staticmethod
    def get_star_icon() -> str:
        """Generates the 3D Star Icon for good scores."""
        svg = """
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="starGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#FFA500;stop-opacity:1" />
                </linearGradient>
                <filter id="starGlow">
                    <feGaussianBlur stdDeviation="10" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <path filter="url(#starGlow)" fill="url(#starGrad)" d="M256,32l56,156h164l-128,96l48,156l-140-96l-140,96l48-156l-128-96h164L256,32z" />
        </svg>
        """
        return base64.b64encode(svg.encode('utf-8')).decode("utf-8")

    @staticmethod
    def get_rain_icon() -> str:
        """Generates the Rain Cloud Icon for critical scores."""
        svg = """
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="cloudGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#4a5568;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#2d3748;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path fill="url(#cloudGrad)" d="M124,200C124,112,184,40,256,40c64,0,118,54,128,124c60,8,104,64,104,128c0,72-56,128-128,128H124C56,420,0,364,0,296S56,188,124,200z"/>
            <path stroke="#3182ce" stroke-width="8" stroke-linecap="round" d="M160,440l-20,40 M256,440l-20,40 M352,440l-20,40"/>
        </svg>
        """
        return base64.b64encode(svg.encode('utf-8')).decode("utf-8")

# ==============================================================================
# MODULE 3: STATE MANAGEMENT SYSTEM
# ==============================================================================
# A rigorous, object-oriented approach to session state.
# ==============================================================================

@dataclass
class UserSession:
    """DTO for the active user session."""
    page: str = "home"
    theme_mode: str = "Dark" # Default to Dark for beauty
    is_transitioning: bool = False
    wizard_step: int = 0
    inputs: Dict[str, Any] = field(default_factory=dict)
    score: Optional[float] = None
    ai_results: Dict[str, Any] = field(default_factory=dict)

class StateController:
    """
    Singleton controller for Streamlit Session State.
    """
    KEY = "olympus_core_session"

    @staticmethod
    def init():
        """Bootstraps the session if not present."""
        if StateController.KEY not in st.session_state:
            st.session_state[StateController.KEY] = UserSession()
        
        # Sync widget key for theme toggle
        if "theme_toggle_btn" not in st.session_state:
            st.session_state.theme_toggle_btn = True # True = Dark

    @staticmethod
    def get() -> UserSession:
        """Returns the current session object."""
        return st.session_state[StateController.KEY]

    @staticmethod
    def toggle_theme():
        """
        Handles the logic of switching themes.
        Sets a transition flag to trigger the animation.
        """
        session = StateController.get()
        session.is_transitioning = True
        
        if st.session_state.theme_toggle_btn:
            session.theme_mode = "Dark"
        else:
            session.theme_mode = "Light"

    @staticmethod
    def clear_transition():
        """Clears the transition flag."""
        StateController.get().is_transitioning = False

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
# MODULE 4: THE TRIPLE-CORE NEBULA CSS ENGINE
# ==============================================================================
# Generates massive, distinct CSS blocks for Dark and Light modes.
# Includes keyframe animations, glassmorphism, and responsive layouts.
# ==============================================================================

class NebulaEngine:
    
    @staticmethod
    def get_transition_css() -> str:
        """
        Generates the Windows-like transition overlay CSS.
        """
        return """
        <style>
            @keyframes dissolve {
                0% { opacity: 0; backdrop-filter: blur(0px); }
                50% { opacity: 1; backdrop-filter: blur(30px); background: rgba(0,0,0,0.6); }
                100% { opacity: 0; backdrop-filter: blur(0px); }
            }
            .theme-transition-overlay {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                z-index: 999999; pointer-events: none;
                animation: dissolve 0.8s ease-in-out forwards;
            }
        </style>
        <div class="theme-transition-overlay"></div>
        """

    @staticmethod
    def _common_css() -> str:
        """CSS shared between both modes."""
        return """
        /* --- FONT IMPORTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;700&family=JetBrains+Mono:wght@400;700&display=swap');

        /* --- GLOBAL RESET --- */
        .stApp { transition: background 0.5s ease; }
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding-top: 1rem; padding-bottom: 6rem; max-width: 1400px; }
        
        /* --- ANIMATIONS --- */
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
        
        .anim-fade { animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .anim-scale { animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .anim-float { animation: float 6s ease-in-out infinite; }
        """

    @staticmethod
    def _dark_mode_css() -> str:
        """
        THE DARK CORE: Cyberpunk/Space Aesthetic.
        """
        return """
        /* --- DARK MODE VARIABLES --- */
        :root {
            --bg-grad: radial-gradient(circle at 50% 0%, #0f172a 0%, #020617 100%);
            --card-bg: rgba(30, 41, 59, 0.4);
            --card-border: 1px solid rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-primary: #38bdf8;   /* Sky Blue */
            --accent-secondary: #818cf8; /* Indigo */
            --accent-glow: 0 0 25px rgba(56, 189, 248, 0.2);
            --input-bg: rgba(15, 23, 42, 0.6);
            --font-head: 'Outfit', sans-serif;
            --font-body: 'Plus Jakarta Sans', sans-serif;
        }

        .stApp {
            background-image: var(--bg-grad);
            color: var(--text-primary);
        }

        h1, h2, h3, h4 {
            font-family: var(--font-head);
            color: var(--text-primary);
            letter-spacing: -0.5px;
        }

        /* --- OLYMPUS CARD (DARK) --- */
        .olympus-card {
            background: var(--card-bg);
            border: var(--card-border);
            border-radius: 24px;
            padding: 3rem;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            margin-bottom: 2rem;
        }
        .olympus-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent-primary);
            box-shadow: var(--accent-glow);
        }

        /* --- INPUTS (DARK) --- */
        .stTextInput input, .stNumberInput input {
            background: var(--input-bg) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
            padding: 15px !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
        }
        
        /* --- BUTTONS (DARK) --- */
        .stButton button {
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 700 !important;
            letter-spacing: 1px;
            border-radius: 50px !important;
            padding: 0.8rem 2.5rem !important;
            transition: transform 0.2s !important;
        }
        .stButton button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 10px 25px rgba(56, 189, 248, 0.4) !important;
        }
        
        /* --- NAVBAR (DARK) --- */
        .nav-glass {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(30px);
            border-radius: 100px;
            padding: 10px 30px;
            margin-bottom: 40px;
        }
        """

    @staticmethod
    def _light_mode_css() -> str:
        """
        THE LIGHT CORE: Aero/Glass Aesthetic.
        """
        return """
        /* --- LIGHT MODE VARIABLES --- */
        :root {
            --bg-grad: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
            --card-bg: rgba(255, 255, 255, 0.7);
            --card-border: 1px solid rgba(255, 255, 255, 0.9);
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --accent-primary: #2563eb;   /* Royal Blue */
            --accent-secondary: #7c3aed; /* Violet */
            --accent-glow: 0 10px 30px rgba(37, 99, 235, 0.15);
            --input-bg: #ffffff;
            --font-head: 'Outfit', sans-serif;
            --font-body: 'Plus Jakarta Sans', sans-serif;
        }

        .stApp {
            background-image: var(--bg-grad);
            color: var(--text-primary);
        }

        h1, h2, h3, h4 {
            font-family: var(--font-head);
            color: #0f172a;
            letter-spacing: -0.5px;
            font-weight: 800;
        }

        /* --- OLYMPUS CARD (LIGHT) --- */
        .olympus-card {
            background: var(--card-bg);
            border: var(--card-border);
            border-radius: 24px;
            padding: 3rem;
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            margin-bottom: 2rem;
        }
        .olympus-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 30px 60px rgba(37, 99, 235, 0.1);
        }

        /* --- INPUTS (LIGHT) --- */
        .stTextInput input, .stNumberInput input {
            background: #ffffff !important;
            color: #1e293b !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 15px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: var(--accent-primary) !important;
        }
        
        /* --- BUTTONS (LIGHT) --- */
        .stButton button {
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 700 !important;
            letter-spacing: 1px;
            border-radius: 50px !important;
            padding: 0.8rem 2.5rem !important;
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2) !important;
            transition: transform 0.2s !important;
        }
        .stButton button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 15px 30px rgba(37, 99, 235, 0.3) !important;
        }
        
        /* --- NAVBAR (LIGHT) --- */
        .nav-glass {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(20px);
            border-radius: 100px;
            padding: 10px 30px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
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
# MODULE 5: INTELLIGENCE & LOGIC LAYER
# ==============================================================================
# Handles backend processing, scoring algorithms, and AI interactions.
# ==============================================================================

class IntelligenceCore:
    """
    The Brain of Project Olympus.
    """
    
    @staticmethod
    @st.cache_resource
    def load_model():
        try:
            return joblib.load(SystemMetadata.MODEL_FILENAME)
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
# MODULE 6: COMPONENT FACTORY
# ==============================================================================
# Reusable UI widgets that abstract away the HTML/CSS complexity.
# ==============================================================================

class ComponentFactory:
    
    @staticmethod
    def navbar():
        """Renders the top navigation with procedural logo."""
        st.markdown('<div class="nav-glass">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 6, 2], gap="small")
        
        with c1:
            # Generate the SVG logo dynamically based on current theme
            current_theme = StateController.get().theme_mode
            b64_logo = ProceduralAssets.get_logo_svg(current_theme)
            st.markdown(f'<img src="data:image/svg+xml;base64,{b64_logo}" height="40" style="margin-top:5px;">', unsafe_allow_html=True)
        
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
        """Renders a standard Olympus Card."""
        align = "center" if center else "left"
        st.markdown(f"""
        <div class="olympus-card anim-fade" style="text-align: {align};">
            <div style="font-size: 3rem; margin-bottom: 15px;" class="anim-float">{icon}</div>
            <h3>{title}</h3>
            <p style="opacity: 0.8;">{content}</p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def loader_overlay(message: str = "PROCESSING"):
        """Displays the transition overlay with complex spinner."""
        b64_svg = base64.b64encode(IconLibrary.get_loader_svg().encode('utf-8')).decode("utf-8")
        
        spinner_html = f"""
        <style>
            .loader-box {{
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.9); z-index: 10000;
                display: flex; flex-direction: column; justify-content: center; align-items: center;
                backdrop-filter: blur(20px);
            }}
            .text {{
                font-family: 'Outfit'; font-weight: 700; letter-spacing: 3px; color: white; margin-top: 30px;
                animation: pulse 1s infinite;
            }}
            @keyframes pulse {{ 50% {{ opacity: 0.5; }} }}
        </style>
        <div class="loader-box">
            <img src="data:image/svg+xml;base64,{b64_svg}" width="100" height="100">
            <div class="text">{message}...</div>
        </div>
        """
        placeholder = st.empty()
        placeholder.markdown(spinner_html, unsafe_allow_html=True)
        time.sleep(UIConfig.LOADER_DURATION_SEC)
        placeholder.empty()

# ==============================================================================
# MODULE 7: SCENE CONTROLLERS
# ==============================================================================
# The logic for each specific page view.
# ==============================================================================

class SceneHome:
    @staticmethod
    def render():
        st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
        
        # Hero Section with procedural gradient text
        state = StateController.get()
        text_color = "#fff" if state.theme_mode == "Dark" else "#1e293b"
        
        st.markdown(f"""
        <div class="anim-scale" style="text-align: center; margin-bottom: 60px;">
            <h1 style="font-size: 6rem; margin-bottom: 10px; color:{text_color}; line-height:1;">MINDCHECK AI</h1>
            <p style="font-size: 1.5rem; opacity: 0.7; letter-spacing: 2px;">THE APEX OF WELLNESS ANALYTICS</p>
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
            <div class="olympus-card" style="text-align: center; padding: 50px;">
                <div style="font-size: 6rem; margin-bottom: 20px;" class="anim-float">🚀</div>
                <p style="font-size: 1.3rem; line-height: 1.8; margin-bottom: 30px;">
                    "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
                </p>
                <div style="height:2px; width:50px; background:gray; margin: 0 auto 20px auto;"></div>
                <p style="opacity: 0.5; font-size: 0.9rem; font-family:'JetBrains Mono';">TIMESTAMP: 2026-02-06</p>
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
        
        # Container for form stability
        with st.container():
            st.markdown('<div class="olympus-card anim-scale" style="margin-top: 30px;">', unsafe_allow_html=True)
            
            # --- WIZARD LOGIC ---
            if curr == 0: # Profile
                state.inputs['Age'] = st.number_input("Age", 10, 100, state.inputs.get('Age', 15))
                state.inputs['Gender'] = st.selectbox("Gender", ["Male", "Female"], index=0)
                state.inputs['Academic_Level'] = st.selectbox("Education", ["Middle School", "High School", "Undergraduate"])
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("NEXT ➔"): StateController.next_step(); st.rerun()

            elif curr == 1: # Habits
                state.inputs['Platform'] = st.selectbox("Platform", ["TikTok", "YouTube", "Instagram", "Snapchat", "Other"])
                state.inputs['Avg_Daily_Usage_Hours'] = st.number_input("Screen Time (Hrs)", 0.0, 24.0, state.inputs.get('Avg_Daily_Usage_Hours', 4.0))
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): StateController.prev_step(); st.rerun()
                with c2: 
                    if st.button("NEXT ➔"): StateController.next_step(); st.rerun()

            elif curr == 2: # Health
                state.inputs['Sleep'] = st.number_input("Sleep (Hrs)", 0.0, 24.0, state.inputs.get('Sleep', 8.0))
                state.inputs['Addiction'] = st.slider("Addiction Level (1-10)", 1, 10, state.inputs.get('Addiction', 5))
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): StateController.prev_step(); st.rerun()
                with c2: 
                    if st.button("NEXT ➔"): StateController.next_step(); st.rerun()

            elif curr == 3: # Final
                state.inputs['Conflicts'] = st.number_input("Conflicts", 0, 20, state.inputs.get('Conflicts', 0))
                state.inputs['Affects_Performance'] = st.radio("Impacts Grades?", ["No", "Yes"])
                
                st.markdown("<br>", unsafe_allow_html=True)
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
            color = "#00ff88" # Neon Green
            b64_icon = ProceduralAssets.get_star_icon() # THE STAR
            msg = "EXCELLENT CONDITION"
        else:
            color = "#ff4757" # Neon Red
            b64_icon = ProceduralAssets.get_rain_icon() # THE SAD CLOUD
            msg = "ATTENTION REQUIRED"
            
        # Score Card
        st.markdown(f"""
        <div class="olympus-card" style="text-align: center; border-top: 5px solid {color}; padding: 4rem;">
            <div style="width: 150px; height: 150px; margin: 0 auto; animation: float 6s infinite ease-in-out;">
                <img src="data:image/svg+xml;base64,{b64_icon}" width="150" height="150">
            </div>
            <h1 style="font-size: 8rem; color: {color}; margin: 20px 0; text-shadow: 0 0 50px {color}; line-height:1;">{score:.1f}</h1>
            <h3 style="color: {color}; opacity: 0.8; letter-spacing: 5px;">{msg}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Section
        st.markdown("<h2 style='text-align:center; margin: 40px 0;'>AI INSIGHTS</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown('<div class="olympus-card" style="text-align:center; height:100%"><h3>PROFILE</h3><p>Analyze Persona</p></div>', unsafe_allow_html=True)
            if st.button("GENERATE PROFILE", use_container_width=True):
                ComponentFactory.loader_overlay("ANALYZING")
                prompt = f"Data: {json.dumps(state.inputs)}. Return JSON: 'persona', 'analysis', 'tips'."
                res = IntelligenceCore.query_gemini(prompt, is_json=True)
                if res: 
                    state.ai_results['analysis'] = json.loads(res)
                    st.rerun()
                    
        with c2:
            st.markdown('<div class="olympus-card" style="text-align:center; height:100%"><h3>TIME TRAVEL</h3><p>Message from 2029</p></div>', unsafe_allow_html=True)
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
            st.markdown(f"<div class='olympus-card' style='border-left:5px solid {color}'><h3>{r.get('persona')}</h3><p>{r.get('analysis')}</p></div>", unsafe_allow_html=True)
        if 'future' in res:
            st.markdown(f"<div class='olympus-card' style='border-left:5px solid {color}'><h3>TRANSMISSION</h3><p style='font-family:monospace'>{res['future']}</p></div>", unsafe_allow_html=True)
            
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
        st.markdown(NebulaEngine.get_transition_css(), unsafe_allow_html=True)
        time.sleep(0.5) # Allow animation to play
        StateController.clear_transition()
        st.rerun()

    # 3. Inject Theme-Specific CSS
    NebulaEngine.inject(session.theme_mode)
    
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
    st.markdown(f"""
    <div style="text-align: center; margin-top: 80px; padding-top: 20px; border-top: 1px solid rgba(128,128,128,0.2); font-size: 0.8rem; opacity: 0.5;">
        PROJECT OLYMPUS // MINDCHECK AI v{SystemMetadata.VERSION} // {datetime.datetime.now().year}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
