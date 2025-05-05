import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns
import folium
from folium import plugins
import json
import requests

# Set Streamlit Page Config
st.set_page_config(page_title="Global Trade Network", page_icon="", layout="wide")

# Country coordinates data (sample of major countries)
# COUNTRY_COORDINATES = {
#     "United States": {"lat": 37.0902, "lon": -95.7129},
#     "China": {"lat": 35.8617, "lon": 104.1954},
#     "Japan": {"lat": 36.2048, "lon": 138.2529},
#     "Germany": {"lat": 51.1657, "lon": 10.4515},
#     "United Kingdom": {"lat": 55.3781, "lon": -3.4360},
#     "France": {"lat": 46.2276, "lon": 2.2137},
#     "India": {"lat": 20.5937, "lon": 78.9629},
#     "Italy": {"lat": 41.8719, "lon": 12.5674},
#     "Brazil": {"lat": -14.2350, "lon": -51.9253},
#     "Canada": {"lat": 56.1304, "lon": -106.3468},
#     # Add more countries as needed
# }

COUNTRY_COORDINATES = {
    "United States": {"lat": 37.0902, "lon": -95.7129},
    "China": {"lat": 35.8617, "lon": 104.1954},
    "Japan": {"lat": 36.2048, "lon": 138.2529},
    "Germany": {"lat": 51.1657, "lon": 10.4515},
    "United Kingdom": {"lat": 55.3781, "lon": -3.4360},
    "France": {"lat": 46.2276, "lon": 2.2137},
    "India": {"lat": 20.5937, "lon": 78.9629},
    "Italy": {"lat": 41.8719, "lon": 12.5674},
    "Brazil": {"lat": -14.2350, "lon": -51.9253},
    "Canada": {"lat": 56.1304, "lon": -106.3468},
    "Russia": {"lat": 61.5240, "lon": 105.3188},
    "Australia": {"lat": -25.2744, "lon": 133.7751},
    "South Korea": {"lat": 35.9078, "lon": 127.7669},
    "Mexico": {"lat": 23.6345, "lon": -102.5528},
    "Indonesia": {"lat": -0.7893, "lon": 113.9213},
    "South Africa": {"lat": -30.5595, "lon": 22.9375},
    "Saudi Arabia": {"lat": 23.8859, "lon": 45.0792},
    "Argentina": {"lat": -38.4161, "lon": -63.6167},
    "Turkey": {"lat": 38.9637, "lon": 35.2433},
    "Spain": {"lat": 40.4637, "lon": -3.7492},
    "Netherlands": {"lat": 52.1326, "lon": 5.2913},
    "Sweden": {"lat": 60.1282, "lon": 18.6435},
    "Switzerland": {"lat": 46.8182, "lon": 8.2275},
    "Poland": {"lat": 51.9194, "lon": 19.1451},
    "Egypt": {"lat": 26.8206, "lon": 30.8025}
}


