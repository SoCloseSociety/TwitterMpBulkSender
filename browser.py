"""
SoClose.co - X/Twitter Bulk DM Sender
Browser management: Chrome setup, login flow, navigation.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from config import X_LOGIN_URL, X_BASE_URL, TIMEOUT, SELECTOR_USERNAME


def setup_driver():
    """Configure and return a Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    driver.maximize_window()

    # Remove webdriver flag to reduce detection
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


def open_login_page(driver):
    """Navigate to X/Twitter login page."""
    driver.get(X_LOGIN_URL)


def navigate_to_profile(driver, profile_path):
    """
    Navigate to a user profile and wait for it to load.
    Returns True if profile loaded successfully, False otherwise.
    """
    full_url = f"{X_BASE_URL}{profile_path}"
    driver.get(full_url)

    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SELECTOR_USERNAME))
        )
        return True
    except TimeoutException:
        return False


def close_driver(driver):
    """Safely close the browser."""
    try:
        driver.quit()
    except Exception:
        pass
