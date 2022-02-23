from urllib.request import Request, urlopen
import pandas as pd
import re
import os, glob
import random
import json
import numpy as np
import collections
from datetime import datetime
import requests
import time

def find_sector(sector):
    lst0 = ['XLY', 'XLP', 'XLF', 'XLE', 'XLI', 'XLU', 'XLV', 'XLK', 'SPY', 'IYT']
    if sector in ['Consumer Durables', 'Consumer Services']:
        return lst0[0] #'XLY'
    elif sector == 'Consumer Non-Durables':
        return lst0[1] #'XLP'
    elif sector == 'Finance':
        return lst0[2] #'XLF'
    elif sector == 'Energy':
        return lst0[3] #'XLE'
    elif sector in ['Basic Industries', 'Capital Goods']:
        return lst0[4] #'XLI'
    elif sector == 'Public Utilities':
        return lst0[5] #'XLU'
    elif sector == 'Health Care':
        return lst0[6] #'XLV'
    elif sector == 'Technology':
        return lst0[7] #'XLK'
    elif sector == 'Miscellaneous':
        return lst0[8] #'spy'
    elif sector == 'Transportation':
        return lst0[9] #'iyt'
    else:
        return ""

def relevant_index_for_comparing(new_index_data, date, sector, vector_of_indexes, percentage):
    print(date)
    #print(new_index_data)

    new_index_data.Date = new_index_data.Date.apply(str)
    unique_dates = pd.Series(new_index_data['Date'].unique())
    date1 = pd.to_datetime(date, format='%d/%m/%Y').date()
    date1_m = date1.strftime('%Y-%m-%d')
    date1_m = date1_m.replace('-', '')
    print(date1_m)

    lst = []
    try:
        for idx2, element in enumerate(vector_of_indexes):
            print(element, idx2)
            data1 = new_index_data[
                 ((new_index_data['Date'] > date1_m) &
                  (new_index_data['Date'] <= unique_dates[unique_dates[unique_dates == date1_m].index[0] + element]))]
            if idx2 == 0:
                lst.append(data1['LastTradePrice'].values[0])
                continue
            print(round(np.percentile(data1['LastTradePrice'], percentage), 4))
            lst.append(round(np.percentile(data1['LastTradePrice'], percentage), 4))
        return [date, sector, data1['Ticker'].values[0], lst[0], lst[1], lst[2], lst[3], lst[4]]
    except:
        return ['', '', '', '', '', '', '', '']


#######################
'''
data = pd.read_csv('C:\\Users\\User\\Desktop\\Work_Adi\\actually_earnings\\master_file_new_new.csv')
'''
#lst0 = ['XLY', 'XLP', 'XLF', 'XLE', 'XLI', 'XLU', 'XLV', 'XLK', 'SPY', 'IYT']
#frame = pd.DataFrame()
#for idx1, element1 in enumerate(lst0):
#    print(element1)
#    new_data = pd.read_csv(
#        f'C:\\Users\\User\\Desktop\\Work_Adi\\stocks_one_minute_by_ticker\\{element1}.csv')
#    print(new_data)
#    frame = pd.concat([frame, new_data], axis=0)
#    print(frame)
#    time.sleep(2)

#frame.to_csv(f'C:\\Users\\User\\Desktop\\Work_Adi\\stocks_one_minute_by_ticker\\indexes_sectors.csv')
#time.sleep(10)
'''

frame = pd.read_csv(f'C:\\Users\\User\\Desktop\\Work_Adi\\stocks_one_minute_by_ticker\\indexes_sectors.csv')
lst_general = []
for idx, (date1, sector1) in enumerate(
            zip(data['date'], data['Sector'])):
    print(date1, sector1)
    if pd.isnull(sector1):
        lst_general.append([""]*7)
        print(lst_general)
        continue

    sector_1 = find_sector(sector1)
    print(sector_1)


    frame1 = frame[frame['Ticker'] == sector_1]
    shortcut = False

    for idx1, each in enumerate(lst_general[::-1]):
        if idx1 >= 10:
            break

        try:
            if ((date1 == each[0]) & (sector_1 == each[2])):
                lst_general.append(lst_general[::-1][idx1])
                print(lst_general)
                shortcut = True
                break
        except:
            pass

    if shortcut == True:
        continue



    lst_general.append(relevant_index_for_comparing(frame1, date1, sector1, [1, 5, 12, 22, 57], 95)) # 1 is this day but I decrease 1 after
    print(lst_general)

columns = ['date12', 'sector2', 'relevant_index', 'relevant_index_price', 'relevant_index_price_after week', 'relevant_index_price_after_two_weeks',
                   'relevant_index_price_month', 'relevant_index_price_after_two_months']
to_save_1 = pd.DataFrame(lst_general, columns=columns)
to_save_1.to_csv('C:\\Users\\User\\Desktop\\Work_Adi\\indexes_to_compare2.csv', index=False)
'''