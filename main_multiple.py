# import data_giver_multiple as dg
import pandas as pd
import brain
import executioner
import csv
import os

icap = 100000000

def run(ticker):
    global icap
    capital = icap
    positions = []
    all_actions = []

    index = 0
    data = pd.read_csv('df_csv/data' + ticker + '.csv')

    while index < len(data):
        # next, data = dg.next(ticker, index) #getting data for next trading session
        
        if index >= len(data):
            next = None
        
        next = data.iloc[index]

        index += 1

        #checking if valid trading session
        if type(next) != pd.core.series.Series:
            break

        #continuing if valid trading session
        execute = brain.calculate(next, positions, capital)
        
        if len(execute) > 0:
            all_actions.extend(execute)
            capital, positions = executioner.trade(execute, capital, positions)
            # print(positions)

    print(capital)

    return all_actions

def write_actions(ticker, all_actions):
    fields = ['Ticker', 'Date', 'Action', 'Quantity', 'Price', 'Total Value', 'Capital Left', 'Trade Type']
    all_actions_list = []
    capital_left = icap

    for a in all_actions:
        action = 'BOUGHT'
        
        if a.sell:
            action = 'SOLD'
            capital_left += a.price*a.qty
        else:
            capital_left -= a.price*a.qty
            
        new_row = (a.ticker, a.date, action, a.qty, a.price, a.qty*a.price, capital_left, a.trade_type)
        all_actions_list.append(new_row)

    with open('writing/actions' + ticker + '.csv', 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

         # writing the fields
        csvwriter.writerow(fields)
        
        # writing the data rows
        csvwriter.writerows(all_actions_list)

    all_actions_refined = []
    fields_refined = ['Date', 'Outcome', 'Time of Entry', 'Option Symbol', 'Entry Price', 'Exit Price', 'Time of Exit', 'Quantity', 'SL', 'PnL', 'Cumulative PnL', 'Equity']

    timeofentry = 0
    entryprice = 0
    total_pnl = 0

    capital_left = icap

    for a in all_actions:
        if (a.sell and a.trade_type == True) or (a.buy and a.trade_type == False): #sold long or bought short
            date = a.date
            qty = a.qty
            timeofexit = a.date[11:]
            exitprice = a.price
            optionticker = a.ticker
            SL = None

            if a.trade_type:
                profit = (exitprice - entryprice)*qty
            else:
                profit = (entryprice - exitprice)*qty

            total_pnl += profit

            if a.sell:
                capital_left += qty*exitprice
            else:
                capital_left -= qty*exitprice

            if a.trade_type:
                outcome = 'LONG'
            else:
                outcome = 'SHORT'

            new_row = (date, outcome, timeofentry, optionticker, entryprice, exitprice, timeofexit, qty, SL, profit, total_pnl, capital_left)
            all_actions_refined.append(new_row)
        else:
            timeofentry = a.date[11:]
            entryprice = a.price

            if a.sell:
                capital_left += a.qty*entryprice
            else:
                capital_left -= a.qty*entryprice


    with open('refined_writing/actions' + ticker + '.csv', 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

         # writing the fields
        csvwriter.writerow(fields_refined)
        
        # writing the data rows
        csvwriter.writerows(all_actions_refined)


if __name__ == '__main__':
    files = os.listdir('df_csv/')
    for f in files:
        t = f[4:-4]
        print('WRITING -', t)
        icap = 100000000
        all_actions = run(t)
        write_actions(t, all_actions)
        print('DONE -', t)