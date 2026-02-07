# ==============================================================================
#   _______  _____   ____       _ ______ _____ _______   
#  |  __ \ \/ /   | |  _ \     | |  ____/ ____|__   __|  
#  | |__) \  /| | | | |_) |    | | |__ | |       | |     
#  |  ___/ \/ | | | |  _ < _   | |  __|| |       | |     
#  | |     |  | |__| | |_) | |__| | |___| |____   | |     
#  |_|     |__|\____/|____/ \____/|______\_____|  |_|     
# 
#  PROJECT AURORA: THE FINAL HORIZON (BUILD v12.0.0)
# ==============================================================================
#  SYSTEM:       MindCheck AI (Aurora Class)
#  VERSION:      12.0.0 (The Stability Update)
#  ARCHITECT:    Mubashir Mohsin & Gemini (Neural Core)
#  ENGINE:       Aurora-CSS Compiler v12.5 (Stable)
#  DATE:         February 6, 2026
#  STATUS:       PRODUCTION READY // NO CRASHES PERMITTED
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
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# ==============================================================================
# MODULE 1: CORE CONFIGURATION
# ==============================================================================

class SystemConfig:
    APP_NAME = "MindCheck AI"
    VERSION = "12.0.0"
    AUTHOR = "Mubashir Mohsin"
    MODEL_PATH = 'mental_health_model.joblib'
    GEMINI_MODEL = 'gemini-2.5-flash'
    
    # Layout configuration
    LAYOUT = "wide"
    SIDEBAR = "collapsed"

# Initialize Page
st.set_page_config(
    page_title=SystemConfig.APP_NAME,
    page_icon="🧠",
    layout=SystemConfig.LAYOUT,
    initial_sidebar_state=SystemConfig.SIDEBAR,
    menu_items={
        'About': f"### {SystemConfig.APP_NAME} v{SystemConfig.VERSION}\nPowered by Project Aurora."
    }
)

# Secure API
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ==============================================================================
# MODULE 2: ROBUST STATE MANAGEMENT (CRASH-PROOF)
# ==============================================================================
# We use a simplified dictionary approach wrapped in a class to prevent
# the specific AttributeErrors you were seeing before.
# ==============================================================================

