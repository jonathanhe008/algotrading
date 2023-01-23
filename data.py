import urllib.request, json 
import os
import datetime as dt
import pandas as pd
import sys
import csv
def downloadAll():
    nasdaq = pd.read_csv("nasdaq_billion.csv")
    for t in range(len(nasdaq['Symbol'])):
        api_key = '9237JMHKQXU276KC'
        url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=%s"%(nasdaq['Symbol'][t],api_key)

        # Save data to this file
        file_to_save = 'stocks_alphavantage/%s.csv'%(nasdaq['Symbol'][t])
        print(nasdaq['Symbol'][t])
        if not os.path.exists(file_to_save):
            with urllib.request.urlopen(url_string) as url:
                data = json.loads(url.read().decode())
                # extract stock market data
                try:
                    data = data['Time Series (Daily)']
                    df = pd.DataFrame(columns=['Date','Low','High','Close', 'Adjusted Close', 'Open'])
                    for k,v in data.items():
                        date = dt.datetime.strptime(k, '%Y-%m-%d')
                        data_row = [date.date(),float(v['3. low']),float(v['2. high']),
                                    float(v['4. close']), float(v['5. adjusted close']), float(v['1. open'])]
                        df.loc[-1,:] = data_row
                        df.index = df.index + 1
                    print('Data saved to : %s'%file_to_save)        
                    df.to_csv(file_to_save)
                except:
                    print(str(sys.exc_info()[0]))
                    continue
            #print('Data saved to : %s'%file_to_save)        
            #df.to_csv(file_to_save)

def cleanCSV():
    with open('nyse_billion.csv', 'rt') as inp, open('nyse_mega.csv', 'wt') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            if row[3] != "n/a" and (row[0] == "Symbol" or float(row[3][1:-1]) > 200): #float(row[3][1:-1]) > 200):
                writer.writerow(row)

if __name__ == "__main__":
    api_key = '9237JMHKQXU276KC'

    if str(sys.argv[1]) == "all":
        downloadAll()
    elif str(sys.argv[1]) == "clean":
        cleanCSV()
    else:
    # Enter stock ticker
        ticker = str(sys.argv[1])

        # JSON file with all the stock market data for AAL within the last 20 years
        url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)

        # Save data to this file
        file_to_save = 'stocks_alphavantage/%s.csv'%ticker
        
        if not os.path.exists(file_to_save):
            with urllib.request.urlopen(url_string) as url:
                data = json.loads(url.read().decode())
                # extract stock market data
                data = data['Time Series (Daily)']
                df = pd.DataFrame(columns=['Date','Low','High','Close','Adjusted Close','Open'])
                for k,v in data.items():
                    date = dt.datetime.strptime(k, '%Y-%m-%d')
                    data_row = [date.date(),float(v['3. low']),float(v['2. high']),
                                float(v['4. close']), float(v['5. adjusted close']), float(v['1. open'])]
                    df.loc[-1,:] = data_row
                    df.index = df.index + 1
            print('Data saved to : %s'%file_to_save)        
            df.to_csv(file_to_save)