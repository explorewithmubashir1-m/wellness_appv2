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

# --- FILE CONFIGURATION ---
FAVICON_FILENAME = "Gemini_Generated_Image_7yh2m17yh2m17yh2.png"
LOGO_FILENAME = "Gemini_Generated_Image_7yh2m17yh2m17yh2.png"

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Mental Health V2",
    page_icon=FAVICON_FILENAME,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONFIGURATION ---
MODEL_FILE = 'mental_health_model.joblib' 
GEMINI_MODEL = 'gemini-2.5-flash'
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# --- STATE MANAGEMENT ---
if "page" not in st.session_state:
    st.session_state.page = "interview"
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"
if "ai_results" not in st.session_state:
    st.session_state.ai_results = {} 
if "score" not in st.session_state:
    st.session_state.score = None
if "inputs" not in st.session_state:
    st.session_state.inputs = {}

def toggle_theme():
    if st.session_state.theme_toggle:
        st.session_state.theme_mode = "Dark"
    else:
        st.session_state.theme_mode = "Light"

def go_to_results():
    st.session_state.page = "results"

def reset_interview():
    st.session_state.page = "interview"
    st.session_state.ai_results = {}
    st.session_state.score = None
    st.session_state.inputs = {}

# --- CUSTOM LOADER (Flexible Duration) ---
def show_custom_loader(duration=4):
    """
    Displays the 'Synthesizing Information' loader.
    Args:
        duration (int): How many seconds to show the loader.
    """
    loader_html = """
    <style>
        .loader-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.95);
            z-index: 99999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(8px);
        }
        .loader-container { position: relative; width: 120px; height: 120px; }
        .ring { position: absolute; border-radius: 50%; border: 4px solid transparent; }
        .ring-1 {
            top: 0; left: 0; width: 100%; height: 100%;
            border-top-color: #0ea5e9; border-right-color: #0ea5e9;
            animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
        }
        .ring-2 {
            top: 15%; left: 15%; width: 70%; height: 70%;
            border-bottom-color: #a855f7; border-left-color: #a855f7;
            animation: spin-reverse 2s linear infinite;
        }
        .heart-core {
            position: absolute; top: 50%; left: 50%; width: 30px; height: 30px;
            background: #ec4899; transform: translate(-50%, -50%) rotate(45deg);
            animation: heartbeat 1.2s ease-in-out infinite; box-shadow: 0 0 20px #ec4899;
        }
        .heart-core:before, .heart-core:after {
            content: ""; position: absolute; width: 30px; height: 30px;
            background: #ec4899; border-radius: 50%;
        }
        .heart-core:before { left: -15px; } .heart-core:after { top: -15px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes spin-reverse { 0% { transform: rotate(360deg); } 100% { transform: rotate(-360deg); } }
        @keyframes heartbeat {
            0% { transform: translate(-50%, -50%) rotate(45deg) scale(0.8); opacity: 0.8; }
            50% { transform: translate(-50%, -50%) rotate(45deg) scale(1.1); opacity: 1; }
            100% { transform: translate(-50%, -50%) rotate(45deg) scale(0.8); opacity: 0.8; }
        }
        .loading-text {
            margin-top: 40px; color: #e2e8f0; font-family: 'Courier New', monospace;
            font-size: 1.2rem; letter-spacing: 2px; font-weight: 600;
            text-transform: uppercase; display: flex; align-items: center;
        }
        .loading-text::after {
            content: "█"; margin-left: 5px; animation: blink 0.8s infinite; color: #0ea5e9;
        }
        @keyframes blink { 0%, 100% { opacity: 0; } 50% { opacity: 1; } }
    </style>
    <div class="loader-overlay">
        <div class="loader-container">
            <div class="ring ring-1"></div>
            <div class="ring ring-2"></div>
            <div class="heart-core"></div>
        </div>
        <div class="loading-text">SYNTHESIZING INFORMATION</div>
    </div>
    """
    placeholder = st.empty()
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    time.sleep(duration) 
    placeholder.empty()

