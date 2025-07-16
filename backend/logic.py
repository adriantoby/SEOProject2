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
# print(response.json())


# alpha vantage (RSI, current_price, SMA)
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
alpha_vantage_base_url = "https://www.alphavantage.co/query?function="

# RSI
RSI_portion = 'RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=ALPHA_VANTAGE_API_KEY'
# response = requests.get(alpha_vantage_base_url + RSI_portion)
# print(response.json())

# SMA
SMA_portion = "SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=ALPHA_VANTAGE_API_KEY"
# response = requests.get(alpha_vantage_base_url + SMA_portion)
# print(response.json())

# current price
current_price_portion = "GLOBAL_QUOTE&symbol=IBM&apikey=ALPHA_VANTAGE_API_KEY"
# response = requests.get(alpha_vantage_base_url + current_price_portion)
# print(response.json())