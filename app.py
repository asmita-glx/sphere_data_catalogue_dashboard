import streamlit as st
import geopandas as gpd
from sqlalchemy import create_engine
import leafmap.foliumap as leafmap

# ----------------------------------------------------
# Page setup
# ----------------------------------------------------
st.set_page_config(page_title="Sphere Data Catalogue", layout="wide")
st.title("🛰️ Sphere Data Catalogue Dashboard")

# ----------------------------------------------------
# Database connection
# ----------------------------------------------------
db = st.secrets["postgres"]
engine = create_engine(
    f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db']}"
)

# ----------------------------------------------------
# Sidebar Controls
# ----------------------------------------------------
st.sidebar.header("Display Filters")

# Limit number of scenes
limit = st.sidebar.slider("Number of scenes to display", 20, 40, 60)

# --- 1️⃣ Sensor Type Toggle ---
st.sidebar.subheader("🛰️ Sensor Type")
show_eo = st.sidebar.checkbox("EO (Electro-Optical)", value=True)
show_sar = st.sidebar.checkbox("SAR (Synthetic Aperture Radar)", value=True)

sensor_filters = []
if show_eo:
    sensor_filters.append("'EO'")
if show_sar:
    sensor_filters.append("'SAR'")

sensor_condition = (
    f"sensor_type IN ({','.join(sensor_filters)})"
    if sensor_filters
    else "FALSE"
)

# --- 2️⃣ Acquisition Year Toggle (2020–2025) ---
st.sidebar.subheader("📅 Acquisition Year")
year_filters = []
for year in range(2020, 2025):
    if st.sidebar.checkbox(f"{year}", value=True):
        year_filters.append(str(year))

# year_condition = (
#     f"EXTRACT(YEAR FROM acquisition_date)::int IN ({','.join(year_filters)})"
#     if year_filters
#     else "FALSE"
# )

# --- 3️⃣ Resolution Filters ---
st.sidebar.subheader("📏 Resolution Range (m)")
res_ranges = {
    "0.3–0.5 m": (0.3, 0.5),
    "0.6–1.0 m": (0.6, 1.0),
    "1.0 m & above": (1.0, 10.0)
}

selected_res = []
for label in res_ranges:
    if st.sidebar.checkbox(f"{label}", value=True):
        selected_res.append(res_ranges[label])

# res_conditions = [
#     f"(resolution_m BETWEEN {low} AND {high})" for low, high in selected_res
# ]
# res_condition = " OR ".join(res_conditions) if res_conditions else "FALSE"

# ----------------------------------------------------
# SQL Query — combining all filters
# ----------------------------------------------------
query = f"""
    SELECT category, file_name, sensor_type, footprint
    FROM images
    WHERE {sensor_condition}
    LIMIT {limit};
"""

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------
try:
    gdf = gpd.read_postgis(query, engine, geom_col="footprint")
except Exception as e:
    st.error(f"Database query failed: {e}")
    st.stop()

if gdf.empty:
    st.warning("No scenes found for the selected filters.")
    st.stop()

# ----------------------------------------------------
# Map Setup
# ----------------------------------------------------
m = leafmap.Map(center=[20, 78], zoom=5, basemap="CartoDB.DarkMatter")
m.add_basemap("CartoDB.DarkMatter")
# m.add_basemap("SATELLITE")

# Sea-green style
style = {
    "color": "#2E8B57",         # Sea green outline
    "weight": 2,                # Border thickness
    "fillColor": "#2E8B57",     # Same sea green for fill
    "fillOpacity": 0.3          # Transparency
}

m.add_gdf(
    gdf,
    layer_name="Image Footprints",
    style=style
)

# ----------------------------------------------------
# Render Map
# ----------------------------------------------------
m.to_streamlit(height=700)
