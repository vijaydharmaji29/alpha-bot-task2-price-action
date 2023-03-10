import os

import pandas as pd
import data_collection as dc

# tickers = os.listdir('big_data/')

print('GETTING STOCK DATA')

#getting data for all stocks in the timeframe
#stock_data = dc.get_data(ticker)
stock_data = pd.read_csv('df_csv/dataRELIANCE.csv') #getting data directly from stored data

def next(index):
    if index >= len(stock_data):
        return None

    return stock_data.iloc[index]

if __name__ == '__main__':
    print('STARTING')
    print(type(next(20)))
    print(next(40))