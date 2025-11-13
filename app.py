# import streamlit as st
# import geopandas as gpd
# from sqlalchemy import create_engine
# import leafmap.foliumap as leafmap

# # ----------------------------------------------------
# # Page setup
# # ----------------------------------------------------
# st.set_page_config(page_title="Sphere Data Catalogue", layout="wide")
# st.title("🛰️ Sphere Data Catalogue Dashboard")

# # ----------------------------------------------------
# # Database connection
# # ----------------------------------------------------
# db = st.secrets["postgres"]
# engine = create_engine(
#     f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db']}"
# )

# # ----------------------------------------------------
# # Sidebar Controls
# # ----------------------------------------------------
# st.sidebar.header("Display Filters")

# # Limit number of scenes
# limit = st.sidebar.slider("Number of scenes to display", 20, 40, 60)

# # --- 1️⃣ Sensor Type Toggle ---
# st.sidebar.subheader("🛰️ Sensor Type")
# show_eo = st.sidebar.checkbox("EO (Electro-Optical)", value=True)
# show_sar = st.sidebar.checkbox("SAR (Synthetic Aperture Radar)", value=True)

# sensor_filters = []
# if show_eo:
#     sensor_filters.append("'EO'")
# if show_sar:
#     sensor_filters.append("'SAR'")

# sensor_condition = (
#     f"sensor_type IN ({','.join(sensor_filters)})"
#     if sensor_filters
#     else "FALSE"
# )

# # --- 2️⃣ Acquisition Year Toggle (2020–2025) ---
# st.sidebar.subheader("📅 Acquisition Year")
# year_filters = []
# for year in range(2020, 2025):
#     if st.sidebar.checkbox(f"{year}", value=True):
#         year_filters.append(str(year))

# # year_condition = (
# #     f"EXTRACT(YEAR FROM acquisition_date)::int IN ({','.join(year_filters)})"
# #     if year_filters
# #     else "FALSE"
# # )

# # --- 3️⃣ Resolution Filters ---
# st.sidebar.subheader("📏 Resolution Range (m)")
# res_ranges = {
#     "0.3–0.5 m": (0.3, 0.5),
#     "0.6–1.0 m": (0.6, 1.0),
#     "1.0 m & above": (1.0, 10.0)
# }

# selected_res = []
# for label in res_ranges:
#     if st.sidebar.checkbox(f"{label}", value=True):
#         selected_res.append(res_ranges[label])

# # res_conditions = [
# #     f"(resolution_m BETWEEN {low} AND {high})" for low, high in selected_res
# # ]
# # res_condition = " OR ".join(res_conditions) if res_conditions else "FALSE"

# # ----------------------------------------------------
# # SQL Query — combining all filters
# # ----------------------------------------------------
# image_query = f"""
#     SELECT category, file_name, sensor_type, footprint
#     FROM images
#     LIMIT {limit};
# """

# labels_query = """
#     SELECT class, subclass, file_name, geometry
#     FROM labels
#     LIMIT 500;
# """

# # ----------------------------------------------------
# # Load Data
# # ----------------------------------------------------
# try:
#     gdf_images = gpd.read_postgis(image_query, engine, geom_col="footprint")
#     gdf_labels = gpd.read_postgis(labels_query, engine, geom_col="geometry")
# except Exception as e:
#     st.error(f"Database query failed: {e}")
#     st.stop()

# if gdf_images.empty and gdf_labels.empty:
#     st.warning("No data found for the selected filters.")
#     st.stop()

# # ----------------------------------------------------
# # Map Setup
# # ----------------------------------------------------
# m = leafmap.Map(center=[20, 78], zoom=5, basemap="CartoDB.DarkMatter")
# m.add_basemap("CartoDB.DarkMatter")

# # --- Styles ---
# image_style = {
#     "color": "#2E8B57",         # Sea green outline
#     "weight": 2,
#     "fillColor": "#2E8B57",
#     "fillOpacity": 0.3
# }

# label_style = {
#     "color": "#FFD700",         # Gold outline
#     "weight": 2,
#     "fillColor": "#FFD700",
#     "fillOpacity": 0.5
# }

# # --- Add layers ---
# if not gdf_images.empty:
#     m.add_gdf(gdf_images, layer_name="Image Footprints", style=image_style)

# if not gdf_labels.empty:
#     m.add_gdf(gdf_labels, layer_name="Labels", style=label_style)

# # ----------------------------------------------------
# # Render Map
# # ----------------------------------------------------
# m.to_streamlit(height=700)
##########################################################################################################################
# import streamlit as st
# import geopandas as gpd
# from sqlalchemy import create_engine
# import leafmap.foliumap as leafmap
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# # ----------------------------------------------------
# # 🎨 Page setup — Black & Orange theme
# # ----------------------------------------------------
# st.set_page_config(page_title="🛰️ Sphere Data Catalogue", layout="wide")

# st.markdown("""
#     <style>
#     body {
#         background-color: #0e0e0e;
#         color: #f5f5f5;
#     }
#     .stApp {
#         background-color: #0e0e0e;
#     }
#     .metric-card {
#         background-color: rgba(255, 140, 0, 0.15);
#         padding: 15px;
#         border-radius: 12px;
#         text-align: center;
#         margin-bottom: 10px;
#         border: 1px solid rgba(255, 165, 0, 0.25);
#     }
#     .metric-title {
#         color: #ffa500;
#         font-weight: 600;
#         font-size: 16px;
#     }
#     .metric-value {
#         font-size: 24px;
#         font-weight: 700;
#         color: #ffffff;
#     }
#     .plotly-chart {
#         background-color: transparent !important;
#     }
#     </style>
# """, unsafe_allow_html=True)

# st.title("🛰️ Sphere Data Catalogue Dashboard")

# # ----------------------------------------------------
# # 🗃️ Database connection
# # ----------------------------------------------------
# db = st.secrets["postgres"]
# engine = create_engine(
#     f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db']}"
# )

# # ----------------------------------------------------
# # 🎛️ Sidebar Filters
# # ----------------------------------------------------
# st.sidebar.header("🔍 Display Filters")

# limit = st.sidebar.slider("Number of scenes to display", 20, 40, 60)

# # Sensor type toggles
# st.sidebar.subheader("🛰️ Sensor Type")
# show_eo = st.sidebar.checkbox("EO", value=True)
# show_sar = st.sidebar.checkbox("SAR", value=True)
# sensor_filters = []
# if show_eo:
#     sensor_filters.append("'EO'")
# if show_sar:
#     sensor_filters.append("'SAR'")
# sensor_condition = (
#     f"sensor_type IN ({','.join(sensor_filters)})" if sensor_filters else "FALSE"
# )

# # Acquisition year toggles
# st.sidebar.subheader("📅 Acquisition Year")
# year_filters = []
# for year in range(2020, 2026):
#     if st.sidebar.checkbox(f"{year}", value=True):
#         year_filters.append(str(year))

# # Resolution filters
# st.sidebar.subheader("📏 Resolution Range (m)")
# res_ranges = {
#     "0.3–0.5 m": (0.3, 0.5),
#     "0.6–1.0 m": (0.6, 1.0),
#     "1.0 m & above": (1.0, 10.0)
# }
# selected_res = []
# for label in res_ranges:
#     if st.sidebar.checkbox(label, value=True):
#         selected_res.append(res_ranges[label])

# # ----------------------------------------------------
# # 🧠 SQL Queries
# # ----------------------------------------------------
# image_query = f"""
#     SELECT category, file_name, sensor_type, footprint
#     FROM images
#     LIMIT {limit};
# """

# labels_query = """
#     SELECT class, subclass, file_name, sensor_type, category, geometry
#     FROM labels
#     LIMIT 5000;
# """

