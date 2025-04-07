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
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

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

    # Wait for the challenge buttons to appear
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "challenge-button")))

    buttons = driver.find_elements(By.CLASS_NAME, "challenge-button")
    tasks = []

    for btn in buttons:
        title_el = btn.find_element(By.TAG_NAME, "p")
        task_id = btn.get_attribute("value")
        title = title_el.text
        tasks.append({
            "id": task_id,
            "title": title
        })

    driver.quit()
    return tasks