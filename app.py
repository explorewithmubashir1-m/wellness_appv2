# ==============================================================================
# PROJECT: MINDCHECK AI - LUMINA MATERIAL HYBRID EDITION
# ==============================================================================
# VERSION: 6.0.0-ULTIMATE
# DATE: February 05, 2026
# ARCHITECTURE: Streamlit + Python + CSS3 Hybrid Engine
# AUTHOR: Mubashir Mohsin & Gemini (AI Architect)
# ==============================================================================
#
# [ SYSTEM DOCUMENTATION ]
# ------------------------------------------------------------------------------
# This application represents the convergence of two distinct design philosophies:
#
# 1. LIQUID GLASS (Apple VisionOS / iOS):
#    - Characterized by high-blur backdrops (50px+).
#    - High saturation layers to mimic light refraction.
#    - Specular highlighting on borders to simulate physical thickness.
#
# 2. MATERIAL EXPRESSIVE (Android 14/15):
#    - Characterized by "Spring" physics animations.
#    - Large, playful border radii (Extra-Large shapes).
#    - High contrast, vibrant tonal palettes.
#
# CODE STRUCTURE:
# 1.0 - CORE CONFIGURATION & IMPORTS
# 2.0 - ASSET LIBRARY (SVG VECTOR DATA)
# 3.0 - CONTENT REPOSITORY (TEXT DATA)
# 4.0 - VISUAL THEME ENGINE (CSS GENERATOR)
# 5.0 - SESSION STATE MANAGER
# 6.0 - BUSINESS LOGIC LAYER (AI & ML)
# 7.0 - COMPONENT LIBRARY (UI WIDGETS)
# 8.0 - ROUTING & PAGE CONTROLLERS
# 9.0 - MAIN EXECUTION LOOP
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
# 1.0 CORE CONFIGURATION & IMPORTS
# ==============================================================================

# 1.1 FILE PATH CONSTANTS
# -----------------------
# While we have an internal AssetLibrary for fail-safety, we still look for
# these files first to respect the user's uploaded assets.
FAVICON_FILENAME = "Gemini_Generated_Image_5b19745b19745b19.jpg"
LOGO_FILENAME = "Gemini_Generated_Image_fq49a6fq49a6fq49.jpg"
MODEL_FILE = 'mental_health_model.joblib'
GEMINI_MODEL = 'gemini-2.5-flash'

# 1.2 SECURITY
# ------------
API_KEY = st.secrets.get("GEMINI_API_KEY", None)
MODEL_COLUMNS = ['Age', 'Gender', 'Academic_Level', 'Avg_Daily_Usage_Hours', 'Affects_Academic_Performance', 'Sleep_Hours_Per_Night', 'Conflicts_Over_Social_Media', 'Addicted_Score', 'Most_Used_Platform_Facebook', 'Most_Used_Platform_Instagram', 'Most_Used_Platform_KakaoTalk', 'Most_Used_Platform_LINE', 'Most_Used_Platform_LinkedIn', 'Most_Used_Platform_Snapchat', 'Most_Used_Platform_TikTok', 'Most_Used_Platform_Twitter', 'Most_Used_Platform_VKontakte', 'Most_Used_Platform_WeChat', 'Most_Used_Platform_WhatsApp', 'Most_Used_Platform_YouTube', 'Most_Used_Platform_Youtube', 'Relationship_Status_Complicated', 'Relationship_Status_In Relationship', 'Relationship_Status_Single']
# 1.3 PAGE SETUP
# --------------
st.set_page_config(
    page_title="MindCheck AI",
    page_icon=FAVICON_FILENAME,
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.mentalhealth.gov',
        'Report a bug': "mailto:support@mindcheck.ai",
        'About': "MindCheck AI v6.0\nHybrid Design Architecture"
    }
)

# ==============================================================================
# 2.0 ASSET LIBRARY (SVG VECTOR DATA)
# ==============================================================================
# This class acts as a fail-safe. If external images are missing,
# the app will render these high-quality SVGs instead.
# ==============================================================================

class AssetLibrary:
    """
    A static repository of Vector Graphics to ensure the UI looks premium
    even without external image dependencies.
    """
    
    @staticmethod
    def get_logo_svg(color="#a855f7"):
        """Returns the XML string for the Main Brand Logo."""
        return f"""
        <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#0ea5e9;stop-opacity:1" />
                </linearGradient>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <path d="M100,20 C55.8,20,20,55.8,20,100 s35.8,80,80,80 s80-35.8,80-80 S144.2,20,100,20 z" 
                  fill="none" stroke="url(#grad1)" stroke-width="8" filter="url(#glow)" />
            <path d="M60,100 L85,125 L140,70" 
                  fill="none" stroke="url(#grad1)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" />
            <circle cx="100" cy="100" r="90" fill="none" stroke="{color}" stroke-width="2" opacity="0.3">
                <animateTransform attributeName="transform" type="rotate" from="0 100 100" to="360 100 100" dur="10s" repeatCount="indefinite"/>
            </circle>
        </svg>
        """

    @staticmethod
    def get_home_icon_svg():
        return """
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
        """

    @staticmethod
    def get_brain_icon_svg():
        return """
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"></path>
            <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"></path>
        </svg>
        """

    @staticmethod
    def get_profile_icon_svg():
        return """
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
        </svg>
        """

    @staticmethod
    def get_news_icon_svg():
        return """
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1m2 13a2 2 0 0 1-2-2V7m2 13a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
        </svg>
        """

