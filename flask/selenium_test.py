from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Path to chromedriver
chrome_driver_path = '/usr/local/bin/chromedriver'

# Initialize WebDriver
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Open the Flask app URL
driver.get("http://127.0.0.1:5000")

# Find the password input element and submit a strong password
password_input = driver.find_element_by_name("password")
password_input.send_keys("StrongPass123")
password_input.send_keys(Keys.RETURN)

# Wait for a bit to let the page load
time.sleep(3)

# Check if the strong password was accepted
assert "Welcome" in driver.page_source

# Submit a weak password
driver.get("http://127.0.0.1:5000")
password_input = driver.find_element_by_name("password")
password_input.send_keys("password")
password_input.send_keys(Keys.RETURN)

# Wait for a bit to let the page load
time.sleep(3)

# Check if the weak password was rejected
assert "Password does not meet the requirements" in driver.page_source

# Close the browser
driver.quit()
