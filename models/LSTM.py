import Global
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

def LSTMModel():
    timeSeries = Global.marketDataFrame["c"].to_numpy()
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(timeSeries.reshape(-1,1))

    def create_sequences(data, seq_length):
        X = []
        y = []
        
        for i in range(len(data) - seq_length):
            X.append(data[i:i+seq_length])
            y.append(data[i+seq_length])
            
        return np.array(X), np.array(y)

    seq_length = 10

    X, y = create_sequences(data_scaled, seq_length)

    split = int(len(X)*0.8)
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]

    model = Sequential()
    model.add(LSTM(units = 50, return_sequences=False, input_shape=(seq_length, 1)))
    # 50 memory cells, returns purely the prediction
    model.add(Dense(1))
    # The final output as a single value
    
    model.compile(
        optimizer='adam',
        loss='mean_squared_error'
    )
    # Minimises mean squared error

    history = model.fit(
        X_train,
        y_train,
        epochs=50,
        batch_size=8,
        validation_data=(X_test, y_test)
    )

    predictions = model.predict(X_test)

    # inverse transform
    predictions = scaler.inverse_transform(predictions)
    y_test_actual = scaler.inverse_transform(y_test)

    plt.plot(y_test_actual, label="Actual")
    plt.plot(predictions, label="Predicted")
    plt.legend()
    plt.show()