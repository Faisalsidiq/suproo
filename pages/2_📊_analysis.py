import streamlit as st
import pandas as pd
from datetime import datetime, time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

logo = "logo.png"
# Display the logo image
st.image(logo, width=200)  # Adjust the width as needed

# URL to the Google Sheets CSV export link
csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"
# Load CSV data using pandas and parse date and time columns
df = pd.read_csv(csv_url, parse_dates=[['Date', 'Time']])

# Preprocess function to replace #NUM! values with random integers
def preprocess_value(value):
    if value == '#NUM!':
        return random.randint(0, 100)
    return value

# Apply preprocessing function to the entire DataFrame
df = df.applymap(preprocess_value)

# Display tools content
st.title('Analysis Tools')

# Select pollutant columns (B to H) and meteorology columns (I to P)
pollutant_columns = df.columns[3:11]  # Assuming pollutant columns start from index 2
meteorology_columns = df.columns[1:3]  # Assuming meteorology columns start from index 9

# Sidebar inputs
selected_pollutant = st.sidebar.selectbox('Select Pollutant', pollutant_columns)
selected_meteorology = st.sidebar.selectbox('Select Meteorology Data', meteorology_columns)

# Start and end date inputs
start_date = st.sidebar.date_input('Start Date', min_value=df['Date_Time'].min().date(), max_value=df['Date_Time'].max().date(), value=df['Date_Time'].min().date())
end_date = st.sidebar.date_input('End Date', min_value=df['Date_Time'].min().date(), max_value=df['Date_Time'].max().date(), value=df['Date_Time'].max().date())

# Hour and minute range inputs
start_hour = st.sidebar.selectbox('Start Hour', range(24), 0)
start_minute = st.sidebar.selectbox('Start Minute', range(0, 60, 30), 0, format_func=lambda x: f'{x:02d}')
end_hour = st.sidebar.selectbox('End Hour', range(24), 23)
end_minute = st.sidebar.selectbox('End Minute', range(0, 60, 30), 1, format_func=lambda x: f'{x:02d}')

# Create start and end datetime objects
start_datetime = datetime.combine(start_date, time(start_hour, start_minute))
end_datetime = datetime.combine(end_date, time(end_hour, end_minute))

# Filter data based on selected date and time range
filtered_df = df[(df['Date_Time'] >= start_datetime) & (df['Date_Time'] <= end_datetime)]

# Create line plot for the correlation between selected pollutant and meteorology data using Plotly
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=filtered_df['Date_Time'], y=filtered_df[selected_pollutant], mode='lines', name=selected_pollutant), secondary_y=False)
fig.add_trace(go.Scatter(x=filtered_df['Date_Time'], y=filtered_df[selected_meteorology], mode='lines', name=selected_meteorology), secondary_y=True)

# Update the layout with titles and y-axis labels
fig.update_layout(
    title=f'Correlation between {selected_pollutant} and {selected_meteorology}',
    xaxis_title='Time',
    yaxis=dict(title=selected_pollutant, side='left'),
    yaxis2=dict(title=selected_meteorology, side='right')
)

# Display the correlation line plot
st.plotly_chart(fig)

