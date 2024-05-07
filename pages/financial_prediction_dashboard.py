import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Forecasting Data 

Select a category and corresponding options to see data.
""")

categories = {
    'Stocks': ['GOOGL - Alphabet', 'AAPL - Apple', 'MSFT - Microsoft', 'AMZN - Amazon', 'META - Meta', 'TSLA - Tesla', 'NFLX - Netflix', 'NVDA - Nvidia', 'BABA - Alibaba', 'IBM - IBM'],
    'Options': ['AAPL - Apple','TSLA - Tesla','NVDA - Nvidia'],
    'Cryptocurrencies': ['BTC-USD - Bitcoin', 'ETH-USD - Ethereum', 'XRP-USD - Ripple', 'LTC-USD - Litecoin', 'BCH-USD - Bitcoin Cash'],
    'Natural Resources': ['GC=F - Gold', 'SI=F - Silver', 'CL=F - Crude Oil', 'NG=F - Natural Gas', 'HG=F - Copper']
}

category = st.selectbox('Select Category:', list(categories.keys()))

ticker_selection = st.selectbox('Select Ticker:', categories[category])
ticker = ticker_selection.split(' - ')[0]  # Extract the ticker symbol

period = st.selectbox('Select Period:', ['1d', '1wk'])
start_date = st.date_input('Start Date', value=pd.Timestamp('2024-07-05'))
end_date = st.date_input('End Date', value=pd.Timestamp('2024-07-06'))

if category == 'Options':
    ticker_data = pd.read_csv(f'./docs/{ticker}_option_extrapolated.csv')
else:
    ticker_data = pd.read_csv(f'./docs/{ticker}_stock_extrapolated.csv')
    
hist_data = ticker_data

if category in ['Stocks', 'Cryptocurrencies', 'Natural Resources']:
    st.write(f"## Predicted Adj Closing Price of {ticker_selection}")
    st.line_chart(hist_data['Adj Close'])
    st.write(f"## Volume of {ticker_selection}")
    st.line_chart(hist_data['Volume'])

elif category == 'Options':

    expirations = ticker_data.options  
    expiration = st.selectbox('Select Expiration Date:', expirations)
    opts = ticker_data.option_chain(expiration)
    st.write(f"## Calls for {ticker_selection}")
    st.dataframe(opts.calls[['lastTradeDate', 'strike', 'lastPrice', 'volume']])
    st.write(f"## Puts for {ticker_selection}")
    st.dataframe(opts.puts[['lastTradeDate', 'strike', 'lastPrice', 'volume']])
