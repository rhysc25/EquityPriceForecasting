import tensorflow as tf
from Prediction import periodAggregation

def cleanDataframe(df, features):
    columns = set(df.columns)
    features = set(features)
    excess = list(columns - features)
    
    df = df.copy()
    df.drop(columns=excess, inplace=True)
    return df

def linearRegression(trainingProportion=0.8, features=["rsi"], epochs=10, batch_size=32):
    # Get your data
    trainingDataframe, validationDataframe = periodAggregation(trainingProportion=trainingProportion)
    
    trainingDataframe = trainingDataframe.copy()
    validationDataframe = validationDataframe.copy()
    trainingDataframe.dropna(inplace=True)  # drop rows with NaN
    validationDataframe.dropna(inplace=True)  # drop rows with NaN

    # Separate labels
    labelTrain = trainingDataframe.pop("c")
    labelValidate = validationDataframe.pop("c")

    # Keep only selected features
    trainingDataframe = cleanDataframe(trainingDataframe, features)
    validationDataframe = cleanDataframe(validationDataframe, features)

    # Convert to NumPy arrays for Keras
    X_train = trainingDataframe[features].values.astype("float32")
    X_val = validationDataframe[features].values.astype("float32")
    y_train = labelTrain.values.astype("float32")
    y_val = labelValidate.values.astype("float32")

    # Normalization layer (optional but recommended)
    normalizer = tf.keras.layers.Normalization()
    normalizer.adapt(X_train)

    # Build a simple logistic regression model
    model = tf.keras.Sequential([
        normalizer,
        tf.keras.layers.Dense(1, activation="sigmoid")  # linear classifier
    ])

    model.compile(optimizer="adam",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])

    # Train
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size
    )

    # Evaluate
    result = model.evaluate(X_val, y_val, batch_size=batch_size, return_dict=True)
    print(result)

    return model