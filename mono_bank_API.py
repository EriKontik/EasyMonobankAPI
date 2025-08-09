import requests
import json
import os
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional

load_dotenv()

API_KEY = os.environ["API_KEY"]

def get_currency():
    res = requests.get("https://api.monobank.ua/bank/currency")
    return res.content

def get_client_info(key: str) -> dict:
    res = requests.get("https://api.monobank.ua/personal/client-info", headers={"X-Token": key})
    return res.json()

import requests
from datetime import datetime, timedelta, timezone
import time

def get_statement(account_id="0", from_date=None, to_date=None):
    """
    Fetch account statement from API with human-friendly date input.
    Defaults to last month if no dates are provided.

    Args:
        account_id (str): Account ID or '0' for default account.
        from_date (str): Start date in 'YYYY-MM-DD HH:MM:SS' format (local time).
        to_date (str, optional): End date in same format. Defaults to current time.

    Returns:
        dict: JSON response from API.
    """
    # If no dates given → default to last 31 days
    if not from_date and not to_date:
        to_dt = datetime.now(timezone.utc)
        from_dt = to_dt - timedelta(days=31)
    else:
        # Parse from_date
        if from_date:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        else:
            # If only to_date given → from_date = to_date - 31 days
            to_dt = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            from_dt = to_dt - timedelta(days=31)

        # Parse to_date
        if to_date:
            to_dt = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        else:
            to_dt = datetime.now(timezone.utc)

    # Convert to Unix timestamps
    from_ts = int(from_dt.timestamp())
    to_ts = int(to_dt.timestamp())

    # Validate range
    if to_ts - from_ts > 2_682_000:
        raise ValueError("Time range exceeds maximum of 31 days + 1 hour")
    #https://api.monobank.ua/personal/statement/{account}/{from}/{to}
    url = f"https://api.monobank.ua/personal/statement/{account_id}/{from_ts}/{to_ts}"
    headers = {"X-Token": API_KEY}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def print_transactions(transactions):
    for tx in transactions:
        # Convert Unix timestamp to human-readable date
        date_str = datetime.fromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M:%S')

        # Format amount with currency
        amount_str = f"{tx['amount'] / 100:.2f} UAH"
        balance_str = f"{tx['balance'] / 100:.2f} UAH"

        # Print nicely
        print("─" * 50)
        print(f"Date:         {date_str}")
        print(f"Description:  {tx.get('description', '-')}")
        if 'comment' in tx:
            print(f"Comment:      {tx['comment']}")
        print(f"MCC:          {tx['mcc']} (Original: {tx['originalMcc']})")
        print(f"Amount:       {amount_str}")
        print(f"Cashback:     {tx['cashbackAmount'] / 100:.2f} UAH")
        print(f"Balance:      {balance_str}")
        print(f"Hold:         {tx['hold']}")
        if 'receiptId' in tx:
            print(f"Receipt ID:   {tx['receiptId']}")
        if 'counterName' in tx:
            print(f"Counterparty: {tx['counterName']}")
    print("─" * 50)

# Example usage
if __name__ == "__main__":
    # Default: past month
    data = get_statement(account_id="0")
    print(data)


def show_data(data: dict) -> None:
    """
    Pretty prints MonoBank client info in an easy-to-read format.
    """
    print(f"Client ID: {data.get('clientId', '-')}")
    print(f"Name: {data.get('name', '-')}")
    print(f"WebHook URL: {data.get('webHookUrl', '-')}")
    print(f"Permissions: {data.get('permissions', '-')}\n")

    accounts = data.get('accounts', [])
    if accounts:
        print("Accounts:")
        for acc in accounts:
            print(f"  - ID: {acc.get('id', '-')}")
            print(f"    Currency: {acc.get('currencyCode', '-')}")
            print(f"    Balance: {acc.get('balance', '-') / 100}")
            print(f"    Credit Limit: {acc.get('creditLimit', '-')}")
            print(f"    Type: {acc.get('type', '-')}")
            print(f"    IBAN: {acc.get('iban', '-')}")
            print(f"    Masked PAN: {', '.join(acc.get('maskedPan', []))}")
            print(f"    Cashback Type: {acc.get('cashbackType', '-')}\n")
    else:
        print("Accounts: None\n")

    jars = data.get('jars', [])
    if jars:
        print("Jars:")
        for jar in jars:
            print(f"  - ID: {jar.get('id', '-')}")
            print(f"    Title: {jar.get('title', '-')}")
            print(f"    Description: {jar.get('description', '-')}")
            print(f"    Currency: {jar.get('currencyCode', '-')}")
            print(f"    Balance: {jar.get('balance', '-')/100}")
            print(f"    Goal: {jar.get('goal', '-')/100}\n")
    else:
        print("Jars: None\n")

if __name__ == "__main__":
    # print(get_client_info(API_KEY))
    print(show_data(get_client_info(API_KEY)))
    data = get_statement(account_id="0")
    print(print_transactions(data))
