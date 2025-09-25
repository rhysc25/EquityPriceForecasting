from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import Global

def RandomForestAlgo():

    df = Global.marketDataFrame.copy()

    # Create target labels
    # 1 if next day's close is higher, 0 if lower
    df['Target'] = (df['c'].shift(-1) > df['c']).astype(int)
    df.dropna(inplace=True)  # drop last row which has no next day to compare

    # Create features (lagged returns)
    df['Return_1'] = df['c'].pct_change(1)
    df['Return_2'] = df['c'].pct_change(2)
    df['Return_3'] = df['c'].pct_change(3)
    df['Return_4'] = df['c'].pct_change(4)
    df['Return_5'] = df['c'].pct_change(5)
    df['Return_6'] = df['c'].pct_change(6)
    df['Return_7'] = df['c'].pct_change(7)
    df['Return_8'] = df['c'].pct_change(8)
    df['Return_9'] = df['c'].pct_change(9)
    df['Return_10'] = df['c'].pct_change(10)
  
    df.dropna(inplace=True)  # drop rows with NaN returns

    # Define feature matrix X and target vector y
    X = df[['Return_1', 'Return_2', 'Return_3','Return_4', 'Return_5', 'Return_6','Return_7', 'Return_8', 'Return_9','Return_10']]
    y = df['Target']

    # Split data into training and testing sets
    # shuffle=False because this is time series data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Create and train Random Forest classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Make predictions
    y_pred = clf.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy on test set:", accuracy)

    # Optional - visualize feature importance
    importances = clf.feature_importances_
    plt.bar(X.columns, importances)
    plt.title("Feature Importance")
    plt.xticks(rotation=45)
    plt.show()
