
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

load_dotenv()

USERNAME = os.getenv("wg_username")
PASSWORD = os.getenv("wg_password")

LOGIN_URL = os.getenv("login_url")
TASKS_URL = os.getenv("tasks_url")

def login_and_fetch_tasks():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.binary_location = "/nix/store/zi4f80l169xlmivz8vja8wlphq74qqk0-chromium-125.0.6422.141/bin/chromium"
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    if os.name != "nt":
        options.binary_location = "/nix/store/zi4f80l169xlmivz8vja8wlphq74qqk0-chromium-125.0.6422.141/bin/chromium"

    driver = webdriver.Chrome(options=options)
    driver.get(LOGIN_URL)

    # Wait for the login form and fill it
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))

    driver.find_element(By.NAME, "name").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Wait for the challenge page to load
    WebDriverWait(driver, 10).until(EC.url_contains("/challenges"))

    driver.get(TASKS_URL)

    # Wait for the challenge board to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.category-header.mb-3"))
    )

    tasks = []
    
    # Find all category sections
    category_headers = driver.find_elements(By.CSS_SELECTOR, "div.category-header.mb-3")
    
    for header_div in category_headers:
        try:
            # Extract category name from the <h3> inside
            category_name = header_div.find_element(By.TAG_NAME, "h3").text.strip()

            # Locate the next sibling containing the tasks (class="category-challenges ...")
            category_challenges = header_div.find_element(
                By.XPATH, "following-sibling::div[contains(@class, 'category-challenges')]"
            )

            # Get all challenge buttons inside this sibling
            challenge_buttons = category_challenges.find_elements(By.CLASS_NAME, "challenge-button")

            for btn in challenge_buttons:
                task_id = btn.get_attribute("value")
                title = btn.find_element(By.TAG_NAME, "p").text

                tasks.append({
                    "id": task_id,
                    "title": title,
                    "category": category_name
                })

        except Exception as e:
            print(f"Error processing a category section: {e}")
            # continue to next category

    driver.quit()
    return tasks
