from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument('--headless')
    else:
        options.add_argument("--start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)
