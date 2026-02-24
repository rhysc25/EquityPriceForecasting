import tensorflow as tf
import Global

Global.marketDataFrame.dropna(inplace=True)
rowsTotal = Global.marketDataFrame.shape[0]

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape = rowsTotal),
    tf.keras.layers.Dense(input_shape = rowsTotal),
    tf.keras.layers.Dense()
])