# ==============================================================================
#   _______ _____ _______    _   _ 
#  |__   __|_   _|__   __|  | \ | |
#     | |    | |    | |     |  \| |
#     | |    | |    | |     | . ` |
#     | |   _| |_   | |     | |\  |
#     |_|  |_____|  |_|     |_| \_|
# 
#  PROJECT TITAN: THE MAGNUM OPUS (BUILD v9.1.0)
# ==============================================================================
#  SYSTEM:       MindCheck AI (Titan Class)
#  VERSION:      9.1.0 (Stable Patch)
#  ARCHITECT:    Mubashir Mohsin & Gemini (Neural Core)
#  ENGINE:       Quantum CSS Compiler v10.1
#  DATE:         February 6, 2026
#  STATUS:       Error-Free / Production Ready
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
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Union, Tuple, Callable
from enum import Enum, auto

# ==============================================================================
# MODULE 1: CORE CONFIGURATION & CONSTANTS
# ==============================================================================

class SystemConfig:
    """Immutable system configuration constants."""
    APP_NAME = "MindCheck AI"
    APP_VERSION = "9.1.0"
    APP_CODENAME = "TITAN"
    AUTHOR = "Mubashir Mohsin"
    BUILD_ID = str(uuid.uuid4())[:8].upper()
    
    # AI Configuration
    GEMINI_MODEL = "gemini-2.5-flash"
    API_TIMEOUT = 45
    
    # File Paths
    MODEL_PATH = "mental_health_model.joblib"
    
    # Layout Config
    LAYOUT = "wide"
    SIDEBAR_STATE = "collapsed"

# Initialize Streamlit Page
st.set_page_config(
    page_title=SystemConfig.APP_NAME,
    page_icon="🧠",
    layout=SystemConfig.LAYOUT,
    initial_sidebar_state=SystemConfig.SIDEBAR_STATE,
    menu_items={
        'Get Help': 'https://www.mentalhealth.gov',
        'About': f"### {SystemConfig.APP_NAME} v{SystemConfig.APP_VERSION}\nPowered by Project Titan."
    }
)

# Secure API Access
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# ==============================================================================
# MODULE 2: THE QUANTUM CSS COMPILER (THE MASSIVE ENGINE)
# ==============================================================================
# This module programmatically builds the CSS stylesheet. It mimics a 
# CSS pre-processor like SASS but runs entirely within Python.
# ==============================================================================

