from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time


def accept_cookies_google(driver):
    print("Accepting Cookies on Google.com")
    try:
        # Wait till page is loaded
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "L2AGLb")))

        # Accept cookies
        accept_button = driver.find_element(By.ID, "L2AGLb")
        accept_button.click()

    except Exception as e:
        print("Failed to accept cookies on Google.com:", e)


def accept_cookies_mercadao(driver):
    try:
        time.sleep(5)
        # Wait till page is loaded
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))

        # Accept Cookies
        accept_cookies_btn = driver.find_element(
            By.ID, "onetrust-accept-btn-handler")
        accept_cookies_btn.click()

    except Exception as e:
        print("Failed to accept cookies on Continente.com:", e)


def accept_cookies_tudogostoso(driver):
    try:
        # Wait till page is loaded
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fc-button-label")))

        # Accept cookies
        accept_button = driver.find_element(By.CLASS_NAME, "fc-button-label")
        accept_button.click()

    except Exception as e:
        print("Failed to accept cookies on TudoGostoso.com:", e)


def search_recipe(driver, desired_recipe):
    try:
        # Find element to start searching
        input_element = driver.find_element(By.CLASS_NAME, "gLFyf")

        # Guarantee empty textarea
        input_element.clear()

        # Insert text and hit enter
        input_element.send_keys(desired_recipe + Keys.ENTER)

    except Exception as e:
        print("Failed to search recipe:", e)


def redirect_to_recipe_page():
    try:
        # Find best link to redirect to favorite recipe webpage:
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tudo Gostoso")
        link.click()

    except Exception as e:
        print("Failed to load TudoGostoso.com.br: ", e)


def redirect_to_pingo_doce(driver):
    try:
        time.sleep(2)
        pingo_doce_store = driver.find_element(
            By.XPATH, "/html/body/pdo-root/main/pdo-page-container/ng-component/div/ng-component/section/pdo-container/div/pdo-brand-logo-top/article/a")
        pingo_doce_store.click()
    except Exception as e:
        print("Fail to redirect to Pingo Doce store: ", e)


def set_postal_code(driver, validated_postal_code):
    try:
        if validated_postal_code is False:
            postal_code_info = driver.find_element(
                By.XPATH, "/html/body/pdo-root/main/pdo-page-container/ng-component/pdo-store-navbar/pdo-navbar-layout/div[2]/pdo-container/ul/li[2]/pdo-navbar-top/div/ul[2]/li[3]/a")
            postal_code_info.click()

            postal_code_input = driver.find_element(
                By.ID, "postalCode")

            user_postal_code = input("Insert your postal code: ")

            postal_code_input.send_keys(user_postal_code + Keys.ENTER)

            time.sleep(2)

            return True

    except Exception as e:
        print("Faild to validate postal code: ", e)


def extract_ingredients(driver):
    ingredient_names = []
    try:
        # Find list of ingredients
        ingredient_elements = driver.find_elements(
            By.XPATH, "//li[@class='is-6 recipe-ingredients-item']/span[@class='recipe-ingredients-item-label']")
        print(ingredient_elements)

        # Create list of shopping items - using regex
        for ingredient in ingredient_elements:
            text_content = ingredient.text

            # Use regex to extract only the ingredient names and remove measures
            ingredient_name = re.sub(
                r'(?i)\b\d+(?:\s+e\s+\d+)?(?:/\d+)?\s*(?:ml|g|kg|colher(?:\(es\))?\s+(?:de\s+)?sopa|colher(?:\(es\))?\s+(?:de\s+)?chá|xícara(?:s)?(?:\s+\(chá\))?|\bpitada\b)\b|\bde\b', '', text_content)

            # Remove any remaining leading/trailing punctuation and whitespace
            ingredient_name = re.sub(r'[^\w\s]', '', ingredient_name.strip())

            # Remove units of measure
            ingredient_name = re.sub(
                r'\b(chá|sopa|colher|colheres|xícara|pitada|bem|cheia|batidos|raspas|casca|gosto|a|latas|lata|com|soro)\b', '', ingredient_name.strip())

            # Remove numbers
            ingredient_name = re.sub(r'\b\d+\b', '', ingredient_name.strip())

            # Remove extra spaces
            ingredient_name = re.sub(r'\s+', ' ', ingredient_name.strip())

            # Add ingredient name to list if not empty
            if ingredient_name:
                ingredient_names.append(ingredient_name)

    except Exception as e:
        print("Failed to extract ingredients:", e)

    return ingredient_names


def add_to_cart(driver, product):
    try:
        # Search product
        search_item = driver.find_element(By.ID, "search")
        search_item.clear()
        search_item.send_keys(product + Keys.ENTER)
        time.sleep(1)

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

        print(f"Add '{product}' to cart")

    except Exception as e:
        print(f"Failed to add product '{product}' to cart:", e)


def revise_shopping_cart(driver):
    try:
        shopping_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/pdo-root/main/pdo-page-container/ng-component/pdo-store-navbar/pdo-navbar-layout/div[2]/pdo-container/ul/li[2]/pdo-navbar-right/ul/li[4]/pdo-nav-cart/button/span/button")))
        shopping_cart_btn.click()

    except Exception as e:
        print("Fail to load shopping cart for review")


# Main script
try:
    # Initialize Chrome WebDriver with Service
    service = Service(
        ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Navigate to Google
    driver.get("https://www.google.com")

    # Accept cookies
    accept_cookies_google(driver)

    # User input for recipe
    desired_recipe = input("Which recipe would you like to try?: ")

    # Search for the recipe
    search_recipe(driver, desired_recipe)

    # Redirect to favorite recipe website (TudoGostoso)
    redirect_to_recipe_page()

    # Accept cookies
    accept_cookies_tudogostoso(driver)

    # Extract ingredients
    ingredient_names = extract_ingredients(driver)

    # Output ingredient names
    print(ingredient_names)

    # Navigate to grocery shop website
    driver.get("https://mercadao.pt")

    # Set postal code validation
    validated_postal_code = False
    print(validated_postal_code)

    # Accept cookies
    accept_cookies_mercadao(driver)

    # Redirect to Pingo Doce Store
    redirect_to_pingo_doce(driver)

    # Set postal code
    validated_postal_code = set_postal_code(driver, validated_postal_code)
    print(validated_postal_code)

    # Search and add each product to the cart
    for product in ingredient_names:
        add_to_cart(driver, product)

    # Revise shopping cart
    revise_shopping_cart(driver)

    # Wait user to revise items in cart and accept items
    accept_shopping_cart = input(
        "Revise the items on shopping cart and then press ENTER")

    print(f"Your items were revised and accepted by you")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
