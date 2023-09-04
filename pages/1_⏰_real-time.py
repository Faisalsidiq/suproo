import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

logo = "logo.png"
# Display the logo image
st.image(logo, width=200)  # Adjust the width as needed

st.title("Real-time Air Pollution Monitoring")

# URL to the Google Sheets CSV export link
csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

# Load CSV data using pandas
df = pd.read_csv(csv_url, parse_dates=[['Date', 'Time']])
df['Date_Time'] = pd.to_datetime(df['Date_Time'])

# Get the latest row from the provided Google Sheets link
new_csv_url = "https://docs.google.com/spreadsheets/d/1YBFtPHmZa6Io25Ef-SNTp2xQCoqK-2Q1bW4XTXQQ_yI/export?format=csv"
new_df = pd.read_csv(new_csv_url, parse_dates=[['Date', 'Time']])
new_df['Date_Time'] = pd.to_datetime(new_df['Date_Time'])
latest_row_new = new_df.iloc[-1]

# Create a Folium map centered around the given latitude and longitude
m = folium.Map(location=[-7.783000, 110.410538], zoom_start=15)

# Define a custom function to create a popup with data values
def create_popup(row):
    popup = '<b>Date:</b> {}<br>'.format(row['Date_Time'])
    for column in df.columns[1:]:
        popup += '<b>{}:</b> {}<br>'.format(column, row[column])
    return folium.Popup(popup, max_width=300)

# Add a marker for the given latitude and longitude with the custom popup (latest data from the provided Google Sheets)
folium.Marker(
    location=[-7.786335507018436, 110.38799288469626],
    popup=create_popup(latest_row_new),
    icon=folium.Icon(color="red"),
).add_to(m)

# Display the map
folium_static(m)

