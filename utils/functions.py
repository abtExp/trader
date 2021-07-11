import numpy as np
import math


'''
	FORMULA TO CALCULATE RSI(MA)

	RSI = 100 – 100 / ( 1 + RS )
	RS = Relative Strength = AvgU / AvgD
	AvgU = average of all up moves in the last N price bars
	AvgD = average of all down moves in the last N price bars
	N = the period of RSI
'''
def rsi(entries):
    last_value = entries[0]['ohlc']['close']

    up_points, down_points = [], []
    for entry in entries[1:]:
        dirn_magn = entry['ohlc']['close'] - last_value
        last_value = entry['ohlc']['close']
        if dirn_magn > 0:
            up_points.append(dirn_magn)
        else:
            down_points.append(-1*dirn_magn)

    avg_up = sum(up_points)/(len(up_points)+1)
    avg_down = sum(down_points)/(len(down_points)+1)
    rs = avg_up/(1e-3 + avg_down)
    rsi = 100 - (100/(1+rs))
    return rsi


def volume_ma(entries):
    return sum([i['volume'] for i in entries])/(1+len(entries))


def open_interest_ma():

    return


def vwap_ma(entries):
    num = 0
    den = 0
    for entry in entries:
        opn, hgh, lw, clse = entry['ohlc'].values()
        price = (hgh+lw+clse)/3
        volume = entry['volume']
        num += (volume*price)
        den += volume

    return num/(den+1e3)


def calc_vals(entries):
    volume = volume_ma(entries[1:])
    vwap = vwap_ma(entries[1:])
    rsi = rsi_ma(entries)
    oi = open_interest_ma(entries)
    return volume, rsi, vwap, oi