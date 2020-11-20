import bs4 as bs
import pickle
import requests
import yfinance as yf
import os
import pandas as pd


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

## Build all ticker main df 
def compile_data():
    with open('python-finance/sp500tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)
    
    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv('python-finance/datasets/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
        
        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('python-finance/sp500tickers_joined.csv')

compile_data()
## add error handling to skip the missing tickers 