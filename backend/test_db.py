from backend.database import TrackedStock, AlertHistory, SessionLocal

def add_stock(symbol, target_buy=None, target_sell=None):
    """
    Adds a new stock to the TrackedStock table in the database.

    Parameters:
        symbol (str): Stock ticker symbol (e.g., 'AAPL').
        target_buy (float, optional): User-defined price to buy the stock.
        target_sell (float, optional): User-defined price to sell the stock.

    Returns:
        int: The database ID of the newly added stock.
    """
    session = SessionLocal()
    stock = TrackedStock(symbol=symbol, target_buy=target_buy, target_sell=target_sell)
    session.add(stock)
    session.commit()
    stock_id = stock.id
    session.close()
    return stock_id

def log_alert(stock_id, alert_type, price_at_alert):
    """
    Logs an alert into the AlertHistory table.

    Parameters:
        stock_id (int): The ID of the stock (foreign key from TrackedStock).
        alert_type (str): The type of alert ('BUY', 'SELL', or 'HOLD').
        price_at_alert (float): The stock price at the time the alert was generated.

    Returns:
        None
    """
    session = SessionLocal()
    alert = AlertHistory(stock_id=stock_id, alert_type=alert_type, price_at_alert=price_at_alert)
    session.add(alert)
    session.commit()
    session.close()

def return_stocks():
    """
    Retrieves all tracked stocks and their most recent alert type.

    Returns:
        list of dict: Each dictionary contains:
            - 'symbol' (str): Stock ticker symbol.
            - 'alert' (str): Most recent alert type or "No alerts" if none exist.
    """
    session = SessionLocal()
    
    stocks = session.query(TrackedStock).all()
    
    result = []
    for stock in stocks:
        if stock.alerts:
            latest_alert = session.query(AlertHistory)\
                .filter(AlertHistory.stock_id == stock.id)\
                .order_by(AlertHistory.timestamp.desc())\
                .first()
            alert_type = latest_alert.alert_type if latest_alert else "No alerts"
        else:
            alert_type = "No alerts"
        
        result.append({
            "symbol": stock.symbol,
            "alert": alert_type
        })
    
    session.close()
    return result




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