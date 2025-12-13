import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config("Earthquake Dashboard", layout="wide")
st.title("🌍 Global Earthquake Dashboard")

# Load data (robust to missing derived cols)
df = pd.read_csv("earthquakes_full_26features.csv")

# If year/month/day missing, create them from time
if "time" in df.columns:
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    if "year" not in df.columns:
        df["year"] = df["time"].dt.year
    if "month" not in df.columns:
        df["month"] = df["time"].dt.month
    if "day_of_week" not in df.columns:
        df["day_of_week"] = df["time"].dt.day_name()
else:
    st.error("No 'time' column found — dashboard cannot build time-based visuals.")
    st.stop()

# ensure numeric columns
df["mag"] = pd.to_numeric(df["mag"], errors="coerce").fillna(0)
df["depth_km"] = pd.to_numeric(df.get("depth_km", 0), errors="coerce").fillna(0)

# safe country extraction if missing
if "country" not in df.columns:
    df["country"] = df["place"].astype(str).str.extract(r",\s*([A-Za-z\s]+)$", expand=False).fillna("unknown").str.lower()

# Depth category if missing
if "depth_category" not in df.columns:
    def depth_cat(x):
        if x < 70: return "shallow"
        if x < 300: return "intermediate"
        return "deep"
    df["depth_category"] = df["depth_km"].apply(depth_cat)

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")
years = sorted(df["year"].dropna().unique().astype(int).tolist())
selected_years = st.sidebar.multiselect("Year", years, default=years[-3:])  # default last 3 years for speed

countries = sorted(df["country"].fillna("unknown").unique().tolist())
selected_countries = st.sidebar.multiselect("Country (optional)", countries, default=[])

mag_min, mag_max = float(df["mag"].min()), float(df["mag"].max())
selected_mag = st.sidebar.slider("Magnitude range", mag_min, mag_max, (mag_min, mag_max))

depth_opts = sorted(df["depth_category"].unique().tolist())
selected_depths = st.sidebar.multiselect("Depth category", depth_opts, default=depth_opts)

# Apply filters
mask = df["year"].isin(selected_years) & (df["mag"].between(selected_mag[0], selected_mag[1])) & df["depth_category"].isin(selected_depths)
if selected_countries:
    mask &= df["country"].isin(selected_countries)
filtered = df[mask].copy()

# ---------------- Top KPIs ----------------
col1, col2, col3 = st.columns(3)
col1.metric("Events (filtered)", f"{len(filtered):,}")
col2.metric("Avg Magnitude", round(filtered["mag"].mean() if len(filtered) else 0, 2))
col3.metric("Avg Depth (km)", round(filtered["depth_km"].mean() if len(filtered) else 0, 2))

# ---------------- Charts Row 1 ----------------
st.markdown("### Trends & Distributions")
c1, c2 = st.columns((2,1))

# Events per year (bar)
events_per_year = filtered.groupby("year").size().reset_index(name="count").sort_values("year")
c1.bar_chart(events_per_year.set_index("year")["count"])

# Magnitude histogram
c2.markdown("Magnitude distribution")
c2.bar_chart(np.histogram(filtered["mag"].dropna(), bins=20)[0])

# ---------------- Charts Row 2 ----------------
st.markdown("### Depth & Geography")
d1, d2 = st.columns((1,1))

# Depth category counts
depth_counts = filtered["depth_category"].value_counts()
d1.write("Depth categories")
d1.bar_chart(depth_counts)

# Top 10 countries by count
top_countries = filtered["country"].value_counts().nlargest(10)
d2.write("Top 10 countries (by events)")
d2.bar_chart(top_countries)

# ---------------- Map (if lat/lon present) ----------------
st.markdown("### Map (events location)")
if "latitude" in filtered.columns and "longitude" in filtered.columns:
    map_df = filtered.dropna(subset=["latitude","longitude"])[:5000]  # limit for speed
    st.map(map_df.rename(columns={"latitude":"lat","longitude":"lon"})[["lat","lon"]])
else:
    st.info("Latitude/Longitude not available - map disabled.")

# ---------------- Data table ----------------
st.markdown("### Sample of filtered data")
st.dataframe(filtered.head(200))

# ---------------- Footer - quick tips ----------------
st.caption("Tip: use the filters on the left to narrow the dataset. Export screenshots for report.")

starttime = "2020-01-01"
endtime = "2024-12-31"

st.subheader("Key Earthquake Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Earthquakes", len(df))

with col2:
    st.metric("Average Magnitude", round(df['mag'].mean(), 2))

with col3:
    st.metric("Deepest Earthquake (km)", df['depth_km'].max())
st.sidebar.header("Filters")

country_list = df["country"].dropna().unique()
selected_country = st.sidebar.multiselect("Country", country_list)

year_list = df["year"].dropna().unique()
selected_year = st.sidebar.multiselect("Year", sorted(year_list))

mag_min, mag_max = float(df['mag'].min()), float(df['mag'].max())
mag_range = st.sidebar.slider("Magnitude Range", mag_min, mag_max, (mag_min, mag_max))

# Apply filters
filtered_df = df.copy()

if selected_country:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_country)]

if selected_year:
    filtered_df = filtered_df[filtered_df["year"].isin(selected_year)]

filtered_df = filtered_df[(filtered_df['mag'] >= mag_range[0]) & (filtered_df['mag'] <= mag_range[1])]


