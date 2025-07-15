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


# alpha vantage ()