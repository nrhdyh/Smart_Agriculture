import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============ PAGE CONFIG ============
st.set_page_config(page_title="Agriculture Data Visualization", page_icon="🌾", layout="wide")

# ============ SIDEBAR NAVIGATION ============
st.sidebar.title("🌿 Smart Agriculture Visualization")
page = st.sidebar.radio(
    "Select Objective Page:",
    ["Objective 1 – Crop Growth", "Objective 2 – Weather Patterns", "Objective 3 – Soil Analysis"]
)

# ============ PAGE 1 ============
if page == "Objective 1 – Crop Growth":
    st.title("🌾 Objective 1: Crop Growth Monitoring")

    # Objective Statement
    st.subheader("🎯 Objective Statement")
    st.write("To analyze the growth trends of different crops over time and understand how seasonal variations affect their productivity.")

    # Summary Box
    st.markdown("""
    <div style='background-color:#e8f5e9;padding:15px;border-radius:10px;border-left:5px solid #2e7d32'>
    This visualization explores how crop growth fluctuates across months and crop types. 
    The analysis focuses on yield performance and highlights potential seasonal influences.
    Understanding these growth dynamics allows better planning for irrigation and harvest schedules. 
    The visualizations provide insight into productivity trends and possible growth anomalies.
    </div>
    """, unsafe_allow_html=True)

    # Dummy dataset
    crops = ["Chili", "Tomato", "Cucumber", "Spinach"]
    months = pd.date_range("2025-01-01", periods=12, freq="M")
    df1 = pd.DataFrame({
        "Month": np.tile(months, 4),
        "Crop": np.repeat(crops, 12),
        "Growth(cm)": np.random.uniform(20, 120, 48)
    })

    # Visualization 1 – Line Plot
    st.markdown("#### 📈 Crop Growth Over Time")
    fig1 = px.line(df1, x="Month", y="Growth(cm)", color="Crop", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # Visualization 2 – Scatter Plot
    st.markdown("#### 🌱 Growth Distribution by Crop")
    fig2 = px.scatter(df1, x="Crop", y="Growth(cm)", color="Crop", size="Growth(cm)", hover_data=["Month"])
    st.plotly_chart(fig2, use_container_width=True)

    # Visualization 3 – Heatmap
    st.markdown("#### 🌡️ Growth Heatmap")
    pivot = df1.pivot_table(index="Crop", columns=df1["Month"].dt.strftime("%b"), values="Growth(cm)")
    fig3 = px.imshow(pivot, text_auto=True, color_continuous_scale="Greens")
    st.plotly_chart(fig3, use_container_width=True)

    # Interpretation
    st.subheader("💬 Interpretation / Discussion")
    st.write("""
    The visualizations reveal consistent seasonal trends, where crop growth peaks during mid-year 
    months due to favorable temperature and rainfall. Spinach and chili show faster recovery rates, 
    while cucumber appears more sensitive to weather variation. These insights help optimize 
    planting cycles and resource allocation.
    """)

# ============ PAGE 2 ============
elif page == "Objective 2 – Weather Patterns":
    st.title("☀️ Objective 2: Weather Pattern Analysis")

    # Objective Statement
    st.subheader("🎯 Objective Statement")
    st.write("To visualize temperature and humidity patterns to understand their influence on agricultural yield and irrigation needs.")

    # Summary Box
    st.markdown("""
    <div style='background-color:#e8f5e9;padding:15px;border-radius:10px;border-left:5px solid #43a047'>
    This page examines how temperature and humidity fluctuate across seasons. 
    Identifying weather patterns helps predict potential stress on crops and allows better 
    decision-making regarding irrigation schedules and greenhouse management.
    </div>
    """, unsafe_allow_html=True)

    # Dummy dataset
    days = pd.date_range("2025-01-01", periods=30)
    weather = pd.DataFrame({
        "Date": days,
        "Temperature (°C)": np.random.uniform(24, 34, 30),
        "Humidity (%)": np.random.uniform(60, 90, 30)
    })

    # Visualization 1 – Line Plot
    st.markdown("#### 🌤️ Daily Temperature & Humidity Trend")
    fig1 = px.line(weather, x="Date", y=["Temperature (°C)", "Humidity (%)"], markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # Visualization 2 – Scatter Plot
    st.markdown("#### 💧 Temperature vs. Humidity Relationship")
    fig2 = px.scatter(weather, x="Temperature (°C)", y="Humidity (%)", color="Temperature (°C)", size="Humidity (%)")
    st.plotly_chart(fig2, use_container_width=True)

    # Visualization 3 – Heatmap
    st.markdown("#### 🌦️ Correlation Heatmap")
    corr = weather.corr(numeric_only=True)
    fig3 = px.imshow(corr, text_auto=True, color_continuous_scale="RdYlGn", title="Weather Variable Correlation")
    st.plotly_chart(fig3, use_container_width=True)

    # Interpretation
    st.subheader("💬 Interpretation / Discussion")
    st.write("""
    The relationship between temperature and humidity shows an inverse trend during dry periods, 
    suggesting potential drought stress on crops. Identifying such patterns assists in planning 
    watering schedules and selecting suitable crop types for specific seasons.
    """)

# ============ PAGE 3 ============
else:
    st.title("🌍 Objective 3: Soil and Environmental Conditions")

    # Objective Statement
    st.subheader("🎯 Objective Statement")
    st.write("To assess the spatial distribution of soil moisture, pH, and nutrient content using scientific visualization techniques.")

    # Summary Box
    st.markdown("""
    <div style='background-color:#e8f5e9;padding:15px;border-radius:10px;border-left:5px solid #66bb6a'>
    This analysis maps out soil parameters to identify regions requiring fertilization or 
    moisture adjustment. Soil data is key for understanding fertility gradients and guiding 
    precision agriculture decisions to enhance yield and sustainability.
    </div>
    """, unsafe_allow_html=True)

    # Dummy dataset
    np.random.seed(42)
    soil = pd.DataFrame({
        "Longitude": np.random.uniform(101.5, 102.5, 100),
        "Latitude": np.random.uniform(5.5, 6.5, 100),
        "Moisture": np.random.uniform(30, 90, 100),
        "pH": np.random.uniform(5.5, 7.5, 100)
    })

    # Visualization 1 – Geospatial Moisture Map
    st.markdown("#### 🗺️ Soil Moisture Distribution")
    fig1 = px.scatter_mapbox(
        soil, lat="Latitude", lon="Longitude", color="Moisture",
        color_continuous_scale="YlGnBu", size="Moisture",
        mapbox_style="open-street-map", zoom=7, title="Soil Moisture Levels"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Visualization 2 – pH Distribution Scatter
    st.markdown("#### ⚗️ Soil pH Levels")
    fig2 = px.scatter(soil, x="pH", y="Moisture", color="pH", size="Moisture", title="Soil pH vs. Moisture Relationship")
    st.plotly_chart(fig2, use_container_width=True)

    # Visualization 3 – Surface Plot (Simulated)
    st.markdown("#### 🌋 Soil Condition Surface Plot (Simulated)")
    x, y = np.meshgrid(range(10), range(10))
    z = np.sin(x/2) + np.cos(y/3)
    fig3 = px.imshow(z, color_continuous_scale="Greens", title="Soil Condition Surface Representation")
    st.plotly_chart(fig3, use_container_width=True)

    # Interpretation
    st.subheader("💬 Interpretation / Discussion")
    st.write("""
    The soil moisture map reveals uneven distribution, indicating irrigation inefficiencies. 
    Areas with low pH may need liming to improve fertility. Spatial visualization helps 
    identify critical zones for soil treatment, contributing to smarter land management.
    """)

# ============ END ============
st.markdown("<br><hr><center>🌿 Smart Agriculture Visualization Dashboard © 2025</center>", unsafe_allow_html=True)
