import pandas as pd
from ml_model import predict

df = pd.read_csv("transactions.csv")

fraud_rows = df[df["isError"] == 1].head(10)


for idx, row in fraud_rows.iterrows():
    sample = {
        "BlockHeight": row["BlockHeight"],
        "TimeStamp": float(row["TimeStamp"]),
        "Value": row["Value"],
        "From": row["From"],
        "To": row["To"]
    }
    print("Actual:", row["isError"], "Predicted:", predict(sample))
