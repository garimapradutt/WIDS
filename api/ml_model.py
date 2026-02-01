import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_PATH = "model.pkl"

def train_model():
    df = pd.read_csv("transactions.csv")
    df["TimeStamp"] = df["TimeStamp"].astype(float)
    sender_stats = df.groupby("From").agg(
        from_tx_count=("From", "count"),
        from_error_rate=("isError", "mean"),
        from_avg_value=("Value", "mean")
    )

    receiver_stats = df.groupby("To").agg(
        to_tx_count=("To", "count"),
        to_error_rate=("isError", "mean"),
        to_avg_value=("Value", "mean")
    )
    df = df.join(sender_stats, on="From")
    df = df.join(receiver_stats, on="To")


    df.fillna(0, inplace=True)
    df["TimeStamp"] = df["TimeStamp"] / 1e9
    features = [
        "BlockHeight", "TimeStamp", "Value",
        "from_tx_count", "from_error_rate", "from_avg_value",
        "to_tx_count", "to_error_rate", "to_avg_value"
    ]
    X = df[features]
    y = df["isError"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(
        n_estimators=400,
        class_weight="balanced_subsample",
        max_depth=15
    )

    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)

    print("Accuracy:", model.score(X_test, y_test))


def predict(sample: dict):

    model = joblib.load(MODEL_PATH)
    df = pd.read_csv("transactions.csv")
    sender_stats = df.groupby("From").agg(
        from_tx_count=("From", "count"),
        from_error_rate=("isError", "mean"),
        from_avg_value=("Value", "mean")
    )
    receiver_stats = df.groupby("To").agg(
        to_tx_count=("To", "count"),
        to_error_rate=("isError", "mean"),
        to_avg_value=("Value", "mean")
    )
    from_row = sender_stats.loc[sample["From"]] if sample["From"] in sender_stats.index else None
    to_row = receiver_stats.loc[sample["To"]] if sample["To"] in receiver_stats.index else None

    sample["from_tx_count"] = float(from_row["from_tx_count"]) if from_row is not None else 0
    sample["from_error_rate"] = float(from_row["from_error_rate"]) if from_row is not None else 0
    sample["from_avg_value"] = float(from_row["from_avg_value"]) if from_row is not None else 0
    sample["to_tx_count"] = float(to_row["to_tx_count"]) if to_row is not None else 0
    sample["to_error_rate"] = float(to_row["to_error_rate"]) if to_row is not None else 0
    sample["to_avg_value"] = float(to_row["to_avg_value"]) if to_row is not None else 0
    sample["TimeStamp"] = sample["TimeStamp"] / 1e9

    feat = pd.DataFrame([sample])

    features = [
        "BlockHeight", "TimeStamp", "Value",
        "from_tx_count", "from_error_rate", "from_avg_value",
        "to_tx_count", "to_error_rate", "to_avg_value"
    ]

    return int(model.predict(feat[features])[0])
