# ==============================================================================
#   _   _  _____  __      __     
#  | \ | |/ _ \ \ \    / /   /\  
#  |  \| | | | \ \  / /   /  \ 
#  | . ` | | | |\ \/ /   / /\ \
#  | |\  | |_| | \  /   / ____ \
#  |_| \_|\___/   \/   /_/    \_\
# 
#  PROJECT NOVA: SINGULARITY UI (BUILD v17.0.0)
# ==============================================================================
#  SYSTEM:       MindCheck AI (Nova Class)
#  VERSION:      17.0.0 (The Visual Overhaul)
#  ARCHITECT:    Mubashir Mohsin & Gemini (Neural Core)
#  ENGINE:       Nova-CSS v17.5 + Physics Engine
#  DATE:         February 6, 2026
#  STATUS:       GOLD MASTER // OPTIMIZED
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components
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
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# ==============================================================================
# MODULE 1: SYSTEM CONFIGURATION
# ==============================================================================

class SystemConfig:
    APP_NAME = "MindCheck AI"
    VERSION = "17.0.0"
    AUTHOR = "Mubashir Mohsin"
    MODEL_PATH = 'mental_health_model.joblib'
    GEMINI_MODEL = 'gemini-2.5-flash'
    
    # UI Constants
    LAYOUT = "wide"
    SIDEBAR = "collapsed"

# Initialize Streamlit Page (MUST BE FIRST)
st.set_page_config(
    page_title=SystemConfig.APP_NAME,
    page_icon="🌌",
    layout=SystemConfig.LAYOUT,
    initial_sidebar_state=SystemConfig.SIDEBAR,
    menu_items={
        'About': f"### {SystemConfig.APP_NAME} v{SystemConfig.VERSION}\nPowered by Project Nova."
    }
)

# Secure API
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ==============================================================================
# MODULE 2: KINETIC PHYSICS ENGINE (JS)
# ==============================================================================

class KineticEngine:
    @staticmethod
    def inject():
        """
        Injects VanillaTilt.js for 3D card physics.
        Includes a MutationObserver to handle Streamlit re-renders.
        """
        js_code = """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.7.2/vanilla-tilt.min.js"></script>
        <script>
            // Initialize Tilt on elements
            function initTilt() {
                const cards = document.querySelectorAll(".nova-card");
                VanillaTilt.init(cards, {
                    max: 8,               // Rotation limit
                    speed: 800,           // Transition speed
                    glare: true,          // Glare effect
                    "max-glare": 0.3,     // Glare opacity
                    scale: 1.01,          // Slight zoom
                    perspective: 1200,    // Depth
                    gyroscope: true       // Mobile support
                });
            }

            // Watch for DOM changes
            const observer = new MutationObserver((mutations) => {
                let shouldReinit = false;
                mutations.forEach((mutation) => {
                    if (mutation.addedNodes.length > 0) {
                        shouldReinit = true;
                    }
                });
                if (shouldReinit) {
                    setTimeout(initTilt, 500); 
                }
            });

            // Start Observer
            observer.observe(window.parent.document.body, {
                childList: true,
                subtree: true
            });
            
            // Initial Run
            setTimeout(initTilt, 1000);
        </script>
        """
        components.html(js_code, height=0, width=0)

# ==============================================================================
# MODULE 3: ROBUST STATE MANAGEMENT
# ==============================================================================

class SessionManager:
    
    DEFAULTS = {
        "page": "home",
        "theme": "Dark", 
        "device_type": None, 
        "inputs": {},
        "score": None,
        "ai_results": {},
        "wizard_step": 0,
        "uuid": str(uuid.uuid4())
    }

    @staticmethod
    def init():
        for key, val in SessionManager.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = val
                
        if "theme_toggle" not in st.session_state:
            st.session_state.theme_toggle = True if st.session_state.theme == "Dark" else False

    @staticmethod
    def get(key):
        return st.session_state.get(key)

    @staticmethod
    def set(key, value):
        st.session_state[key] = value

    @staticmethod
    def handle_theme_change():
        if st.session_state.theme_toggle:
            st.session_state.theme = "Dark"
        else:
            st.session_state.theme = "Light"

    @staticmethod
    def set_device(device: str):
        with st.spinner(f"CALIBRATING UI FOR {device.upper()}..."):
            time.sleep(0.8)
        st.session_state.device_type = device
        st.rerun()

    @staticmethod
    def navigate(page):
        st.session_state.page = page
        if page != "interview":
            st.session_state.wizard_step = 0
        st.rerun()

    @staticmethod
    def wizard_next():
        st.session_state.wizard_step += 1
        st.rerun()

    @staticmethod
    def wizard_prev():
        if st.session_state.wizard_step > 0:
            st.session_state.wizard_step -= 1
            st.rerun()

    @staticmethod
    def reset():
        st.session_state.inputs = {}
        st.session_state.score = None
        st.session_state.ai_results = {}
        st.session_state.wizard_step = 0
        st.session_state.page = "interview"
        st.rerun()

