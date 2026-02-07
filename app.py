# ==============================================================================
#   ___  __  __  _____  ___   _
#  / _ \|  \/  ||  ___|/ _ \ / \
# | | | | |\/| || |__ | | | / _ \
# | |_| | |  | ||  __|| |_| / ___ \
#  \___/|_|  |_||_|___ \___/_/   \_\
#      PROJECT OMEGA: MINDCHECK AI
# ==============================================================================
# SYSTEM:       MindCheck AI (Enterprise Singularity Edition)
# VERSION:      6.0.0 (The Final Horizon)
# ARCHITECT:    Mubashir Mohsin & Gemini (Neural Architect)
# ENGINE:       Nebula CSS v10.0 + Streamlit Reactive Core
# DATE:         February 6, 2026
# COPYRIGHT:    (c) 2026 MindCheck Industries. All rights reserved.
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
# MODULE 1: CONSTANTS & ASSET CONFIGURATION
# ==============================================================================
# Defines the immutable constants used throughout the application runtime.
# ==============================================================================

class Assets:
    """Static asset manager for file paths and identifiers."""
    APP_NAME = "MindCheck AI"
    VERSION = "6.0.0"
    AUTHOR = "Mubashir Mohsin"
    FAVICON = "Gemini_Generated_Image_g704tpg704tpg704.png" # User Defined
    LOGO_MAIN = "Gemini_Generated_Image_g704tpg704tpg704.png" # User Defined
    MODEL_FILE = 'mental_health_model.joblib'
    GEMINI_MODEL = 'gemini-2.5-flash'

class UIConfig:
    """Configuration for UI layout constraints."""
    LAYOUT = "wide"
    SIDEBAR_STATE = "collapsed"
    ANIMATION_SPEED = 0.4 # seconds
    LOADER_DURATION = 3.5 # seconds

# Secure API Key Retrieval
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# Initialize Streamlit Page
st.set_page_config(
    page_title=Assets.APP_NAME,
    page_icon=Assets.FAVICON,
    layout=UIConfig.LAYOUT,
    initial_sidebar_state=UIConfig.SIDEBAR_STATE
)

# ==============================================================================
# MODULE 2: THE NEBULA CSS ENGINE (ADVANCED STYLING CORE)
# ==============================================================================
# This class generates the massive CSS block that overrides Streamlit's default
# styling. It implements the "Glassmorphism 3.0" design language.
# ==============================================================================

