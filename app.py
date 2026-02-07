# ==============================================================================
# PROJECT: MINDCHECK AI - AETHER OS EDITION (ULTIMATE BUILD)
# ==============================================================================
# AUTHOR: Mubashir Mohsin & Gemini (AI Architect)
# VERSION: 5.0.1 (Stable Release)
# DATE: 2026-02-06
# ENGINE: Hyper-CSS v9.0 + Streamlit Custom Components
# DESCRIPTION: A quantum-leap in UI/UX design for mental health analytics.
#              Features a dedicated CSS engine, object-oriented state management,
#              and a step-by-step wizard interface.
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
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# ==============================================================================
# PART 1: SYSTEM CONFIGURATION & CONSTANTS
# ==============================================================================
SYSTEM_CONFIG = {
    "APP_NAME": "MindCheck AI",
    "VERSION": "5.0.0",
    "ICON": "🧠",
    "AUTHOR": "Mubashir Mohsin",
    "MODEL_FILE": 'mental_health_model.joblib',
    "GEMINI_MODEL": 'gemini-2.5-flash'
}

# Initialize Streamlit Page Configuration
st.set_page_config(
    page_title=SYSTEM_CONFIG["APP_NAME"],
    page_icon=SYSTEM_CONFIG["ICON"],
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Secure API Key Retrieval
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ==============================================================================
# PART 2: THE "HYPER-CSS" ENGINE
# ==============================================================================
# This class is responsible for generating the massive CSS block that powers
# the visual aesthetics of the application. It handles variables, animations,
# and component styling.
# ==============================================================================

class HyperCSSEngine:
    """
    The core visual engine. Generates dynamic CSS based on theme state.
    Contains extensive keyframe animations and glassmorphism logic.
    """

    def __init__(self, theme_mode: str):
        self.theme = theme_mode
        self.palettes = {
            "Dark": {
                "bg_base": "#030014",
                "bg_gradient": "radial-gradient(circle at 50% 50%, #1a1a2e 0%, #000000 100%)",
                "primary": "#00f3ff",     # Neon Cyan
                "secondary": "#bd00ff",   # Neon Purple
                "accent": "#00ff9d",      # Neon Green
                "surface": "rgba(20, 20, 30, 0.4)",
                "surface_border": "rgba(255, 255, 255, 0.08)",
                "text_main": "#ffffff",
                "text_dim": "rgba(255, 255, 255, 0.6)",
                "glass_blur": "25px",
                "shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.8)",
                "input_bg": "rgba(0, 0, 0, 0.3)"
            },
            "Light": {
                "bg_base": "#f8f9fa",
                "bg_gradient": "linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)",
                "primary": "#2563eb",     # Royal Blue
                "secondary": "#7c3aed",   # Deep Violet
                "accent": "#059669",      # Emerald
                "surface": "rgba(255, 255, 255, 0.65)",
                "surface_border": "rgba(255, 255, 255, 0.4)",
                "text_main": "#1e293b",
                "text_dim": "rgba(30, 41, 59, 0.6)",
                "glass_blur": "20px",
                "shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.1)",
                "input_bg": "rgba(255, 255, 255, 0.8)"
            }
        }
        self.c = self.palettes[self.theme]

    def _generate_animations(self) -> str:
        """Generates complex CSS keyframes."""
        return """
        /* 1. FADE IN UP */
        @keyframes fadeInUp {
            0% { opacity: 0; transform: translate3d(0, 40px, 0); }
            100% { opacity: 1; transform: translate3d(0, 0, 0); }
        }

        /* 2. ORBITAL ROTATION (For Loader) */
        @keyframes orbit {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* 3. NEON PULSE */
        @keyframes neonPulse {
            0% { box-shadow: 0 0 5px var(--primary), 0 0 10px var(--primary); }
            50% { box-shadow: 0 0 20px var(--primary), 0 0 40px var(--primary); }
            100% { box-shadow: 0 0 5px var(--primary), 0 0 10px var(--primary); }
        }

        /* 4. FLOAT EFFECT */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
            100% { transform: translateY(0px); }
        }

        /* 5. GLITCH TEXT EFFECT */
        @keyframes glitch {
            2%, 64% { transform: translate(2px,0) skew(0deg); }
            4%, 60% { transform: translate(-2px,0) skew(0deg); }
            62% { transform: translate(0,0) skew(5deg); }
        }

        /* 6. GRADIENT SHIFT */
        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 7. PROGRESS BAR FILL */
        @keyframes fillProgress {
            from { width: 0%; }
            to { width: var(--progress-width); }
        }
        """

    def _generate_typography(self) -> str:
        """Sets up the font stack."""
        return f"""
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;700&display=swap');
        
        :root {{
            --font-display: 'Syncopate', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-code: 'JetBrains Mono', monospace;
        }}
        
        h1, h2, h3, h4 {{ font-family: var(--font-display); text-transform: uppercase; letter-spacing: 2px; }}
        p, label, li, span, div {{ font-family: var(--font-body); }}
        code {{ font-family: var(--font-code); }}
        """

    def _generate_core_styles(self) -> str:
        """Defines the core variables and reset styles."""
        return f"""
        :root {{
            --primary: {self.c['primary']};
            --secondary: {self.c['secondary']};
            --accent: {self.c['accent']};
            --bg-base: {self.c['bg_base']};
            --surface: {self.c['surface']};
            --surface-border: {self.c['surface_border']};
            --text-main: {self.c['text_main']};
            --text-dim: {self.c['text_dim']};
            --glass-blur: {self.c['glass_blur']};
            --shadow: {self.c['shadow']};
            --input-bg: {self.c['input_bg']};
        }}

        .stApp {{
            background: {self.c['bg_gradient']};
            background-attachment: fixed;
            background-size: cover;
        }}

        /* Clean Streamlit UI */
        #MainMenu {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        .stDeployButton {{ display: none; }}
        
        .block-container {{
            padding-top: 3rem;
            padding-bottom: 6rem;
            max-width: 1100px;
        }}
        """

    def _generate_component_styles(self) -> str:
        """Detailed styling for Cards, Inputs, Buttons."""
        return """
        /* --- AETHER CARD SYSTEM --- */
        .aether-card {
            background: var(--surface);
            border: 1px solid var(--surface-border);
            border-radius: 24px;
            padding: 3rem;
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
            z-index: 1;
        }

        .aether-card:hover {
            transform: translateY(-8px) scale(1.01);
            border-color: var(--primary);
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }

        .aether-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.03), transparent);
            transform: translateX(-100%);
            transition: 0.5s;
            z-index: -1;
        }

        .aether-card:hover::before {
            transform: translateX(100%);
        }

        /* --- NEON INPUT FIELDS --- */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background: var(--input-bg) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--surface-border) !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            font-family: var(--font-body) !important;
            transition: all 0.3s ease !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 15px var(--primary) !important;
            transform: scale(1.01);
        }

        .stSelectbox > div > div > div {
            background: var(--input-bg) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--surface-border) !important;
            border-radius: 12px !important;
        }
        
        div[data-baseweb="popover"], div[data-baseweb="menu"] {
            background: var(--bg-base) !important;
            border: 1px solid var(--surface-border) !important;
        }
        
        div[role="option"] {
            color: var(--text-main) !important;
        }

        /* --- LIQUID METAL BUTTONS --- */
        .stButton > button {
            background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
            background-size: 200% 200% !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.8rem 2.5rem !important;
            font-family: var(--font-display) !important;
            font-size: 0.9rem !important;
            font-weight: 700 !important;
            letter-spacing: 2px !important;
            transition: all 0.4s ease !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
            animation: gradientFlow 3s ease infinite;
        }

        .stButton > button:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 0 30px var(--primary) !important;
        }

        /* --- NAV BAR --- */
        .nav-wrapper {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--surface);
            padding: 15px 40px;
            border-radius: 100px;
            border: 1px solid var(--surface-border);
            margin-bottom: 50px;
            backdrop-filter: blur(var(--glass-blur));
        }

        .nav-logo {
            font-family: var(--font-display);
            font-weight: 700;
            font-size: 1.2rem;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* --- WIZARD PROGRESS --- */
        .progress-track {
            width: 100%;
            height: 4px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            margin-bottom: 2rem;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: var(--primary);
            box-shadow: 0 0 10px var(--primary);
            transition: width 0.5s ease-in-out;
        }

        /* --- ANIMATION CLASSES --- */
        .anim-fade-up { animation: fadeInUp 0.8s ease-out forwards; }
        .anim-float { animation: float 6s ease-in-out infinite; }
        .anim-glitch:hover { animation: glitch 0.3s cubic-bezier(.25, .46, .45, .94) both infinite; }

        /* --- FOOTER --- */
        .footer-text {
            text-align: center;
            margin-top: 100px;
            color: var(--text-dim);
            font-family: var(--font-code);
            font-size: 0.8rem;
            letter-spacing: 1px;
            border-top: 1px solid var(--surface-border);
            padding-top: 30px;
        }
        """

    def inject(self):
        """Combines all CSS parts and injects into Streamlit."""
        full_css = f"""
        <style>
            {self._generate_typography()}
            {self._generate_animations()}
            {self._generate_core_styles()}
            {self._generate_component_styles()}
        </style>
        """
        st.markdown(full_css, unsafe_allow_html=True)


# ==============================================================================
# PART 3: OBJECT-ORIENTED STATE MANAGEMENT
# ==============================================================================
# Handles all session data, persistent variables, and wizard flow logic.
# ==============================================================================

@dataclass
class AppState:
    page: str = "home"
    theme_mode: str = "Light"
    theme_toggle: bool = False
    score: Optional[float] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    ai_results: Dict[str, Any] = field(default_factory=dict)
    wizard_step: int = 0

class SessionManager:
    """Singleton-like class to manage Streamlit session state."""
    
    @staticmethod
    def initialize():
        if "app_state" not in st.session_state:
            st.session_state.app_state = AppState()
        
        # Sync simple session state keys for widgets
        if "theme_toggle" not in st.session_state:
            st.session_state.theme_toggle = False

    @staticmethod
    def get() -> AppState:
        return st.session_state.app_state

    @staticmethod
    def toggle_theme():
        state = SessionManager.get()
        # Toggle logic based on widget state
        if st.session_state.theme_toggle:
            state.theme_mode = "Dark"
        else:
            state.theme_mode = "Light"

    @staticmethod
    def navigate(page: str):
        state = SessionManager.get()
        state.page = page
        state.wizard_step = 0 # Reset wizard on new navigation
        # Force re-run logic handles automatically in Streamlit

    @staticmethod
    def reset_data():
        state = SessionManager.get()
        state.page = "interview"
        state.wizard_step = 0
        state.inputs = {}
        state.score = None
        state.ai_results = {}

    @staticmethod
    def wizard_next():
        state = SessionManager.get()
        state.wizard_step += 1

    @staticmethod
    def wizard_prev():
        state = SessionManager.get()
        if state.wizard_step > 0:
            state.wizard_step -= 1

    @staticmethod
    def update_input(key: str, value: Any):
        state = SessionManager.get()
        state.inputs[key] = value

# ==============================================================================
# PART 4: BACKEND LOGIC & AI INTEGRATION
# ==============================================================================
# Handles ML Model loading and Gemini API communication.
# ==============================================================================

class LogicEngine:
    
    @staticmethod
    @st.cache_resource
    def load_model():
        try:
            return joblib.load(SYSTEM_CONFIG["MODEL_FILE"])
        except Exception:
            return None

    @staticmethod
    def calculate_fallback_score(data: Dict[str, Any]) -> float:
        """
        Calculates score if ML model fails.
        Algorithm: Base 10 - Penalties + Sleep Bonus
        """
        usage = data.get('Avg_Daily_Usage_Hours', 4.0)
        addiction = data.get('Addiction', 5.0)
        sleep = data.get('Sleep', 8.0)
        
        score = 10.0
        score -= (usage * 0.35)
        score -= (addiction * 0.25)
        score += (sleep * 0.1) # Small bonus for good sleep
        
        # Clamp between 1.0 and 10.0
        return max(1.0, min(10.0, score))

    @staticmethod
    def call_gemini(prompt: str, is_json: bool = True) -> Any:
        if not API_KEY:
            return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{SYSTEM_CONFIG['GEMINI_MODEL']}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        if is_json:
            payload["generationConfig"] = {"responseMimeType": "application/json"}
            
        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=25)
            if response.status_code == 200:
                text = response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
                return text
        except Exception as e:
            # Silent failure in prod, or st.error(e) in dev
            pass
        return None