# # ----------------------------------------------------
# # 📥 Load Data
# # ----------------------------------------------------
# try:
#     gdf_images = gpd.read_postgis(image_query, engine, geom_col="footprint")
#     gdf_labels = gpd.read_postgis(labels_query, engine, geom_col="geometry")
# except Exception as e:
#     st.error(f"Database query failed: {e}")
#     st.stop()

# if gdf_images.empty and gdf_labels.empty:
#     st.warning("No data found for the selected filters.")
#     st.stop()

# # ----------------------------------------------------
# # 🧭 Layout: Map | Metrics panel
# # ----------------------------------------------------
# col1, col2 = st.columns([2, 1])

# # ----------------------------------------------------
# # 🌍 LEFT PANEL — INTERACTIVE MAP
# # ----------------------------------------------------
# with col1:
#     m = leafmap.Map(center=[20, 78], zoom=5)
#     m.add_basemap("SATELLITE")
#     m.add_basemap("CartoDB.DarkMatter")

#     # Sea-green footprints
#     image_style = {
#         "color": "#0F1EE6",
#         "weight": 2,
#         "fillColor": "#0F1EE6",
#         "fillOpacity": 0.3
#     }
#     label_style = {
#         "color": "#FF0000",
#         "weight": 2,
#         "fillColor":"#FF0000",
#         "fillOpacity": 0.3
#     }
    

#     if not gdf_images.empty:
#         m.add_gdf(gdf_images, layer_name="Image Footprints", style=image_style)
#     if not gdf_labels.empty:
#         m.add_gdf(gdf_labels, layer_name="Labels", style=label_style)

#     m.to_streamlit(height=700)

# # ----------------------------------------------------
# # 📊 RIGHT PANEL — METRIC STYLE DASHBOARD
# # ----------------------------------------------------
# with col2:
#     st.subheader("📈 Subclass Metrics Overview")

#     if not gdf_labels.empty and "subclass" in gdf_labels.columns:
#         label_counts = gdf_labels["subclass"].value_counts().reset_index()
#         label_counts.columns = ["Subclass", "Count"]

#         total_labels = label_counts["Count"].sum()
#         st.markdown(f"<div class='metric-card'><div class='metric-title'>Total Labels</div><div class='metric-value'>{total_labels:,}</div></div>", unsafe_allow_html=True)

#         # Display metric cards for top subclasses
#         for _, row in label_counts.iterrows():
#             st.markdown(
#                 f"<div class='metric-card'>"
#                 f"<div class='metric-title'>{row['Subclass']}</div>"
#                 f"<div class='metric-value'>{row['Count']:,}</div>"
#                 f"</div>",
#                 unsafe_allow_html=True
#             )

#         # Small trend/line chart (visual overview)
#         fig = px.line(
#             label_counts,
#             x="Subclass",
#             y="Count",
#             markers=True,
#             title="Subclass Distribution Trend",
#             color_discrete_sequence=["#FFA500"]
#         )

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",
#             paper_bgcolor="rgba(0,0,0,0)",
#             font_color="white",
#             title_font_size=16,
#             margin=dict(l=20, r=20, t=40, b=20)
#         )

#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("No label data available to display statistics.")

####################################################################################

# import streamlit as st
# import geopandas as gpd
# from sqlalchemy import create_engine
# import leafmap.foliumap as leafmap
# import pandas as pd
# import plotly.express as px

# # ----------------------------------------------------
# # 🎨 Page setup — Black & Orange theme
# # ----------------------------------------------------
# st.set_page_config(page_title="🛰️ Sphere Data Catalogue", layout="wide")

# st.markdown("""
#     <style>
#     body {
#         background-color: #0e0e0e;
#         color: #f5f5f5;
#     }
#     .stApp {
#         background-color: #0e0e0e;
#     }
#     .metric-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
#         gap: 10px;
#         margin-top: 10px;
#     }
#     .metric-card {
#         background-color: rgba(255, 140, 0, 0.12);
#         padding: 15px 10px;
#         border-radius: 12px;
#         text-align: center;
#         border: 1px solid rgba(255, 165, 0, 0.25);
#         transition: transform 0.2s ease-in-out;
#     }
#     .metric-card:hover {
#         transform: scale(1.03);
#         background-color: rgba(255, 165, 0, 0.2);
#     }
#     .metric-title {
#         color: #ffa500;
#         font-weight: 600;
#         font-size: 14px;
#         margin-bottom: 5px;
#     }
#     .metric-value {
#         font-size: 20px;
#         font-weight: 700;
#         color: #ffffff;
#     }
#     </style>
# """, unsafe_allow_html=True)