# ==============================================================================
# 3.0 CONTENT REPOSITORY (TEXT DATA)
# ==============================================================================
# Separating content from logic allows for easier updates and translation support.
# ==============================================================================

class ContentRepository:
    """
    Holds all static text, legal disclaimers, and educational content.
    """
    
    APP_TITLE = "MindCheck AI"
    APP_SUBTITLE = "The Hybrid Intelligence for Mental Resilience."
    
    LEGAL_DISCLAIMER = """
    <div style='
        font-family: "SF Pro Text", sans-serif;
        font-size: 0.75rem;
        opacity: 0.6;
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        border-top: 1px solid rgba(255,255,255,0.1);
    '>
        <strong>DISCLAIMER:</strong> This application is a demonstration of AI capabilities in mental health screening. 
        It provides educational insights based on self-reported data. 
        <strong>It is NOT a diagnostic tool.</strong> 
        The results generated by MindCheck AI should not replace professional medical advice, diagnosis, or treatment. 
        If you are experiencing a mental health crisis, please contact emergency services immediately.
    </div>
    """
    
    ABOUT_TEXT = """
    ## The Philosophy
    MindCheck AI was built to bridge the gap between digital habits and mental awareness.
    Using advanced machine learning, we analyze patterns in your daily digital consumption
    to provide a mirror to your mental state.
    
    ## The Technology
    Built on a **Lumina-Material Hybrid** architecture, this app combines the fluid, 
    glass-like aesthetics of modern spatial computing with the playful, expressive 
    motion of touch-first interfaces.
    """
    
    VERSION_INFO = "v6.0.0 (Build 2026.02.05)"

# ==============================================================================
# 4.0 VISUAL THEME ENGINE (CSS GENERATOR)
# ==============================================================================
# This is the heart of the UI. It generates thousands of lines of CSS 
# dynamically based on the active theme state.
# ==============================================================================

