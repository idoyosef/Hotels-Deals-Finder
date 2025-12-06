import os
import requests
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

# --- Constants ---
CURRENCY_SYMBOLS = {"ILS": "₪", "USD": "$", "EUR": "€", "GBP": "£"}


def get_shortened_link(url):
    """Shortens a URL."""
    try:
        params = {"url": url}
        response = requests.post(os.getenv("LINK_SHORTENER_URL"), params=params)
        response.raise_for_status()
        data = response.json()
        return data["data"]["url"]
    except Exception as e:
        print(f"Failed to shorten link: {e}")
        return url


def fetch_exchange_rate(currency_code):
    """Fetches the exchange rate from USD to the target currency."""
    try:
        response = requests.get(url=os.getenv("EXCHANGE_RATES_URL")).json()
        return response["conversion_rates"].get(currency_code.upper(), None)
    except Exception as e:
        print(f"Failed to get exchange rates: {e}")
        return None


def is_valid_email(email: str):
    """Validates an email address format."""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def calculate_days(date1_str, date2_str):
    """Calculates the total number of nights between two dates."""
    try:
        d1 = datetime.strptime(date1_str, "%Y-%m-%d").date()
        d2 = datetime.strptime(date2_str, "%Y-%m-%d").date()
        return abs((d1 - d2).days)
    except ValueError:
        return 0


def get_children_ages(children_str, babies_str):
    """Calculates the comma-separated string of children's ages for the API."""
    try:
        children = int(children_str)
        babies = int(babies_str)
    except ValueError:
        return None, "Please enter valid numbers for children and babies."

    if babies < 0 or children < 0:
        return None, "Number of children and babies cannot be negative."

    if babies > children:
        return None, "Number of babies cannot exceed the total number of children."

    children_over_2 = children - babies
    ages_of_children_list = []

    ages_of_children_list.extend(['0'] * babies)
    ages_of_children_list.extend(['10'] * children_over_2)

    return ",".join(ages_of_children_list), None