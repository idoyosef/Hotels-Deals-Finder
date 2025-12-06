import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta

# Import the core modules
from core import hotels, utils, preferences


class HotelDealFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Deal Finder")
        self.city_var = tk.StringVar()
        self.hotel_var = tk.StringVar()
        self.currency_var = tk.StringVar(value="ILS")
        self.adults_var = tk.StringVar(value="2")
        self.children_var = tk.StringVar(value="0")
        self.babies_var = tk.StringVar(value="0")

        self.hotel_service = hotels.HotelService()

        self.setup_styles()
        self.create_widgets()


    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        primary_color = "#2563EB"
        accent_color = "#1E40AF"
        text_color = "#111827"
        bg_color = "#F3F4F6"

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"),
                        padding=6, background=primary_color, foreground="white", borderwidth=0)
        style.map("TButton",
                  background=[("active", accent_color)],
                  relief=[("pressed", "sunken")])
        style.configure("TCombobox", padding=4, font=("Segoe UI", 10),
                        fieldbackground="white", background="white")
        style.configure("TEntry", padding=4, font=("Segoe UI", 10), fieldbackground="white", background="white")

    def create_widgets(self):
        # --- Header ---
        header = tk.Label(self.root, text="🏨 Hotel Deal Finder",
                          font=("Segoe UI Semibold", 16), bg="#F3F4F6", fg="#2563EB")
        header.pack(pady=(15, 10))

        # --- Form Frame ---
        form_frame = ttk.Frame(self.root, padding=10)
        form_frame.pack(fill="x", padx=20, pady=5)
        form_frame.columnconfigure(1, weight=1)

        # Helper for form fields
        def add_field(label, variable, row):
            ttk.Label(form_frame, text=label + ":", anchor="w").grid(row=row, column=0, sticky="w", pady=3)
            ttk.Entry(form_frame, textvariable=variable, width=30).grid(row=row, column=1, sticky="ew", pady=3)

        # Fields
        add_field("City", self.city_var, 0)
        add_field("Hotel Name", self.hotel_var, 1)

        # Currency Dropdown
        ttk.Label(form_frame, text="Currency:").grid(row=2, column=0, sticky="w", pady=3)
        currency_dropdown = ttk.Combobox(form_frame, textvariable=self.currency_var,
                                         values=["ILS", "USD", "EUR", "GBP"],
                                         width=27, state="readonly")
        currency_dropdown.grid(row=2, column=1, sticky="ew", pady=3)
        dropdown_style = ttk.Style()
        dropdown_style.map('TCombobox',
                           fieldbackground=[('readonly', 'white')],
                           selectbackground=[('readonly', 'white')],
                           selectforeground=[('readonly', 'black')])

        add_field("Number of Adults", self.adults_var, 3)
        add_field("Number of Children", self.children_var, 4)
        add_field("Children under 2 years", self.babies_var, 5)

        # Date Pickers
        today = date.today()
        one_year_from_now = today + timedelta(days=365)

        ttk.Label(form_frame, text="Check-in Date:").grid(row=6, column=0, sticky="w", pady=3)
        self.checkin_picker = DateEntry(form_frame, mindate=today, maxdate=one_year_from_now,
                                        date_pattern="yyyy-mm-dd", firstweekday="sunday", weekenddays=[6, 7])
        self.checkin_picker.grid(row=6, column=1, sticky="ew", pady=3)

        ttk.Label(form_frame, text="Check-out Date:").grid(row=7, column=0, sticky="w", pady=3)
        self.checkout_picker = DateEntry(form_frame, mindate=today, maxdate=one_year_from_now,
                                         date_pattern="yyyy-mm-dd", firstweekday="sunday", weekenddays=[6, 7])
        self.checkout_picker.grid(row=7, column=1, sticky="ew", pady=3)

        # --- Buttons ---
        btn_frame = ttk.Frame(self.root, padding=8)
        btn_frame.pack(fill="x", padx=20, pady=5)

        search_btn = ttk.Button(btn_frame, text="🔍 Search Hotels", command=self.search_hotels)
        search_btn.pack(side="left", padx=(0, 10))

        self.notification_button = ttk.Button(btn_frame, text="🔔 Get Notification", state="disabled")
        self.notification_button.pack(side="left")

        # --- Results Box ---
        results_label = ttk.Label(self.root, text="Results:")
        results_label.pack(anchor="w", padx=25, pady=(8, 0))

        self.results_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=22, font=("Consolas", 10),
                                                     bg="white", relief="solid", borderwidth=1)
        self.results_box.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    def get_user_preferences(self):
        """Collects and validates user input from the GUI."""
        children_ages, error = utils.get_children_ages(self.children_var.get(), self.babies_var.get())
        if error:
            messagebox.showwarning("Input Error", error)
            return None

        user_choice = {
            "city": self.city_var.get().strip(),
            "wanted_hotel": self.hotel_var.get().strip(),
            "currency": self.currency_var.get().strip().upper(),
            "adults": self.adults_var.get(),
            "children": children_ages,
            "chk_in": self.checkin_picker.get_date().strftime("%Y-%m-%d"),
            "chk_out": self.checkout_picker.get_date().strftime("%Y-%m-%d"),
        }
        # Basic validation (moved from utils to here, as this is GUI validation)
        if not user_choice["city"].isalpha():
            messagebox.showwarning("Input Error", "Please enter a valid city name (letters only).")
            return None
        if user_choice["wanted_hotel"] and not user_choice["wanted_hotel"].replace(" ", "").isalnum():
            messagebox.showwarning("Input Error", "Please enter a valid hotel name (letters and numbers).")
            return None
        if user_choice["chk_out"] <= user_choice["chk_in"]:
            messagebox.showwarning("Input Error", "Check-out date must be after check-in date.")
            return None
        if not user_choice["adults"].isdigit() or int(user_choice["adults"]) < 1:
            messagebox.showwarning("Input Error", "Please enter a valid number of adults (1 or more).")
            return None

        return user_choice

    def search_hotels(self):
        self.results_box.delete('1.0', tk.END)
        self.notification_button.config(state="disabled")

        user_choice = self.get_user_preferences()
        if not user_choice:
            return

        try:
            # CALLS THE CORE SERVICE
            results = self.hotel_service.get_hotels(user_choice, target_price=0)
            self.results_box.insert(tk.END, results)

            if results:
                self.notification_button.config(state="active", command=lambda: self.get_notification(user_choice))
            else:
                messagebox.showinfo("Search Results",
                                    f"No hotels found in {user_choice['city']} for your chosen dates.")

        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred during search: {e}")
            print(f"Error: {e}")

    def get_notification(self, user_preferences):
        """Displays a popup window for the user to enter notification details."""
        popup_window = tk.Toplevel(self.root)
        popup_window.title("Get notification")
        popup_window.geometry("300x360")

        # Popup widgets
        label = ttk.Label(popup_window, text="Enter your contact info and target price below:")
        label.pack(pady=20)

        user_name = ttk.Label(popup_window, text="Name:")
        user_name.pack()
        name_var = tk.StringVar()
        ttk.Entry(popup_window, textvariable=name_var).pack()

        user_email = ttk.Label(popup_window, text="E-Mail:")
        user_email.pack()
        email_var = tk.StringVar()
        ttk.Entry(popup_window, textvariable=email_var).pack()

        target_price = ttk.Label(popup_window, text="Target Price:")
        target_price.pack()
        price_var = tk.StringVar(value="0")
        ttk.Entry(popup_window, textvariable=price_var).pack()

        def save_and_notify():
            name = name_var.get()
            email = email_var.get()
            price = price_var.get()

            # CALLS THE CORE PREFERENCES/UTILS
            success = preferences.check_details(name, email, price, user_preferences)

            if success:
                popup_window.destroy()
                messagebox.showinfo("Success", f"Your details have been saved.\n"
                                               f"We will keep you updated via e-mail when"
                                               f" we find deals within your budget.")

        get_notification_button = ttk.Button(popup_window, text="Get notification",
                                             command=save_and_notify)
        get_notification_button.pack(pady=20)

        close_button = ttk.Button(popup_window, text="Close", command=popup_window.destroy)
        close_button.pack(pady=25)