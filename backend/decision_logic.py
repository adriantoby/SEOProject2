from backend.logic import get_insider_transactions, get_RSI, get_SMA, get_current_price, get_company_logo
from backend.test_db import add_stock, log_alert

'''
#not being used anymore as the final decision maker for the trade signal.
#User_threshold is no longer being used in the decison making as well
def get_trade_signal(rsi, current_price, moving_avg):
    """
    Determines a trade signal (BUY, SELL, HOLD) based on RSI and current price vs. SMA.

    Parameters:
        rsi (float): Relative Strength Index of the stock.
        current_price (float): The current price of the stock.
        moving_avg (float): Simple Moving Average of the stock.

    Returns:
        str: "BUY", "SELL", or "HOLD" as a suggested trading signal.
    """
    if rsi < 30 and current_price < moving_avg:
        return "BUY"
    elif rsi > 70 and current_price > moving_avg:
        return "SELL"
    else:
        return "HOLD"

def check_user_thresholds(current_price, target_buy=None, target_sell=None):
    """
    Checks if the current price meets user-defined buy or sell thresholds.

    Parameters:
        current_price (float): Current stock price.
        target_buy (float, optional): User's target buy price.
        target_sell (float, optional): User's target sell price.

    Returns:
        str: "BUY" if target_buy hit, "SELL" if target_sell hit, otherwise "HOLD".
    """
    if target_buy and current_price <= target_buy:
        return "BUY"
    elif target_sell and current_price >= target_sell:
        return "SELL"
    else:
        return "HOLD"
'''   

def should_send_alert(current_price, last_alert_price, threshold=2.0):
    """
    Determines whether a price alert should be sent based on a price change threshold.

    Parameters:
        current_price (float): Current stock price.
        last_alert_price (float or None): Last price at which an alert was sent.
        threshold (float): Minimum price change required to trigger a new alert.

    Returns:
        bool: True if alert should be sent, False otherwise.
    """
    if last_alert_price is None:
        return True
    return abs(current_price - last_alert_price) >= threshold


def process_stock(symbol):
    """
    Combines technical indicators and insider transactions to generate a final trading decision.

    - Uses RSI, current price, and SMA to determine a technical decision.
    - Retrieves insider transaction data for a separate decision.
    - Merges both using rule-based logic.
    - Logs the decision and explanation to the database.

    Parameters:
        symbol (str): Stock ticker symbol (e.g., 'AAPL').

    Returns:
        tuple:
            - str: Final decision ("BUY", "SELL", "HOLD", or "INVALID SYMBOL").
            - dict: Explanation including RSI, current price, SMA, and both decisions.
    """
    rsi = get_RSI(symbol)
    current_price = get_current_price(symbol)
    moving_avg = get_SMA(symbol)
    insider_decision = get_insider_transactions(symbol)

    if not rsi or not current_price:
        return "INVALID SYMBOL"
    if rsi < 30 and current_price < moving_avg:
        tech_decision = 'BUY'
    elif rsi > 70 and current_price > moving_avg:
        tech_decision = 'SELL'
    else:
        tech_decision = 'HOLD'
    
    if tech_decision == insider_decision:
        final_decision = tech_decision
    elif tech_decision == 'HOLD':
        final_decision = insider_decision
    elif insider_decision == 'HOLD':
        final_decision = tech_decision
    else:
        final_decision = 'HOLD'

    explanation = {
        "rsi": rsi,
        "Current Price": current_price,
        "Moving Average": moving_avg,
        "tech_decision": tech_decision,
        "insider_decision": insider_decision
    }

    stock_id = add_stock(symbol)
    log_alert(stock_id, final_decision, current_price)

    return final_decision, explanation