# st.title("🛰️ Sphere Data Catalogue Dashboard")

# # ----------------------------------------------------
# # 🗃️ Database connection
# # ----------------------------------------------------
# db = st.secrets["postgres"]
# engine = create_engine(
#     f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db']}"
# )

# # ----------------------------------------------------
# # 🎛️ Sidebar Filters
# # ----------------------------------------------------
# st.sidebar.header("🔍 Display Filters")

# limit = st.sidebar.slider("Number of scenes to display", 20, 40, 60)


# # Sensor type toggles
# st.sidebar.subheader("🛰️ Sensor Type")
# show_eo = st.sidebar.checkbox("EO", value=True)
# show_sar = st.sidebar.checkbox("SAR", value=True)
# sensor_filters = []
# if show_eo:
#     sensor_filters.append("'EO'")
# if show_sar:
#     sensor_filters.append("'SAR'")
# sensor_condition = (
#     f"sensor_type IN ({','.join(sensor_filters)})" if sensor_filters else "FALSE"
# )

# # # Acquisition year toggles
# # st.sidebar.subheader("📅 Acquisition Year")
# # year_filters = []
# # for year in range(2020, 2026):
# #     if st.sidebar.checkbox(f"{year}", value=True):
# #         year_filters.append(str(year))

# # # Resolution filters
# # st.sidebar.subheader("📏 Resolution Range (m)")
# # res_ranges = {
# #     "0.3–0.5 m": (0.3, 0.5),
# #     "0.6–1.0 m": (0.6, 1.0),
# #     "1.0 m & above": (1.0, 10.0)
# # }
# # selected_res = []
# # for label in res_ranges:
# #     if st.sidebar.checkbox(label, value=True):
# #         selected_res.append(res_ranges[label])

# # ----------------------------------------------------
# # 🧠 SQL Queries
# # ----------------------------------------------------
# image_query = f"""
#     SELECT category, file_name, sensor_type, footprint
#     FROM images
#     LIMIT {limit};
# """

# labels_query = """
#     SELECT class, subclass, file_name, sensor_type, category, geometry
#     FROM labels
#     LIMIT 8000;
# """

# # ----------------------------------------------------
# # 📥 Load Data
# # ----------------------------------------------------
# try:
#     gdf_images = gpd.read_postgis(image_query, engine, geom_col="footprint")
#     gdf_labels = gpd.read_postgis(labels_query, engine, geom_col="geometry")
# except Exception as e:
#     st.error(f"Database query failed: {e}")
#     st.stop()

# if gdf_images.empty and gdf_labels.empty:
#     st.warning("No data found for the selected filters.")
#     st.stop()

# # ----------------------------------------------------
# # 🧭 Layout: Map | Metrics panel
# # ----------------------------------------------------
# col1, col2 = st.columns([2, 1])

# # ----------------------------------------------------
# # 🌍 LEFT PANEL — INTERACTIVE MAP
# # ----------------------------------------------------
# with col1:
#     m = leafmap.Map(center=[20, 78], zoom=5)
#     m.add_basemap("SATELLITE")
#     m.add_basemap("CartoDB.DarkMatter")

#     # Map styles
#     image_style = {
#         "color": "#0F1EE6",
#         "weight": 2,
#         "fillColor": "#0F1EE6",
#         "fillOpacity": 0.3
#     }
#     label_style = {
#         "color": "#FF0000",
#         "weight": 2,
#         "fillColor": "#FF0000",
#         "fillOpacity": 0.3
#     }

