class action(object):
    def __init__(self, ticker, qty, buy, sell, price, date, trade_type):
        self.ticker = ticker #which ticker is being traded
        self.qty = qty #qty of the ticker being bought/sold
        self.buy = buy #true if buying, false if selling
        self.sell = sell #true if selling, false if buying
        self.price = price #price of 1 qty of ticker
        self.date = date #date of trade
        self.trade_type = trade_type #True for longing, False for shorting

def calculate(session_data, positions, capital): #list of all active positions, length should be one or zero   
    execute = []
    slrl_limit = 20

    buy_signal = (session_data.close > session_data.filt) and (session_data.supports - slrl_limit < session_data.close) and (session_data.supports + slrl_limit > session_data.close)
    sell_signal = (session_data.close < session_data.filt) and (session_data.direction == -1) and (session_data.resistances - slrl_limit < session_data.close) and (session_data.resistances + slrl_limit > session_data.close)
    
    #longing stocks
    if buy_signal and len(positions) == 0:
        qty = int(capital/session_data.close)
        new_action = action(session_data.symbol, qty, True, False, session_data.close, session_data.date, True)
        execute.append(new_action)
    
    elif sell_signal and (len(positions) == 1):
        qty = positions[0].qty
        new_action = action(session_data.symbol, qty, False, True, session_data.close, session_data.date, True)
        execute.append(new_action)
    
    return execute
