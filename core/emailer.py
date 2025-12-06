from smtplib import SMTP_SSL, SMTPAuthenticationError, SMTPException
from email.message import EmailMessage
import os

from . import utils
from tkinter import messagebox

class EmailAuthenticationError(Exception):
    pass

class EmailConnectionError(Exception):
    pass

class EmailSender:
    def __init__(self):
        # Credentials are read from environment variables loaded in main.py
        self.sender = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_APP_PASSCODE")

    def send_deals_to_email(self, name, email, target_price, currency, details):
        """Sends an email with found hotel deals."""
        if not self.sender or not self.password:
            messagebox.showerror("Email Error", "Email credentials (EMAIL_USERNAME/PASSCODE) are missing.")
            return

        receiver = email
        msg = EmailMessage()
        msg["From"] = self.sender
        msg["To"] = receiver
        msg["Subject"] = f"We found new deals below your target price of {target_price}{utils.CURRENCY_SYMBOLS[currency]}!"
        msg.set_content(f"""Hi {name},
        \nWe found some deals that you might be interested in:
        \n{details}\nBest wishes,\nHotels Deals Finder.""")

        try:
            with SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender, self.password)
                server.send_message(msg)
        except SMTPAuthenticationError:
            raise EmailAuthenticationError("Authentication failed. Check Gmail App Password.")
        except SMTPException as e:
            raise EmailConnectionError(f"An error occurred while trying to send an email: {e}")