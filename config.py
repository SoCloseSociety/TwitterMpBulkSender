"""
SoClose.co - X/Twitter Bulk DM Sender
Configuration and branding constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────────────────────
# Brand
# ──────────────────────────────────────────────────────────────
APP_NAME = "SoClose DM Sender"
APP_VERSION = "2.0.0"
BRAND_URL = "https://soclose.co"
BRAND_TAGLINE = "Digital Innovation Through Automation & AI"

# Rich color theme (SoClose brand palette)
COLOR_PRIMARY = "#1b1b1b"
COLOR_ACCENT = "#c5c1b9"
COLOR_FOCUS = "#575ECF"
COLOR_SUCCESS = "#2ecc71"
COLOR_ERROR = "#e74c3c"
COLOR_WARNING = "#f39c12"

BANNER = f"""[bold {COLOR_FOCUS}]
  ███████╗  ██████╗   ██████╗ ██╗      ██████╗  ███████╗ ███████╗
  ██╔════╝ ██╔═══██╗ ██╔════╝ ██║     ██╔═══██╗ ██╔════╝ ██╔════╝
  ███████╗ ██║   ██║ ██║      ██║     ██║   ██║ ███████╗ █████╗
  ╚════██║ ██║   ██║ ██║      ██║     ██║   ██║ ╚════██║ ██╔══╝
  ███████║ ╚██████╔╝ ╚██████╗ ███████╗╚██████╔╝ ███████║ ███████╗
  ╚══════╝  ╚═════╝   ╚═════╝ ╚══════╝ ╚═════╝  ╚══════╝ ╚══════╝
[/]
[{COLOR_ACCENT}]  {BRAND_TAGLINE}[/]
[dim]  v{APP_VERSION} | {BRAND_URL}[/]
"""

# ──────────────────────────────────────────────────────────────
# Selenium / Automation
# ──────────────────────────────────────────────────────────────
DELAY_MIN = int(os.getenv("DELAY_MIN", "3"))
DELAY_MAX = int(os.getenv("DELAY_MAX", "7"))
TIMEOUT = int(os.getenv("TIMEOUT", "15"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# X/Twitter
X_BASE_URL = "https://x.com"
X_LOGIN_URL = "https://x.com/i/flow/login"

# Data-testid selectors (X/Twitter DOM)
SELECTOR_USERNAME = '[data-testid="UserName"]'
SELECTOR_DM_BUTTON = '[data-testid="sendDMFromProfile"]'
SELECTOR_DM_INPUT = '[data-testid="dmComposerTextInput"]'
SELECTOR_DM_SEND = '[data-testid="dmComposerSendButton"]'

# ──────────────────────────────────────────────────────────────
# Files
# ──────────────────────────────────────────────────────────────
MESSAGE_FILE = os.getenv("MESSAGE_FILE", "message.txt")
REPORTS_DIR = "reports"
