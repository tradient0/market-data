import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure Chrome runs in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL to fetch cookies from
url = 'https://www.nseindia.com/companies-listing/corporate-filings-actions'

# Open the website
driver.get(url)

# Wait for the page to load completely
driver.implicitly_wait(10)

# Get cookies from the browser session
cookies = driver.get_cookies()

# Convert cookies to a dictionary
cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

# Format cookies as a single string
cookie_string = '; '.join([f"{name}={value}" for name, value in cookies_dict.items()])

# Save cookies to an environment variable
os.environ['COOKIES'] = cookie_string

# Print the cookies string to set the output in GitHub Actions
print(f"::set-output name=cookies::{cookie_string}")

# Clean up and close the browser
driver.quit()
