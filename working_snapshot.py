import os
import yfinance as yf

with open('python-finance/symbols.csv') as f:
    lines = f.read().splitlines()
    # print(lines)
    # print(type(lines))
    for symbol in lines:
        print(symbol)
        data = yf.download(symbol, start='2019-01-01', end='2020-11-30')
        data.to_csv('python-finance/datasets/{}.csv'.format(symbol))