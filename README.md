<p align="center">
  <strong>SOCLOSE.CO</strong><br>
  <em>Digital Innovation Through Automation & AI</em>
</p>

<h1 align="center">X/Twitter Bulk DM Sender</h1>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-575ECF?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-c5c1b9?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/selenium-4.x-575ECF?style=flat-square" alt="Selenium">
  <img src="https://img.shields.io/badge/by-SoClose.co-1b1b1b?style=flat-square" alt="SoClose">
</p>

<p align="center">
  A professional-grade automation tool for sending bulk direct messages on X (formerly Twitter).<br>
  Built with Selenium, Rich CLI, and robust error handling.
</p>

---

## Features

- **Branded CLI Interface** - Professional terminal UI with progress bars, status tables, and SoClose branding
- **Smart Browser Automation** - Selenium WebDriver with anti-detection, configurable timeouts, and proper waits
- **CSV Profile Management** - Validated input with deduplication and preview
- **Retry Logic** - Configurable retry attempts per profile with intelligent failure handling
- **Rate Limiting** - Random delays between messages to avoid detection
- **Detailed Reporting** - Automatic CSV report generation (success/failed/skipped)
- **Configurable** - Environment variables for delays, timeouts, and retries

## Prerequisites

- **Python 3.8+**
- **Google Chrome** browser installed
- A valid X/Twitter account

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/TwitterBulkMpSender.git
cd TwitterBulkMpSender

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure (optional)
cp .env.example .env
# Edit .env to customize delays, timeouts, etc.
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DELAY_MIN` | `3` | Minimum delay between messages (seconds) |
| `DELAY_MAX` | `7` | Maximum delay between messages (seconds) |
| `TIMEOUT` | `15` | Selenium element wait timeout (seconds) |
| `MAX_RETRIES` | `3` | Max retry attempts per profile |
| `MESSAGE_FILE` | `message.txt` | Path to the message file |

## Usage

### 1. Prepare your data

**CSV file** with a `tweeter_profile_link` column:

```csv
,tweeter_profile_link,tweeter_profile_name
0,/username1,@username1
1,/username2,@username2
```

**Message file** (`message.txt`):

```
Your message content here.
```

### 2. Run the tool

```bash
python main.py
```

### 3. Follow the CLI prompts

1. Enter your CSV file path (or press Enter for `Test.csv`)
2. Review the profile summary and message preview
3. Log into X/Twitter in the browser window that opens
4. Press Enter to start the DM session
5. Monitor progress in real-time via the progress bar
6. Review the summary report at the end

## Reports

After each session, a detailed CSV report is saved to the `reports/` directory:

```
reports/dm_report_20260219_143022.csv
```

Each report contains: profile, status (success/failed/skipped), reason, and timestamp.

## Project Structure

```
TwitterBulkMpSender/
├── main.py           # CLI entry point
├── config.py         # Configuration & branding
├── browser.py        # Chrome WebDriver management
├── messenger.py      # DM sending logic
├── utils.py          # Utilities (validation, reporting)
├── requirements.txt  # Python dependencies
├── .env.example      # Environment config template
├── .gitignore        # Git ignore rules
├── message.txt       # Message content
├── Test.csv          # Sample profile data
└── reports/          # Generated session reports
```

## Disclaimer

This tool is intended for legitimate outreach and business communication purposes only. Users are responsible for complying with X/Twitter's Terms of Service. Do not use this tool for spam or unsolicited messaging. The authors are not responsible for any misuse or account restrictions resulting from use of this tool.

---

<p align="center">
  <strong>Built by <a href="https://soclose.co">SoClose.co</a></strong><br>
  <em>Digital Innovation Through Automation & AI</em><br>
  <a href="mailto:hello@soclose.co">hello@soclose.co</a>
</p>
