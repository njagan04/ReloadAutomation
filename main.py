import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --------- CONFIGURE ---------
target_url = "https://github.com/njagan04"  
reload_count = 50           
delay_min_seconds = 2.0     
delay_max_seconds = 5.0      
headless = False             
implicit_wait_seconds = 5    
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def make_driver(headless_mode: bool) -> webdriver.Chrome:
    chrome_opts = Options()
    if headless_mode:
        chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--disable-gpu")

    chrome_opts.add_argument("--log-level=3")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_opts)
    driver.implicitly_wait(implicit_wait_seconds)
    return driver

def main():
    logging.info("Starting reload automation (for testing/learning only).")
    logging.info(f"Target URL: {target_url}")
    logging.info(f"Reloads: {reload_count}, delay range: [{delay_min_seconds}, {delay_max_seconds}]s, headless={headless}")

    driver = None
    try:
        driver = make_driver(headless)
        driver.get(target_url)
        logging.info("Initial page load complete.")

        for i in range(1, reload_count + 1):
            delay = random.uniform(delay_min_seconds, delay_max_seconds)
            logging.info(f"Reload #{i}: waiting {delay:.2f}s before reload.")
            time.sleep(delay)

            try:
                driver.refresh()
                logging.info(f"Reload #{i}: page refreshed successfully.")
            except Exception as e:
                logging.error(f"Reload #{i}: error during refresh: {e}")


        logging.info("Completed all reloads.")
    except Exception as main_e:
        logging.exception("Fatal error in automation: %s", main_e)
    finally:
        if driver:
            driver.quit()
        logging.info("Driver closed. Exiting.")

if __name__ == "__main__":
    main()
