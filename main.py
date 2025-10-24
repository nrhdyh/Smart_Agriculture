import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    page_icon="🌿",
    layout="wide",
)

# --- CUSTOM STYLE ---
st.markdown("""
    <style>
        .main {
            background-color: #f0f9f4;
            color: #2b4d3f;
        }
        .metric {
            background-color: #e2f3ea;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        h1, h2, h3 {
            color: #2b4d3f;
        }
        .stDataFrame, .stPlotlyChart {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🌿 Smart Agriculture Monitoring System")
st.write("Empowering sustainable farming through data-driven insights.")

# --- DATE & TIME ---
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("📅 Today's Overview")
with col2:
    st.metric("Date", dt.date.today().strftime("%d %B %Y"))

# --- SIMULATED SENSOR DATA ---
st.markdown("### 🌱 Real-Time Sensor Readings (Simulated Data)")

sensor_data = {
    "Sensor": ["Temperature (°C)", "Humidity (%)", "Soil Moisture (%)", "Light Intensity (LUX)"],
    "Current": [round(np.random.uniform(24, 35), 1),
                round(np.random.uniform(55, 80), 1),
                round(np.random.uniform(40, 90), 1),
                round(np.random.uniform(1000, 5000), 0)]
}
df = pd.DataFrame(sensor_data)

cols = st.columns(4)
for i, row in df.iterrows():
    cols[i].metric(label=row["Sensor"], value=row["Current"])

# --- WEATHER FORECAST CHART ---
st.markdown("### ☀️ Weather Forecast (Next 7 Days)")

days = pd.date_range(dt.date.today(), periods=7)
weather_df = pd.DataFrame({
    "Date": days,
    "Temperature (°C)": np.random.uniform(25, 33, 7),
    "Humidity (%)": np.random.uniform(60, 80, 7),
})
fig = px.line(
    weather_df,
    x="Date", y=["Temperature (°C)", "Humidity (%)"],
    markers=True,
    title="Weekly Temperature and Humidity Trend",
    color_discrete_sequence=["#3a9257", "#59b89a"]
)
st.plotly_chart(fig, use_container_width=True)

# --- CROP HEALTH SECTION ---
st.markdown("### 🌾 Crop Health Overview")
crop_data = pd.DataFrame({
    "Crop": ["Chili", "Tomato", "Cucumber", "Spinach"],
    "Health (%)": [92, 85, 78, 95],
    "Water Needs (L/day)": [2.1, 1.8, 1.5, 1.2],
})

fig_bar = px.bar(
    crop_data,
    x="Crop",
    y="Health (%)",
    text="Health (%)",
    color="Health (%)",
    color_continuous_scale="greens",
    title="Crop Health Index",
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- FOOTER ---
st.markdown("""
---
👩‍🌾 Developed for sustainable agriculture monitoring.  
© 2025 SmartAgri Team
""")
