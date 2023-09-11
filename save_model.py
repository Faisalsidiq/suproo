import pickle

with open('arima_model.pkl', 'rb') as model_file:
    model_fit = pickle.load(model_file)
