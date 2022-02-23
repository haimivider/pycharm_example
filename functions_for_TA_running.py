import warnings
from datetime import datetime as dt, timedelta
import math
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from talib import RSI, BBANDS, MACD
#from Fundamental_Technical_tools import *
from matplotlib.dates import MonthLocator
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import time


def ohlc_plot(ticker, Data, window, lst_minmax, lst_res, lst_sup, sup_break1, res_break1, mivne_mehirim, runaway_lis):
    Chosen = Data[-window:, ]
    print(Chosen)
    #print(mivne_mehirim)
    #time.sleep(222222)

    min_max_kind = [a[1] for a in lst_minmax]
    min_max_indexes = [a[2]-3 for a in lst_minmax]
    close_value = [a[3] for a in lst_minmax]
    open_value = [a[4] for a in lst_minmax]

    print(Chosen[0])

    for i in range(len(Chosen)):

        plt.vlines(x=i, ymin=Chosen[i, 2], ymax=Chosen[i, 1], color='black', linewidth=1)
        if Chosen[i, 3] > Chosen[i, 0]:
            color_chosen = 'green'
            plt.vlines(x=i, ymin=Chosen[i, 0], ymax=Chosen[i, 3], color=color_chosen, linewidth=4)
        if Chosen[i, 3] < Chosen[i, 0]:
            color_chosen = 'red'
            plt.vlines(x=i, ymin=Chosen[i, 3], ymax=Chosen[i, 0], color=color_chosen, linewidth=4)
        if Chosen[i, 3] == Chosen[i, 0]:
            color_chosen = 'black'
            plt.vlines(x=i, ymin=Chosen[i, 3], ymax=Chosen[i, 0], color=color_chosen, linewidth=4)


        if i in min_max_indexes:
            p = min_max_indexes.index(i)

            if min_max_kind[p] == 'min':
                color_chosen = 'black'
                if close_value[p] >= open_value[p]:
                    plt.plot(i + (7//2), open_value[p], '^', color=color_chosen, markersize= 6)
                else:
                    plt.plot(i + (7//2), close_value[p], '^', color=color_chosen,markersize=6)

            else:
                color_chosen = 'blue'
                if close_value[p] >= open_value[p]:
                    plt.plot(i + (7//2), close_value[p], 'o', color=color_chosen,markersize=5)
                else:
                    plt.plot(i + (7//2), open_value[p], 'o', color=color_chosen,markersize=5)

        # mark maximums and minimum lines
        print([value[0] for value in lst_res])
        print(i)
        if i in [value[0] for value in lst_res]:
            if len(lst_res) == 0:
                continue
            while i in [value[0] for value in lst_res]:
                index12 = [value[0] for value in lst_res].index(i)
                plt.hlines(y=lst_res[index12][2], xmin=lst_res[index12][0], xmax=lst_res[index12][1], linewidth=2.5, color='darkviolet')
                lst_res.pop(index12)

        if i in [value[0] for value in lst_sup]:
            if len(lst_sup) == 0:
                continue

            while i in [value[0] for value in lst_sup]:
                index23 = [value[0] for value in lst_sup].index(i)
                plt.hlines(y=lst_sup[index23][2], xmin=lst_sup[index23][0], xmax=lst_sup[index23][1], linewidth=2.5, color='brown')
                lst_sup.pop(index23)

        # mark_upper_lower_points

        if i in [element[2] for element in mivne_mehirim]:
            index_of_i = [element[2] for element in mivne_mehirim].index(i)
            print(mivne_mehirim[index_of_i])
            if mivne_mehirim[index_of_i][0] == 'upper':
                if mivne_mehirim[index_of_i-1][0] == 'upper':
                    continue
                else:
                    plt.plot(mivne_mehirim[index_of_i][2], mivne_mehirim[index_of_i][1], '*', color='fuchsia', markersize=4)
            elif mivne_mehirim[index_of_i][0] == 'lower':
                if mivne_mehirim[index_of_i-1][0] == 'lower':
                    continue
                else:
                    plt.plot(mivne_mehirim[index_of_i][2], mivne_mehirim[index_of_i][1], '*', color='deepskyblue', markersize=4)
            else:
                continue

        else:
            continue

    if len(sup_break1) > 0:

        for i in sup_break1:
            plt.plot(i[0] + 1, i[1], '*', color='lime', markersize=4)
    if len(res_break1) > 0:
        for i in res_break1:
            plt.plot(i[0] + 1, i[1], '*', color='orange', markersize=4)

    for i in runaway_lis:
        if i[2] == 'decreasing_runaway':
            plt.plot(i[0], i[1], '^', color='brown', markersize=3)
        elif i[2] == 'increasing_runaway':
            plt.plot(i[0], i[1], '^', color='grey', markersize=3)

    plt.plot(Chosen[:, 5], label='MA20')
    plt.plot(Chosen[:, 6], label='MA50')
    plt.plot(Chosen[:, 7], label='MA200')
    plt.xlim([0, window])
    plt.grid()
    plt.legend()
    plt.title(ticker+' stock_price_graph', fontweight='bold')
    plt.savefig("C:\\Users\\User\\Desktop\\Work_Adi\\charts_TA\\" + ticker + "(1).png", bbox_inches="tight")
    #plt.show()

# Using the function
def ma(Data, lookback, what, where):
    for i in range(len(Data)):
        try:
            Data[i, where] = (Data[i - lookback + 1:i + 1, what].mean())
        except IndexError:
            pass
    return Data


def adder(Data, times):
    for i in range(1, times + 1):
        z = np.zeros((len(Data), 1), dtype=float)
        Data = np.append(Data, z, axis=1)

    return Data


def plot_chart(ticker, data, n, my_ohlc_d, lst_minmax1, lst_res1, lst_sup1, sup_break1, res_break1, mivne_mehirim1, runaway_lis):
    # Filter number of observations to plot
    data = data.iloc[-n:]

    # Create figure and set axes for subplots
    fig = plt.figure()
    fig.set_size_inches((12, 9.6))
    ax_candle = fig.add_axes((0.05, 0.72, 0.9, 0.2))

    # Plot candlestick chart
    ohlc_plot(ticker, my_ohlc_d, 500, lst_minmax1, lst_res1, lst_sup1, sup_break1, res_break1, mivne_mehirim1, runaway_lis)

    ax_macd = fig.add_axes((0.05, 0.49, 0.9, 0.2), sharex=ax_candle)
    ax_macd.set_title('MACD', fontweight='bold')
    ax_rsi = fig.add_axes((0.05, 0.258, 0.9, 0.2), sharex=ax_candle)
    ax_rsi.set_title('RSI', fontweight='bold')
    ax_vol = fig.add_axes((0.05, 0.023, 0.9, 0.2), sharex=ax_candle)
    ax_vol.set_title('Volume', fontweight='bold')

    data = data.set_index(data['Date'])

    # Plot MACD
    macd, macdsignal, macdhist = MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    data['macd'] = macd
    data['macd_signal'] = macdsignal
    data['macd_hist'] = macdhist

    ax_macd.plot(data.index, data["macd"], label="macd")
    ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist")
    ax_macd.plot(data.index, data["macd_signal"], label="signal")
    ax_macd.legend(loc="upper left",  ncol=3)

    # Plot RSI
    # Above 70% = overbought, below 30% = oversold
    data['rsi'] = RSI(data['Close'], timeperiod=14)
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(data.index, [70] * len(data.index), label="overbought - 70")
    ax_rsi.plot(data.index, [50] * len(data.index), label="score_50", color='hotpink')
    ax_rsi.plot(data.index, [30] * len(data.index), label="oversold - 30")
    ax_rsi.plot(data.index, data["rsi"], label="rsi")
    ax_rsi.legend(loc="upper left",  ncol=4)

    # Show volume in millions
    ax_vol.bar(data.index, data["Volume"] / 1000000)
    ax_vol.set_ylabel("(Million)")

    plt.xticks(np.arange(0, 500, 50))
    # Save the chart as PNG
    fig.savefig("C:\\Users\\User\\Desktop\\Work_Adi\\charts_TA\\" + ticker + ".png", bbox_inches="tight")

    plt.show()


def find_max_min_points1(minmax_list, close_check1, open_check1, low_check1, high_check1, date_check1, index2, index1):
    print(minmax_list)
    print('!@#!@#')
    min_max_check = []
    print(date_check1[7//2])
    if index1 < index2:
        return "no_minmax"
    # print(checking_one_on_one_max_point(close_check, open_check, low_check, high_check, 9, date[index1+steps // 2], index1))
    result_max = checking_one_on_one_max_point1(close_check1, open_check1, low_check1, high_check1, 7,
                                           date_check1[7//2], index1) # date_check1[-1])
    print("checking max:", result_max, '##')
    if result_max is not None:
        print("#00")
        if len(minmax_list) > 0:

            if minmax_list[-1][1] == "max":
                print(max(result_max[3], result_max[4]))
                print(max(minmax_list[-1][3], minmax_list[-1][4]))
                if (max(result_max[3], result_max[4]) > max(minmax_list[-1][3],minmax_list[-1][4])):
                    minmax_list.pop()

                    #minmax_list.append(result_max)
                    return result_max
                else:
                   pass

            else:
                if int(result_max[2]) - int(minmax_list[-1][2]) < 3:
                    if max(result_max[3], result_max[4]) \
                    / (min(minmax_list[-1][3], #change to min to be more aggreasive - more signals
                           minmax_list[-1][4])) > 1.02:
                        return result_max
                    else:
                        pass

                elif max(result_max[3], result_max[4]) \
                       /(min(minmax_list[-1][3], #change to min to be more aggreasive - more signals
                           minmax_list[-1][4])) > 1.01:
                    #min_max_check.append(result_max)
                    return result_max

                else:
                     pass

        else:
            #minmax_list.append(result_max)
            print(minmax_list)
            return result_max

    result_min = checking_one_on_one_min_point1(close_check1, open_check1, low_check1, high_check1, 7,
                                           date_check1[7//2], index1)# date_check1[-1])

    print("checking min:", result_min, '#99')
    if result_min is not None:
        print("@@")
        if len(minmax_list) > 0:
            if minmax_list[-1][1] == "min":
                if min(result_min[3], result_min[4])< \
                    min(minmax_list[-1][3],minmax_list[-1][4]):
                    minmax_list.pop()
                    #min_max_check.append(result_min)
                    return result_min
                else:
                   pass

            else:

                if int(result_min[2]) - int(minmax_list[-1][2]) < 3:
                    if min(result_min[3], result_min[4]) \
                    / (max(minmax_list[-1][3], #change to max to be more aggreasive - more signals
                           minmax_list[-1][4])) < 0.98:  #Can improve with regard to high and low

                        return result_min

                elif min(result_min[3], result_min[4]) \
                       /(max(minmax_list[-1][3], #change to max to be more aggreasive - more signals
                           minmax_list[-1][4])) < 0.99:
                    #min_max_check.append(result_min)
                    return result_min

                else:
                     pass

        else:
            #minmax_list.append(result_min)
            return  result_min

    return "no_minmax"


def checking_one_on_one_max_point1(close1, open1, low1, high1, steps, date1, index1):
    print('close:', close1)
    print('open:', open1)
    print('low:', low1)
    print('high:', high1)

    print(high1[steps-2])
    print(high1[steps//2])

    if ((high1[steps // 2] > high1[((steps // 2) - 1)]) is True) \
            & (((high1[steps // 2] > high1[((steps // 2) + 1)])) is True):
        first_num = 1
    else:
        first_num = 0
    print(first_num)

    if (((high1[((steps // 2) - 1)] > np.maximum(open1[((steps // 2) - 2)], close1[((steps // 2) - 2)])) is True)
            & (high1[((steps // 2) + 1)] > np.maximum(open1[((steps // 2) + 2)], close1[((steps // 2) + 2)])) is True):
        second_num = 1
        print(second_num, '$$')
    elif first_num == 1:
        print(first_num, '%')
        if ((high1[steps // 2] > high1[((steps // 2) - 2)]) is True) \
                & (((high1[steps // 2] > high1[((steps // 2) + 2)])) is True):
            second_num = 1
            print(second_num)
        else:
            second_num = 0
            print(second_num)
    elif first_num == 0:
        second_num = 0
        print(second_num)

    if ((((np.maximum(open1[((steps // 2) - 2)], close1[((steps // 2) -2)]) > low1[((steps // 2) - 3)])) == True)):# (or/and +3 instead of -3)

        third_num = 1
    else:
        third_num = 0

    print(third_num)

    if (first_num + second_num + third_num == 3):
        print('max_signal! ', 'date: ', date1, ', close_price:', round(close1[steps // 2], 2))
        print(index1)
        print(steps // 2)
        return [date1, 'max', index1 - (steps // 2), round(close1[steps // 2], 2), round(open1[steps // 2], 2)]

    return

def checking_one_on_one_min_point1(close1,open1,low1,high1,steps,date1,index1):
    print(date1)

    print('close:', close1)
    print('open:', open1)
    print('low:', low1)
    print('high:', high1)

    if ((low1[steps // 2] < low1[((steps // 2) - 1)]) == True) \
            & (((low1[steps // 2] < low1[((steps // 2) + 1)])) == True)\
            & (((low1[steps // 2] < low1[((steps // 2) + 2)])) == True):
        first_num = 1
    else:
        first_num = 0
    print(first_num)

    if (((low1[((steps // 2) - 1)]  < np.minimum(open1[((steps // 2) - 2)], close1[((steps // 2) - 2)])) == True)):
        second_num = 1
        print(second_num, '$$')
    elif first_num == 1:
        print(first_num, '%')
        if ((low1[steps // 2] < low1[((steps // 2) - 2)]) == True) & (((low1[steps // 2] < low1[((steps // 2) + 2)]))== True):

            second_num = 1
            print(second_num)
        else:
            second_num = 0
            print(second_num)
    elif first_num == 0:
        second_num = 0
        print(second_num)

    if ((((np.minimum(open1[((steps // 2) - 1)], close1[((steps // 2) -1)]) < high1[((steps // 2) - 2)])) == True)):# &


        third_num = 1
    else:
        third_num = 0

    print(third_num)

    if (first_num + second_num + third_num == 3):
        print('min_signal!! ', 'date: ', date1, ',close_price:', round(close1[steps // 2],2))
        return [date1, 'min', index1 - (steps // 2), round(close1[steps // 2], 2), round(open1[steps // 2], 2)]

    return


def resistence1(lst_of_lst):
    if len(lst_of_lst) <2:
        print('lower than 2')
        return 'no_resist1', 'no_resist2'

    print(lst_of_lst)
    lst_of_lst_max = [item for item in lst_of_lst if item[1] == "max"][::-1]
    print(lst_of_lst_max)
    list_of_maximums = []
    for i in lst_of_lst_max:
        list_of_maximums.append([max(i[3], i[4]), i[2]]) #take maximum from start and end - append: max,location
    print('list_of_maximums: max,location, in reversal!', list_of_maximums)
    for index, element in enumerate(list_of_maximums):
        checklist = [ind[0] for ind in list_of_maximums][index+1:]# start after the same point
        timelist = [ind[1] for ind in list_of_maximums][index+1:]
        for idx, element1 in enumerate(checklist):
            print(element[0], element1)
            print(index, idx)
            print(list_of_maximums[index][1], timelist[idx])
            if (element1 > element[0] * 1.02): #list_of_maximums[-1]* 1.05):
                print('Im stop check because one of previous max point bigger too much')
                break
            if (list_of_maximums[index][1] - timelist[idx]) < 6:
                continue
            if (element1 > element[0] * 0.98) and (element1 < element[0] * 1.02):
                print(element, 'resistence')
                print('haimi!')
                print(element, [timelist[idx], list_of_maximums[index][1], (element[0]+element1)/2, [timelist[idx], list_of_maximums[index][1]]])
                return element, [timelist[idx], list_of_maximums[index][1], (element[0]+element1)/2, [timelist[idx], list_of_maximums[index][1]]]
            else:
                continue
        return 'no_resist1', 'no_resist2'


def support1(lst_of_lst):
    if len(lst_of_lst) < 2:
        print('lower than 2')
        return 'no_resist1', 'no_resist2'

    lst_of_lst_min = [item for item in lst_of_lst if item[1] == "min"][::-1]
    print(lst_of_lst_min)
    list_of_minimums = []
    for i in lst_of_lst_min:
        list_of_minimums.append([min(i[3], i[4]), i[2]])
    print('list_of_minimums: min,location, in reversal!', list_of_minimums)
    for index, element in enumerate(list_of_minimums):
        checklist = [ind[0] for ind in list_of_minimums][index+1:]
        timelist  = [ind[1] for ind in list_of_minimums][index+1:]
        for idx, element1 in enumerate(checklist):
            print(element[0], element1)
            print(index, idx)
            print(list_of_minimums[index][1], timelist[idx])
            if (element1 < element[0] * 0.985):
                print('Im stop check because one of previous min point lower too much')
                break
            if (list_of_minimums[index][1] - timelist[idx]) < 6:
                continue
            if (element1 > element[0] * 0.98) and (element1 < element[0] * 1.02):
                print(element, 'support')
                print(element, [timelist[idx], list_of_minimums[index][1], (element[0]+element1)/2, [timelist[idx], list_of_minimums[index][1]]])
                return element, [timelist[idx], list_of_minimums[index][1], (element[0]+element1)/2, [timelist[idx], list_of_minimums[index][1]]]
            else:
                continue
        return 'no_resist1', 'no_resist2'


# def Breakaway1(index1, lst_of_resistence, lst_of_support, close_last_sup_res, open_last_sup_res, low_last_sup_res, high_last_sup_res
#              , close_check12, open_check12, low_check12, high_check12, date_check12,steps): ## also global max or global_min

def Breakaway(index3, lst_of_resistence, lst_of_support, low_check12, high_check12, open_check12, low_general, high_general, close_check12, steps):
    print(index3, 'idit')
    print('check_breakaway:')
    print(low_check12)
    print(high_check12)
    print('lst_of_support:', lst_of_support)
    print('lst_of_resistence:', lst_of_resistence)
    print([x[1] for x in lst_of_support])
    if len(lst_of_support) > 0:
        print('start to check if breakaway support exists:')
        lst_of_broken_support = []
        for element in lst_of_support:
            low_general_temp = low_general[element[1]+1:index3-1] #observation from relevant index
            print(low_general_temp)
            print(element)
            print(element[2]) #value
            print(element[1]) #location

            if any(low_el < element[2] * 0.98 for low_el in low_general_temp):

                #print(low_general)
                #print(high_general)
                continue

            if element[1]+3 > (index3):
                print('&^%&^%')
                continue

            #print(low_check12)
            #print(high_check12)
            #print(low_check12[-1])
            #print(high_check12[-2])
            #print(element[0])

            if ((open_check12[-1] < element[2]) & # high_check12[-1]*1.02 #it was high_check12[-1]!!!!!!!!!!
                    (low_check12[-2] > element[2])): #low_check12[-2]*1.02
                print('its support breakaway!')

                #I added it!!!!!!!!!!
                if high_check12[-1] > element[2]:
                    return ([index3-2, open_check12[-1], 'fail_break_sup', element[2], low_check12[-2],
                                              element[1], element[-1], close_check12[-1], high_check12[-1]])

                #return(index3-2, open_check12[-1], 'break_sup', element[2], high_check12[-2])
                lst_of_broken_support.append([index3-2, open_check12[-1], 'break_sup', element[2], low_check12[-2],
                                              element[1], element[-1], close_check12[-1], high_check12[-1]])
                continue #in order to get all "broken" lines

            else:
                print('no breakaway')
                pass
        print(lst_of_broken_support)


        if len(lst_of_broken_support) == 0:
            pass

        elif len(lst_of_broken_support) == 1:
            return lst_of_broken_support[0]

        else:
            lens = [(a[1] - a[0]) for a in lst_of_broken_support]
            print(lens)
            max_len = max(lens)
            print(max_len)
            max_index = lens.index(max_len)
            print(max_index)
            print(lst_of_broken_support[max_index])
            return lst_of_broken_support[max_index] #return the largest

    else:
        print('no support breakaway because no support line')
    if len(lst_of_resistence) > 0:
        print('start to check if breakaway resistance exists ')
        lst_of_broken_resistence = []
        print('lst_of_resistence:', lst_of_resistence)
        for element in lst_of_resistence:
            print(element)
            high_general_temp = high_general[(element[1] + 1):(index3-1)]
            print(high_general_temp)

            if any(high_general > element[2] * 1.02 for high_general in high_general_temp):
                print('^^^^^&')
                continue

            if (element[1] + 3 > (index3)) :
                continue
            #print(low_check12)
            #print(high_check12)
            #print(low_check12[-2])
            #print(high_check12[-1])
            #print(element[0])

            if ((high_check12[-2] < element[2]) &    #high_check12[-2]*0.98
                    (open_check12[-1] > element[2])):  #low_check12[-1]*0.98
                print('its resistence breakaway!')

                if low_check12[-1] < element[2]:
                    return ([index3-2, open_check12[-1], 'fail_break_res', element[2], high_check12[-2],
                                              element[1], element[-1], close_check12[-1], low_check12[-1]])

                lst_of_broken_resistence.append([index3-2, open_check12[-1], 'break_res', element[2], high_check12[-2],
                                                 element[1], element[-1], close_check12[-1], low_check12[-1]])
            else:
                print('no breakaway')

        if len(lst_of_broken_resistence) == 0:
            pass

        elif len(lst_of_broken_resistence) == 1:

            print(lst_of_broken_resistence[0])
            return lst_of_broken_resistence[0]

        else:
            lens = [(a[1] - a[0]) for a in lst_of_broken_resistence]
            #print(lens)
            max_len = max(lens)
            #print(max_len)
            max_index = lens.index(max_len)
            #print(max_index)
            #print(lst_of_broken_resistence[max_index])
            return lst_of_broken_resistence[max_index] #return the largest

        return (index3-2, 'nothing', 'nothing', 'nothing', 'nothing','nothing', 'nothing','nothing')


    else:
        print('no resistence breakaway because no resistence line')
        return (index3-2, 'nothing', 'nothing', 'nothing', 'nothing','nothing', 'nothing','nothing')

def mivne_mehirim(list_of_min_max_points, index3 ,low_check12, high_check12, open_check12, close_check12, date_check12):
    print(index3)
    print('low_check12:', low_check12)
    print('high_check12:', high_check12)
    print('open_check12:', open_check12)
    print('close_check12: ', close_check12)
    print('date_check12:', date_check12)
    #print([item for item in list_of_min_max_points if item[2]])
    vector_of_relevant_min_max_points_until_it_included = [item for item in list_of_min_max_points if item[2] <= index3][-3:]  # last three min_max_point
    #print(vector_of_relevant_min_max_points_until_it_included[2][2])
    print('3 last minmax points', vector_of_relevant_min_max_points_until_it_included)
    if [item[1] for item in vector_of_relevant_min_max_points_until_it_included] == ['min', 'max', 'min']:
        print(max(vector_of_relevant_min_max_points_until_it_included[1][3:5]))
        if (high_check12[-1] >= max(vector_of_relevant_min_max_points_until_it_included[1][3:5]))\
                and (min(vector_of_relevant_min_max_points_until_it_included[2][3:5]) >
            min(vector_of_relevant_min_max_points_until_it_included[0][3:5]))\
                and (max(vector_of_relevant_min_max_points_until_it_included[1][3:5]) >
                min(vector_of_relevant_min_max_points_until_it_included[2][3:5])):
            print('upper')
            if open_check12[-1] >= max(vector_of_relevant_min_max_points_until_it_included[1][3:5]): #start with gap
                return ('upper', open_check12[-1], index3-1, vector_of_relevant_min_max_points_until_it_included
                        , date_check12[-1])

            if (high_check12[-1] >= max(vector_of_relevant_min_max_points_until_it_included[1][3:5])):
                return ('upper', max(vector_of_relevant_min_max_points_until_it_included[1][3:5]),
                        index3-1, vector_of_relevant_min_max_points_until_it_included
                        , date_check12[-1])
            #else:
            #    return ('upper', max(vector_of_relevant_min_max_points_until_it_included[1][3:5]), index3-1, vector_of_relevant_min_max_points_until_it_included
            #            , date_check12[-1])
            else:
                return ('natural', 'no intresting', index3-1, vector_of_relevant_min_max_points_until_it_included,
                        date_check12[-1])

        else:
            print('natural')
            return ('natural','no intresting', index3-1, vector_of_relevant_min_max_points_until_it_included, date_check12[-1])
    else:
        if ((low_check12[-1] <= min(vector_of_relevant_min_max_points_until_it_included[1][3:5]))
            and (max(vector_of_relevant_min_max_points_until_it_included[2][3:5]) <
                 max(vector_of_relevant_min_max_points_until_it_included[0][3:5])))\
            and (min(vector_of_relevant_min_max_points_until_it_included[1][3:5]) <
                max(vector_of_relevant_min_max_points_until_it_included[2][3:5])):
            print('lower')

            if open_check12[-1] <= min(vector_of_relevant_min_max_points_until_it_included[1][3:5]):
                print('tlry')
                return ('lower', open_check12[-1], index3-1, vector_of_relevant_min_max_points_until_it_included, date_check12[-1])

            if low_check12[-1] <= min(vector_of_relevant_min_max_points_until_it_included[1][3:5]):
                print('plug')
                return ('lower', min(vector_of_relevant_min_max_points_until_it_included[1][3:5]),
                        index3-1, vector_of_relevant_min_max_points_until_it_included
                        , date_check12[-1])
            #else:
            #    return ('lower', min(vector_of_relevant_min_max_points_until_it_included[1][3:5]), index3-1, vector_of_relevant_min_max_points_until_it_included, date_check12[-1])
            else:
                return ('natural', 'no intresting', index3-1, vector_of_relevant_min_max_points_until_it_included,
                        date_check12[-1])

        else:
            print('natural')
            return ('natural', 'no intresting', index3-1, vector_of_relevant_min_max_points_until_it_included, date_check12[-1])


# candle_over_resistence_or_support():

#def over_global_maximum(passed_days = 200, ):


#def double_peak():


def Runaway(low_check1, high_check1, gaps_inquired): #close_check1,  open_check1, looking_back_days
    #low_check1 = low_check1[0:len(date_check1) // 2]
    #high_check1 = high_check1[0:len(date_check1) // 2]
    print('low_check:', low_check1)
    print('high_check:', high_check1)
    print('__+__')
    count_of_increasing_runaway = 1
    count_of_decreasing_runaway = 1
    #date_now = date_check1[len(date_check1) // 2] #7//2
    for i in range(len(high_check1)):
        if i == 0:
            continue

        if i == (len(high_check1)-1):
            return 'no runaway'

        if (high_check1[-2] < low_check1[-1]):
            if (high_check1[i-1] < low_check1[i]):
                count_of_increasing_runaway = count_of_increasing_runaway + 1
                if count_of_increasing_runaway == gaps_inquired:
                    print("increasing_runaway!")
                    return "increasing_runaway"
                else:
                    continue
            else:
                continue

        elif (high_check1[-1] < low_check1[-2]):
            if(low_check1[i-1] > high_check1[i]):
                count_of_decreasing_runaway = count_of_decreasing_runaway + 1
                if count_of_decreasing_runaway == gaps_inquired:
                    print("decreasing_runaway!")
                    return "decreasing_runaway"
                else:
                    continue
            else:
                continue

        return 'no runaway'

    return 'no runaway'
