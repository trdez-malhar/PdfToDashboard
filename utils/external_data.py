import requests
import os
from dotenv import load_dotenv
load_dotenv()
isin_endpoint = f"https://financialmodelingprep.com/stable/search-isin?isin="
# isin_endpoint = r"isin=US0378331005"&apikey=0DQnppt4tSkHumZK3GWVG1mZOHfjVhNu
SECRETKEY = os.getenv("APIKEY")
def get_isin_data(isin):
    # print(f"{isin_endpoint}{isin}&apikey={SECRETKEY}")
    response = requests.get(f"{isin_endpoint}{isin}&apikey={SECRETKEY}")
    # print(response)
    if response.status_code == 200:
        if response.json().__len__() > 0:
            return response.json()[0]["symbol"]
    return None
company_data_endpoint = "https://financialmodelingprep.com/stable/profile?symbol="
def get_company_profile(symbol):
    if symbol:
        # print(f"{company_data_endpoint}{symbol}?apikey={SECRETKEY}")
        response = requests.get(f"{company_data_endpoint}{symbol}&apikey={SECRETKEY}")
        if response.status_code == 200:
            if response.json().__len__() > 0:
                return response.json()[0]["industry"]
        return None