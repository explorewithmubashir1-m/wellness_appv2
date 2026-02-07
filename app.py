# ==============================================================================
# MINDCHECK AI - ONEUI INFRASTRUCTURE EDITION
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

# 4. ONEUI CSS ENGINE
themes = {
    "Dark": {
        "bg": "#000000",
        "card_bg": "#1C1C1E",
        "text": "#FFFFFF",
        "sub_text": "#999999",
        "accent": "#3E91FF",
        "divider": "#2C2C2E"
    },
    "Light": {
        "bg": "#F2F2F7",
        "card_bg": "#FFFFFF",
        "text": "#000000",
        "sub_text": "#8E8E93",
        "accent": "#007AFF",
        "divider": "#E5E5EA"
    }
}
c = themes[st.session_state.theme_mode]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {{ background-color: {c['bg']}; color: {c['text']}; font-family: 'Inter', sans-serif; }}
    
    /* Reachability Area - Push content down */
    .reachability-spacer {{ height: 80px; }}
    
    /* OneUI Typography */
    h1 {{ font-weight: 700; font-size: 3rem; letter-spacing: -0.5px; margin-bottom: 0.5rem; color: {c['text']}; }}
    h2 {{ font-weight: 600; font-size: 1.5rem; color: {c['text']}; }}
    h3, h4 {{ font-weight: 600; color: {c['text']}; margin-bottom: 5px; }}
    p {{ color: {c['sub_text']}; font-size: 1rem; }}
    
    /* OneUI Squircle Cards */
    .oneui-card {{
        background-color: {c['card_bg']};
        border-radius: 22px; 
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.01);
    }}
    
    /* OneUI Buttons */
    .stButton > button {{
        background-color: {c['accent']} !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        height: 50px;
        font-weight: 600;
        border: none;
        width: 100%;
        font-size: 1.1rem;
    }}
    .stButton > button:hover {{ opacity: 0.9; }}
    
    /* Grouped List Input Style */
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > div {{
        background-color: {c['card_bg']} !important;
        border: none !important;
        border-bottom: 1px solid {c['divider']} !important;
        color: {c['text']} !important;
        border-radius: 0 !important;
        padding-left: 0 !important;
    }}
    
    /* Navigation */
    .nav-bar {{ padding: 10px 0; border-bottom: 1px solid {c['divider']}; margin-bottom: 20px; }}
    
    /* Footer */
    .footer {{ text-align: center; margin-top: 60px; padding-top: 20px; color: {c['sub_text']}; font-size: 0.8rem; }}
