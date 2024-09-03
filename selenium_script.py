import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL to be opened
url = "https://www.nseindia.com/companies-listing/corporate-filings-actions"

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Set to False if you want to see the browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set custom headers
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
chrome_options.add_argument("accept-language=en-US,en;q=0.9")

# Initialize the WebDriver with the options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the URL and wait until the page is fully loaded
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Wait for 2 seconds to ensure cookies are set
    time.sleep(2)

    # Retrieve cookies from the browser's application storage
    cookies = driver.get_cookies()

    # Define the desired order of cookies, including the additional cookies from manual extraction
    cookie_order = [
        "_ga", "_ga_87M7PJ3R97", "RT", "_abck", "ak_bmsc", 
        "nseappid", "bm_mi", "bw==~1", "bm_sz", "defaultLang=en", "bm_sv",
        "AKA_A2", "nsit"
    ]

    # Create a dictionary of cookies by their names
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    # Combine the cookies in the specified order, ignoring any that are not present
    combined_cookies = '; '.join([f"{name}={cookie_dict.get(name, '')}" for name in cookie_order if name in cookie_dict])

    # Output the combined cookies string
    print(f"cookies={combined_cookies}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the WebDriver is properly closed
    driver.quit()
