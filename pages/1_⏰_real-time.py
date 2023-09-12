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

# URL to the Google Sheets CSV export link for the second data
second_csv_url = "https://docs.google.com/spreadsheets/d/1evsslVMH2fx8EUEjDqS0PA0JzBsSdo1jVG4ddmq4dE4/export?format=csv"

# Load both CSV data using pandas
df_first = pd.read_csv(first_csv_url, parse_dates=[['Date', 'Time']])
df_first['Date_Time'] = pd.to_datetime(df_first['Date_Time'])

df_second = pd.read_csv(second_csv_url, parse_dates=[['Date', 'Time']])
df_second['Date_Time'] = pd.to_datetime(df_second['Date_Time'])

# Get the latest rows from both datasets
latest_row_first = df_first.iloc[-1]
latest_row_second = df_second.iloc[-1]

# Create a Folium map centered around a specific latitude and longitude
m = folium.Map(location=[-7.786335507018436, 110.38799288469626], zoom_start=15)


            

# Define custom functions to create popups with data values
def create_popup_first(row):
    popup = '<b>Date:</b> {}<br>'.format(row['Date_Time'])
    for column in df_first.columns[1:]:
       popup += '<b>CO Level:</b> {} ({})<br>'.format(row['CO'])
    
    return folium.Popup(popup, max_width=300)

def create_popup_second(row):
    popup = '<b>Date:</b> {}<br>'.format(row['Date_Time'])
    for column in df_second.columns[1:]:
        popup += '<b>{}:</b> {}<br>'.format(column, row[column])
    return folium.Popup(popup, max_width=300)

# Add markers for the first and second latitude and longitude with custom popups
folium.Marker(
    location=[-7.776015, 110.374410],
    popup=create_popup_first(latest_row_first),
    icon=folium.Icon(color="blue"),
).add_to(m)

folium.Marker(
    location=[-7.786335507018436, 110.38799288469626],
    popup=create_popup_second(latest_row_second),
    icon=folium.Icon(color="red"),
).add_to(m)

# Display the map with both markers
st.subheader("Map with Data from Both Spreadsheets")
folium_static(m)



