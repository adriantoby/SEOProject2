import os
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


# finnhub (insider transactions)
def get_insider_transactions(symbol):
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


# alpha vantage (RSI, current_price, SMA)
def get_RSI(symbol):
    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    alpha_vantage_base_url = "https://www.alphavantage.co/query?function="

    RSI_portion = f'RSI&symbol={symbol}&interval=weekly&time_period=10&series_type=open&apikey=ALPHA_VANTAGE_API_KEY'
    response = requests.get(alpha_vantage_base_url + RSI_portion)
    # print(response.status_code)
    RSI_data = response.json()
    RSI_info = RSI_data["Meta Data"]
    company = RSI_info["1: Symbol"]
    last_refreshed = RSI_info["3: Last Refreshed"]
    RSI = RSI_data["Technical Analysis: RSI"][last_refreshed]["RSI"]
    # print(f"{company} RSI: {RSI} on {last_refreshed}")
    return float(RSI)

def get_SMA(symbol):
    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    alpha_vantage_base_url = "https://www.alphavantage.co/query?function="
    SMA_portion = f"SMA&symbol={symbol}&interval=weekly&time_period=10&series_type=open&apikey=ALPHA_VANTAGE_API_KEY"
    response = requests.get(alpha_vantage_base_url + SMA_portion)
    # print(response.status_code)
    SMA_data = response.json()
    SMA_info = SMA_data["Meta Data"]
    company = SMA_info["1: Symbol"]
    last_refreshed = SMA_info["3: Last Refreshed"]
    SMA = SMA_data["Technical Analysis: SMA"][last_refreshed]["SMA"]
    # print(f"{company} SMA: {SMA} on {last_refreshed}")
    return float(SMA)

def get_current_price(symbol):
    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    alpha_vantage_base_url = "https://www.alphavantage.co/query?function="
    current_price_portion = f"GLOBAL_QUOTE&symbol={symbol}&apikey=ALPHA_VANTAGE_API_KEY"
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
    my_api_key = os.getenv('GENAI_API_KEY')

    client = genai.Client(
        api_key=my_api_key,
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="""You are a master of stocks and finances, and can
            help with any question related to stocks, finances, and anything related
            to that field. You answer in a brief paragraph, providing the most relevant
            and accurate information to the user. You provide answers like a human
            mentor speaking out loud, so do not use any markdown nor code."""),
        contents=question,
    )

    return response.text

# if __name__ == "__main__":
#     print(ask_gemini("What is an RSI"))
