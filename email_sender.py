from price_checker import get_last_price
import smtplib
from email.mime.text import MIMEText
import logging
import streamlit as st

logger = logging.getLogger(__name__)

def send_email(ticker: str, alert_price: float, requested_email: str) -> str:
    """
    Check stock price and send email alert if price threshold is met.
    
    Args:
        ticker: Stock ticker symbol
        alert_price: Price threshold for triggering alert
        
    Returns:
        Status message indicating whether alert was sent
        
    Raises:
        ValueError: If credentials are missing or invalid
        smtplib.SMTPException: If email sending fails
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")
    
    if alert_price <= 0:
        raise ValueError("Alert price must be positive")
    
    app_email = st.secrets['GOOGLE_EMAIL']
    app_password = st.secrets['GOOGLE_APP_PASSWORD'
    ]
    if not app_email or not app_password:
        raise ValueError("Email credentials not found in environment variables")
    
    try:
        last_price = get_last_price(ticker)
        
        if last_price <= alert_price:
            msg = MIMEText(
                f"{ticker} has reached your alert price!\n\n"
                f"Current Price: ${last_price}\n"
                f"Alert Price: ${alert_price}"
            )
            msg['Subject'] = f'Stock Alert: {ticker} at ${last_price}'
            msg['From'] = app_email
            msg['To'] = requested_email
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(app_email, app_password)
                smtp.send_message(msg)
            
            logger.info(f"Alert sent for {ticker} at ${last_price}")
            return f"Alert sent! {ticker} is at ${last_price}"
        else:
            logger.info(f"No alert: {ticker} at ${last_price} (target: ${alert_price})")
            return f"No alert: {ticker} at ${last_price} (target: ${alert_price})"
            
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"Email sending failed: {str(e)}")
        raise smtplib.SMTPException(f"Failed to send email: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in send_email: {str(e)}")
        raise