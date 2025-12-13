import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_month_data(start_date, end_date):
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query?"
        f"format=geojson&starttime={start_date}&endtime={end_date}&limit=20000"
    )

    try:
        response = requests.get(url, timeout=20)
        data = response.json()

        records = []

        for f in data["features"]:
            p = f["properties"]
            g = f["geometry"]

            record = {
                "time": p.get("time"),
                "updated": p.get("updated"),

                "mag": p.get("mag"),
                "magType": p.get("magType"),
                "type": p.get("type"),
                "place": p.get("place"),

                "status": p.get("status"),
                "tsunami": p.get("tsunami"),
                "alert": p.get("alert"),

                "net": p.get("net"),
                "sources": p.get("sources"),
                "types": p.get("types"),

                "nst": p.get("nst"),
                "dmin": p.get("dmin"),
                "rms": p.get("rms"),
                "gap": p.get("gap"),

                "magError": p.get("magError"),
                "depthError": p.get("depthError"),
                "magNst": p.get("magNst"),

                "sig": p.get("sig"),
                "cdi": p.get("cdi"),
                "mmi": p.get("mmi"),
                "felt": p.get("felt"),

                "longitude": g["coordinates"][0] if g else None,
                "latitude": g["coordinates"][1] if g else None,
                "depth_km": g["coordinates"][2] if g else None,
            }

            records.append(record)

        return records

    except Exception as e:
        print("Error fetching:", e)
        return []


# ------------------------------------------
# MAIN EXTRACTION LOOP
# ------------------------------------------
print("Starting FULL 26-feature extraction...")

start = datetime(2020, 1, 1)
end = datetime(2025, 1, 1)

current = start
all_records = []

while current < end:
    next_month = current + timedelta(days=32)
    next_month = next_month.replace(day=1)

    s = current.strftime("%Y-%m-%d")
    e = next_month.strftime("%Y-%m-%d")

    print(f"Fetching {s} → {e}")

    rows = fetch_month_data(s, e)
    all_records.extend(rows)

    current = next_month

# DataFrame
df = pd.DataFrame(all_records)

# Convert timestamps
df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], unit="ms", errors="coerce")

df.to_csv("earthquakes_full_26features.csv", index=False)

print("\nSaved: earthquakes_full_26features.csv")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))