class ThemeEngine:
    """
    Manages color tokens, physics constants, and CSS injection.
    """
    
    # 4.1 THEME DEFINITIONS
    # ---------------------
    THEMES = {
        "Dark": {
            # Backgrounds
            "bg_layer": "radial-gradient(circle at 50% 0%, #111111 0%, #050505 100%)",
            "bg_noise": "url('data:image/svg+xml;base64,...')", # Placeholder for noise texture
            
            # Liquid Glass Properties
            "glass_surface": "rgba(20, 20, 20, 0.6)",
            "glass_border": "rgba(255, 255, 255, 0.1)",
            "glass_highlight": "rgba(255, 255, 255, 0.15)",
            "glass_shadow": "0 25px 50px -12px rgba(0, 0, 0, 0.5)",
            
            # Typography
            "text_primary": "#ffffff",
            "text_secondary": "#a1a1aa",
            "text_tertiary": "#52525b",
            
            # Accents (Neon Cyber)
            "accent_primary": "#a855f7", # Purple
            "accent_secondary": "#ec4899", # Pink
            "accent_tertiary": "#6366f1", # Indigo
            
            # Semantic Colors
            "success": "#34d399",
            "warning": "#fbbf24",
            "danger": "#f87171",
            "info": "#38bdf8",
            
            # Gradients
            "brand_gradient": "linear-gradient(135deg, #a855f7 0%, #ec4899 100%)",
            
            # Physics
            "blur_strength": "50px",
            "saturation": "180%",
            "brightness": "1.1"
        },
        "Light": {
            # Backgrounds
            "bg_layer": "radial-gradient(circle at 50% 0%, #f8fafc 0%, #e2e8f0 100%)",
            
            # Liquid Glass Properties
            "glass_surface": "rgba(255, 255, 255, 0.65)",
            "glass_border": "rgba(255, 255, 255, 0.8)",
            "glass_highlight": "rgba(255, 255, 255, 0.9)",
            "glass_shadow": "0 20px 40px -12px rgba(0, 0, 0, 0.1)",
            
            # Typography
            "text_primary": "#0f172a",
            "text_secondary": "#64748b",
            "text_tertiary": "#94a3b8",
            
            # Accents (Oceanic)
            "accent_primary": "#0ea5e9", # Sky
            "accent_secondary": "#3b82f6", # Blue
            "accent_tertiary": "#06b6d4", # Cyan
            
            # Semantic Colors
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            "info": "#0ea5e9",
            
            # Gradients
            "brand_gradient": "linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)",
            
            # Physics
            "blur_strength": "35px",
            "saturation": "200%",
            "brightness": "1.05"
        }
    }

    @staticmethod
    def get_current_theme():
        mode = st.session_state.get("theme_mode", "Light")
        return ThemeEngine.THEMES[mode]

    @staticmethod
    def generate_css():
        """
        Constructs the massive CSS block for the application.
        Incorporates Liquid Glass physics and Material 3 motion.
        """
        t = ThemeEngine.get_current_theme()
        
        # Define the SVG background pattern for score visualization
        emoji = "🌟" if (st.session_state.get('score', 0) or 0) >= 6 else "🌧️"
        svg_bg = f"""
        <svg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'>
            <text x='50%' y='50%' font-size='20' text-anchor='middle' dominant-baseline='middle' opacity='0.03'>{emoji}</text>
        </svg>
        """
        b64_bg = base64.b64encode(svg_bg.encode('utf-8')).decode('utf-8')
        bg_image_combined = f"url('data:image/svg+xml;base64,{b64_bg}'), {t['bg_layer']}"

        return f"""
        <style>
            /* ====================================================================
               1. FONT STACK IMPORT
               ==================================================================== */
            @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@100;300;400;500;600;700;900&family=Outfit:wght@300;400;600;800&display=swap');

            /* ====================================================================
               2. CSS VARIABLES (DESIGN TOKENS)
               ==================================================================== */
            :root {{
                /* Colors */
                --bg: {t['bg_layer']};
                --surface: {t['glass_surface']};
                --border: {t['glass_border']};
                --highlight: {t['glass_highlight']};
                --shadow: {t['glass_shadow']};
                
                --text-main: {t['text_primary']};
                --text-sub: {t['text_secondary']};
                
                --accent: {t['accent_primary']};
                --accent-glow: {t['accent_primary']}44;
                
                --brand-grad: {t['brand_gradient']};
                
                --success: {t['success']};
                --warning: {t['warning']};
                --danger: {t['danger']};
                
                /* Physics & Optics */
                --blur: {t['blur_strength']};
                --sat: {t['saturation']};
                --bright: {t['brightness']};
                
                /* Geometry (Material 3 Expressive Shapes) */
                --radius-xs: 8px;
                --radius-sm: 16px;
                --radius-md: 24px;
                --radius-lg: 32px;
                --radius-xl: 48px;
                --radius-pill: 9999px;
                
                /* Animation Timing (Spring Physics) */
                --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Bouncy */
                --ease-fluid: cubic-bezier(0.4, 0, 0.2, 1); /* Standard */
                --ease-snappy: cubic-bezier(0.075, 0.82, 0.165, 1); /* Fast */
            }}

            /* ====================================================================
               3. GLOBAL RESET & SCAFFOLDING
               ==================================================================== */
            .stApp {{
                background: {bg_image_combined};
                background-attachment: fixed;
                background-size: cover;
                font-family: 'SF Pro Display', 'Outfit', sans-serif;
                color: var(--text-main);
                transition: background 0.8s var(--ease-fluid);
            }}
            
            .block-container {{
                padding-top: 1rem !important;
                padding-bottom: 6rem !important;
                max-width: 1200px;
            }}

            /* ====================================================================
               4. COMPONENT: LIQUID GLASS CARD (The Core Container)
               ==================================================================== */
            .liquid-card {{
                position: relative;
                background: var(--surface);
                
                /* The Optical Engine */
                backdrop-filter: blur(var(--blur)) saturate(var(--sat)) brightness(var(--bright));
                -webkit-backdrop-filter: blur(var(--blur)) saturate(var(--sat)) brightness(var(--bright));
                
                /* Refractive Border */
                border: 1px solid var(--border);
                border-top: 1px solid rgba(255,255,255,0.4);
                border-left: 1px solid rgba(255,255,255,0.2);
                
                border-radius: var(--radius-lg);
                padding: 40px;
                margin-bottom: 30px;
                
                /* Depth Simulation */
                box-shadow: 
                    0 20px 40px -10px var(--shadow),
                    inset 0 0 20px rgba(255,255,255,0.05);
                    
                transform-style: preserve-3d;
                transition: transform 0.5s var(--ease-spring), box-shadow 0.5s var(--ease-fluid);
                
                overflow: hidden;
            }}
            
            /* Hover State: Lift & Glow */
            .liquid-card:hover {{
                transform: translateY(-8px) scale(1.01);
                box-shadow: 
                    0 30px 60px -12px var(--shadow),
                    0 0 0 2px var(--accent-glow);
                z-index: 10;
            }}
            
            /* Internal Sheen Animation (Light flowing across glass) */
            .liquid-card::before {{
                content: '';
                position: absolute;
                top: 0; left: -100%;
                width: 50%; height: 100%;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(255,255,255,0.2),
                    transparent
                );
                transform: skewX(-25deg);
                transition: 0.5s;
                pointer-events: none;
            }}
            
            .liquid-card:hover::before {{
                animation: sheen 0.8s forwards;
            }}
            
            @keyframes sheen {{
                100% {{ left: 150%; }}
            }}

            /* ====================================================================
               5. COMPONENT: NAVIGATION DOCK (Floating Pill)
               ==================================================================== */
            .nav-dock-container {{
                width: 100%;
                display: flex;
                justify-content: center;
                margin-top: 20px;
                margin-bottom: 50px;
                position: sticky;
                top: 20px;
                z-index: 999;
            }}
            
            .nav-dock {{
                background: var(--surface);
                backdrop-filter: blur(40px) saturate(180%);
                -webkit-backdrop-filter: blur(40px) saturate(180%);
                border: 1px solid var(--border);
                border-radius: var(--radius-pill);
                
                /* Dynamic Sizing */
                padding: 12px 30px;
                width: 90%;
                max-width: 1000px;
                
                display: flex;
                align-items: center;
                justify-content: space-between;
                
                box-shadow: 0 15px 35px -10px var(--shadow);
                
                /* Bounce entrance */
                animation: dock-pop 0.8s var(--ease-spring);
            }}
            
            @keyframes dock-pop {{
                0% {{ transform: translateY(-50px) scale(0.8); opacity: 0; }}
                100% {{ transform: translateY(0) scale(1); opacity: 1; }}
            }}

            /* ====================================================================
               6. COMPONENT: EXPRESSIVE BUTTONS (Haptic Feedack Sim)
               ==================================================================== */
            .stButton > button {{
                background: var(--brand-grad) !important;
                color: white !important;
                border: none !important;
                border-radius: var(--radius-md) !important;
                padding: 16px 32px !important;
                
                font-family: 'Outfit', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
                letter-spacing: 0.5px !important;
                text-transform: uppercase !important;
                
                /* Physics */
                transition: all 0.3s var(--ease-spring) !important;
                box-shadow: 0 10px 20px -5px var(--accent-glow) !important;
                
                width: 100%;
                position: relative;
                overflow: hidden;
            }}
            
            .stButton > button:hover {{
                transform: translateY(-4px) scale(1.02);
                box-shadow: 0 20px 40px -10px var(--accent-glow) !important;
                filter: brightness(1.1);
            }}
            
            .stButton > button:active {{
                transform: scale(0.92); /* Significant press effect */
                box-shadow: 0 5px 10px -5px var(--accent-glow) !important;
            }}
            
            /* Secondary Button Variant (Outline) */
            .stButton > button.secondary {{
                background: transparent !important;
                border: 2px solid var(--text-main) !important;
                color: var(--text-main) !important;
            }}

            /* ====================================================================
               7. COMPONENT: INPUTS (Pure White Requirement)
               ==================================================================== */
            /* Enforcing strict white/black contrast for accessibility */
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input,
            .stSelectbox > div > div > div {{
                background-color: #ffffff !important;
                color: #000000 !important;
                caret-color: var(--accent) !important;
                
                border: 2px solid rgba(0,0,0,0.05) !important;
                border-radius: var(--radius-sm) !important;
                padding: 14px 18px !important;
                
                font-weight: 600 !important;
                transition: all 0.3s var(--ease-fluid);
            }}
            
            .stTextInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus {{
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 4px var(--accent-glow) !important;
                transform: scale(1.01);
            }}
            
            /* Dropdown Fixes */
            div[data-baseweb="select"] > div {{ background-color: #ffffff !important; color: #000000 !important; border-radius: var(--radius-sm) !important; }}
            div[data-testid="stSelectbox"] div[class*="st-"] {{ color: #000000 !important; }}
            div[data-baseweb="popover"] {{ background-color: #ffffff !important; border-radius: var(--radius-sm) !important; box-shadow: 0 10px 40px rgba(0,0,0,0.2) !important; }}
            div[role="option"] {{ color: #000000 !important; background-color: #ffffff !important; padding: 12px 20px !important; }}
            div[role="option"]:hover {{ background-color: #f0f9ff !important; }}

            /* ====================================================================
               8. TYPOGRAPHY & DECORATION
               ==================================================================== */
            h1, .hero-font {{
                font-family: 'Outfit', sans-serif;
                font-weight: 800;
                letter-spacing: -0.04em;
                background: var(--brand-grad);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 20px;
                text-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            .section-label {{
                font-size: 0.85rem;
                font-weight: 800;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                color: var(--accent);
                margin-bottom: 15px;
                display: flex; align-items: center; gap: 10px;
            }}
            
            .section-label::after {{
                content: ''; flex: 1; height: 2px;
                background: linear-gradient(90deg, var(--accent), transparent);
                opacity: 0.3;
            }}

            /* ====================================================================
               9. ANIMATION LIBRARY
               ==================================================================== */
            .anim-enter {{
                animation: slide-up 0.8s var(--ease-spring) forwards;
                opacity: 0; transform: translateY(50px);
            }}
            
            @keyframes slide-up {{
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            .anim-float {{
                animation: float 6s ease-in-out infinite;
            }}
            
            @keyframes float {{
                0% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-15px); }}
                100% {{ transform: translateY(0px); }}
            }}

            /* ====================================================================
               10. LOADER OVERLAY (The Cyber Heart)
               ==================================================================== */
            .loader-screen {{
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: rgba(0,0,0,0.9);
                backdrop-filter: blur(50px);
                z-index: 999999;
                display: flex; flex-direction: column; justify-content: center; align-items: center;
            }}
            
            .loader-stage {{ position: relative; width: 200px; height: 200px; }}
            
            .orbit-1 {{
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                border-radius: 50%; border: 4px solid transparent;
                border-top-color: var(--accent);
                border-right-color: #0ea5e9;
                animation: spin 2s linear infinite;
            }}
            
            .orbit-2 {{
                position: absolute; top: 20%; left: 20%; width: 60%; height: 60%;
                border-radius: 50%; border: 4px solid transparent;
                border-bottom-color: #ec4899;
                border-left-color: #f59e0b;
                animation: spin-rev 3s linear infinite;
            }}
            
            .core-pulse {{
                position: absolute; top: 50%; left: 50%; width: 40px; height: 40px;
                background: var(--brand-grad); border-radius: 50%;
                transform: translate(-50%, -50%);
                animation: heartbeat 1.2s ease-in-out infinite;
                box-shadow: 0 0 50px var(--accent);
            }}
            
            .loader-text {{
                margin-top: 40px;
                color: white; font-family: 'Outfit';
                font-weight: 800; letter-spacing: 0.3em;
                animation: flicker 3s infinite;
            }}
            
            @keyframes spin {{ 0% {{transform: rotate(0deg);}} 100% {{transform: rotate(360deg);}} }}
            @keyframes spin-rev {{ 0% {{transform: rotate(360deg);}} 100% {{transform: rotate(-360deg);}} }}
            @keyframes heartbeat {{ 
                0% {{transform: translate(-50%,-50%) scale(1);}} 
                15% {{transform: translate(-50%,-50%) scale(1.3);}} 
                30% {{transform: translate(-50%,-50%) scale(1);}} 
                100% {{transform: translate(-50%,-50%) scale(1);}} 
            }}
            @keyframes flicker {{ 
                0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {{ opacity: 1; }} 
                20%, 24%, 55% {{ opacity: 0.1; }} 
            }}

            /* ====================================================================
               11. UTILITIES
               ==================================================================== */
            /* Custom Scrollbar */
            ::-webkit-scrollbar {{ width: 10px; }}
            ::-webkit-scrollbar-track {{ background: transparent; }}
            ::-webkit-scrollbar-thumb {{
                background: var(--border);
                border-radius: 20px;
                border: 3px solid transparent;
                background-clip: content-box;
            }}
            ::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}
            
            /* Hide Footers */
            footer {{ visibility: hidden; }}
            #MainMenu {{ visibility: hidden; }}
            
        </style>
        """

