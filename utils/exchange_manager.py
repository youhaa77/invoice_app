import json
import os
import requests
from datetime import datetime, timedelta

# Path to local JSON cache
CACHE_FILE = "exchange_rates.json"
API_URL = "https://v6.exchangerate-api.com/v6/dc309a3ff4827edc59610c17/latest/USD"

# In-memory cache
exchange_data = {
    "conversion_rates": {},
    "last_update": None
}

def load_rates_from_file():
    """Load exchange rates from local JSON file if available."""
    if not os.path.exists(CACHE_FILE):
        return False
    
    with open(CACHE_FILE, "r") as f:
        data = json.load(f)
    
    # Check if file is older than 24 hours
    last_update = datetime.fromisoformat(data["last_update"])
    if datetime.utcnow() - last_update > timedelta(hours=24):
        return False

    exchange_data["conversion_rates"] = data["conversion_rates"]
    exchange_data["last_update"] = last_update
    return True


def save_rates_to_file(rates):
    """Save exchange rates to local JSON file."""
    data = {
        "conversion_rates": rates,
        "last_update": datetime.utcnow().isoformat()
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    
    exchange_data["conversion_rates"] = rates
    exchange_data["last_update"] = datetime.utcnow()


def fetch_rates_from_api():
    """Fetch latest exchange rates from API."""
    print(f"[{datetime.utcnow().isoformat()}] Fetching new exchange rates from API...")
    try:
        response = requests.get(API_URL)
        data = response.json()
        if "conversion_rates" not in data:
            raise Exception("Invalid API response")
        save_rates_to_file(data["conversion_rates"])
        print(" Exchange rates updated successfully.")
        return data["conversion_rates"]
    except Exception as e:
        print("Error fetching exchange rates:", e)
        return None


def get_exchange_rates():
    """Get current exchange rates (cached or fetched if needed)."""
    # if cache empty OR older than 24h → reload
    if (
        not exchange_data["conversion_rates"]
        or not exchange_data["last_update"]
        or datetime.utcnow() - exchange_data["last_update"] > timedelta(hours=24)
    ):
        if not load_rates_from_file():
            fetch_rates_from_api()
    return exchange_data["conversion_rates"]
