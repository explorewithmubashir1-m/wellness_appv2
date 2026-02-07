# ==============================================================================
# MINDCHECK AI - MATERIAL 3 EXPRESSIVE EDITION
# ==============================================================================
import streamlit as st
import pandas as pd
import joblib
import json
import time
import requests
import os

# 1. CONFIGURATION
FAVICON_FILENAME = "Gemini_Generated_Image_g704tpg704tpg704.png"
LOGO_FILENAME = "Gemini_Generated_Image_g704tpg704tpg704.png"
MODEL_FILE = 'mental_health_model.joblib' 
GEMINI_MODEL = 'gemini-2.5-flash'
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

st.set_page_config(page_title="MindCheck AI", page_icon=FAVICON_FILENAME, layout="wide", initial_sidebar_state="collapsed")

# 2. STATE MANAGEMENT
if "page" not in st.session_state: st.session_state.page = "home"
if "theme_mode" not in st.session_state: st.session_state.theme_mode = "Light"
if "ai_results" not in st.session_state: st.session_state.ai_results = {} 
if "score" not in st.session_state: st.session_state.score = None
if "inputs" not in st.session_state: st.session_state.inputs = {}

# 3. CORE LOGIC
def toggle_theme():
    st.session_state.theme_mode = "Dark" if st.session_state.theme_toggle else "Light"

def go_to_page(page_name):
    st.session_state.page = page_name

def reset_interview():
    st.session_state.page = "interview"
    st.session_state.ai_results = {}
    st.session_state.score = None
    st.session_state.inputs = {}

@st.cache_resource
def load_ml_model():
    try: return joblib.load(MODEL_FILE)
    except: return None

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

model = load_ml_model()
MODEL_COLUMNS = ['Age', 'Gender', 'Academic_Level', 'Avg_Daily_Usage_Hours', 'Affects_Academic_Performance', 'Sleep_Hours_Per_Night', 'Conflicts_Over_Social_Media', 'Addicted_Score', 'Most_Used_Platform_Facebook', 'Most_Used_Platform_Instagram', 'Most_Used_Platform_KakaoTalk', 'Most_Used_Platform_LINE', 'Most_Used_Platform_LinkedIn', 'Most_Used_Platform_Snapchat', 'Most_Used_Platform_TikTok', 'Most_Used_Platform_Twitter', 'Most_Used_Platform_VKontakte', 'Most_Used_Platform_WeChat', 'Most_Used_Platform_WhatsApp', 'Most_Used_Platform_YouTube', 'Relationship_Status_Complicated', 'Relationship_Status_In Relationship', 'Relationship_Status_Single']

