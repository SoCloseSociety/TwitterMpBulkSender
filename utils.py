"""
SoClose.co - X/Twitter Bulk DM Sender
Utility functions: connectivity, CSV validation, reporting.
"""

import os
import socket
from datetime import datetime

import pandas as pd
from rich.console import Console

from config import REPORTS_DIR


def check_internet(host="one.one.one.one", port=80, timeout=3):
    """Check internet connectivity by reaching Cloudflare DNS."""
    try:
        addr = socket.gethostbyname(host)
        conn = socket.create_connection((addr, port), timeout)
        conn.close()
        return True
    except OSError:
        return False


def validate_csv(filepath):
    """
    Validate and load a CSV file of Twitter/X profiles.
    Returns a cleaned DataFrame or raises ValueError with details.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)

    if "tweeter_profile_link" not in df.columns:
        raise ValueError(
            "CSV must contain a 'tweeter_profile_link' column. "
            f"Found columns: {list(df.columns)}"
        )

    # Drop rows with missing profile links
    df = df.dropna(subset=["tweeter_profile_link"])

    # Clean profile links: ensure they start with /
    df["tweeter_profile_link"] = df["tweeter_profile_link"].str.strip()
    df = df[df["tweeter_profile_link"].str.startswith("/")]

    # Deduplicate
    before = len(df)
    df = df.drop_duplicates(subset=["tweeter_profile_link"])
    dupes = before - len(df)

    if len(df) == 0:
        raise ValueError("No valid profiles found in CSV after cleaning.")

    return df, dupes


def load_message(filepath):
    """Load and validate the message file."""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Message file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError("Message file is empty.")

    return content


def generate_report(results, console: Console):
    """
    Generate a CSV report from send results.
    results: list of dicts with keys: profile, status, reason, timestamp
    Returns the report file path.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORTS_DIR, f"dm_report_{timestamp}.csv")

    df = pd.DataFrame(results)
    df.to_csv(report_path, index=False)

    return report_path
