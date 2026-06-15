import pandas as pd

# Load original dataset
df = pd.read_csv("datasets/ai4i2020.csv")

# Rename columns to fleet-friendly names
df = df.rename(columns={
    "Air temperature [K]": "ambient_temp",
    "Process temperature [K]": "engine_temp",
    "Rotational speed [rpm]": "engine_rpm",
    "Torque [Nm]": "engine_load",
    "Tool wear [min]": "operating_hours",
    "Machine failure": "failure"
})

# Create synthetic fleet feature: mileage
df["mileage"] = df["operating_hours"] * 0.8

# Select final columns
fleet_df = df[
    [
        "ambient_temp",
        "engine_temp",
        "engine_rpm",
        "engine_load",
        "operating_hours",
        "mileage",
        "failure"
    ]
]

# Save new dataset
fleet_df.to_csv("datasets/fleet_dataset.csv", index=False)

print("Fleet dataset created successfully!")
print(fleet_df.head())