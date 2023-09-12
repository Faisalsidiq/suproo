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


# SO2 predictions
st.title("Prediksi SO2 dengan Model ARIMA")
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


# CO predictions
st.title("Prediksi CO dengan Model ARIMA")
df['CO'] = pd.to_numeric(df['CO'], errors='coerce', downcast='integer')
CO = df['CO']
train_size = int(len(CO) * 0.8)
train, test = CO[:train_size], CO[train_size:]
p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()
# Predict CO values for the next 7 days
predictions = model_fit.forecast(steps=7)

# Create date range for predictions
prediction_dates = pd.date_range(start=CO.index[train_size], periods=len(predictions), freq='D')

# Print CO predictions for each day
st.subheader("Prediksi CO untuk 7 hari ke depan:")
for date, prediction in zip(prediction_dates, predictions):
    st.write(f'Tanggal: {date.date()}, Prediksi CO: {prediction:.2f}')


# O3 predictions
st.title("Prediksi O3 dengan Model ARIMA")
df['O3'] = pd.to_numeric(df['O3'], errors='coerce', downcast='integer')
O3 = df['O3']

train_size = int(len(O3) * 0.8)
train, test = O3[:train_size], O3[train_size:]
p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()
# Predict O3 values for the next 7 days
predictions = model_fit.forecast(steps=7)

# Create date range for predictions
prediction_dates = pd.date_range(start=O3.index[train_size], periods=len(predictions), freq='D')

# Print O3 predictions for each day
st.subheader("Prediksi O3 untuk 7 hari ke depan:")
for date, prediction in zip(prediction_dates, predictions):
    st.write(f'Tanggal: {date.date()}, Prediksi O3: {prediction:.2f}')
    
    
    
