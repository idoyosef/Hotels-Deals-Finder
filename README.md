# 🏨 Hotels Deals Finder

Hotels Deals Finder is a Python application that automates the process of finding the best hotel offers based on user-defined preferences.
It provides a modern GUI for hotel searching, saving preferences, and sending email alerts — as well as a headless mode for automated or scheduled checks.
The project integrates external APIs, secret management with environment variables, data validation, and a modular service-based architecture.

## 🎮 Demo

<img src="https://github.com/idoyosef/Hotels-Deals-Finder/blob/main/screenshot.png" alt="Hotels Deals Finder GUI Screenshot" height="400" width="400"/>

## 🚀 Features

- Modern GUI Interface
    -	Built with Tkinter
    -	Intuitive input fields, date selection, and results display
    -	Validation for all fields
    -	Saves user preferences automatically
    -	Clean layout with scrolling results and error dialogs
- Headless Automation Mode
  - Run the tool without the GUI to automatically:
    -	Load saved preferences
    -	Search for updated hotel deals
    -	Send results directly via email
  - Useful for CRON jobs and automated daily scans.
- Hotel Search Service
    -	API-based querying
    -	Sorting, filtering and price checking
    -	Error-handling for unavailable or invalid results
- Email Sending
    -	Custom email sending system
    -	Distinct exceptions for authentication and connectivity
    -	Detailed success and failure messages
    -	Uses secure environment variables
- Preferences System
    -	JSON-based user preference saving
    -	Shared between GUI and headless mode
    -	Includes city, date range, price limits, and more
 

## 📦 Project Structure

This project follows a modular structure to maintain separation of concerns (SOLID principles):

* `main.py`: Application entry point, handles CLI arguments for headless implementation (e.g., `--headless`).
* `gui.py`: Contains the Tkinter GUI implementation.
* `core/`: Contains the business logic and external service layers.
    * `hotels.py`: Handles all external API interactions (Xotelo, Exchange Rate, Link Shortener).
    * `emailer.py`: Handles sending emails via Gmail SMTP.
    * `preferences.py`: Handles reading/writing user notification preferences.
    * `utils.py`: Contains general helper functions (date math, currency constants, validation).
    * `.env.example`: Contains Email credentials and API keys (Email credentials and Rapid API key should be filled in by the user).

## 🛠️ Setup and Installation

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment Variables:**
    * Rename `.env.example` to **`.env`**.
    * Fill in your `RAPID_API_KEY`, `EMAIL_USERNAME` and `EMAIL_APP_PASSCODE`. (Note: Gmail requires an App Password for SMTP.)


3.  **Run the application:**
    ```bash
    python main.py 
    # for launching GUI
	
    python main.py --headless
    # for running in headless mode
    ```

## 🧠 Technical Highlights

- Modular/clean architecture
- GUI separated from business logic
- Error-resistant email system
- Secure credentials handling
- Supports both manual and automated operation
- Fully validated user inputs