import streamlit as st

import yfinance as yf

import google.generativeai as genai

from datetime import datetime



# --- SETTINGS ---

GOOGLE_API_KEY = "AIzaSyD-87JD7e4vkpZlp6dLExEIXoyIaHcWQEw" # <-- Apni Key Yahan Dalein

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')



st.set_page_config(page_title="RUDRA AI TERMINAL", layout="wide")



# --- UI STYLE ---

st.markdown("""

    <style>

    .main { background-color: #0b0e11; color: white; }

    .ai-blog-card { 

        background: #161b22; 

        padding: 30px; 

        border-radius: 15px; 

        border-left: 5px solid #3b82f6;

        margin-bottom: 25px;

        line-height: 1.8;

    }

    .badge { background: #3b82f6; padding: 5px 10px; border-radius: 5px; font-size: 12px; }

    </style>

    """, unsafe_allow_html=True)



st.title("⚡ RUDRA AI: Smart Market Terminal")



# --- 1. LIVE TICKER (Short version) ---

st.subheader("📊 Live Snapshot")

cols = st.columns(3)

indices = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "GOLD": "GC=F"}

for i, (name, sym) in enumerate(indices.items()):

    p = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]

    cols[i].metric(name, f"{p:,.2f}")



st.markdown("---")



# --- 2. AI AUTO-BLOG GENERATOR ---

st.subheader("✍️ AI Generated Market Analysis")



def generate_ai_content(headline):

    prompt = f"Write a professional financial blog post in Hinglish (Hindi + English) about this news headline: '{headline}'. Include an introduction, market impact, and a conclusion. Keep it around 300 words. Do not use bold symbols like **."

    response = model.generate_content(prompt)

    return response.text



try:

    # Latest News uthana

    news_item = yf.Ticker("^NSEI").news[0]

    headline = news_item['title']

    

    with st.spinner('RUDRA AI is writing a fresh article for you...'):

        ai_article = generate_ai_content(headline)

    

    # Displaying the AI Blog

    st.markdown(f"""

        <div class="ai-blog-card">

            <span class="badge">AI GENERATED ARTICLE</span>

            <p style='color: #768390; margin-top:10px;'>📅 {datetime.now().strftime('%d %b %Y | %I:%M %p')}</p>

            <h1 style='color: #58a6ff; font-size: 28px;'>{headline}</h1>

            <hr style='border: 0.1px solid #30363d;'>

            <div style='font-size: 17px; color: #adbac7;'>

                {ai_article}

            </div>

            <br>

            <p style='font-size: 14px; color: #3b82f6;'>Source: Financial Data Feed & RUDRA Intelligence</p>

        </div>

    """, unsafe_allow_html=True)



except Exception as e:

    st.warning("AI is taking a break. Refresh in 1 minute!")
