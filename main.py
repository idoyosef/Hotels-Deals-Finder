import json
import tkinter as tk
import gui
import os
import sys
from core import hotels
from core.emailer import EmailSender, EmailAuthenticationError, EmailConnectionError


def run_headless():
    """Runs existing saved preferences without GUI."""
    if os.path.exists("saved_preferences.json"):
        with open("saved_preferences.json", "r") as file:
            data = json.load(file)

        target_price = int(data["target_price"])
        hotel_service = hotels.HotelService()
        results = hotel_service.get_hotels(data, target_price)

        if len(results) > 0:
            try:
                email_sender = EmailSender()
                email_sender.send_deals_to_email(
                    data["name"],
                    data["email"],
                    data["target_price"],
                    data["currency"],
                    results
                )
            except (EmailAuthenticationError, EmailConnectionError) as e:
                print(e)
            else:
                print("Email sent successfully!")
                os.remove("saved_preferences.json")
        else:
            print("No results found.")
    else:
        print("There are no saved preferences.")


def main():
    # Runs in HEADLESS mode
    if "--headless" in sys.argv:
        print("Running in headless mode...")
        run_headless()
    else:
        print("Starting Hotel Deal Finder GUI...")
        root = tk.Tk()
        app = gui.HotelDealFinderApp(root)
        root.mainloop()


if __name__ == "__main__":
    main()