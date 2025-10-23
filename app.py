import streamlit as st
import geopandas as gpd
from sqlalchemy import create_engine
import leafmap.foliumap as leafmap


# --- Page setup ---
st.set_page_config(page_title="Image Footprints Catalogue", layout="wide")
st.title("🛰️ Sphere Data Catalogue Dashboard")

# # --- Database connection ---
# db_user = "asmita"
# db_pass = "asmita123"
# db_host = "34.136.145.76"
# db_port = "5432"
# db_name = "qgis_labeling_db"
# # DB connection
# engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

db = st.secrets["postgres"]

engine = create_engine(
    f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db']}"
)
# Sidebar controls
limit = st.sidebar.slider("Number of scenes to display", 20, 40, 60)
# stroke_color = st.sidebar.color_picker("Border color", "#00FF00")
# fill_color = st.sidebar.color_picker("Fill color", "#FFFF00")
# fill_opacity = st.sidebar.slider("Fill opacity", 0.0, 1.0, 0.4)
# line_width = st.sidebar.slider("Border thickness", 1, 10, 2)

# Load footprints
query = f"SELECT * FROM images LIMIT {limit};"
gdf = gpd.read_postgis(query, engine, geom_col="footprint")

# Map
m = leafmap.Map(center=[20, 78], zoom=5, basemap="CartoDB.DarkMatter")
m.add_basemap("CartoDB.DarkMatter")
m.add_gdf(
    gdf,
    layer_name="Image Footprints",
    popup_property=["filename", "satellite", "acquisition_date"]  # <-- fixed
    # stroke_color=stroke_color,
    # fill_color=fill_color,
    # fill_opacity=fill_opacity,
    # line_width=line_width
)

m.to_streamlit(height=1000)
