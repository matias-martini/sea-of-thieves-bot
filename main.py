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
from get_player_stats import get_lowest_score_by_tier, get_player_stats, get_friend_scores
from prettytable import PrettyTable
from table_generator import create_svg_table


chromedriver_autoinstaller.install()

username = os.environ.get("MICROSOFT_USERNAME")
password = os.environ.get("MICROSOFT_PASSWORD")
removebg_api_key = os.environ.get("REMOVE_BG_API_KEY")
telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
telegram_token = os.environ.get("TELEGRAM_TOKEN")

options = Options()
options.add_argument("--headless")
options.add_argument('window-size=1980,960')

driver = webdriver.Chrome(options=options)
driver.get("https://www.seaofthieves.com/login")


def login_to_microsoft(driver, username, password):
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "loginfmt")))
    username_field = driver.find_element(By.NAME, "loginfmt")
    username_field.clear()
    username_field.send_keys(username)

    next_button = driver.find_element(By.ID, "idSIButton9")
    next_button.click()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "passwd")))
    time.sleep(2)

    password_field = driver.find_element(By.NAME, "passwd")
    password_field.send_keys(password)

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    sign_in_button = driver.find_element(By.ID, "idSIButton9")
    sign_in_button.click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    sign_in_button = driver.find_element(By.ID, "idSIButton9")
    sign_in_button.click()

    driver.get("https://www.seaofthieves.com/profile/guilds/b98af840-cb54-4a70-8490-f61250b55c06/members")
    time.sleep(10)

    div = driver.find_element(By.CSS_SELECTOR, '.guild-roundel.guild-roundel--supernatural-sailor')
    div.screenshot('div_screenshot.png')  # saves the screenshot in the current directory


def get_player_stats_for_ledger(driver, guild_name):
    driver.get(f"https://www.seaofthieves.com/leaderboards/{guild_name}/friends")
    time.sleep(5)
    friend_scores = get_friend_scores(driver.page_source)

    driver.get(f"https://www.seaofthieves.com/leaderboards/{guild_name}/global")
    time.sleep(5)
    lowest_score_by_tier = get_lowest_score_by_tier(driver.page_source)

    return get_player_stats(friend_scores, lowest_score_by_tier)


async def send_player_scores(driver, chat_id, token):
    goal_hoarders_stats = get_player_stats_for_ledger(driver, "GoldHoarders")
    order_of_souls_stats = get_player_stats_for_ledger(driver, "OrderOfSouls")
    athenas_stats = get_player_stats_for_ledger(driver, "AthenasFortune")
    merchant_stats = get_player_stats_for_ledger(driver, "MerchantAlliance")
    reaper_stats = get_player_stats_for_ledger(driver, "ReapersBones")

    # Combine all the stats
    all_stats = {
        "Gold Hoarders": goal_hoarders_stats,
        "Order of Souls": order_of_souls_stats,
        "Athena's": athenas_stats,
        "Merchant Alliance": merchant_stats,
        "Reaper's Bones": reaper_stats
    }

    # Creating the table
    # table = PrettyTable()
    # table.field_names = ["Guild Name", "Character Name", "Current Tier", "Score [Current/Next]"]

    # # Populating the table
    # for guild_name, stats in all_stats.items():
    #     for character_name, character_stats in stats.items():
    #         current_score = character_stats['current_score']
    #         next_score = character_stats['next_score']
    #         player_tier = character_stats['player_tier']
    #         score_str = f"{current_score:.1f} / {next_score:.1f}"

    #         table.add_row([guild_name, character_name, player_tier, score_str])
    create_svg_table(all_stats, filename='table.png')

    bot = Bot(token=token)
    with open("table.png", 'rb') as image_file:
        await bot.send_photo(chat_id=chat_id, photo=image_file)

    # await bot.send_message(
    #         chat_id=chat_id,
    #         text=f"<pre>{table}</pre>",
    #         parse_mode='HTML'
    #     )


async def send_image_to_telegram_group(image_path, chat_id, token):
    bot = Bot(token=token)
    with open(image_path, 'rb') as image_file:
        await bot.send_photo(chat_id=chat_id, photo=image_file, caption="Vamo manga de croto que falta una bocha hasta el 15")

if __name__ == "__main__":
    for i in range(3):
        try:
            login_to_microsoft(driver, username, password)
            break
        except Exception as e:
            print(f"Attempt {i+1} failed. Error: {str(e)}")
            if i == 2:
                print("All attempts failed.")
    asyncio.run(send_player_scores(driver, int(telegram_chat_id), telegram_token))
    asyncio.run(send_image_to_telegram_group('div_screenshot.png', int(telegram_chat_id), telegram_token))