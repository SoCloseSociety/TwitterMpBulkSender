# NEO_CONNECTOR -- TwitterBulkMpSender
- service: twitterbulkmp
- base_url_prod: N/A (no HTTP service -- local interactive CLI)
- auth: none (no API; X/Twitter session via manual browser login at runtime)
- env_required: [DELAY_MIN, DELAY_MAX, TIMEOUT, MAX_RETRIES, MESSAGE_FILE]
- generated_at:

## Endpoints
NONE. This repo exposes **no** HTTP API, webhook, SSE, WebSocket, cron, or queue.
Proven by reading every source file:
- `main.py` -- interactive Rich CLI entry point (`Prompt.ask`, `console.print`). Requires
  a human to log into X/Twitter in a launched Chrome window and press Enter to start.
- `browser.py` -- Selenium Chrome WebDriver (`webdriver.Chrome`), navigates to
  `https://x.com` profiles. No server bound, no port opened.
- `messenger.py` -- DM-sending loop driving the X/Twitter DOM via `data-testid` CSS
  selectors. Pure browser automation.
- `utils.py` -- local CSV validation + report writing; `check_internet()` only opens an
  outbound TCP socket to `one.one.one.one:80` (connectivity probe, not a server).
- `config.py` -- constants only (delays, selectors, brand). The only URLs are X/Twitter
  targets (`X_BASE_URL=https://x.com`, `X_LOGIN_URL=https://x.com/i/flow/login`), which
  are destinations the tool drives, not endpoints it serves.

There is no Flask/FastAPI/Express/aiohttp/Next.js import anywhere; `requirements.txt` is
`selenium`, `webdriver-manager`, `pandas`, `rich`, `python-dotenv` only.

## Flows
Local, human-in-the-loop CLI run (NOT machine-callable):
1. `python main.py`
2. Internet check (`utils.check_internet`).
3. Prompt for CSV path (default `Test.csv`); validate via `utils.validate_csv`
   (requires a `tweeter_profile_link` column; links must start with `/`; dedupes).
4. Load message body from `MESSAGE_FILE` (default `message.txt`) via `utils.load_message`.
5. Launch Chrome (`browser.setup_driver`), open X login (`browser.open_login_page`),
   then **block on `Prompt.ask`** until the operator has logged in manually.
6. `messenger.process_all_profiles` -> for each profile: navigate, click DM button,
   type message, click send; retry up to `MAX_RETRIES`; random `DELAY_MIN..DELAY_MAX`
   pause between profiles.
7. `messenger.display_summary` + `utils.generate_report` -> writes
   `reports/dm_report_<timestamp>.csv`.

## Env vars (call/config only -- names, never values)
- DELAY_MIN (default 3) -- min seconds between DMs.
- DELAY_MAX (default 7) -- max seconds between DMs.
- TIMEOUT (default 15) -- Selenium element wait, seconds.
- MAX_RETRIES (default 3) -- send attempts per profile.
- MESSAGE_FILE (default message.txt) -- path to the DM body.
(No API keys or secrets: the X/Twitter session is established by manual login, not stored.)

## Gaps
None ambiguous. Definitive conclusion: this is a pure local, interactive CLI +
browser-automation bot. It has nothing for Neo to call over HTTP.

## Recap
- Endpoints found: 0 (HTTP / webhook / SSE / WS / cron / queue).
- Already covered vs new: N/A.
- **Wiring verdict: do NOT wire as Neo HTTP tools.** There is no service to reach. It
  cannot run unattended (manual X login is required) and exposes no programmatic surface.
  If integration is ever wanted, it would have to be a host-shell/subprocess invocation of
  `python main.py` on a machine with a human-driven browser, not an HTTP integration.
