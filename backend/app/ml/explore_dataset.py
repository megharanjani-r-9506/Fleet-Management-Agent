import pandas as pd
from pathlib import Path

df = pd.read_csv("datasets/ai4i2020.csv")

print("\nColumns:")
print(df.columns.tolist())

print("\nShape:")
print(df.shape)

