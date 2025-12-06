# 🏨 Hotel Deal Finder

A Tkinter application to search for hotel deals using the Xotelo API and notify users via email when a target price is met.

## 🚀 Project Structure

This project follows a modular structure to maintain separation of concerns (SOLID principles):

* `main.py`: Application entry point, handles CLI arguments (e.g., `--gui`).
* `gui.py`: Contains the Tkinter GUI implementation.
* `core/`: Contains the business logic and external service layers.
    * `hotels.py`: Handles all external API interactions (Xotelo, Exchange Rate, Link Shortener).
    * `emailer.py`: Handles sending emails via Gmail SMTP.
    * `preferences.py`: Handles reading/writing user notification preferences.
    * `utils.py`: Contains general helper functions (date math, currency constants, validation).

## 🛠️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [your_repo_url]
    cd hotel-deal-finder
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    * Rename `.env.example` to **`.env`**.
    * Fill in your `EMAIL_USERNAME` and `EMAIL_APP_PASSCODE`. (Note: Gmail requires an App Password for SMTP.)

4.  **Run the application:**
    ```bash
    python main.py --gui
    # or simply
    python main.py
    ```