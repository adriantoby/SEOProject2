from backend.database import TrackedStock, AlertHistory, SessionLocal

def add_stock(symbol, target_buy=None, target_sell=None):
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
    print(f"Alert logged: {alert_type} at ${price_at_alert} for stock ID {stock_id}")
    session.close()

if __name__ == "__main__":
    stock_id = add_stock("IBM")
    log_alert(stock_id, "BUY", 139.5)



# from database import SessionLocal, TrackedStock, AlertHistory
# from datetime import datetime

# session = SessionLocal()

# new_stock = TrackedStock(
#     symbol="AAPL",
#     target_buy=130.0,
#     target_sell=150.0
# )

# session.add(new_stock)
# session.commit()
# print(f" stock saved with ID {new_stock.id}")

# current_price = 125.0

# if current_price <= new_stock.target_buy:
#     action = "BUY"
# elif current_price >= new_stock.target_sell:
#     action = "SELL"
# else:
#     action = "HOLD"

# if action:
#     alert = AlertHistory(
#         stock_id=new_stock.id,
#         alert_type=action,
#         price_at_alert=current_price,
#         timestamp=datetime.utcnow()
#     )
#     session.add(alert)
#     session.commit()
#     print(f" Alert saved: {action} at {current_price}")
# else:
#     print(" No alert generated for current price.")