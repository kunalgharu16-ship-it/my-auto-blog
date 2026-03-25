import streamlit as st
import pandas as pd
import os

# Page ki settings
st.set_page_config(page_title="Live Market Tracker", layout="wide")

st.title("📈 Real-Time Market & Crypto Dashboard")
st.write("Ye data Python script ke zariye automate kiya gaya hai.")

# CSV file check karna
file_name = 'market_history.csv'

if os.path.exists(file_name):
    # Data read karna
    df = pd.DataFrame(pd.read_csv(file_name))
    
    # Sabse latest data upar dikhane ke liye reverse karna
    df = df.iloc[::-1]

    # Ek sundar Table dikhana
    st.subheader("Latest Market Movements")
    st.dataframe(df, use_container_width=True)

    # Chhota sa Chart dikhana (Nifty 50 ke liye)
    st.subheader("Market Trend")
    nifty_data = df[df['Asset'] == 'Nifty 50']
    if not nifty_data.empty:
        st.line_chart(nifty_data.set_index('Time')['Price'])
else:
    st.warning("Abhi tak koi data save nahi hua hai. Pehle 'market_tracker.py' run karein.")

st.sidebar.info("System Status: Automated via Python")