#     if not gdf_images.empty:
#         m.add_gdf(gdf_images, layer_name="Image Footprints", style=image_style)
#     if not gdf_labels.empty:
#         m.add_gdf(gdf_labels, layer_name="Labels", style=label_style)

#     m.to_streamlit(height=700)

# # ----------------------------------------------------
# # 📊 RIGHT PANEL — METRIC GRID DASHBOARD
# # ----------------------------------------------------
# with col2:
#     st.subheader("📈 Subclass Metrics Overview")

#     if not gdf_labels.empty and "subclass" in gdf_labels.columns:
#         label_counts = gdf_labels["subclass"].value_counts().reset_index()
#         label_counts.columns = ["Subclass", "Count"]

#         total_labels = label_counts["Count"].sum()
#         st.markdown(
#             f"""
#             <div class='metric-card'>
#                 <div class='metric-title'>Total Labels</div>
#                 <div class='metric-value'>{total_labels:,}</div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         # Metric cards grid
#         cards_html = "<div class='metric-grid'>"
#         for _, row in label_counts.iterrows():
#             cards_html += (
#                 f"<div class='metric-card'>"
#                 f"<div class='metric-title'>{row['Subclass']}</div>"
#                 f"<div class='metric-value'>{row['Count']:,}</div>"
#                 f"</div>"
#             )
#         cards_html += "</div>"

#         st.markdown(cards_html, unsafe_allow_html=True)

#         # Mini trend chart (compact, fits below grid)
#         fig = px.line(
#             label_counts,
#             x="Subclass",
#             y="Count",
#             markers=True,
#             title="Subclass Distribution Trend",
#             color_discrete_sequence=["#FFA500"]
#         )

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",
#             paper_bgcolor="rgba(0,0,0,0)",
#             font_color="white",
#             title_font_size=14,
#             height=280,
#             margin=dict(l=20, r=20, t=40, b=30)
#         )

#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("No label data available to display statistics.")

##########################################################################

import streamlit as st
import geopandas as gpd
from sqlalchemy import create_engine
import leafmap.foliumap as leafmap
import pandas as pd
import plotly.express as px
import folium
from folium import TileLayer

