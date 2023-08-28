import streamlit as st
import pandas as pd
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
    return folium.Popup(popup, max_width=600)

# Add a marker for the given latitude and longitude with the custom popup
folium.Marker(
    location=[-7.783000, 110.410538],
    popup=create_popup(latest_row),
    icon=folium.Icon(color="blue"),
).add_to(m)

# Display the map using Streamlit's map component
st.title("Map with Latest Data Value")
st.write("Click the blue marker to view the latest data from the CSV.")

# Apply custom CSS style to adjust map frame size
map_html = f'<div style="width: 800px; height: 600px;">{m.get_root().render()}</div>'
st.markdown(map_html, unsafe_allow_html=True)


