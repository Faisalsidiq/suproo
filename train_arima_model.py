from statsmodels.tsa.arima.model import ARIMA
import pickle

# Melatih dan fit model ARIMA
p, d, q = 5, 1, 0
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()

# Menyimpan model ke dalam file
with open('arima_model.pkl', 'wb') as model_file:
    pickle.dump(model_fit, model_file)