# ==============================================================================
# MODULE 4: THE NOVA VISUAL ENGINE (CSS)
# ==============================================================================

class NovaEngine:
    
    @classmethod
    def _get_tokens(cls, theme: str) -> Dict[str, str]:
        if theme == "Dark":
            return {
                # --- NOVA DARK (Void/Nebula) ---
                "bg_base": "#020617",
                # Animated mesh gradient colors
                "grad_1": "#4c1d95", # Violet
                "grad_2": "#0f172a", # Slate
                "grad_3": "#000000", # Black
                
                "surface": "rgba(15, 23, 42, 0.6)", 
                "surface_border": "rgba(255, 255, 255, 0.1)",
                "surface_highlight": "rgba(30, 41, 59, 0.8)",
                
                "text_main": "#ffffff",
                "text_sub": "#cbd5e1",
                
                "accent": "#00f0ff", # Cyan
                "accent_sec": "#7000ff", # Neon Violet
                
                # SOLID INPUTS FOR READABILITY
                "input_bg": "#0f172a", 
                "input_text": "#ffffff",
                "input_border": "#334155",
                
                "glass_blur": "40px",
                "shadow": "0 20px 50px rgba(0,0,0,0.6)"
            }
        else:
            return {
                # --- NOVA LIGHT (Frost/Aurora) ---
                "bg_base": "#f8fafc",
                # Animated mesh gradient colors
                "grad_1": "#e0f2fe", # Sky
                "grad_2": "#f3e8ff", # Purple
                "grad_3": "#ffffff", # White
                
                "surface": "rgba(255, 255, 255, 0.65)", 
                "surface_border": "rgba(255, 255, 255, 0.9)",
                "surface_highlight": "#ffffff",
                
                "text_main": "#0f172a",
                "text_sub": "#475569",
                
                "accent": "#0ea5e9", # Sky Blue
                "accent_sec": "#6366f1", # Indigo
                
                # SOLID INPUTS FOR READABILITY
                "input_bg": "#ffffff",
                "input_text": "#0f172a",
                "input_border": "#cbd5e1",
                
                "glass_blur": "40px",
                "shadow": "0 20px 50px rgba(14, 165, 233, 0.1)"
            }

    @classmethod
    def _device_overrides(cls, device: str) -> str:
        if device == "Phone":
            return """
            .block-container { max-width: 100% !important; padding: 1rem 0.5rem !important; }
            h1 { font-size: 3rem !important; margin-bottom: 0.5rem !important; line-height: 1 !important; }
            h2 { font-size: 1.8rem !important; }
            .nova-card { padding: 1.5rem !important; border-radius: 20px !important; margin-bottom: 1rem !important; }
            .stButton > button { padding: 1rem !important; font-size: 1rem !important; border-radius: 12px !important; }
            .nova-nav { flex-direction: column; gap: 15px; padding: 20px !important; border-radius: 24px !important; }
            """
        elif device == "Tablet":
            return """
            .block-container { max-width: 900px !important; padding: 2rem !important; }
            h1 { font-size: 5rem !important; }
            .nova-card { padding: 2.5rem !important; }
            """
        else:
            return ".block-container { max-width: 1400px !important; }"

    @classmethod
    def _animations(cls) -> str:
        return """
        /* --- AURORA BACKGROUND ANIMATION --- */
        @keyframes aurora {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.05); opacity: 0.8; } 100% { transform: scale(1); opacity: 1; } }
        @keyframes shine { to { background-position: 200% center; } }
        
        .anim-enter { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .anim-float { animation: float 6s ease-in-out infinite; }
        .anim-pulse { animation: pulse 3s infinite; }
        """

    @classmethod
    def _core_styles(cls, t: Dict[str, str]) -> str:
        return f"""
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* --- GLOBAL RESET --- */
        .stApp {{
            background: linear-gradient(-45deg, {t['grad_1']}, {t['grad_2']}, {t['grad_3']}, {t['bg_base']});
            background-size: 400% 400%;
            animation: aurora 15s ease infinite;
            background-attachment: fixed;
        }}
        
        #MainMenu, footer, header {{ visibility: hidden; }}
        .stDeployButton {{ display: none; }}
        
        /* --- TYPOGRAPHY --- */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Outfit', sans-serif;
            color: {t['text_main']};
            font-weight: 800;
            letter-spacing: -0.02em;
            text-transform: uppercase;
        }}
        
        h1 {{ font-size: 6rem; line-height: 0.95; margin-bottom: 1.5rem; text-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        h2 {{ font-size: 3rem; margin-bottom: 2rem; }}
        h3 {{ font-size: 1.5rem; color: {t['accent']}; letter-spacing: 2px; }}
        
        p, li, span, label {{
            font-family: 'Space Grotesk', sans-serif;
            color: {t['text_sub']};
            font-size: 1.15rem;
            line-height: 1.7;
            font-weight: 500;
        }}
        
        /* --- NOVA CARD (THE GLASS CONTAINER) --- */
        .nova-card {{
            background: {t['surface']};
            border: 1px solid {t['surface_border']};
            border-radius: 32px;
            padding: 3.5rem;
            backdrop-filter: blur({t['glass_blur']}) saturate(180%);
            -webkit-backdrop-filter: blur({t['glass_blur']}) saturate(180%);
            box-shadow: {t['shadow']};
            margin-bottom: 2rem;
            transform-style: preserve-3d;
            transform: perspective(1000px);
            z-index: 1;
            /* Inner shine border */
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1);
        }}
        
        .nova-card h3, .nova-card p, .nova-card div {{
            transform: translateZ(20px); /* 3D Pop for content */
        }}
        
        /* --- SOLID INPUTS (MAX READABILITY) --- */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {{
            background-color: {t['input_bg']} !important;
            color: {t['input_text']} !important;
            border: 1px solid {t['input_border']} !important;
            border-radius: 16px !important;
            padding: 18px 24px !important;
            font-weight: 600 !important;
            font-family: 'JetBrains Mono', monospace !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease;
        }}
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {t['accent']} !important;
            box-shadow: 0 0 0 4px {t['accent']}33 !important;
            transform: translateY(-2px);
        }}
        
        /* Select Boxes */
        .stSelectbox > div > div > div {{
            background-color: {t['input_bg']} !important;
            color: {t['input_text']} !important;
            border: 1px solid {t['input_border']} !important;
            border-radius: 16px !important;
            font-weight: 600 !important;
        }}
        
        /* Dropdowns */
        div[data-baseweb="popover"], div[data-baseweb="menu"] {{
            background-color: {t['input_bg']} !important;
            border: 1px solid {t['input_border']} !important;
            border-radius: 16px !important;
            overflow: hidden !important;
        }}
        div[role="option"] {{
            color: {t['input_text']} !important;
            padding: 12px 20px !important;
            font-weight: 500 !important;
        }}
        div[role="option"]:hover {{
            background-color: {t['accent']} !important;
            color: #ffffff !important;
        }}
        
        /* --- HOLOGRAPHIC BUTTONS --- */
        .stButton > button {{
            width: 100%;
            background: linear-gradient(90deg, {t['accent']} 0%, {t['accent_sec']} 50%, {t['accent']} 100%) !important;
            background-size: 200% auto !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 1.2rem 3rem !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            transition: 0.5s !important;
            box-shadow: 0 10px 30px {t['accent']}66 !important;
        }}
        
        .stButton > button:hover {{
            background-position: right center !important; /* change the direction of the change here */
            transform: translateY(-5px) scale(1.02) !important;
            box-shadow: 0 15px 40px {t['accent']}88 !important;
        }}
        
        /* --- NAVBAR --- */
        .nova-nav {{
            background: {t['surface']};
            border: 1px solid {t['surface_border']};
            backdrop-filter: blur({t['glass_blur']});
            padding: 20px 40px;
            border-radius: 100px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 5rem;
            position: sticky;
            top: 25px;
            z-index: 999;
            box-shadow: {t['shadow']};
        }}
        
        /* --- PROGRESS BAR --- */
        .nova-progress-track {{
            width: 100%; height: 8px; background: {t['surface_border']};
            border-radius: 10px; margin: 2rem 0; overflow: hidden;
        }}
        .nova-progress-fill {{
            height: 100%; background: {t['accent']};
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 20px {t['accent']};
        }}
        
        /* --- GAUGE (CSS ONLY) --- */
        .gauge-wrapper {{ position: relative; width: 220px; height: 110px; margin: 0 auto; overflow: hidden; }}
        .gauge-bg {{ width: 220px; height: 220px; border-radius: 50%; background: {t['surface_border']}; }}
        .gauge-value {{ width: 220px; height: 220px; border-radius: 50%; background: conic-gradient({t['accent']} 0%, {t['accent_sec']} var(--p), transparent var(--p)); mask: radial-gradient(transparent 65%, black 66%); -webkit-mask: radial-gradient(transparent 65%, black 66%); transform: rotate(-90deg); position: absolute; top: 0; left: 0; }}
        """

    @classmethod
    def inject(cls):
        theme = st.session_state.theme
        device = st.session_state.device_type
        tokens = cls._get_tokens(theme)
        
        css_block = f"""
        <style>
            {cls._animations()}
            {cls._core_styles(tokens)}
            {cls._device_overrides(device) if device else ""}
        </style>
        """
        st.markdown(css_block, unsafe_allow_html=True)