# ==============================================================================
# 5.0 COMPONENT LIBRARY (UI WIDGETS)
# ==============================================================================

class UILibrary:
    """
    Static class containing reusable UI rendering logic.
    """
    
    @staticmethod
    def render_navbar():
        """Renders the top navigation dock."""
        st.markdown('<div class="nav-dock-container"><div class="nav-dock">', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1.5, 3, 1.5])
        
        # Branding
        with c1:
            if os.path.exists(LOGO_FILENAME):
                st.image(LOGO_FILENAME, width=130)
            else:
                # SVG Fallback
                st.markdown(AssetLibrary.get_logo_svg(ThemeEngine.get_current_theme()['accent_primary']), unsafe_allow_html=True)
                
        # Navigation
        with c2:
            st.markdown("<div style='display:flex; justify-content:center; width:100%;'>", unsafe_allow_html=True)
            if st.button("🏠 DASHBOARD HOME", key="nav_home_btn"):
                go_to_page("home")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Controls
        with c3:
            st.markdown("<div style='display:flex; justify-content:flex-end; align-items:center; width:100%;'>", unsafe_allow_html=True)
            is_dark = (st.session_state.theme_mode == "Dark")
            st.toggle("Night Mode", value=is_dark, key="theme_toggle", on_change=toggle_theme)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown('</div></div>', unsafe_allow_html=True)

    @staticmethod
    def show_loader(duration=4):
        """Displays the blocking loading screen."""
        html = """
        <div class="loader-screen">
            <div class="loader-stage">
                <div class="orbit-1"></div>
                <div class="orbit-2"></div>
                <div class="core-pulse"></div>
            </div>
            <div class="loader-text">SYNTHESIZING</div>
        </div>
        """
        placeholder = st.empty()
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(duration)
        placeholder.empty()

    @staticmethod
    def render_card_start(extra_styles=""):
        st.markdown(f'<div class="liquid-card anim-enter" style="{extra_styles}">', unsafe_allow_html=True)

    @staticmethod
    def render_card_end():
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 6.0 BUSINESS LOGIC (ROUTING & CONTROLLERS)
# ==============================================================================

