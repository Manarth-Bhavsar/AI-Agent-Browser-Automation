from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from pathlib import Path
import time 
import os

# Capthca handled manually as of now
env_path = Path(".") / ".env"
load_dotenv()

def login_amazon(driver):
    try:
        username = os.getenv("AMAZON_USERNAME")
        password = os.getenv("AMAZON_PASSWORD")
        driver.get("https://www.amazon.com")
        account_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "nav-link-accountList")))
        greeting_text = account_element.text

        if "Hello, sign in" in greeting_text:
            print("Signing in:")
            account_element.click()

            user_ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ap_email")))
            user_ele.send_keys(username)
            user_ele.send_keys(Keys.RETURN)

            # Pop-up needs to be handled manually for now.
            passwd_ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ap_password")))
            time.sleep(5)
            passwd_ele.send_keys(password)
            passwd_ele.send_keys(Keys.RETURN)
            WebDriverWait(driver, 15).until(EC.text_to_be_present_in_element((By.ID, "nav-link-accountList-nav-line-1"), "Hello"))
            print("✅ Login successful")
            return True

        else:
            print("Already Signed In")
            return True
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False



def login_ebay(driver):
    try:
        driver.get("https://www.ebay.com")
        username = os.getenv("EBAY_USERNAME")
        password = os.getenv("EBAY_PASSWORD")
        account_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gh"]/nav/div[1]/span[1]/span/a')))
        greeting_text = account_element.text

        if "Sign in" in greeting_text:
            print("Signing in:")
            account_element.click()

            user_ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userid")))
            user_ele.send_keys(username)
            user_ele.send_keys(Keys.RETURN)

            # Pop-up needs to be handled manually for now.
            passwd_ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
            time.sleep(5)
            passwd_ele.send_keys(password)
            passwd_ele.send_keys(Keys.RETURN)
            time.sleep(10)
            return True

        else:
            print("Already Signed In")
            return True
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False
