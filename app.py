import streamlit as st
import pandas as pd
import joblib
import json
import time
import requests
import numpy as np
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Social Impact AI",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar initially for focus
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

# --- DYNAMIC BACKGROUND ---
def get_background_style(theme_mode, score):
    gradients = {
        "Dark": "linear-gradient(135deg, #240b36 0%, #2d3436 74%)", 
        "Light": "linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)" 
    }
    base_bg = gradients[theme_mode]
    
    # Only show emojis in result mode
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
        "card_bg": "rgba(40, 40, 60, 0.5)",
        "card_border": "rgba(255, 255, 255, 0.15)",
        "score_box_bg": "rgba(0,0,0,0.2)",
        "button_grad": "linear-gradient(90deg, #8E2DE2, #4A00E0)", 
        "highlight": "#c084fc"
    },
    "Light": {
        "text_main": "#2c3e50", 
        "text_header": "#576574",
        "card_bg": "rgba(255, 255, 255, 0.85)", 
        "card_border": "#ffffff",
        "score_box_bg": "rgba(255,255,255,0.5)",
        "button_grad": "linear-gradient(90deg, #FF9966, #FF5E62)", 
        "highlight": "#FF5E62"
    }
}

current_theme = themes[st.session_state.theme_mode]
current_bg = get_background_style(st.session_state.theme_mode, st.session_state.get('score'))

# --- CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    .stApp {{
        background: {current_bg};
        color: {current_theme['text_main']};
        font-family: 'Poppins', sans-serif;
        transition: background 0.5s ease;
    }}

    h1, h2, h3, h4, h5, h6, p, label {{ color: {current_theme['text_main']} !important; }}
    
    /* INPUT FIELDS - GLOBAL OVERRIDE (White Box / Black Text) */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 10px;
    }}
    
    /* Dropdowns */
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
        border: 2px solid {current_theme['card_border']};
        border-radius: 25px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }}
    
    /* Section Headers */
    .section-title {{
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 1rem;
        margin-bottom: 1rem;
        color: {current_theme['highlight']} !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Score Box */
    .score-container {{
        text-align: center;
        padding: 2.5rem;
        border-radius: 30px;
        background: {current_theme['score_box_bg']};
        border: 2px solid {current_theme['card_border']};
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

# --- SIDEBAR (Settings Only) ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.toggle("Night Mode", value=(st.session_state.theme_mode == "Dark"), key="theme_toggle", on_change=toggle_theme)
    if st.session_state.page == "results":
        st.markdown("---")
        if st.button("🔄 Retake Interview"):
            reset_interview()
            st.rerun()

# ==========================================
# PAGE 1: THE INTERVIEW
# ==========================================
if st.session_state.page == "interview":
    st.markdown(f'<h1 style="text-align:center; font-size: 3rem;">📝 Social Impact Interview</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; opacity:0.8; margin-bottom:3rem;">Answer a few questions to unlock your digital wellness score.</p>', unsafe_allow_html=True)

    # Use a form to group inputs
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
        # Center the submit button
        col_dummy1, col_btn, col_dummy2 = st.columns([1, 2, 1])
        with col_btn:
            submitted = st.form_submit_button("🏁 FINISH & ANALYZE")
            
        if submitted:
            # Store data in session state
            st.session_state.inputs = {
                "Age": age, "Gender": gender, "Academic_Level": academic_level,
                "Avg_Daily_Usage_Hours": avg_daily_usage, "Platform": platform,
                "Addiction": addiction, "Sleep": sleep, "Relationship": rel_status,
                "Affects_Performance": affects_perf, "Conflicts": conflicts
            }
            
            # --- CALCULATION LOGIC ---
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
                    wellness_score = max(1, min(10, base))

                st.session_state.score = wellness_score
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
    
    # Header
    st.markdown(f'<h1 style="text-align:center; font-size: 3rem;">Your <span style="color:{current_theme["highlight"]}">Results</span> are In!</h1>', unsafe_allow_html=True)
    
    # Score Display
    score_color = "#FF6B6B" if score < 4 else "#FFD93D" if score < 7 else "#6BCB77"
    st.markdown(f"""
    <div class="score-container">
        <h3 style="margin:0; opacity:0.7; letter-spacing:2px; font-size:1rem;">WELLNESS SCORE</h3>
        <h1 style="font-size: 6rem; font-weight: 800; margin: 0; color: {score_color} !important;">
            {score:.1f}<span style="font-size:2rem; opacity:0.5;">/10</span>
        </h1>
        <p style="opacity:0.8;">{ "Doing great!" if score > 7 else "Needs some attention." if score > 4 else "Time for a detox?" }</p>
    </div>
    """, unsafe_allow_html=True)

    # AI Tools
    st.markdown(f'<h3 style="text-align:center; color:{current_theme["highlight"]}; margin-bottom:20px;">✨ AI Insights</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("📊 My Persona"):
            with st.spinner("Analyzing..."):
                prompt = f"Based on: {json.dumps(data)}. Return JSON: {{'persona': 'Fun Title', 'analysis': 'Short analysis', 'tips': ['Tip 1', 'Tip 2']}}"
                res = call_gemini(prompt)
                if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🕰️ Future Self"):
            with st.spinner("Connecting..."):
                prompt = f"Write a note from future 2029 self based on habits: {json.dumps(data)}. Max 50 words."
                res = call_gemini(prompt, is_json=False)
                if res: st.session_state.ai_results['future'] = res; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🍃 Detox Plan"):
            with st.spinner("Planning..."):
                prompt = f"3-day detox for {data['Platform']} user. JSON: {{'days': [{{'day': 'Day 1', 'theme': 'Theme', 'tasks': ['Task 1', 'Task 2']}}]}}"
                res = call_gemini(prompt)
                if res: st.session_state.ai_results['detox'] = json.loads(res); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Render AI Results
    if st.session_state.get('ai_results'):
        st.markdown("<br>", unsafe_allow_html=True)
        results = st.session_state.ai_results
        
        if 'analysis' in results:
            r = results['analysis']
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color:#4DA3FF !important;">📊 {r.get('persona', 'User')}</h3>
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
                <h3 style="color:#6BCB77 !important;">🍃 Detox Challenge</h3>
                {days_html}
            </div>
            """, unsafe_allow_html=True)
