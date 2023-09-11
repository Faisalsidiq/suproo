import streamlit as st
import pandas as pd
from datetime import datetime, time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import pickle
from statsmodels.tsa.arima.model import ARIMA

# Function to preprocess data
def preprocess_data(df):
    for column in df.columns:
        df[column] = df[column].apply(preprocess_value)
        df[column] = pd.to_numeric(df[column], errors='coerce', downcast='integer')
    return df

def preprocess_value(value):
    if value == '#NUM!':
        return random.randint(0, 100)
    return value

# Function to load and preprocess data
def load_and_preprocess_data(csv_url):
    df = pd.read_csv(csv_url, parse_dates=[['Date', 'Time']])
    df = df.applymap(preprocess_value)
    return df

def predict_arima(selected_variable, model_fit):
    # Ambil data dari kolom yang dipilih
    selected_data = filtered_df[selected_variable]
    
    # Lakukan prediksi menggunakan model ARIMA
    predictions = model_fit.forecast(steps=len(selected_data))
    
    return predictions

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
    
    # Check if the selected_variabel1 is one of the variables to predict with ARIMA
    arima_variables = ['CO', 'SO2', 'O3', 'NO2', 'HC', 'PM1p0', 'PM2p5', 'PM10']
    if selected_variabel1 in arima_variables:
        # Run ARIMA prediction
        predictions = predict_arima(df[selected_variabel1])

        # Display ARIMA predictions
        st.subheader(f"Prediksi {selected_variabel1} untuk 7 hari ke depan:")
        for prediction in predictions:
            st.write(f'Prediksi: {prediction:.2f}')
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

elif selected_tool == 'Statistics':
    st.write('Statistics tool selected')
    
    # Option to show bar plot of mean of all columns
    show_mean_bar_plot = st.sidebar.checkbox('Show Mean Bar Plot')
    if show_mean_bar_plot:
        mean_values = filtered_df.mean()
        st.write("Mean Values:")
        st.write(mean_values)

        fig_mean = go.Figure(df=[go.Bar(x=mean_values.index, y=mean_values.values)])
        fig_mean.update_layout(title='Mean Values of Variabels', xaxis_title='Variabels', yaxis_title='Mean Value')
        st.plotly_chart(fig_mean)

    # Option to show bar plot of mode of all columns
    show_mode_bar_plot = st.sidebar.checkbox('Show Mode Bar Plot')
    if show_mode_bar_plot:
        mode_values = filtered_df.mode().iloc[0]
        st.write("Mode Values:")
        st.write(mode_values)

        fig_mode = go.Figure(df=[go.Bar(x=mode_values.index, y=mode_values.values)])
        fig_mode.update_layout(title='Mode Values of Variabels', xaxis_title='Variabels', yaxis_title='Mode Value')
        st.plotly_chart(fig_mode)

if selected_tool == 'Correlation':
    st.subheader('ARIMA Prediction')
    
    # Muat model ARIMA yang sesuai
    with open(f'arima_model_{selected_variabel1}.pkl', 'rb') as model_file:
        model_fit = pickle.load(model_file)

    # Lakukan prediksi menggunakan model ARIMA
    predictions = predict_arima(selected_variabel1, model_fit)
    
    # Tampilkan hasil prediksi
    st.write(f'ARIMA Predictions for {selected_variabel1}:')
    st.write(predictions)






