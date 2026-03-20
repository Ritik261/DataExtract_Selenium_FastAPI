from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time

app = FastAPI()


# -------- Request Schema --------
class LoginRequest(BaseModel):
    login_url: str
    email: str
    password: str


# -------- Selenium Setup --------
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # modern headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


# -------- Core Logic --------
def login_and_extract(data: LoginRequest):
    driver = get_driver()

    try:
        driver.get(data.login_url)

        wait = WebDriverWait(driver, 15)

        # -------- CHANGE THESE SELECTORS BASED ON WEBSITE --------
        email = wait.until(
            EC.presence_of_element_located((By.ID, "Email"))
        )
        password_input = driver.find_element(By.ID, "Password")
        login_button = driver.find_element(By.ID, "btnLogin")

        # -------- Perform Login --------
        email.send_keys(data.email)
        password_input.send_keys(data.password)
        login_button.click()

        # -------- Wait for Home/Dashboard --------
        # Change selector to something visible after login
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(2)  # optional: allow JS to load fully

        # -------- Extract Data --------
        page_title = driver.title

        # Example: get headings / important elements
        # headings = driver.find_elements(By.TAG_NAME, "h1")
        # heading_texts = [h.text for h in headings if h.text.strip()]

        # para = driver.find_elements(By.TAG_NAME, "strong")
        # paraText = [p.text for p in para if p.text.strip()]
        
        # # # Example: extract links
        # links = driver.find_elements(By.TAG_NAME, "a")
        # link_data = [
        #     {"text": link.text, "href": link.get_attribute("href")}
        #     for link in links if link.get_attribute("href")
        # ]

        return {
            "Login": "Success",
            "title": page_title
            # "title":page_title, # limit for response size
            # "heading":heading_texts,
            # "para":paraText,
            # "links": link_data
        
        }

    except Exception as e:
        raise Exception(str(e))

    finally:
        driver.quit()


# -------- API Endpoint --------

    