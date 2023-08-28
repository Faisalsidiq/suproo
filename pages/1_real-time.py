import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

# URL to the Google Sheets CSV export link
csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

# Load CSV data using pandas
df = pd.read_csv(csv_url, parse_dates=[['Date', 'Time']])
df['Date_Time'] = pd.to_datetime(df['Date_Time'])

# Get the latest row
latest_row = df.iloc[-1]

# Create a Folium map centered around the given latitude and longitude
m = folium.Map(location=[-7.783000, 110.410538], zoom_start=15)

# Define a custom function to create a popup with data values
def create_popup(row):
    popup = '<b>Date:</b> {}<br>'.format(row['Date_Time'])
    for column in df.columns[1:]:
        popup += '<b>{}:</b> {}<br>'.format(column, row[column])
    return folium.Popup(popup, max_width=300)

# Add a marker for the given latitude and longitude with the custom popup
folium.Marker(
    location=[-7.783000, 110.410538],
    popup=create_popup(latest_row),
    icon=folium.Icon(color="blue"),
).add_to(m)

# Display the map
folium_static(m)

# When the marker is clicked, display the custom popup
if m.get_name() in st._widget_to_ctx:
    marker = st._widget_to_ctx[m.get_name()].map_children[0]
    if marker.get_name() in st._widget_to_ctx:
        clicked = st._widget_to_ctx[marker.get_name()].button("Click to Load Latest Value")
        if clicked:
            st.write("Latest Value:")
            selected_column = st.selectbox("Select a column", df.columns[1:])
            st.write(f"{selected_column}: {latest_row[selected_column]}")

