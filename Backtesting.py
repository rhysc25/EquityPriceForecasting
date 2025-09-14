import Global

def betaReturns():

    percReturns = 100 * (Global.marketDataFrame["c"][Global.rowsTotal - 1] - Global.marketDataFrame["c"][0])/Global.marketDataFrame["c"][0]

    return percReturns

def backtest(orders, balance, propInitBuy, propBuy, propSell):
  
    initialBalance = balance
    sharesOwned = 0
    
    sharesOwned += (balance * propInitBuy)/Global.marketDataFrame["c"][0]
    balance -= (balance*propInitBuy)
    
    for order in orders:
        num = order[1]
        if order[0] == "buy":
            sharesOwned += (balance * propBuy)/Global.marketDataFrame["c"][num]
            balance -= balance * propBuy
        if order[0] == "sell":
            sharesValue = sharesOwned * Global.marketDataFrame["c"][num]
            sharesOwned -= (sharesValue * propSell)/Global.marketDataFrame["c"][num]
            balance += sharesValue * propSell    
    
    assetTotal = balance + sharesOwned * Global.marketDataFrame["c"][Global.rowsTotal - 1]
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