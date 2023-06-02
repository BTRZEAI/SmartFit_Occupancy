import pandas as pd
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, \
    ElementNotInteractableException


def get_last_processed_city(filename):
    try:
        with open(filename, "r") as f:
            data_city = json.load(f)
            return data_city["last_processed_city"]
    except FileNotFoundError:
        return 0


def update_last_processed_city(filename, i):
    data_city = {"last_processed_city": i}
    with open(filename, "w") as f:
        json.dump(data_city, f)


def load_gym_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_gym_data(filename, data_gym):
    with open(filename, "w") as f:
        json.dump(data_gym, f)


# Configuring webdriver - in my case, I chose ChromeDriver
options = Options()
options.add_argument("--no-sandbox")
driver = webdriver.Chrome("chromedriver", options=options)

# Uploading all brazilian cities and states from CSV
file_path = "./webcrawling/utilities/cities.csv"
cities_df = pd.read_csv(file_path)

last_processed_city_filename = "../../SmartFit_Occupancy/webcrawling/checkpoints/last_processed_city.json"
last_processed_city_index = get_last_processed_city(last_processed_city_filename)

gym_data_filename = "../../SmartFit_Occupancy/webcrawling/checkpoints/gym_data.json"
gyms = load_gym_data(gym_data_filename)

url = "https://www.smartfit.com.br/academias"

# gyms = []
# Opening URL
driver.get(url)
# driver.implicitly_wait(2)

for index, row in cities_df.iterrows():
    if index < last_processed_city_index:
        continue
    city = row["name"]
    state = row["state"]

    # Close Cookie Consent box
    try:
        cookie_consent_btn = driver.find_element(By.ID, "newv4CookieConsentBtn")
        cookie_consent_btn.click()
    except (NoSuchElementException, ElementNotInteractableException):
        print("")

    # Put brazilian city name, click on search button
    search_field = driver.find_element(By.ID, "address-input")
    search_field.clear()
    search_field.send_keys(f"{city}, {state}")
    search_button = driver.find_element(By.CLASS_NAME, "v4-search-button-submit")
    search_button.click()

    # Wait fot  "new-animation-loading-wrapper" element to be removed
    loading_wrapper = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.CLASS_NAME, "new-animation-loading-wrapper"))
    )
    WebDriverWait(driver, 2).until(EC.staleness_of(loading_wrapper))
    # Check until "v4-search-feedback-container" class element is not there
    feedback_containers = driver.find_elements(By.XPATH, '//div[contains(@class, "v4-search-feedback-container")]')
    if not feedback_containers:
        print("Found! ")
        print(feedback_containers)
        # Click on "ver mais" button until all units are loaded
        while True:
            try:
                ver_mais_btn = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "js-next-page-button"))
                )
                ver_mais_btn.click()
                time.sleep(1.5)  # Wait for content to be loaded
            except StaleElementReferenceException:
                continue
            except Exception as e:
                print("Button 'ver mais' not found or clickable.")
                break
    else:
        print(feedback_containers)
        print("Not found gyms")

    # Check page content through BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find divs which contains the link I want
    divs = soup.find_all("div", class_="Locations__item_wrap")

    # Extract the links from found divs
    links = []
    names = []
    address = []
    for div in divs:
        data = div.find("div", class_="card__address")
        link = div.find("a", class_="card__link")
        if link:
            link = "https://www.smartfit.com.br" + link["href"]
        if data:
            name = data.find("h3").text
            address = data.find("p").text
        print(link)
        gyms.append([link, name, address])

    # In the end of the loop, refresh the JSON file with the last processed city
    # Saving data for each 10 processed cities
    if index % 10 == 0:
        save_gym_data(gym_data_filename, gyms)
        update_last_processed_city(last_processed_city_filename, index)

# Saving gym data in the end of the script
save_gym_data(gym_data_filename, gyms)

# Compiling the data in a single csv file
df = pd.DataFrame(gyms, columns=["link", "Nome", "Endereco"])

df.to_csv('../../SmartFit_Occupancy/webcrawling/results/smartfit_gyms.csv', index=False)
driver.quit()
