import pandas as pd

def betaReturns(marketDataFrame):
    shape = marketDataFrame.shape
    rowsTotal, columnsTotal = shape[0], shape[1]

    percReturns = 100 * (marketDataFrame["c"][rowsTotal - 1] - marketDataFrame["c"][0])/marketDataFrame["c"][0]

    return percReturns

def backtest(marketDataFrame, orders, balance, propBuy, propSell):
    shape = marketDataFrame.shape
    rowsTotal, columnsTotal = shape[0], shape[1]
    
    initialBalance = balance
    sharesOwned = 0
    
    for order in orders:
        num = order[1]
        if order[0] == "buy":
            sharesOwned += (balance * propBuy)/marketDataFrame["c"][num]
            balance -= balance * propBuy
        if order[0] == "sell":
            sharesValue = sharesOwned * marketDataFrame["c"][num]
            sharesOwned -= (sharesValue * propSell)/marketDataFrame["c"][num]
            balance += sharesValue * propSell    
    
    assetTotal = balance + sharesOwned * marketDataFrame["c"][rowsTotal - 1]
    percReturns = 100*(assetTotal - initialBalance)/initialBalance

    return percReturns

def alphaCalc(betaReturns, Returns):
    alpha = Returns - betaReturns
    return alpha

def andOrderLists(orders1, orders2):
    orders = []
    orders2Dict = {}
    for order in orders2:
        orders2Dict[order[1]] = order[0]
    
    for order in orders1:
        try: 
            temp = orders2Dict[order[1]]
            if temp == order[0]:
                orders.append(order)
        except:
            pass
  
    return orders