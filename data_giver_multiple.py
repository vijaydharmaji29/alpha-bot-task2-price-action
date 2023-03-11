import os

import pandas as pd
import data_collection as dc

# tickers = os.listdir('big_data/')
print('GETTING STOCK DATA')

#getting data for all stocks in the timeframe
# stock_data = dc.get_data(ticker)

def next(ticker, index):
    stock_data = pd.read_csv('df_csv/data' + ticker + '.csv') #getting data directly from stored data

    if index >= len(stock_data):
        return None

    return stock_data.iloc[index], data

if __name__ == '__main__':
    print('STARTING')
    print(type(next(20)))
    print(next(40))