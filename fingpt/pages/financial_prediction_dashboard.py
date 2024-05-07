import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Forecasting Data 

Select a category and corresponding options to see data.
""")

# Define categories and their respective tickers with readable names
categories = {
    'Stocks': ['GOOGL - Alphabet', 'AAPL - Apple', 'MSFT - Microsoft', 'AMZN - Amazon', 'META - Meta', 'TSLA - Tesla', 'NFLX - Netflix', 'NVDA - Nvidia', 'BABA - Alibaba', 'IBM - IBM'],
    'Options': ['GOOGL - Alphabet', 'AAPL - Apple', 'MSFT - Microsoft', 'AMZN - Amazon', 'META - Meta', 'TSLA - Tesla', 'NFLX - Netflix', 'NVDA - Nvidia', 'BABA - Alibaba', 'IBM - IBM'],
    'Cryptocurrencies': ['BTC-USD - Bitcoin', 'ETH-USD - Ethereum', 'XRP-USD - Ripple', 'LTC-USD - Litecoin', 'BCH-USD - Bitcoin Cash'],
    'Natural Resources': ['GC=F - Gold', 'SI=F - Silver', 'CL=F - Crude Oil', 'NG=F - Natural Gas', 'HG=F - Copper']
}

# Dropdown to select category
category = st.selectbox('Select Category:', list(categories.keys()))

# Dropdown to select ticker based on category
ticker_selection = st.selectbox('Select Ticker:', categories[category])
ticker = ticker_selection.split(' - ')[0]  # Extract the ticker symbol

# Widgets for selecting the period, start, and end date
period = st.selectbox('Select Period:', ['1d', '1wk', '1mo', '3mo', '6mo', '1y'])
start_date = st.date_input('Start Date', value=pd.Timestamp('2024-01-01'))
end_date = st.date_input('End Date', value=pd.Timestamp('2024-07-05'))

# Fetch data
ticker_data = yf.Ticker(ticker)
hist_data = ticker_data.history(period=period, start=start_date, end=end_date)

if category in ['Stocks', 'Cryptocurrencies', 'Natural Resources']:
    st.write(f"## Predicted Adj Closing Price of {ticker_selection}")
    st.line_chart(hist_data['Adj Close'])
    st.write(f"## Volume of {ticker_selection}")
    st.line_chart(hist_data['Volume'])

elif category == 'Options':
    # Get options data
    expirations = ticker_data.options  # Get available expirations
    expiration = st.selectbox('Select Expiration Date:', expirations)
    opts = ticker_data.option_chain(expiration)
    st.write(f"## Calls for {ticker_selection}")
    st.dataframe(opts.calls[['lastTradeDate', 'strike', 'lastPrice', 'volume']])
    st.write(f"## Puts for {ticker_selection}")
    st.dataframe(opts.puts[['lastTradeDate', 'strike', 'lastPrice', 'volume']])