import os
import sys
import time
import random
import logging
import threading
import signal
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

# Constants
BLOCK_ID = 3852
DATA_FILE = "data.txt"
MAX_WORKERS = 5
RETRY_LIMIT = 5
WAIT_TIME_RANGE = (150, 180)

# ANSI escape codes for color formatting
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Logging Setup
logger = logging.getLogger("AdWatcher")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log', encoding='utf-8')

formatter = logging.Formatter('%(asctime)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Thread-safe stop signal
stop_event = threading.Event()

# Initialize a retryable requests session
session = requests.Session()
retries = Retry(total=RETRY_LIMIT, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))


def display_banner(filename, account_count):
    """
    Display the ASCII banner with details.
    """
    banner = f"""
{CYAN}
 ██████╗██╗██████╗  ██████╗██╗     ███████╗    ██████╗  ██████╗ ████████╗
██╔════╝██║██╔══██╗██╔════╝██║     ██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██║     ██║██████╔╝██║     ██║     █████╗      ██████╔╝██║   ██║   ██║   
██║     ██║██╔══██╗██║     ██║     ██╔══╝      ██╔══██╗██║   ██║   ██║   
╚██████╗██║██║  ██║╚██████╗███████╗███████╗    ██████╔╝╚██████╔╝   ██║   
 ╚═════╝╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝  

{RESET}📁 File: {YELLOW}{filename}{RESET}
📊 Accounts Loaded: {GREEN}{account_count}{RESET}

{YELLOW}👋 Hey there! I’m your friendly ad-watching assistant. Let’s get started! 🚀{RESET}
🔔 Keep me updated with 'git pull' to unlock the latest features!

🎉 Created by GitHub user @airdropcodex. Support his first project with a ⭐ or donation, details at the bottom of the instrunctions 💖!

============================================================================================
    """
    print(banner)


def build_headers(authorization):
    """
    Build headers for making HTTP requests.
    """
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': authorization,
        'cache-control': 'max-age=0',
        'content-type': 'application/json',
        'origin': 'https://bot.toncircle.org',
        'pragma': 'no-cache',
        'referer': 'https://bot.toncircle.org/',
        'x-requested-with': 'org.telegram.messenger',
    }


def build_ad_url(account):
    """
    Construct the ad URL for a given account.
    """
    return f"https://api.adsgram.ai/adv?blockId={BLOCK_ID}&tg_id={account['tg_id']}&tg_platform={account['tg_platform']}&platform=Win32&language={account['language']}&chat_type={account['chat_type']}&chat_instance={account['chat_instance']}&top_domain={account['top_domain']}"



def read_multiple_accounts(filename="data.txt"):
    """
    Reads and parses account details from the specified file.
    Filters accounts to include only those with valid entries for required keys.

    Args:
        filename (str): Path to the file containing account details.

    Returns:
        list: A list of valid accounts with non-placeholder values.
    """
    accounts = []
    required_keys = ["tg_id", "tg_platform", "language", "chat_type", "chat_instance", "top_domain"]

    try:
        with open(filename, "r") as file:
            account_data = {}
            for line in file:
                line = line.strip()
                if not line:
                    # End of an account entry
                    if account_data:
                        # Check if all required keys are present
                        if all(key in account_data for key in required_keys) and "YOUR_" not in str(account_data):
                            accounts.append(account_data)
                        account_data = {}
                elif "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    # Normalize keys by removing numeric suffixes
                    base_key = key
                    if base_key[-1].isdigit():
                        base_key = ''.join([ch for ch in base_key if not ch.isdigit()])

                    # Add the normalized key-value pair to the account data
                    account_data[base_key] = value

            # Add the last account if it's valid
            if account_data:
                if all(key in account_data for key in required_keys) and "YOUR_" not in str(account_data):
                    accounts.append(account_data)

        # Display banner with valid account count
        file_name_only = os.path.basename(filename)
        display_banner(file_name_only, len(accounts))
        return accounts

    except FileNotFoundError:
        logger.error(f"{RED}File {filename} not found.{RESET}")
        file_name_only = os.path.basename(filename)
        display_banner(file_name_only, 0)  # Show banner even if the file is missing
        return []
    except Exception as e:
        logger.error(f"{RED}Error reading accounts from file: {e}{RESET}")
        file_name_only = os.path.basename(filename)
        display_banner(file_name_only, 0)  # Show banner even if there's an error
        return []


def claim_ad(account):
    """
    Claims ad rewards for the given account.
    """
    headers = build_headers(account.get("authorization", ""))
    ad_url = build_ad_url(account)

    try:
        response = session.get(ad_url, headers=headers)

        if response.status_code == 200:
            ad_data = response.json()
            tracking_urls = [t.get("value") for t in ad_data.get("banner", {}).get("trackings", [])]

            if not tracking_urls:
                logger.warning(f"No claim URLs found for account {account['tg_id']}. Retrying... Hold on!")
                return False

            for tracking_url in tracking_urls:
                tracking_response = session.get(tracking_url)
                if tracking_response.status_code != 200:
                    logger.error(f"Tracking failed for URL: {tracking_url}. Trying another one.")
                    return False

            return True
        else:
            logger.error(f"Failed to claim ad for {account['tg_id']} (Error: {response.text}).")
            return False

    except Exception as e:
        logger.error(f"{RED}Error while claiming ads for {account['tg_id']}: {e}.{RESET}")
        return False


def watch_ads_for_account(account):
    """
    Watches ads for a single account.
    """
    while not stop_event.is_set():
        if claim_ad(account):
            logger.info(f"{GREEN}✨ Success! Rewards claimed for {account['tg_id']}! +1000 Sparks added! 🎉{RESET}")
            break
        time.sleep(5)


def wait_between_ads(wait_time):
    """
    Waits between ad-watching rounds.
    """
    logger.info(f"⏳ Let’s pause for {wait_time} seconds before the next round! Or your account will be banned")
    for remaining in range(wait_time, 0, -1):
        if stop_event.is_set():
            break
        minutes, seconds = divmod(remaining, 60)
        sys.stdout.write(f"\r⏳ Time left: {minutes:02}:{seconds:02}  ")
        sys.stdout.flush()
        time.sleep(1)
    print()


def watch_ads():
    """
    Main function to manage ad-watching for all accounts.
    """
    accounts = read_multiple_accounts(DATA_FILE)
    if not accounts:
        return

    while not stop_event.is_set():
        logger.info("🌟 Starting a new round of ad-watching. Sit back and relax!")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for account in accounts:
                executor.submit(watch_ads_for_account, account)

        if not stop_event.is_set():
            wait_between_ads(random.randint(*WAIT_TIME_RANGE))


def shutdown_handler(signum, frame):
    """
    Gracefully shuts down the program on termination signals.
    """
    print()
    logger.info(f"{RED}Wrapping things up..See you next time !{RESET}")
    stop_event.set()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    os.system('cls' if os.name == 'nt' else 'clear')

    watch_ads()
