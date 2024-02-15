from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


service = Service(
    ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")


# Wait till page is loaded
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "L2AGLb")))

# Accept cookies
accept_button = driver.find_element(By.ID, "L2AGLb")
accept_button.click()

# User's input of recipe
driver.implicitly_wait(2)
desired_recipe = input("Which recipe would you like to try?: ")

# Find element to start searching
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")

# Guarantee empty textarea
input_element.clear()

# Insert text and hit enter
input_element.send_keys(desired_recipe + Keys.ENTER)
driver.implicitly_wait(2)

# Click on link (LINK_TEXT for exact text)
link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tudo Gostoso")
link.click()

# Wait page to be loaded and accept cookies
driver.implicitly_wait(10)
cookies_btn = driver.find_element(By.CLASS_NAME, "fc-button-label")
cookies_btn.click()

# Search for ingridients
ingredient_elements = driver.find_elements(
    By.XPATH, "//li[@class='is-6 recipe-ingredients-item']/span[@class='recipe-ingredients-item-label']")
print(ingredient_elements)


# Create list of shopping items
# Usar expressão regular - regex
ingredient_names = []
for ingredient in ingredient_elements:
    text_content = ingredient.text

    # Use regex to extract only the ingredient names and remove measures
    ingredient_name = re.sub(
        r'(?i)\b\d+(?:\s+e\s+\d+)?(?:/\d+)?\s*(?:ml|g|kg|colher(?:\(es\))?\s+(?:de\s+)?sopa|colher(?:\(es\))?\s+(?:de\s+)?chá|xícara(?:s)?(?:\s+\(chá\))?|\bpitada\b)\b|\bde\b', '', text_content)

    # Remove any remaining leading/trailing punctuation and whitespace
    ingredient_name = re.sub(r'[^\w\s]', '', ingredient_name.strip())

    # Remove units of measure
    ingredient_name = re.sub(
        r'\b(chá|sopa|colher|colheres|xícara|pitada)\b', '', ingredient_name.strip())

    # Remove numbers
    ingredient_name = re.sub(r'\b\d+\b', '', ingredient_name.strip())

    # Remove extra spaces
    ingredient_name = re.sub(r'\s+', ' ', ingredient_name.strip())

    # Add ingredient name to list if not empty
    if ingredient_name:
        ingredient_names.append(ingredient_name)


print(ingredient_names)

# Go to grocery shop web page
driver.get("https://mercadao.pt")

# Set postal code validation
validated_postal_code = False

# Wait till page is loaded
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))

# Accept Cookies
accept_cookies_btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
accept_cookies_btn.click()

# Click on Specific Store
pingo_doce_store = driver.find_element(
    By.XPATH, "/html/body/pdo-root/main/pdo-page-container/ng-component/div/ng-component/section/pdo-container/div/pdo-brand-logo-top/article/a")
pingo_doce_store.click()

# Check if postal code was inserted
if validated_postal_code is False:
    postal_code_info = driver.find_element(
        By.XPATH, "/html/body/pdo-root/main/pdo-page-container/ng-component/pdo-store-navbar/pdo-navbar-layout/div[2]/pdo-container/ul/li[2]/pdo-navbar-top/div/ul[2]/li[3]/a")
    postal_code_info.click()

    driver.implicitly_wait(2)

    postal_code_input = driver.find_element(
        By.ID, "postalCode")
    postal_code_input.send_keys("4200282" + Keys.ENTER)
    validated_postal_code = True
    time.sleep(1)


# Insert each product on the shopping cart
for product in ingredient_names:

    # Search product
    search_item = driver.find_element(By.ID, "search")
    search_item.clear()
    search_item.send_keys(product + Keys.ENTER)
    time.sleep(1)

    try:
        # Select product that matches
        select_item = driver.find_element(
            By.XPATH, "/html/body/pdo-root/main/pdo-page-container/ng-component/section/pdo-container/div/section/div/ng-component/pdo-product-grid/pdo-product-grid-layout/div/div[1]/pdo-product-item[1]/article/a")
        select_item.click()

        # Add some waiting time to ensure the product page is loaded before interacting with it
        time.sleep(2)

        # Find the add to cart button and click on it
        add_to_cart_button = driver.find_element(
            By.XPATH, "/html/body/pdo-root/main/pdo-page-container/ng-component/section/pdo-container/div/section/div/ng-component/div/div[2]/div/div[2]/article/div[4]/pdo-cart-button")
        add_to_cart_button.click()

    except:
        print(f"Product {product} not found.")


time.sleep(10)

driver.quit()
