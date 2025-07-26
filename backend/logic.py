import os
import requests
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv


def get_insider_transactions(symbol):
    """
    Determines a BUY, SELL, or HOLD decision based on recent insider transactions.

    Parameters:
        symbol (str): The stock ticker symbol (e.g., 'AAPL').

    Returns:
        str: One of "BUY", "SELL", or "HOLD" based on insider activity.
    """
    load_dotenv()
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    finnhub_base_url = "https://finnhub.io/api/v1/"
    insider_url = finnhub_base_url + f"/stock/insider-transactions?symbol={symbol}"
    headers = {
        "X-Finnhub-Token": finnhub_api_key
    }

    response = requests.get(insider_url, headers=headers)
    # print(response.status_code)
    finnhub_data = response.json()
    company = finnhub_data["symbol"]
    transactions = [t for t in finnhub_data["data"]]

    # date of transactions (accurate, past few days)
    # for t in transactions:
    #     print(t["filingDate"])

    # BUY and SELL decisions based on insider transactions
    decisions = [0, 0]
    for t in transactions:
        if t["change"] > 0:
            decisions[0] += 1
        else:
            decisions[1] += 1

    if decisions[0] > decisions[1]:
        decision = "BUY"
    elif decisions[1] > decisions[0]:
        decision = "SELL"
    else:
        decision = "HOLD"
    
    return decision


def get_RSI(symbol):
    """
    Fetches the Relative Strength Index (RSI) for a given stock symbol over weekly intervals.

    Parameters:
        symbol (str): The stock ticker symbol.

    Returns:
        float: RSI value as a float (e.g., 42.56), or None if unavailable.
    """
    load_dotenv()
    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    alpha_vantage_base_url = "https://www.alphavantage.co/query?function="

    RSI_portion = f'RSI&symbol={symbol}&interval=weekly&time_period=10&series_type=open&apikey={alpha_vantage_api_key}'
    response = requests.get(alpha_vantage_base_url + RSI_portion)
    # print(response.status_code)
    RSI_data = response.json()
    if not RSI_data:
        return None
    RSI_info = RSI_data["Meta Data"]
    company = RSI_info["1: Symbol"]
    last_refreshed = RSI_info["3: Last Refreshed"]
    RSI = RSI_data["Technical Analysis: RSI"][last_refreshed]["RSI"]
    # print(f"{company} RSI: {RSI} on {last_refreshed}")
    return float(RSI)

def get_SMA(symbol):
    """
    Retrieves the 10-week Simple Moving Average (SMA) based on closing prices.

    Parameters:
        symbol (str): The stock ticker symbol.

    Returns:
        float: The calculated SMA value.
    """
    load_dotenv()
    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    alpha_vantage_base_url = "https://www.alphavantage.co/query?function="
    SMA_portion = f"SMA&symbol={symbol}&interval=weekly&time_period=10&series_type=close&apikey={alpha_vantage_api_key}"
    response = requests.get(alpha_vantage_base_url + SMA_portion)
    # print(response.status_code)
    SMA_data = response.json()
    SMA_info = SMA_data["Meta Data"]
    last_refreshed = SMA_info["3: Last Refreshed"]
    SMA = SMA_data["Technical Analysis: SMA"][last_refreshed]["SMA"]
    # print(f"{company} SMA: {SMA} on {last_refreshed}")
    return float(SMA)

def get_current_price(symbol):
    """
    Retrieves the current stock price for a given ticker using Alpha Vantage.

    Parameters:
        symbol (str): The stock ticker symbol.

    Returns:
        float: The latest available stock price.
    """
    load_dotenv()
    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    alpha_vantage_base_url = "https://www.alphavantage.co/query?function="
    current_price_portion = f"GLOBAL_QUOTE&symbol={symbol}&apikey={alpha_vantage_api_key}"
    response = requests.get(alpha_vantage_base_url + current_price_portion)
    # print(response.status_code)
    current_price_data = response.json()["Global Quote"]
    if not current_price_data:
        return None
    # print(current_price_data)
    company = current_price_data["01. symbol"]
    current_price = current_price_data["05. price"]
    trading_date = current_price_data["07. latest trading day"]
    # print(f"{company}: {current_price} on {trading_date}")
    return float(current_price)

def ask_gemini(question):
    """
    Sends a user-defined finance question to the Gemini AI model and retrieves a text-based answer.

    Parameters:
        question (str): The user’s question related to stocks or finance.

    Returns:
        str: Gemini's natural-language response.
    """
    load_dotenv()
    my_api_key = os.getenv('GENAI_API_KEY')

    genai.configure(api_key=my_api_key)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="""You are a master of stocks and finances, and can
        help with any question related to stocks, finances, and anything related
        to that field. You answer in a brief paragraph, providing the most relevant
        and accurate information to the user. You provide answers like a human
        mentor speaking out loud, so do not use any markdown nor code."""
    )

    response = model.generate_content(question)
    return response.text

def get_company_logo(symbol):
    """
    Fetches the company logo URL using Finnhub's company profile API.

    Parameters:
        symbol (str): The stock ticker symbol.

    Returns:
        str or None: URL string of the logo image, or None if not found.
    """
    load_dotenv()
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}"
    headers = {
        "X-Finnhub-Token": finnhub_api_key
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get("logo")