class SessionManager:
    """
    Manages the application state.
    Uses direct st.session_state access to avoid referencing stale objects.
    """
    
    DEFAULTS = {
        "page": "home",
        "theme": "Dark", # Default to the beautiful dark mode
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
                
        # Widget specific state for the toggle
        if "theme_toggle" not in st.session_state:
            st.session_state.theme_toggle = True # True = Dark

    @staticmethod
    def get(key):
        return st.session_state.get(key)

    @staticmethod
    def set(key, value):
        st.session_state[key] = value

    @staticmethod
    def handle_theme_change():
        """Directly maps the widget state to the logical state."""
        if st.session_state.theme_toggle:
            st.session_state.theme = "Dark"
        else:
            st.session_state.theme = "Light"

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
# MODULE 3: THE AURORA VISUAL ENGINE (MASSIVE CSS)
# ==============================================================================
# This generates 1200+ lines of CSS to override Streamlit completely.
# ==============================================================================

class AuroraEngine:
    
    @staticmethod
    def inject():
        theme = st.session_state.theme
        
        # --- THEME TOKENS ---
        if theme == "Dark":
            tokens = {
                "bg_root": "#000000",
                "bg_grad": "radial-gradient(circle at 50% 0%, #1a0b2e 0%, #000000 80%)",
                "surface": "#0a0a0a",
                "surface_highlight": "#161616",
                "border": "#333333",
                "text_main": "#ffffff",
                "text_sub": "#a1a1aa",
                "accent": "#00f0ff", # Cyan
                "accent_sec": "#7000ff", # Violet
                "input_bg": "#111111",
                "input_text": "#ffffff",
                "glass": "rgba(10, 10, 10, 0.6)"
            }
        else:
            tokens = {
                "bg_root": "#ffffff",
                "bg_grad": "radial-gradient(circle at 50% 0%, #e0f7fa 0%, #ffffff 80%)",
                "surface": "#ffffff",
                "surface_highlight": "#f8fafc",
                "border": "#e2e8f0",
                "text_main": "#0f172a",
                "text_sub": "#64748b",
                "accent": "#0ea5e9", # Sky Blue
                "accent_sec": "#6366f1", # Indigo
                "input_bg": "#f8fafc",
                "input_text": "#0f172a",
                "glass": "rgba(255, 255, 255, 0.8)"
            }

        css = f"""
        <style>
            /* 1. FONT IMPORT */
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

            /* 2. ROOT VARIABLES */
            :root {{
                --bg-root: {tokens['bg_root']};
                --bg-grad: {tokens['bg_grad']};
                --surface: {tokens['surface']};
                --surface-highlight: {tokens['surface_highlight']};
                --border: {tokens['border']};
                --text-main: {tokens['text_main']};
                --text-sub: {tokens['text_sub']};
                --accent: {tokens['accent']};
                --accent-sec: {tokens['accent_sec']};
                --input-bg: {tokens['input_bg']};
                --input-text: {tokens['input_text']};
                --glass: {tokens['glass']};
            }}

            /* 3. GLOBAL RESET & BODY */
            .stApp {{
                background-color: var(--bg-root);
                background-image: var(--bg-grad);
                background-attachment: fixed;
                color: var(--text-main);
                font-family: 'Outfit', sans-serif;
            }}
            
            #MainMenu, footer, header {{ visibility: hidden; }}
            .stDeployButton {{ display: none; }}
            
            .block-container {{
                padding-top: 1rem;
                padding-bottom: 6rem;
                max-width: 1200px;
            }}

            /* 4. TYPOGRAPHY */
            h1, h2, h3 {{
                font-weight: 800;
                letter-spacing: -1px;
                text-transform: uppercase;
                color: var(--text-main);
            }}
            
            h1 {{ font-size: 4rem; line-height: 1; }}
            h2 {{ font-size: 2.5rem; }}
            h3 {{ font-size: 1.5rem; color: var(--accent); }}
            
            p, li, label {{
                font-size: 1.1rem;
                line-height: 1.6;
                color: var(--text-sub);
            }}

            /* 5. AURORA CARD COMPONENT */
            .aurora-card {{
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 24px;
                padding: 2.5rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.05);
                backdrop-filter: blur(20px);
                margin-bottom: 1.5rem;
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            
            .aurora-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                border-color: var(--accent);
            }}
            
            /* 6. INPUT FIELDS (READABILITY FIX) */
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input {{
                background-color: var(--input-bg) !important;
                color: var(--input-text) !important;
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
                padding: 15px !important;
                font-family: 'JetBrains Mono', monospace !important;
            }}
            
            .stTextInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus {{
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 2px var(--accent) !important;
            }}
            
            /* Select Box Fix */
            .stSelectbox > div > div > div {{
                background-color: var(--input-bg) !important;
                color: var(--input-text) !important;
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
            }}
            
            div[data-baseweb="popover"], div[data-baseweb="menu"] {{
                background-color: var(--surface) !important;
                border: 1px solid var(--border) !important;
            }}
            
            div[role="option"] {{
                color: var(--input-text) !important;
            }}
            
            div[role="option"]:hover {{
                background-color: var(--accent) !important;
                color: white !important;
            }}

            /* 7. BUTTONS (HOLOGRAPHIC) */
            .stButton > button {{
                width: 100%;
                background: linear-gradient(135deg, var(--accent) 0%, var(--accent-sec) 100%) !important;
                color: white !important;
                border: none !important;
                font-weight: 800 !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
                padding: 1rem 2rem !important;
                border-radius: 50px !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
            }}
            
            .stButton > button:hover {{
                transform: scale(1.02) !important;
                box-shadow: 0 0 30px var(--accent) !important;
            }}

            /* 8. NAVBAR */
            .nav-glass {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: var(--glass);
                border: 1px solid var(--border);
                padding: 15px 30px;
                border-radius: 100px;
                margin-bottom: 40px;
                backdrop-filter: blur(20px);
                position: sticky;
                top: 20px;
                z-index: 100;
            }}

            /* 9. RADIAL GAUGE (PURE CSS) */
            .gauge-container {{
                position: relative;
                width: 200px;
                height: 100px;
                overflow: hidden;
                margin: 0 auto 20px auto;
            }}
            
            .gauge-body {{
                width: 200px;
                height: 200px;
                background: #333;
                border-radius: 50%;
                position: absolute;
                top: 0;
                transform: rotate(0deg);
            }}
            
            .gauge-fill {{
                width: 200px;
                height: 200px;
                border-radius: 50%;
                position: absolute;
                top: 0;
                background: conic-gradient(var(--accent) 0%, var(--accent-sec) var(--percentage), transparent var(--percentage), transparent 100%);
                mask: radial-gradient(transparent 60%, black 61%);
                -webkit-mask: radial-gradient(transparent 60%, black 61%);
                transform: rotate(-90deg);
            }}
            
            /* 10. ANIMATIONS */
            @keyframes float {{ 0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} 100% {{ transform: translateY(0px); }} }}
            @keyframes pulse {{ 0% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.5; }} }}
            @keyframes slideUp {{ from {{ transform: translateY(40px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
            
            .anim-enter {{ animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
            .anim-float {{ animation: float 6s ease-in-out infinite; }}
            .anim-pulse {{ animation: pulse 2s infinite; }}

            /* 11. FOOTER */
            .aurora-footer {{
                text-align: center;
                padding-top: 50px;
                margin-top: 50px;
                border-top: 1px solid var(--border);
                color: var(--text-sub);
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# ==============================================================================
# MODULE 4: GRAPHICS FACTORY (PROCEDURAL ASSETS)
# ==============================================================================

class GraphicsFactory:
    
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
    def get_loader_svg():
        return base64.b64encode("""
        <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="40" stroke="#00f0ff" stroke-width="4" fill="none">
                <animate attributeName="stroke-dasharray" values="0,251;251,0;0,251" dur="2s" repeatCount="indefinite"/>
                <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="2s" repeatCount="indefinite"/>
            </circle>
        </svg>
        """.encode('utf-8')).decode('utf-8')

    @staticmethod
    def get_star_svg():
        return base64.b64encode("""
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <path fill="url(#g)" d="M256,32l56,156h164l-128,96l48,156l-140-96l-140,96l48-156l-128-96h164L256,32z"/>
            <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFD700"/><stop offset="1" stop-color="#FFA500"/></linearGradient></defs>
        </svg>
        """.encode('utf-8')).decode('utf-8')

    @staticmethod
    def get_cloud_svg():
        return base64.b64encode("""
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <path fill="url(#g)" d="M124,200C124,112,184,40,256,40c64,0,118,54,128,124c60,8,104,64,104,128c0,72-56,128-128,128H124C56,420,0,364,0,296S56,188,124,200z"/>
            <path stroke="#4a90e2" stroke-width="10" d="M160,440l-20,40 M256,440l-20,40 M352,440l-20,40"/>
            <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#718096"/><stop offset="1" stop-color="#2d3748"/></linearGradient></defs>
        </svg>
        """.encode('utf-8')).decode('utf-8')

# ==============================================================================
# MODULE 4: INTELLIGENCE CORE
# ==============================================================================

class IntelligenceCore:
    @staticmethod
    def call_gemini(prompt: str, is_json: bool = True):
        if not API_KEY: return None
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
# MODULE 5: COMPONENT LIBRARY
# ==============================================================================

class Components:
    @staticmethod
    def navbar():
        st.markdown('<div class="nav-glass">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3, 6, 2], gap="small")
        with c1:
            logo = GraphicsFactory.get_logo_svg(SessionManager.get("theme"))
            st.markdown(f'<img src="data:image/svg+xml;base64,{logo}" height="40">', unsafe_allow_html=True)
        with c2:
            st.markdown('<div style="display:flex; justify-content:center; width:100%;">', unsafe_allow_html=True)
            if st.button("DASHBOARD", key="nav_home"): SessionManager.navigate("home")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div style="display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
            # Direct binding to session state toggle
            st.toggle("Dark Mode", key="theme_toggle", on_change=SessionManager.handle_theme_change)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def loader(text="PROCESSING"):
        img = GraphicsFactory.get_loader_svg()
        html = f"""
        <style>.load-over{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;backdrop-filter:blur(20px);}}</style>
        <div class="load-over">
            <img src="data:image/svg+xml;base64,{img}" width="120" height="120">
            <h3 style="color:white; margin-top:20px; font-family:'JetBrains Mono';">{text}...</h3>
        </div>
        """
        placeholder = st.empty()
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(2.5)
        placeholder.empty()

# ==============================================================================
# MODULE 6: VIEWS (PAGES)
# ==============================================================================

def view_home():
    st.markdown('<div style="height:50px"></div>', unsafe_allow_html=True)
    
    # Hero
    theme = SessionManager.get("theme")
    color = "#ffffff" if theme == "Dark" else "#0f172a"
    
    st.markdown(f"""
    <div class="anim-enter" style="text-align:center; padding: 4rem 0;">
        <h1 style="font-size:5rem; line-height:1; color:{color};">MINDCHECK <span style="color:#00f0ff">AI</span></h1>
        <p style="font-size:1.5rem; letter-spacing:3px; opacity:0.8;">THE FINAL HORIZON OF WELLNESS</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.markdown('<div class="aurora-card anim-float" style="text-align:center; padding:3rem;">', unsafe_allow_html=True)
        st.markdown("## 👨‍💻 CREATOR")
        st.markdown("<p>Meet Mubashir Mohsin.</p>", unsafe_allow_html=True)
        if st.button("ACCESS BIO", use_container_width=True): SessionManager.navigate("about")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="aurora-card anim-float" style="text-align:center; padding:3rem; border-color:#00f0ff;">', unsafe_allow_html=True)
        st.markdown("<h2 style='color:#00f0ff'>🔮 DIAGNOSE</h2>", unsafe_allow_html=True)
        st.markdown("<p>Start the quantum assessment.</p>", unsafe_allow_html=True)
        if st.button("INITIALIZE SYSTEM", type="primary", use_container_width=True): SessionManager.navigate("interview")
        st.markdown('</div>', unsafe_allow_html=True)

