import warnings
from datetime import datetime as dt, timedelta
import math
import json
import pandas as pd
import numpy as np
import time
import math

path = 'C:\\Users\\User\\Desktop\\Work_Adi'

def import_company_data(comp_prices, hour):
    comp_prices['TimeBarStart'] = comp_prices['TimeBarStart'].str.replace(r'\D', '')
    comp_prices = comp_prices[comp_prices['TimeBarStart'] == str(hour)]
    return comp_prices, hour

model_name = ['beaten', 'missed']

model_name = model_name[0]

if model_name == 'beaten':
    important_arguments = {"take_profit": 1.08, "stop_loss": 0.75, "money_per_stock": 5500}

else:
    important_arguments = {"take_profit": 0.85, "stop_loss": 1.2, "money_per_stock": 10000}

#date_of_trade, I take it from tsla, because all of days was teaded in tsla
relevant_data = pd.read_csv(path + f"\\stocks_one_minute_by_ticker\\tsla.csv")
dates_of_exchange = pd.Series(relevant_data['Date'].unique()).tolist()
dates_of_exchange = [str(date1) for date1 in dates_of_exchange]
print(dates_of_exchange)

#beaten - '20180509', '20180710','20161107'

#previous_day = '20180303'
date_today = '20170530'
money = 1000000

idx_date_today = dates_of_exchange.index(date_today) #idx of date_today

#important_arguments = {"take_profit": 1.08, "stop_loss": 0.8, "money_per_stock": 8500}

signals_data = pd.read_csv(path + '\\actually_earnings\\master_file_new_new.csv')

#Its neet to be sorted!!!!!!!! date,bmo,hour

signals_data['date'] = [pd.to_datetime(date1, format='%d/%m/%Y').date() for date1 in signals_data['date']]
signals_data['date'] = [date1.strftime('%Y-%m-%d') for date1 in signals_data['date']]
signals_data['date'] = [date1.replace('-', '') for date1 in signals_data['date']]

#signals_data = signals_data[signals_data['date']]
index_day21 = [i for i, x in enumerate(signals_data['date']) if x == date_today][0]
print(index_day21)
signals_data = signals_data.loc[index_day21:].reset_index(drop=True)
print(signals_data)

list_of_companies = {}
list_of_companies_not_buyed_because_lack_money = {}
data_frame_all_ticker_in_portfolio = None


