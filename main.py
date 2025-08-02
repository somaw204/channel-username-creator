import os
import re
import asyncio
from telethon import TelegramClient, errors, functions

# === Configuration ===
API_ID = 21757615  # Replace with your API ID
API_HASH = '2fa60f09b1f9edc6f9cec0714850840f'  # Replace with your API Hash

SESSION_FILE = 'session.session'


def sanitize_username(username: str) -> str:
    """Remove '@' prefix and validate username format."""
    username = username.strip()
    if username.startswith('@'):
        username = username[1:]
    if not 5 <= len(username) <= 32:
        return None
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return None
    if '__' in username:
        return None
    return username.lower()


async def create_public_channel(client: TelegramClient, username: str):
    """
    Create a public Telegram channel with the given username.
    Returns True on success, False otherwise.
    """
    try:
        channel = await client(functions.channels.CreateChannelRequest(
            title=username,
            about=f'Public channel for @{username}',
            megagroup=False
        ))
        await client(functions.channels.UpdateUsernameRequest(
            channel=channel.chats[0].id,
            username=username
        ))
        print(f"[+] Channel @{username} created successfully.")
        return True
    except errors.UsernameOccupiedError:
        print(f"[-] Username @{username} is already taken.")
    except errors.UsernameInvalidError:
        print(f"[-] Username @{username} is invalid.")
    except Exception as e:
        print(f"[-] Failed to create channel @{username}: {str(e)}")
    return False


async def login():
    """
    Login flow using Telethon:
    - Load session file if exists, login automatically.
    - Otherwise, prompt for phone + OTP + optional 2FA password.
    - Session file is saved automatically by Telethon.
    """
    if os.path.exists(SESSION_FILE):
        print("[*] Loading existing session...")
        client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        await client.start()  # Will load session and login automatically
        print("[*] Logged in successfully using saved session.")
        return client

    # No session file - new login required
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        phone = input("Enter your phone number (with country code, e.g. +123456789): ").strip()
        try:
            await client.send_code_request(phone)
            code = input("Enter the code you received: ").strip()
            await client.sign_in(phone, code)
        except errors.SessionPasswordNeededError:
            password = input("Two-step verification enabled. Enter your password: ").strip()
            await client.sign_in(password=password)
        except Exception as e:
            print(f"Login failed: {e}")
            await client.disconnect()
            return None

    print("[*] Logged in successfully.")
    return client


async def register_single_username(client: TelegramClient):
    username = input("Enter username to register (with or without '@'): ").strip()
    username = sanitize_username(username)
    if not username:
        print("[-] Invalid username format. Must be 5-32 chars, letters, digits or underscores, start with a letter, no double underscores.")
        return
    await create_public_channel(client, username)


async def register_mass_usernames(client: TelegramClient):
    if not os.path.exists('username.txt'):
        print("[-] username.txt file not found.")
        return

    with open('username.txt', 'r', encoding='utf-8') as f:
        usernames = [sanitize_username(line) for line in f if line.strip()]
    usernames = [u for u in usernames if u]

    if not usernames:
        print("[-] No valid usernames found in username.txt.")
        return

    print(f"[*] Attempting to create {len(usernames)} channels...")

    for username in usernames:
        print(f"Trying @{username} ...")
        await create_public_channel(client, username)


async def main_menu():
    client = None

    while True:
        print("\n=== Telegram Channel Username Registrar ===")
        print("1. Login to Telegram")
        print("2. Register a single username")
        print("3. Mass register usernames from username.txt")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == '0':
            print("Exiting...")
            if client:
                await client.disconnect()
            break

        if choice == '1':
            if client:
                print("[*] Already logged in.")
            else:
                client = await login()
                if client is None:
                    print("[-] Login failed. Try again.")
        elif choice in ('2', '3'):
            if client is None:
                print("[-] You must login first (option 1).")
                continue
            if choice == '2':
                await register_single_username(client)
            else:
                await register_mass_usernames(client)
        else:
            print("[-] Invalid option, please choose again.")


if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user, exiting...")
