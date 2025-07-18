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
            # ticker = "FAKE COMPANY"
            # decision = "INVALID SYMBOL"
        print(f"(Demo) You asked to trade: {ticker}, we have decided to {decision}")

    return render_template("trade.html", decision=decision, ticker=ticker)

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
    