def check_stoploss_takeprofit(date_now, list_of_companies,
                              data_frame_all_ticker_in_portfolio, money, kind_of_SL):

    list_of_tickers = [*list_of_companies.keys()]
    list_of_values_in_protfoilio = [*list_of_companies.values()]
    print('date_now:', date_now)
    for idx1, element10 in enumerate(list_of_tickers):
        print(element10)
        time = list_of_values_in_protfoilio[idx1][0]
        print(time, 'is the time!')

        check_data = list_of_values_in_protfoilio[idx1][4].strftime('%Y-%m-%d')
        check_data = check_data.replace('-', '')
        #print(check_data)

        print(data_frame_all_ticker_in_portfolio)

        if check_data == date_now:
            data_per_tick = data_frame_all_ticker_in_portfolio[
                (data_frame_all_ticker_in_portfolio['TimeBarStart'] > time) &
                (data_frame_all_ticker_in_portfolio['Date'] == date_now) &
                (data_frame_all_ticker_in_portfolio['Ticker'] == element10)][1:].reset_index(drop=True)
            print('haimi1')

        else:
            data_per_tick = data_frame_all_ticker_in_portfolio[
                (data_frame_all_ticker_in_portfolio['Date'] == date_now) &
                (data_frame_all_ticker_in_portfolio['Ticker'] == element10)].reset_index(drop=True)
            print('haimi2')

        #print(data_per_tick)
        print('price buyed:', list_of_values_in_protfoilio[idx1][2])

        if kind_of_SL == 'trailing':
            print('list_of_companies:', list_of_companies)
            kind_of_action, new_stop_loss_for_update = trailing_stop(list_of_tickers[idx1], data_per_tick, list_of_values_in_protfoilio[idx1],
                                                     important_arguments['stop_loss'], important_arguments['take_profit'])

            if (kind_of_action == 'SL') or (kind_of_action == 'TP'):
                print('price now:', new_stop_loss_for_update)
                if kind_of_action == 'SL':
                    print('stop_loss!')
                else:
                    print('Take_profit!')
                print('money:', money)
                print(new_stop_loss_for_update * int(list_of_values_in_protfoilio[idx1][3]))
                if model_name == 'beaten':
                    money = money + new_stop_loss_for_update * int(list_of_values_in_protfoilio[idx1][3])
                else:
                    money = money - new_stop_loss_for_update * int(list_of_values_in_protfoilio[idx1][3])
                print('money:', money)

                print('list_of_companies:', list_of_companies)
                list_of_companies.pop(element10)
                data_frame_all_ticker_in_portfolio = data_frame_all_ticker_in_portfolio.drop(
                    data_frame_all_ticker_in_portfolio
                    [data_frame_all_ticker_in_portfolio.Ticker == element10].index)


            else:
                print('Not SL')
                print(list_of_values_in_protfoilio[idx1])
                list_of_values_in_protfoilio[idx1][-1] = new_stop_loss_for_update
                print(list_of_values_in_protfoilio[idx1])

            print('list_of_companies:', list_of_companies)
            continue

        print(list_of_values_in_protfoilio[idx1][-1])
        if len([v for i, v in enumerate(data_per_tick['LastTradePrice']) if
                v < list_of_values_in_protfoilio[idx1][-1]]) > 0:
            price_close_position = [v for i, v in enumerate(data_per_tick['LastTradePrice']) if
                                    v < list_of_values_in_protfoilio[idx1][-1]][0]
            print('price now:', price_close_position)
            print('stop_loss!')
            print('money:', money)
            print(price_close_position * int(list_of_values_in_protfoilio[idx1][3]))
            if model_name == 'beaten':
                money = money + price_close_position * int(list_of_values_in_protfoilio[idx1][3])
            else:
                money = money - price_close_position * int(list_of_values_in_protfoilio[idx1][3])
            print('money:', money)

            print('list_of_companies:', list_of_companies)
            list_of_companies.pop(element10)
            data_frame_all_ticker_in_portfolio = data_frame_all_ticker_in_portfolio.drop(data_frame_all_ticker_in_portfolio
                [data_frame_all_ticker_in_portfolio.Ticker == element10].index)

            print('list_of_companies:', list_of_companies)
            continue

        #elif kind_of_SL != 'trailing':
        if len([v for i, v in enumerate(data_per_tick['LastTradePrice']) if
              v > list_of_values_in_protfoilio[idx1][-2]]) > 0:
            price_close_position = [v for i, v in enumerate(data_per_tick['LastTradePrice']) if
                                    v > list_of_values_in_protfoilio[idx1][-2]][0]
            print('price now:', price_close_position)
            print('take_profit!')
            print(price_close_position * int(list_of_values_in_protfoilio[idx1][3]))
            print('money:', money)
            if model_name == 'beaten':
                money = money + price_close_position * int(list_of_values_in_protfoilio[idx1][3])
            else:
                money = money - price_close_position * int(list_of_values_in_protfoilio[idx1][3])
            print('money:', money)
            print('list_of_companies:', list_of_companies)
            list_of_companies.pop(element10)
            data_frame_all_ticker_in_portfolio = data_frame_all_ticker_in_portfolio.drop(
                data_frame_all_ticker_in_portfolio
                [data_frame_all_ticker_in_portfolio.Ticker == element10].index)
            print('list_of_companies:', list_of_companies)

        print('continue to check')

    return list_of_companies, money, data_frame_all_ticker_in_portfolio

