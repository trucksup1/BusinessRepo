from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the desired capabilities for Appium
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "10"
options.device_name = "OnePlus 6T"
options.app_package = "com.trucksup.field_officer"  # Field Officer app package
options.app_activity = ".activities.LoginActivity"  # Activity name for Field Officer login screen
options.automation_name = "UiAutomator2"
options.no_reset = True

# Initialize the Appium driver
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

# Wait for the mobile number input field to be clickable
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//android.widget.EditText[@resource-id='com.trucksup.field_officer:id/phone_txt']"))
)

# XPaths for the mobile number input field, password input field, login button, and OK button
phone_input_xpath = "//android.widget.EditText[@resource-id='com.trucksup.field_officer:id/phone_txt']"  # Phone input field
password_input_xpath = "//android.widget.EditText[@resource-id='com.trucksup.field_officer:id/password_txt']"  # Password input field
login_button_xpath = "//android.widget.TextView[@resource-id='com.trucksup.field_officer:id/login_btn']"  # Login button XPath
ok_button_xpath = "//android.widget.TextView[@resource-id='com.trucksup.field_officer:id/ok']"  # OK button XPath (for pop-up)


# Function to enter mobile number, password, click login, handle pop-up, and allow time to read the message
def test_login(mobile_number, password, is_third_attempt=False):
    # Enter mobile number
    mobile_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, phone_input_xpath))
    )
    mobile_field.clear()
    mobile_field.send_keys(mobile_number)
    print(f"Entered mobile number: {mobile_number}")

    # Enter password
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, password_input_xpath))
    )
    password_field.clear()
    password_field.send_keys(password)
    print(f"Entered password: {password}")

    # Click on the login button
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, login_button_xpath))
    )
    login_button.click()
    print(f"Clicked on 'Login' button.")

    # Handle pop-up (OK button) after login attempt (for 1st and 2nd attempt)
    if not is_third_attempt:
        try:
            # Wait for the OK button (pop-up) to be clickable
            ok_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, ok_button_xpath))
            )

            # Allow some time for the user to read the pop-up message
            print("Waiting for user to read the pop-up message...")
            time.sleep(5)  # Adjust the time as needed (in seconds)

            # Click on the OK button to close the pop-up
            ok_button.click()
            print(f"Clicked on 'OK' button for the pop-up.")
        except Exception as e:
            print(f"No pop-up found or error while clicking 'OK': {e}")


# First attempt: Enter mobile number and password, and click login
mobile_number1 = "8303871416"
password1 = "Test@1234"
test_login(mobile_number1, password1)

# Wait for 2 seconds before the second attempt
time.sleep(2)

# Second attempt: Enter mobile number and password, and click login
mobile_number2 = "8303871415"
password2 = "Test@1234565"
test_login(mobile_number2, password2)

# Wait for 2 seconds before the third attempt
time.sleep(2)

# Third attempt: Enter mobile number and password, and click login (without handling the OK pop-up)
mobile_number3 = "8303871415"
password3 = "Test@12345"
test_login(mobile_number3, password3, is_third_attempt=True)

# Wait for a while to observe the result
time.sleep(5)

# Close the Appium session
driver.quit()
