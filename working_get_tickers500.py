import bs4 as bs
import pickle
import requests

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

save_sp500_tickers()