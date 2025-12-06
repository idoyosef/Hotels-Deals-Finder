import json
from tkinter import messagebox

from . import utils

def save_preferences(name, email, target_price, user_preferences):
    """Saves user notification preferences to a JSON file."""
    preferences = {
        "city": user_preferences["city"],
        "wanted_hotel": user_preferences["wanted_hotel"],
        "currency": user_preferences["currency"],
        "adults": user_preferences["adults"],
        "children": user_preferences["children"],
        "chk_in": user_preferences["chk_in"],
        "chk_out": user_preferences["chk_out"],
        "name": name,
        "email": email,
        "target_price": target_price,
    }

    try:
        with open("saved_preferences.json", 'w') as file:
            json.dump(preferences, file, indent=4)
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save preferences: {e}")


def check_details(name, email, price, user_preferences):
    """Validates notification details and saves preferences."""
    if not name.isalpha():
        messagebox.showerror("Validation Error", "Please enter a valid name (letters only).")
        return False

    if not utils.is_valid_email(email):
        messagebox.showerror("Validation Error", "Please enter a valid e-mail address.")
        return False

    if not price.isdigit() or int(price) < 0:
        messagebox.showerror("Validation Error", "Please enter a valid target price (non-negative number).")
        return False

    save_preferences(name, email, price, user_preferences)
    return True