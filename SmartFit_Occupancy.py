# Loading Libraries
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium

# Loading Data
df = pd.read_csv('./data/SmartFit_Data.csv')

st.set_page_config(
    page_title="Mapa de Ocupação SmartFit",
    page_icon=":world_map:",
    layout="wide",
)

"# Gym Dashboard"
"Para eu identificar qual Smart Fit está cheia e qual não está."

# Map focused on Insper college
m = folium.Map(location=[-23.59, -46.67], zoom_start=12)

# Adding markers for each gym
for index, row in df.iterrows():
    location = row['latitude'], row['longitude']
    gym_name = row['name']
    gym_address = row['address']
    occupancy_data = list(row[4:23])
    popup_text = '<b>' + gym_name + '</b><br>' + gym_address + '<br><br>'
    popup_text += '<table><tr><th>Hour</th><th>Occupancy</th></tr>'
    for i in range(4, 23):
        popup_text += '<tr><td>' + str(i) + ':00</td><td>' + str(occupancy_data[i - 4]) + '%</td></tr>'
    popup_text += '</table>'
    marker = folium.Marker(location=location, popup=popup_text)
    marker.add_to(m)


# Choropleth layer function
def add_choropleth(map_folium, hour_gym):
    # Add a choropleth layer to the map
    folium.Choropleth(
        geo_data='https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json',
        name='choropleth',
        data=df,
        columns=['name', str(hour_gym)],
        key_on='feature.properties.name',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Occupancy (%)'
    ).add_to(map_folium)


# Adding slider to select which hour of the day to display
hour = st.slider('Select hour', 4, 23, 12)

# Adding button to update map
if st.button('Update map'):
    # Remove existing choropleth layer
    for layer in m._children:
        if layer.startswith('choropleth'):
            del m._children[layer]

    # Adding new choropleth layer
    add_choropleth(m, hour)

# Display map
st_data = st_folium(m, width=2000, height=500)
