import requests
import time

global API_KEY
API_KEY = "OhOis7n5SskS5OswmI7kqgqow66tCtiT"

def make_request_with_retry(url, params=None):
    """Helper function to make requests with retry on 429 error"""
    while True:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting 20 seconds before retrying...")
            time.sleep(20)  # Wait 20 seconds before retrying
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

def get_stock_price(ticker, date='2025-02-21'):
    url = f"https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted=true&apiKey={API_KEY}"
    response = make_request_with_retry(url)
    if response:
        data = response.json()
        return data.get("close")
    else:
        return None

def get_option_market(ticker, expiration=None, strike=None, contract="call"):
    base_url = "https://api.polygon.io/v3/reference/options/contracts"
    params = {"underlying_ticker": ticker, "contract_type": contract, "limit": 1000, "apiKey": API_KEY}
    if expiration:
        params["expiration_date"] = expiration
    if strike:
        params["strike_price"] = strike
    
    response = make_request_with_retry(base_url, params=params)
    if response:
        data = response.json()
        if "results" in data and data["results"]:
            return data["results"]
        else:
            print("No options contracts found.")
            return None
    return None
    
def get_option_contract_cost(option_code):
    url = f"https://api.polygon.io/v2/aggs/ticker/{option_code}/prev?adjusted=true&apiKey={API_KEY}"
    response = make_request_with_retry(url)
    if response:
        data = response.json()
        # Check if the response contains results
        if "results" in data and data["results"]:
            return data["results"][0]["c"]  # Return closing price
        else:
            print(f"No data found for option contract: {option_code}")
            return None
    return None

    
