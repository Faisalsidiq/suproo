import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import pickle


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
    
# Baca data dari sumber Anda (misalnya, file CSV)
# Load data based on the selected dataset
if selected_dataset == 'Dataset 1':
    csv_url = "https://docs.google.com/spreadsheets/d/1tjFxtP6AiQ2xZ927yGs1kCB5Cg9OSNeWA-McsX5Bxq8/export?format=csv"
    df = load_and_preprocess_data(csv_url)
else:
    csv_url = "https://docs.google.com/spreadsheets/d/1evsslVMH2fx8EUEjDqS0PA0JzBsSdo1jVG4ddmq4dE4/export?format=csv"
    df = load_and_preprocess_data(csv_url)

# Lakukan pra-pemrosesan data jika diperlukan
df['Datetime'] = pd.to_datetime(df['Datetime'])
df.set_index('Datetime', inplace=True)

# Spesifikasi parameter ARIMA (p, d, q)
p, d, q = 5, 1, 0

# List semua kolom yang ingin Anda latih
kolom_latih = ['CO', 'SO2', 'O3', 'NO2', 'HC', 'PM1p0', 'PM2p5', 'PM10']

# Melatih model ARIMA dan menyimpannya untuk setiap kolom
for kolom in kolom_latih:
    model = ARIMA(data[kolom], order=(p, d, q))
    model_fit = model.fit()

    # Simpan model ke dalam file dengan nama yang sesuai dengan kolom
    nama_file_model = f'arima_model_{kolom.lower()}.pkl'
    with open(nama_file_model, 'wb') as model_file:
        pickle.dump(model_fit, model_file)
