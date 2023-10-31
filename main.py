import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from telegram import Bot
import os

chromedriver_autoinstaller.install()

username = os.environ.get("MICROSOFT_USERNAME")
password = os.environ.get("MICROSOFT_PASSWORD")
removebg_api_key = os.environ.get("REMOVE_BG_API_KEY")
telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
telegram_token = os.environ.get("TELEGRAM_TOKEN")

def login_to_microsoft(username, password):
    options = Options()
    options.add_argument("--headless")
    options.add_argument('window-size=1980,960')

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.seaofthieves.com/login")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "loginfmt")))
    username_field = driver.find_element(By.NAME, "loginfmt")
    username_field.clear()
    username_field.send_keys(username)

    next_button = driver.find_element(By.ID, "idSIButton9")
    next_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "passwd")))
    time.sleep(2)

    password_field = driver.find_element(By.NAME, "passwd")
    password_field.send_keys(password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    sign_in_button = driver.find_element(By.ID, "idSIButton9")
    sign_in_button.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    sign_in_button = driver.find_element(By.ID, "idSIButton9")
    sign_in_button.click()

    driver.get("https://www.seaofthieves.com/profile/guilds/b98af840-cb54-4a70-8490-f61250b55c06/members")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "guild-roundel.guild-roundel--supernatural-sailor")))
    time.sleep(10)

    div = driver.find_element(By.CSS_SELECTOR, '.guild-roundel.guild-roundel--supernatural-sailor')
    div.screenshot('div_screenshot.png')  # saves the screenshot in the current directory

async def send_image_to_telegram_group(image_path, chat_id, token):
    bot = Bot(token=token)
    with open(image_path, 'rb') as image_file:
        await bot.send_photo(chat_id=chat_id, photo=image_file, caption="Vamo manga de croto que falta una bocha hasta el 15")

def remove_background_from_img_file(image_path, API_key):
    from removebg import RemoveBg
    rmbg = RemoveBg(API_key, "error.log")
    rmbg.remove_background_from_img_file(image_path)


if __name__ == "__main__":
    login_to_microsoft(username, password)
    remove_background_from_img_file('div_screenshot.png',removebg_api_key)
    asyncio.run(send_image_to_telegram_group('div_screenshot.png_no_bg.png', int(telegram_chat_id), telegram_token))