# 4. MATERIAL 3 CSS ENGINE
themes = {
    "Dark": {
        "bg": "#141218",
        "surface": "#1D1B20",
        "surface_container": "#2B2930",
        "surface_bright": "#36343B",
        "primary": "#D0BCFF",
        "on_primary": "#381E72",
        "primary_container": "#4F378B",
        "text": "#E6E1E5",
        "outline": "#938F99"
    },
    "Light": {
        "bg": "#FEF7FF",
        "surface": "#F7F2FA",
        "surface_container": "#F3EDF7",
        "surface_bright": "#EADDFF",
        "primary": "#6750A4",
        "on_primary": "#FFFFFF",
        "primary_container": "#EADDFF",
        "text": "#1D1B20",
        "outline": "#79747E"
    }
}
c = themes[st.session_state.theme_mode]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    .stApp {{ background-color: {c['bg']}; color: {c['text']}; font-family: 'Roboto', sans-serif; }}
    
    /* M3 Navigation Bar */
    .m3-nav {{
        display: flex; align-items: center; justify-content: space-between;
        background-color: {c['surface_container']}; border-radius: 100px;
        padding: 12px 24px; margin-bottom: 40px;
    }}
    
    /* M3 Cards */
    .m3-card {{
        background-color: {c['surface_container']};
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 16px;
        transition: background-color 0.2s ease;
        height: 100%;
        display: flex; flex-direction: column; justify-content: space-between;
    }}
    .m3-card:hover {{ background-color: {c['surface_bright']}; }}
    
    /* M3 Typography */
    h1 {{ font-weight: 400; letter-spacing: -0.5px; color: {c['text']}; font-size: 3.5rem; }}
    h2 {{ font-weight: 400; color: {c['text']}; }}
    h3, h4 {{ font-weight: 500; color: {c['text']}; margin-bottom: 0.5rem; }}
    p, li {{ color: {c['text']}; opacity: 0.8; line-height: 1.6; font-size: 1rem; }}
    
    /* M3 Buttons (Pills) */
    .stButton > button {{
        border-radius: 100px !important;
        height: 48px;
        background-color: {c['primary']} !important;
        color: {c['on_primary']} !important;
        border: none;
        font-weight: 500;
        letter-spacing: 0.1px;
        transition: box-shadow 0.2s;
        text-transform: none;
        padding: 0 24px;
    }}
    .stButton > button:hover {{ box-shadow: 0 1px 3px 1px rgba(0,0,0,0.15); opacity: 0.9; }}
    
    /* M3 Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {{
        background-color: {c['surface']} !important;
        border: 1px solid {c['outline']} !important;
        border-radius: 4px 4px 0 0 !important;
        border-bottom: 2px solid {c['outline']} !important;
        color: {c['text']} !important;
    }}
    .stSelectbox > div > div > div {{ background-color: {c['surface']} !important; color: {c['text']} !important; border-radius: 8px !important; }}
    div[data-baseweb="popover"] {{ background-color: {c['surface']} !important; }}
    div[role="option"] {{ color: {c['text']} !important; }}
    
    /* Footer */
    .footer {{ text-align: center; margin-top: 80px; padding-top: 20px; border-top: 1px solid {c['outline']}33; opacity: 0.6; font-size: 0.8rem; }}