class NebulaEngine:
    """
    The rendering core for Project Omega.
    Generates dynamic CSS based on the current theme state.
    """

    def __init__(self, theme_mode: str):
        self.theme = theme_mode
        self._init_palettes()

    def _init_palettes(self):
        """Defines the color tokens for Dark (Cyber) and Light (Aero) modes."""
        self.palettes = {
            "Dark": {
                "bg_root": "#050505",
                "bg_gradient": "linear-gradient(180deg, #020024 0%, #090979 0%, #000000 100%)",
                "text_primary": "#ffffff",
                "text_secondary": "rgba(255, 255, 255, 0.6)",
                "accent_primary": "#00f3ff", # Cyan
                "accent_secondary": "#bc13fe", # Neon Purple
                "accent_tertiary": "#00ff88", # Neon Green
                "surface_glass": "rgba(20, 20, 30, 0.5)",
                "surface_border": "rgba(255, 255, 255, 0.1)",
                "surface_hover": "rgba(40, 40, 60, 0.6)",
                "input_bg": "rgba(0, 0, 0, 0.4)",
                "shadow_soft": "0 10px 30px rgba(0,0,0,0.5)",
                "shadow_neon": "0 0 20px rgba(0, 243, 255, 0.3)"
            },
            "Light": {
                "bg_root": "#f0f2f5",
                "bg_gradient": "linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%)",
                "text_primary": "#1a1a1a",
                "text_secondary": "rgba(0, 0, 0, 0.6)",
                "accent_primary": "#2563eb", # Royal Blue
                "accent_secondary": "#7c3aed", # Deep Violet
                "accent_tertiary": "#059669", # Emerald
                "surface_glass": "rgba(255, 255, 255, 0.75)",
                "surface_border": "rgba(255, 255, 255, 0.8)",
                "surface_hover": "rgba(255, 255, 255, 0.9)",
                "input_bg": "rgba(255, 255, 255, 0.6)",
                "shadow_soft": "0 10px 30px rgba(31, 38, 135, 0.15)",
                "shadow_neon": "0 0 20px rgba(37, 99, 235, 0.2)"
            }
        }
        self.c = self.palettes[self.theme]

    def _fonts(self) -> str:
        """Imports Google Fonts."""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Outfit:wght@200;300;400;500;700&family=Share+Tech+Mono&display=swap');
        """

    def _keyframes(self) -> str:
        """Defines complex CSS animations."""
        return """
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(0, 243, 255, 0.4); }
            70% { box-shadow: 0 0 0 15px rgba(0, 243, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 243, 255, 0); }
        }
        @keyframes slideInUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        @keyframes gradient-x {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        @keyframes scanline {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        @keyframes glitch-anim-1 {
            0% { clip: rect(20px, 9999px, 10px, 0); }
            100% { clip: rect(50px, 9999px, 80px, 0); }
        }
        @keyframes scaleIn {
            from { transform: scale(0.9); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        """

    def _core_styles(self) -> str:
        """Base CSS variables and resets."""
        return f"""
        :root {{
            --primary: {self.c['accent_primary']};
            --secondary: {self.c['accent_secondary']};
            --tertiary: {self.c['accent_tertiary']};
            --bg-glass: {self.c['surface_glass']};
            --border-glass: {self.c['surface_border']};
            --text-main: {self.c['text_primary']};
            --text-sub: {self.c['text_secondary']};
            --shadow-soft: {self.c['shadow_soft']};
            --shadow-neon: {self.c['shadow_neon']};
            --font-head: 'Rajdhani', sans-serif;
            --font-body: 'Outfit', sans-serif;
            --font-mono: 'Share Tech Mono', monospace;
        }}

        html, body, [class*="css"] {{
            font-family: var(--font-body);
            color: var(--text-main);
            background: transparent;
        }}

        /* APP CONTAINER BACKGROUND */
        .stApp {{
            background: {self.c['bg_gradient']};
            background-size: 200% 200%;
            animation: gradient-x 15s ease infinite;
        }}

        /* HIDE STREAMLIT CHROME */
        #MainMenu, footer, header {{ visibility: hidden; }}
        .stDeployButton {{ display: none; }}

        /* MAIN CONTENT AREA */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 5rem;
            max-width: 1200px;
        }}
        """

    def _components(self) -> str:
        """Component-specific styling (Cards, Buttons, Inputs)."""
        return f"""
        /* --- OMEGA CARD --- */
        .omega-card {{
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            border-radius: 20px;
            padding: 2.5rem;
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            box-shadow: var(--shadow-soft);
            margin-bottom: 2rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        .omega-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-neon);
            border-color: var(--primary);
        }}
        
        /* --- TYPOGRAPHY --- */
        h1, h2, h3 {{ font-family: var(--font-head); text-transform: uppercase; font-weight: 700; }}
        h1 {{ font-size: 4.5rem; letter-spacing: -2px; line-height: 1; }}
        h2 {{ font-size: 2.5rem; letter-spacing: -1px; }}
        h3 {{ font-size: 1.5rem; letter-spacing: 1px; color: var(--primary); }}
        p {{ font-size: 1.1rem; line-height: 1.7; opacity: 0.9; }}
        
        /* --- INPUT FIELDS --- */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input {{
            background: {self.c['input_bg']} !important;
            border: 1px solid var(--border-glass) !important;
            color: var(--text-main) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            font-family: var(--font-mono) !important;
            transition: 0.3s;
        }}
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 15px var(--primary) !important;
        }}
        
        /* --- BUTTONS --- */
        .stButton > button {{
            background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
            border: none !important;
            color: white !important;
            font-family: var(--font-head) !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            padding: 0.8rem 2rem !important;
            border-radius: 50px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
            width: 100%;
        }}
        .stButton > button:hover {{
            transform: scale(1.02) translateY(-2px) !important;
            box-shadow: 0 0 30px var(--primary) !important;
        }}
        
        /* --- PROGRESS BAR --- */
        .omega-progress-track {{
            width: 100%; height: 6px; background: rgba(128,128,128,0.2);
            border-radius: 10px; margin: 20px 0; overflow: hidden;
        }}
        .omega-progress-fill {{
            height: 100%; background: var(--primary);
            box-shadow: 0 0 10px var(--primary);
            transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1);
        }}
        
        /* --- ANIMATION UTILS --- */
        .anim-enter {{ animation: slideInUp 0.6s ease-out forwards; }}
        .anim-float {{ animation: float 6s ease-in-out infinite; }}
        
        /* --- NAV BAR --- */
        .nav-glass {{
            display: flex; align-items: center; justify-content: space-between;
            background: var(--bg-glass); border: 1px solid var(--border-glass);
            padding: 10px 25px; border-radius: 16px; margin-bottom: 40px;
            backdrop-filter: blur(30px); box-shadow: var(--shadow-soft);
        }}
        
        /* --- LOGO IMAGE STYLING --- */
        .logo-img {{
            max-height: 50px;
            width: auto;
            transition: 0.3s;
        }}
        .logo-img:hover {{ filter: drop-shadow(0 0 10px var(--primary)); }}
        """

    def inject(self):
        """Compiles and injects the CSS payload."""
        full_style = f"""
        <style>
            {self._fonts()}
            {self._keyframes()}
            {self._core_styles()}
            {self._components()}
        </style>
        """
        st.markdown(full_style, unsafe_allow_html=True)

# ==============================================================================
# MODULE 3: OBJECT-ORIENTED STATE MANAGEMENT
# ==============================================================================
# A robust state machine to handle the application flow, data persistence,
# and wizard navigation logic.
# ==============================================================================

@dataclass
class UserSession:
    """Data Transfer Object for the active user session."""
    page: str = "home"
    theme_mode: str = "Dark" # Default to Dark for beauty
    wizard_step: int = 0
    inputs: Dict[str, Any] = field(default_factory=dict)
    score: Optional[float] = None
    ai_insights: Dict[str, Any] = field(default_factory=dict)
    
class StateManager:
    """Singleton controller for Streamlit Session State."""
    
    KEY = "omega_session"

    @staticmethod
    def initialize():
        """Bootstraps the session if not present."""
        if StateManager.KEY not in st.session_state:
            st.session_state[StateManager.KEY] = UserSession()
        
        # Sync widget key for theme toggle
        if "theme_toggle_widget" not in st.session_state:
            st.session_state.theme_toggle_widget = True # True = Dark

    @staticmethod
    def get() -> UserSession:
        return st.session_state[StateManager.KEY]

    @staticmethod
    def set_theme():
        """Callback for theme toggle."""
        session = StateManager.get()
        if st.session_state.theme_toggle_widget:
            session.theme_mode = "Dark"
        else:
            session.theme_mode = "Light"

    @staticmethod
    def route_to(page: str):
        """Navigates to a specific page and resets wizard if needed."""
        session = StateManager.get()
        session.page = page
        if page != "interview":
            session.wizard_step = 0

    @staticmethod
    def wizard_next():
        StateManager.get().wizard_step += 1

    @staticmethod
    def wizard_prev():
        s = StateManager.get()
        if s.wizard_step > 0:
            s.wizard_step -= 1

    @staticmethod
    def reset_system():
        """Hard reset of all assessment data."""
        session = StateManager.get()
        session.page = "interview"
        session.wizard_step = 0
        session.inputs = {}
        session.score = None
        session.ai_insights = {}

# ==============================================================================
# MODULE 4: INTELLIGENCE LAYER (AI & MODEL)
# ==============================================================================
# Handles communication with Gemini and local ML inference.
# ==============================================================================

class IntelligenceCore:
    
    @staticmethod
    @st.cache_resource
    def load_local_model():
        """Loads the .joblib model with error handling."""
        try:
            return joblib.load(Assets.MODEL_FILE)
        except:
            return None # Fail silently, fall back to algorithmic scoring

    @staticmethod
    def query_gemini(prompt: str, is_json: bool = True) -> Any:
        """
        Executes a remote procedure call to Google Gemini.
        Includes timeout protection and JSON parsing.
        """
        if not API_KEY:
            return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{Assets.GEMINI_MODEL}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        if is_json:
            payload["generationConfig"] = {"responseMimeType": "application/json"}
            
        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=20)
            if response.status_code == 200:
                result = response.json()
                text_content = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
                return text_content
        except Exception:
            pass # Graceful degradation
        return None

# ==============================================================================
# MODULE 5: UI COMPONENT LIBRARY
# ==============================================================================
# Reusable UI widgets and layout structures.
# ==============================================================================

class OmegaUI:
    
    @staticmethod
    def navbar():
        """Renders the top navigation bar with Image Logo support."""
        state = StateManager.get()
        
        st.markdown('<div class="nav-glass">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 6, 2], gap="small")
        
        # 1. LOGO SECTION (Left)
        with c1:
            if os.path.exists(Assets.LOGO_MAIN):
                st.image(Assets.LOGO_MAIN, width=120)
            else:
                # Fallback text logo if image missing
                st.markdown('<h3 style="margin:0; font-size:1.2rem;">MINDCHECK AI</h3>', unsafe_allow_html=True)
        
        # 2. HOME ACTION (Center)
        with c2:
            st.markdown('<div style="display:flex; justify-content:center; width:100%;">', unsafe_allow_html=True)
            if st.button("🏠 COMMAND CENTER", key="nav_home_btn"):
                StateManager.route_to("home")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        # 3. THEME TOGGLE (Right)
        with c3:
            st.markdown('<div style="display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
            st.toggle("Dark Mode", value=(state.theme_mode=="Dark"), key="theme_toggle_widget", on_change=StateManager.set_theme)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def loader_animation(text: str = "SYNCHRONIZING"):
        """Displays the 'Singularity' loading animation."""
        html = f"""
        <style>
            .overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center; backdrop-filter: blur(20px); }}
            .orb {{ width: 100px; height: 100px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, #00f3ff, #000); box-shadow: 0 0 50px #00f3ff; animation: pulse-glow 2s infinite; }}
            .text {{ margin-top: 30px; font-family: 'Rajdhani'; color: white; letter-spacing: 5px; animation: blink 1s infinite; }}
            @keyframes blink {{ 50% {{ opacity: 0.5; }} }}
        </style>
        <div class="overlay">
            <div class="orb"></div>
            <div class="text">{text}...</div>
        </div>
        """
        placeholder = st.empty()
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(3)
        placeholder.empty()

# ==============================================================================
# MODULE 6: SCENE CONTROLLERS (PAGE LOGIC)
# ==============================================================================

class SceneHome:
    @staticmethod
    def render():
        state = StateManager.get()
        title_color = "#fff" if state.theme_mode == "Dark" else "#1a1a1a"
        
        st.markdown(f"""
        <div class="anim-enter" style="text-align: center; padding: 5rem 0;">
            <h1 style="color:{title_color}; text-shadow: 0 0 30px rgba(0,243,255,0.3);">
                MINDCHECK<span style="color:#00f3ff">AI</span>
            </h1>
            <p style="font-size: 1.5rem; letter-spacing: 2px; text-transform: uppercase; margin-top: 1rem;">
                Advanced Biometric & Behavioral Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            st.markdown('<div class="anim-enter" style="animation-delay: 0.1s;">', unsafe_allow_html=True)
            st.markdown("""
            <div class="omega-card" style="text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">👨‍💻</div>
                <h3>CREATOR BIO</h3>
                <p>Access the developer profile of Mubashir Mohsin.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ACCESS PROFILE", use_container_width=True):
                StateManager.route_to("about")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="anim-enter" style="animation-delay: 0.2s;">', unsafe_allow_html=True)
            st.markdown("""
            <div class="omega-card" style="text-align: center; border-color: #00f3ff;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">💠</div>
                <h3 style="color: #00f3ff;">SYSTEM CHECK</h3>
                <p>Initialize the step-by-step diagnostic wizard.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("INITIALIZE", type="primary", use_container_width=True):
                StateManager.route_to("interview")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

class SceneAbout:
    @staticmethod
    def render():
        st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; margin-bottom:3rem;">DEVELOPER LOG</h1>', unsafe_allow_html=True)
        
        c_fill_l, c_main, c_fill_r = st.columns([1, 4, 1])
        with c_main:
            st.markdown("""
            <div class="omega-card" style="text-align: center; padding: 4rem;">
                <div style="font-size: 5rem; margin-bottom: 2rem;">🚀</div>
                <p style="font-size: 1.3rem; line-height: 2; margin-bottom: 2rem; font-weight: 300;">
                    "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
                </p>
                <div style="width: 60px; height: 3px; background: #00f3ff; margin: 0 auto 1rem auto;"></div>
                <p style="font-family: 'Share Tech Mono'; opacity: 0.6;">TIMESTAMP: FEB-06-2026</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

class SceneInterview:
    @staticmethod
    def render():
        state = StateManager.get()
        
        # Define Wizard Steps
        STEPS = [
            {"name": "BIOMETRICS", "desc": "Baseline Identification"},
            {"name": "DIGITAL HABITS", "desc": "Usage Pattern Recognition"},
            {"name": "WELLNESS", "desc": "Recovery Metrics"},
            {"name": "IMPACT", "desc": "Social & Cognitive Load"}
        ]
        
        curr = state.wizard_step
        total = len(STEPS)
        step_info = STEPS[curr]
        
        # Progress Bar
        pct = ((curr) / (total - 1)) * 100 if total > 1 else 100
        st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <div class="omega-progress-track">
                <div class="omega-progress-fill" style="width: {pct}%;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; font-family:'Share Tech Mono'; opacity:0.7;">
                <span>SEQUENCE {curr + 1}/{total}</span>
                <span>{step_info['name']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h2 style='text-align:center;'>{step_info['name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; margin-bottom:3rem; opacity:0.6;'>{step_info['desc']}</p>", unsafe_allow_html=True)
        
        # Wizard Form Container
        with st.container():
            st.markdown('<div class="omega-card anim-enter">', unsafe_allow_html=True)
            
            # --- STEP 0: BIO ---
            if curr == 0:
                state.inputs['Age'] = st.number_input("Subject Age", 10, 100, state.inputs.get('Age', 15))
                state.inputs['Gender'] = st.selectbox("Gender Identity", ["Male", "Female"], index=0)
                state.inputs['Academic_Level'] = st.selectbox("Education Tier", ["Middle School", "High School", "Undergraduate", "Graduate"])
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("NEXT SEQUENCE ➔"): StateManager.wizard_next(); st.rerun()

            # --- STEP 1: HABITS ---
            elif curr == 1:
                state.inputs['Platform'] = st.selectbox("Primary Network", ["TikTok", "YouTube", "Instagram", "Snapchat", "Other"])
                state.inputs['Avg_Daily_Usage_Hours'] = st.number_input("Daily Exposure (Hours)", 0.0, 24.0, state.inputs.get('Avg_Daily_Usage_Hours', 4.0))
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): StateManager.wizard_prev(); st.rerun()
                with c2: 
                    if st.button("NEXT SEQUENCE ➔"): StateManager.wizard_next(); st.rerun()

            # --- STEP 2: WELLNESS ---
            elif curr == 2:
                state.inputs['Sleep'] = st.number_input("Sleep Cycles (Hours)", 0.0, 24.0, state.inputs.get('Sleep', 8.0))
                st.markdown("<label>Dependency Index (1-10)</label>", unsafe_allow_html=True)
                state.inputs['Addiction'] = st.slider("", 1, 10, state.inputs.get('Addiction', 5))
                state.inputs['Relationship'] = st.selectbox("Relationship Status", ["Single", "Complicated", "Partnered"])
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): StateManager.wizard_prev(); st.rerun()
                with c2: 
                    if st.button("NEXT SEQUENCE ➔"): StateManager.wizard_next(); st.rerun()

            # --- STEP 3: IMPACT ---
            elif curr == 3:
                state.inputs['Conflicts'] = st.number_input("Real-world Conflicts (Weekly)", 0, 20, state.inputs.get('Conflicts', 0))
                st.markdown("<label>Academic Performance Degradation?</label>", unsafe_allow_html=True)
                state.inputs['Affects_Performance'] = st.radio("", ["No", "Yes"], horizontal=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): StateManager.wizard_prev(); st.rerun()
                with c2: 
                    if st.button("PROCESS DATA 🚀"):
                        OmegaUI.loader_animation("COMPILING NEURAL NET")
                        
                        # Calculation Logic
                        data = state.inputs
                        base = 10.0
                        base -= (data['Avg_Daily_Usage_Hours'] * 0.35)
                        base -= (data['Addiction'] * 0.25)
                        base += (data['Sleep'] * 0.15)
                        if data['Affects_Performance'] == "Yes": base -= 1.0
                        
                        state.score = max(1.0, min(10.0, base))
                        StateManager.route_to("results")
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

class SceneResults:
    @staticmethod
    def render():
        state = StateManager.get()
        score = state.score
        
        # Color Logic
        if score < 5: 
            color = "#ff0055"
            status = "CRITICAL FAILURE"
        elif score < 7.5: 
            color = "#ffaa00"
            status = "SYSTEM UNSTABLE"
        else: 
            color = "#00ffaa"
            status = "SYSTEM OPTIMAL"
            
        st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
        
        # 1. Header Card
        st.markdown(f"""
        <div class="omega-card" style="border-left: 5px solid {color}; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-family: 'Share Tech Mono'; opacity: 0.6;">REF ID: {random.randint(9999,99999)}</span>
                <h3 style="margin:0;">DIAGNOSTIC REPORT</h3>
            </div>
            <div style="text-align: right;">
                <span style="opacity: 0.6;">STATUS</span><br>
                <b style="color: {color};">{status}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Score Card
        st.markdown(f"""
        <div class="omega-card" style="text-align: center; padding: 4rem; border-color: {color};">
            <h4 style="letter-spacing: 5px; opacity: 0.6; margin-bottom: 1rem;">WELLNESS INDEX</h4>
            <h1 style="font-size: 8rem; margin: 0; color: {color}; text-shadow: 0 0 40px {color}; line-height: 1;">
                {score:.1f}
            </h1>
            <p style="font-family: 'Share Tech Mono'; font-size: 1.2rem; margin-top: 10px;">/ 10.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. AI Insights Grid
        st.markdown("<h2 style='text-align:center; margin: 4rem 0 2rem 0;'>GENERATIVE INSIGHTS</h2>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2, gap="medium")
        
        # Feature A: Persona
        with c1:
            st.markdown("""
            <div class="omega-card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3>Psychometric Profile</h3>
                <p>Generate behavioral archetype.</p>
                <div style="margin-top:20px;"></div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("GENERATE PROFILE", use_container_width=True):
                OmegaUI.loader_animation("ANALYZING PATTERNS")
                prompt = f"Data: {json.dumps(state.inputs)}. Return JSON: 'persona', 'analysis', 'tips'."
                res = IntelligenceCore.query_gemini(prompt, is_json=True)
                if res: 
                    state.ai_insights['analysis'] = json.loads(res)
                    st.rerun()

        # Feature B: Time Travel
        with c2:
            st.markdown("""
            <div class="omega-card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⏳</div>
                <h3>Temporal Bridge</h3>
                <p>Incoming message from 2029.</p>
                <div style="margin-top:20px;"></div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("CONNECT TIMELINE", use_container_width=True):
                OmegaUI.loader_animation("ESTABLISHING LINK")
                prompt = f"Message from 2029 for user: {json.dumps(state.inputs)}. Max 50 words."
                res = IntelligenceCore.query_gemini(prompt, is_json=False)
                if res: 
                    state.ai_insights['future'] = res
                    st.rerun()
                    
        # 4. Display Results
        results = state.ai_insights
        
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="omega-card" style="border-left: 5px solid #00f3ff; margin-top: 2rem;">
                <span style="font-family: 'Share Tech Mono'; color: #00f3ff;">ARCHETYPE IDENTIFIED</span>
                <h2 style="color: #00f3ff;">{r.get('persona', 'Unknown')}</h2>
                <p style="font-style: italic; opacity: 0.8; font-size: 1.1rem; margin-bottom: 1.5rem;">"{r.get('analysis')}"</p>
                <ul style="margin-top: 1rem; line-height: 1.8;">
                    {''.join([f'<li>{t}</li>' for t in r.get('tips', [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        if 'future' in results:
            st.markdown(f"""
            <div class="omega-card" style="border-left: 5px solid #bc13fe; background: rgba(0,0,0,0.3); margin-top: 2rem;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <span style="background: #bc13fe; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-family:'Share Tech Mono';">ENCRYPTED</span>
                    <h3 style="color: #bc13fe; margin: 0;">Transmission 2029</h3>
                </div>
                <p style="font-family: 'Share Tech Mono'; color: white; font-size: 1rem; line-height: 1.6;">
                    > {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("RESTART SYSTEM", use_container_width=True):
            StateManager.reset_system()
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 8: MAIN EXECUTION THREAD
# ==============================================================================

def main():
    # 1. Init Session
    StateManager.initialize()
    
    # 2. Inject CSS Engine
    css = NebulaEngine(StateManager.get().theme_mode)
    css.inject()
    
    # 3. Render Navbar
    OmegaUI.navbar()
    
    # 4. Route
    page = StateManager.get().page
    
    if page == "home":
        SceneHome.render()
    elif page == "about":
        SceneAbout.render()
    elif page == "interview":
        SceneInterview.render()
    elif page == "results":
        SceneResults.render()
        
    # 5. Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 80px; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.1); font-family: 'Share Tech Mono'; font-size: 0.8rem; opacity: 0.5;">
        MINDCHECK AI v6.0 // AETHER OS // 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