# ==============================================================================
# MODULE 5: PROCEDURAL GRAPHICS
# ==============================================================================

class AssetFactory:
    
    @staticmethod
    def get_logo_svg(theme):
        c1 = "#00f0ff" if theme == "Dark" else "#0ea5e9"
        c2 = "#7000ff" if theme == "Dark" else "#6366f1"
        return base64.b64encode(f"""
        <svg width="300" height="60" xmlns="http://www.w3.org/2000/svg">
            <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
            <text x="0" y="45" font-family="sans-serif" font-weight="900" font-size="35" fill="url(#g)" letter-spacing="1">MINDCHECK AI</text>
        </svg>
        """.encode('utf-8')).decode('utf-8')

    @staticmethod
    def get_star_svg():
        return base64.b64encode("""
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <path fill="url(#g)" d="M256,32l56,156h164l-128,96l48,156l-140-96l-140,96l48-156l-128-96h164L256,32z"/>
            <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbbf24"/><stop offset="1" stop-color="#d97706"/></linearGradient></defs>
        </svg>
        """.encode('utf-8')).decode('utf-8')

    @staticmethod
    def get_cloud_svg():
        return base64.b64encode("""
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <path fill="url(#g)" d="M124,200C124,112,184,40,256,40c64,0,118,54,128,124c60,8,104,64,104,128c0,72-56,128-128,128H124C56,420,0,364,0,296S56,188,124,200z"/>
            <path stroke="#3b82f6" stroke-width="10" d="M160,440l-20,40 M256,440l-20,40 M352,440l-20,40"/>
            <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#94a3b8"/><stop offset="1" stop-color="#475569"/></linearGradient></defs>
        </svg>
        """.encode('utf-8')).decode('utf-8')

