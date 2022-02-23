import warnings
from datetime import datetime as dt, timedelta
import math
import json
import pandas as pd
import numpy as np
from functions_for_TA_running import *
import matplotlib.pyplot as plt
from analyze_data_TA_strategy import*
import time
from Serious_Build_model_technial_analysis import *
import os
import glob
#print(os.getcwd())
#os.chdir('C:\\Users\\User\\Desktop\\Work_Adi\\scripts_algo')
#print(os.getcwd())
from relevant_index_return import *

def choose_company(com1, build_data_for_model):
    try:
        my_ohlc_data_first = pd.read_csv(f'C:\\Users\\User\\Desktop\Work_Adi\\daily_data_tickers_breakaway_model\\{com1}.csv')
    except:
        return 'lack_of_data'

    try:
        for_check = pd.read_csv(f'C:\\Users\\User\\Desktop\\Work_Adi\\actually_earnings\\{com1}.csv')
        print(for_check)
    except:
        return 'lack_of_data'

    #try:
    #    for_check0 = pd.read_csv(
    #        f'C:\\Users\\User\\Desktop\Work_Adi\\daily_data_tickers_breakaway_model\\{relevant_index}.csv')
    #    print(for_check0)
    #except:
    #    return 'lack_of_data'

    my_ohlc_data_first = my_ohlc_data_first[-1300:-700]#[-1000:-487] #.tail(486)
    my_ohlc_data = my_ohlc_data_first.iloc[:, 1:6]
    # Converting to Array
    my_ohlc_data = np.array(my_ohlc_data)
    print(my_ohlc_data_first)

    # add 3 columns
    my_ohlc_data = adder(my_ohlc_data, 3)

    #add 3 Moving Avreage
    my_ohlc_data = ma(my_ohlc_data, 20, 3, 5)
    my_ohlc_data = ma(my_ohlc_data, 50, 3, 6)
    my_ohlc_data = ma(my_ohlc_data, 200, 3, 7)

    # Converting to Array
    #my_ohlc_data_first = my_ohlc_data_first[-1028:-360]#.tail(360)
    print(my_ohlc_data_first)

    close1 = my_ohlc_data_first['Close'].tolist()
    open1 = my_ohlc_data_first['Open'].tolist()
    low1 = my_ohlc_data_first['Low'].tolist()
    high1 = my_ohlc_data_first['High'].tolist()
    date1 = my_ohlc_data_first['Date'].tolist()

    #position_active = None
    steps = 6
    list_of_min_max_points = []
    list_of_resistence = []
    list_of_support = []
    #lst_sup_points = []
    lst_sup_for_chart = []
    #lst_res_points = []
    lst_res_for_chart = []
    sup_break = []
    res_break = []
    fail_sup_break = []
    fail_res_break = []
    runaway_lis = []
    mivne_mehirim_vector_positions = []
    for index1 in range(1, len(close1)+1):
        if index1 <steps:
            continue
        print(index1)
        close_check = close1[(index1 - steps):index1]
        open_check = open1[(index1 - steps):index1]
        low_check = low1[(index1 - steps):index1]
        high_check = high1[(index1 - steps):index1]
        date_check = date1[(index1 - steps):index1]
        print(date_check)

        try:
            print('4441')
            print(mivne_mehirim_vector_positions)

        except:
            print('No position_active check because lower than 3 signals until now')
            #mivne_mehirim_vector_positions.append(['lower than 3 signals', 'no intresting', index1-1, date1[-1]])

        try:
            a = find_max_min_points1(list_of_min_max_points, close_check, open_check, low_check, high_check, date_check, (steps//2)+1, index1)
            print(a)
            if a != "no_minmax":
                list_of_min_max_points.append(a)

                res, lst_res_for_chart1 = resistence1(list_of_min_max_points)
                print(lst_res_for_chart1)
                print(res)
                print('resistence-', list_of_resistence)
                if lst_res_for_chart1 != 'no_resist2':

                    if len(lst_res_for_chart) > 0:
                        print(lst_res_for_chart1[2])
                        print(lst_res_for_chart[-1][2])
                        if lst_res_for_chart1 not in lst_res_for_chart:
                            #if ((lst_res_for_chart1[2]/lst_res_for_chart[-1][2]) > 1.03) or\
                            #        ((lst_res_for_chart1[2]/lst_res_for_chart[-1][2]) < 0.97):
                                lst_res_for_chart.append(lst_res_for_chart1)
                                #print('lst_res_for_chart after adding', lst_res_for_chart)

                            #else:
                            #    print('&&')
                            #    print(res[1])
                            #    print(lst_res_for_chart)
                            #    print(lst_res_for_chart[-1])
                            #    lst_res_for_chart[-1][1] = res[1]
                            #    lst_res_for_chart[-1][2] = (res[0] + lst_res_for_chart[-1][2])/2
                            #    print('**&123')
                            #    print(lst_res_for_chart)

                        print('lst_res_for_chart after adding', lst_res_for_chart)

                    #else:
                        #if...
                    elif lst_res_for_chart1 not in lst_res_for_chart:
                            lst_res_for_chart.append(lst_res_for_chart1)
                            print('lst_res_for_chart after adding', lst_res_for_chart)

                if res != 'no_resist1':
                    print(res)
                    print(list_of_resistence)

                    if [lst_res_for_chart1[2], res[1]] not in list_of_resistence:
                        list_of_resistence.append([lst_res_for_chart1[2], res[1]])
                        print('resistance after adding', list_of_resistence)

                sup, lst_sup_for_chart1 = support1(list_of_min_max_points)
                print(lst_sup_for_chart1)
                print(sup)
                print('support:', list_of_support)
                if lst_sup_for_chart1 != 'no_resist2':

                    if lst_sup_for_chart1 not in lst_sup_for_chart:
                        lst_sup_for_chart.append(lst_sup_for_chart1)
                        print('lst_sup_for_chart after adding', lst_sup_for_chart)

                if sup != 'no_resist1':
                    print(sup)
                    print(list_of_support)
                    if sup not in list_of_support:
                        list_of_support.append((sup))
                        print('support after adding:', list_of_support)

            # Breakaway
            #index_breakaway_point, value_breakaway_point, kind_of_break, line_broken, last_low_or_high = Breakaway(index1, list_of_resistence,
            #                                    list_of_support, low_check, high_check, open_check, low1, high1, steps)

            index_breakaway_point, value_breakaway_point, kind_of_break, line_broken, last_low_or_high,\
            index_end_brokenned, indexes_of_touched,close_new_point, high_or_low_new_point = Breakaway(
                index1, lst_res_for_chart, lst_sup_for_chart, low_check, high_check, open_check, low1, high1, close_check, steps)

            if kind_of_break == 'break_sup':
                sup_break.append([index_breakaway_point, value_breakaway_point, date_check[-1], com1, kind_of_break, line_broken, last_low_or_high, index_end_brokenned, indexes_of_touched,close_new_point, high_or_low_new_point])
            elif kind_of_break == 'break_res':
                res_break.append([index_breakaway_point, value_breakaway_point, date_check[-1], com1, kind_of_break, line_broken, last_low_or_high, index_end_brokenned, indexes_of_touched,close_new_point, high_or_low_new_point])

            elif kind_of_break =='fail_break_sup':
                fail_sup_break.append([index_breakaway_point, value_breakaway_point, date_check[-1], com1, kind_of_break, line_broken, last_low_or_high, index_end_brokenned, indexes_of_touched,close_new_point, high_or_low_new_point])

            elif kind_of_break == 'fail_break_res':
                fail_res_break.append([index_breakaway_point, value_breakaway_point, date_check[-1], com1, kind_of_break, line_broken, last_low_or_high, index_end_brokenned, indexes_of_touched,close_new_point, high_or_low_new_point])

            # Runaway
            runaway_value = Runaway(low_check, high_check, 2)
            if runaway_value == 'increasing_runaway':
                runaway_lis.append([index1 - 1, close_check[-1], runaway_value])
            elif runaway_value == 'decreasing_runaway':
                runaway_lis.append([index1 - 1, close_check[-1], runaway_value])

            # Mivne_mehirim
            mivne_mehirim_position, price_if_interesting, index123, vector_of_relevant_min_max_points_until_it_included, date_event = mivne_mehirim(list_of_min_max_points, index1, low_check, high_check, open_check, close_check, date_check) #index1-(steps//2)
            mivne_mehirim_vector_positions.append([mivne_mehirim_position, price_if_interesting, index123, date_event, com1])
            print([mivne_mehirim_position, price_if_interesting, index123])

            print('$$$$$$$$$$$$$')
            print(lst_res_for_chart)
            firsts = [a[0] for a in lst_res_for_chart]  # merge if first number is the same
            lasts = [a[1] for a in lst_res_for_chart] #only for count touch
            print(firsts)
            print(lasts)
            while True:
                one_changed = False
                for idx2, ele1 in enumerate(firsts):
                    for idx3, ele2 in enumerate(firsts[idx2 + 1:]):
                        if ele1 == ele2:
                            print(idx2)
                            print(idx3)
                            print(lst_res_for_chart[idx2])
                            number_of_touches = lst_res_for_chart[idx2][-1]
                            print(number_of_touches)
                            print(lasts[idx2 + idx3+1])

                            if lasts[idx2 + idx3 + 1] not in lst_res_for_chart[idx2][-1]:
                                number_of_touches.append(lasts[idx2 + idx3+1])


                            lst_res_for_chart[idx2] = [lst_res_for_chart[idx2][0],
                                                       lst_res_for_chart[idx2 + idx3 + 1][1],
                                                       ((lst_res_for_chart[idx2][2]) + (
                                                       lst_res_for_chart[idx2 + idx3 + 1][2])) / 2, number_of_touches]

                            lst_res_for_chart.pop(idx2 + idx3 + 1)
                            firsts.pop(idx2)
                            print(lst_res_for_chart)
                            one_changed = True
                            break

                    if one_changed:
                        break

                if one_changed:
                    continue
                else:
                    break

            print(lst_res_for_chart)

            firsts = [a[0] for a in lst_res_for_chart]
            lasts = [a[1] for a in lst_res_for_chart]  # merge if second number is the same
            print(lasts)
            while True:
                one_changed = False
                for idx2, ele1 in enumerate(lasts):
                    num_of_touch = lst_res_for_chart[idx2][-1]
                    for idx3, ele2 in enumerate(lasts[idx2 + 1:]):
                        if ele1 == ele2:

                            print(idx2)
                            print(lst_res_for_chart[idx2])

                            if firsts[idx2 + idx3 + 1] not in lst_res_for_chart[idx2][-1]:
                                num_of_touch.append(lasts[idx2 + idx3 + 1])

                            lst_res_for_chart[idx2] = [lst_res_for_chart[idx2][0],
                                                       lst_res_for_chart[idx2 + idx3 + 1][1],
                                                       ((lst_res_for_chart[idx2][2]) + (
                                                           lst_res_for_chart[idx2 + idx3 + 1][2])) / 2, num_of_touch]
                            lst_res_for_chart.pop(idx2 + idx3 + 1)
                            lasts.pop(idx2)
                            print(lst_res_for_chart)
                            one_changed = True
                            break

                    if one_changed:
                        break

                if one_changed:
                    continue
                else:
                    break

            print(lst_res_for_chart)

            while True:
                again = False
                for idx1, ii in enumerate(lst_res_for_chart):
                    print(idx1)
                    check = lst_res_for_chart[idx1]
                    print(check, '*')
                    for idx, element in enumerate(lst_res_for_chart[idx1 + 1:]): #end of obs, equal to its following.
                        print(ii[1], element)
                        if ii[1] == element[0]:
                            relevant_obs = lst_res_for_chart[idx1][-1]
                            print(lst_res_for_chart[idx1][-1])

                            if lasts[idx1 + idx + 1] not in lst_res_for_chart[idx1][-1]:
                                relevant_obs.append(lasts[idx1 + idx + 1])

                            print(relevant_obs)
                            new_res = (check[2] + element[2]) / 2
                            new_point = [check[0], element[1], new_res, relevant_obs]
                            lst_res_for_chart[idx1] = new_point
                            lst_res_for_chart.pop(idx + idx1 + 1)
                            again = True
                            print(lst_res_for_chart)
                if not again:
                    break
            print(lst_res_for_chart)

            while True:  # If pair of points are overlap (not absolutly..), and values max 1%)
                one_changed = False
                for idx2, ele1 in enumerate(lst_res_for_chart):
                    num_of_touch = lst_res_for_chart[idx2][-1]
                    for idx3, ele2 in enumerate(lst_res_for_chart[idx2 + 1:]):
                        print(ele1, ele2)
                        print(((abs(ele1[2] / ele2[2])) < 1.02) and (abs(ele1[2] / ele2[2])) > 0.98)
                        print(((ele1[1] < ele2[1]) and (ele1[1] > ele2[0])))
                        print((ele1[0] > ele2[0]) and (ele1[0] < ele2[1]))
                        if (((abs(ele1[2] / ele2[2])) < 1.02) and (abs(ele1[2] / ele2[2])) > 0.98) and\
                                (((ele1[1] < ele2[1]) and (ele1[1] > ele2[0]) and (ele1[0] < ele2[0])) or
                                                                  (ele1[0] > ele2[0]) and (ele1[0] <ele2[1]) and (ele1[1] > ele2[1]) ):
                            print(idx2)
                            print(lst_res_for_chart[idx2])
                            print(lst_res_for_chart[-1])
                            last_point = lst_res_for_chart[-1][-1]  # I need both, because two of them can be inside the line
                            for num in last_point:
                                if num not in lst_res_for_chart[idx2][-1]:

                                    num_of_touch.append(num)
                                    print(num_of_touch)
                                    print(num)

                                    lst_res_for_chart[idx2] = [lst_res_for_chart[idx2][0],
                                                               lst_res_for_chart[idx2 + idx3 + 1][1],
                                                               ((lst_res_for_chart[idx2][2]) + (
                                                                   lst_res_for_chart[idx2 + idx3 + 1][2])) / 2, num_of_touch]

                            lst_res_for_chart.pop(idx2 + idx3 + 1)
                            print(lst_res_for_chart)
                            one_changed = True
                            break

                    if one_changed:
                        break

                if one_changed:
                    continue
                else:
                    break


            while True:  # If pair of points are overlap (not absolutly..), and values max 1%)
                one_changed = False
                for idx2, ele1 in enumerate(lst_res_for_chart):
                    num_of_touch = lst_res_for_chart[idx2][-1]
                    for idx3, ele2 in enumerate(lst_res_for_chart[idx2 + 1:]):
                        print(ele1[2], ele2[2], ')(*')
                        if (((abs(ele1[2] / ele2[2])) < 1.02) and (abs(ele1[2] / ele2[2])) > 0.98):
                            if ele1[1] < ele2[0]:

                                if any(hig > max((ele1[2]), ele2[2]) * 1.025 for hig in high1[ele1[1]+1:ele2[0]]):
                                    continue

                                else:
                                    print(num_of_touch)
                                    for i in ele2[0:2]:
                                        num_of_touch.append(i)
                                    print(num_of_touch)

                                    lst_res_for_chart[idx2] = [lst_res_for_chart[idx2][0],
                                                               lst_res_for_chart[idx2 + idx3 + 1][1],
                                                               ((lst_res_for_chart[idx2][2]) + (
                                                                   lst_res_for_chart[idx2 + idx3 + 1][2])) / 2,
                                                               num_of_touch]

                                lst_res_for_chart.pop(idx2 + idx3 + 1)
                                print(lst_res_for_chart)
                                one_changed = True
                        else:
                            continue

                    if one_changed:
                        break
                if one_changed:
                    continue
                else:
                    break

            print('&&&&&&&&&&&')

            print(lst_sup_for_chart, '%%%')
            firsts = [a[0] for a in lst_sup_for_chart]
            lasts = [a[1] for a in lst_sup_for_chart]
            print(firsts)
            while True:
                one_changed = False
                for idx2, ele1 in enumerate(firsts):
                    for idx3, ele2 in enumerate(firsts[idx2 + 1:]):
                        if ele1 == ele2:
                            print(idx2)
                            print(lst_sup_for_chart[idx2])
                            print(lst_sup_for_chart[idx2][0])
                            number_of_touches = lst_sup_for_chart[idx2][-1]

                            if lasts[idx2 + idx3 + 1] not in lst_sup_for_chart[idx2][-1]:
                                number_of_touches.append(lasts[idx2 + idx3+1])

                            lst_sup_for_chart[idx2] = [lst_sup_for_chart[idx2][0],
                                                       lst_sup_for_chart[idx2 + idx3 + 1][1],
                                                       ((lst_sup_for_chart[idx2][2]) + (
                                                       lst_sup_for_chart[idx2 + idx3 + 1][2])) / 2, number_of_touches]
                            lst_sup_for_chart.pop(idx2 + idx3 + 1)
                            firsts.pop(idx2)
                            print(lst_sup_for_chart)
                            one_changed = True
                            break

                    if one_changed:
                        break

                if one_changed:
                    continue
                else:
                    break

            print(lst_sup_for_chart)

            lasts1 = [a[1] for a in lst_sup_for_chart]
            print(lasts1)
            while True:
                one_changed = False
                for idx2, ele1 in enumerate(lasts1):
                    num_of_touch = lst_sup_for_chart[idx2][-1]
                    for idx3, ele2 in enumerate(lasts1[idx2 + 1:]):
                        if ele1 == ele2:
                            print(idx2)
                            print(lst_sup_for_chart[idx2])
                            print(lst_sup_for_chart[idx2][0])

                            if firsts[idx2 + idx3 + 1] not in lst_sup_for_chart[idx2][-1]:
                                num_of_touch.append(lasts[idx2 + idx3 + 1])

                            lst_sup_for_chart[idx2] = [lst_sup_for_chart[idx2][0],
                                                       lst_sup_for_chart[idx2 + idx3 + 1][1],
                                                       ((lst_sup_for_chart[idx2][2]) + (
                                                       lst_sup_for_chart[idx2 + idx3 + 1][2])) / 2, num_of_touch]
                            lst_sup_for_chart.pop(idx2 + idx3 + 1)
                            lasts1.pop(idx2)
                            print(lst_sup_for_chart)
                            one_changed = True
                            break

                    if one_changed:
                        break

                if one_changed:
                    continue
                else:
                    break

            print(lst_sup_for_chart)


            while True:
                again = False
                for idx1, ii in enumerate(lst_sup_for_chart):
                    print(idx1)
                    check = lst_sup_for_chart[idx1]
                    print(check, '%')
                    for idx, element in enumerate(lst_sup_for_chart[idx1 + 1:]):
                        print(ii[1], element)
                        if ii[1] == element[0]:
                            relevant_obs = lst_sup_for_chart[idx1][-1]
                            if lasts[idx1 + idx + 1] not in lst_sup_for_chart[idx1][-1]:
                                relevant_obs.append(lasts[idx1 + idx + 1])
                            new_sup = (check[2] + element[2]) / 2
                            new_point = [check[0], element[1], new_sup, relevant_obs]
                            print(new_point)
                            lst_sup_for_chart[idx1] = new_point
                            lst_sup_for_chart.pop(idx + idx1 + 1)
                            print(lst_sup_for_chart)
                            again = True
                if not again:
                    break

            print('^^^^^^^^^')
            while True:
                one_changed = False
                for idx2, ele1 in enumerate(lst_sup_for_chart):
                    num_of_touch = lst_sup_for_chart[idx2][-1]
                    for idx3, ele2 in enumerate(lst_sup_for_chart[idx2 + 1:]):

                        if (((abs(ele1[2] / ele2[2])) < 1.02) and (abs(ele1[2] / ele2[2])) > 0.98) and \
                                (((ele1[1] < ele2[1]) and (ele1[1] > ele2[0]) and (ele1[0] < ele2[0])) or
                                 (ele1[0] > ele2[0]) and (ele1[0] < ele2[1]) and (ele1[1] > ele2[1])):
                            print(idx2)
                            print(lst_sup_for_chart[idx2])
                            last_point = lst_sup_for_chart[-1][-1]

                            for num in last_point:
                                if num not in lst_sup_for_chart[idx2][-1]:
                                    num_of_touch.append(num)
                                    print(num_of_touch)

                                    lst_sup_for_chart[idx2] = [lst_sup_for_chart[idx2][0],
                                                       lst_sup_for_chart[idx2 + idx3 + 1][1],
                                                       ((lst_sup_for_chart[idx2][2]) + (
                                                           lst_sup_for_chart[idx2 + idx3 + 1][2])) / 2, num_of_touch]

                            lst_sup_for_chart.pop(idx2 + idx3 + 1)
                            print(lst_sup_for_chart)
                            one_changed = True
                            break

                    if one_changed:
                        break

                if one_changed:
                    continue
                else:
                    break


            while True:  # If pair of points are overlap (not absolutly..), and values max 1%)
                one_changed = False
                for idx2, ele1 in enumerate(lst_sup_for_chart):
                    num_of_touch = lst_sup_for_chart[idx2][-1]
                    for idx3, ele2 in enumerate(lst_sup_for_chart[idx2 + 1:]):
                        #print(ele1[2], ele2[2], '(())*')
                        if (((abs(ele1[2] / ele2[2])) < 1.02) and (abs(ele1[2] / ele2[2])) > 0.98):

                            if ele1[1] < ele2[0]:

                                if any(lo1 < min((ele1[2]), ele2[2]) * 0.975 for lo1 in low1[ele1[1]+1:ele2[0]]):
                                    continue

                                else:
                                    print(num_of_touch)
                                    for i in ele2[0:2]:
                                        num_of_touch.append(i)
                                    print(num_of_touch)

                                    lst_sup_for_chart[idx2] = [lst_sup_for_chart[idx2][0],
                                                               lst_sup_for_chart[idx2 + idx3 + 1][1],
                                                               ((lst_sup_for_chart[idx2][2]) + (
                                                                   lst_sup_for_chart[idx2 + idx3 + 1][2])) / 2,
                                                               num_of_touch]

                                lst_sup_for_chart.pop(idx2 + idx3 + 1)
                                print(lst_sup_for_chart)
                                one_changed = True
                        else:
                            continue

                    if one_changed:
                        break
                if one_changed:
                    continue
                else:
                    break

            if len(list_of_min_max_points) > 0:
                print('list_of_min_max_points:', list_of_min_max_points)
                print('list_of_resistence:', list_of_resistence)
                print('list_of_support:', list_of_support)
                print('lst_res_for_chart:', lst_res_for_chart)
                print('lst_sup_for_chart:', lst_sup_for_chart)
                print('***********')
        except:
                print('problem!')
                continue

    print("########################################")
    print(list_of_min_max_points)
    print('list of resistence:', list_of_resistence)
    print('list of support:', list_of_support)

    #plot charts
    #plt.xticks(np.arange(0, 150, 50))
    print('lst_res_for_chart:', lst_res_for_chart)
    print('lst_sup_for_chart:', lst_sup_for_chart)
    print(runaway_lis)
    print('*&*&*&*&*')
    print(sup_break)
    print(res_break)
    print(fail_sup_break)
    print(fail_res_break)
    print(list_of_min_max_points)

    print('mivne_mehirim_vector_positions:', mivne_mehirim_vector_positions)


    if build_data_for_model == 'build_breakaway_model_data':
        lst_this_model = []
        for idx1, ele in enumerate([res_break, sup_break, fail_sup_break, fail_res_break]):
            print(ele)
            if len(ele) > 0:
                for element in ele:
                    print(element)
                    print('HHA')

                    #print(breakaway_model(my_ohlc_data_first, 20, my_ohlc_data, element, open_check,
                    #close_check, high_check, low_check, mivne_mehirim_vector_positions)) #sup_break, res_break,

                    breakaway_model_values = breakaway_model(my_ohlc_data_first, 20, my_ohlc_data, element, open_check,
                    close_check, high_check, low_check, mivne_mehirim_vector_positions, list_of_min_max_points)

                    print('vieder', breakaway_model_values)
                    lst_this_model.append([element[2], element[4], com1, list(breakaway_model_values)])

                    pass
            else:
                continue
        print(lst_this_model)

        if len(lst_this_model) == 1:
            return lst_this_model[0]

        return lst_this_model

    #ohlc_plot(com1, my_ohlc_data, 350, list_of_min_max_points, lst_res_for_chart, lst_sup_for_chart, sup_break, res_break, mivne_mehirim_vector_positions, runaway_lis)
    #plot_chart(com1, my_ohlc_data_first, 350, my_ohlc_data, list_of_min_max_points, lst_res_for_chart, lst_sup_for_chart, sup_break, res_break, mivne_mehirim_vector_positions, runaway_lis)

def flatten_list_element_from_list(big_list):
    new_list = []
    for element in big_list:

        print(element)
        if type(element) is not list:
            print(element)
            new_list.append(element)
        else:
            for i in element:
                print(i)
                new_list.append(i)
    return new_list


#choose_company('CRM', 'build_breakaway_model_data')

#com = ['CRM', 'NKE','DIS', 'ZBRA','AAPL']
com = ['MSFT', 'AXP', 'ADSK','A', 'MU', 'ZM','CRM', 'PEP', 'T', 'ADBE', 'AVGO', 'NFLX', 'FB', 'CSCO', 'F', 'AMD',  'A', 'AA'
       , 'CRM', 'NIO', 'AMZN', 'JPM', 'AAL', 'DIS', 'ZBRA', 'ROKU', 'DISH', 'NKE', 'NVDA', 'AAPL', 'QCOM', 'ADI', 'KO'] #'TSM',

#payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
#first_table = payload[0]
#second_table = payload[1]

#symbols_sp500 = first_table['Symbol'].values.tolist()
#print(symbols_sp500)

directory = os.getcwd()

os.chdir('C:\\Users\\User\\Desktop\\Work_Adi\\earnings_new') #actually_earnings')

print(directory)
extension = 'csv'

names_result = [ele.split('.')[0] for ele in glob.glob('*.{}'.format(extension))]
print(names_result)
print(len(names_result))

os.chdir('C:\\Users\\User\\Desktop\\Work_Adi\\daily_data_tickers_breakaway_model')
#names_result = [ele.split('.')[0] for ele in glob.glob('*.{}'.format(extension))]


'''
#keep = True
for symbol in names_result:
    #if keep:
    #    if symbol != 'SHOO':
    #        continue
    #    else:
    #        keep = False
    #print(symbol)
    if not os.path.exists(f"{symbol}.csv"):

        time.sleep(1)
        loop = 0
        while loop < 1:
            daily_data = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=1420070400&period2=1643673600&interval=1d&events=history&includeAdjustedClose=true'
            print(daily_data)
            try:
                df = pd.read_csv(daily_data).set_index('Date')
                df.to_csv(f'{symbol}.csv')
                print(df)
                print('***')
                break
            except:
                loop = loop + 1
                print('error')
                continue

'''
lst = []
start = 988

while True:
    for element123 in names_result[start:start+10]:
        #print(element123)

        #if element123 in ['GOOG', 'BBWI', 'BRK.B', 'MTCH','JPM']:
        #    continue

        #if element123 in ['MMM', 'AOS', 'ABT', 'ABBV', 'ABMD']:
        #    continue

    #for element123 in ['CDNS']: # ['RL']
        details = choose_company(element123, 'build_breakaway_model_data')

        if details == 'lack_of_data':
            continue

        if len(details) == 0:
            continue

        print(element123)
        print(details)

        if ((len(details) > 1) and type(details[0]) == list):
            for el in details:
                print(el)
                el = flatten_list_element_from_list(el)
                print(el)
                lst.append(el)
                print(lst)

        else: #  if details[0][2] == element123:
            details = flatten_list_element_from_list(details)
            lst.append(details)
            print(lst)

        print(len(lst))

    columns = ['Date', 'break_kind', 'ticker', 'volume_location','volume_tomorrow_location', 'return_day_after_breakaway','rsi_today', 'change_rsi_end_of_the day',
               'percentage_of_broken_resistence_or_support', 'mivne_mehirim', 'change_eps_from_previous_report_eps',
               'change_revenue_from_previous_report_revenue', 'change_eps_from_previous_year_eps', 'change_revenue_from_previous_year_revenue',
               'time_after_last_report', 'today eps actually', 'today eps estimated', 'today revenue actually','today revenue estimated',
               'AMC/BMO', 'hour', 'spy_return', 'vxx_retrun', 'sector', 'capitalization', 'change_return_sector_lastday', 'gap_long','gap_long_next_open',
               'location_our_gap_compare_x_days_before', 'time_past_from_end_of_support', 'how_much_touch', 'lentgh_of_line','target', 'return_position','Date_close_position',
               'stop_loss', 'price_enter_to_position', 'Take_profit']

    ss = pd.DataFrame(lst, columns=columns)
    ss.to_csv(f'C:\\Users\\User\\Desktop\\Work_Adi\\data_created_of_{start}new_ev_obs_breakaway_model_02_16.csv')
    time.sleep(5)
    start = start + 10
    if start >= 7000:
        break

'''
date_today = '30/05/2017'
lst1 = []
for idx1, i in enumerate(com):
       print(i)
       list_movne_mehirim = choose_company(i)
       for element in list_movne_mehirim:
            lst1.append(element)
       print('$$123')
       if idx1 == 1:
              break
columns = ["mivne", "value", "number_of_day", "date", 'ticker']
df = pd.DataFrame(lst1, columns=columns)
df.to_csv('C:\\Users\\User\\Desktop\\Work_Adi\\scripts_algo\\technical_analysis\\rrr3.csv', index=False)

data_general_signal = pd.read_csv('C:\\Users\\User\\Desktop\\Work_Adi\\scripts_algo\\technical_analysis\\rrr.csv')
print(data_general_signal)

data_general_signal['date'] = [pd.to_datetime(date1, format='%d/%m/%Y').date() for date1 in data_general_signal['date']]
data_general_signal['date'] =  [date1.strftime('%Y-%m-%d') for date1 in data_general_signal['date']]
dates = pd.read_csv(f'C://Users//User//Downloads//MU.csv', usecols=['Date'])
print(dates)

money = 100000
pass_row_dates_signal = 0
lst_tic_in_portfolio = []
lst_return_upper = []
lst_return_lower = []

for element in dates.values.tolist(): #dates of trading
    print('$$', element)

    for index, row in data_general_signal[pass_row_dates_signal:].iterrows(): #dates signal
        #print(row['date'], element[0])
        #print(type(row['date']), type(element[0]))

        #pass_row_dates_signal = pass_row_dates_signal + index

        print(data_general_signal[pass_row_dates_signal:])

        if row['date'] == element[0]:
            dt1 = row['date']
            print(dt1, 'haimi')
            #print(row['ticker'], row['value'], row['mivne'])
            tic = row['ticker']
            relevant_data = pd.read_csv(f'C://Users//User//Downloads//{tic}.csv')
            try:
                print(tic)
                relevant_data['Date'] = [pd.to_datetime(date1, format='%d/%m/%Y').date() for date1 in
                                               relevant_data['Date']]
                relevant_data['Date'] = [date1.strftime('%Y-%m-%d') for date1 in relevant_data['Date']]

            except:
                pass

            print('%%^')
            #print(relevant_data)
            #print(relevant_data['Date'].values)
            #print(type(relevant_data['Date'].iloc[0]))
            idx_date_today = relevant_data['Date'].values.tolist().index(dt1)
            #print(idx_date_today)
            relevant_data = relevant_data.loc[idx_date_today:idx_date_today+1] #its 2 because in the model we want to sell until tomorrow maximum. its can be mor than 2....
            print(relevant_data)
            relevant_data['tic'] = tic
            try:
                if row['mivne'] in ['upper', 'lower']:
                    print([a[0] for a in lst_tic_in_portfolio], '$$$!')
                    if tic not in [a[0] for a in lst_tic_in_portfolio]:
                        data_frame_all_ticker_in_portfolio = pd.concat([data_frame_all_ticker_in_portfolio, relevant_data],
                                                                       ignore_index=True)
                        print(data_frame_all_ticker_in_portfolio, '*&^')
                        amount_this_purchase = math.floor(1000 / float(row['value']))
                        lst_tic_in_portfolio.append([row['ticker'], row['value'], row['mivne'], row['date'],amount_this_purchase])
                        if row['mivne'] == 'upper':
                            money = money - amount_this_purchase * float(row['value'])
                        else:
                            money = money + amount_this_purchase * float(row['value'])
                    print('money:', money)
                    print(lst_tic_in_portfolio, '*(')

            except:
                if row['mivne'] in ['upper', 'lower']:
                    data_frame_all_ticker_in_portfolio = relevant_data
                    print(data_frame_all_ticker_in_portfolio, '^^')
                    amount_this_purchase = math.floor(1000 / float(row['value']))
                    lst_tic_in_portfolio.append([row['ticker'], row['value'], row['mivne'], row['date'], amount_this_purchase])
                    if row['mivne'] == 'upper':
                        money = money - amount_this_purchase * float(row['value'])
                    else:
                        money = money + amount_this_purchase * float(row['value'])
                    print('money:', money)
                    print(lst_tic_in_portfolio, '*)')

            pass_row_dates_signal = pass_row_dates_signal + 1

            #check take_profit:
            for com_details in lst_tic_in_portfolio:
                
                #if com_details[2] == 'lower':
                #    print(com_details[0])
                #    rel_data = data_frame_all_ticker_in_portfolio[data_frame_all_ticker_in_portfolio['tic'] == com_details[0]]
                #    for idx3, date2 in rel_data.iterrows():
                #        if dt1 == date2['Date']: #dt1 - date today
                #            print(date2['Low'])
                #            #if date2['Low'] <= 0.98 * com_details[1]:
                #            #    money = money +
                #            #time.sleep(20)
                #        else:
                #            continue
                
                if com_details[2] == 'upper':
                    print(com_details[0])
                    rel_data = data_frame_all_ticker_in_portfolio[data_frame_all_ticker_in_portfolio['tic'] == com_details[0]]
                    for idx3, date2 in rel_data.iterrows():
                        if dt1 == date2['Date']:
                            print(date2['High'])
                            print(com_details[1])
                            if date2['High'] > 1.02 * float(com_details[1]):
                                money = money + com_details[-1] * 1.02 * float(com_details[1])
                                lst_return_upper.append([com_details[0], dt1, 1.02,])
                                print(lst_return_upper)
                                print(money)
                            time.sleep(20)
                        else:
                            continue

            continue

        else:
            break
    continue

'''
