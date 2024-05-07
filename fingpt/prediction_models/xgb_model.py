import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
import matplotlib.pyplot as plt

def get_data (stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    columns_to_use = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    data = stock_data[columns_to_use]
    return data

scaler = MinMaxScaler(feature_range=(0.1, 1))
scaler_y = MinMaxScaler(feature_range=(0.1, 1))

def scale_data(data):
    
    data_scaled = scaler.fit_transform(data)
    
    y = scaler_y.fit_transform(data[['Adj Close']])

    X = [data_scaled[i][:5] for i in range(len(data_scaled))]
    X, y = np.array(X), np.array(y)
    return X, y

def modelf(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

    params = {
        'max_depth': 3,
        'eta': 0.1,
        'objective': 'reg:squarederror',
        'eval_metric': 'rmse'
    }

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    evals_result = {}
    num_rounds = 100
    bst = xgb.train(params, dtrain, num_rounds, evals=[(dtrain, 'train'), (dtest, 'eval')], evals_result=evals_result)
    return bst

def predict(stock_symbol, start_date, end_date, dataset):
    data = get_data(stock_symbol, start_date, end_date)
    X, y = scale_data(data)
    bst = modelf(X, y)
    y_test_pred = bst.predict(dataset)
    y_test_pred_actual = scaler_y.inverse_transform(y_test_pred.reshape(-1, 1))
    return y_test_pred_actual
