from prediction_models.xgb_model import predict
import pandas as pd
import xgboost as xgb

elements = ['GOOGL', 'AAPL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'BABA', 'IBM', 'BTC-USD',
            'ETH-USD', 'XRP-USD', 'LTC-USD', 'BCH-USD', 'GC=F', 'SI=F', 'CL=F', 'NG=F', 'HG=F']

start_date = "1980-01-01"

end_date = "2024-05-07"

for element in elements:

    current_db = pd.read_csv(f'../docs/{element}_stock_extrapolated.csv')
    
    # Remove non-numeric columns
    current_db.drop(columns=['Unnamed: 0'], inplace=True)
    
    # Convert DataFrame to DMatrix
    dmatrix = xgb.DMatrix(data=current_db)
    
    # Make predictions
    predictions = predict(element, start_date, end_date, dmatrix)
    
    # Assign predictions to the DataFrame
    current_db['Adj Close'] = predictions
    
    # Save DataFrame to CSV, overwriting the existing file
    current_db.to_csv(f'../docs/{element}_stock_extrapolated.csv', index=False, mode='w')