# ==============================================================================
# MODULE 6: INTELLIGENCE CORE
# ==============================================================================

class IntelligenceCore:
    @staticmethod
    def call_gemini(prompt: str, is_json: bool = True):
        # Simulation Mode for Polished Demo when API Key is missing
        if not API_KEY:
            time.sleep(2)
            if is_json:
                return json.dumps({
                    "persona": "The Digital Architect",
                    "analysis": "SIMULATION MODE: Your metrics indicate a balanced approach to digital integration, though recent data suggests slight fatigue.",
                    "tips": ["Implement the 20-20-20 rule.", "Schedule offline blocks."]
                })
            else:
                return "SIMULATION: 'Greetings from 2029. Your focus on balance paid off. We are thriving.'"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{SystemConfig.GEMINI_MODEL}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        if is_json: payload["generationConfig"] = {"responseMimeType": "application/json"}
        try:
            r = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=20)
            if r.status_code == 200:
                return r.json()['candidates'][0]['content']['parts'][0]['text']
        except: pass
        return None

# ==============================================================================
# MODULE 7: UI COMPONENTS
# ==============================================================================

class Components:
    @staticmethod
    def navbar():
        st.markdown('<div class="nova-nav">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3, 6, 2], gap="small")
        with c1:
            logo = AssetFactory.get_logo_svg(SessionManager.get("theme"))
            st.markdown(f'<img src="data:image/svg+xml;base64,{logo}" height="40">', unsafe_allow_html=True)
        with c2:
            st.markdown('<div style="display:flex; justify-content:center; width:100%;">', unsafe_allow_html=True)
            if st.button("DASHBOARD", key="nav_home"): SessionManager.navigate("home")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div style="display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
            st.toggle("Dark Mode", key="theme_toggle", on_change=SessionManager.handle_theme_change)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def loader(text="PROCESSING"):
        html = f"""
        <style>.load-over{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;backdrop-filter:blur(30px);}}</style>
        <div class="load-over">
            <h2 style="color:#00f0ff; margin-top:20px; font-family:'JetBrains Mono'; letter-spacing:3px;">{text}...</h2>
        </div>
        """
        placeholder = st.empty()
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(1.5)
        placeholder.empty()

# ==============================================================================
# MODULE 8: SCENES (PAGES)
# ==============================================================================

def view_device_selection():
    """Initial landing page for device optimization."""
    # Special CSS just for this screen
    st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #1e1b4b 0%, #000000 100%); }
    .device-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 32px; padding: 4rem 2rem; text-align: center; cursor: pointer;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .device-card:hover { transform: translateY(-10px) scale(1.02); background: rgba(0, 240, 255, 0.1); border-color: #00f0ff; box-shadow: 0 0 30px rgba(0, 240, 255, 0.2); }
    .device-icon { font-size: 5rem; margin-bottom: 20px; }
    h1 { font-family: 'Outfit', sans-serif; text-align: center; margin-bottom: 4rem; font-size: 4rem; color: white; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>SELECT INTERFACE</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3, gap="large")
    
    with c1:
        st.markdown('<div class="device-card"><div class="device-icon">📱</div><h3>PHONE</h3><p style="color:#aaa">Touch Optimized</p></div>', unsafe_allow_html=True)
        if st.button("SELECT PHONE", use_container_width=True): SessionManager.set_device("Phone")
    
    with c2:
        st.markdown('<div class="device-card"><div class="device-icon">💻</div><h3>LAPTOP</h3><p style="color:#aaa">High Fidelity</p></div>', unsafe_allow_html=True)
        if st.button("SELECT LAPTOP", use_container_width=True): SessionManager.set_device("Laptop")
        
    with c3:
        st.markdown('<div class="device-card"><div class="device-icon">📟</div><h3>TABLET</h3><p style="color:#aaa">Balanced Layout</p></div>', unsafe_allow_html=True)
        if st.button("SELECT TABLET", use_container_width=True): SessionManager.set_device("Tablet")

def view_home():
    st.markdown('<div style="height:50px"></div>', unsafe_allow_html=True)
    
    theme = SessionManager.get("theme")
    color = "#f8fafc" if theme == "Dark" else "#0f172a"
    accent = "#00f0ff" if theme == "Dark" else "#0ea5e9"
    
    st.markdown(f"""
    <div class="anim-enter" style="text-align:center; padding: 4rem 0;">
        <h1 style="font-size:6rem; line-height:1; color:{color};">MINDCHECK <span style="color:{accent}">AI</span></h1>
        <p style="font-size:1.5rem; letter-spacing:3px; opacity:0.8;">THE NOVA STANDARD IN WELLNESS</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.markdown('<div class="nova-card anim-float" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown("## 👨‍💻 CREATOR")
        st.markdown("<p>Meet the architect: Mubashir Mohsin.</p>", unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("VIEW PROFILE", use_container_width=True): SessionManager.navigate("about")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown(f'<div class="nova-card anim-float" style="text-align:center; height:100%; border-color:{accent};">', unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:{accent}'>🔮 DIAGNOSE</h2>", unsafe_allow_html=True)
        st.markdown("<p>Initialize the assessment wizard.</p>", unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("START WIZARD", type="primary", use_container_width=True): SessionManager.navigate("interview")
        st.markdown('</div>', unsafe_allow_html=True)

def view_about():
    st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom:3rem;">CREATOR LOG</h1>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown("""
        <div class="nova-card" style="text-align:center; padding:4rem;">
            <div style="font-size:5rem; margin-bottom:2rem;">🚀</div>
            <h2 style="margin-bottom:2rem;">ORIGIN STORY</h2>
            <p style="font-size:1.2rem; line-height:2;">
                "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
            </p>
            <div style="width:100px; height:2px; background:currentColor; margin: 2rem auto; opacity:0.3;"></div>
            <p style="font-family:'JetBrains Mono'; opacity:0.5;">ID: MM-2026</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def view_interview():
    step = SessionManager.get("wizard_step")
    steps = ["BIOMETRICS", "DIGITAL HABITS", "WELLNESS", "IMPACT"]
    
    # Progress
    pct = ((step + 1) / len(steps)) * 100
    st.markdown(f"""
    <div style="margin-bottom:2rem;">
        <div class="nova-progress-track"><div class="nova-progress-fill" style="width:{pct}%;"></div></div>
        <div style="display:flex; justify-content:space-between; font-family:'JetBrains Mono'; opacity:0.7;">
            <span>SEQUENCE {step + 1}/{len(steps)}</span>
            <span>{steps[step]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Wizard Container
    with st.container():
        st.markdown('<div class="nova-card anim-enter">', unsafe_allow_html=True)
        
        inputs = SessionManager.get("inputs")
        
        if step == 0:
            st.markdown("<h2>SUBJECT PROFILE</h2>", unsafe_allow_html=True)
            inputs['Age'] = st.number_input("Age", 10, 100, inputs.get('Age', 15))
            inputs['Gender'] = st.selectbox("Gender", ["Male", "Female"], index=0)
            inputs['Academic_Level'] = st.selectbox("Education", ["Middle School", "High School", "Undergraduate"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("NEXT ➔"):
                SessionManager.set("inputs", inputs)
                SessionManager.wizard_next()

        elif step == 1:
            st.markdown("<h2>DIGITAL FOOTPRINT</h2>", unsafe_allow_html=True)
            inputs['Platform'] = st.selectbox("Platform", ["TikTok", "YouTube", "Instagram", "Snapchat", "Other"])
            inputs['Avg_Daily_Usage_Hours'] = st.number_input("Daily Hours", 0.0, 24.0, inputs.get('Avg_Daily_Usage_Hours', 4.0))
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ BACK"): SessionManager.wizard_prev()
            with c2: 
                if st.button("NEXT ➔"):
                    SessionManager.set("inputs", inputs)
                    SessionManager.wizard_next()

        elif step == 2:
            st.markdown("<h2>RECOVERY METRICS</h2>", unsafe_allow_html=True)
            inputs['Sleep'] = st.number_input("Sleep (Hrs)", 0.0, 24.0, inputs.get('Sleep', 8.0))
            st.markdown("<label>Addiction Level (1-10)</label>", unsafe_allow_html=True)
            inputs['Addiction'] = st.slider("", 1, 10, inputs.get('Addiction', 5))
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ BACK"): SessionManager.wizard_prev()
            with c2: 
                if st.button("NEXT ➔"):
                    SessionManager.set("inputs", inputs)
                    SessionManager.wizard_next()

        elif step == 3:
            st.markdown("<h2>COGNITIVE LOAD</h2>", unsafe_allow_html=True)
            inputs['Conflicts'] = st.number_input("Conflicts", 0, 20, inputs.get('Conflicts', 0))
            st.markdown("<label>Grades Impacted?</label>", unsafe_allow_html=True)
            inputs['Affects_Performance'] = st.radio("", ["No", "Yes"], horizontal=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("⬅ BACK"): SessionManager.wizard_prev()
            with c2: 
                if st.button("ANALYZE 🚀"):
                    Components.loader("CALCULATING VECTORS")
                    SessionManager.set("inputs", inputs)
                    
                    # Logic
                    base = 10.0
                    base -= (inputs['Avg_Daily_Usage_Hours'] * 0.3)
                    base -= (inputs['Addiction'] * 0.2)
                    base += (inputs['Sleep'] * 0.1)
                    if inputs['Affects_Performance'] == "Yes": base -= 1.0
                    
                    SessionManager.set("score", max(1.0, min(10.0, base)))
                    SessionManager.navigate("results")

        st.markdown('</div>', unsafe_allow_html=True)

def view_results():
    score = SessionManager.get("score")
    data = SessionManager.get("inputs")
    ai_results = SessionManager.get("ai_results")
    
    # Visual Logic
    if score < 5:
        color = "#ff4757" # Red
        icon = AssetFactory.get_cloud_svg()
        msg = "CRITICAL"
    elif score < 8:
        color = "#ffa502" # Orange
        icon = AssetFactory.get_cloud_svg()
        msg = "WARNING"
    else:
        color = "#2ed573" # Green
        icon = AssetFactory.get_star_svg()
        msg = "OPTIMAL"
        
    st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
    
    # HEADER
    st.markdown(f"""
    <div class="nova-card" style="border-left: 5px solid {color}; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <span style="font-family:'JetBrains Mono'; opacity:0.6;">ID: {random.randint(1000,9999)}</span>
            <h3 style="margin:0; color:{color}">DIAGNOSTIC REPORT</h3>
        </div>
        <div style="text-align:right;">
            <span style="opacity:0.6">STATUS</span><br>
            <b style="color:{color}">{msg}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # GAUGE & SCORE
    percentage = (score / 10) * 100
    st.markdown(f"""
    <div class="nova-card" style="text-align:center; padding:4rem;">
        <div class="gauge-wrapper">
            <div class="gauge-bg"></div>
            <div class="gauge-value" style="--p: {percentage}%;"></div>
        </div>
        <div style="margin-top:-50px;">
            <img src="data:image/svg+xml;base64,{icon}" width="80" height="80" class="anim-float">
        </div>
        <h1 style="font-size:7rem; color:{color}; text-shadow:0 0 40px {color}; line-height:1; margin-top:20px;">{score:.1f}</h1>
        <p style="font-family:'JetBrains Mono'; font-size:1.2rem;">/ 10.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI GRID
    st.markdown("<h2 style='text-align:center; margin:40px 0;'>NEURAL INSIGHTS</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="nova-card" style="text-align:center; height:100%"><h3>📊 PROFILE</h3><p>Generate Persona</p></div>', unsafe_allow_html=True)
        if st.button("GENERATE", use_container_width=True):
            Components.loader("ANALYZING")
            prompt = f"Data: {json.dumps(data)}. Return JSON: 'persona', 'analysis', 'tips'."
            res = IntelligenceCore.call_gemini(prompt, is_json=True)
            if res:
                ai_results['analysis'] = json.loads(res)
                SessionManager.set("ai_results", ai_results)
                st.rerun()
                
    with c2:
        st.markdown('<div class="nova-card" style="text-align:center; height:100%"><h3>⏳ FUTURE</h3><p>Time Travel 2029</p></div>', unsafe_allow_html=True)
        if st.button("CONNECT", use_container_width=True):
            Components.loader("CONNECTING")
            prompt = f"Message from 2029 self based on: {json.dumps(data)}. Max 50 words."
            res = IntelligenceCore.call_gemini(prompt, is_json=False)
            if res:
                ai_results['future'] = res
                SessionManager.set("ai_results", ai_results)
                st.rerun()
                
    # RESULTS DISPLAY
    if 'analysis' in ai_results:
        r = ai_results['analysis']
        # Theme dependent border color logic
        c_acc = "#00f0ff" if SessionManager.get("theme") == "Dark" else "#0ea5e9"
        
        st.markdown(f"""
        <div class="nova-card" style="border-left:5px solid {c_acc}; margin-top:2rem;">
            <h3 style="color:{c_acc}">{r.get('persona')}</h3>
            <p>"{r.get('analysis')}"</p>
            <ul>{''.join([f'<li>{t}</li>' for t in r.get('tips', [])])}</ul>
        </div>
        """, unsafe_allow_html=True)
        
    if 'future' in ai_results:
        c_sec = "#7000ff" if SessionManager.get("theme") == "Dark" else "#6366f1"
        st.markdown(f"""
        <div class="nova-card" style="border-left:5px solid {c_sec}; margin-top:2rem;">
            <h3 style="color:{c_sec}">TRANSMISSION RECEIVED</h3>
            <p style="font-family:'JetBrains Mono'">{ai_results['future']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("SYSTEM RESET", use_container_width=True): SessionManager.reset()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    SessionManager.init()
    
    # 3D TILT ENGINE INJECTION
    KineticEngine.inject()
    
    # Logic Flow: Device Selection -> Navbar+App
    device = SessionManager.get("device_type")
    
    if device is None:
        view_device_selection()
    else:
        NovaEngine.inject()
        Components.navbar()
        
        page = SessionManager.get("page")
        
        if page == "home": view_home()
        elif page == "about": view_about()
        elif page == "interview": view_interview()
        elif page == "results": view_results()
        
        st.markdown("""
        <div class="aurora-footer" style="text-align:center; opacity:0.5; margin-top:50px;">
            PROJECT NOVA // MINDCHECK AI v17.0 // 2026
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
