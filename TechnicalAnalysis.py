import numpy as np
from Backtesting import backtest, betaReturns, alphaCalc, andOrderLists
from AddColumns import simpleMovingAverage, exponentialMovingAverageExc, makeRSIColumn
from Exporting import chopDateFrame
from Parameters import parameters
import Global

def RSI(periods):

    if 'rsi' not in Global.marketDataFrame.columns:
        makeRSIColumn(periods=periods)

    df = chopDateFrame(parameters=parameters)
    dfRows = df.shape[0]

    rsiBuyTimes = np.array([])
    rsiSellTimes = np.array([])
    orders = []

    for i in range(0, dfRows):

        if df["rsi"].iloc[i] > 70:
            rsiSellTimes = np.append(rsiSellTimes, [i, df["t"].iloc[i], df["vw"].iloc[i]])
            orders.append(["sell",i])
        if df["rsi"].iloc[i] < 30:
            rsiBuyTimes = np.append(rsiBuyTimes, [i, df["t"].iloc[i], df["vw"].iloc[i]])
            orders.append(["buy",i])

    return orders

def movingAverageCrossoverLogic(i, buyTimes, sellTimes, orders, df): #Needs edge cases, if both are equal
    if df["ma5"].iloc[i] < df["ma15"].iloc[i] and df["ma5"].iloc[i+1] > df["ma15"].iloc[i+1]:
        buyTimes = np.append(buyTimes, [i+1, df["t"].iloc[i+1], df["vw"].iloc[i+1]])
        orders.append(["buy",i+1])
    elif df["ma5"].iloc[i] > df["ma15"].iloc[i] and df["ma5"].iloc[i+1] < df["ma15"].iloc[i+1]:
        sellTimes = np.append(sellTimes, [i+1, df["t"].iloc[i+1], df["vw"].iloc[i+1]])
        orders.append(["sell",i+1])
    return buyTimes, sellTimes, orders

def movingAverageCrossover():
    simpleMovingAverage(sampleNumber= 5)
    simpleMovingAverage(sampleNumber= 15)
    
    buyTimes = np.array([])
    sellTimes = np.array([])

    orders = []

    df = chopDateFrame(parameters=parameters)
    dfRows = df.shape[0]

    for i in range(0,dfRows - 1):
        buyTimes, sellTimes, orders = movingAverageCrossoverLogic(i, buyTimes=buyTimes, sellTimes=sellTimes, orders=orders, df=df)

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