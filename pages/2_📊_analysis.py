import streamlit as st
import pandas as pd
from datetime import datetime, time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# Function to preprocess data
def preprocess_value(value):
    if value == '#NUM!':
        return random.randint(0, 100)
    return value

# Function to load and preprocess data
def load_and_preprocess_data(csv_url):
    df = pd.read_csv(csv_url, parse_dates=[['Date', 'Time']])
    df = df.applymap(preprocess_value)
    return df

# Sidebar options
st.sidebar.title('Options')
selected_dataset = st.sidebar.selectbox('Select Dataset', ['Dataset 1', 'Dataset 2'])

# Load data based on the selected dataset
if selected_dataset == 'Dataset 1':
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"
    df = load_and_preprocess_data(csv_url)
else:
    csv_url = "https://docs.google.com/spreadsheets/d/1evsslVMH2fx8EUEjDqS0PA0JzBsSdo1jVG4ddmq4dE4/export?format=csv"
    df = load_and_preprocess_data(csv_url)

st.title('Air Pollution Data Analysis')

# Display tools content
st.subheader('Tools')

# Sidebar options
selected_tool = st.selectbox('Select Tool', ['Correlation', 'Statistics'])

# Filter data based on date and time
start_date = st.sidebar.date_input('Start Date', min_value=df['Date_Time'].min().date(), max_value=df['Date_Time'].max().date(), value=df['Date_Time'].min().date())
end_date = st.sidebar.date_input('End Date', min_value=df['Date_Time'].min().date(), max_value=df['Date_Time'].max().date(), value=df['Date_Time'].max().date())

start_hour = st.sidebar.selectbox('Start Hour', range(24), 0, key='start_hour')
start_minute = st.sidebar.selectbox('Start Minute', range(60), 0, key='start_minute')
end_hour = st.sidebar.selectbox('End Hour', range(24), 23, key='end_hour')
end_minute = st.sidebar.selectbox('End Minute', range(60), 59, key='end_minute')

start_datetime = datetime.combine(start_date, time(start_hour, start_minute))
end_datetime = datetime.combine(end_date, time(end_hour, end_minute))

filtered_df = df[(df['Date_Time'] >= start_datetime) & (df['Date_Time'] <= end_datetime)]

# Display selected dataset and date/time range
st.write(f'Selected Dataset: {selected_dataset}')
st.write(f'Date/Time Range: {start_datetime} to {end_datetime}')

if selected_tool == 'Correlation':
    st.write('Correlation tool selected')
    
    # Select pollutant columns (B to H) and meteorology columns (I to P)
    pollutant_columns = df.columns[3:12]  # Assuming pollutant columns start from index 2
    meteorology_columns = df.columns[1:3]  # Assuming meteorology columns start from index 9
    
    # Sidebar inputs
    selected_pollutant = st.sidebar.selectbox('Select Pollutant', pollutant_columns, key='corr_pollutant')
    selected_meteorology = st.sidebar.selectbox('Select Meteorology Data', meteorology_columns, key='corr_meteorology')
    
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

    # Calculate the correlation coefficient between the selected pollutant and meteorology data
    if not filtered_df.empty and selected_pollutant in filtered_df.columns and selected_meteorology in filtered_df.columns:
        correlation_df = filtered_df[[selected_pollutant, selected_meteorology]].corr()
        if not correlation_df.empty and correlation_df.shape[0] > 1 and correlation_df.shape[1] > 1:
            correlation_coefficient = correlation_df.iloc[0, 1]
            # Display the correlation coefficient
            st.write("Correlation Coefficient:", correlation_coefficient)
        else:
            st.write("Not enough data for correlation calculation.")
    else:
        st.write("No data available for correlation calculation.")

elif selected_tool == 'Statistics':
    st.write('Statistics tool selected')
    pollutant_columns = df.columns[3:12]  # Assuming pollutant columns start from index 2
    meteorology_columns = df.columns[1:3]  # Assuming meteorology columns start from index 9
    
    # Option to show bar plot of mean of all pollutants
    show_mean_bar_plot = st.sidebar.checkbox('Show Mean Bar Plot')
    if show_mean_bar_plot:
        mean_values = filtered_df[pollutant_columns].mean()
        st.write("Mean Values:")
        st.write(mean_values)

        fig_mean = go.Figure(data=[go.Bar(x=mean_values.index, y=mean_values.values)])
        fig_mean.update_layout(title='Mean Values of Pollutants', xaxis_title='Pollutants', yaxis_title='Mean Value')
        st.plotly_chart(fig_mean)

    # Option to show bar plot of mode of all pollutants
    show_mode_bar_plot = st.sidebar.checkbox('Show Mode Bar Plot')
    if show_mode_bar_plot:
        mode_values = filtered_df[pollutant_columns].mode().iloc[0]
        st.write("Mode Values:")
        st.write(mode_values)

        fig_mode = go.Figure(data=[go.Bar(x=mode_values.index, y=mode_values.values)])
        fig_mode.update_layout(title='Mode Values of Pollutants', xaxis_title='Pollutants', yaxis_title='Mode Value')
        st.plotly_chart(fig_mode)


