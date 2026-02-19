"""
SoClose.co - X/Twitter Bulk DM Sender
Messaging logic: send DMs, handle errors, track results.
"""

import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
)
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel

from config import (
    TIMEOUT,
    DELAY_MIN,
    DELAY_MAX,
    MAX_RETRIES,
    SELECTOR_DM_BUTTON,
    SELECTOR_DM_INPUT,
    SELECTOR_DM_SEND,
    COLOR_FOCUS,
    COLOR_SUCCESS,
    COLOR_ERROR,
    COLOR_WARNING,
    COLOR_ACCENT,
)
from browser import navigate_to_profile


def send_dm(driver, profile_path, message):
    """
    Send a DM to a single profile.
    Returns a dict: {profile, status, reason, timestamp}
    """
    username = profile_path.lstrip("/")
    result = {
        "profile": f"@{username}",
        "status": "failed",
        "reason": "",
        "timestamp": datetime.now().isoformat(),
    }

    # Navigate to the profile
    if not navigate_to_profile(driver, profile_path):
        result["reason"] = "Profile not found or failed to load"
        return result

    try:
        # Click the DM button on the profile
        dm_button = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTOR_DM_BUTTON))
        )
        dm_button.click()
    except TimeoutException:
        result["reason"] = "DM button not found (DMs may be disabled)"
        result["status"] = "skipped"
        return result
    except ElementClickInterceptedException:
        result["reason"] = "DM button blocked by overlay"
        return result

    try:
        # Wait for and click the message input box
        msg_input = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTOR_DM_INPUT))
        )
        msg_input.click()
        time.sleep(0.5)
        msg_input.send_keys(message)
    except TimeoutException:
        result["reason"] = "Message input box not found"
        return result

    try:
        # Click the send button
        send_button = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTOR_DM_SEND))
        )
        send_button.click()
        time.sleep(1)

        result["status"] = "success"
        result["reason"] = "Message sent"
    except TimeoutException:
        result["reason"] = "Send button not found"
    except ElementClickInterceptedException:
        result["reason"] = "Send button blocked"

    return result


def process_all_profiles(driver, profiles_df, message, console: Console):
    """
    Process all profiles: send DMs with progress tracking.
    Returns a list of result dicts.
    """
    results = []
    total = len(profiles_df)

    console.print()
    with Progress(
        SpinnerColumn(style=COLOR_FOCUS),
        TextColumn(f"[bold {COLOR_FOCUS}]Sending DMs"),
        BarColumn(complete_style=COLOR_FOCUS, finished_style=COLOR_SUCCESS),
        TaskProgressColumn(),
        TextColumn("[dim]{task.fields[status]}[/]"),
        console=console,
    ) as progress:
        task = progress.add_task("Sending", total=total, status="Starting...")

        for index, row in profiles_df.iterrows():
            profile_path = row["tweeter_profile_link"]
            username = profile_path.lstrip("/")
            progress.update(task, status=f"@{username}")

            # Retry logic
            result = None
            for attempt in range(1, MAX_RETRIES + 1):
                result = send_dm(driver, profile_path, message)
                if result["status"] != "failed" or attempt == MAX_RETRIES:
                    break
                console.print(
                    f"  [{COLOR_WARNING}]Retry {attempt}/{MAX_RETRIES} for @{username}[/]"
                )
                time.sleep(2)

            results.append(result)
            progress.advance(task)

            # Status indicator
            if result["status"] == "success":
                console.print(
                    f"  [{COLOR_SUCCESS}]Sent[/] -> @{username}"
                )
            elif result["status"] == "skipped":
                console.print(
                    f"  [{COLOR_WARNING}]Skipped[/] -> @{username} ({result['reason']})"
                )
            else:
                console.print(
                    f"  [{COLOR_ERROR}]Failed[/] -> @{username} ({result['reason']})"
                )

            # Random delay between messages to avoid rate limiting
            if index < total - 1:
                delay = random.uniform(DELAY_MIN, DELAY_MAX)
                progress.update(task, status=f"Waiting {delay:.0f}s...")
                time.sleep(delay)

    return results


def display_summary(results, console: Console):
    """Display a branded summary table of all results."""
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    total = len(results)

    # Summary stats
    console.print()
    stats_table = Table(
        title=f"[bold {COLOR_FOCUS}]Session Summary",
        border_style=COLOR_ACCENT,
        show_header=True,
        header_style=f"bold {COLOR_FOCUS}",
    )
    stats_table.add_column("Metric", style="bold")
    stats_table.add_column("Count", justify="center")
    stats_table.add_row("Total Profiles", str(total))
    stats_table.add_row(f"[{COLOR_SUCCESS}]Sent", f"[{COLOR_SUCCESS}]{success}")
    stats_table.add_row(f"[{COLOR_ERROR}]Failed", f"[{COLOR_ERROR}]{failed}")
    stats_table.add_row(f"[{COLOR_WARNING}]Skipped", f"[{COLOR_WARNING}]{skipped}")
    console.print(stats_table)

    # Detailed results
    if failed > 0 or skipped > 0:
        console.print()
        detail_table = Table(
            title=f"[bold {COLOR_FOCUS}]Details (Failed & Skipped)",
            border_style=COLOR_ACCENT,
            show_header=True,
            header_style=f"bold {COLOR_FOCUS}",
        )
        detail_table.add_column("Profile", style="bold")
        detail_table.add_column("Status")
        detail_table.add_column("Reason")

        for r in results:
            if r["status"] != "success":
                status_color = COLOR_ERROR if r["status"] == "failed" else COLOR_WARNING
                detail_table.add_row(
                    r["profile"],
                    f"[{status_color}]{r['status']}[/]",
                    r["reason"],
                )
        console.print(detail_table)