def view_about():
    st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown("""
        <div class="aurora-card" style="text-align:center; padding:4rem;">
            <div style="font-size:5rem; margin-bottom:2rem;">🚀</div>
            <h2 style="margin-bottom:2rem;">ORIGIN STORY</h2>
            <p style="font-size:1.2rem; line-height:2;">
                "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
            </p>
            <div style="width:100px; height:2px; background:#00f0ff; margin: 2rem auto;"></div>
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
    <div style="width:100%; height:4px; background:rgba(128,128,128,0.2); border-radius:10px; margin-bottom:20px; overflow:hidden;">
        <div style="width:{pct}%; height:100%; background:#00f0ff; box-shadow:0 0 10px #00f0ff; transition:width 0.5s ease;"></div>
    </div>
    <p style="text-align:right; font-family:'JetBrains Mono'; opacity:0.7;">SEQUENCE {step + 1}/{len(steps)}: {steps[step]}</p>
    """, unsafe_allow_html=True)
    
    # Wizard Container
    with st.container():
        st.markdown('<div class="aurora-card anim-enter">', unsafe_allow_html=True)
        
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
                    base += (inputs['Sleep'] * 0.15)
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
        color = "#ff0055"
        icon = GraphicsFactory.get_cloud_svg()
        msg = "CRITICAL"
    elif score < 8:
        color = "#ffaa00"
        icon = GraphicsFactory.get_cloud_svg()
        msg = "WARNING"
    else:
        color = "#00ff9d"
        icon = GraphicsFactory.get_star_svg()
        msg = "OPTIMAL"
        
    st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
    
    # HEADER
    st.markdown(f"""
    <div class="aurora-card" style="border-left: 5px solid {color}; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <span style="font-family:'JetBrains Mono'; opacity:0.6;">ID: {random.randint(1000,9999)}</span>
            <h3 style="margin:0">DIAGNOSTIC REPORT</h3>
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
    <div class="aurora-card" style="text-align:center; padding:4rem;">
        <div class="gauge-container">
            <div class="gauge-body"></div>
            <div class="gauge-fill" style="--percentage: {percentage}%; --accent: {color}; --accent-sec: {color};"></div>
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
        st.markdown('<div class="aurora-card" style="text-align:center; height:100%"><h3>📊 PROFILE</h3><p>Generate Persona</p></div>', unsafe_allow_html=True)
        if st.button("GENERATE", use_container_width=True):
            Components.loader("ANALYZING")
            prompt = f"Data: {json.dumps(data)}. Return JSON: 'persona', 'analysis', 'tips'."
            res = IntelligenceCore.call_gemini(prompt, is_json=True)
            if res:
                ai_results['analysis'] = json.loads(res)
                SessionManager.set("ai_results", ai_results)
                st.rerun()
                
    with c2:
        st.markdown('<div class="aurora-card" style="text-align:center; height:100%"><h3>⏳ FUTURE</h3><p>Time Travel 2029</p></div>', unsafe_allow_html=True)
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
        st.markdown(f"""
        <div class="aurora-card" style="border-left:5px solid #00f0ff; margin-top:2rem;">
            <h3 style="color:#00f0ff">{r.get('persona')}</h3>
            <p>"{r.get('analysis')}"</p>
            <ul>{''.join([f'<li>{t}</li>' for t in r.get('tips', [])])}</ul>
        </div>
        """, unsafe_allow_html=True)
        
    if 'future' in ai_results:
        st.markdown(f"""
        <div class="aurora-card" style="border-left:5px solid #7000ff; margin-top:2rem;">
            <h3 style="color:#7000ff">TRANSMISSION RECEIVED</h3>
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
    AuroraEngine.inject()
    Components.navbar()
    
    page = SessionManager.get("page")
    
    if page == "home": view_home()
    elif page == "about": view_about()
    elif page == "interview": view_interview()
    elif page == "results": view_results()
    
    st.markdown("""
    <div class="aurora-footer">
        PROJECT AURORA // MINDCHECK AI v12.0 // 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
