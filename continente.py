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


def accept_cookies_continente(driver):
    try:
        time.sleep(5)
        # Wait till page is loaded
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "CybotCookiebotDialog")))

        # Accept cookies
        accept_button = driver.find_element(
            By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        accept_button.click()

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
        print("Failed to load TudoGostoso.com.br ")


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
        search_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "q")))
        search_item.clear()
        search_item.send_keys(product + Keys.ENTER)

        time.sleep(5)

        select_item = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div[1]/div[3]/div[2]/div/div[1]/div/div[2]/div[3]/div[1]/div/div/div/div[2]/div[2]/div[3]/div[2]/button")))
        select_item.click()

        print(f"Add '{product}' to cart")

    except Exception as e:
        print(f"Failed to add product '{product}' to cart:", e)


def revise_shopping_cart(driver):
    try:
        shopping_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/nav/div/div[1]/div[2]/div[3]/div[1]/a")))
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
    driver.get("https://continente.pt")

    # Accept cookies
    accept_cookies_continente(driver)

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
