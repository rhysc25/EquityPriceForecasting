import numpy as np
from Backtesting import backtest, betaReturns, alphaCalc, andOrderLists
import Global


def simpleMovingAverage(sampleNumber):
    num = str(sampleNumber)
    Global.marketDataFrame["ma" + num] = Global.marketDataFrame["c"].rolling(window=sampleNumber, min_periods=1).mean()

def exponentialMovingAverageExc(scaleFactor):

    temp = np.zeros(Global.rowsTotal)

    for i in range(0, Global.rowsTotal):
        if i == 0:
            temp[0] = Global.marketDataFrame["c"][0]
        else:
            temp[i] = Global.marketDataFrame["c"][i] * scaleFactor + temp[i-1] * (1 - scaleFactor)

    Global.marketDataFrame["ema"] = temp

def RSI(periods):

    temp = np.zeros(Global.rowsTotal)

    rsiBuyTimes = np.array([])
    rsiSellTimes = np.array([])
    orders = []

    for i in range(0, Global.rowsTotal):
        gainSum = 0
        lossSum = 0
        if i == 0:
            RSI = None
            temp[i] = RSI
        elif i < periods:
            for j in range(0, i):
                diff = Global.marketDataFrame["c"][i - j] - Global.marketDataFrame["c"][i - j - 1]
                if diff > 0:
                    gainSum += diff
                elif diff < 0:
                    lossSum -= diff
            if lossSum == 0:
                RSI = 100
            else:
                RS = gainSum/lossSum
                RSI = 100 - (100/(1 + RS))

                if RSI > 70:
                    rsiSellTimes = np.append(rsiSellTimes, (Global.marketDataFrame["t"][i], Global.marketDataFrame["vw"][i]))
                    orders.append(["sell",i])
                if RSI < 30:
                    rsiBuyTimes = np.append(rsiBuyTimes, (Global.marketDataFrame["t"][i], Global.marketDataFrame["vw"][i]))
                    orders.append(["buy",i])

            temp[i] = RSI
        else:
            for j in range(0, periods):
                diff = Global.marketDataFrame["c"][i - j] - Global.marketDataFrame["c"][i - j - 1]
                if diff > 0:
                    gainSum += diff
                elif diff < 0:
                    lossSum -= diff
            if lossSum == 0:
                RSI = 100
            else:
                RS = gainSum/lossSum
                RSI = 100 - (100/(1 + RS))

                if RSI > 70:
                    rsiSellTimes = np.append(rsiSellTimes, [i, Global.marketDataFrame["t"][i], Global.marketDataFrame["vw"][i]])
                    orders.append(["sell",i])
                if RSI < 30:
                    rsiBuyTimes = np.append(rsiBuyTimes, [i, Global.marketDataFrame["t"][i], Global.marketDataFrame["vw"][i]])
                    orders.append(["buy",i])

            temp[i] = RSI

    Global.marketDataFrame["rsi"] = temp
    
    return orders


def movingAverageCrossoverLogic(i, buyTimes, sellTimes, orders): #Needs edge cases, if both are equal
    if Global.marketDataFrame["ma5"][i] < Global.marketDataFrame["ma15"][i] and Global.marketDataFrame["ma5"][i+1] > Global.marketDataFrame["ma15"][i+1]:
        buyTimes = np.append(buyTimes, [i+1, Global.marketDataFrame["t"][i+1], Global.marketDataFrame["vw"][i+1]])
        orders.append(["buy",i+1])
    elif Global.marketDataFrame["ma5"][i] > Global.marketDataFrame["ma15"][i] and Global.marketDataFrame["ma5"][i+1] < Global.marketDataFrame["ma15"][i+1]:
        sellTimes = np.append(sellTimes, [i+1, Global.marketDataFrame["t"][i+1], Global.marketDataFrame["vw"][i+1]])
        orders.append(["sell",i+1])
    return buyTimes, sellTimes, orders

def movingAverageCrossover():
    simpleMovingAverage(sampleNumber= 5)
    simpleMovingAverage(sampleNumber= 15)
    
    buyTimes = np.array([])
    sellTimes = np.array([])

    orders = []

    for i in range(0,Global.rowsTotal - 1):
        buyTimes, sellTimes, orders = movingAverageCrossoverLogic(i, buyTimes=buyTimes, sellTimes=sellTimes, orders=orders)

    return buyTimes, sellTimes, orders

def backTesting():

    buyTimes, sellTimes, movingAverageOrders= movingAverageCrossover()
    exponentialMovingAverageExc(scaleFactor=0.5)
    RSIOrders = RSI(periods=20)

    bothIntoAccountOrders = andOrderLists(orders1=movingAverageOrders,orders2=RSIOrders)

    betaReturn = betaReturns()
    movingAverageBacktestReturn = backtest(orders=movingAverageOrders, balance=100, propInitBuy=1, propBuy=0.1, propSell=0.05)
    RSIBacktestReturn = backtest(orders = RSIOrders, balance=100, propInitBuy=1, propBuy=0.1, propSell=0.05)
    bothIntoAccountReturn = backtest(orders = bothIntoAccountOrders, balance=100, propInitBuy= 1, propBuy=0.1, propSell=0.05)


    alpha1 = alphaCalc(betaReturns=betaReturn, Returns= movingAverageBacktestReturn)
    alpha2 = alphaCalc(betaReturns=betaReturn, Returns=RSIBacktestReturn)
    alpha3 = alphaCalc(betaReturns=betaReturn, Returns=bothIntoAccountReturn)

    print("Beta: ", betaReturn)
    print("MA return: ", movingAverageBacktestReturn, " MA alpha: ", alpha1)
    print("RSI return: ", RSIBacktestReturn, " RSI alpha: ", alpha2)
    print("Both return: ", bothIntoAccountReturn, " Both alpha: ", alpha3)