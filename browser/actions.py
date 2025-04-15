from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser.logins import login_amazon, login_ebay
import time 


# This function is to make the app site independent but as of now testing with 2 sites so not in use.
'''def load_site_config(site):
    with open("config/sites.yaml") as f:
        config = yaml.safe_load(f)
    return config.get(site,{})
'''

# Capthca handled manually as of now
def login(driver, site) -> bool:

    login_map = {
        "amazon": login_amazon,
        "ebay": login_ebay,
    }
    if site not in login_map:
        raise Exception(f"No login flow defined for: {site}")
    return login_map[site](driver)

def search(driver, site, parsed_data):

    keyword = parsed_data.get("search_item", "")
    if site == "amazon":
        driver.get("https://www.amazon.com")
        box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        box.send_keys(keyword)
        box.send_keys(Keys.RETURN)
        return f"Searched for {keyword}"
    elif site == "ebay":
        driver.get("https://www.ebay.com")
        box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gh-ac")))
        box.send_keys(keyword)
        box.send_keys(Keys.RETURN)
        return f"Searched for {keyword}"
    else:
        raise Exception(f"Try either amazon or ebay")


def interact_element(driver, site, parsed_data):
    keyword = parsed_data.get("search_item", "")
    product_name = parsed_data.get("match_keyword", "")

    use_fallback = not product_name or product_name == keyword

    def fallback_click():
        print("[Fallback Triggered] Clicking first valid search result...")
        if site == "amazon":
            results = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item a.a-link-normal[href*='/dp/']")
        elif site == "ebay":
            results = driver.find_elements(By.CSS_SELECTOR, ".s-item__link")
        else:
            raise Exception(f"No fallback logic defined for site: {site}")

        for link in results:
            try:
                href = link.get_attribute("href")
                title = link.text.strip()

                if not href or not title or "shop on ebay" in title.lower() or "123456" in href:
                    continue

                print(f"✅ Clicking: {title} -> {href}")
                driver.execute_script("arguments[0].removeAttribute('target');", link)
                driver.execute_script("arguments[0].scrollIntoView();", link)
                driver.execute_script("arguments[0].click();", link)
                return f"[Fallback Success] Clicked: {title}"
            except Exception as e:
                print(f"Skipping link due to error: {e}")
                continue
        return "[Fallback Failed] No suitable result found."

    def match_and_click():
        print(f"🔍 Looking for product match: '{product_name}'")

        if site == "amazon":
            candidates = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item a.a-link-normal[href*='/dp/']")
        elif site == "ebay":
            candidates = driver.find_elements(By.CSS_SELECTOR, ".s-item__link")
        else:
            raise Exception(f"Site '{site}' not supported for matching.")

        for link in candidates:
            try:
                title = link.text.strip().lower()
                if product_name in title:
                    print(f"✅ Matched and clicking: {title}")
                    driver.execute_script("arguments[0].removeAttribute('target');", link)
                    driver.execute_script("arguments[0].scrollIntoView();", link)
                    driver.execute_script("arguments[0].click();", link)
                    return f"Clicked matched product: {title}"
            except Exception as e:
                print(f"Error while trying to match and click: {e}")
                continue

        print("[Match Failed] Could not find matching product, falling back...")
        return fallback_click()

    # Logic control
    if use_fallback:
        return fallback_click()
    else:
        return match_and_click()

        

def add_to_cart(driver, site):

    if site == "amazon":
        try:
            # Try regular button
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
            )
        except:
            # Fallback to the alternate button
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-button-ubb"))
            )
        button.click()
        try:
            inner = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="attachSiNoCoverage"]/span/input')))
            inner.click()
            time.sleep(5)
        except:
            print("No inner button found")
    
    elif site == "ebay":
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "atcBtn_btn_1")))
        button.click()
        # Can't figure out why it is not picking the element.
        # try:
        #     inner = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='bottom-ctas']//button[contains(text(), 'Proceed to cart')]")))

        #     if inner:
        #         inner.click()
        #         print("inner clicked")
        #         time.sleep(5)
        # except Exception as e:
        #     raise Exception(f"error:{e}")

    else:
        raise Exception(f"add_to_cart not supported for site: {site}")

    return f"Item added to cart on {site}"


def execute_actions(driver, site, actions, parsed_data):
    executed_actions = []
    logged_in = False

    for action in actions:
        try:
            print(f"Running action: {action}")
            if action == "login":
                logged_in = login(driver, site)
                if logged_in:
                    executed_actions.append("login")
            elif action == "search":
                # Allows search without login sessions
                search(driver, site, parsed_data)
                interact_element(driver, site, parsed_data)
                executed_actions.append("search")
            elif action == "add_to_cart":
                # Only adds to cart if logged in
                if not logged_in:
                    print("Cannot add to cart: Please login first.")
                    return executed_actions
                add_to_cart(driver, site)
                executed_actions.append("add_to_cart")
            else:
                print(f"Action '{action}' not supported for site '{site}'")

        except Exception as e:
            print(f"Error executing action '{action}': {str(e)}")
            raise e
        
    return executed_actions