# 6.1 HELPER FUNCTIONS
# --------------------
def toggle_theme():
    st.session_state.theme_mode = "Dark" if st.session_state.theme_toggle else "Light"

def go_to_page(page):
    st.session_state.page = page

def reset_interview():
    st.session_state.page = "interview"
    st.session_state.score = None
    st.session_state.ai_results = {}
    st.session_state.inputs = {}

# 6.2 INJECT STYLES
# -----------------
st.markdown(ThemeEngine.generate_css(), unsafe_allow_html=True)

# 6.3 MAIN RENDER LOOP
# --------------------
UILibrary.render_navbar()

# --- HOME PAGE ---
if st.session_state.page == "home":
    st.markdown(f"""
    <div class="anim-enter" style="text-align: center; padding: 80px 0 60px 0;">
        <h1 style="font-size: 5rem; margin-bottom: 20px; line-height: 1.1;">MindCheck AI</h1>
        <p style="font-size: 1.5rem; opacity: 0.7; max-width: 600px; margin: 0 auto;">
            {ContentRepository.APP_SUBTITLE}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3, gap="medium")
    
    with c1:
        st.markdown('<div class="liquid-card anim-enter" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="anim-float" style="font-size: 3.5rem; margin-bottom:20px;">👤</div>', unsafe_allow_html=True)
        st.markdown('<h3>Profile</h3>', unsafe_allow_html=True)
        st.markdown('<p style="opacity:0.6; margin-bottom:30px;">Developer Information.</p>', unsafe_allow_html=True)
        if st.button("About Me!", key="btn_about"):
            go_to_page("about")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        t = ThemeEngine.get_current_theme()
        st.markdown(f'<div class="liquid-card anim-enter" style="text-align:center; height:100%; border:2px solid {t["accent_primary"]};">', unsafe_allow_html=True)
        st.markdown('<div class="anim-float" style="font-size: 3.5rem; margin-bottom:20px;">🧠</div>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:{t["accent_primary"]} !important;">MindCheck AI</h3>', unsafe_allow_html=True)
        st.markdown('<p style="opacity:0.6; margin-bottom:30px;">Start your assessment.</p>', unsafe_allow_html=True)
        if st.button("START CHECK-IN", key="btn_start"):
            go_to_page("interview")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c3:
        st.markdown('<div class="liquid-card anim-enter" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="anim-float" style="font-size: 3.5rem; margin-bottom:20px;">📢</div>', unsafe_allow_html=True)
        st.markdown('<h3>Updates</h3>', unsafe_allow_html=True)
        st.markdown('<p style="opacity:0.6; margin-bottom:30px;">Latest Version News.</p>', unsafe_allow_html=True)
        if st.button("Latest Update", key="btn_update"):
            go_to_page("updates")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- ABOUT PAGE ---
elif st.session_state.page == "about":
    st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 40px;">About Me</h1>', unsafe_allow_html=True)
    t = ThemeEngine.get_current_theme()
    st.markdown(f"""
    <div class="liquid-card" style="text-align: center; max-width: 600px; margin: 0 auto; padding: 80px 40px;">
        <h2 style="font-weight: 300; font-size: 4rem; background: {t['brand_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Hi.</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- UPDATES PAGE ---
elif st.session_state.page == "updates":
    st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom: 40px;">Latest Updates</h1>', unsafe_allow_html=True)
    t = ThemeEngine.get_current_theme()
    st.markdown(f"""
    <div class="liquid-card" style="text-align: center; max-width: 600px; margin: 0 auto; padding: 80px 40px;">
        <h2 style="font-weight: 300; font-size: 4rem; background: {t['brand_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Hello</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- INTERVIEW PAGE ---
elif st.session_state.page == "interview":
    st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align:center; margin-bottom: 10px;">📝 Mental Health Check-In</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; opacity:0.7; margin-bottom: 50px;">Complete the assessment below to unlock your insights.</p>', unsafe_allow_html=True)
    
    with st.form("interview_form"):
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            UILibrary.render_card_start("height: 100%;")
            st.markdown('<div class="section-label">👤 Profile Details</div>', unsafe_allow_html=True)
            age = st.number_input("How old are you?", 10, 100, 15)
            gender = st.selectbox("Gender Identity", ["Male", "Female"])
            academic_level = st.selectbox("Current School Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
            st.markdown('<br><div class="section-label">❤️ Health Metrics</div>', unsafe_allow_html=True)
            sleep = st.number_input("Average Sleep (Hours/Night)", 0.0, 24.0, 8.0, 0.5)
            rel_status = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced"])
            UILibrary.render_card_end()
            
        with c2:
            UILibrary.render_card_start("height: 100%;")
            st.markdown('<div class="section-label">📱 Digital Footprint</div>', unsafe_allow_html=True)
            avg_daily_usage = st.number_input("Daily Screen Time (Hours)", 0.0, 24.0, 4.0, 0.5)
            platform = st.selectbox("Dominant Platform", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
            st.markdown("<br><label style='font-weight:600;'>Self-Perceived Addiction Level (1-10)</label>", unsafe_allow_html=True)
            addiction = st.slider("", 1, 10, 5)
            st.markdown('<br><div class="section-label">⚠️ Impact Assessment</div>', unsafe_allow_html=True)
            affects_perf = st.radio("Does usage affect your grades/work?", ["No", "Yes"], horizontal=True)
            conflicts = st.number_input("Weekly conflicts caused by social media?", 0, 10, 0)
            UILibrary.render_card_end()
            
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn_layout = st.columns([1, 2, 1])[1]
        with col_btn_layout:
            submitted = st.form_submit_button("🏁 ANALYZE MY DATA")
            
        if submitted:
            UILibrary.show_loader(duration=4)
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
                go_to_page("results")
                st.rerun()
            except Exception as e:
                st.error(f"Computation Error: {e}")

# --- RESULTS PAGE ---
elif st.session_state.page == "results":
    st.markdown('<div class="anim-enter">', unsafe_allow_html=True)
    score = st.session_state.score
    data = st.session_state.inputs
    t = ThemeEngine.get_current_theme()
    
    # Recap
    st.markdown(f"""
    <div class="liquid-card" style="padding: 1.2rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; border-left: 6px solid {t['accent_primary']};">
        <div>
            <strong style="color:{t['accent_primary']}; font-size: 0.85rem; letter-spacing: 1.5px; text-transform:uppercase;">ANALYSIS PARAMETERS:</strong>&nbsp;&nbsp;
            <span style="font-size: 0.95rem; opacity:0.8;">
                <b>{data.get('Age')}y/o {data.get('Gender')}</b> • 
                <b>{data.get('Platform')}</b> ({data.get('Avg_Daily_Usage_Hours')}h/day)
            </span>
        </div>
        <div style="font-size:1.5rem;">✅</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header Control
    c_head, c_restart = st.columns([4, 1.2])
    with c_head: st.markdown(f'<h1 style="text-align:left; font-size: 3rem; margin:0;">Mental Health Scorecard</h1>', unsafe_allow_html=True)
    with c_restart:
        if st.button("🔄 Restart?", use_container_width=True):
            UILibrary.show_loader(2)
            reset_interview()
            st.rerun()
            
    # Score Calculation
    if score < 4:
        s_color = t['danger']
        msg = "Immediate Action Recommended"
    elif score < 7:
        s_color = t['warning']
        msg = "Moderate Impact Detected"
    else:
        s_color = t['success']
        msg = "Excellent Mental Balance"
        
    st.markdown(f"""
    <div class="liquid-card" style="text-align: center; border: 2px solid {s_color}; position:relative; overflow:hidden;">
        <div style="position:absolute; top:0; left:0; width:100%; height:8px; background:{s_color}; opacity:0.8;"></div>
        <h3 style="margin-top:20px; opacity:0.6; letter-spacing:4px; font-size:1rem; font-weight:700;">MENTAL HEALTH INDEX</h3>
        <h1 style="font-size: 9rem; font-weight: 900; margin: 10px 0; color: {s_color} !important; text-shadow: 0 0 40px {s_color}44; line-height:1;">
            {score:.1f}<span style="font-size:2.5rem; opacity:0.5; color:{t['text_main']};">/10</span>
        </h1>
        <div style="background:{s_color}22; display:inline-block; padding:10px 25px; border-radius:100px; margin-bottom:20px;">
            <p style="margin:0; color:{s_color} !important; font-weight:700; letter-spacing:0.5px;">{msg}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Grid
    st.markdown(f'<h3 style="text-align:center; color:{t["accent_primary"]}; margin: 50px 0 30px 0;">✨ Generative AI Insights</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    
    with c1:
        st.markdown('<div class="liquid-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="anim-float" style="font-size:2.5rem;">📊</div>', unsafe_allow_html=True)
        st.markdown('<h4>My Persona</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">Deep behavioral analysis.</p>', unsafe_allow_html=True)
        if st.button("Generate", key="btn_persona", use_container_width=True):
            UILibrary.show_loader(4)
            with st.spinner("Analyzing..."):
                prompt = f"Based on: {json.dumps(data)}. Return JSON: {{'persona': 'Fun Title', 'analysis': 'Short analysis', 'tips': ['Tip 1', 'Tip 2']}}"
                res = call_gemini_api(prompt)
                if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="liquid-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="anim-float" style="font-size:2.5rem;">🕰️</div>', unsafe_allow_html=True)
        st.markdown('<h4>Future Self</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">A message from 2029.</p>', unsafe_allow_html=True)
        if st.button("Warp Time", key="btn_future", use_container_width=True):
            UILibrary.show_loader(4)
            with st.spinner("Establishing link..."):
                prompt = f"Write a note from future 2029 self based on habits: {json.dumps(data)}. Max 50 words."
                res = call_gemini_api(prompt, expect_json=False)
                if res: st.session_state.ai_results['future'] = res; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c3:
        st.markdown('<div class="liquid-card" style="text-align:center; height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="anim-float" style="font-size:2.5rem;">🍃</div>', unsafe_allow_html=True)
        st.markdown('<h4>Detox Plan</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.8rem; opacity:0.7;">3-Day cleansing protocol.</p>', unsafe_allow_html=True)
        if st.button("Build Plan", key="btn_detox", use_container_width=True):
            UILibrary.show_loader(4)
            with st.spinner("Drafting..."):
                prompt = f"3-day detox for {data['Platform']} user. JSON: {{'days': [{{'day': 'Day 1', 'theme': 'Theme', 'tasks': ['Task 1']}}]}}"
                res = call_gemini_api(prompt)
                if res: st.session_state.ai_results['detox'] = json.loads(res); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Result Rendering
    if st.session_state.get('ai_results'):
        st.markdown("<br><hr style='opacity:0.2; margin: 3rem 0;'><br>", unsafe_allow_html=True)
        results = st.session_state.ai_results
        
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="liquid-card anim-enter" style="border-left: 5px solid {t['accent_primary']};">
                <h3 style="color:{t['accent_primary']} !important; margin:0;">📊 {r.get('persona', 'User')}</h3>
                <p style="font-style:italic; font-size:1.15rem; opacity:0.9; margin-top:15px;">"{r.get('analysis', '')}"</p>
                <div style="margin-top:25px; padding-top:20px; border-top:1px solid {t['glass_border']};">
                    <strong style="text-transform:uppercase; font-size:0.8rem; letter-spacing:1px; opacity:0.7;">Key Recommendations:</strong>
                    <ul style="margin-top:15px; list-style-type:none; padding:0;">
                        {"".join([f"<li style='margin-bottom:10px; padding-left:20px; position:relative;'><span style='position:absolute; left:0; color:{t['accent_primary']};'>➤</span> {tip}</li>" for tip in r.get('tips', [])])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if 'future' in results:
            st.markdown(f"""
            <div class="liquid-card anim-enter" style="border-left: 5px solid {t['warning']};">
                <h3 style="color:{t['warning']} !important; margin:0;">🕰️ Incoming Transmission (2029)</h3>
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
                <div style='background:rgba(255,255,255,0.03); padding:1.5rem; margin-bottom:15px; border-radius:20px; border:1px solid {t['glass_border']}'>
                    <strong style="color:{t['success']}; font-size:1.2rem; display:block; margin-bottom:10px;">{d.get('day')}: {d.get('theme')}</strong>
                    <ul style="list-style-type:none; padding-left:10px;">{tasks}</ul>
                </div>
                """
            st.markdown(f"""
            <div class="liquid-card anim-enter" style="border-left: 5px solid {t['success']};">
                <h3 style="color:{t['success']} !important; margin:0;">🍃 Detox Challenge</h3>
                {days_html}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7.0 FOOTER
# ==============================================================================
st.markdown(ContentRepository.LEGAL_DISCLAIMER, unsafe_allow_html=True)
st.markdown(f"""
<br><br>
<div style="text-align: center; margin-top: 2rem; opacity: 0.4; font-size: 0.8rem; font-family: 'SF Pro Display'; letter-spacing: 1px;">
    <p>MindCheck AI v6.0.0 • Powered by Gemini • 2026</p>
    <p style="font-size: 0.7rem;">Lumina Glass Engine Active • {st.session_state.theme_mode} Mode</p>
</div>
<br>
""", unsafe_allow_html=True)

# End of Script
