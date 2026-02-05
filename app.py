import streamlit as st
import pandas as pd
import joblib
import json
import time
import requests
import numpy as np
import base64

# --- PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="Social Impact AI",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURATION ---
MODEL_FILE = 'mental_health_model.joblib' 
GEMINI_MODEL = 'gemini-2.5-flash'
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# --- THEME MANAGEMENT ---
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light" # Default to Light for friendliness

def toggle_theme():
    if st.session_state.theme_toggle:
        st.session_state.theme_mode = "Dark"
    else:
        st.session_state.theme_mode = "Light"

# --- DYNAMIC BACKGROUND GENERATOR ---
def get_background_style(theme_mode, score):
    # Kid-Friendly Gradients
    gradients = {
        # Deep Space Purple (Cool & Calm)
        "Dark": "linear-gradient(135deg, #240b36 0%, #2d3436 74%)", 
        # Sunny Sky Blue (Optimistic & Bright)
        "Light": "linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)" 
    }
    base_bg = gradients[theme_mode]
    
    if score is None:
        return base_bg

    # Emoji Selection: Happy vs Sad
    emoji = "🌟" if score >= 6 else "🌧️" # Star for good, Rain cloud for bad
    
    # Create subtle SVG pattern
    svg = f"""
    <svg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'>
        <text x='50%' y='50%' font-size='35' text-anchor='middle' dominant-baseline='middle' opacity='0.15'>{emoji}</text>
    </svg>
    """
    b64_svg = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    emoji_layer = f"url('data:image/svg+xml;base64,{b64_svg}')"
    
    return f"{emoji_layer}, {base_bg}"

# --- DEFINE THEME PALETTES ---
themes = {
    "Dark": {
        "text_main": "#ffffff",
        "text_header": "#d1d5db", # Light Grey
        "sidebar_bg": "rgba(20, 20, 40, 0.7)",
        "card_bg": "rgba(40, 40, 60, 0.5)",
        "card_border": "rgba(255, 255, 255, 0.15)",
        "input_bg": "rgba(255, 255, 255, 0.1)",
        "input_text": "#ffffff",
        "score_box_bg": "rgba(0,0,0,0.2)",
        "button_grad": "linear-gradient(90deg, #8E2DE2, #4A00E0)", # Purple/Blue
        "highlight": "#c084fc"
    },
    "Light": {
        "text_main": "#2c3e50", # Dark Blue/Grey (Softer than black)
        "text_header": "#576574",
        "sidebar_bg": "rgba(255, 255, 255, 0.65)",
        "card_bg": "rgba(255, 255, 255, 0.85)", # High readability
        "card_border": "#ffffff",
        "input_bg": "#ffffff",
        "input_text": "#2c3e50",
        "score_box_bg": "rgba(255,255,255,0.5)",
        "button_grad": "linear-gradient(90deg, #FF9966, #FF5E62)", # Orange/Pink (Fun!)
        "highlight": "#FF5E62"
    }
}

current_theme = themes[st.session_state.theme_mode]
current_bg = get_background_style(st.session_state.theme_mode, st.session_state.get('score'))

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    /* IMPORT FONT: Poppins is rounded, friendly, yet professional */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    .stApp {{
        background: {current_bg};
        color: {current_theme['text_main']};
        font-family: 'Poppins', sans-serif;
        transition: background 0.5s ease;
    }}

    /* TEXT COLORS */
    h1, h2, h3, h4, h5, h6 {{ color: {current_theme['text_main']} !important; font-weight: 800; }}
    p, li, label {{ color: {current_theme['text_main']} !important; }}
    .sidebar-header {{ color: {current_theme['text_header']} !important; font-weight: 600; font-size: 1.1rem; }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background-color: {current_theme['sidebar_bg']};
        border-right: 2px solid {current_theme['card_border']};
        backdrop-filter: blur(15px);
    }}

    /* INPUTS - Rounded & Bubbly */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stSlider > div > div > div {{
        background-color: {current_theme['input_bg']} !important;
        color: {current_theme['input_text']} !important;
        border: 2px solid rgba(0,0,0,0.05) !important;
        border-radius: 15px !important; /* Very rounded */
        padding: 10px;
    }}
    
    div[data-baseweb="popover"], div[data-baseweb="select"] ul {{
        background-color: {current_theme['input_bg']} !important;
        color: {current_theme['input_text']} !important;
    }}
    
    /* BUTTONS - Pill Shaped & Colorful */
    .stButton > button {{
        background: {current_theme['button_grad']} !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important; /* Pill shape */
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.05); /* Pop effect */
    }}
    
    /* CARDS */
    .glass-card {{
        background: {current_theme['card_bg']};
        border: 2px solid {current_theme['card_border']};
        border-radius: 25px; /* Big rounded corners */
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }}

    /* SCORE BOX */
    .score-container {{
        text-align: center;
        padding: 2.5rem;
        border-radius: 30px;
        background: {current_theme['score_box_bg']};
        border: 2px solid {current_theme['card_border']};
        margin: 2rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }}
    
    /* LISTS */
    li {{ padding-left: 1.5em; text-indent: -1.5em; margin-bottom: 10px; font-weight: 500; }}
    li::before {{ content: "●"; color: {current_theme['highlight']}; padding-right: 10px; font-size: 0.8rem; }}

