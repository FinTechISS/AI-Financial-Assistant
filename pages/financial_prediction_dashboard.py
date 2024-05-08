import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Forecasting Data 

Select a category and corresponding options to see data.
""")

categories = {
    'Stocks': ['GOOGL - Alphabet', 'AAPL - Apple', 'MSFT - Microsoft', 'AMZN - Amazon', 'META - Meta', 'TSLA - Tesla', 'NFLX - Netflix', 'NVDA - Nvidia', 'BABA - Alibaba', 'IBM - IBM'],
    'Options': ['AAPL - Apple'],
    'Cryptocurrencies': ['BTC-USD - Bitcoin', 'ETH-USD - Ethereum', 'XRP-USD - Ripple', 'LTC-USD - Litecoin', 'BCH-USD - Bitcoin Cash'],
    'Natural Resources': ['GC=F - Gold', 'SI=F - Silver', 'CL=F - Crude Oil', 'NG=F - Natural Gas', 'HG=F - Copper']
}

category = st.selectbox('Select Category:', list(categories.keys()))

ticker_selection = st.selectbox('Select Ticker:', categories[category])
ticker = ticker_selection.split(' - ')[0]  # Extract the ticker symbol

start_date = st.date_input('Start Date', value=pd.Timestamp('2024-05-08'))
end_date = st.date_input('End Date', value=pd.Timestamp('2024-06-08'))
    
# Fetch data

if category == 'Options':
    ticker_data = pd.read_csv(f'./docs/merged.csv')
else:
    ticker_data = yf.Ticker(ticker)
    
hist_data = ticker_data.history(start='2024-04-08', end='2024-05-08')

if category in ['Stocks', 'Cryptocurrencies', 'Natural Resources']:
    st.write(f"## Closing Price of {ticker_selection}")
    st.line_chart(hist_data['Close'])
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
