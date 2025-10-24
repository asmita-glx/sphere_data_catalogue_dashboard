# import streamlit as st
# import geopandas as gpd
# from sqlalchemy import create_engine
# import leafmap.foliumap as leafmap


# # --- Page setup ---
# st.set_page_config(page_title="Image Footprints Catalogue", layout="wide")
# st.title("🛰️ Sphere Data Catalogue Dashboard")

# db = st.secrets["postgres"]

# engine = create_engine(
#     f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db']}"
# )
# # Sidebar controls
# limit = st.sidebar.slider("Number of scenes to display", 20, 40, 60)
# # stroke_color = st.sidebar.color_picker("Border color", "#00FF00")
# # fill_color = st.sidebar.color_picker("Fill color", "#FFFF00")
# # fill_opacity = st.sidebar.slider("Fill opacity", 0.0, 1.0, 0.4)
# # line_width = st.sidebar.slider("Border thickness", 1, 10, 2)

# # Load footprints
# query = f"SELECT * FROM images LIMIT {limit};"
# gdf = gpd.read_postgis(query, engine, geom_col="footprint")

# # Map
# m = leafmap.Map(center=[20, 78], zoom=5, basemap="CartoDB.DarkMatter")
# m.add_basemap("CartoDB.DarkMatter")
# m.add_gdf(
#     gdf,
#     layer_name="Image Footprints",
#     popup_property=["filename", "satellite", "acquisition_date"]  # <-- fixed
#     # stroke_color=stroke_color,
#     # fill_color=fill_color,
#     # fill_opacity=fill_opacity,
#     # line_width=line_width
# )

# m.to_streamlit(height=1000)



import streamlit as st
import geopandas as gpd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import leafmap.foliumap as leafmap

# --- Page setup ---
st.set_page_config(page_title="🛰️ Sphere Data Catalogue Dashboard", layout="wide")
st.title("🛰️ Sphere Data Catalogue Dashboard")

# --- Database setup ---
db = st.secrets["postgres"]

# Use connection pooling and auto-recycle idle connections
engine = create_engine(
    f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db']}",
    pool_size=5,         # max number of persistent connections
    max_overflow=10,     # temporary connections if pool is full
    pool_timeout=30,     # wait 30s before giving up
    pool_recycle=1800,   # recycle connections every 30 mins
)

# --- Sidebar controls ---
limit = st.sidebar.slider("Number of scenes to display", 20, 40, 60)

# --- Load data safely ---
query = f"SELECT * FROM images LIMIT {limit};"

try:
    with engine.connect() as conn:  # ensures connection auto-closes
        gdf = gpd.read_postgis(query, conn, geom_col="footprint")

except OperationalError as e:
    st.error(
        "⚠️ Database connection failed. Please try again later.\n\n"
        "Possible reason: too many active connections to the database."
    )
    st.stop()

except Exception as e:
    st.error(f"❌ Unexpected error while loading data: {e}")
    st.stop()

# --- Map visualization ---
if not gdf.empty:
    m = leafmap.Map(center=[20, 78], zoom=5, basemap="CartoDB.DarkMatter")
    m.add_basemap("CartoDB.DarkMatter")

    m.add_gdf(
        gdf,
        layer_name="Image Footprints",
        popup_property=["filename", "satellite", "acquisition_date"],
    )

    m.to_streamlit(height=1000)
else:
    st.warning("No image footprints found in the database.")
