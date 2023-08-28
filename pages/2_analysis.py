import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# URL to the Google Sheets CSV export link
csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"
# Load CSV data using pandas and parse date and time columns
df = pd.read_csv(csv_url, parse_dates=[['Date', 'Time']])
df['Date_Time'] = pd.to_datetime(df['Date_Time'])  # Ensure the Date_Time column is in datetime format

# Sidebar options
st.sidebar.header('Options')
selected_date = st.sidebar.date_input('Select a date', df['Date_Time'].dt.date.min(), df['Date_Time'].dt.date.max())
times_for_selected_date = df[df['Date_Time'].dt.date == selected_date]['Date_Time'].dt.time.unique()
selected_time = st.sidebar.selectbox('Select a time', times_for_selected_date)
selected_meteorology = st.sidebar.selectbox('Select meteorology column', ['Temperature', 'Humidity'])
selected_pollutant = st.sidebar.selectbox('Select pollutant column', ['SO2', 'CO', 'O3', 'NO2', 'HC', 'PM1p0', 'PM2p5', 'PM10'])

# Filter data based on user selection
filtered_df = df[(df['Date_Time'].dt.date == selected_date) & (df['Date_Time'].dt.time == selected_time)]

# Ensure selected_meteorology and selected_pollutant columns contain numeric values
numeric_cols = ['Temperature', 'Humidity', 'SO2', 'CO', 'O3', 'NO2', 'HC', 'PM1p0', 'PM2p5', 'PM10']
if selected_meteorology not in numeric_cols or selected_pollutant not in numeric_cols:
    st.warning("Selected columns should be numeric for correlation calculation.")
else:
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

