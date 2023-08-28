import streamlit as st
import pandas as pd
import folium
from io import BytesIO

# URL to the Google Sheets CSV export link
csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"

# Load CSV data using pandas
df = pd.read_csv(csv_url, parse_dates=[['Date', 'Time']])
df['Date_Time'] = pd.to_datetime(df['Date_Time'])

# Get the latest row
latest_row = df.iloc[-1]

# Create a Folium map centered around the given latitude and longitude
m = folium.Map(location=[-7.783000, 110.410538], zoom_start=15)

# Add a marker for the given latitude and longitude
folium.Marker(
    location=[-7.783000, 110.410538],
    popup="Click here to load latest value",
    icon=folium.Icon(color="blue"),
).add_to(m)

# Convert the Folium map to an image
image = BytesIO()
m.save(image, close_file=False)

# Display the map image with a specific size
st.title("Map with Latest Data Value")
st.write("Click the blue marker to load the latest value from the CSV.")
st.image(image, width=800, height=600)  # Set the width and height here