def trailing_stop(tick_name, data_per_tick, details_of_tick, percentage_of_trailing, percentage_take_profit):
    print(f'details_of_{tick_name}', details_of_tick)
    updated_sl = details_of_tick[-1]
    #print(data_per_tick['LastTradePrice'])
    #print(data_per_tick['HighTradePrice'])
    print('******')

    if model_name == 'beaten':

        for idx, (element1, element2) in enumerate(zip(data_per_tick['HighTradePrice'],
                                                                 data_per_tick['LastTradePrice'])):

            #print(element1, details_of_tick[2] * percentage_take_profit)

            if element1 > details_of_tick[2] * percentage_take_profit:
                return 'TP', element2

            if element1 > details_of_tick[2]:
                if element1 * percentage_of_trailing > updated_sl: #SL only can increase
                    print(idx)
                    updated_sl = element1 * percentage_of_trailing
                    print('new SL:', updated_sl)
                    print(f'change SL of {tick_name}!')
                    continue

            if element2 < updated_sl:
                print(f'The price arrived to SL, it is now {element2}')
                print(details_of_tick[2])
                print(f'profit of {(element2 - details_of_tick[2]) * details_of_tick[3]}')
                print(element2)
                time.sleep(2)
                return 'SL', element2

        return 'not change', updated_sl

    else:

        for idx, (element1, element2) in enumerate(zip(data_per_tick['LowTradePrice'],
                                                       data_per_tick['LastTradePrice'])):

            # print(element1, details_of_tick[2] * percentage_take_profit)

            if element1 < details_of_tick[2] * percentage_take_profit:
                return 'TP', element2

            if element1 < details_of_tick[2]:
                if element1 * percentage_of_trailing < updated_sl:  # SL only can increase
                    print(idx)
                    updated_sl = element1 * percentage_of_trailing
                    print('new SL:', updated_sl)
                    print(f'change SL of {tick_name}!')
                    continue

            if element2 > updated_sl:
                print(f'The price arrived to SL, it is now {element2}')
                print(details_of_tick[2])
                print(f'profit of {(element2 - details_of_tick[2]) * details_of_tick[3]}')
                print(element2)
                time.sleep(2)
                return 'SL', element2

        return 'not change', updated_sl


def calculate_return():
    pass


def calculate_value_tickers_in_protfolio(date_now, list_of_companies, data_frame_all_ticker_in_portfolio):
    list_of_tickers = [*list_of_companies.keys()]
    list_of_values_in_protfoilio = [*list_of_companies.values()]
    value_ticker_in_portfolio = None
    for idx2, i in enumerate(list_of_tickers):
        print(i)
        data_per_tick = data_frame_all_ticker_in_portfolio[
            (data_frame_all_ticker_in_portfolio['Date'] == date_now) &
            (data_frame_all_ticker_in_portfolio['Ticker'] == i) &
            (data_frame_all_ticker_in_portfolio['TimeBarStart'] <= 1559)].reset_index(drop=True)

        print(data_per_tick)
        try:
            price_end_of_date = data_per_tick['LastTradePrice'].iloc[-1]
            print('currecnt price:', price_end_of_date)
            print('purchase price:', list_of_values_in_protfoilio[idx2][2])

        except:
            price_end_of_date = list_of_values_in_protfoilio[idx2][2] #the same price
            print('speical_price')

        try:
            print(value_ticker_in_portfolio)
            value_ticker_in_portfolio = value_ticker_in_portfolio + float(price_end_of_date * list_of_values_in_protfoilio[idx2][3])
            print(value_ticker_in_portfolio)
        except:
            print(value_ticker_in_portfolio)
            value_ticker_in_portfolio = float(price_end_of_date * list_of_values_in_protfoilio[idx2][3])
            print(value_ticker_in_portfolio)


    print('value_ticker_in_portfolio:', value_ticker_in_portfolio)
    return value_ticker_in_portfolio


check_protfolio_value = False

number_of_ticker_were_buyed = 0

