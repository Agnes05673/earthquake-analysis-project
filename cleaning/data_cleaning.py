import pandas as pd
import re

df = pd.read_csv("earthquakes_full_5years.csv")

print("Original shape:", df.shape)

# -----------------------------
# CLEAN DATETIME
# -----------------------------
df["time"] = pd.to_datetime(df["time"], errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], errors="coerce")

# -----------------------------
# CLEAN TEXT FIELDS
# -----------------------------
text_columns = ["magType", "place", "type"]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip().str.lower()

# -----------------------------
# EXTRACT COUNTRY USING REGEX
# -----------------------------
def extract_country(place):
    if place is None or place == "nan":
        return "unknown"
    match = re.findall(r",\s*([A-Za-z\s]+)$", place)
    return match[0].strip().lower() if match else "unknown"

df["country"] = df["place"].apply(extract_country)

# -----------------------------
# NUMERIC FIX
# -----------------------------
numeric_cols = ["mag", "depth_km"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# -----------------------------
# ADD EXTRA FEATURES
# -----------------------------
df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["hour"] = df["time"].dt.hour
df["day_of_week"] = df["time"].dt.day_name()

# depth classification
df["depth_category"] = df["depth_km"].apply(
    lambda x: "shallow" if x < 70 else ("intermediate" if x < 300 else "deep")
)

# magnitude classification
df["mag_category"] = df["mag"].apply(
    lambda x: "minor" if x < 4 else
              "light" if x < 5 else
              "moderate" if x < 6 else
              "strong" if x < 7 else
              "major" if x < 8 else
              "great"
)

# -----------------------------
# SAVE CLEANED DATA
# -----------------------------
df.to_csv("earthquakes_cleaned.csv", index=False)

print("\nCleaned dataset saved as earthquakes_cleaned.csv")
print("New shape:", df.shape)