</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_resource
def load_ml_model():
    try:
        model = joblib.load(MODEL_FILE)
        return model
    except Exception as e:
        return None

model = load_ml_model()

# --- GEMINI API CALL HANDLER ---
def call_gemini(prompt, is_json=True, max_retries=3):
    if not API_KEY:
        st.warning("⚠️ Gemini API key missing.")
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    for i in range(max_retries):
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        if is_json:
            payload["generationConfig"] = {"responseMimeType": "application/json"}
        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=20)
            if response.status_code == 200:
                data = response.json()
                return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
            time.sleep(1)
        except Exception:
            pass
    return None

# --- ML FEATURE PREP ---
MODEL_COLUMNS = [
    'Age', 'Gender', 'Academic_Level', 'Avg_Daily_Usage_Hours', 'Affects_Academic_Performance', 'Sleep_Hours_Per_Night', 'Conflicts_Over_Social_Media', 'Addicted_Score', 'Most_Used_Platform_Facebook', 'Most_Used_Platform_Instagram', 'Most_Used_Platform_KakaoTalk', 'Most_Used_Platform_LINE', 'Most_Used_Platform_LinkedIn', 'Most_Used_Platform_Snapchat', 'Most_Used_Platform_TikTok', 'Most_Used_Platform_Twitter', 'Most_Used_Platform_VKontakte', 'Most_Used_Platform_WeChat', 'Most_Used_Platform_WhatsApp', 'Most_Used_Platform_YouTube', 'Relationship_Status_Complicated', 'Relationship_Status_In Relationship', 'Relationship_Status_Single']