while True:
    for index, first_element in enumerate(
            zip(signals_data['date'], signals_data['symbol'], signals_data['time'], signals_data['bmo-last_day_close_price / amc-this_day_close_price'],
             signals_data['price_immeditaly_after_filings'], signals_data['bmo-this_day_close_price / amc-next_day_close_price'],
             signals_data['hour'], signals_data['two_beat'], signals_data['percentage_95_week_after'], signals_data['first_time_of_trading'])):

        print(first_element)

        dont_check = False
        if index > 0:
            if (index % 40) == 0:
                print('now its ready!')
                check_protfolio_value = True

        if first_element[7] != 1:
            continue
            #dont_check = True

        if pd.isna(first_element[8]): # because adsk 17/6/2017. something wrong there
            continue

        if pd.isna(first_element[4]):
            continue

        #if pd.isna(first_element[4]):
        #    first_element = list(first_element)
        #    print(first_element)
        #    #tt = first_element[9]
        #    #first_element[4] = tt
        #    first_element[4] = first_element[9]
        #    first_element = tuple(first_element)
        #    print(first_element)
        #    print('change')

        if model_name == 'beaten':
            if first_element[3] > first_element[4]:
                continue
        else:
            if first_element[3] < first_element[4]:
                continue

        while True:
            try:
                if  date_today == first_element[0]:
                    print(first_element[1])
                    relevant_data = pd.read_csv(path + f"\\stocks_one_minute_by_ticker\\{first_element[1]}.csv")
                    relevant_data['TimeBarStart'] = [int(date1.replace(':', ''))
                                                     for date1 in relevant_data['TimeBarStart']]

                    relevant_data['Date'] = [str(date1) for date1 in relevant_data['Date']]

                    try:
                        unique_dates = pd.Series(relevant_data['Date'].unique()).tolist()

                        #get the indexes of this day
                        index_day = [i for i, x in enumerate(relevant_data['Date']) if x == date_today][0]
                        print(index_day)
                        relevant_data = relevant_data.loc[index_day:].reset_index(drop=True)

                    except Exception as e:
                        print(e)

                    try:
                        if index == 0:
                           data_frame_all_ticker_in_portfolio = relevant_data

                        else:
                            data_frame_all_ticker_in_portfolio = pd.concat([data_frame_all_ticker_in_portfolio, relevant_data], ignore_index=True)

                    except Exception as e:
                              print(e)

                    #print(data_frame_all_ticker_in_portfolio)
                    amount_this_purchase = math.floor(int(important_arguments['money_per_stock'])/float(first_element[4]))
                    #print(amount_this_purchase)
                    #print(float(first_element[4]))
                    if money >= (first_element[4] * amount_this_purchase):

                        this_specific_time = int(first_element[2].replace(':', ''))
                        #print(this_specific_time)
                        list_of_companies[first_element[1]] = [this_specific_time, 'buy', first_element[4],
                                amount_this_purchase, pd.to_datetime(date_today, format='%Y%m%d').date(),
                                first_element[4] * important_arguments["take_profit"], first_element[4]
                                                               * important_arguments["stop_loss"]]
                        print('added company to the protfolio!')
                        number_of_ticker_were_buyed = number_of_ticker_were_buyed + 1
                        print('Total number_of_ticker_were_buyed:', number_of_ticker_were_buyed)
                        print('list_of_companies:', list_of_companies)
                        print('money:', money)
                        if model_name == 'beaten':
                            money = money - (first_element[4] * amount_this_purchase)
                        else:
                            money = money + (first_element[4] * amount_this_purchase)
                        print('money:', money)

                    else:
                        list_of_companies_not_buyed_because_lack_money[first_element[1]] = ['buy', first_element[4],
                                        amount_this_purchase, pd.to_datetime(date_today, format='%Y%m%d').date()]
                        print('list_of_companies_not_buyed_because_lack_money:',
                              list_of_companies_not_buyed_because_lack_money)
                    break

                else:
                    previous_day = date_today
                    idx_date_today = idx_date_today + 1
                    date_today = dates_of_exchange[idx_date_today]

                    #previous_day = date_today
                    #date_today = pd.to_datetime(date_today, format='%Y%m%d').date()
                    #date_today = date_today + timedelta(days=1)
                    #date_today = date_today.strftime('%Y-%m-%d')
                    #date_today = date_today.replace('-', '')
                    print('date_now_1:', date_today)

                    if len(list_of_companies) > 0:
                        print([*list_of_companies.values()])
                        list_of_values_in_protfoilio = [*list_of_companies.values()]
                        print('list_of_companies', [*list_of_companies.keys()])
                        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                        print(first_element[0], previous_day, list_of_companies)
                        list_of_companies, money, data_frame_all_ticker_in_portfolio = check_stoploss_takeprofit(
                            previous_day,
                            list_of_companies, data_frame_all_ticker_in_portfolio, money, 'trailing')

                        print(list_of_companies)

                        if check_protfolio_value == True:
                            value_of_tickers = calculate_value_tickers_in_protfolio(previous_day, list_of_companies,
                                                                                    data_frame_all_ticker_in_portfolio)
                            if model_name == 'beaten':
                                print('money cash:', money)
                                print(f'date of checking is {previous_day}')
                                print('value_of_tickers:', value_of_tickers)
                                print('Total_value:', value_of_tickers + money)
                                print('^^^^^^^^^^^^^^^^^^^^')
                                check_protfolio_value = False

                            else:
                                print('money cash:', money)
                                print(f'date of checking is {previous_day}')
                                print('value_of_tickers:', value_of_tickers)
                                print('Total_value:',  money - value_of_tickers )
                                print('^^^^^^^^^^^^^^^^^^^^')
                                check_protfolio_value = False
                    #break
                    continue

            except Exception as e:
                print(e)
                print('problem')
                time.sleep(30)
