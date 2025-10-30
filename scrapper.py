from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
# Set up Selenium options
options = Options()
options.add_argument("--headless")  # Enable headless mode for GitHub Actions
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Rotate User-Agent to prevent detection
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")

# Set up ChromeDriver using webdriver_manager
# service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(options=options)

# Define the target website (CoinMarketCap Bitcoin page)
URL = "https://www.ebay.com/globaldeals/tech"


def infinite_Scroll():
    # Scroll down multiple times to load more content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Stop scrolling when no new content is loaded
    last_height = new_height


Data = []

def scrape_ebay_data():
    """Scrape Bitcoin details from CoinMarketCap."""
    driver.get(URL)
    time.sleep(10)  # Allow time for elements to load
    cards = driver.find_elements(By.XPATH, '//div[@itemscope="itemscope"]')
    for card in cards:
        try:
            # Capture timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Extract  Price

            try:
                price = card.find_element(
                    By.XPATH, './/span[@itemprop="price"]').text
            except:
                print("Error in getting the price")
                price = "NA"

            # title

            try:
                Title = card.find_element(
                    By.XPATH, './/span[@itemprop="name"]').text
            except:
                print("Error in getting the title")
                Title = "Unknown"
            # Extract Original Price
            try:
                original_price = card.find_element(
                    By.XPATH, './/span[@class="itemtile-price-strikethrough"]').text
            except:
                print("Error in getting the original_price")
                original_price = "NA"

            # Extract item URL
            

            try:
                item_url_a = card.find_element(By.XPATH, ".//div//a")
                item_URL = item_url_a.get_attribute("href")
            except:
                print("Error in getting the item_URL")
                item_URL = "NA"
            shipping = "N/A"
            try:            
                resp = requests.get(
                    item_URL,
                    headers={"User-Agent": ua.random},
                    timeout=10
                )
                if resp.ok:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    shipping_div = soup.find(
                        "div", class_="ux-labels-values__values-content")

                    if shipping_div:
                        bold_span = shipping_div.find(
                            "span", class_="ux-textspans--BOLD")
                        spans = shipping_div.find_all(
                            "span", class_="ux-textspans")

                        bold_text = bold_span.get_text(
                            strip=True) if bold_span else ""
                        rest_text = spans[2].get_text(
                            strip=True) if len(spans) >= 3 else ""

                        candidate = f"{bold_text} {rest_text}".strip()
                        if candidate:
                            shipping = candidate
            except Exception:
             pass               
            Data.append({
                "timestamp": timestamp,
                "Title": Title,
                "price": price,
                "Original_Price": original_price,
                "Shipping_Info": shipping,
                "URL": item_URL
            })
        except Exception as e:
            print("Error occurred:", e)
            return None
    return Data

def save_to_csv(data):
    file_name = "ebay_tech_deals.csv"
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
if __name__ == "__main__":
    print("Scraping Ebay Data...")
    print("Starting the infinite Scroll...")
    infinite_Scroll()
    scraped_data = scrape_ebay_data()

    if scraped_data:
        save_to_csv(scraped_data)
        print("Data saved to ebay_tech_deals.csv")
    else:
        print("Failed to scrape data.")
    driver.quit()
