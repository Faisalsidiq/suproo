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


# Fungsi untuk memprediksi kolom tertentu
def predict_column(column_name):
    # Mengonversi kolom menjadi tipe data numerik
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce', downcast='integer')
    column_data = df[column_name]
    
    train_size = int(len(column_data) * 0.8)
    train, test = column_data[:train_size], column_data[train_size:]

    p, d, q = 5, 1, 0
    model = ARIMA(train, order=(p, d, q))
    model_fit = model.fit()

    # Memprediksi nilai kolom per hari dalam periode pengujian
    predictions = model_fit.forecast(steps=7)

    # Membuat rentang waktu harian untuk prediksi
    start_date = column_data.index[train_size]  # Tanggal data pengujian terakhir
    prediction_dates = pd.date_range(start=start_date, periods=7, freq='D')

    # Mencetak prediksi kolom untuk setiap hari dalam satu minggu ke depan
    prediction_result = []
    for date, prediction in zip(prediction_dates, predictions):
        prediction_result.append(f'Tanggal: {date.date()}, Prediksi {column_name}: {prediction:.2f}')
    
    return prediction_result

# UI Streamlit
st.title("Prediksi Data Time Series")
selected_column = st.selectbox("Pilih kolom yang ingin diolah:", df.columns)

if st.button("Prediksi"):
    st.write(f"Hasil Prediksi untuk Kolom '{selected_column}':")
    predictions = predict_column(selected_column)
    st.write(predictions)
