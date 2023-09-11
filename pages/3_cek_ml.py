import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Membaca data dari Google Sheets
url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"
df = pd.read_csv(url)

# Menambahkan kolom Datetime
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df = df.drop(['Date', 'Time'], axis=1)
df.set_index('Datetime', inplace=True)


st.title("Prediksi SO2 dengan Model ARIMA")

# CO predictions
df['SO2'] = pd.to_numeric(df['SO2'], errors='coerce', downcast='integer')
SO2 = df['SO2']

train_size = int(len(SO2) * 0.8)
train, test = SO2[:train_size], SO2[train_size:]

p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()

# Predict SO2 values for the next 7 days
predictions = model_fit.forecast(steps=7)

# Create date range for predictions
prediction_dates = pd.date_range(start=SO2.index[train_size], periods=len(predictions), freq='D')

# Print SO2 predictions for each day
st.subheader("Prediksi SO2 untuk 7 hari ke depan:")
for date, prediction in zip(prediction_dates, predictions):
    st.write(f'Tanggal: {date.date()}, Prediksi SO2: {prediction:.2f}')
