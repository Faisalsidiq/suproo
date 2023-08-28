import streamlit as st
import pandas as pd
import folium
from streamlit.components.v1 import html

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
marker = folium.Marker(
    location=[-7.783000, 110.410538],
    popup="Click here to load latest value",
    icon=folium.Icon(color="blue"),
)
marker.add_to(m)

# Convert the Folium map to HTML
folium_html = m.get_root().render()

# Display the map using Streamlit's html component
st.title("Map with Latest Data Value")
st.write("Click the blue marker to load the latest value from the CSV.")
html(folium_html, height=500)  # Display the Folium map

# When the marker is clicked, display the latest value
if marker.get_name() in st._widget_to_ctx:
    ctx = st._widget_to_ctx[marker.get_name()]
    if ctx.triggered:
        st.write("Latest Value:")
        selected_column = st.selectbox("Select a column", df.columns[1:])
        st.write(f"{selected_column}: {latest_row[selected_column]}")