# --- DYNAMIC BACKGROUND ---
def get_background_style(theme_mode, score):
    gradients = {
        "Dark": "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)", 
        "Light": "linear-gradient(120deg, #f0f9ff 0%, #cbebff 100%)" 
    }
    base_bg = gradients[theme_mode]
    
    if st.session_state.page == "interview" or score is None:
        return base_bg

    emoji = "🌟" if score >= 6 else "🌧️" 
    svg = f"""
    <svg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'>
        <text x='50%' y='50%' font-size='35' text-anchor='middle' dominant-baseline='middle' opacity='0.15'>{emoji}</text>
    </svg>
    """
    b64_svg = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"url('data:image/svg+xml;base64,{b64_svg}'), {base_bg}"

# --- THEME PALETTES ---
themes = {
    "Dark": {
        "text_main": "#ffffff",
        "text_header": "#d1d5db", 
        "card_bg": "rgba(30, 41, 59, 0.7)", 
        "card_border": "rgba(255, 255, 255, 0.1)",
        "score_box_bg": "rgba(0,0,0,0.3)",
        "button_grad": "linear-gradient(90deg, #6366f1, #8b5cf6)", 
        "highlight": "#a78bfa"
    },
    "Light": {
        "text_main": "#1e293b", 
        "text_header": "#475569",
        "card_bg": "rgba(255, 255, 255, 0.9)", 
        "card_border": "#e2e8f0",
        "score_box_bg": "rgba(255,255,255,0.6)",
        "button_grad": "linear-gradient(90deg, #3b82f6, #06b6d4)", 
        "highlight": "#0ea5e9"
    }
}

current_theme = themes[st.session_state.theme_mode]
current_bg = get_background_style(st.session_state.theme_mode, st.session_state.get('score'))