</style>
""", unsafe_allow_html=True)

# 5. UI COMPONENTS
def render_navbar():
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    c1, c2 = st.columns([8, 2])
    with c1: 
        if st.button(" < Back", key="back_btn"): go_to_page("home"); st.rerun()
    with c2:
        st.toggle("Dark", value=(st.session_state.theme_mode=="Dark"), key="theme_toggle", on_change=toggle_theme)
    st.markdown('</div>', unsafe_allow_html=True)

def show_loader(duration=3):
    with st.spinner("Processing..."): time.sleep(duration)

# 6. PAGES
render_navbar()

if st.session_state.page == "home":
    # Reachability Header
    st.markdown("<div class='reachability-spacer'></div>", unsafe_allow_html=True)
    
    # Title Logic: Strict solid colors for OneUI Cleanliness (No gradients)
    title_color = c['text'] 
    
    st.markdown(f"<h1 style='color: {title_color};'>MindCheck</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: {c['accent']}; margin-top:-20px;'>AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin-bottom: 40px;'>Your digital wellness companion.</p>", unsafe_allow_html=True)
    
    # OneUI Grid
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown(f'<div class="oneui-card"><h2>Creator</h2><p style="margin-bottom:20px;">Mubashir Mohsin</p></div>', unsafe_allow_html=True)
        if st.button("Read Story", use_container_width=True): go_to_page("about"); st.rerun()
    with c2:
        st.markdown(f'<div class="oneui-card"><h2 style="color:{c["accent"]}">Check-In</h2><p style="margin-bottom:20px;">Start Assessment</p></div>', unsafe_allow_html=True)
        if st.button("Start", use_container_width=True): go_to_page("interview"); st.rerun()

elif st.session_state.page == "about":
    st.markdown("<div class='reachability-spacer'></div>", unsafe_allow_html=True)
    st.markdown(f"<h1>About the<br>Creator</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="oneui-card">
        <p style="color: {c['text']}; font-size: 1.1rem; line-height: 1.6;">
        "My name is <b>Mubashir Mohsin</b>, and I’m a 6th grader. I was inspired to create this web app after noticing a decline in my own grades. That spark led to a successful journey of building the Mental Health Calculator, which is powered by my very own <b>MindCheck AI</b>. I also want to give a quick shout-out to <b>Gemini AI</b> for helping me bring this project to life!"
        </p>
        <p style="margin-top: 20px; font-weight: 600; color: {c['sub_text']}">- February 6, 2026</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "interview":
    st.markdown("<div class='reachability-spacer'></div>", unsafe_allow_html=True)
    st.markdown("<h1>Check-In</h1>", unsafe_allow_html=True)
    
    with st.form("interview_form"):
        # Grouped Settings Look
        st.markdown(f'<div class="oneui-card">', unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:{c['accent']}'>Personal Info</h4>", unsafe_allow_html=True)
        age = st.number_input("Age", 10, 100, 15)
        gender = st.selectbox("Gender", ["Male", "Female"])
        ac_level = st.selectbox("Education Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="oneui-card">', unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:{c['accent']}'>Digital Habits</h4>", unsafe_allow_html=True)
        usage = st.number_input("Daily Screen Time (Hrs)", 0.0, 24.0, 4.0)
        plat = st.selectbox("Main Platform", ["TikTok", "YouTube", "Instagram", "Snapchat"])
        sleep = st.number_input("Sleep (Hrs)", 0.0, 24.0, 8.0)
        addiction = st.slider("Addiction Level", 1, 10, 5)
        conflicts = st.number_input("Conflicts", 0, 10, 0)
        perf = st.radio("Affects Grades?", ["No", "Yes"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("Analyze"):
            show_loader()
            st.session_state.inputs = {"Age": age, "Gender": gender, "Platform": plat, "Sleep": sleep}
            # Simplified Scoring
            base = 10 - (usage * 0.3) - (addiction * 0.2)
            st.session_state.score = max(1, min(10, base))
            go_to_page("results")
            st.rerun()

elif st.session_state.page == "results":
    score = st.session_state.score
    
    st.markdown("<div class='reachability-spacer'></div>", unsafe_allow_html=True)
    
    # Big Clean Score Display
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-size: 8rem; color: {c['accent']}; margin: 0;">{score:.1f}</h1>
        <p style="font-size: 1.5rem;">Wellness Score</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='margin-left: 10px; margin-bottom: 15px;'>AI Features</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown(f'<div class="oneui-card" style="height:100%"><h3>👤 Profile</h3><p>Analysis</p></div>', unsafe_allow_html=True)
        if st.button("Generate", key="btn_gen", use_container_width=True):
             show_loader()
             prompt = f"Based on this user data: {json.dumps(st.session_state.inputs)}. Return JSON with keys: 'persona', 'analysis', 'tips'."
             res = call_gemini(prompt)
             if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
    with c2:
        st.markdown(f'<div class="oneui-card" style="height:100%"><h3>⏳ Time</h3><p>Travel</p></div>', unsafe_allow_html=True)
        if st.button("Connect", key="btn_con", use_container_width=True):
             show_loader()
             prompt = f"Write a note from future self in 2029 based on: {json.dumps(st.session_state.inputs)}. Max 50 words."
             res = call_gemini(prompt, is_json=False)
             if res: st.session_state.ai_results['future'] = res; st.rerun()
    
    results = st.session_state.ai_results
    if results:
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
        if 'analysis' in results:
             r = results['analysis']
             st.markdown(f"<div class='oneui-card'><h3>{r.get('persona', 'User')}</h3><p>{r.get('analysis')}</p></div>", unsafe_allow_html=True)
        if 'future' in results:
             st.markdown(f"<div class='oneui-card'><h3>Incoming Message</h3><p>{results['future']}</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start Over", use_container_width=True): reset_interview(); st.rerun()

# 7. FOOTER
st.markdown(f"<div class='footer'><p>MindCheck AI v2.0 • Empowered by Gemini Models • 2026</p></div>", unsafe_allow_html=True)
