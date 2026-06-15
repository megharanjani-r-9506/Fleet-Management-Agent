import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv("datasets/fleet_dataset.csv")

X = df[
    [
        "ambient_temp",
        "engine_temp",
        "engine_rpm",
        "engine_load",
        "operating_hours",
        "mileage"
    ]
]

y = df["failure"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
joblib.dump(
    model,
    "app/models/failure_model.pkl"
)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy)