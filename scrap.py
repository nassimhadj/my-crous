from selenium import webdriver
from dotenv import chaat_id , token_id
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import requests

# Define the path to the ChromeDriver executable (use raw string to avoid backslash issues)
PATH = r"'C:\Users\nsmhadj\Downloads\chromedriver.exe"
TOKEN = token_id
chat_id = chaat_id

# Start ChromeDriver service
service = Service(PATH)
driver = webdriver.Chrome(service=service)

# Define function to send a Telegram message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

# Navigate to the page and maximize the window
driver.get("https://trouverunlogement.lescrous.fr/tools/36/search?bounds=-0.6176931_47.5262993_-0.508546_47.4373546")
driver.maximize_window()

try:
    while True:
        try:
            # Wait for up to 20 seconds for the results element to be visible after page load
            h2_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'SearchResults-desktop'))
            )

            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Check if "Aucun logement" is present
            if "Aucun logement" in h2_element.text:
                print(f"{current_time} - No apartments found.")
            else:
                nassimmsg = f"{current_time} - {h2_element.text}"
                send_telegram_message(nassimmsg)
                print(nassimmsg)

        except Exception as e:
            print(f"An error occurred during element lookup: {e}")

        # Refresh the page and wait for it to reload
        driver.refresh()
        time.sleep(5)  # Give the page a little time to reload before trying to locate the element again

        # Optional: Wait for a few seconds before the next refresh to reduce the number of requests
        time.sleep(30)

except Exception as outer_exception:
    print(f"An outer error occurred: {outer_exception}")

finally:
    driver.quit()  # Ensure the browser is closed at the end