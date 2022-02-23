import warnings
from datetime import datetime as dt, timedelta
import math
import json
import pandas as pd
import numpy as np
import time
from talib import RSI, BBANDS,MACD
from functions_for_TA_running import *
#from sectors_and_marketcap import * #for the capitalization value
from relevant_index_return import *

path = 'C:\\Users\\User\\Desktop\\Work_Adi'

def breakaway_model(date_check,p ,date_check_array ,ticker_details, open_check,close_check, low_check, high_check,mivne_mehirim_vector_positions,list_of_min_max_points): # sup_lines, res_lines):
    print(ticker_details)
    print('list_of_min_max_points', list_of_min_max_points)
    # fix indexes of touching (until specific breakaway)
    ticker_details[-3] = [ind for ind in ticker_details[-3] if ind < ticker_details[0]]

    print(ticker_details)

    # Volume(In compare to 25 previuos days)
    print(date_check)
    index12 = date_check['Date'].values.tolist().index(ticker_details[2])
    print(index12)
    if index12 < 25:
        print(date_check.iloc[:index12 + 1]['Volume'].reset_index(drop=True))
        volume_value = date_check.iloc[:index12 + 1]['Volume'].reset_index(drop=True)[index12]
        volume_location = date_check.iloc[:index12 + 1]['Volume'].reset_index(drop=True).sort_values(
            ascending=False).values.tolist().index(volume_value)
        #print(volume_location)

    else:
        print(date_check.iloc[index12-25:index12+1]['Volume'].reset_index(drop=True))
        volume_value = date_check.iloc[index12-25:index12+1]['Volume'].reset_index(drop=True)[25]
        #print(volume_value)
        volume_location = date_check.iloc[index12-25:index12+1]['Volume'].reset_index(drop=True).sort_values(ascending=False).values.tolist().index(volume_value)
        print('volume_location:', volume_location)

    print('abcc')

    # volumne_next_day
    print(ticker_details[2])
    try:
        tomorrow_date = pd.to_datetime(ticker_details[2], format='%Y-%m-%d').date() + timedelta(days=1)
    except:
        tomorrow_date = pd.to_datetime(ticker_details[2], format='%d/%m/%Y').date() + timedelta(days=1)

    tomorrow_str = tomorrow_date.strftime('%Y-%m-%d')
    print(tomorrow_str)
    attempt = 0
    print(date_check['Date'].values.tolist())
    while attempt < 8:
        try:
            index_attempt = date_check['Date'].values.tolist().index(tomorrow_str)
            print(index_attempt)
            print('%$%')
            break
        except:
            attempt = attempt + 1
            tomorrow_date = pd.to_datetime(tomorrow_str, format='%Y-%m-%d').date() + timedelta(days=1)
            tomorrow_str = tomorrow_date.strftime('%Y-%m-%d')
            print(tomorrow_str)
            continue

    try:
        print('attempt', attempt)
        if attempt == 8:
            tomorrow_date = pd.to_datetime(ticker_details[2], format='%d/%m/%Y').date() + timedelta(days=1)
            tomorrow_str = tomorrow_date.strftime('%d/%m/%Y') #again,onlt beacuse this format.
            print(tomorrow_str)
            attempt = 0
            print(date_check['Date'].values.tolist())
            while attempt < 8:
                try:
                    index_attempt = date_check['Date'].values.tolist().index(tomorrow_str)
                    print(index_attempt)
                    print('%$%')
                    break
                except:
                    attempt = attempt + 1
                    tomorrow_date = pd.to_datetime(tomorrow_str, format='%d/%m/%Y').date() + timedelta(days=1)
                    tomorrow_str = tomorrow_date.strftime('%d/%m/%Y')
                    print(tomorrow_str)
                    continue

        try:

            if index_attempt < 25:
                relevant_vector = (date_check.iloc[:index_attempt + 1]['Volume'].reset_index(drop=True)).tolist()
                print(relevant_vector)
                relevant_vector.pop(-2)
                print(relevant_vector)
                volume_value = relevant_vector[-1]
                print(volume_value)
                relevant_vector.sort(reverse=True)
                print(relevant_vector)
                volume_tomorrow_location = relevant_vector.index(volume_value)
                print(volume_tomorrow_location)

            else:
                relevant_vector = date_check.iloc[index_attempt-25:index_attempt + 1]['Volume'].reset_index(drop=True).tolist()
                print(relevant_vector)
                relevant_vector.pop(-2)
                print(relevant_vector)
                volume_value = relevant_vector[-1]
                print(volume_value)
                relevant_vector.sort(reverse=True)
                print(relevant_vector)
                volume_tomorrow_location = relevant_vector.index(volume_value)
                print(volume_tomorrow_location)

        except:
            volume_tomorrow_location = None
    except:
        volume_tomorrow_location = None

    # Intra-day return
    print(date_check.iloc[index12]['Close'])
    print(float(date_check.iloc[index12]['Open']))
    today_return = round(((float(date_check.iloc[index12]['Close']) / float(date_check.iloc[index12]['Open'])) - 1), 3)
    print('today_return:', today_return)

    # RSI
    #relevant_index_data = pd.read_csv(f'C:\\Users\\User\\Downloads\\{ticker_details[3]}.csv')
    #index = relevant_index_data['Date'].values.tolist().index(ticker_details[2])
    #rsi = RSI(relevant_index_data['Close'], timeperiod=14).values.tolist()
    print(RSI(date_check['Adj Close'], timeperiod=14))
    rsi_today = round(RSI(date_check['Adj Close'], timeperiod=14).values.tolist()[index12], 2)
    print('rsi_today:', rsi_today)
    rsi_yesterday = round(RSI(date_check['Adj Close'], timeperiod=14).values.tolist()[index12 - 1], 2)
    print('rsi_yesterday:', rsi_yesterday)
    change_rsi = rsi_today - rsi_yesterday
    print('change_rsi:', change_rsi)

    # Gap long
    if (ticker_details[4] == 'break_res') or (ticker_details[4] == 'fail_break_res'):
        gap_long = round(((float(ticker_details[-1])/float(ticker_details[6])) - 1), 4)  # it's take_profit also.
        gap_long_next_open = round(((float(ticker_details[1])/float(ticker_details[6])) - 1), 4)  # it's take_profit also.
        print('gap_long:', gap_long)
        print('gap_long_open:', gap_long_next_open)
        print(ticker_details)

    else:
        gap_long = round(((float(ticker_details[6])/float(ticker_details[-1])) - 1), 4)  # it's take_profit also.
        gap_long_next_open = round(((float(ticker_details[6])/float(ticker_details[1])) - 1), 4)  # it's take_profit also.
        print('gap_long:', gap_long)
        print('gap_long_open:', gap_long_next_open)
        print(ticker_details)

    #print(ticker_details)
    #gap_long = abs(round(((float(ticker_details[1])/float(ticker_details[6])) - 1), 4))  # it's take_profit also.
    #print("gap_long(in percentage):", gap_long)


    # How much we broke the res/sup line
    percentage_of_broken_resistence_or_support = abs(round(((float(ticker_details[6])/float(ticker_details[5])) - 1), 5))
    print('percentage_of_broken_resistence_or_support:', percentage_of_broken_resistence_or_support)

    # Mivne_Mehirim
    print('mivne_mehirim_vector_positions:', mivne_mehirim_vector_positions)
    try:
        index_of_i = ([element[2] for element in mivne_mehirim_vector_positions].index(ticker_details[0])) + 1
        mivne_mehirim_obs = mivne_mehirim_vector_positions[index_of_i][0]
        print(mivne_mehirim_obs)
    except:
        mivne_mehirim_obs = False

    # Financial reports
    financial_reports_details = pd.read_csv(path + f"\\actually_earnings\\{ticker_details[3]}.csv")
    print(financial_reports_details)

    try:
        new_event_date = pd.to_datetime(ticker_details[2], format='%d/%m/%Y').date()
    except:
        new_event_date = pd.to_datetime(ticker_details[2], format='%Y-%m-%d').date()

    financial_values = False

    print(new_event_date)

    try:

        for idx, date_column in enumerate(financial_reports_details['date'].values.tolist()):

            try:
                date_column = pd.to_datetime(date_column, format='%d/%m/%Y').date()
            except:
                date_column = pd.to_datetime(date_column, format='%Y-%m-%d').date()

            print(date_column)

            if financial_reports_details.iloc[idx]['hour'] == 'amc':
                date_column = date_column + timedelta(days=1)

            print(financial_reports_details.iloc[idx])
            print('date_column:', date_column)
            print('new_event_date:',new_event_date)

            if financial_reports_details.iloc[idx]['hour'] == 'amc':
                try:
                    financial_reports_details_date = pd.to_datetime(financial_reports_details.iloc[idx]['date'], format='%Y-%m-%d').date() + timedelta(days=1)
                except:
                    financial_reports_details_date = pd.to_datetime(financial_reports_details.iloc[idx]['date'],
                                                                    format='%d/%m/%Y').date() + timedelta(days=1)
            else:
                try:
                    financial_reports_details_date = pd.to_datetime(financial_reports_details.iloc[idx]['date'],
                                                                    format='%Y-%m-%d').date() # + timedelta(days=1)
                except:
                    financial_reports_details_date = pd.to_datetime(financial_reports_details.iloc[idx]['date'], format='%d/%m/%Y').date()

            try:
                next_date = pd.to_datetime(financial_reports_details.iloc[idx+1]['date'], format='%Y-%m-%d').date()
                print('next_date:', next_date)
            except:
                next_date = pd.to_datetime(financial_reports_details.iloc[idx + 1]['date'], format='%d/%m/%Y').date()
                print('next_date:', next_date)

            if financial_reports_details.iloc[idx]['hour'] == 'bmo':
                print(new_event_date, date_column)
                if (new_event_date == date_column): # or new_event_date  date_column :
                    pass
                elif ((new_event_date > date_column) and (new_event_date < next_date)) :
                    pass
                else:
                    continue

            elif new_event_date > next_date:

                continue

            print(date_column)
            print(new_event_date)
            print(financial_reports_details_date)
            print(int((new_event_date - financial_reports_details_date).days))
            time_after_report = int((new_event_date - financial_reports_details_date).days)
            print('sssa')

            try:
                this_report = financial_reports_details.iloc[idx].loc[['epsActual', 'epsEstimate',
                                                                       'revenueActual', 'revenueEstimate', 'hour',
                                                                       'time']].values.tolist()
                #print(financial_reports_details.iloc[idx].iloc[[2, 3, 4, 6, 7]].values)
            except:
                this_report = None
            try:
                previous_report = financial_reports_details.iloc[idx - 1].loc[['epsActual', 'epsEstimate',
                                                                               'revenueActual', 'revenueEstimate', 'hour',
                                                                               'time']].values.tolist()
            except:
                previous_report = None

            try:
                last_year_same_qtr_report = financial_reports_details.iloc[idx - 4].loc[
                    ['epsActual', 'epsEstimate',
                     'revenueActual', 'revenueEstimate', 'hour',
                     'time']].values.tolist()
            except:
                last_year_same_qtr_report = None

            print('this_report:', this_report)
            print('previous_report:', previous_report)
            print('last_year_same_qtr_report:', last_year_same_qtr_report)

            try:
                if previous_report[0] > 0:  # if eps positive
                    change_eps_from_previous_report_eps = (this_report[0] - previous_report[0]) / previous_report[0]
                else:
                    change_eps_from_previous_report_eps = -(this_report[0] - previous_report[0]) / \
                                                              previous_report[0]

                change_revenue_from_previous_report_revenue = (this_report[2] - previous_report[2]) / \
                                                                  previous_report[2]
            except:
                change_eps_from_previous_report_eps = None
                change_revenue_from_previous_report_revenue = None

            # last year:
            try:
                if (last_year_same_qtr_report[0] > 0):
                    change_eps_from_previous_year_eps = (this_report[0] - last_year_same_qtr_report[0]) \
                                                            / last_year_same_qtr_report[0]
                else:
                    change_eps_from_previous_year_eps = -(this_report[0] - last_year_same_qtr_report[0]) \
                                                            / last_year_same_qtr_report[0]

                change_revenue_from_previous_year_revenue = (this_report[2] - last_year_same_qtr_report[
                    2]) \
                    / last_year_same_qtr_report[2]

            except:
                change_eps_from_previous_year_eps = None
                change_revenue_from_previous_year_revenue = None

            print("change previous report eps:", change_eps_from_previous_report_eps, "\nchange"
                                                                                          " previous report revenue:",
                  change_revenue_from_previous_report_revenue, "\nchange previ"
                                                               "ous year report eps:",
                  change_eps_from_previous_year_eps, "\nchange previous year"
                                                         " report revenue:", change_revenue_from_previous_year_revenue,
                  "\ntoday eps actually:", this_report[0], "\ntoday eps estimated:", this_report[1],
                  "\ntoday revenue actually:", this_report[2], "\ntoday revenue estimated:", this_report[3],
                  this_report[4], this_report[5])

            financial_values = True
            break

        if not financial_values:
            print('last_financial_reporting_row')
            try:
                financial_reports_details_date = pd.to_datetime(financial_reports_details.iloc[-1]['date'],
                                                                format='%Y-%m-%d').date()
            except:
                financial_reports_details_date = pd.to_datetime(financial_reports_details.iloc[-1]['date'],
                                                                format='%d/%m/%Y').date()

            if financial_reports_details.iloc[-1]['hour'] == 'amc':  # it refers to previous day (because report belongs it)
                print(new_event_date)

                time_after_report = int((new_event_date - financial_reports_details_date - timedelta(days=1)).days)
            else:
                time_after_report = int((new_event_date - financial_reports_details_date).days)

            print(time_after_report)

            try:
                this_report = financial_reports_details.iloc[-1].loc[['epsActual', 'epsEstimate',
                                                                           'revenueActual', 'revenueEstimate', 'hour',
                                                                           'time']].values.tolist()
            except:
                this_report = None

            try:
                previous_report = financial_reports_details.iloc[-2].loc[['epsActual', 'epsEstimate',
                                                                               'revenueActual', 'revenueEstimate', 'hour',
                                                                               'time']].values.tolist()
            except:
                previous_report = None

            try:
                last_year_same_qtr_report = financial_reports_details.iloc[-5].loc[
                    ['epsActual', 'epsEstimate',
                     'revenueActual', 'revenueEstimate', 'hour',
                     'time']].values.tolist()
            except:
                last_year_same_qtr_report = None

            print('this_report:', this_report)
            print('previous_report:', previous_report)
            print('last_year_same_qtr_report:', last_year_same_qtr_report)

            try:
                if previous_report[0] > 0:  # if eps positive
                    change_eps_from_previous_report_eps = (this_report[0] - previous_report[0]) / previous_report[0]
                else:
                    change_eps_from_previous_report_eps = -(this_report[0] - previous_report[0]) / \
                                                          previous_report[0]

                change_revenue_from_previous_report_revenue = (this_report[2] - previous_report[2]) / \
                                                              previous_report[2]
            except:
                change_eps_from_previous_report_eps = None
                change_revenue_from_previous_report_revenue = None

            # last year:
            try:
                if (last_year_same_qtr_report[0] > 0):
                    change_eps_from_previous_year_eps = (this_report[0] - last_year_same_qtr_report[0]) \
                                                        / last_year_same_qtr_report[0]
                else:
                    change_eps_from_previous_year_eps = -(this_report[0] - last_year_same_qtr_report[0]) \
                                                        / last_year_same_qtr_report[0]

                change_revenue_from_previous_year_revenue = (this_report[2] - last_year_same_qtr_report[2]) \
                                                            / last_year_same_qtr_report[2]

            except:
                change_eps_from_previous_year_eps = None
                change_revenue_from_previous_year_revenue = None

            print("change previous report eps:", change_eps_from_previous_report_eps, "\nchange"
                                                                                      " previous report revenue:",
                  change_revenue_from_previous_report_revenue, "\nchange previ"
                                                               "ous year report eps:",
                  change_eps_from_previous_year_eps, "\nchange previous year"
                                                     " report revenue:", change_revenue_from_previous_year_revenue,
                  "\ntoday eps actually:", this_report[0], "\ntoday eps estimated:", this_report[1],
                  "\ntoday revenue actually:", this_report[2], "\ntoday revenue estimated:", this_report[3],
                  this_report[4], this_report[5])
    except:
        this_report = [None, None, None, None, None, None]
        change_eps_from_previous_report_eps = None
        change_revenue_from_previous_report_revenue = None
        change_eps_from_previous_year_eps = None
        change_revenue_from_previous_year_revenue = None
        time_after_report = None


    # Spy return
    spy = pd.read_csv('C:\\Users\\User\\Desktop\Work_Adi\\daily_data_tickers_breakaway_model\\spy.csv')
    answer = False

    try:

        try:
            new_event_date = (pd.to_datetime(ticker_details[2], format='%d/%m/%Y').date())
            new_event_date = new_event_date.strftime('%Y-%m-%d')
            spy_date1 = [(pd.to_datetime(date1, format='%d/%m/%Y')).strftime('%Y-%m-%d') for date1 in spy['Date']]
            index = spy_date1.index(new_event_date) #.values.tolist()
            spy_return = round(spy.iloc[index - 1:index + 1]['Adj Close'].pct_change().values[-1], 4)
            print(spy_return)
            answer = True
            print('123123')

        except:
            new_event_date = (pd.to_datetime(ticker_details[2], format='%m/%d/%Y').date())
            new_event_date = new_event_date.strftime('%Y-%d-%m')
            spy_date2 = [(pd.to_datetime(date1, format='%d/%m/%Y')).strftime('%Y-%d-%m') for date1 in spy['Date']]
            index = spy_date2.index(new_event_date) #.values.tolist()
            spy_return = round(spy.iloc[index - 1:index + 1]['Adj Close'].pct_change().values[-1], 4)
            print(spy_return, 4)
            answer = True

    except:
        new_event_date = ticker_details[2]
        print('normal')
        print(new_event_date)

    if not answer:
        #try:
        #    new_event_date = (pd.to_datetime(new_event_date, format='%Y-%d-%m').date())
        #    new_event_date = new_event_date.strftime('%Y-%d-%m')
        #    print(new_event_date)
        #    spy_date3 = [(pd.to_datetime(date1)).strftime('%Y-%d-%m') for date1 in spy['Date']]
        #    index = spy_date3.index(new_event_date) #.values.tolist()
        #    print(round(spy.iloc[index - 1:index + 6]))
        #    spy_return = round(spy.iloc[index - 1:index + 1]['Adj Close'].pct_change().values[-1], 4)
        #    print(spy_return)
        #    print('33321321')
        #    time.sleep(121)

        #except:
        new_event_date = (pd.to_datetime(ticker_details[2], format='%Y-%m-%d').date())
        print(new_event_date)
        new_event_date = new_event_date.strftime('%Y-%m-%d')
        print(new_event_date)
        print(spy['Date'])
        spy_date4 = [(pd.to_datetime(date1, format='%d/%m/%Y'))for date1 in spy['Date']]
        spy_date4 = [date1.strftime('%Y-%m-%d') for date1 in spy_date4]
        print(spy_date4)
        index = spy_date4.index(new_event_date) #.values.tolist()
        print(round(spy.iloc[index - 1:index + 1]))#['Adj Close']))
        spy_return = round(spy.iloc[index - 1:index + 1]['Adj Close'].pct_change().values[-1], 4)
        print(spy_return)

    print(new_event_date)
    print('*&*&')
    print(type(new_event_date))

    print(type(spy['Date'].iloc[0]))
    print(spy['Date'].values.tolist())

    '''
    #spy megama
    relevant_index_data = pd.read_csv(f'C:\\Users\\User\\Desktop\Work_Adi\\daily_data_tickers_breakaway_model\\spy.csv')
    index = relevant_index_data['Date'].values.tolist().index(ticker_details[2])
    lst_date_mivne_mehirim = [a[3] for a in mivne_mehirim_vector_positions]
    index_mivne_mehirim_spy = lst_date_mivne_mehirim.index(relevant_index_data['Date'].iloc[index])
    print(index_mivne_mehirim_spy)
    '''

    # sector
    try:
        sector_data = pd.read_csv(path + f"\\nasdaq_sectors.csv")
        specific_sector = sector_data[sector_data['Symbol'] == ticker_details[3]]['Sector'].values[0]
        print(specific_sector)
    except:
        specific_sector = None


    '''
    #sector_megama
    relevant_index_data = pd.read_csv(f'C:\\Users\\User\\Desktop\Work_Adi\\daily_data_tickers_breakaway_model\\specific_sector.csv')
    index = relevant_index_data['Date'].values.tolist().index(ticker_details[2])
    lst_date_mivne_mehirim = [a[3] for a in mivne_mehirim_vector_positions]
    index_mivne_mehirim_sector = lst_date_mivne_mehirim.index(relevant_index_data['Date'].iloc[index])
    '''

    # market_cap
    cap_data = pd.read_csv('C:\\Users\\User\\Desktop\\Work_Adi\\outstanding_shares1_2020-01-01.csv')
    tick_new = ticker_details[3]

    capital_stocks = cap_data[cap_data['tic1'] == tick_new]['capital'].values[0]
    print(capital_stocks)


    try:
        index = date_check['Date'].values.tolist().index(new_event_date)
        print(date_check.iloc[index]['Adj Close'])
        capitalization = float(date_check.iloc[index]['Adj Close']) * capital_stocks
        print(capitalization)

    except:
        try:
            specific_day = new_event_date.strftime('%d/%m/%Y')
            index = date_check['Date'].values.tolist().index(specific_day)
            print(date_check.iloc[index]['Adj Close'])
            capitalization = float(date_check.iloc[index]['Adj Close']) * capital_stocks
            print(capitalization)

        except:
            specific_day = (pd.to_datetime(new_event_date, format='%Y-%m-%d').date())
            print(new_event_date)
            specific_day = specific_day.strftime('%d/%m/%Y')
            index = date_check['Date'].values.tolist().index(specific_day)
            print(date_check.iloc[index]['Adj Close'])
            capitalization = float(date_check.iloc[index]['Adj Close']) * capital_stocks
            print(capitalization)

    # change_specfic_sector_lastday
    relevant_index = find_sector(specific_sector)
    print(relevant_index)
    try:
        relevant_index_data = pd.read_csv(f'C:\\Users\\User\\Desktop\Work_Adi\\daily_data_tickers_breakaway_model\\{relevant_index}.csv')
        try:
            specific_day = pd.to_datetime(ticker_details[2], format='%d/%m/%Y').date()
        except:
            specific_day = pd.to_datetime(ticker_details[2], format='%Y-%m-%d').date()

        try:
            specific_day = specific_day.strftime('%Y-%m-%d')
            index = relevant_index_data['Date'].values.tolist().index(specific_day)

        except:
            specific_day = specific_day.strftime('%d/%m/%Y')
            index = relevant_index_data['Date'].values.tolist().index(specific_day)

        print(relevant_index_data.iloc[index - 1:index + 1]['Adj Close'])
        change_specfic_sector_lastday = (relevant_index_data.iloc[index - 1:index + 1]['Adj Close'].pct_change().values[-1])
        print(change_specfic_sector_lastday)

    except:
        change_specfic_sector_lastday = None

    # long_gap compared with x previuos candels
    relevant_index_data = pd.read_csv(f'C:\\Users\\User\\Desktop\Work_Adi\\daily_data_tickers_breakaway_model\\{ticker_details[3]}.csv')
    #index = relevant_index_data['Date'].values.tolist().index(ticker_details[2])
    ere = pd.DataFrame(relevant_index_data.iloc[index - 20:index][['High', 'Low', 'Date']]).reset_index(
        drop=True)  # until (but without) the day of breakaway
    ere['day_return'] = ((ere['High'] / ere['Low'])) - 1

    ere = ere.sort_values(by=['day_return'])
    print(ere)
    answer = False

    print(ere['day_return'].values.tolist()[::-1])

    for idx, specific_return in enumerate(ere['day_return'].values.tolist()[::-1]):
        print(specific_return)

        if gap_long < specific_return:
            continue
        else:
            print(idx)
            location_our_gap = idx
            answer = True
            break

    if not answer:
        location_our_gap = len(ere)
        print(location_our_gap)

    # time from end line, its length and number of touches
    time_past_from_end_of_support = ticker_details[0] - ticker_details[-3][-1]
    print(time_past_from_end_of_support)
    len_touch = len(ticker_details[-3])
    print(len_touch)
    lentgh_of_line = int(ticker_details[-3][-1]) - int(ticker_details[-3][0])
    print(lentgh_of_line)

    # VXX return
    answer = False
    vxx = pd.read_csv('C:\\Users\\User\\Desktop\Work_Adi\\daily_data_tickers_breakaway_model\\vxx.csv')

    print(ticker_details[2])
    print(vxx)

    try:

        try:
            new_event_date = (pd.to_datetime(ticker_details[2], format='%d/%m/%Y').date())
            new_event_date = new_event_date.strftime('%Y-%d-%m')
            vxx_date1 = [(pd.to_datetime(date1, format='%d/%m/%Y')).strftime('%Y-%d-%m') for date1 in vxx['Date']]
            index = vxx_date1.index(new_event_date) #.values.tolist()
            vxx_return = round(vxx.iloc[index - 1:index + 1]['Adj Close'].pct_change().values[-1], 4)
            print(vxx_return)
            answer = True

        except:
            new_event_date = (pd.to_datetime(ticker_details[2], format='%m/%d/%Y').date())
            new_event_date = new_event_date.strftime('%Y-%d-%m')
            vxx_date2 = [(pd.to_datetime(date1, format='%d/%m/%Y')).strftime('%Y-%d-%m') for date1 in vxx['Date']]
            index = vxx_date2.index(new_event_date) #.values.tolist()
            vxx_return = round(vxx.iloc[index - 1:index + 1]['Adj Close'].pct_change().values[-1], 4)
            print(vxx_return, 4)
            answer = True

    except:
        new_event_date = ticker_details[2]
        print('normal')
        print(new_event_date)

    if not answer:
        try:
            new_event_date = pd.to_datetime(ticker_details[2], format='%Y-%m-%d').date()
            print(new_event_date)
            new_event_date = new_event_date.strftime('%d/%m/%Y')
            print(new_event_date)
        except:
            pass

        try:
            vxx_date4 = [(pd.to_datetime(date1, format='%Y-%m-%d'))for date1 in vxx['Date']]
            vxx_date4 = [date1.strftime('%Y-%m-%d') for date1 in vxx_date4]
        except:
            vxx_date4 = [(pd.to_datetime(date1, format='%d/%m/%Y')) for date1 in vxx['Date']]
            vxx_date4 = [date1.strftime('%d/%m/%Y') for date1 in vxx_date4]

        print(vxx_date4)
        try:
            index = vxx_date4.index(new_event_date) #.values.tolist()
            print(round(vxx.iloc[index - 1:index + 1]))#['Adj Close']))
            vxx_return = round(vxx.iloc[index - 1:index + 1]['Adj Close'].pct_change().values[-1], 4)
            print(vxx_return)
        except:
            vxx_return = False

    #print(new_event_date)
    #print(vxx['Date'].values.tolist())

    # Target(s) - with "little" backtesting

    #if len(gap) > 2% its -"0.5*len" else: 2%

    tar = 2
    precentage_of_SL_TP = False
    Date_close_position = False

    print('ticker_details:', ticker_details)

    index12 = date_check['Date'].values.tolist().index(ticker_details[2])
    print(date_check.iloc[index12+1:].reset_index(drop=True))
    dt = date_check.iloc[index12+1:].reset_index(drop=True)

    if (ticker_details[4] == 'break_res') or ticker_details[4] == 'fail_break_res':

        if (ticker_details[-1]/ticker_details[6]) > 1.03: #open_last_obs = [1], in order to insert position immeditly
            target = (ticker_details[-1]/ticker_details[6]) * ticker_details[-2]
            print('target:', target)
            time.sleep(0.2)

        else:
            target = 1.03 * ticker_details[-2]
            print('target:', target)
            time.sleep(0.2)

    else:
        if (ticker_details[-1]/ticker_details[6]) < 0.97:
            target = (ticker_details[-2] + (ticker_details[-1]/ticker_details[6]) * ticker_details[-2])/2
            print('target:', target)
            time.sleep(0.2)

        else:
            target = 0.97 * ticker_details[-2]
            print('target:', target)

    specific_date = ticker_details[2]
    loop = 0

    while True:
        if loop == 50:
            break

        try:
            idx_in_min_max_vector = ([element[0] for element in list_of_min_max_points].index(specific_date))
            break

        except:
            try:
                specific_date = pd.to_datetime((specific_date), format='%d/%m/%Y').date()
                specific_date = specific_date + timedelta(days=1)
                specific_date = specific_date.strftime('%d/%m/%Y')
                print(specific_date)
                loop = loop + 1
            except:
                specific_date = pd.to_datetime((specific_date), format='%Y-%m-%d').date()
                specific_date = specific_date + timedelta(days=1)
                specific_date = specific_date.strftime('%Y-%m-%d')
                print(specific_date)
                loop = loop + 1

    #print(list_of_min_max_points[idx_in_min_max_vector - 3:idx_in_min_max_vector])
    if loop < 50:
        last_min_max_obs = list_of_min_max_points[idx_in_min_max_vector - 3:idx_in_min_max_vector]
    else:
        last_min_max_obs = list_of_min_max_points[-3:]
    print(list_of_min_max_points)
    print(last_min_max_obs)
    print(dt)

    try:
        if (ticker_details[4] == 'break_res') or ticker_details[4] == 'fail_break_res':
            for element in [-1, -2, -3]:
                if last_min_max_obs[element][1] == 'min':
                    sl = (min(last_min_max_obs[element][-2], last_min_max_obs[element][-1]))*0.98
                    print('sl', sl)
                    time.sleep(0.2)
                    break

        else:
            for element in [-1, -2, -3]:
                if last_min_max_obs[element][1] == 'max':
                    sl = max(last_min_max_obs[element][-2], last_min_max_obs[element][-1])*1.02
                    print('sl', sl)
                    time.sleep(0.2)
                    break
    except:
        sl = 'prob'

    # index_of_i = ([element[2] for element in mivne_mehirim_vector_positions].index(ticker_details[0])) + 1
    # mivne_mehirim_obs = mivne_mehirim_vector_positions[index_of_i-3:index_of_i][0]

    if sl == 'prob':
        Date_close_position = 'prob'
        tar = 2
        precentage_of_SL_TP = 'prob'

    else:
        for idx, (element0, element1, element2, element3, element4) in \
            enumerate(zip(dt['Date'], dt['Open'], dt['High'], dt['Low'], dt['Close'])):
            print('index123:', idx)
            if (ticker_details[4] == 'break_res') or ticker_details[4] == 'fail_break_res':
                if element2 > target:
                    print(element0)
                    Date_close_position = element0
                    print(element2, target)
                    print('take_profit')
                    tar = 1
                    precentage_of_SL_TP = ((target/ticker_details[-2]) - 1)
                    time.sleep(0.2)
                    break

                #if (idx == 0) and (element3 < ticker_details[5]):
                #    print(element0)
                #    Date_close_position = element0
                #    print(element3, ticker_details[5])
                #    print('Stop_Loss_same_date')
                #    tar = 0
                #    precentage_of_SL_TP = (ticker_details[5]/ticker_details[1]) - 1
                #    print(precentage_of_SL_TP)
                #    time.sleep(3)
                #    break

                elif element3 < sl:
                    print(element0)
                    Date_close_position = element0
                    print(element3, sl)
                    print('Stop_Loss')
                    precentage_of_SL_TP = (sl/ticker_details[-2]) - 1
                    time.sleep(0.2)
                    tar = 0
                    break

            else:

                if element3 < target:
                    print(element0)
                    Date_close_position = element0
                    print(element3, target)
                    precentage_of_SL_TP = ((ticker_details[-2] / target) - 1)
                    print('take_profit')
                    tar = 1
                    time.sleep(0.2)
                    break

                #if (idx == 0) and (element2 > ticker_details[5]):
                #    print(element0)
                #    Date_close_position = element0
                #    print(element2, ticker_details[5])
                #    print('Stop_Loss_same_date')
                #    precentage_of_SL_TP = (ticker_details[1] / ticker_details[5]) - 1
                #    print(precentage_of_SL_TP)
                #    tar = 0
                #    time.sleep(3)
                #    break

                elif element2 > sl:
                    print(element0)
                    Date_close_position = element0
                    print(element3, sl)
                    print('Stop_Loss')
                    precentage_of_SL_TP = (ticker_details[-2]/sl) - 1
                    time.sleep(0.2)
                    tar = 0
                    break


    print(volume_location,volume_tomorrow_location, today_return, rsi_today, change_rsi\
           , percentage_of_broken_resistence_or_support, mivne_mehirim_obs\
           , change_eps_from_previous_report_eps, change_revenue_from_previous_report_revenue, change_eps_from_previous_year_eps\
            , change_revenue_from_previous_year_revenue, time_after_report, this_report[0], this_report[1],this_report[2],this_report[3]\
            , this_report[4], this_report[5], spy_return, vxx_return, specific_sector, capitalization, change_specfic_sector_lastday\
            , gap_long, gap_long_next_open, location_our_gap, time_past_from_end_of_support, len_touch, lentgh_of_line, tar, precentage_of_SL_TP, Date_close_position, sl, ticker_details[-2], target)

    return volume_location,volume_tomorrow_location, today_return, rsi_today, change_rsi\
            , percentage_of_broken_resistence_or_support, mivne_mehirim_obs\
            , change_eps_from_previous_report_eps, change_revenue_from_previous_report_revenue, change_eps_from_previous_year_eps\
            , change_revenue_from_previous_year_revenue, time_after_report, this_report[0], this_report[1], this_report[2], this_report[3]\
            , this_report[4], this_report[5], spy_return, vxx_return, specific_sector, capitalization, change_specfic_sector_lastday\
            , gap_long,gap_long_next_open, location_our_gap\
            , time_past_from_end_of_support, len_touch, lentgh_of_line, tar, precentage_of_SL_TP,Date_close_position, sl, ticker_details[-2], target

            #'index_mivne_mehirim_spy, index_mivne_mehirim_sector