</style>
""", unsafe_allow_html=True)

# 5. UI COMPONENTS
def render_navbar():
    st.markdown('<div class="m3-nav">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2,6,2])
    with c1: st.markdown(f"<span style='font-weight:700; font-size:1.2rem; color:{c['primary']}'>MindCheck AI</span>", unsafe_allow_html=True)
    with c2: 
        if st.button("Home", key="nav_home", use_container_width=True): go_to_page("home"); st.rerun()
    with c3:
        st.toggle("Dark Mode", value=(st.session_state.theme_mode=="Dark"), key="theme_toggle", on_change=toggle_theme)
    st.markdown('</div>', unsafe_allow_html=True)

def show_loader(duration=3):
    with st.spinner("Processing..."): time.sleep(duration)

# 6. PAGES
render_navbar()

if st.session_state.page == "home":
    # Title Logic
    title_style = f"font-size: 5rem; text-align: center; margin-bottom: 1rem; color: {c['text']};"
    if st.session_state.theme_mode == "Light":
        title_style += f" background: linear-gradient(45deg, {c['primary']}, #9C27B0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
    
    st.markdown(f"<h1 style='{title_style}'>MindCheck AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; max-width: 600px; margin: 0 auto 4rem auto;'>Material 3 Edition. Your digital wellbeing companion.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="m3-card" style="text-align:center;"><h3>👨‍💻 Creator</h3><p>Meet Mubashir Mohsin and read his story.</p></div>', unsafe_allow_html=True)
        if st.button("View Story", use_container_width=True): go_to_page("about"); st.rerun()
    with col2:
        st.markdown('<div class="m3-card" style="text-align:center;"><h3>🧠 Check-In</h3><p>Start your comprehensive assessment.</p></div>', unsafe_allow_html=True)
        if st.button("Start Now", type="primary", use_container_width=True): go_to_page("interview"); st.rerun()

elif st.session_state.page == "about":
    st.markdown(f"<h1 style='text-align:center;'>About the Creator</h1>", unsafe_allow_html=True)
    col_centered = st.columns([1,2,1])[1]
    with col_centered:
        st.markdown(f"""
        <div class="m3-card" style="line-height: 1.8; padding: 40px;">
            <p style="font-size: 1.1rem;">"My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"</p>
            <p style="text-align: right; opacity: 0.6; font-size: 0.9rem; margin-top: 20px;">- February 6, 2026</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == "interview":
    st.markdown("<h1 style='text-align:center;'>Check-In</h1>", unsafe_allow_html=True)
    with st.form("interview_form"):
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.markdown('<div class="m3-card">', unsafe_allow_html=True)
            st.markdown("### Profile")
            age = st.number_input("Age", 10, 100, 15)
            gender = st.selectbox("Gender", ["Male", "Female"])
            ac_level = st.selectbox("Education", ["High School", "Undergraduate", "Graduate", "Middle School"])
            sleep = st.number_input("Sleep (Hrs)", 0.0, 24.0, 8.0)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="m3-card">', unsafe_allow_html=True)
            st.markdown("### Habits")
            usage = st.number_input("Screen Time (Hrs)", 0.0, 24.0, 4.0)
            plat = st.selectbox("Platform", ["TikTok", "YouTube", "Instagram", "Snapchat", "Other"])
            addiction = st.slider("Addiction (1-10)", 1, 10, 5)
            conflicts = st.number_input("Weekly Conflicts", 0, 10, 0)
            perf = st.radio("Affects Grades?", ["No", "Yes"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("Analyze Data", use_container_width=True):
            show_loader()
            st.session_state.inputs = {"Age": age, "Gender": gender, "Platform": plat, "Sleep": sleep}
            # Simplified Scoring for Demo
            base = 10 - (usage * 0.3) - (addiction * 0.2)
            st.session_state.score = max(1, min(10, base))
            go_to_page("results")
            st.rerun()

elif st.session_state.page == "results":
    score = st.session_state.score
    
    st.markdown(f"""
    <div class="m3-card" style="text-align: center; padding: 60px; background-color: {c['primary_container']}; margin-bottom: 40px;">
        <h4 style="margin:0; opacity: 0.7; color: {c['on_primary']};">WELLNESS SCORE</h4>
        <h1 style="font-size: 8rem; margin: 0; color: {c['primary']} !important;">{score:.1f}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin-bottom: 20px;'>AI Insights</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    
    with c1:
        st.markdown(f'<div class="m3-card" style="height:100%"><h4>👤 Profile Analysis</h4><p>Deep dive into patterns.</p></div>', unsafe_allow_html=True)
        if st.button("Generate Persona", use_container_width=True):
             show_loader()
             prompt = f"Based on this user data: {json.dumps(st.session_state.inputs)}. Return JSON with keys: 'persona', 'analysis', 'tips'."
             res = call_gemini(prompt)
             if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
             
    with c2:
        st.markdown(f'<div class="m3-card" style="height:100%"><h4>⏳ Time Travel</h4><p>Message from 2029.</p></div>', unsafe_allow_html=True)
        if st.button("Connect to Future", use_container_width=True):
             show_loader()
             prompt = f"Write a note from future self in 2029 based on: {json.dumps(st.session_state.inputs)}. Max 50 words."
             res = call_gemini(prompt, is_json=False)
             if res: st.session_state.ai_results['future'] = res; st.rerun()
    
    # Render Results
    results = st.session_state.ai_results
    if results:
        st.markdown("<hr style='margin: 40px 0; opacity:0.2'>", unsafe_allow_html=True)
        if 'analysis' in results:
             r = results['analysis']
             st.markdown(f"<div class='m3-card'><h3>{r.get('persona', 'User')}</h3><p>{r.get('analysis')}</p></div>", unsafe_allow_html=True)
        if 'future' in results:
             st.markdown(f"<div class='m3-card' style='background:{c['surface_bright']}'><h3>Incoming Message</h3><p>{results['future']}</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start Over", type="secondary", use_container_width=True): reset_interview(); st.rerun()

# 7. FOOTER
st.markdown(f"<div class='footer'><p>MindCheck AI v2.0 • Empowered by Gemini Models • 2026</p></div>", unsafe_allow_html=True)
