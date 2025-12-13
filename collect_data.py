import requests
import pandas as pd

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "geojson",
    "starttime": "2024-01-01",
    "endtime": "2024-01-31",
    "minmagnitude": 1
}

response = requests.get(url, params=params)

data = response.json()

df = pd.json_normalize(data["features"])

print(df.head())   # shows first 5 rows in terminal

df.to_csv("earthquake_sample.csv", index=False)

print("Saved as earthquake_sample.csv")


