from flask import Flask, render_template, request
from backend.logic import ask_gemini
from backend.decision_logic import process_stock

app = Flask(__name__)

@app.route("/") # home page
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about") # about page
def about():
    return render_template("about.html")

@app.route("/trade", methods=["GET", "POST"]) # trade page
def trade():
    decision = None
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        if ticker:
            decision = process_stock(ticker)
        print(f"(Demo) You asked to trade: {ticker}, we have decided to {decision}")

    return render_template("trade.html", decision=decision)

@app.route("/assistant", methods=["GET", "POST"]) # GENAI assistant 
def assistant():
    ai_answer = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            ai_answer = ask_gemini(user_input)
        print(f"(Demo) You asked: {user_input}")
    return render_template("assistant.html", ai_answer=ai_answer)
            
if __name__ == "__main__":
    app.run(debug=True)
    



# @app.route("/api/stocks", methods=["GET"])
# def get_stocks():
#     session = SessionLocal()
#     stocks = session.query(TrackedStock).all()
#     result = [
#         {
#             "id": stock.id,
#             "symbol": stock.symbol,
#             "target_buy": stock.target_buy,
#             "target_sell": stock.target_sell
#         }
#         for stock in stocks
#     ]
#     session.close()
#     return jsonify(result)

# @app.route("/api/stocks", methods=["POST"])
# def add_stock():
#     data = request.get_json()
#     symbol = data.get("symbol")
#     target_buy = data.get("target_buy")
#     target_sell = data.get("target_sell")

#     session = SessionLocal()
#     new_stock = TrackedStock(
#         symbol=symbol,
#         target_buy=target_buy,
#         target_sell=target_sell
#     )
#     session.add(new_stock)
#     session.commit()
#     session.close()
#     return jsonify({"message": f"{symbol} added successfully!"}), 201

# @app.route("/dashboard", methods=["GET"])
# def dashboard():
#     ticker = request.args.get("ticker").upper()
#     session = SessionLocal()

#     stock = session.query(TrackedStock).filter_by(symbol=ticker).first()

#     if not stock:
#         stock = TrackedStock(symbol=ticker, target_buy=140.0, target_sell=180.0)
#         session.add(stock)
#         session.commit()

#     current_price = 150.0

#     if current_price <= stock.target_buy:
#         action = "BUY"
#     elif current_price >= stock.target_sell:
#         action = "SELL"
#     else:
#         action = "HOLD"

#     alert = AlertHistory(stock_id=stock.id, alert_type=f"{action} Alert", price_at_alert=current_price)
#     session.add(alert)
#     session.commit()
#     session.close()

#     return render_template("dashboard.html", ticker=ticker, price=current_price, action=action)