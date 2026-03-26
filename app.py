import streamlit as st
import yfinance as yf
from datetime import datetime

# Page Settings
st.set_page_config(page_title="RUDRA TERMINAL", layout="wide")

# --- PREMIUM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0b0e11; color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; padding: 10px; border-radius: 8px; }
    .price-card { background: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; text-align: center; }
    .news-card { border-left: 4px solid #3b82f6; background: #161b22; padding: 20px; margin-bottom: 15px; border-radius: 0 10px 10px 0; }
    .up { color: #39d353; font-weight: bold; }
    .down { color: #f85149; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color: #3b82f6;'>⚡ RUDRA TERMINAL</h1>", unsafe_allow_html=True)
st.caption(f"Market Sync: {datetime.now().strftime('%d %b %Y | %H:%M:%S')}")

# --- MARKET DATA TABS ---
t1, t2, t3 = st.tabs(["EQUITY", "COMMODITY", "GLOBAL"])

def load_market(assets, tab_obj, unit="₹"):
    with tab_obj:
        cols = st.columns(len(assets))
        for i, (name, sym) in enumerate(assets.items()):
            try:
                d = yf.Ticker(sym).history(period="2d")
                price = d['Close'].iloc[-1]
                chg = price - d['Close'].iloc[-2]
                pct = (chg / d['Close'].iloc[-2]) * 100
                clr = "up" if chg >= 0 else "down"
                with cols[i]:
                    st.markdown(f"""<div class="price-card">
                        <div style='color:#8b949e; font-size:12px;'>{name}</div>
                        <div style='font-size:22px; font-weight:bold;'>{unit}{price:,.2f}</div>
                        <div class="{clr}">{'▲' if chg>=0 else '▼'} {pct:.2f}%</div>
                    </div>""", unsafe_allow_html=True)
            except: pass

load_market({"Nifty 50": "^NSEI", "Sensex": "^BSESN", "Bank Nifty": "^NSEBANK"}, t1)
load_market({"Gold": "GC=F", "Silver": "SI=F", "Crude": "CL=F"}, t2, "$")
load_market({"Dow Jones": "^DJI", "Nasdaq": "^IXIC", "FTSE 100": "^FTSE"}, t3, "")

# --- AUTOMATIC BLOG FEED ---
st.markdown("---")
st.subheader("📰 Market Insights & Updates")
try:
    news = yf.Ticker("^NSEI").news
    for n in news[:6]:
        dt = datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b | %I:%M %p')
        st.markdown(f"""<div class="news-card">
            <small style='color:#768390;'>📅 {dt} | Source: {n['provider']}</small>
            <h3 style='margin:10px 0; font-size:20px;'>{n['title']}</h3>
            <p style='color:#8b949e;'>RUDRA Intelligence: Analysis suggests monitoring these trends for potential breakouts.</p>
            <a href="{n['link']}" target="_blank" style='color:#3b82f6; text-decoration:none; font-weight:bold;'>Full Analysis →</a>
        </div>""", unsafe_allow_html=True)
except: st.error("Updating Feed...")
