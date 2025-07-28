from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from supabase import create_client, Client
from backend.logic import ask_gemini
from backend.decision_logic import process_stock
from backend.test_db import return_stocks, add_user
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)
session = None

@app.route("/") # home page
@app.route("/home")
def home():
    if not session or not session.access_token:
        return redirect(url_for('signup'))
    return render_template("home.html")

@app.route("/about") # about page
def about():
    if not session or not session.access_token:
        return redirect(url_for('signup'))
    return render_template("about.html")

@app.route("/trade", methods=["GET", "POST"]) # trade page
def trade():
    if not session or not session.access_token:
        return redirect(url_for('signup'))
    decision = None
    ticker = None
    stocks = None
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        if ticker:
            decision = process_stock(ticker)
            # ticker = "IBM"
            # decision = "BUY"
            stocks = return_stocks()
            print(f"(Demo) You asked to trade: {ticker}, we have decided to {decision}")

    return render_template("trade.html", decision=decision, ticker=ticker, stocks=stocks)

@app.route("/assistant", methods=["GET", "POST"]) # GENAI assistant 
def assistant():
    if not session or not session.access_token:
        return redirect(url_for('signup'))
    ai_answer = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            ai_answer = ask_gemini(user_input)
        print(f"(Demo) You asked: {user_input}")
    return render_template("assistant.html", ai_answer=ai_answer)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = supabase.auth.sign_up({"email": email, "password": password})
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error during sign up: {e}")
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            global session
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session = response.session
            print(session)
            return redirect(url_for('home'))
        except Exception as e:
            print(f"Error during login: {e}")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # if not session or not session.access_token:
    #     return redirect(url_for('signup'))
    if request.method == "POST":
        try:
            supabase.auth.sign_out()
            global session
            session = None
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error during logout: {e}")
            return redirect(url_for('logout'))
    return render_template('logout.html')

@app.route("/profile") #Profile Page
def profile():
    return render_template("profile.html")

            
if __name__ == "__main__":
    app.run(debug=True)
    