# --- SIDEBAR UI ---
with st.sidebar:
    st.markdown('<p class="sidebar-header">🎨 Theme</p>', unsafe_allow_html=True)
    toggle_state = st.toggle("Night Mode", value=(st.session_state.theme_mode == "Dark"), key="theme_toggle", on_change=toggle_theme)
    
    st.markdown("---")
    st.markdown('<p class="sidebar-header">👤 About You</p>', unsafe_allow_html=True)
    age = st.number_input("Age", 10, 100, 15)
    gender = st.selectbox("Gender", ["Male", "Female"])
    academic_level = st.selectbox("School Level", ["High School", "Undergraduate", "Graduate", "Middle School"])
    
    st.markdown("---")
    st.markdown('<p class="sidebar-header">📱 Screen Time</p>', unsafe_allow_html=True)
    avg_daily_usage = st.number_input("Hours per Day", 0.0, 24.0, 4.0, 0.5)
    platform = st.selectbox("Favorite App", ["TikTok", "YouTube", "Instagram", "Twitter", "Facebook", "Snapchat", "WhatsApp", "LinkedIn"])
    addiction = st.slider("Addiction Level (1-10)", 1, 10, 5)
    
    st.markdown("---")
    st.markdown('<p class="sidebar-header">❤️ Health</p>', unsafe_allow_html=True)
    sleep = st.number_input("Sleep Hours", 0.0, 24.0, 8.0, 0.5)
    affects_perf = st.radio("Affects Grades?", ["No", "Yes"], horizontal=True)
    conflicts = st.number_input("Arguments over Phone", 0, 10, 0)
    rel_status = st.selectbox("Relationship", ["Single", "In a relationship", "Married", "Divorced"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    calculate_button = st.button("🚀 Check My Score")

# --- MAIN UI ---
st.markdown(f'<h1 style="font-size: 3.5rem; text-align:center; margin-bottom: 0;">Social <span style="color:{current_theme["highlight"]}">Impact</span> Checker</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size: 1.2rem; text-align:center; opacity:0.8;">Discover how your apps affect your daily happiness.</p>', unsafe_allow_html=True)

# --- APP LOGIC ---
if calculate_button:
    st.session_state.ai_results = {} 
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
            base_score = 10 - (avg_daily_usage * 0.3) - (addiction * 0.2) + (sleep * 0.2)
            wellness_score = max(1, min(10, base_score)) 

        st.session_state['score'] = wellness_score
        st.session_state['user_data_ai'] = {"Age": age, "Hours": avg_daily_usage, "Platform": platform, "Addiction": addiction, "Sleep": sleep}
        st.rerun() 
    except Exception as e:
        st.error(f"Prediction Error: {e}")

# --- RESULTS DISPLAY ---
if 'score' in st.session_state:
    score = st.session_state['score']
    # Kid-friendly colors: Green = Good, Yellow = Okay, Red = Watch out
    score_color = "#FF6B6B" if score < 4 else "#FFD93D" if score < 7 else "#6BCB77"
    
    st.markdown(f"""
    <div class="score-container">
        <h3 style="margin:0; opacity:0.7; text-transform:uppercase; letter-spacing:2px; font-size:1rem;">Your Wellness Score</h3>
        <h1 style="font-size: 6rem; font-weight: 800; margin: 0; color: {score_color} !important; text-shadow: 2px 2px 0px rgba(0,0,0,0.1);">
            {score:.1f}<span style="font-size:2rem; opacity:0.5;">/10</span>
        </h1>
        <p style="opacity:0.8;">Based on your habits and sleep.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<br><h3 style="text-align:center; color:{current_theme["highlight"]};">✨ AI Assistant</h3>', unsafe_allow_html=True)
    data = st.session_state.get('user_data_ai', {})
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("📊 My Profile"):
            with st.spinner("Thinking..."):
                prompt = f"Analyze this student's data: {json.dumps(data)}. Return JSON with keys: 'persona' (Fun 2 word title like 'Digital Ninja'), 'analysis' (Simple explanation), 'tips' (2 easy tips)."
                res = call_gemini(prompt)
                if res: st.session_state.ai_results['analysis'] = json.loads(res); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🕰️ Time Travel"):
            with st.spinner("Warping to 2029..."):
                prompt = f"Write a funny but helpful note from this user's future self in 2029. {json.dumps(data)}. Max 50 words."
                res = call_gemini(prompt, is_json=False)
                if res: st.session_state.ai_results['future'] = res; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🍃 Mini Detox"):
            with st.spinner("Planning..."):
                prompt = f"Create a fun 3-day social media detox for a {data['Platform']} user. Return JSON: {{'days': [{{'day': 'Day 1', 'theme': 'Theme', 'tasks': ['Fun Task 1', 'Fun Task 2']}}]}}"
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
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                    <span style="font-size:2rem;">📊</span>
                    <h3 style="margin:0; color:#4DA3FF !important;">{r.get('persona', 'User')}</h3>
                </div>
                <p style="font-size:1.1rem;">"{r.get('analysis', '')}"</p>
                <hr style="border-color:{current_theme['card_border']}; opacity:0.3;">
                <p style="font-weight:bold; font-size:0.9rem;">QUICK TIPS</p>
                <ul>{"".join([f"<li>{t}</li>" for t in r.get('tips', [])])}</ul>
            </div>
            """, unsafe_allow_html=True)

        if 'future' in results:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 8px solid #FFD93D;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                    <span style="font-size:2rem;">🕰️</span>
                    <h3 style="margin:0; color:#FFD93D !important;">Message from 2029</h3>
                </div>
                <p style="font-family: 'Courier New', monospace; background:rgba(0,0,0,0.05); padding:1.5rem; border-radius:15px; font-weight:600;">
                    {results['future']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        if 'detox' in results:
            r = results['detox']
            days_html = ""
            for d in r.get('days', []):
                tasks_html = "".join([f"<li>{t}</li>" for t in d.get('tasks', [])])
                days_html += f"""
                <div style="background:{current_theme['input_bg']}; padding:1.5rem; border-radius:20px; margin-bottom:15px; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
                    <strong style="color:#FF6B6B; font-size:1.1rem;">{d.get('day')}: {d.get('theme')}</strong>
                    <ul style="margin-top:10px;">{tasks_html}</ul>
                </div>
                """
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
                    <span style="font-size:2rem;">🍃</span>
                    <h3 style="margin:0; color:#6BCB77 !important;">Detox Challenge</h3>
                </div>
                {days_html}
            </div>
            """, unsafe_allow_html=True)

st.markdown(f"<br><br><div style='text-align:center; opacity:0.5; font-size:0.8rem;'>Made with ❤️ for STEAM Fair</div>", unsafe_allow_html=True)
