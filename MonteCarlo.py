import Global
import numpy as np

def logNormalReturnsStdDev():
    Global.marketDataFrame["logReturns"] = np.log(Global.marketDataFrame["c"] / Global.marketDataFrame["c"].shift(1))
    return Global.marketDataFrame["logReturns"].std(skipna=True)

def monteCarloSim():
    # Parameters
    S0 = Global.marketDataFrame["c"].iloc[-1]       # initial stock price
    K = 400        # strike price
    T = 1.0        # time to maturity in years
    r = 0.05       # risk-free rate
    dailySigma = logNormalReturnsStdDev()    # volatility
    trading_days = 252  # typical US trading days
    sigma = dailySigma * np.sqrt(trading_days)
    N = 1000     # number of simulations

    # Simulate terminal prices
    Z = np.random.normal(0, 1, N)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    # Payoff for a call option
    payoff = np.maximum(ST - K, 0)

    # Discounted expected payoff
    price = np.exp(-r * T) * np.mean(payoff)

    print("Monte Carlo Call Price:", price)
