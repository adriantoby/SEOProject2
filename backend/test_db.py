from database import TrackedStock, AlertHistory, SessionLocal

def add_stock(symbol, target_buy, target_sell):
    session = SessionLocal()
    stock = TrackedStock(symbol=symbol, target_buy=target_buy, target_sell=target_sell)
    session.add(stock)
    session.commit()
    print(f"stock '{symbol}' added with ID {stock.id}")
    session.close()
    return stock.id

def log_alert(stock_id, alert_type, price_at_alert):
    session = SessionLocal()
    alert = AlertHistory(stock_id=stock_id, alert_type=alert_type, price_at_alert=price_at_alert)
    session.add(alert)
    session.commit()
    print(f" Alert logged: {alert_type} at ${price_at_alert} for stock ID {stock_id}")
    session.close()

if __name__ == "__main__":
    stock_id = add_stock("AAPL", 140.0, 160.0)
    log_alert(stock_id, "BUY ALERT", 139.5)