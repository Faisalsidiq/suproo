import streamlit as st
import pandas as pd
from datetime import datetime, time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA



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
    
    # Select columns for Variabel1 and Variabel2
    all_columns = df.columns[2:]  # Exclude Date and Time columns
    selected_variabel1 = st.sidebar.selectbox('Select Variabel1', all_columns, key='corr_variabel1')
    selected_variabel2 = st.sidebar.selectbox('Select Variabel2', all_columns, key='corr_variabel2')
    
    # Create line plot for the correlation between selected Variabel1 and Variabel2 using Plotly
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=filtered_df['Date_Time'], y=filtered_df[selected_variabel1], mode='lines', name=selected_variabel1), secondary_y=False)
    fig.add_trace(go.Scatter(x=filtered_df['Date_Time'], y=filtered_df[selected_variabel2], mode='lines', name=selected_variabel2), secondary_y=True)
    
    # Update the layout with titles and y-axis labels
    fig.update_layout(
        title=f'Correlation between {selected_variabel1} and {selected_variabel2}',
        xaxis_title='Time',
        yaxis=dict(title=selected_variabel1, side='left'),
        yaxis2=dict(title=selected_variabel2, side='right')
    )
    
    # Display the correlation line plot
    st.plotly_chart(fig)


    # Calculate the correlation coefficient between the selected Variabel1 and Variabel2
    if not filtered_df.empty and selected_variabel1 in filtered_df.columns and selected_variabel2 in filtered_df.columns:
        correlation_df = filtered_df[[selected_variabel1, selected_variabel2]].corr()
        if not correlation_df.empty and correlation_df.shape[0] > 1 and correlation_df.shape[1] > 1:
            correlation_coefficient = correlation_df.iloc[0, 1]
            # Display the correlation coefficient
            st.write("Correlation Coefficient:", correlation_coefficient)

            
                    
        else:
            st.write("Not enough data for correlation calculation.")
    else:
        st.write("No data available for correlation calculation.")

    
    df.set_index('Date_Time', inplace=True)
    # selected_variabel1 predictions
    st.title(f"Prediksi {selected_variabel1} 7 Hari Kedepan")
    df[selected_variabel1] = pd.to_numeric(df[selected_variabel1], errors='coerce', downcast='integer')
    selected_variabel1 = df[selected_variabel1]
    train_size = int(len(selected_variabel1) * 0.8)
    train, test = selected_variabel1[:train_size], selected_variabel1[train_size:]
    p, d, q = 5, 1, 0
    model = ARIMA(train, order=(p, d, q))
    model_fit = model.fit()
    # Predict selected_variabel1 values for the next 7 days
    predictions = model_fit.forecast(steps=7)
            
    # Create date range for predictions
    prediction_dates = pd.date_range(start=selected_variabel1.index[train_size], periods=len(predictions), freq='D')
            
    # Print selected_variabel1 predictions for each day
    for date, prediction in zip(prediction_dates, predictions):
        st.write(f'Tanggal: {date.date()}, Prediksi {selected_variabel1.name}: {prediction:.2f}')

    st.title(f"Prediksi {selected_variabel2} 7 Hari Kedepan")
    df[selected_variabel2] = pd.to_numeric(df[selected_variabel2], errors='coerce', downcast='integer')
    selected_variabel2 = df[selected_variabel2]
    train_size = int(len(selected_variabel2) * 0.8)
    train, test = selected_variabel2[:train_size], selected_variabel2[train_size:]
    p, d, q = 5, 1, 0
    model = ARIMA(train, order=(p, d, q))
    model_fit = model.fit()
    # Predict selected_variabel2 values for the next 7 days
    predictions = model_fit.forecast(steps=7)
            
    # Create date range for predictions
    prediction_dates = pd.date_range(start=selected_variabel2.index[train_size], periods=len(predictions), freq='D')
            
    # Print selected_variabel2 predictions for each day
    for date, prediction in zip(prediction_dates, predictions):
        st.write(f'Tanggal: {date.date()}, Prediksi {selected_variabel2.name}: {prediction:.2f}')


     
 
elif selected_tool == 'Statistics':
    st.write('Statistics tool selected')
    
    # Option to show bar plot of mean of all columns
    show_mean_bar_plot = st.sidebar.checkbox('Show Mean Bar Plot')
    if show_mean_bar_plot:
        mean_values = filtered_df.mean()
        st.write("Mean Values:")
        st.write(mean_values)

        fig_mean = go.Figure(data=[go.Bar(x=mean_values.index, y=mean_values.values)])
        fig_mean.update_layout(title='Mean Values of Variabels', xaxis_title='Variabels', yaxis_title='Mean Value')
        st.plotly_chart(fig_mean)

    # Option to show bar plot of mode of all columns
    show_mode_bar_plot = st.sidebar.checkbox('Show Mode Bar Plot')
    if show_mode_bar_plot:
        mode_values = filtered_df.mode().iloc[0]
        st.write("Mode Values:")
        st.write(mode_values)

        fig_mode = go.Figure(data=[go.Bar(x=mode_values.index, y=mode_values.values)])
        fig_mode.update_layout(title='Mode Values of Variabels', xaxis_title='Variabels', yaxis_title='Mode Value')
        st.plotly_chart(fig_mode)
