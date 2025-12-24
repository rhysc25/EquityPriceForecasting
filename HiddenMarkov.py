from Exporting import chopDateFrame
from Parameters import parameters
import numpy as np
from hmmlearn.hmm import GaussianHMM
import pandas as pd


def rolling_zscore(series, window=20):
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std

def classify_state(row):
    if row["vol_30"] < -0.5 and row["autocorr_5"] < -0.3:
        return "mean_reversion"
    elif row["autocorr_5"] > 0.3 and row["vol_30"] > 0:
        return "fast_trend"
    else:
        return "normal_trend"

def HiddenMarkovAlgo():

    df = chopDateFrame(parameters=parameters)

    df["ret_1"] = np.log(df["c"] / df["c"].shift(1))

    df["vol_10"] = df["ret_1"].rolling(10).std()
    df["vol_30"] = df["ret_1"].rolling(30).std()

    df["atr_14"] = (
        (df["h"] - df["l"])
        .rolling(14)
        .mean()
    )

    df["ma_20"] = df["c"].rolling(20).mean()
    df["ma_50"] = df["c"].rolling(50).mean()

    df["ma_slope"] = df["ma_20"] - df["ma_20"].shift(5)

    df["trend_strength"] = abs(df["ma_20"] - df["ma_50"])

    df["autocorr_5"] = (
        df["ret_1"]
        .rolling(20)
        .apply(lambda x: x.autocorr(lag=5))
    )

    features = [
        "ret_1",
        "vol_10",
        "vol_30",
        "atr_14",
        "ma_slope",
        "trend_strength",
        "autocorr_5",
    ]

    for col in features:
        df[col] = rolling_zscore(df[col])

    X = df[features].dropna()

    print(X.columns)
    print(X.shape)

    n_states = 3

    hmm = GaussianHMM(
        n_components=n_states,
        covariance_type="full",
        n_iter=1000,
        random_state=42
    )

    hmm.fit(X.values)
    
    df.loc[X.index, "regime"] = hmm.predict(X.values)

    probs = hmm.predict_proba(X.values)

    for i in range(n_states):
        df.loc[X.index, f"regime_{i}_prob"] = probs[:, i]

    regime_summary = (
        df
        .loc[X.index]
        .groupby("regime")[features]
        .mean()
    )

    print(regime_summary)

    REGIME_MAP = {
        0: "normal_trend",
        1: "fast_trend",
        2: "mean_reversion"
    }

    train_window = 100

    for t in range(train_window, len(df)):

        train_X = X.iloc[t-train_window:t]
        hmm.fit(train_X.values)

        # relabel states AFTER fitting
        state_means = pd.DataFrame(hmm.means_, columns=features)
        state_labels = state_means.apply(classify_state, axis=1)
        REGIME_MAP = dict(state_labels)

        # infer current state
        state = hmm.predict(X.iloc[t:t+1].values)[0]
        regime_name = REGIME_MAP[state]

        df.iloc[t, df.columns.get_loc("regime_name")] = regime_name

