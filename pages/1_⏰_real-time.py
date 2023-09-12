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

def hitung_tingkat_polusi(pollutant_name, value):
    if pollutant_name == 'CO':
        if value < 4000:
            return "Baik"
        elif value >= 4000 and value < 8000:
            return "Sedang"
        elif value >= 8000 and value < 30000:
            return "Tidak Sehat"
        elif value >= 30000 and value < 45000:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"
            
    elif pollutant_name == 'SO2':
        if value < 52:
            return "Baik"
        elif value >= 52 and value < 180:
            return "Sedang"
        elif value >= 180 and value < 400:
            return "Tidak Sehat"
        elif value >= 400 and value < 800:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"
            
    elif pollutant_name == 'O3':
        if value < 120:
            return "Baik"
        elif value >= 120 and value < 235:
            return "Sedang"
        elif value >= 235 and value < 400:
            return "Tidak Sehat"
        elif value >= 400 and value < 800:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"
            
    elif pollutant_name == 'NO2':
        if value < 80:
            return "Baik"
        elif value >= 80 and value < 200:
            return "Sedang"
        elif value >= 200 and value < 1130:
            return "Tidak Sehat"
        elif value >= 1130 and value < 2260:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"
            
    elif pollutant_name == 'HC':
        if value < 45:
            return "Baik"
        elif value >= 45 and value < 1000:
            return "Sedang"
        elif value >= 1000 and value < 215:
            return "Tidak Sehat"
        elif value >= 215 and value < 432:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"
            
    elif pollutant_name == 'PM10':
        if value < 50:
            return "Baik"
        elif value >= 50 and value < 150:
            return "Sedang"
        elif value >= 150 and value < 350:
            return "Tidak Sehat"
        elif value >= 350 and value < 420:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"
            
    elif pollutant_name == 'PM2p5':
        if value < 15.5:
            return "Baik"
        elif value >= 15.5 and value < 55.4:
            return "Sedang"
        elif value >= 55.4 and value < 150.4:
            return "Tidak Sehat"
        elif value >= 150.4 and value < 250.4:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"


def create_popup_first(row):
    popup = '<b>Date:</b> {}<br>'.format(row['Date_Time'])
    for column in df_first.columns[1:]:
        value = row[column]
        pollutant_category = hitung_tingkat_polusi(column, value)
        popup += '<b>{}:</b> {} ({})<br>'.format(column, value, pollutant_category)
    return folium.Popup(popup, max_width=300)

def create_popup_second(row):
    popup = '<b>Date:</b> {}<br>'.format(row['Date_Time'])
    for column in df_second.columns[1:]:
        value = row[column]
        pollutant_category = hitung_tingkat_polusi(column, value)
        popup += '<b>{}:</b> {} ({})<br>'.format(column, value, pollutant_category)
    return folium.Popup(popup, max_width=300)






# Add markers for the first and second latitude and longitude with custom popups

folium.Marker(
    location=[-7.786335507018436, 110.38799288469626],
    popup=create_popup_second(latest_row_second),
    icon=folium.Icon(color="red"),
).add_to(m)

folium.Marker(
    location=[-7.776015, 110.374410],
    popup=create_popup_first(latest_row_first),
    icon=folium.Icon(color="blue"),
).add_to(m)

# Display the map with both markers
st.subheader("Map with Data from Both Spreadsheets")
folium_static(m)


