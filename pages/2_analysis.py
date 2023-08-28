import streamlit as st
import gspread
import pandas as pd



df = pd.DataFrame(data, columns=data[0])
df = df[1:]  # Exclude the header row

# Sidebar options
st.sidebar.header('Options')
selected_date = st.sidebar.date_input('Select a date', pd.to_datetime(df['Date']).dt.date.unique())
selected_time = st.sidebar.selectbox('Select a time', pd.to_datetime(df['Time']).dt.time.unique())
selected_meteorology = st.sidebar.selectbox('Select meteorology column', ['Temperature', 'Humidity'])
selected_pollutant = st.sidebar.selectbox('Select pollutant column', ['Pollutant 1', 'Pollutant 2', 'Pollutant 3'])

# Filter data based on user selection
filtered_df = df[(pd.to_datetime(df['Date']).dt.date == selected_date) & 
                 (pd.to_datetime(df['Time']).dt.time == selected_time)]

# Main content
st.title('Google Sheets Data Viewer')
st.write('Selected Data:')
st.write(f'Date: {selected_date}, Time: {selected_time}')
st.write(f'Meteorology: {selected_meteorology}')
st.write(f'Pollutant: {selected_pollutant}')
st.write(filtered_df[[selected_meteorology, selected_pollutant]])

# Optionally, you can visualize the data using charts or plots here
