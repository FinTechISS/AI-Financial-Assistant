import yfinance as yf
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

elements = ['GOOGL', 'AAPL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'BABA', 'IBM', 'BTC-USD',
            'ETH-USD', 'XRP-USD', 'LTC-USD', 'BCH-USD', 'GC=F', 'SI=F', 'CL=F', 'NG=F', 'HG=F']

for element in elements:    
    the_element = yf.download(element, start='2020-01-01', end='2024-05-06')
    the_element_extrapolation = the_element.drop(columns=['Adj Close'])

    extrapolated_data = pd.DataFrame(index=pd.date_range(start=the_element_extrapolation.index[-1], periods=30))

    for column in the_element_extrapolation.columns:
        # LSTM with a rolling window
        window_size = 30  # Size of the rolling window
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(window_size, 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(the_element_extrapolation[column].values.reshape(-1,1))

        for i in range(window_size, len(scaled_data)):
            X_train = np.array([scaled_data[i-window_size:i]])
            y_train = np.array([scaled_data[i]])
            model.fit(X_train, y_train, epochs=1, verbose=0)

        # Extrapolate future values
        future_values = []
        for _ in range(len(extrapolated_data)):
            x_input = np.array([scaled_data[-window_size:]])
            x_input = x_input.reshape((1, window_size, 1))  # Reshape to (batch_size, timesteps, features)
            yhat = model.predict(x_input, verbose=0)
            future_values.append(yhat[0][0])
            scaled_data = np.append(scaled_data, yhat)

        future_values = scaler.inverse_transform(np.array(future_values).reshape(-1,1))
        extrapolated_data[column] = future_values

    extrapolated_data.to_csv(f'./docs/{element}_element_extrapolated.csv')
