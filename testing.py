import bs4 as bs
import pickle
import requests
import yfinance as yf
import os
import pandas


## Save the list of 500 tickers from Wiki page
def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    #print(resp)
    soup = bs.BeautifulSoup(resp.text, features='lxml')
    #print(soup)
    table = soup.find('table', {'class':'wikitable sortable'})
    #print(table)
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text[:-1]
        tickers.append(ticker)
    
    with open('python-finance/sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)
    
    print(tickers)
    
    return tickers

## Get data for the above list from yahoo
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('python-finance/sp500tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)
    for ticker in tickers[:100]:
        if not os.path.exists('python-finance/datasets/{}.csv'.format(ticker)):
            data = yf.download(ticker, start='2000-01-01', end='2017-01-01')
            data.to_csv('python-finance/datasets/{}.csv'.format(ticker))
        else:
            print('Aleady have {}'.format(ticker))

## Get symbol data
symbol = 'AMD'
symbol_df = pandas.read_csv('python-finance/datasets/{}.csv'.format(symbol), parse_dates=True, index_col=0)
print(symbol_df)

## Get entry data from CSV
entry_df = pandas.DataFrame({'Date': ['2000-01-04'], 'AMD': ['15']}).set_index('Date')
print(entry_df)

## Set R/R parameters (Stop; Target; Risk$)
STOP = '14'
TARGET = '16'

## Compare entry against data and return Win %, R/R

        