# Custom CSS for styling
st.markdown("""
    <style>
        .stApp {
            background-color: grey;
            padding: 20px;
        }
        .reportview-container .main .block-container {
            padding: 20px;
            border-radius: 10px;
            background-color: skyblue;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        }
        .sidebar .sidebar-content {
            background-color: #4CAF50;
            color: white;
        }
        .folium-map {
            width: 100%;
            height: 500px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
    <div style="text-align: center; color: #333;">
        <h1 style="color: skyblue;">Global Trade Network</h1>
        <p style="font-size: 18px;">Analyze international trade data and visualize connections between countries.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar File Upload
with st.sidebar:
    st.header("📂 Upload Data")
    uploaded_file = st.file_uploader("Upload your trade data (CSV)", type="csv")

def create_trade_map(selected_country, df_top, top_partners):
    # Create base map centered on selected country
    if selected_country in COUNTRY_COORDINATES:
        center_lat = COUNTRY_COORDINATES[selected_country]["lat"]
        center_lon = COUNTRY_COORDINATES[selected_country]["lon"]
    else:
        center_lat, center_lon = 0, 0  # Default to world center if country not found
    
    # Add slider for longitude adjustment
    init_lon = float(center_lon) if isinstance(center_lon, (int, float)) else 0.0
    longitude_offset = st.slider(
        "Adjust Map View (Longitude)",
        min_value=-180.0,
        max_value=180.0,
        value=init_lon,
        step=10.0,
        help="Slide to shift the map view left or right"
    )
    
    # Ensure location is a list of two float values
    map_location = [float(center_lat), float(longitude_offset)]
    m = folium.Map(location=map_location, zoom_start=3)
    
    # Add selected country marker
    if selected_country in COUNTRY_COORDINATES:
        folium.CircleMarker(
            location=[COUNTRY_COORDINATES[selected_country]["lat"], 
                     COUNTRY_COORDINATES[selected_country]["lon"]],
            radius=10,
            color='red',
            fill=True,
            popup=folium.Popup(
                f"<b>{selected_country}</b><br>" 
                f"Latitude: {COUNTRY_COORDINATES[selected_country]['lat']:.4f}<br>" 
                f"Longitude: {COUNTRY_COORDINATES[selected_country]['lon']:.4f}",
                max_width=200
            ),
            tooltip=selected_country
        ).add_to(m)
        
        # Add trading partners and connection lines
        max_trade = top_partners.max()
        for partner, trade_value in top_partners.items():
            if partner in COUNTRY_COORDINATES:
                # Add partner marker
                folium.CircleMarker(
                    location=[COUNTRY_COORDINATES[partner]["lat"], 
                             COUNTRY_COORDINATES[partner]["lon"]],
                    radius=8,
                    color='blue',
                    fill=True,
                    popup=folium.Popup(
                        f"<b>{partner}</b><br>" 
                        f"Latitude: {COUNTRY_COORDINATES[partner]['lat']:.4f}<br>" 
                        f"Longitude: {COUNTRY_COORDINATES[partner]['lon']:.4f}<br>" 
                        f"Trade Value: {trade_value:,.0f} USD",
                        max_width=200
                    ),
                    tooltip=f"{partner}"
                ).add_to(m)
                
                # Draw connection line
                line_weight = (trade_value / max_trade) * 5
                color_intensity = int((trade_value / max_trade) * 255)
                
                folium.PolyLine(
                    locations=[[COUNTRY_COORDINATES[selected_country]["lat"], 
                              COUNTRY_COORDINATES[selected_country]["lon"]],
                             [COUNTRY_COORDINATES[partner]["lat"], 
                              COUNTRY_COORDINATES[partner]["lon"]]],
                    weight=line_weight,
                    color=f'rgb({color_intensity},0,{255-color_intensity})',
                    popup=f"Trade Value: {trade_value:,.0f} USD"
                ).add_to(m)
    
    return m

if uploaded_file:
    try:
        with st.spinner("Processing data..."):
            # Read data
            df = pd.read_csv(uploaded_file)

            # Validate required columns
            required_columns = {'ReporterName', 'PartnerName', 'TradeValue in 1000 USD'}
            if not required_columns.issubset(df.columns):
                st.error("❌ CSV file is missing required columns: ReporterName, PartnerName, TradeValue in 1000 USD")
            else:
                # Sidebar country selection
                selected_country = st.sidebar.selectbox(
                    "🌎 Select a country:",
                    sorted(df['ReporterName'].dropna().unique()),
                    index=0
                )

                # Filter for the selected country
                df_country = df[df['ReporterName'] == selected_country].dropna(subset=['PartnerName', 'TradeValue in 1000 USD'])
                df_country = df_country[df_country['PartnerName'] != 'Unspecified']

                # Get top 10 trading partners
                top_partners = df_country.groupby('PartnerName')['TradeValue in 1000 USD'].sum().nlargest(10)
                df_top = df_country[df_country['PartnerName'].isin(top_partners.index)]

                # Create two columns for visualizations
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Display Map
                    st.markdown("### 🗺️ Trade Flow Map")
                    trade_map = create_trade_map(selected_country, df_top, top_partners)
                    st_folium = st.components.v1.html(trade_map._repr_html_(), height=400)
                
                with col2:
                    # Show Bar Chart
                    st.markdown("### 📊 Trade Value Distribution")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    sns.barplot(y=top_partners.index, x=top_partners.values, palette='coolwarm', ax=ax)
                    ax.set_xlabel("Trade Value (in 1000 USD)")
                    ax.set_ylabel("Trading Partner")
                    st.pyplot(fig)

                # Create Graph below the map and bar chart
                st.markdown("### 📌 Trade Network Graph")
                
                # Create Graph
                G = nx.Graph()
                G.add_node(selected_country, color="#E74C3C", size=800)
                
                for country in top_partners.index:
                    G.add_node(country, color="#3498DB", size=600)
                    trade_value = top_partners[country]
                    G.add_edge(selected_country, country, weight=trade_value)

                # Define Node and Edge Properties
                node_colors = ["#E74C3C" if node == selected_country else "#3498DB" for node in G.nodes]
                node_sizes = [800 if node == selected_country else 600 for node in G.nodes]
                edge_weights = [G[u][v]['weight'] / max(top_partners) * 5 if max(top_partners) > 0 else 1 for u, v in G.edges]
                edge_colors = [cm.viridis(G[u][v]['weight'] / max(top_partners)) for u, v in G.edges]

                # Select Layout
                layout_options = {
                    "Spring Layout": lambda G: nx.spring_layout(G, seed=42),
                    "Circular Layout": nx.circular_layout,
                    "Kamada-Kawai Layout": nx.kamada_kawai_layout
                }
                layout_choice = st.sidebar.selectbox("📌 Select Graph Layout:", list(layout_options.keys()))
                pos = layout_options[layout_choice](G)

                # Display Graph
                fig, ax = plt.subplots(figsize=(12, 8))
                nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors,
                        font_size=10, edge_color=edge_colors, width=edge_weights, alpha=0.7, ax=ax)
                st.pyplot(fig)
                plt.clf()
                
                # Show Data Table with Expander
                with st.expander(f"📊 View Top 10 Trading Partners Data for {selected_country}"):
                    st.dataframe(df_top)
                    csv = df_top.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download Data as CSV", data=csv, file_name=f"{selected_country}_trade_data.csv", mime='text/csv')

                # Show Summary Statistics
                with st.expander(f"📈 View Summary Statistics for {selected_country}"):
                    st.write(df_top.describe())

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
else:
    st.info("📂 Please upload a CSV file to analyze.")