import os
import requests
from dotenv import load_dotenv

load_dotenv()

# finnhub (insider transactions)
finnhub_api_key = os.getenv("FINNHUB_API_KEY")
finnhub_base_url = "https://finnhub.io/api/v1/"
insider_url = finnhub_base_url + "/stock/insider-transactions?symbol"
headers = {
    "X-Finnhub-Token": finnhub_api_key
}

# response = requests.get(insider_url, headers=headers)
# print(response.status_code)
# finnhub_data = response.json()
# company = finnhub_data["symbol"]
# transactions = [t for t in finnhub_data["data"]]

# date of transactions (accurate, past few days)
# for t in transactions:
#     print(t["filingDate"])

# BUY and SELL decisions based on insider transactions
# decisions = []
# for t in transactions:
#     if t["change"] > 0:
#         decisions.append("BUY")
#     else:
#         decisions.append("SELL")
# print(decisions)


# alpha vantage (RSI, current_price, SMA)
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
alpha_vantage_base_url = "https://www.alphavantage.co/query?function="

# RSI
RSI_portion = 'RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=ALPHA_VANTAGE_API_KEY'
# response = requests.get(alpha_vantage_base_url + RSI_portion)
# print(response.status_code)
# RSI_data = response.json()
# RSI_info = RSI_data["Meta Data"]
# company = RSI_info["1: Symbol"]
# last_refreshed = RSI_info["3: Last Refreshed"]
# RSI = RSI_data["Technical Analysis: RSI"][last_refreshed]["RSI"]
# print(f"{company} RSI: {RSI} on {last_refreshed}")

# SMA
SMA_portion = "SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=ALPHA_VANTAGE_API_KEY"
# response = requests.get(alpha_vantage_base_url + SMA_portion)
# print(response.status_code)
# SMA_data = response.json()
# SMA_info = SMA_data["Meta Data"]
# company = SMA_info["1: Symbol"]
# last_refreshed = SMA_info["3: Last Refreshed"]
# SMA = SMA_data["Technical Analysis: SMA"][last_refreshed]["SMA"]
# print(f"{company} SMA: {SMA} on {last_refreshed}")

# current price
current_price_portion = "GLOBAL_QUOTE&symbol=IBM&apikey=ALPHA_VANTAGE_API_KEY"
# response = requests.get(alpha_vantage_base_url + current_price_portion)
# print(response.status_code)
# current_price_data = response.json()["Global Quote"]
# company = current_price_data["01. symbol"]
# current_price = current_price_data["05. price"]
# trading_date = current_price_data["07. latest trading day"]
# print(f"{company}: {current_price} on {trading_date}")