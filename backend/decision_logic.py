from logic import get_insider_transactions, get_RSI, get_SMA, get_current_price
from test_db import add_stock, log_alert

def get_trade_signal(rsi, current_price, moving_avg):
    if rsi < 30 and current_price < moving_avg:
        return "BUY"
    elif rsi > 70 and current_price > moving_avg:
        return "SELL"
    else:
        return "HOLD"
    

def check_user_thresholds(current_price, target_buy=None, target_sell=None):
    if target_buy and current_price <= target_buy:
        return "BUY"
    elif target_sell and current_price >= target_sell:
        return "SELL"
    else:
        return "HOLD"
    

def should_send_alert(current_price, last_alert_price, threshold=2.0):
    if last_alert_price is None:
        return True
    return abs(current_price - last_alert_price) >= threshold


def process_stock(symbol):
    rsi = get_RSI(symbol)
    current_price = get_current_price(symbol)
    moving_avg = get_SMA(symbol)
    decision = get_trade_signal(rsi, current_price, moving_avg)
    insider_decision = get_insider_transactions(symbol)

    final_decision = "HOLD"
    if decision == insider_decision:
        final_decision = decision
    elif decision == "HOLD":
        if insider_decision == "BUY":
            final_decision = "BUY"
        elif insider_decision == "SELL":
            final_decision = "SELL"
    elif insider_decision == "HOLD":
        final_decision = decision

    # debugging
    print(f"RSI: {rsi}")
    print(f"Current Price: {current_price}")
    print(f"Moving Average: {moving_avg}")
    print(f"Decision: {decision}")
    print(f"Insider Decision: {insider_decision}")
    print(final_decision)

    stock_id = add_stock(symbol)
    log_alert(stock_id, final_decision, current_price)


if __name__ == "__main__":
    symbol = "AAPL"
    process_stock(symbol)