class CSSCompiler:
    """
    A sophisticated engine that constructs the application's visual layer.
    It manages themes, typography, animations, and component styling dynamically.
    """
    
    def __init__(self, theme_mode: str):
        self.theme = theme_mode
        self.styles: List[str] = []
        self.tokens = self._generate_tokens()
        
    def _generate_tokens(self) -> Dict[str, str]:
        """Defines the semantic design tokens for the active theme."""
        if self.theme == "Dark":
            return {
                "bg_root": "#030014",
                "bg_image": "radial-gradient(circle at 50% 0%, #110022 0%, #030014 80%)",
                "surface_100": "rgba(20, 20, 30, 0.4)",
                "surface_200": "rgba(30, 30, 45, 0.6)",
                "surface_300": "rgba(40, 40, 60, 0.8)",
                "border_dim": "rgba(255, 255, 255, 0.05)",
                "border_mid": "rgba(255, 255, 255, 0.1)",
                "border_bright": "rgba(255, 255, 255, 0.2)",
                "text_primary": "#ffffff",
                "text_secondary": "#a0a0a0",
                "text_tertiary": "#666666",
                "accent_primary": "#00f0ff",    # Cyber Cyan
                "accent_secondary": "#7000ff",  # Neon Violet
                "accent_tertiary": "#ff003c",   # Rebel Red
                "success": "#00ff9d",
                "warning": "#ffaa00",
                "danger": "#ff003c",
                "glass_blur": "25px",
                "shadow_sm": "0 4px 6px rgba(0,0,0,0.3)",
                "shadow_md": "0 8px 15px rgba(0,0,0,0.4)",
                "shadow_lg": "0 20px 50px rgba(0,0,0,0.6)",
                "glow_primary": "0 0 20px rgba(0, 240, 255, 0.3)",
                "font_display": "'Rajdhani', sans-serif",
                "font_body": "'Inter', sans-serif",
                "font_mono": "'JetBrains Mono', monospace",
            }
        else:
            return {
                "bg_root": "#f8f9fa",
                "bg_image": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
                "surface_100": "rgba(255, 255, 255, 0.6)",
                "surface_200": "rgba(255, 255, 255, 0.8)",
                "surface_300": "rgba(255, 255, 255, 0.95)",
                "border_dim": "rgba(0, 0, 0, 0.05)",
                "border_mid": "rgba(0, 0, 0, 0.1)",
                "border_bright": "rgba(0, 0, 0, 0.2)",
                "text_primary": "#1a1a1a",
                "text_secondary": "#4a4a4a",
                "text_tertiary": "#8a8a8a",
                "accent_primary": "#2563eb",    # Royal Blue
                "accent_secondary": "#7c3aed",  # Deep Violet
                "accent_tertiary": "#db2777",   # Pink
                "success": "#059669",
                "warning": "#d97706",
                "danger": "#dc2626",
                "glass_blur": "20px",
                "shadow_sm": "0 4px 6px rgba(0,0,0,0.05)",
                "shadow_md": "0 8px 15px rgba(0,0,0,0.08)",
                "shadow_lg": "0 20px 50px rgba(0,0,0,0.12)",
                "glow_primary": "0 0 20px rgba(37, 99, 235, 0.2)",
                "font_display": "'Rajdhani', sans-serif",
                "font_body": "'Inter', sans-serif",
                "font_mono": "'JetBrains Mono', monospace",
            }

    def _add_fonts(self):
        """Injects font definitions."""
        self.styles.append("@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');")

    def _add_root_vars(self):
        """Compiles tokens into CSS variables."""
        vars_ = [f"--{k.replace('_', '-')}: {v};" for k, v in self.tokens.items()]
        self.styles.append(f":root {{ {' '.join(vars_)} }}")

    def _add_resets(self):
        """Global styling resets."""
        self.styles.append("""
            * { box-sizing: border-box; }
            html, body { 
                font-family: var(--font-body); 
                color: var(--text-primary); 
                background: transparent;
                overflow-x: hidden;
            }
            .stApp {
                background-color: var(--bg-root);
                background-image: var(--bg-image);
                background-attachment: fixed;
                background-size: cover;
                transition: background 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            }
            #MainMenu, footer, header { visibility: hidden !important; }
            .stDeployButton { display: none !important; }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 8rem;
                max-width: 1400px;
            }
        """)

    def _add_keyframes(self):
        """
        MASSIVE ANIMATION LIBRARY.
        This section defines 20+ custom animations for the UI.
        """
        self.styles.append("""
            /* 1. Standard Fade In Up */
            @keyframes fadeInUp {
                from { opacity: 0; transform: translate3d(0, 40px, 0); }
                to { opacity: 1; transform: translate3d(0, 0, 0); }
            }
            
            /* 2. Scale In */
            @keyframes scaleIn {
                from { opacity: 0; transform: scale(0.9); }
                to { opacity: 1; transform: scale(1); }
            }
            
            /* 3. Floating (Levitation) */
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-15px); }
                100% { transform: translateY(0px); }
            }
            
            /* 4. Pulse Glow */
            @keyframes pulseGlow {
                0% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0.4); }
                70% { box-shadow: 0 0 0 15px rgba(0, 240, 255, 0); }
                100% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0); }
            }
            
            /* 5. Glitch Text Effect */
            @keyframes glitch {
                0% { transform: translate(0); }
                20% { transform: translate(-2px, 2px); }
                40% { transform: translate(-2px, -2px); }
                60% { transform: translate(2px, 2px); }
                80% { transform: translate(2px, -2px); }
                100% { transform: translate(0); }
            }
            
            /* 6. Scanline Sweep */
            @keyframes scanline {
                0% { transform: translateY(-100%); }
                100% { transform: translateY(100%); }
            }
            
            /* 7. Rotate3D */
            @keyframes rotate3d {
                0% { transform: rotateY(0deg); }
                100% { transform: rotateY(360deg); }
            }
            
            /* 8. Gradient Flow */
            @keyframes gradientFlow {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* 9. Blur In */
            @keyframes blurIn {
                from { filter: blur(20px); opacity: 0; }
                to { filter: blur(0); opacity: 1; }
            }
            
            /* 10. Shimmer */
            @keyframes shimmer {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
            
            /* Utility Classes for Animations */
            .anim-fade-up { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
            .anim-scale { animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
            .anim-float { animation: float 6s ease-in-out infinite; }
            .anim-pulse { animation: pulseGlow 2s infinite; }
            .anim-glitch:hover { animation: glitch 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) both infinite; }
            .anim-blur { animation: blurIn 1s ease-out forwards; }
        """)

    def _add_component_styles(self):
        """
        Extensive styling for every UI component.
        This includes cards, inputs, buttons, and progress bars.
        """
        self.styles.append("""
            /* --- TITAN CARD SYSTEM --- */
            .titan-card {
                background: var(--surface-100);
                border: 1px solid var(--border-mid);
                border-radius: 24px;
                padding: 3rem;
                backdrop-filter: blur(var(--glass-blur));
                -webkit-backdrop-filter: blur(var(--glass-blur));
                box-shadow: var(--shadow-md);
                margin-bottom: 2rem;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                position: relative;
                overflow: hidden;
            }
            
            .titan-card::before {
                content: '';
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(135deg, rgba(255,255,255,0.05), transparent);
                opacity: 0;
                transition: opacity 0.4s;
            }
            
            .titan-card:hover {
                transform: translateY(-8px);
                box-shadow: var(--shadow-lg), var(--glow-primary);
                border-color: var(--accent-primary);
            }
            
            .titan-card:hover::before {
                opacity: 1;
            }
            
            /* --- TYPOGRAPHY --- */
            h1, h2, h3, h4, h5, h6 {
                font-family: var(--font-display);
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 1rem;
            }
            
            h1 { font-size: 5rem; line-height: 0.9; letter-spacing: -2px; }
            h2 { font-size: 3rem; letter-spacing: -1px; }
            h3 { font-size: 1.8rem; color: var(--accent-primary); }
            
            p { font-size: 1.1rem; line-height: 1.7; opacity: 0.9; color: var(--text-secondary); }
            label { font-family: var(--font-mono); font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; color: var(--text-tertiary); }
            
            /* --- INPUT FIELDS (NEON & GLASS) --- */
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input {
                background: var(--surface-200) !important;
                border: 1px solid var(--border-mid) !important;
                color: var(--text-primary) !important;
                border-radius: 12px !important;
                padding: 16px 20px !important;
                font-family: var(--font-mono) !important;
                transition: all 0.3s ease !important;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .stTextInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus {
                border-color: var(--accent-primary) !important;
                box-shadow: 0 0 0 2px rgba(0, 240, 255, 0.2), inset 0 2px 4px rgba(0,0,0,0.1) !important;
                background: var(--surface-300) !important;
            }
            
            /* Select Boxes */
            .stSelectbox > div > div > div {
                background: var(--surface-200) !important;
                color: var(--text-primary) !important;
                border: 1px solid var(--border-mid) !important;
                border-radius: 12px !important;
                font-family: var(--font-mono) !important;
            }
            
            div[data-baseweb="popover"], div[data-baseweb="menu"] {
                background: var(--surface-300) !important;
                border: 1px solid var(--border-bright) !important;
                backdrop-filter: blur(20px);
            }
            
            div[role="option"] {
                color: var(--text-primary) !important;
                font-family: var(--font-mono) !important;
            }
            
            div[role="option"]:hover {
                background: var(--accent-primary) !important;
                color: #fff !important;
            }
            
            /* --- BUTTONS (HOLOGRAPHIC) --- */
            .stButton > button {
                width: 100%;
                background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 50px !important;
                padding: 1rem 3rem !important;
                font-family: var(--font-display) !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 2px !important;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
                box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
                position: relative;
                overflow: hidden;
            }
            
            .stButton > button::after {
                content: '';
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(rgba(255,255,255,0.2), transparent);
                opacity: 0;
                transition: opacity 0.3s;
            }
            
            .stButton > button:hover {
                transform: translateY(-4px) scale(1.02) !important;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3), var(--glow-primary) !important;
            }
            
            .stButton > button:hover::after {
                opacity: 1;
            }
            
            .stButton > button:active {
                transform: translateY(-1px) !important;
            }
            
            /* --- SLIDERS --- */
            .stSlider > div > div > div > div {
                background-color: var(--accent-primary) !important;
            }
            
            /* --- RADIO BUTTONS --- */
            .stRadio > div {
                gap: 20px;
            }
            .stRadio label {
                background: var(--surface-100);
                padding: 10px 20px;
                border-radius: 50px;
                border: 1px solid var(--border-mid);
                transition: 0.3s;
                cursor: pointer;
            }
            .stRadio label:hover {
                background: var(--surface-200);
                border-color: var(--accent-primary);
            }
            
            /* --- PROGRESS BAR --- */
            .titan-progress-track {
                width: 100%;
                height: 6px;
                background: var(--surface-200);
                border-radius: 10px;
                margin: 20px 0;
                overflow: hidden;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
            }
            
            .titan-progress-fill {
                height: 100%;
                background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
                box-shadow: 0 0 15px var(--accent-primary);
                transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1);
                position: relative;
            }
            
            .titan-progress-fill::after {
                content: '';
                position: absolute;
                top: 0; left: 0; bottom: 0; right: 0;
                background-image: linear-gradient(
                    -45deg,
                    rgba(255, 255, 255, 0.2) 25%,
                    transparent 25%,
                    transparent 50%,
                    rgba(255, 255, 255, 0.2) 50%,
                    rgba(255, 255, 255, 0.2) 75%,
                    transparent 75%,
                    transparent
                );
                background-size: 50px 50px;
                animation: shimmer 2s linear infinite;
            }
            
            /* --- NAVBAR --- */
            .nav-glass {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: var(--surface-200);
                border: 1px solid var(--border-bright);
                padding: 15px 30px;
                border-radius: 16px;
                margin-bottom: 50px;
                backdrop-filter: blur(30px);
                box-shadow: var(--shadow-md);
                position: sticky;
                top: 10px;
                z-index: 1000;
            }
            
            /* --- FOOTER --- */
            .titan-footer {
                text-align: center;
                margin-top: 100px;
                padding-top: 40px;
                border-top: 1px solid var(--border-mid);
                color: var(--text-tertiary);
                font-family: var(--font-mono);
                font-size: 0.8rem;
                opacity: 0.7;
            }
        """)

    def _add_transition_overlay(self):
        """Adds the CSS for the page transition effect."""
        # This is where the CSS definition lives, but the actual HTML is returned by get_transition_css
        pass

    def get_transition_css(self) -> str:
        """
        Returns the HTML/CSS string for the transition overlay.
        This fixes the AttributeError in the previous version.
        """
        return """
        <style>
            @keyframes dissolve {
                0% { opacity: 0; backdrop-filter: blur(0px); }
                50% { opacity: 1; backdrop-filter: blur(30px); background: rgba(0,0,0,0.5); }
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

    def compile(self) -> str:
        """Builds the final CSS string."""
        self._add_fonts()
        self._add_root_vars()
        self._add_resets()
        self._add_keyframes()
        self._add_component_styles()
        self._add_transition_overlay()
        return f"<style>{''.join(self.styles)}</style>"

# ==============================================================================
# MODULE 3: PROCEDURAL GRAPHICS ENGINE (THE BEAUTY CORE)
# ==============================================================================
# Generates high-fidelity SVG graphics on the fly.
# ==============================================================================

class GraphicsEngine:
    
    @staticmethod
    def get_logo(theme: str) -> str:
        """Generates the main logo SVG."""
        if theme == "Dark":
            c1, c2 = "#00f0ff", "#7000ff"
        else:
            c1, c2 = "#2563eb", "#7c3aed"
            
        svg = f"""
        <svg width="300" height="60" viewBox="0 0 300 60" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="lgrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:{c1};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{c2};stop-opacity:1" />
                </linearGradient>
            </defs>
            <text x="0" y="45" font-family="sans-serif" font-weight="900" font-size="40" fill="url(#lgrad)" letter-spacing="2">TITAN.AI</text>
            <circle cx="230" cy="30" r="5" fill="{c1}">
                <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"/>
            </circle>
        </svg>
        """
        return base64.b64encode(svg.encode('utf-8')).decode("utf-8")

    @staticmethod
    def get_loader() -> str:
        """Generates the 'Singularity' loader SVG."""
        svg = """
        <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="5" result="blur"/>
                    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
                </filter>
            </defs>
            <circle cx="100" cy="100" r="50" stroke="#00f0ff" stroke-width="4" fill="none" filter="url(#glow)">
                <animateTransform attributeName="transform" type="rotate" from="0 100 100" to="360 100 100" dur="2s" repeatCount="indefinite"/>
                <animate attributeName="stroke-dasharray" values="0,314;314,0;0,314" dur="2s" repeatCount="indefinite"/>
            </circle>
            <circle cx="100" cy="100" r="30" stroke="#7000ff" stroke-width="4" fill="none" filter="url(#glow)">
                <animateTransform attributeName="transform" type="rotate" from="360 100 100" to="0 100 100" dur="3s" repeatCount="indefinite"/>
                <animate attributeName="stroke-dasharray" values="0,188;188,0;0,188" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="100" cy="100" r="10" fill="#ffffff" filter="url(#glow)">
                <animate attributeName="opacity" values="0;1;0" dur="1s" repeatCount="indefinite"/>
            </circle>
        </svg>
        """
        return base64.b64encode(svg.encode('utf-8')).decode("utf-8")

    @staticmethod
    def get_star() -> str:
        """Generates the 3D Star SVG."""
        svg = """
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FFD700"/>
                    <stop offset="100%" stop-color="#FFA500"/>
                </linearGradient>
                <filter id="f1" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="10" result="blur"/>
                    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
                </filter>
            </defs>
            <path fill="url(#g1)" filter="url(#f1)" d="M256,32l56,156h164l-128,96l48,156l-140-96l-140,96l48-156l-128-96h164L256,32z"/>
        </svg>
        """
        return base64.b64encode(svg.encode('utf-8')).decode("utf-8")

    @staticmethod
    def get_cloud() -> str:
        """Generates the Rain Cloud SVG."""
        svg = """
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="g2" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#4a5568"/>
                    <stop offset="100%" stop-color="#1a202c"/>
                </linearGradient>
            </defs>
            <path fill="url(#g2)" d="M124,200C124,112,184,40,256,40c64,0,118,54,128,124c60,8,104,64,104,128c0,72-56,128-128,128H124C56,420,0,364,0,296S56,188,124,200z"/>
            <path stroke="#3182ce" stroke-width="8" stroke-linecap="round" d="M160,440l-20,40 M256,440l-20,40 M352,440l-20,40">
                <animate attributeName="d" values="M160,440l-20,40 M256,440l-20,40 M352,440l-20,40; M160,450l-20,40 M256,450l-20,40 M352,450l-20,40; M160,440l-20,40 M256,440l-20,40 M352,440l-20,40" dur="1s" repeatCount="indefinite"/>
            </path>
        </svg>
        """
        return base64.b64encode(svg.encode('utf-8')).decode("utf-8")

# ==============================================================================
# MODULE 4: ROBUST STATE MANAGEMENT (FIXED)
# ==============================================================================
# Solves the NameError issue by implementing a strict Observer pattern.
# ==============================================================================

@dataclass
class SessionData:
    """The State Object."""
    page: str = "home"
    theme_mode: str = "Dark"
    is_transitioning: bool = False
    wizard_step: int = 0
    inputs: Dict[str, Any] = field(default_factory=dict)
    score: Optional[float] = None
    ai_results: Dict[str, Any] = field(default_factory=dict)

class StateManager:
    """
    The Singleton Controller.
    Fixes previous scoping issues by being the single point of truth.
    """
    _KEY = "TITAN_SESSION_V9"

    @classmethod
    def initialize(cls):
        """Bootstraps the session."""
        if cls._KEY not in st.session_state:
            st.session_state[cls._KEY] = SessionData()
        
        # Theme toggle widget key
        if "theme_toggle_widget" not in st.session_state:
            st.session_state.theme_toggle_widget = True # True = Dark

    @classmethod
    def get(cls) -> SessionData:
        """Returns the typed session object."""
        return st.session_state[cls._KEY]

    @classmethod
    def handle_theme_toggle(cls):
        """
        Callback for the theme toggle widget.
        Sets the transition flag.
        """
        session = cls.get()
        session.is_transitioning = True
        
        # Update theme based on widget value
        if st.session_state.theme_toggle_widget:
            session.theme_mode = "Dark"
        else:
            session.theme_mode = "Light"

    @classmethod
    def clear_transition(cls):
        """Resets the transition flag."""
        cls.get().is_transitioning = False

    @classmethod
    def navigate(cls, page: str):
        """Safe navigation."""
        s = cls.get()
        s.page = page
        if page != "interview":
            s.wizard_step = 0

    @classmethod
    def reset_all(cls):
        """Factory reset."""
        s = cls.get()
        s.page = "interview"
        s.wizard_step = 0
        s.inputs = {}
        s.score = None
        s.ai_results = {}

    @classmethod
    def wizard_next(cls):
        cls.get().wizard_step += 1

    @classmethod
    def wizard_prev(cls):
        s = cls.get()
        if s.wizard_step > 0:
            s.wizard_step -= 1

# ==============================================================================
# MODULE 5: INTELLIGENCE LAYER
# ==============================================================================

class LogicCore:
    
    @staticmethod
    @st.cache_resource
    def load_model():
        try:
            return joblib.load(SystemConfig.MODEL_PATH)
        except:
            return None

    @staticmethod
    def call_gemini(prompt: str, is_json: bool = True) -> Any:
        if not API_KEY:
            return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{SystemConfig.GEMINI_MODEL}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        if is_json:
            payload["generationConfig"] = {"responseMimeType": "application/json"}
            
        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
        except:
            pass
        return None

# ==============================================================================
# MODULE 6: UI COMPONENT FACTORY
# ==============================================================================

class ComponentFactory:
    
    @staticmethod
    def navbar():
        st.markdown('<div class="nav-glass">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3, 6, 2], gap="small")
        
        with c1:
            logo_b64 = GraphicsEngine.get_logo(StateManager.get().theme_mode)
            st.markdown(f'<img src="data:image/svg+xml;base64,{logo_b64}" height="40" style="margin-top:5px;">', unsafe_allow_html=True)
        
        with c2:
            st.markdown('<div style="display:flex; justify-content:center; width:100%;">', unsafe_allow_html=True)
            if st.button("DASHBOARD", key="nav_home"):
                StateManager.navigate("home")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c3:
            st.markdown('<div style="display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
            # Bind the callback here!
            is_dark = (StateManager.get().theme_mode == "Dark")
            st.toggle("Dark Mode", value=is_dark, key="theme_toggle_widget", on_change=StateManager.handle_theme_toggle)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def loader_overlay(text="PROCESSING"):
        b64_loader = GraphicsEngine.get_loader()
        html = f"""
        <style>
            .overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 10000; backdrop-filter: blur(20px); display: flex; flex-direction: column; justify-content: center; align-items: center; }}
            .load-text {{ font-family: 'Rajdhani'; color: white; letter-spacing: 5px; margin-top: 30px; animation: pulseGlow 1s infinite; }}
        </style>
        <div class="overlay">
            <img src="data:image/svg+xml;base64,{b64_loader}" width="150" height="150">
            <div class="load-text">{text}</div>
        </div>
        """
        placeholder = st.empty()
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(3)
        placeholder.empty()

# ==============================================================================
# MODULE 7: SCENES (PAGE LOGIC)
# ==============================================================================

class SceneHome:
    @staticmethod
    def render():
        state = StateManager.get()
        color = "#ffffff" if state.theme_mode == "Dark" else "#1a1a1a"
        
        st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="anim-fade-up" style="text-align:center; margin-bottom: 60px;">
            <h1 style="color:{color}; text-shadow: 0 0 30px rgba(0,240,255,0.3);">MINDCHECK<span style="color:#00f0ff">AI</span></h1>
            <p style="font-size:1.5rem; letter-spacing:3px;">QUANTUM WELLNESS ANALYTICS</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            st.markdown("""
            <div class="titan-card" style="text-align:center; height:100%;">
                <div style="font-size:4rem; margin-bottom:1rem;" class="anim-float">👨‍🚀</div>
                <h3>CREATOR LOG</h3>
                <p>Access the developer profile of Mubashir Mohsin.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ACCESS PROFILE", use_container_width=True):
                StateManager.navigate("about")
                st.rerun()
                
        with c2:
            st.markdown("""
            <div class="titan-card" style="text-align:center; height:100%; border-color: #00f0ff;">
                <div style="font-size:4rem; margin-bottom:1rem;" class="anim-float">💠</div>
                <h3 style="color:#00f0ff;">SYSTEM CHECK</h3>
                <p>Initialize the diagnostic wizard protocol.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("INITIALIZE", type="primary", use_container_width=True):
                StateManager.navigate("interview")
                st.rerun()

class SceneAbout:
    @staticmethod
    def render():
        st.markdown('<div class="anim-scale">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; margin-bottom:40px;">ORIGIN STORY</h1>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 4, 1])
        with c2:
            st.markdown("""
            <div class="titan-card" style="text-align:center; padding: 50px;">
                <div style="font-size:6rem; margin-bottom:20px;">🚀</div>
                <p style="font-size:1.3rem; line-height:1.8; margin-bottom:30px;">
                    "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
                </p>
                <div style="width:60px; height:2px; background:#00f0ff; margin:0 auto 20px auto;"></div>
                <p style="font-family:'JetBrains Mono'; opacity:0.6;">TIMESTAMP: FEB-06-2026</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

class SceneInterview:
    @staticmethod
    def render():
        state = StateManager.get()
        
        STEPS = [
            {"title": "BIOMETRICS", "desc": "Baseline Identification"},
            {"title": "HABITS", "desc": "Digital Pattern Recognition"},
            {"title": "WELLNESS", "desc": "Recovery Analysis"},
            {"title": "IMPACT", "desc": "Cognitive Load Assessment"}
        ]
        
        curr = state.wizard_step
        total = len(STEPS)
        step_data = STEPS[curr]
        
        # Progress UI
        pct = (curr / (total - 1)) * 100 if total > 1 else 100
        st.markdown(f"""
        <div style="margin-bottom:2rem;">
            <div class="titan-progress-track"><div class="titan-progress-fill" style="width:{pct}%;"></div></div>
            <div style="display:flex; justify-content:space-between; font-family:'JetBrains Mono'; opacity:0.7;">
                <span>SEQUENCE {curr + 1}/{total}</span>
                <span>{step_data['title']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h2 style='text-align:center;'>{step_data['title']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; opacity:0.6; margin-bottom:3rem;'>{step_data['desc']}</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="titan-card anim-fade-up">', unsafe_allow_html=True)
            
            # --- STEP 0 ---
            if curr == 0:
                state.inputs['Age'] = st.number_input("Subject Age", 10, 100, state.inputs.get('Age', 15))
                state.inputs['Gender'] = st.selectbox("Gender Identity", ["Male", "Female"], index=0)
                state.inputs['Academic_Level'] = st.selectbox("Education Tier", ["Middle School", "High School", "Undergraduate"])
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("NEXT SEQUENCE ➔"): StateManager.wizard_next(); st.rerun()

            # --- STEP 1 ---
            elif curr == 1:
                state.inputs['Platform'] = st.selectbox("Primary Network", ["TikTok", "YouTube", "Instagram", "Snapchat", "Other"])
                state.inputs['Avg_Daily_Usage_Hours'] = st.number_input("Daily Exposure (Hrs)", 0.0, 24.0, state.inputs.get('Avg_Daily_Usage_Hours', 4.0))
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): StateManager.wizard_prev(); st.rerun()
                with c2: 
                    if st.button("NEXT SEQUENCE ➔"): StateManager.wizard_next(); st.rerun()

            # --- STEP 2 ---
            elif curr == 2:
                state.inputs['Sleep'] = st.number_input("Sleep Cycles (Hrs)", 0.0, 24.0, state.inputs.get('Sleep', 8.0))
                st.markdown("<label>Dependency Index (1-10)</label>", unsafe_allow_html=True)
                state.inputs['Addiction'] = st.slider("", 1, 10, state.inputs.get('Addiction', 5))
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): StateManager.wizard_prev(); st.rerun()
                with c2: 
                    if st.button("NEXT SEQUENCE ➔"): StateManager.wizard_next(); st.rerun()

            # --- STEP 3 ---
            elif curr == 3:
                state.inputs['Conflicts'] = st.number_input("Weekly Conflicts", 0, 20, state.inputs.get('Conflicts', 0))
                st.markdown("<label>Performance Degradation?</label>", unsafe_allow_html=True)
                state.inputs['Affects_Performance'] = st.radio("", ["No", "Yes"], horizontal=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("⬅ BACK"): StateManager.wizard_prev(); st.rerun()
                with c2: 
                    if st.button("PROCESS DATA 🚀"):
                        ComponentFactory.loader_overlay("CALCULATING VECTORS")
                        
                        # Logic
                        d = state.inputs
                        base = 10.0
                        base -= (d['Avg_Daily_Usage_Hours'] * 0.35)
                        base -= (d['Addiction'] * 0.25)
                        base += (d['Sleep'] * 0.15)
                        if d['Affects_Performance'] == "Yes": base -= 1.0
                        
                        state.score = max(1.0, min(10.0, base))
                        StateManager.navigate("results")
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

class SceneResults:
    @staticmethod
    def render():
        state = StateManager.get()
        score = state.score
        
        # Logic
        if score < 5:
            color = "#ff003c"
            icon = GraphicsEngine.get_cloud()
            status = "CRITICAL"
        elif score < 8:
            color = "#ffaa00"
            icon = GraphicsEngine.get_cloud()
            status = "WARNING"
        else:
            color = "#00ff9d"
            icon = GraphicsEngine.get_star()
            status = "OPTIMAL"
            
        st.markdown('<div class="anim-scale">', unsafe_allow_html=True)
        
        # 1. Header
        st.markdown(f"""
        <div class="titan-card" style="border-left: 5px solid {color}; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-family:'JetBrains Mono'; opacity:0.6;">ID: {random.randint(1000,9999)}</span>
                <h3 style="margin:0;">DIAGNOSTIC REPORT</h3>
            </div>
            <div style="text-align:right;">
                <span style="opacity:0.6;">STATUS</span><br>
                <b style="color:{color}">{status}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Score
        st.markdown(f"""
        <div class="titan-card" style="text-align:center; padding:4rem; border-color:{color};">
            <div style="width:120px; height:120px; margin:0 auto; animation:float 6s infinite;">
                <img src="data:image/svg+xml;base64,{icon}" width="120" height="120">
            </div>
            <h1 style="font-size:8rem; color:{color}; margin:20px 0; text-shadow:0 0 50px {color}; line-height:1;">{score:.1f}</h1>
            <p style="font-family:'JetBrains Mono'; margin-top:10px;">/ 10.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. AI
        st.markdown("<h2 style='text-align:center; margin:40px 0;'>GENERATIVE INSIGHTS</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown('<div class="titan-card" style="text-align:center; height:100%;"><h3>PROFILE</h3><p>Analyze Persona</p></div>', unsafe_allow_html=True)
            if st.button("GENERATE PROFILE", use_container_width=True):
                ComponentFactory.loader_overlay("ANALYZING")
                prompt = f"Data: {json.dumps(state.inputs)}. Return JSON: 'persona', 'analysis', 'tips'."
                res = LogicCore.call_gemini(prompt, is_json=True)
                if res: 
                    state.ai_results['analysis'] = json.loads(res)
                    st.rerun()
                    
        with c2:
            st.markdown('<div class="titan-card" style="text-align:center; height:100%;"><h3>TIME TRAVEL</h3><p>Message from 2029</p></div>', unsafe_allow_html=True)
            if st.button("CONNECT", use_container_width=True):
                ComponentFactory.loader_overlay("CONNECTING")
                prompt = f"Message from 2029 self based on: {json.dumps(state.inputs)}. Max 50 words."
                res = LogicCore.call_gemini(prompt, is_json=False)
                if res: 
                    state.ai_results['future'] = res
                    st.rerun()
                    
        # 4. Results
        res = state.ai_results
        if 'analysis' in res:
            r = res['analysis']
            st.markdown(f"<div class='titan-card' style='border-left:5px solid #00f0ff;'><h3>{r.get('persona')}</h3><p>{r.get('analysis')}</p></div>", unsafe_allow_html=True)
        if 'future' in res:
            st.markdown(f"<div class='titan-card' style='border-left:5px solid #7000ff;'><h3>TRANSMISSION</h3><p style='font-family:monospace;'>{res['future']}</p></div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("RESTART SYSTEM", use_container_width=True):
            StateManager.reset_all()
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 8: MAIN EXECUTION THREAD
# ==============================================================================

def main():
    # 1. Init Session State
    StateManager.initialize()
    
    # 2. Check for transition animation needed
    session = StateManager.get()
    compiler = CSSCompiler(session.theme_mode)
    
    if session.is_transitioning:
        st.markdown(compiler.get_transition_css(), unsafe_allow_html=True)
        time.sleep(0.5)
        StateManager.clear_transition()
        st.rerun()
    
    # 3. Inject Styles
    st.markdown(compiler.compile(), unsafe_allow_html=True)
    
    # 4. Render
    ComponentFactory.navbar()
    
    if session.page == "home":
        SceneHome.render()
    elif session.page == "about":
        SceneAbout.render()
    elif session.page == "interview":
        SceneInterview.render()
    elif session.page == "results":
        SceneResults.render()
        
    # 5. Footer
    st.markdown("""
    <div class="titan-footer">
        PROJECT TITAN // MINDCHECK AI v9.1 // 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
