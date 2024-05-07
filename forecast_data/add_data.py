import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression

#stocks = ['GOOGL', 'AAPL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NFLX', 'NVDA', 'BABA', 'IBM']['BTC-USD', 'ETH-USD', 'XRP-USD', 'LTC-USD', 'BCH-USD']
stocks = ['GC=F', 'SI=F', 'CL=F', 'NG=F', 'HG=F']
for stock in stocks:    
    the_stock = yf.download(stock, start='2023-01-01', end='2024-05-06')

    # Drop the "Adj Close" column
    the_stock_extrapolation = the_stock.drop(columns=['Adj Close'])

    # Extrapolate the data using linear regression
    dates = pd.to_numeric(the_stock_extrapolation.index)
    extrapolated_data = pd.DataFrame(index=pd.date_range(start=the_stock_extrapolation.index[-1], periods=30))

    for column in the_stock_extrapolation.columns:
        model = LinearRegression()
        model.fit(dates.values.reshape(-1, 1), the_stock_extrapolation[column].values.reshape(-1, 1))
        future_dates_numeric = pd.to_numeric(extrapolated_data.index)
        future_values = model.predict(future_dates_numeric.values.reshape(-1, 1))
        extrapolated_data[column] = future_values.flatten()

    # Save the extrapolated data to a CSV file
    extrapolated_data.to_csv(f'{stock}_stock_extrapolated.csv')
