import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# URL to the Google Sheets CSV export link
csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"
# Load CSV data using pandas
df = pd.read_csv(csv_url)

# Sidebar options
st.sidebar.header('Options')
selected_date = st.sidebar.date_input('Select a date', pd.to_datetime(df['Date']).dt.date.unique())
selected_time = st.sidebar.selectbox('Select a time', pd.to_datetime(df['Time']).dt.time.unique())
selected_meteorology = st.sidebar.selectbox('Select meteorology column', ['Temperature', 'Humidity'])
selected_pollutant = st.sidebar.selectbox('Select pollutant column', ['SO2', 'CO', 'O3', 'NO2', 'HC', 'PM1p0', 'PM2p5', 'PM10'])

# Filter data based on user selection
filtered_df = df[(pd.to_datetime(df['Date']).dt.date == selected_date) &
                 (pd.to_datetime(df['Time']).dt.time == selected_time)]

# Calculate correlation
correlation = filtered_df[selected_meteorology].astype(float).corr(filtered_df[selected_pollutant].astype(float))

# Main content
st.title('Google Sheets Data Viewer')
st.write('Selected Data:')
st.write(f'Date: {selected_date}, Time: {selected_time}')
st.write(f'Meteorology: {selected_meteorology}')
st.write(f'Pollutant: {selected_pollutant}')
st.write(filtered_df[[selected_meteorology, selected_pollutant]])

# Correlation line plot
st.write('Correlation Line Plot:')
plt.figure(figsize=(8, 6))
sns.regplot(x=filtered_df[selected_meteorology].astype(float), y=filtered_df[selected_pollutant].astype(float))
plt.xlabel(selected_meteorology)
plt.ylabel(selected_pollutant)
plt.title(f'Correlation: {correlation:.2f}')
st.pyplot(plt)
