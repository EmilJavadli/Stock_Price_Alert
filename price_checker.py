import yfinance as yf
import logging

logger = logging.getLogger(__name__)

def get_last_price(ticker: str) -> float:
    """
    Fetch the last available closing price for a given ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', '^VIX')
        
    Returns:
        Last closing price rounded to 2 decimal places
        
    Raises:
        ValueError: If ticker is invalid or no data available
        ConnectionError: If network request fails
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")
    
    ticker = ticker.strip().upper()
    
    try:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(period="1d", interval="1m")
        
        if data.empty:
            logger.warning(f"No data available for ticker: {ticker}")
            raise ValueError(f"No data available for ticker: {ticker}")
        
        last_price = round(float(data['Close'].iloc[-1]), 2)
        logger.info(f"Fetched price for {ticker}: {last_price}")
        
        return last_price
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error fetching price for {ticker}: {str(e)}")
        raise ConnectionError(f"Failed to fetch price for {ticker}: {str(e)}")