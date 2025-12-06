import requests
import math
from tkinter import messagebox
import os
from dotenv import load_dotenv
from . import utils


class HotelService:
    def __init__(self):
        load_dotenv()

        self.rapidapi_headers = {
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "x-rapidapi-host": os.getenv("RAPID_API_HOST"),
        }


    def get_hotels(self, user_choice, target_price=0):
        """Manages the hotel search, rate retrieval, and result formatting."""
        exchange_rate = utils.fetch_exchange_rate(user_choice["currency"])
        if exchange_rate is None:
            return ""

        # 1. Search for hotels in the city
        search_params = {
            "location_type": "accommodation",
            "query": user_choice["city"]
        }
        try:
            search_resp = requests.get(os.getenv("SEARCH_URL"), headers=self.rapidapi_headers, params=search_params)
            search_resp.raise_for_status()
            search_data = search_resp.json()
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to search for hotels: {e}")
            return ""

        if not search_data.get("result") or not search_data["result"].get("list"):
            return ""

        hotels = search_data["result"]["list"]
        results = ""

        for hotel in hotels:
            hotel_name = hotel["name"]
            hotel_key = hotel["hotel_key"]
            hotel_url = hotel["url"]

            if user_choice["wanted_hotel"].lower() not in hotel_name.lower():
                continue

            # 2. Get rates for the specific hotel
            rates_params = {
                "hotel_key": hotel_key,
                "chk_in": user_choice["chk_in"],
                "chk_out": user_choice["chk_out"],
                "adults": user_choice["adults"],
                "age_of_children": user_choice["children"],
            }
            try:
                rates_resp = requests.get(url=os.getenv("RATES_URL"), params=rates_params)
                rates_resp.raise_for_status()
                rates_data = rates_resp.json()
            except Exception as e:
                print(f"Failed to get rates for {hotel_name}: {e}")
                continue

            rates = rates_data["result"].get("rates", [])
            check_in_date = rates_data["result"]["chk_in"]
            check_out_date = rates_data["result"]["chk_out"]

            temp_results = ""
            deal_found = False

            if rates:
                temp_results += f"{hotel_name}:\n"
                for entry in rates:
                    website = entry["name"]
                    price_per_night_usd = (entry["rate"] + entry["tax"])
                    price_per_night_target = math.ceil(price_per_night_usd * exchange_rate)

                    num_days = utils.calculate_days(check_in_date, check_out_date)
                    total_price = num_days * price_per_night_target

                    # 3. Apply target price filter
                    if target_price == 0 or total_price <= target_price:
                        deal_found = True
                        currency_symbol = utils.CURRENCY_SYMBOLS.get(user_choice['currency'])
                        temp_results += f"  Website: {website}\n"
                        temp_results += f"  Price: {total_price}{currency_symbol}\n\n"

            if deal_found:
                new_link = utils.get_shortened_link(hotel_url)
                temp_results += "  View deals: "
                temp_results += f"{new_link}\n\n"
                results += temp_results

        return results