# Recipe to Cart - Portugal Supermarkets

This repository contains Python scripts for automating tasks related to online shopping in two major supermarkets in Portugal: Continente and Pingo Doce (via Mercadao.pt).

## Overview

In this project, Selenium WebDriver is utilized to automate various tasks such as accepting cookies, searching for recipes, extracting ingredients, setting postal codes, adding items to the shopping cart, and revising the shopping cart. The main purpose is to streamline the process of online grocery shopping by automating repetitive tasks. It revolves around searching for a recipe, extracting its ingredients, and preparing the shopping cart accordingly.

## Files

- `continente.py`: Python script for automating tasks on Continente's website.
- `mercadao.py`: Python script for automating tasks on Pingo Doce's website.

## Features

- **Accept Cookies**: Automatically accepts cookies on the respective supermarket websites.
- **Recipe Search**: Searches for a desired recipe on Google and redirects to a popular recipe website (TudoGostoso).
- **Ingredient Extraction**: Extracts ingredients from the recipe webpage.
- **Postal Code Setting**: Allows users to input and validate their postal codes.
- **Adding to Cart**: Searches for and adds each ingredient to the shopping cart.
- **Cart Revision**: Automatically navigates to the shopping cart page for revision.

## Requirements

- Python 3.x
- Selenium WebDriver
- Chrome WebDriver
- Webdriver Manager


## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies (`pip install -r requirements.txt`).
3. Ensure you have the latest Chrome browser installed.
4. _(Optional but Recommended)_ Create and activate a virtual environment to isolate project dependencies.
5. Run the desired script (`python continente.py` or `python mercadao.py`).
6. Follow the instructions provided by the script.