# --- CSS STYLING ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    .stApp {{
        background: {current_bg};
        color: {current_theme['text_main']};
        font-family: 'Poppins', sans-serif;
        transition: background 0.5s ease;
    }}

    /* Global Text Colors */
    h1, h2, h3, h4, h5, h6, p, label {{ color: {current_theme['text_main']} !important; }}
    
    /* INPUT FIELDS - FORCE WHITE BG / BLACK TEXT */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 10px;
    }}
    
    /* Dropdown text fix */
    div[data-baseweb="select"] > div {{ background-color: #ffffff !important; color: #000000 !important; }}
    div[data-testid="stSelectbox"] div[class*="st-"] {{ color: #000000 !important; }}
    
    /* Buttons */
    .stButton > button {{
        background: {current_theme['button_grad']} !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }}
    .stButton > button:hover {{ transform: scale(1.05); }}

    /* Cards */
    .glass-card {{
        background: {current_theme['card_bg']};
        border: 1px solid {current_theme['card_border']};
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    /* Headers */
    .section-title {{
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 1rem;
        color: {current_theme['highlight']} !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}
    
    /* Score Box */
    .score-container {{
        text-align: center;
        padding: 3rem;
        border-radius: 30px;
        background: {current_theme['score_box_bg']};
        border: 1px solid {current_theme['card_border']};
        margin: 2rem 0;
    }}
    
    li {{ padding-left: 1.5em; text-indent: -1.5em; margin-bottom: 10px; font-weight: 500; }}
    li::before {{ content: "●"; color: {current_theme['highlight']}; padding-right: 10px; }}
    
</style>
""", unsafe_allow_html=True)

# --- LOAD MODEL ---
@st.cache_resource
def load_ml_model():
    try:
        return joblib.load(MODEL_FILE)
    except:
        return None
model = load_ml_model()

# --- GEMINI FUNCTION ---
def call_gemini(prompt, is_json=True):
    if not API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    if is_json: payload["generationConfig"] = {"responseMimeType": "application/json"}
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
    except: pass
    return None

MODEL_COLUMNS = [
    'Age', 'Gender', 'Academic_Level', 'Avg_Daily_Usage_Hours', 'Affects_Academic_Performance', 'Sleep_Hours_Per_Night', 'Conflicts_Over_Social_Media', 'Addicted_Score', 'Most_Used_Platform_Facebook', 'Most_Used_Platform_Instagram', 'Most_Used_Platform_KakaoTalk', 'Most_Used_Platform_LINE', 'Most_Used_Platform_LinkedIn', 'Most_Used_Platform_Snapchat', 'Most_Used_Platform_TikTok', 'Most_Used_Platform_Twitter', 'Most_Used_Platform_VKontakte', 'Most_Used_Platform_WeChat', 'Most_Used_Platform_WhatsApp', 'Most_Used_Platform_YouTube', 'Relationship_Status_Complicated', 'Relationship_Status_In Relationship', 'Relationship_Status_Single']

# ==========================================
# TOP NAVIGATION BAR
# ==========================================
top_col1, top_col2, top_col3 = st.columns([1, 6, 2])

with top_col1:
    if os.path.exists(LOGO_FILENAME):
        st.image(LOGO_FILENAME, width=150) 
    else:
        st.markdown(f"### 💜 Mental Health V2") 
        st.caption("Logo not found.")

with top_col3:
    st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
    st.toggle("Dark Mode", value=(st.session_state.theme_mode == "Dark"), key="theme_toggle", on_change=toggle_theme)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# PAGE 1: THE INTERVIEW
# ==========================================
if st.session_state.page == "interview":
    st.markdown(f'<h1 style="text-align:center; font-size: 3rem; margin-top:1rem;">📝 Mental Health Check-In</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; opacity:0.8; margin-bottom:3rem;">Answer a few questions to unlock your digital Mental Health score.</p>', unsafe_allow_html=True)

    with st.form("interview_form"):
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown('<div class="section-title">👤 About You</div>', unsafe_allow_html=True)
            age = st.number_input("How old are you?", 10, 100, 15)
            gender = st.selectbox("Gender", ["Male", "Female"])
            academic_level = st.selectbox("Current School Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
            
            st.markdown('<div class="section-title">❤️ Health & Life</div>', unsafe_allow_html=True)
            sleep = st.number_input("Average Sleep (Hours)", 0.0, 24.0, 8.0, 0.5)
            rel_status = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced"])

        with c2:
            st.markdown('<div class="section-title">📱 Digital Habits</div>', unsafe_allow_html=True)
            avg_daily_usage = st.number_input("Daily Screen Time (Hours)", 0.0, 24.0, 4.0, 0.5)
            platform = st.selectbox("Most Used App", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
            addiction = st.slider("Self-Perceived Addiction (1-10)", 1, 10, 5)
            
            st.markdown('<div class="section-title">⚠️ Impact</div>', unsafe_allow_html=True)
            affects_perf = st.radio("Does it affect your grades?", ["No", "Yes"], horizontal=True)
            conflicts = st.number_input("Arguments caused by social media?", 0, 10, 0)

        st.markdown("<br><br>", unsafe_allow_html=True)
        col_dummy1, col_btn, col_dummy2 = st.columns([1, 2, 1])
        with col_btn:
            submitted = st.form_submit_button("🏁 FINISH & ANALYZE")
            
        if submitted:
            show_custom_loader(duration=4) # 4 seconds for analysis
            st.session_state.inputs = {
                "Age": age, "Gender": gender, "Academic_Level": academic_level,
                "Avg_Daily_Usage_Hours": avg_daily_usage, "Platform": platform,
                "Addiction": addiction, "Sleep": sleep, "Relationship": rel_status,
                "Affects_Performance": affects_perf, "Conflicts": conflicts
            }
            
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
                    mental_health = model.predict(input_df)[0]
                else:
                    base = 10 - (avg_daily_usage * 0.3) - (addiction * 0.2) + (sleep * 0.2)
                    mental_health = max(1, min(10, base))

                st.session_state.score = mental_health
                go_to_results()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# PAGE 2: THE RESULTS DASHBOARD
# ==========================================
elif st.session_state.page == "results":
    score = st.session_state.score
    data = st.session_state.inputs
    
    # --- INPUT SUMMARY / PARAMETER RECAP ---
    st.markdown(f"""
    <div class="glass-card" style="padding: 1rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; border-left: 5px solid {current_theme['highlight']};">
        <div>
            <strong style="color:{current_theme['highlight']}; font-size: 0.9rem;">RECAP:</strong>&nbsp;&nbsp;
            <span style="font-size: 0.9rem;">
                <b>{data.get('Age')}y/o {data.get('Gender')}</b> • 
                <b>{data.get('Platform')}</b> ({data.get('Avg_Daily_Usage_Hours')}h/day) • 
                Sleep: <b>{data.get('Sleep')}h</b> • 
                Addiction: <b>{data.get('Addiction')}/10</b>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Restart Button (Top Right of results area)
    col_head_1, col_head_2 = st.columns([4, 1])
    with col_head_1:
        st.markdown(f'<h1 style="text-align:left; font-size: 3rem;">Your <span style="color:{current_theme["highlight"]}">Results</span> are In!</h1>', unsafe_allow_html=True)
    with col_head_2:
        if st.button("🔄 Restart?", use_container_width=True):
            show_custom_loader(duration=2) # 2 seconds for reset
            reset_interview()
            st.rerun()
    
    score_color = "#FF6B6B" if score < 4 else "#FFD93D" if score < 7 else "#6BCB77"
    st.markdown(f"""
    <div class="score-container">
        <h3 style="margin:0; opacity:0.7; letter-spacing:2px; font-size:1rem;">Mental Health SCORE</h3>
        <h1 style="font-size: 6rem; font-weight: 800; margin: 0; color: {score_color} !important;">
            {score:.1f}<span style="font-size:2rem; opacity:0.5;">/10</span>
        </h1>
        <p style="opacity:0.8;">{ "Doing great!" if score > 7 else "Needs some attention." if score > 4 else "Time for a detox?" }</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<h3 style="text-align:center; color:{current_theme["highlight"]}; margin-bottom:20px;">✨ AI Insights</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("📊 My Persona"):
            show_custom_loader(duration=4)
            with st.spinner("Finalizing..."):
                prompt = f"Based on: {json.dumps(data)}. Return JSON: {{'persona': 'Fun Title', 'analysis': 'Short analysis', 'tips': ['Tip 1', 'Tip 2']}}"
                res = call_gemini(prompt)
                if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🕰️ Future Self"):
            show_custom_loader(duration=4)
            with st.spinner("Connecting..."):
                prompt = f"Write a note from future 2029 self based on habits: {json.dumps(data)}. Max 50 words."
                res = call_gemini(prompt, is_json=False)
                if res: st.session_state.ai_results['future'] = res; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🍃 Detox Plan"):
            show_custom_loader(duration=4)
            with st.spinner("Planning..."):
                prompt = f"3-day detox for {data['Platform']} user. JSON: {{'days': [{{'day': 'Day 1', 'theme': 'Theme', 'tasks': ['Task 1', 'Task 2']}}]}}"
                res = call_gemini(prompt)
                if res: st.session_state.ai_results['detox'] = json.loads(res); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get('ai_results'):
        st.markdown("<br>", unsafe_allow_html=True)
        results = st.session_state.ai_results
        
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color:#0ea5e9 !important;">📊 {r.get('persona', 'User')}</h3>
                <p>"{r.get('analysis', '')}"</p>
                <hr style="opacity:0.2;">
                <strong>💡 Quick Tips:</strong>
                <ul>{"".join([f"<li>{t}</li>" for t in r.get('tips', [])])}</ul>
            </div>
            """, unsafe_allow_html=True)

        if 'future' in results:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 8px solid #FFD93D;">
                <h3 style="color:#FFD93D !important;">🕰️ Message from 2029</h3>
                <p style="font-family:monospace; background:rgba(0,0,0,0.05); padding:1rem; border-radius:10px;">{results['future']}</p>
            </div>
            """, unsafe_allow_html=True)

        if 'detox' in results:
            r = results['detox']
            days_html = ""
            for d in r.get('days', []):
                tasks = "".join([f"<li>{t}</li>" for t in d.get('tasks', [])])
                days_html += f"<div style='background:{current_theme['card_bg']}; padding:1rem; margin-bottom:10px; border-radius:10px; border:1px solid {current_theme['card_border']}'><strong>{d.get('day')}: {d.get('theme')}</strong><ul>{tasks}</ul></div>"
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color:#22c55e !important;">🍃 Detox Challenge</h3>
                {days_html}
            </div>
            """, unsafe_allow_html=True)
