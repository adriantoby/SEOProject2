from logic import get_insider_transactions, get_RSI, get_SMA, get_current_price

def get_trade_signal(rsi, current_price, moving_avg):
    if rsi < 30 and current_price < moving_avg:
        return "BUY"
    elif rsi > 70 and current_price > moving_avg:
        return "SELL"
    else:
        return "HOLD"
    

def check_user_thresholds(current_price, target_buy=None, target_sell=None):
    if target_buy and current_price <= target_buy:
        return "BUY ALERT"
    elif target_sell and current_price >= target_sell:
        return "SELL ALERT"
    else:
        return "NO ALERT"
    

def should_send_alert(current_price, last_alert_price, threshold=2.0):
    if last_alert_price is None:
        return True
    return abs(current_price - last_alert_price) >= threshold


if __name__ == "__main__":
    symbol = "CAT"
    rsi = get_RSI(symbol)
    current_price = get_current_price(symbol)
    moving_avg = get_SMA(symbol)

    print(rsi)
    print(current_price)
    print(moving_avg)

    decision = get_trade_signal(rsi, current_price, moving_avg)
    print(f"Trade signal: {decision}")

