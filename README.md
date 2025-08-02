# Telegram Username Registrar

A Python script leveraging the [Telethon](https://github.com/LonamiWebs/Telethon) library to securely login to Telegram and automate the registration of public channel usernames. This tool supports both single username registration and bulk registration from a file, with session persistence to avoid repeated logins.

---

## Features

- **Secure Telegram Login**  
  Login using phone number, OTP, and optional two-factor authentication (2FA). Session files are saved locally to reuse on subsequent runs, eliminating the need for repeated login prompts.

- **Single & Bulk Username Registration**  
  Register a single username on demand or bulk-register multiple usernames by reading from a `username.txt` file.

- **Username Validation**  
  Validates usernames to comply with Telegram's rules:  
  - Length between 5 and 32 characters  
  - Starts with a letter  
  - Contains only letters, digits, and underscores  
  - No consecutive underscores

- **Robust Error Handling**  
  Handles username conflicts (already taken), invalid usernames, and other API errors gracefully with clear feedback.

- **User-Friendly CLI Menu**  
  Interactive command-line menu to guide through login and username registration tasks.

- **Session Persistence**  
  Saves Telegram session securely in a local file (`session.session`) for automatic login on subsequent runs.

---

## Requirements

- Python 3.7+  
- [Telethon](https://pypi.org/project/telethon/) library

---

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/tg-username-registrar.git
    cd tg-username-registrar
    ```

2. Install dependencies:
    ```bash
    pip install telethon
    ```

3. Replace `API_ID` and `API_HASH` in the script with your own Telegram API credentials from [my.telegram.org/apps](https://my.telegram.org/apps).

---

## Usage

Run the script:

```bash
python autopk.py


You will see a menu:

=== Telegram Channel Username Registrar ===
1. Login to Telegram
2. Register a single username
3. Mass register usernames from username.txt
0. Exit
Select an option:
