from flask import Flask, render_template, request, jsonify
from backend.logic import ask_gemini, get_company_logo
from backend.decision_logic import process_stock
from backend.test_db import return_stocks
from backend.database import AvailableStock, SessionLocal

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
    ticker = None
    stocks = None
    logo = None
    explanation = None
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        if ticker:
            decision, explanation = process_stock(ticker)
            stocks = return_stocks()
            logo = get_company_logo(ticker)
    return render_template("trade.html", decision=decision, ticker=ticker, stocks=stocks, logo=logo, explanation=explanation)

@app.route("/assistant", methods=["GET", "POST"]) # GENAI assistant 
def assistant():
    ai_answer = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            ai_answer = ask_gemini(user_input)
    return render_template("assistant.html", ai_answer=ai_answer)

@app.route("/api/all-stocks")   
def get_all_stocks():
    session = SessionLocal()
    stocks = session.query(AvailableStock).all() #gets all records(rows) from the database
    session.close()
    
    stock_list = [
        {
            "symbol": stock.symbol,
            "name": stock.company_name
        }
        for stock in stocks
    ]
    
    return jsonify(stock_list) #need this or you get a weird 500 error, its needed to convert into a valid json response object      
if __name__ == "__main__":
    app.run(debug=True)
    