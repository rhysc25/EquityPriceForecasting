from GlobalVariables import marketDataFrame, rowsTotal

def betaReturns():

    percReturns = 100 * (marketDataFrame["c"][rowsTotal - 1] - marketDataFrame["c"][0])/marketDataFrame["c"][0]

    return percReturns

def backtest(orders, balance, propInitBuy, propBuy, propSell):
  
    initialBalance = balance
    sharesOwned = 0
    
    sharesOwned += (balance * propInitBuy)/marketDataFrame["c"][0]
    balance -= (balance*propInitBuy)
    
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
    # 1. Convert inner lists to tuples
    set1 = set(map(tuple, orders1))
    set2 = set(map(tuple, orders2))

    # 2. Perform set operation
    common = set1 & set2   # {(3, 4)}

    # 3. Convert back to list of lists
    result = [list(t) for t in common]

    return result