import pytest 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
CHROME_DRIVER_PATH = "/Applications/chromedriver-mac-x64 2/chromedriver"

@pytest.fixture(scope="module")
def setup_teardown():
    global driver
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get("https://github.com/login")
    yield
    driver.quit()

# def teardown_module(module):
#     driver.quit()

def login(username_input, password_input):
    driver.get("https://github.com/login")

    username = driver.find_element(By.ID, "login_field")
    username.send_keys(username_input)

    password = driver.find_element(By.ID, "password")
    password.send_keys(password_input)

    login_button = driver.find_element(By.NAME, "commit")
    login_button.click()
    
   
def test_valid_login(setup_teardown):
    login("validUsername", "validPassword")
    try:
        WebDriverWait(driver, 10).until(EC.title_contains("GitHub"))
        print("Valid Login Test Passed")
    except Exception as e:
        print(f"Valid Login Test Failed: {e}")
        assert False

def test_invalid_login_incorrect_password(setup_teardown):
    login("validUsername", "invalidPassword")
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.flash.flash-full.flash-error"))
        )
        assert "Incorrect username or password." in error_message.text
        print("Invalid Login (Incorrect Password) Test Passed")
    except Exception as e:
        print(f"Invalid Login (Incorrect Password) Test Failed: {e}")
        assert False




    if __name__ == "__main__":
        pytest.main()