# ==============================================================================
# PART 5: UI COMPONENT LIBRARY
# ==============================================================================
# Specialized functions to render specific HTML/CSS structures.
# ==============================================================================

class UIComponents:
    
    @staticmethod
    def navbar():
        state = SessionManager.get()
        st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3, 6, 2], gap="small")
        
        with c1:
            st.markdown('<div class="nav-logo">AETHER OS // MINDCHECK</div>', unsafe_allow_html=True)
        
        with c2:
            st.markdown('<div style="display:flex; justify-content:center; width:100%">', unsafe_allow_html=True)
            if st.button("HOME DASHBOARD", key="nav_home"):
                SessionManager.navigate("home")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c3:
            st.markdown('<div style="display:flex; justify-content:flex-end">', unsafe_allow_html=True)
            is_dark = (state.theme_mode == "Dark")
            st.toggle("Night Mode", value=is_dark, key="theme_toggle", on_change=SessionManager.toggle_theme)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def loader(text: str = "INITIALIZING NEURAL LINK"):
        """
        The requested EYE-CATCHING loading sign.
        Uses complex CSS geometry (rotating rings).
        """
        loader_html = f"""
        <style>
            .loader-overlay {{
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.9); z-index: 10000;
                backdrop-filter: blur(30px);
                display: flex; flex-direction: column;
                justify-content: center; align-items: center;
            }}
            
            .singularity {{
                position: relative; width: 150px; height: 150px;
                perspective: 1000px; transform-style: preserve-3d;
            }}
            
            .ring {{
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%;
                border: 4px solid transparent;
                border-top-color: #00f3ff;
                border-bottom-color: #bd00ff;
                animation: orbit 2s linear infinite;
            }}
            
            .ring:nth-child(2) {{
                width: 70%; height: 70%; top: 15%; left: 15%;
                border-top-color: #00ff9d; border-bottom-color: #ffffff;
                animation-direction: reverse;
                animation-duration: 3s;
            }}
            
            .ring:nth-child(3) {{
                width: 40%; height: 40%; top: 30%; left: 30%;
                border-top-color: #ff0055; border-bottom-color: #ffff00;
                animation-duration: 1.5s;
            }}
            
            .core {{
                position: absolute; top: 50%; left: 50%;
                width: 10px; height: 10px; background: white;
                border-radius: 50%;
                transform: translate(-50%, -50%);
                box-shadow: 0 0 20px white;
                animation: neonPulse 1s ease-in-out infinite;
            }}
            
            .loading-text {{
                margin-top: 50px;
                font-family: 'Syncopate', sans-serif;
                color: white; letter-spacing: 4px; font-size: 1.2rem;
                text-transform: uppercase;
                animation: glitch 2s infinite;
            }}
        </style>
        <div class="loader-overlay">
            <div class="singularity">
                <div class="ring"></div>
                <div class="ring"></div>
                <div class="ring"></div>
                <div class="core"></div>
            </div>
            <div class="loading-text">{text}...</div>
        </div>
        """
        placeholder = st.empty()
        placeholder.markdown(loader_html, unsafe_allow_html=True)
        time.sleep(4) # 4 seconds to admire the animation
        placeholder.empty()

    @staticmethod
    def card(content: str, center: bool = False):
        align = "center" if center else "left"
        st.markdown(f"""
        <div class="aether-card anim-fade-up" style="text-align: {align};">
            {content}
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PART 6: PAGE CONTROLLERS (SCENES)
# ==============================================================================
# Each function represents a "Scene" or "Page" in the app.
# ==============================================================================

class SceneController:

    @staticmethod
    def render_home():
        state = SessionManager.get()
        
        # Hero Section
        title_color = "#ffffff" if state.theme_mode == "Dark" else "#1e293b"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 6rem 0; position: relative;">
            <h1 style="font-size: 7rem; line-height: 0.9; margin-bottom: 2rem; color: {title_color}; letter-spacing: -5px;" class="anim-glitch">
                MINDCHECK<br><span style="color:var(--primary);">AI</span>
            </h1>
            <p style="font-size: 1.5rem; max-width: 800px; margin: 0 auto; opacity: 0.8; font-weight: 300;">
                THE QUANTUM-ENHANCED DIGITAL WELLNESS SYSTEM
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 2-Column High-Impact Grid
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            st.markdown('<div class="anim-fade-up" style="animation-delay: 0.1s;">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="aether-card" style="text-align: center; padding: 4rem;">
                <div style="font-size: 5rem; margin-bottom: 1.5rem;" class="anim-float">👨‍🚀</div>
                <h3>About the Creator</h3>
                <p style="margin-bottom: 2rem;">Meet Mubashir Mohsin and the origin story.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ACCESS BIO", use_container_width=True):
                SessionManager.navigate("about")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="anim-fade-up" style="animation-delay: 0.2s;">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="aether-card" style="text-align: center; padding: 4rem; border-color: var(--primary);">
                <div style="font-size: 5rem; margin-bottom: 1.5rem;" class="anim-float">🔮</div>
                <h3 style="color: var(--primary);">Start Check-In</h3>
                <p style="margin-bottom: 2rem;">Initiate the step-by-step diagnostic wizard.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("INITIALIZE WIZARD", type="primary", use_container_width=True):
                SessionManager.navigate("interview")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_about():
        st.markdown('<div class="anim-fade-up">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; margin-bottom:3rem;">ORIGIN STORY</h1>', unsafe_allow_html=True)
        
        c_spacer_l, c_main, c_spacer_r = st.columns([1, 4, 1])
        with c_main:
            st.markdown(f"""
            <div class="aether-card" style="text-align: center; padding: 4rem;">
                <div style="font-size: 6rem; margin-bottom: 2rem;">🚀</div>
                <p style="font-size: 1.4rem; line-height: 2; margin-bottom: 3rem; font-weight: 300;">
                    "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
                </p>
                <div style="width: 100px; height: 2px; background: var(--primary); margin: 0 auto 1.5rem auto;"></div>
                <p style="font-family: 'JetBrains Mono'; opacity: 0.6; font-size: 0.9rem;">
                    LOG DATE: FEBRUARY 6, 2026
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_interview():
        state = SessionManager.get()
        
        # Wizard Configuration
        STEPS = [
            {"title": "BIOMETRICS", "subtitle": "Let's establish your baseline."},
            {"title": "DIGITAL FOOTPRINT", "subtitle": "Analyzing your connectivity habits."},
            {"title": "WELLNESS METRICS", "subtitle": "Measuring recovery and balance."},
            {"title": "IMPACT ANALYSIS", "subtitle": "Assessing cognitive and social load."}
        ]
        
        current_idx = state.wizard_step
        total_steps = len(STEPS)
        current_step_data = STEPS[current_idx]
        
        # Progress Bar Visualization
        progress_pct = ((current_idx) / (total_steps - 1)) * 100 if total_steps > 1 else 100
        
        st.markdown(f"""
        <div style="margin-bottom: 3rem;">
            <div class="progress-track">
                <div class="progress-fill" style="width: {progress_pct}%;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:10px; font-family:'JetBrains Mono'; font-size:0.8rem; opacity:0.7;">
                <span>STEP {current_idx + 1} / {total_steps}</span>
                <span>{current_step_data['title']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h2 style='text-align:center;'>{current_step_data['title']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; opacity:0.6; margin-bottom:2rem;'>{current_step_data['subtitle']}</p>", unsafe_allow_html=True)
        
        # Container for inputs to keep layout stable
        with st.container():
            st.markdown('<div class="aether-card anim-fade-up">', unsafe_allow_html=True)
            
            # --- WIZARD STEP 0: BIOMETRICS ---
            if current_idx == 0:
                state.inputs['Age'] = st.number_input(
                    "Age", 
                    min_value=10, max_value=100, 
                    value=state.inputs.get('Age', 15)
                )
                state.inputs['Gender'] = st.selectbox(
                    "Gender Identity", 
                    ["Male", "Female"], 
                    index=0 if state.inputs.get('Gender') == "Male" else 1
                )
                state.inputs['Academic_Level'] = st.selectbox(
                    "Education Level", 
                    ["Middle School", "High School", "Undergraduate", "Graduate"],
                    index=0
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("CONTINUE TO DIGITAL FOOTPRINT ➔"):
                    SessionManager.wizard_next()
                    st.rerun()

            # --- WIZARD STEP 1: DIGITAL FOOTPRINT ---
            elif current_idx == 1:
                state.inputs['Platform'] = st.selectbox(
                    "Dominant Platform", 
                    ["TikTok", "YouTube", "Instagram", "Snapchat", "Twitter", "Facebook", "Other"],
                    index=0
                )
                state.inputs['Avg_Daily_Usage_Hours'] = st.number_input(
                    "Daily Screen Time (Hours)", 
                    0.0, 24.0, 
                    state.inputs.get('Avg_Daily_Usage_Hours', 4.0), 
                    0.5
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): 
                        SessionManager.wizard_prev()
                        st.rerun()
                with c2: 
                    if st.button("CONTINUE TO WELLNESS ➔"): 
                        SessionManager.wizard_next()
                        st.rerun()

            # --- WIZARD STEP 2: WELLNESS ---
            elif current_idx == 2:
                state.inputs['Sleep'] = st.number_input(
                    "Average Sleep (Hours/Night)", 
                    0.0, 24.0, 
                    state.inputs.get('Sleep', 8.0), 
                    0.5
                )
                
                st.markdown("<label>Self-Perceived Addiction Level (1-10)</label>", unsafe_allow_html=True)
                state.inputs['Addiction'] = st.slider(
                    "", 
                    1, 10, 
                    state.inputs.get('Addiction', 5)
                )
                
                state.inputs['Relationship'] = st.selectbox(
                    "Relationship Status",
                    ["Single", "In a Relationship", "Complicated"]
                )

                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): 
                        SessionManager.wizard_prev()
                        st.rerun()
                with c2: 
                    if st.button("CONTINUE TO IMPACT ➔"): 
                        SessionManager.wizard_next()
                        st.rerun()

            # --- WIZARD STEP 3: IMPACT (FINAL) ---
            elif current_idx == 3:
                state.inputs['Conflicts'] = st.number_input(
                    "Weekly Offline Conflicts", 
                    0, 20, 
                    state.inputs.get('Conflicts', 0)
                )
                
                st.markdown("<label>Does usage impact academic grades?</label>", unsafe_allow_html=True)
                state.inputs['Affects_Performance'] = st.radio(
                    "", 
                    ["No", "Yes"], 
                    horizontal=True
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): 
                        SessionManager.wizard_prev()
                        st.rerun()
                with c2: 
                    if st.button("INITIATE SYSTEM ANALYSIS 🚀"):
                        UIComponents.loader("PROCESSING NEURAL PATHWAYS")
                        
                        # Calculate Score Logic
                        data = state.inputs
                        base_score = 10.0
                        base_score -= (data['Avg_Daily_Usage_Hours'] * 0.35)
                        base_score -= (data['Addiction'] * 0.25)
                        base_score += (data['Sleep'] * 0.15)
                        if data['Affects_Performance'] == "Yes":
                            base_score -= 1.0
                        
                        state.score = max(1.0, min(10.0, base_score))
                        SessionManager.navigate("results")
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_results():
        state = SessionManager.get()
        score = state.score
        data = state.inputs
        
        # Dynamic Coloring
        if score < 5:
            color = "#ff0055"
            msg = "CRITICAL: DETOX REQUIRED"
        elif score < 7.5:
            color = "#ffaa00"
            msg = "WARNING: BALANCE NEEDED"
        else:
            color = "#00ffaa"
            msg = "OPTIMAL: HEALTHY HABITS"
            
        st.markdown('<div class="anim-fade-up">', unsafe_allow_html=True)
        
        # Result Header
        st.markdown(f"""
        <div class="aether-card" style="border-left: 5px solid {color}; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-family: var(--font-code); opacity: 0.6;">ANALYSIS ID: {random.randint(10000,99999)}</span>
                <h3 style="margin:0;">DIAGNOSTIC COMPLETE</h3>
            </div>
            <div style="text-align: right;">
                <span style="opacity: 0.6;">PLATFORM</span><br>
                <b>{data.get('Platform')}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Score Visualization
        st.markdown(f"""
        <div class="aether-card" style="text-align: center; padding: 4rem; position: relative; border-color: {color};">
            <div style="position: absolute; top:0; left:0; width:100%; height:6px; background: {color}; box-shadow: 0 0 20px {color};"></div>
            <h4 style="letter-spacing: 5px; opacity: 0.7;">WELLNESS INDEX</h4>
            <h1 style="font-size: 8rem; margin: 0; color: {color}; text-shadow: 0 0 50px {color}; line-height: 1.1;">
                {score:.1f}
            </h1>
            <p style="font-family: var(--font-code); font-size: 1.2rem; margin-top: 10px;">/ 10.0</p>
            <div style="margin-top: 2rem; display: inline-block; padding: 10px 30px; border: 1px solid {color}; border-radius: 50px; color: {color}; font-weight: 700;">
                {msg}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Grid
        st.markdown("<h2 style='text-align:center; margin: 4rem 0 2rem 0;'>GENERATIVE INSIGHTS</h2>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2, gap="medium")
        
        # Persona Logic
        with c1:
            st.markdown(f"""
            <div class="aether-card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3>Psycho-Metric Persona</h3>
                <p>Generate a behavioral archetype profile.</p>
                <div style="margin-top: 2rem;"></div>
            </div>
            """, unsafe_allow_html=True)
            # We place button outside card to avoid nesting issues in Streamlit
            if st.button("GENERATE PERSONA", use_container_width=True):
                UIComponents.loader("ANALYZING BEHAVIOR PATTERNS")
                prompt = f"Based on user data: {json.dumps(data)}. Return JSON with keys: 'persona' (2-3 words title), 'analysis' (1 sentence), 'tips' (Array of 2 short tips)."
                res = LogicEngine.call_gemini(prompt)
                if res: 
                    state.ai_results['analysis'] = json.loads(res)
                    st.rerun()

        # Time Travel Logic
        with c2:
            st.markdown(f"""
            <div class="aether-card" style="text-align: center; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⏳</div>
                <h3>Temporal Bridge</h3>
                <p>Receive a transmission from your 2029 self.</p>
                <div style="margin-top: 2rem;"></div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("CONNECT TO 2029", use_container_width=True):
                UIComponents.loader("ESTABLISHING QUANTUM LINK")
                prompt = f"Write a dramatic note from future self in 2029 based on habits: {json.dumps(data)}. Max 50 words. Be encouraging but real."
                res = LogicEngine.call_gemini(prompt, is_json=False)
                if res:
                    state.ai_results['future'] = res
                    st.rerun()
        
        # Display AI Results
        results = state.ai_results
        
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="aether-card" style="border-left: 5px solid #00f3ff; margin-top: 2rem;">
                <span style="font-family: var(--font-code); color: #00f3ff;">ARCHETYPE DETECTED</span>
                <h2 style="color: #00f3ff;">{r.get('persona', 'User')}</h2>
                <p style="font-style: italic; opacity: 0.8; font-size: 1.1rem; margin-bottom: 1.5rem;">"{r.get('analysis')}"</p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <ul style="margin-top: 1rem; line-height: 1.8;">
                    {''.join([f'<li>{t}</li>' for t in r.get('tips', [])])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        if 'future' in results:
            st.markdown(f"""
            <div class="aether-card" style="border-left: 5px solid #bd00ff; background: rgba(0,0,0,0.3); margin-top: 2rem;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <span style="background: #bd00ff; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">INCOMING</span>
                    <h3 style="color: #bd00ff; margin: 0;">Transmission 2029</h3>
                </div>
                <p style="font-family: var(--font-code); color: var(--text-main); font-size: 1rem; line-height: 1.6;">
                    > {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("RESTART SYSTEM", use_container_width=True):
            SessionManager.reset_data()
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# PART 7: EXECUTION ENTRY POINT
# ==============================================================================

def main():
    # 1. Initialize Session
    SessionManager.initialize()
    
    # 2. Inject CSS Engine based on current theme
    engine = HyperCSSEngine(SessionManager.get().theme_mode)
    engine.inject()
    
    # 3. Render Navigation
    UIComponents.navbar()
    
    # 4. Route Pages
    page = SessionManager.get().page
    
    if page == "home":
        SceneController.render_home()
    elif page == "about":
        SceneController.render_about()
    elif page == "interview":
        SceneController.render_interview()
    elif page == "results":
        SceneController.render_results()
        
    # 5. Render Footer
    st.markdown("""
    <div class="footer-text">
        MINDCHECK AI v5.0 // AETHER OS // 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
