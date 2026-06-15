# CLAUDE.md -- TwitterBulkMpSender

## 1. Project Identity

**Name:** TwitterBulkMpSender -- Twitter/X Bulk DM Sender
**Role:** Professional bulk Twitter/X direct message automation with retry logic, progress tracking, and detailed CSV reports.
**Author:** SoClose Society (https://soclose.co)
**License:** MIT | **Version:** 2.0.0

### Stack

- **Language:** Python 3.9+
- **Browser:** Selenium 4.15+ with webdriver-manager
- **Data:** pandas
- **UI:** Rich (CLI tables, progress bars)
- **Config:** python-dotenv + config.py
- **Architecture:** Modular (5 files, ~598 LOC)

### Project Structure

```
main.py (176 LOC)       CLI orchestration
config.py (61 LOC)      Constants, selectors, branding
browser.py (66 LOC)     WebDriver setup
messenger.py (207 LOC)  DM sending with retry logic
utils.py (88 LOC)       CSV validation, reporting
```

### Critical Files

- `messenger.py` -- DM logic with data-testid selectors
- `config.py` -- Twitter DOM selectors and timing constants

## 2-5. Standard Workflow

- Enter plan mode for non-trivial tasks
- Test with a single profile first
- Verify CSV report is generated after run
- Track tasks in `tasks/todo.md`, lessons in `tasks/lessons.md`

## 6. Project-Specific Rules

### Dev Commands
```bash
pip install -r requirements.txt
cp .env.example .env
echo "Your message" > message.txt
# Add profiles to profiles.csv
python main.py
```

### Environment Variables
- DELAY_MIN=3, DELAY_MAX=7
- TIMEOUT=15, MAX_RETRIES=3
- MESSAGE_FILE=message.txt

### Config (config.py)
- Twitter data-testid selectors for DM UI elements
- Brand colors: PRIMARY=#1b1b1b, ACCENT=#c5c1b9, FOCUS=#575ECF

### Known Fragile Areas
- Twitter data-testid selectors -- can change with UI updates
- Manual login required (no automated auth)
- Rate limiting -- Twitter throttles bulk DMs aggressively

## Neo Connector (auto)
Ce projet expose `NEO_CONNECTOR.md` : le manifeste machine-lisible de TOUS ses
endpoints/auth/env, consommé par NeoBot pour se câbler automatiquement.
- RÈGLE : à chaque ajout/suppression/modif d'un endpoint, d'une auth ou d'une env var,
  régénère le manifeste via `/neo-connector` (ou le prompt dans .claude/skills/neo-connector).
- Ne jamais éditer NEO_CONNECTOR.md à la main : il est généré.
- Le hook pre-commit (.git/hooks/pre-commit) avertit si des routes ont changé sans MAJ du manifeste.
- NOTE (ce repo) : pas d'API HTTP -- CLI Selenium interactif. À NE PAS câbler comme tool HTTP Neo.

## 7. Core Principles

- Simplicity First, No Laziness, Minimal Impact
- Never use em dashes (use -- instead)
- Never reduce delay below 3 seconds
