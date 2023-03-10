import csv
from datetime import datetime 
import math

capital = 100000000
icap = capital


position_ticker = {}
profitable_trades = []
loss_making_trades = []

flag = True

start_date = datetime.today()
end_date = datetime.today()

# opening the CSV file
ticker = 'RELIANCE'
with open('writing/actions' + ticker + '.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    for trade in csvFile:
        #housekeeping stuff, initialising variable and bringing to the correct datatype
        ticker, datetimeobj, action, qty, price, total_val, capital_left, trade_type = trade
        if datetimeobj == 'Date':
            continue

        qty = int(qty)
        price = float(price)
        total_val = float(total_val)
        capital_left = float(capital_left)

        if trade_type == 'True':
            trade_type = True
        else:
            trade_type = False

        date = datetime.strptime(datetimeobj, "%Y-%m-%d %H:%M:%S")
        if flag:
            start_date = date
            end_date = date
            flag = False

        if date > end_date:
            end_date = date

        if total_val == 0: #ensuring it was a legit trade
            continue    

        if action == 'BOUGHT':
            capital -= total_val

            if trade_type == False:
                trade_profit = (float(position_ticker[ticker][5]) - total_val)
                profit_percentage = trade_profit*100/total_val
                if trade_profit > 0:
                    profitable_trades.append(trade_profit)
                else:
                    loss_making_trades.append(trade_profit)
                    
                position_ticker.pop(ticker)
            else:
                position_ticker[ticker] = trade
        
        else:
            capital += total_val
            
            if trade_type == True:
                trade_profit = (total_val - float(position_ticker[ticker][5]))
                profit_percentage = trade_profit*100/float(position_ticker[ticker][5])
                if trade_profit > 0:
                    profitable_trades.append(trade_profit)
                else:
                    loss_making_trades.append(trade_profit)
                    
                position_ticker.pop(ticker)


##calculating all stats:
no_proftable_trades = len(profitable_trades)
no_loss_making_trades = len(loss_making_trades)
no_total_trades = no_loss_making_trades+no_proftable_trades
win_rate = no_proftable_trades/no_total_trades

total_profits = 0
avg_profit_per_trade = 0 #only if the trade is profitable
total_loss = 0
avg_loss_per_trade = 0 #only if the trade is loss making

for i in profitable_trades:
    total_profits += i

for i in loss_making_trades:
    total_loss += i

avg_loss_per_trade = total_loss/no_loss_making_trades
avg_profit_per_trade = total_profits/no_proftable_trades

final_val = capital

equity = 0

for i in position_ticker:
    equity += position_ticker[i].total_val

final_val += equity
final_profit = final_val - icap

dtstart = start_date
dtend = end_date
total_days = int((dtend - dtstart).days)

expectancy = win_rate*avg_profit_per_trade + (1 - win_rate)*avg_loss_per_trade

total_loss_profit_perc = 0
for i in loss_making_trades + profitable_trades:
    total_loss_profit_perc += i

ror = total_loss_profit_perc/no_total_trades #what is ror

# cagr = ((math.pow(((final_val)/icap),365/total_days)) - 1)*100
cagr = (final_val/icap)*100
print(final_val)
risk_reward_ratio = total_profits/total_loss


print('BACKTEST START DATE: ', start_date)
print('BACKTEST END DATE: ', end_date)
print('TOTAL DAYS: ', total_days)
print('FINAL PROFIT: ', final_profit)
print('TOTAL TRADES: ', no_total_trades)
print('PROFITABLE TRADES: ', no_proftable_trades)
print('LOSS MAKING TRADES: ', no_loss_making_trades)
print('WIN RATE: ', win_rate)
print('AVG PROFIT PER TRADE: ', avg_profit_per_trade)
print('AVG LOSS PER TRADE: ', avg_loss_per_trade)
print('RISK REWARD RATIO: ', risk_reward_ratio)
print('EXPECTANCY: ', expectancy)
print('AVERAGE ROR PER TRADE: (%)', ror)
# print('MAX DRAWDOWN: ', max_drawdown)
# print('MAX DRAWDOWN PERCENTAGE: ', max_drawdown_perc)
print('AVG ANNUALISED RETURNS (%): ', cagr)