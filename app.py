from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from backend.logic import ask_gemini
from backend.decision_logic import process_stock
from backend.test_db import return_stocks
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

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
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        if ticker:
            # decision = process_stock(ticker)
            ticker = "IBM"
            decision = "BUY"
            stocks = return_stocks()
            print(f"(Demo) You asked to trade: {ticker}, we have decided to {decision}")

    return render_template("trade.html", decision=decision, ticker=ticker, stocks=stocks)

@app.route("/assistant", methods=["GET", "POST"]) # GENAI assistant 
def assistant():
    ai_answer = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            ai_answer = ask_gemini(user_input)
        print(f"(Demo) You asked: {user_input}")
    return render_template("assistant.html", ai_answer=ai_answer)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
            
if __name__ == "__main__":
    app.run(debug=True)
    