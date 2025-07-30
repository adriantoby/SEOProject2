from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_behind_proxy import FlaskBehindProxy
from supabase import create_client, Client
from backend.logic import ask_gemini, get_company_logo, get_current_price, get_RSI, get_SMA
from backend.decision_logic import process_stock, analyze_stock
from backend.test_db import return_stocks, add_user
from backend.database import AvailableStock, SessionLocal, TrackedStock, AlertHistory, User
from dotenv import load_dotenv
from datetime import datetime
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

    try:
        supabase.auth.set_session(session.access_token, session.refresh_token)
    except:
        return redirect(url_for('login'))
    decision = None
    ticker = None
    stocks = None
    logo = None
    explanation = None
    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        if ticker:
            uid = supabase.auth.get_user().user.id
            decision, explanation = analyze_stock(ticker)
            stocks = return_stocks(uid)
            logo = get_company_logo(ticker)
    return render_template("trade.html", decision=decision, ticker=ticker, stocks=stocks, logo=logo, explanation=explanation)

@app.route("/assistant", methods=["GET", "POST"]) # GENAI assistant 
def assistant():
    if not session or not session.access_token:
        return redirect(url_for('signup'))
    ai_answer = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            ai_answer = ask_gemini(user_input)
    return render_template("assistant.html", ai_answer=ai_answer)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = supabase.auth.sign_up({"email": email, "password": password})
            if user:
                add_user(username, email, password) #so, i can get the username in the profile section.
            return redirect(url_for('login'))
        except Exception as e:
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
            return redirect(url_for('home'))
        except Exception as e:
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
    if not session or not session.access_token:
        return redirect(url_for('signup'))
    
    try:
        supabase.auth.set_session(session.access_token, session.refresh_token)
    except:
        return redirect(url_for('login'))
    # Get current user from Supabase
    user_data = supabase.auth.get_user().user
    uid = user_data.id
    email = user_data.email
    created_at = user_data.created_at
    member_since = created_at.strftime('%B %d, %Y')
    
    # Enhanced stock data with additional information
    db_session = SessionLocal()
    tracked_stocks = db_session.query(TrackedStock).filter(TrackedStock.uid == uid).all()
    
    watchlist = []
    for stock in tracked_stocks:
        # Get latest alert
        latest_alert = db_session.query(AlertHistory)\
            .filter(AlertHistory.stock_id == stock.id)\
            .order_by(AlertHistory.timestamp.desc())\
            .first()
        
        # Get current price and other data with error handling
        try:
            current_price = get_current_price(stock.symbol)
        except:
            current_price = None
        
        try:
            company_logo = get_company_logo(stock.symbol)
        except:
            company_logo = None
        
        try:
            rsi = get_RSI(stock.symbol)
            rsi = round(rsi, 2) if rsi else None
        except:
            rsi = None
        
        try:
            sma = get_SMA(stock.symbol)
            sma = round(sma, 2) if sma else None
        except:
            sma = None
        
        stock_card = {
            'id': stock.id,  # For untrack functionality
            'symbol': stock.symbol,
            'recommendation': latest_alert.alert_type if latest_alert else "No alerts",
            'current_price': current_price,
            'company_logo': company_logo,
            'rsi': rsi,
            'sma': sma,
            'date_started': stock.created_at.strftime('%B %d, %Y') if stock.created_at else 'Unknown'
        }
        watchlist.append(stock_card)
    
    # Get recent activity from AlertHistory
    recent_alerts = db_session.query(AlertHistory)\
        .filter(AlertHistory.uid == uid)\
        .order_by(AlertHistory.timestamp.desc())\
        .limit(10).all()
    
    recent_activity = []
    for alert in recent_alerts:
        stock = db_session.query(TrackedStock).filter(TrackedStock.id == alert.stock_id).first()
        if stock:
            activity_text = f"{alert.alert_type} alert for {stock.symbol} at ${alert.price_at_alert:.2f} on {alert.timestamp.strftime('%Y-%m-%d %H:%M')}"
            recent_activity.append(activity_text)
    
    if not recent_activity:
        recent_activity = ["No recent activity. Start tracking stocks to see alerts here!"]
    
    # Get username
    user = db_session.query(User).filter(User.email == email).first()
    username = user.username if user else email.split('@')[0]
    
    db_session.close()
    
    return render_template('profile.html', 
                         username=username, 
                         email=email, 
                         member_since=member_since, 
                         watchlist=watchlist, 
                         recent_activity=recent_activity)
    
@app.route("/untrack-stock", methods=["POST"])
def untrack_stock():
    if not session or not session.access_token:
        return redirect(url_for('signup'))
    
    try:
        supabase.auth.set_session(session.access_token, session.refresh_token)
    except:
        return redirect(url_for('login'))
    
    stock_id = request.form.get("stock_id")
    if not stock_id:
        flash("Invalid stock ID", "error")
        return redirect(url_for('profile'))
    
    uid = supabase.auth.get_user().user.id
    db_session = SessionLocal()
    
    try:
        # Find the stock to delete
        stock_to_delete = db_session.query(TrackedStock).filter(
            TrackedStock.id == stock_id,
            TrackedStock.uid == uid  # Ensure user owns this stock
        ).first()
        
        if stock_to_delete:
            # Delete associated alerts first (due to foreign key constraint)
            db_session.query(AlertHistory).filter(AlertHistory.stock_id == stock_id).delete()
            
            # Delete the tracked stock
            db_session.delete(stock_to_delete)
            db_session.commit()
            
            flash(f"Successfully removed {stock_to_delete.symbol} from your watchlist", "success")
        else:
            flash("Stock not found or you don't have permission to remove it", "error")
            
    except Exception as e:
        db_session.rollback()
        flash("An error occurred while removing the stock", "error")
        print(f"Error removing stock: {e}")
    finally:
        db_session.close()
    
    return redirect(url_for('profile'))

@app.route("/track-stock", methods=["POST"])
def track_stock():
    if not session or not session.access_token:
        return redirect(url_for('signup'))
    
    try:
        supabase.auth.set_session(session.access_token, session.refresh_token)
    except:
        return redirect(url_for('login'))
    
    ticker = request.form.get("ticker")
    if not ticker:
        flash("Invalid stock symbol", "error")
        return redirect(url_for('trade'))
    
    uid = supabase.auth.get_user().user.id
    
    # Use process_stock to actually add to database and log alert
    decision, explanation = process_stock(ticker.upper(), uid)
    
    if decision == "INVALID SYMBOL":
        flash(f"Could not track {ticker} - invalid symbol", "error")
    else:
        flash(f"Successfully added {ticker.upper()} to your watchlist with {decision} recommendation", "success")
    
    return redirect(url_for('trade'))

@app.route("/api/all-stocks")  
#get the stock name and symbol
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
    