import pandas as pd
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
import sys
import os
def determine_sma(data):
    buy = []
    sell = []
    flag = -1
    b = 0.0
    s = 0.0
    num_b = 0
    num_s = 0

    for i in range(len(data)):
        if data['SMA50'][i] > data['SMA200'][i]: #if data['EMA13'][i] > data['EMA50'][i]:  if data['SMA50'][i] > data['SMA200'][i]:
            if flag != 1:
                buy.append(data['Stock'][i])
                sell.append(np.nan)
                b += data['Stock'][i]
                num_b += 1
                flag = 1
            else:
                buy.append(np.nan)
                sell.append(np.nan)
        elif data['SMA50'][i] < data['SMA200'][i]: #elif data['EMA13'][i] < data['EMA50'][i]:  elif data['SMA50'][i] < data['SMA200'][i]:
            if flag != 0:
                buy.append(np.nan)
                sell.append(data['Stock'][i])
                s += data['Stock'][i]
                num_s += 1
                flag = 0
            else:
                buy.append(np.nan)
                sell.append(np.nan)
        else:
            buy.append(np.nan)
            sell.append(np.nan)

    if (num_b > num_s) :
        s += data['Stock'][len(data) - 1]
    if (num_b < num_s) :
        b += data['Stock'][len(data) - 1]
    #print(s-b)
    #print(num_s)
    #print(num_b)
    return [buy, sell, s-b, num_s, num_b]

def determine_ema(data):
    buy = []
    sell = []
    flag = -1
    b = 0.0
    s = 0.0
    num_b = 0
    num_s = 0

    for i in range(len(data)):
        if data['EMA13'][i] > data['EMA50'][i]: #if data['EMA13'][i] > data['EMA50'][i]:  if data['SMA50'][i] > data['SMA200'][i]:
            if flag != 1:
                buy.append(data['Stock'][i])
                sell.append(np.nan)
                b += data['Stock'][i]
                num_b += 1
                flag = 1
            else:
                buy.append(np.nan)
                sell.append(np.nan)
        elif data['EMA13'][i] < data['EMA50'][i]: #elif data['EMA13'][i] < data['EMA50'][i]:  elif data['SMA50'][i] < data['SMA200'][i]:
            if flag != 0:
                buy.append(np.nan)
                sell.append(data['Stock'][i])
                s += data['Stock'][i]
                num_s += 1
                flag = 0
            else:
                buy.append(np.nan)
                sell.append(np.nan)
        else:
            buy.append(np.nan)
            sell.append(np.nan)

    if (num_b > num_s) :
        s += data['Stock'][len(data) - 1]
    if (num_b < num_s) :
        b += data['Stock'][len(data) - 1]
    #print(s-b)
    #print(num_s)
    #print(num_b)
    return [buy, sell, s-b, num_s, num_b]

def ema(data, window):
    run_avg_predictions = []

    running_mean = 0.0
    run_avg_predictions.append(running_mean)
    smoothing_factor = 2

    decay = smoothing_factor/(window+1)

    for pred_idx in range(1,data.size):
        running_mean = running_mean*decay + (1.0-decay)*data[pred_idx-1]
        run_avg_predictions.append(running_mean)
        

    return run_avg_predictions


def sma(data, window):
    window_size = window
    N = data.size
    std_avg_predictions = []
    std_avg_x = []
    mse_errors = []

    for pred_idx in range(1,N):
        std_avg_predictions.append(np.mean(data[pred_idx-window_size:pred_idx]))
        mse_errors.append((std_avg_predictions[-1]-data[pred_idx])**2)

    return std_avg_predictions
