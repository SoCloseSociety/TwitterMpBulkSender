"""
SoClose.co - X/Twitter Bulk DM Sender
Main entry point with branded CLI interface.
"""

import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from config import (
    BANNER,
    BRAND_URL,
    MESSAGE_FILE,
    COLOR_FOCUS,
    COLOR_ACCENT,
    COLOR_SUCCESS,
    COLOR_ERROR,
    COLOR_WARNING,
    DELAY_MIN,
    DELAY_MAX,
    TIMEOUT,
    MAX_RETRIES,
)
from utils import check_internet, validate_csv, load_message, generate_report
from browser import setup_driver, open_login_page, close_driver
from messenger import process_all_profiles, display_summary

console = Console()


def print_config():
    """Display current configuration."""
    console.print(
        Panel(
            f"[bold]Delay:[/] {DELAY_MIN}-{DELAY_MAX}s  |  "
            f"[bold]Timeout:[/] {TIMEOUT}s  |  "
            f"[bold]Retries:[/] {MAX_RETRIES}",
            title=f"[{COLOR_FOCUS}]Configuration[/]",
            border_style=COLOR_ACCENT,
        )
    )


def main():
    # ── Banner ──────────────────────────────────────────────
    console.print(BANNER)
    console.print()

    # ── Internet check ──────────────────────────────────────
    console.print(f"[{COLOR_FOCUS}]Checking internet connection...[/]", end=" ")
    if not check_internet():
        console.print(f"[{COLOR_ERROR}]No internet connection. Exiting.[/]")
        sys.exit(1)
    console.print(f"[{COLOR_SUCCESS}]Connected[/]")
    console.print()

    # ── Configuration ───────────────────────────────────────
    print_config()
    console.print()

    # ── CSV input ───────────────────────────────────────────
    csv_path = Prompt.ask(
        f"[bold {COLOR_FOCUS}]Enter CSV file path[/]",
        default="Test.csv",
    )

    try:
        df, dupes = validate_csv(csv_path)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[{COLOR_ERROR}]CSV Error: {e}[/]")
        sys.exit(1)

    console.print(
        Panel(
            f"[bold]Profiles loaded:[/] {len(df)}"
            + (f"  |  [dim]Duplicates removed: {dupes}[/]" if dupes else ""),
            title=f"[{COLOR_FOCUS}]CSV Summary[/]",
            border_style=COLOR_ACCENT,
        )
    )

    # Preview first 5 profiles
    preview = df.head(5)
    profiles_preview = ", ".join(
        f"@{p.lstrip('/')}" for p in preview["tweeter_profile_link"]
    )
    console.print(f"  [dim]Preview: {profiles_preview}...[/]")
    console.print()

    # ── Message ─────────────────────────────────────────────
    try:
        message = load_message(MESSAGE_FILE)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[{COLOR_ERROR}]Message Error: {e}[/]")
        sys.exit(1)

    console.print(
        Panel(
            message,
            title=f"[{COLOR_FOCUS}]Message to send[/]",
            border_style=COLOR_ACCENT,
        )
    )
    console.print()

    # ── Browser launch ──────────────────────────────────────
    console.print(f"[{COLOR_FOCUS}]Launching browser...[/]")
    driver = setup_driver()
    open_login_page(driver)

    console.print(
        Panel(
            "[bold]1.[/] Log into your X/Twitter account in the browser window\n"
            "[bold]2.[/] Make sure you are on the home page\n"
            f"[bold]3.[/] Come back here and press [{COLOR_SUCCESS}]Enter[/] to start sending",
            title=f"[{COLOR_FOCUS}]Login Required[/]",
            border_style=COLOR_FOCUS,
        )
    )

    Prompt.ask(f"\n[bold {COLOR_SUCCESS}]Press Enter when logged in[/]")
    console.print()

    # ── Send DMs ────────────────────────────────────────────
    console.print(
        Panel(
            f"Sending to [bold]{len(df)}[/] profiles with "
            f"[bold]{DELAY_MIN}-{DELAY_MAX}s[/] delay between messages.",
            title=f"[{COLOR_FOCUS}]Starting DM Session[/]",
            border_style=COLOR_FOCUS,
        )
    )

    try:
        results = process_all_profiles(driver, df, message, console)
    except KeyboardInterrupt:
        console.print(f"\n[{COLOR_WARNING}]Session interrupted by user.[/]")
        results = []
    finally:
        close_driver(driver)

    if not results:
        console.print(f"[{COLOR_WARNING}]No messages were sent.[/]")
        sys.exit(0)

    # ── Summary ─────────────────────────────────────────────
    display_summary(results, console)

    # ── Report ──────────────────────────────────────────────
    report_path = generate_report(results, console)
    console.print(
        f"\n[{COLOR_SUCCESS}]Report saved:[/] {report_path}"
    )

    # ── Footer ──────────────────────────────────────────────
    console.print()
    console.print(
        Panel(
            f"[{COLOR_ACCENT}]Powered by[/] [{COLOR_FOCUS}]SoClose.co[/] "
            f"[dim]| {BRAND_URL}[/]",
            border_style=COLOR_ACCENT,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n[{COLOR_WARNING}]Interrupted. Goodbye.[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[{COLOR_ERROR}]Fatal error: {e}[/]")
        sys.exit(1)
