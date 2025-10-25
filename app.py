from email_sender import send_email
import time
from datetime import datetime
import streamlit as st


st.title("Stock Price Alert System")

ticker = st.text_input("Ticker Symbol", value="^VIX")
alert_price = st.number_input("Alert Price", value=16.0)
requested_email = st.text_input('Email', value='')
interval = st.selectbox("Check Interval", ["Every Hour", "Every 30 Minutes", "Every 15 Minutes", "Every 5 Minutes"])

if st.button("Start Monitoring"):
    st.success(f"Monitoring {ticker} - Alert when price <= {alert_price}")
    
    interval_map = {
        "Every Hour": 3600,
        "Every 30 Minutes": 1800,
        "Every 15 Minutes": 900,
        "Every 5 Minutes": 300
    }
    
    status_placeholder = st.empty()
    
    while True:
        result = send_email(ticker, alert_price, requested_email)
        status_placeholder.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {result}")
        time.sleep(interval_map[interval])
        st.rerun()
    

# python -m streamlit run app.py