import re
import pandas as pd
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_last_processed_city(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data["last_processed_city"]
    except FileNotFoundError:
        return 0


def update_last_processed_city(filename, i):
    data = {"last_processed_city": i}
    with open(filename, "w") as f:
        json.dump(data, f)


def load_gym_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_gym_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


# Configuring webdriver - in my case, I chose ChromeDriver
options = Options()
options.add_argument("--no-sandbox")
driver = webdriver.Chrome("chromedriver", options=options)

# Uploading all gyms' data from CSV obtained
smartfit_data = pd.read_csv("../../SmartFit_Occupancy/webcrawling/results/smartfit_gyms.csv")

# List to store CSV updated file
occupancy_data_upd = "../../SmartFit_Occupancy/webcrawling/checkpoints/occupancy_data_upd.json"
updated_rows = load_gym_data(occupancy_data_upd)

last_processed_city_filename = "../../SmartFit_Occupancy/webcrawling/checkpoints/last_processed_city_occupancy.json"
last_processed_city_index = get_last_processed_city(last_processed_city_filename)

for index, row in smartfit_data.iterrows():
    if index < last_processed_city_index:
        continue
    link = row["link"]
    name = row["Nome"]
    address = row["Endereco"]

    # Print Extracting
    print(f"Extracting gym's occupancy: {name}")
    # Get webpage, obtain 'const {data}' value, extract parameter sent to JSON.parse()
    driver.get(link)

    # Wait for content to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//body'))
    )

    # Check page source code with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all script elements in the page
    script_tags = soup.find_all("script")

    # Look for "const {data}" for each script element
    data_value = None
    for script_tag in script_tags:
        match = re.search(r"const\s+{data}\s*=\s*JSON\.parse\(\'(.*?)\'\);", script_tag.string or "")

        if match:
            data_value = match.group(1)
            break

    # If "const {data}" is found, parse JSON and extract the "date" key
    if data_value:
        json_data = json.loads(data_value)
        hourly_data = json_data["data"]

        # Update the row with the extracted values
        updated_row = {
            "link": link,
            "name": name,
            "address": address,
        }

        for hour, value in hourly_data.items():
            updated_row[str(hour)] = value
        updated_row["Updated_At"] = json_data["updatedAt"]
        updated_rows.append(updated_row)

    # After the loop, update the JSON file with the last processed city
    # Save gym occupancy for each 10 cities
    if index % 10 == 0:
        save_gym_data(occupancy_data_upd, updated_rows)
        update_last_processed_city(last_processed_city_filename, index)

# Finish WebDriver
driver.quit()

# New DataFrame with the new rows
updated_gym_data = pd.DataFrame(updated_rows)

# New DataFrame to CSV file
updated_gym_data.to_csv("../../SmartFit_Occupancy/webcrawling/results/gym_occupancy_data.csv", index=False)

