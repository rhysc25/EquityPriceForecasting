import tensorflow as tf
from Prediction import periodAggregation

def makeFeatureColumns(features=["rsi"]):
    # Must be fed some array of features (column names of our dataframe)
    feature_columns = []
    for feature in features:
        feature_columns.append(tf.feature_column.numeric_column(feature, dtype  = tf.float32))
    return feature_columns

def makeInputFunction(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
    def inputFunction():
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
        if shuffle:
            ds = ds.shuffle(1000)
        ds = ds.batch(batch_size).repeat(num_epochs)
        return ds
    return inputFunction

def cleanDataframe(df, features):
    columns = set(df.columns)
    features = set(features)
    excess = list(columns - features)
    
    df = df.copy()
    df.drop(columns=excess, inplace=True)
    return df

def linearRegression(trainingProportion = 0.8, features = ["rsi"]):

    trainingDataframe, validationDataframe = periodAggregation(trainingProportion=trainingProportion)
    
    trainingDataframe = trainingDataframe.copy()
    validationDataframe = validationDataframe.copy()
    trainingDataframe.dropna(inplace=True)  # drop rows with NaN
    validationDataframe.dropna(inplace=True)  # drop rows with NaN returns

    labelTrain = trainingDataframe.pop("c")
    labelValidate = validationDataframe.pop("c")

    cleanDataframe(trainingDataframe, features)
    cleanDataframe(validationDataframe, features)

    trainInputFunction = makeInputFunction(trainingDataframe, labelTrain, num_epochs=10, shuffle=True, batch_size=32)
    validateInputFunction = makeInputFunction(validationDataframe, labelValidate, num_epochs=10, shuffle=True, batch_size=32)

    feature_columns = makeFeatureColumns()
    linearEst = tf.estimator.LinearClassifier(feature_columns=feature_columns)

    linearEst.train(trainInputFunction)
    result = linearEst.evaluate(validateInputFunction)

    print(result)

# Currently uses legacy estimator