def runAll():
    mega = pd.read_csv("nyse_nasdaq_mega.csv")
    s = 0
    e = 0
    comp = []
    scomp = []
    ecomp = []
    profit = 0
    for filename in os.listdir("stocks_alphavantage"):
        file_name = "stocks_alphavantage/%s.csv"%(filename[:-4]) #stocks_alphavantage/
        csv = pd.read_csv(file_name)
        csv['Adjusted Close'] = csv['Adjusted Close'][::-1].reset_index(drop=True)
        
        SMA50 = pd.DataFrame()
        SMA50['Close'] = csv['Adjusted Close'].rolling(window=10).mean()

        SMA200 = pd.DataFrame()
        SMA200['Close'] = csv['Adjusted Close'].rolling(window=20).mean()

        data = pd.DataFrame()
        data['Stock'] = csv['Adjusted Close']

        data['SMA50'] = SMA50['Close']
        data['SMA200'] = SMA200['Close']

        data['EMA13'] = ema(data['Stock'], 15)
        data['EMA50'] = ema(data['Stock'], 50)

        bs_sma = determine_sma(data)
        bs_ema = determine_ema(data)
        if bs_sma[3] == bs_sma[4]: print("%s has same buy and sell for SMA"%filename[:-4])
        if bs_ema[3] == bs_ema[4]: print("%s has same buy and sell for EMA"%filename[:-4])
        if bs_sma[2] < bs_ema[2]:
            if bs_ema[2] > 0:
                comp.append(filename[:-4])
                profit += 1
                e += 1
                ecomp.append(filename[:-4])
        else:
            if bs_sma[2] > 0:
                comp.append(filename[:-4])
                profit += 1
                s += 1
                scomp.append(filename[:-4])
    print("Total Companies: %s"%len(os.listdir("stocks_alphavantage")))
    print(comp)
    print("Profitable: %s"%profit)
    print("Simple Moving Average: %s"%s)
    print(scomp)
    print("Exponential Moving Average: %s"%e)
    print(ecomp)
        


if __name__ == "__main__":
    plt.style.use('fivethirtyeight')
    if sys.argv[1] == "all":
        runAll()
        
    elif len(sys.argv) == 2:
        file_name = "stocks_alphavantage/%s.csv"%(sys.argv[1]) #stocks_alphavantage/
        csv = pd.read_csv(file_name)
        
        #nasdaq = pd.read_csv("nasdaq.csv")
        #print(nasdaq['Symbol'][0])
        csv['Adjusted Close'] = csv['Adjusted Close'][::-1].reset_index(drop=True)
        
        SMA50 = pd.DataFrame()
        SMA50['Close'] = csv['Adjusted Close'].rolling(window=15).mean()

        SMA200 = pd.DataFrame()
        SMA200['Close'] = csv['Adjusted Close'].rolling(window=30).mean()

        #plt.figure(figsize=(12.5, 4.5))
        #plt.plot(csv['Close'], label = 'AAPL')
        #plt.plot(SMA50['Close'], label = 'SMA50')
        #plt.plot(SMA200['Close'], label = 'SMA200')
        #plt.title('Close Price History')
        #plt.xlabel('Nov. 01, 1999 - Nov. 20, 2020')
        #plt.ylabel('Close Price')
        #plt.legend(loc='upper left')
        #plt.show()

        data = pd.DataFrame()
        data['Stock'] = csv['Adjusted Close']

        data['SMA50'] = SMA50['Close']
        data['SMA200'] = SMA200['Close']

        data['EMA13'] = ema(data['Stock'], 13)
        data['EMA50'] = ema(data['Stock'], 48.5)

        bs_sma = determine_sma(data)
        bs_ema = determine_ema(data)
        #buy_sell = ((lambda: bs_sma, lambda: bs_ema)[bs_sma[2] < bs_ema[2]]())
        buy_sell = []
        if bs_sma[2] < bs_ema[2]:
            buy_sell = bs_ema
            print("EMA : %s"%(bs_ema[2]))
            print("Number of Sells: %s"%(bs_ema[3]))
            print("Number of Buys: %s"%(bs_ema[4]))
            print("SMA : %s"%(bs_sma[2]))
        else:
            buy_sell = bs_sma
            print("SMA : %s"%(bs_sma[2]))
            print("Number of Sells: %s"%(bs_sma[3]))
            print("Number of Buys: %s"%(bs_sma[4]))
            print("EMA : %s"%(bs_ema[2]))
        data['Buy_Signal_Price'] = buy_sell[0]
        data['Sell_Signal_Price'] = buy_sell[1]

        plt.figure(figsize=(12.5, 4.5))
        plt.plot(data['Stock'], label = sys.argv[1], alpha = 0.35)
        plt.plot(data['SMA50'], label = 'SMA50', alpha = 0.5)
        plt.plot(data['SMA200'], label = 'SMA200', alpha = 0.5)
        plt.plot(data['EMA13'], label = 'EMA13', alpha = 0.5)
        plt.plot(data['EMA50'], label = 'EMA50', alpha = 0.5)
        plt.scatter(data.index, data['Buy_Signal_Price'], label = 'Buy', marker = '^', color = 'green')
        plt.scatter(data.index, data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color = 'red')
        plt.title('%s Close Price History Buy & Sell Signals'%(sys.argv[1]))
        plt.xlabel('IPO - Current')
        plt.ylabel('Close Price')
        plt.legend(loc='upper left')
        plt.show()
    