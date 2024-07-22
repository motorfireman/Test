from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (make sure the path to your WebDriver is correct)
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# Navigate to the web application
driver.get("http://127.0.0.1:5000")

# Find the password input field and enter a strong password
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("StrongPass123")
password_field.send_keys(Keys.RETURN)

# Wait for a few seconds to observe the result
time.sleep(3)

# Assert the welcome message
assert "Welcome" in driver.page_source

# Test a weak password
driver.get("http://127.0.0.1:5000")
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("password")
password_field.send_keys(Keys.RETURN)

# Wait for a few seconds to observe the result
time.sleep(3)

# Assert the error message
assert "Password does not meet the requirements" in driver.page_source

# Close the browser
driver.quit()
