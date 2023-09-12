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



# NO2 predictions
st.title("Prediksi NO2 dengan Model ARIMA")
df['NO2'] = pd.to_numeric(df['NO2'], errors='coerce', downcast='integer')
NO2 = df['NO2']

train_size = int(len(NO2) * 0.8)
train, test = NO2[:train_size], NO2[train_size:]
p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()
# Predict NO2 values for the next 7 days
predictions = model_fit.forecast(steps=7)

# Create date range for predictions
prediction_dates = pd.date_range(start=NO2.index[train_size], periods=len(predictions), freq='D')

# Print NO2 predictions for each day
st.subheader("Prediksi NO2 untuk 7 hari ke depan:")
for date, prediction in zip(prediction_dates, predictions):
    st.write(f'Tanggal: {date.date()}, Prediksi NO2: {prediction:.2f}')



# HC predictions
st.title("Prediksi HC dengan Model ARIMA")
df['HC'] = pd.to_numeric(df['HC'], errors='coerce', downcast='integer')
HC = df['HC']

train_size = int(len(HC) * 0.8)
train, test = HC[:train_size], HC[train_size:]
p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()
# Predict HC values for the next 7 days
predictions = model_fit.forecast(steps=7)

# Create date range for predictions
prediction_dates = pd.date_range(start=HC.index[train_size], periods=len(predictions), freq='D')

# Print HC predictions for each day
st.subheader("Prediksi HC untuk 7 hari ke depan:")
for date, prediction in zip(prediction_dates, predictions):
    st.write(f'Tanggal: {date.date()}, Prediksi HC: {prediction:.2f}')


# PM1p0 predictions
st.title("Prediksi PM1p0 dengan Model ARIMA")
df['PM1p0'] = pd.to_numeric(df['PM1p0'], errors='coerce', downcast='integer')
PM1p0 = df['PM1p0']

train_size = int(len(PM1p0) * 0.8)
train, test = PM1p0[:train_size], PM1p0[train_size:]
p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()
# Predict PM1p0 values for the next 7 days
predictions = model_fit.forecast(steps=7)

# Create date range for predictions
prediction_dates = pd.date_range(start=PM1p0.index[train_size], periods=len(predictions), freq='D')

# Print PM1p0 predictions for each day
st.subheader("Prediksi PM1p0 untuk 7 hari ke depan:")
for date, prediction in zip(prediction_dates, predictions):
    st.write(f'Tanggal: {date.date()}, Prediksi PM1p0: {prediction:.2f}')


# PM2p5 predictions
st.title("Prediksi PM2p5 dengan Model ARIMA")
df['PM2p5'] = pd.to_numeric(df['PM2p5'], errors='coerce', downcast='integer')
PM2p5 = df['PM2p5']

train_size = int(len(PM2p5) * 0.8)
train, test = PM2p5[:train_size], PM2p5[train_size:]
p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()
# Predict PM2p5 values for the next 7 days
predictions = model_fit.forecast(steps=7)

# Create date range for predictions
prediction_dates = pd.date_range(start=PM2p5.index[train_size], periods=len(predictions), freq='D')

# Print PM2p5 predictions for each day
st.subheader("Prediksi PM2p5 untuk 7 hari ke depan:")
for date, prediction in zip(prediction_dates, predictions):
    st.write(f'Tanggal: {date.date()}, Prediksi PM2p5: {prediction:.2f}')



# PM10 predictions
st.title("Prediksi PM10 dengan Model ARIMA")
df['PM10'] = pd.to_numeric(df['PM10'], errors='coerce', downcast='integer')
PM10 = df['PM10']

train_size = int(len(PM10) * 0.8)
train, test = PM10[:train_size], PM10[train_size:]
p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()
# Predict PM10 values for the next 7 days
predictions = model_fit.forecast(steps=7)

# Create date range for predictions
prediction_dates = pd.date_range(start=PM10.index[train_size], periods=len(predictions), freq='D')

# Print PM10 predictions for each day
st.subheader("Prediksi PM10 untuk 7 hari ke depan:")
for date, prediction in zip(prediction_dates, predictions):
    st.write(f'Tanggal: {date.date()}, Prediksi PM10: {prediction:.2f}')
    
    
