import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Sidebar options
st.sidebar.title('Options')
selected_dataset = st.sidebar.selectbox('Select Data ', ['CO', 'SO2','O3','NO2', 'HC]', 'PM1p0', 'PM2p5', 'PM10'])

    url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"
    df = pd.read_csv(url)

    # Menambahkan kolom Datetime
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df = df.drop(['Date', 'Time'], axis=1)
    df.set_index('Datetime', inplace=True)

    st.title("Prediksi Data dengan Model ARIMA")

    # Train ARIMA models for all columns
    p, d, q = 5, 1, 0
    models = {}

    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce', downcast='integer')
        data = df[column]

        train_size = int(len(data) * 0.8)
        train, test = data[:train_size], data[train_size:]

        model = ARIMA(train, order=(p, d, q))
        model_fit = model.fit()
        models[column] = model_fit

    # Predict data for the next 7 days for all columns
    num_periods = 7
    prediction_results = {}

    for column in df.columns:
        model_fit = models[column]
        last_date = df.index[-1]
        prediction_dates = pd.date_range(start=last_date, periods=num_periods + 1, closed='right')
        predictions = model_fit.forecast(steps=num_periods)
        prediction_results[column] = {'dates': prediction_dates[1:], 'predictions': predictions}

    # Display the predictions (You can choose to display or not)
    for column in df.columns:
        st.subheader(f"Prediksi {column} untuk 7 hari ke depan:")
        prediction_df = pd.DataFrame({'Date': prediction_results[column]['dates'], 'Prediction': prediction_results[column]['predictions']})
        st.write(prediction_df)
