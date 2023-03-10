class position(object):
    def __init__(self, ticker, qty, price, trade_type):
        self.ticker = ticker
        self.qty = qty
        self.price = price
        self.trade_type = trade_type #shorting (false) or longing (true)


def trade(execute, capital, positions):
    positions = positions
    capital = capital

    for e in execute:
        #buying a stock - long
        if e.buy and e.trade_type:
            new_pos = position(e.ticker, e.qty, e.price, e.trade_type)
            positions.append(new_pos)
            capital -= e.qty*e.price

        elif e.sell and e.trade_type:
            positions.pop()
            capital += e.qty*e.price

    return capital, positions