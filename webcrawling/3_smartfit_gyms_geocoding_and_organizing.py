import pandas as pd
import ftfy
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
import time

# Getting Data
df = pd.read_csv("../../SmartFit_Occupancy/webcrawling/results/gym_occupancy_data.csv",
                 usecols=['name', 'address', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                          '17', '18', '19', '20', '21', '22', '23'])


# Correcting broken characters with FTFY
def clean_text(text):
    return ftfy.fix_text(text)


df['name'] = 'SmartFit ' + df['name'].apply(clean_text)
df['address'] = df['address'].apply(clean_text)
df['lat'] = None
df['long'] = None

# Configuring Google geocoder with API key
APIKEY = 'yourkeyhere'
geolocator = GoogleV3(api_key=APIKEY)


# Function to geocode the address with timeout handling
def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location is not None:
            return location.lat, location.long
    except GeocoderTimedOut:
        # Timeout occurred, introduce a delay and retry
        time.sleep(2)
        return geocode_address(address)
    return None, None


# Iterate over the rows and geocode the addresses
for index, row in df.iterrows():
    address = row['address']
    lat, long = geocode_address(address)
    if lat is None or long is None:
        name = row['name']
        lat, long = geocode_address(name)
    df.at[index, 'lat'] = lat
    df.at[index, 'long'] = long


nan_rows = df[df['lat'].isnull()]
print(nan_rows)

#Here, two addresses were not found - I've dropped them bc they are irrelevant to me.

df = df.dropna(subset=['lat', 'long'])

df.to_csv('../../SmartFit_Occupancy/data/SmartFit_Data.csv', encoding='utf-8')
