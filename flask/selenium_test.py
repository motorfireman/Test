from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
import time
import os

# Path to chromedriver
chrome_driver_path = os.path.abspath('workspace/chromedriver')

# Initialize WebDriver with Service object
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the Flask app URL
driver.get("http://127.0.0.1:5000")

# Find the password input element and submit a strong password
password_input = driver.find_element("name", "password")
password_input.send_keys("StrongPass123")
password_input.send_keys(Keys.RETURN)

# Wait for a bit to let the page load
time.sleep(3)

# Check if the strong password was accepted
assert "Welcome" in driver.page_source

# Submit a weak password
driver.get("http://127.0.0.1:5000")
password_input = driver.find_element("name", "password")
password_input.send_keys("password")
password_input.send_keys(Keys.RETURN)

# Wait for a bit to let the page load
time.sleep(3)

# Check if the weak password was rejected
assert "Password does not meet the requirements" in driver.page_source

# Close the browser
driver.quit()