# ----------------------------------------------------
# 🎨 Page setup — Black & Orange theme
# ----------------------------------------------------
st.set_page_config(page_title="🛰️ Sphere Data Catalogue", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0e0e0e;
        color: #f5f5f5;
    }
    .stApp {
        background-color: #0e0e0e;
    }
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 10px;
        margin-top: 10px;
    }
    .metric-card {
        background-color: rgba(255, 140, 0, 0.12);
        padding: 15px 10px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(255, 165, 0, 0.25);
        transition: transform 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: scale(1.03);
        background-color: rgba(255, 165, 0, 0.2);
    }
    .metric-title {
        color: #ffa500;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
    }
    .sensor-toggle {
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛰️ Sphere Data Catalogue Dashboard")

# ----------------------------------------------------
# 🔘 EO / SAR Toggle Buttons (centered)
# ----------------------------------------------------
st.markdown("<div class='sensor-toggle'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    eo_clicked = st.button("EO", use_container_width=True)
with col2:
    sar_clicked = st.button("SAR", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Determine selected sensor
sensor_selected = None
if eo_clicked:
    sensor_selected = "EO"
elif sar_clicked:
    sensor_selected = "SAR"

sensor_condition = f"sensor_type = '{sensor_selected}'" if sensor_selected else "TRUE"

# ----------------------------------------------------
# 🗃️ Database connection
# ----------------------------------------------------
db = st.secrets["postgres"]
engine = create_engine(
    f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db']}"
)

# ----------------------------------------------------
# 🧠 SQL Queries
# ----------------------------------------------------
image_query = f"""
    SELECT category, file_name, sensor_type, footprint
    FROM images
    WHERE {sensor_condition}
    LIMIT 60;
"""

labels_query = f"""
    SELECT class, subclass, file_name, sensor_type, category, geometry
    FROM labels
    WHERE {sensor_condition}
    LIMIT 8000;
"""

# ----------------------------------------------------
# 📥 Load Data
# ----------------------------------------------------
try:
    gdf_images = gpd.read_postgis(image_query, engine, geom_col="footprint")
    gdf_labels = gpd.read_postgis(labels_query, engine, geom_col="geometry")
except Exception as e:
    st.error(f"Database query failed: {e}")
    st.stop()

if gdf_images.empty and gdf_labels.empty:
    st.warning("No data found for the selected sensor type.")
    st.stop()

# ----------------------------------------------------
# 🧭 Layout: Map | Metrics panel
# ----------------------------------------------------
col1, col2 = st.columns([2, 1])

# ----------------------------------------------------
# 🌍 LEFT PANEL — INTERACTIVE MAP
# ----------------------------------------------------
# with col1:
#     m = leafmap.Map(center=[20, 78], zoom=5)
#     m.add_basemap("SATELLITE")
#     m.add_basemap("CartoDB.DarkMatter")

#     # Map styles
#     image_style = {
#         "color": "#0F1EE6",
#         "weight": 2,
#         "fillColor": "#0F1EE6",
#         "fillOpacity": 0.3
#     }
#     label_style = {
#         "color": "#FF0000",
#         "weight": 2,
#         "fillColor": "#FF0000",
#         "fillOpacity": 0.3
#     }

#     if not gdf_images.empty:
#         m.add_gdf(gdf_images, layer_name="Image Footprints", style=image_style)
#     if not gdf_labels.empty:
#         m.add_gdf(gdf_labels, layer_name="Labels", style=label_style)

#     m.to_streamlit(height=600)

with col1:

    m = leafmap.Map(center=[20, 78], zoom=5)

    # Google Satellite layer
    TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google Satellite",
        name="Google Satellite",
        overlay=False,
        control=True,
    ).add_to(m)

    # Optional dark background for toggle
    TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="© OpenStreetMap, © CartoDB",
        name="Dark Matter",
        overlay=False,
        control=True,
    ).add_to(m)

    # Map styles for overlay layers
    image_style = {
        "color": "#0F1EE6",
        "weight": 2,
        "fillColor": "#0F1EE6",
        "fillOpacity": 0.3
    }
    label_style = {
        "color": "#FF0000",
        "weight": 2,
        "fillColor": "#FF0000",
        "fillOpacity": 0.3
    }

    if not gdf_images.empty:
        m.add_gdf(gdf_images, layer_name="Image Footprints", style=image_style)
    if not gdf_labels.empty:
        m.add_gdf(gdf_labels, layer_name="Labels", style=label_style)

    folium.LayerControl().add_to(m)  # Add layer switcher
    m.to_streamlit(height=600)

# ----------------------------------------------------
# 📊 RIGHT PANEL — METRIC GRID DASHBOARD
# ----------------------------------------------------
with col2:
    st.subheader("📈 Subclass Metrics Overview")

    if not gdf_labels.empty and "subclass" in gdf_labels.columns:
        label_counts = gdf_labels["subclass"].value_counts().reset_index()
        label_counts.columns = ["Subclass", "Count"]
        total_labels = len(gdf_labels)
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-title'>Total Labels</div>
                <div class='metric-value'>{total_labels:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Metric cards grid
        cards_html = "<div class='metric-grid'>"
        for _, row in label_counts.iterrows():
            cards_html += (
                f"<div class='metric-card'>"
                f"<div class='metric-title'>{row['Subclass']}</div>"
                f"<div class='metric-value'>{row['Count']:,}</div>"
                f"</div>"
            )
        cards_html += "</div>"

        st.markdown(cards_html, unsafe_allow_html=True)

        # Mini trend chart (compact, fits below grid)
        fig = px.line(
            label_counts,
            x="Subclass",
            y="Count",
            markers=True,
            title="Subclass Distribution Trend",
            color_discrete_sequence=["#FFA500"]
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_size=14,
            height=280,
            margin=dict(l=20, r=20, t=40, b=30)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No label data available to display statistics.")
