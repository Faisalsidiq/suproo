import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

logo = "logo.png"
# Display the logo image
st.image(logo, width=200)  # Adjust the width as needed

st.title("Real-time Air Pollution Monitoring")

# URL to the Google Sheets CSV export link for the first data
first_csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

# Load the first CSV data using pandas
df_first = pd.read_csv(first_csv_url, parse_dates=[['Date', 'Time']])
df_first['Date_Time'] = pd.to_datetime(df_first['Date_Time'])

# Get the latest row from the first data
latest_row_first = df_first.iloc[-1]

# URL to the Google Sheets CSV export link for the second data
second_csv_url = "https://docs.google.com/spreadsheets/d/your_second_spreadsheet_url/export?format=csv"

# Load the second CSV data using pandas
df_second = pd.read_csv(second_csv_url, parse_dates=[['Waktu']])
df_second['Date_Time'] = pd.to_datetime(df_second['Date_Time'])

# Get the latest row from the second data
latest_row_second = df_second.iloc[-1]

# Create a Folium map centered around the given latitude and longitude
m = folium.Map(location=[-7.783000, 110.410538], zoom_start=15)

# Define a custom function to create a popup with data values
def create_popup(row):
    popup = '<b>Date:</b> {}<br>'.format(row['Date_Time'])
    for column in row.index:
        if column != 'Date_Time':
            popup += '<b>{}:</b> {}<br>'.format(column, row[column])
    return folium.Popup(popup, max_width=300)

# Add a marker for the given latitude and longitude with the custom popup (latest data from the second Google Sheets)
folium.Marker(
    location=[-7.786335507018436, 110.38799288469626],
    popup=create_popup(latest_row_second),
    icon=folium.Icon(color="red"),
).add_to(m)

# Display the map
folium_static(m)


