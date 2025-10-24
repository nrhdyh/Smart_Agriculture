import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    page_icon="🌱",
    layout="wide",
)

# --- CUSTOM CSS STYLE ---
st.markdown("""
    <style>
        /* Background Gradient */
        .main {
            background: linear-gradient(135deg, #d6f5e3 0%, #f2fff8 100%);
            font-family: 'Poppins', sans-serif;
        }
        /* Header Banner */
        .header {
            background: linear-gradient(90deg, #1b5e20, #43a047);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        }
        h1 {
            font-size: 42px;
            margin: 0;
            letter-spacing: 1px;
        }
        .subtitle {
            font-size: 18px;
            opacity: 0.9;
        }
        /* Metric Cards */
        .metric-card {
            background: rgba(255,255,255,0.7);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: 0.3s;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 18px rgba(0,0,0,0.2);
        }
        .stPlotlyChart, .stDataFrame {
            background-color: white;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        /* Footer */
        .footer {
            text-align: center;
            font-size: 14px;
            color: #2b4d3f;
            padding: 20px;
            margin-top: 30px;
            border-top: 1px solid #b8e0c2;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header">
        <h1>🌿 Smart Agriculture Dashboard</h1>
        <div class="subtitle">Empowering Sustainable Farming Through Data Intelligence</div>
    </div>
""", unsafe_allow_html=True)

# --- DATE DISPLAY ---
col_date1, col_date2 = st.columns([3, 1])
with col_date1:
    st.subheader("📅 Today's Overview")
with col_date2:
    st.metric("Date", dt.date.today().strftime("%d %B %Y"))

# --- SIMULATED SENSOR DATA ---
st.markdown("## 🌱 Real-Time Sensor Readings")

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
    with cols[i]:
        st.markdown(f"""
            <div class='metric-card'>
                <h3>{row["Sensor"]}</h3>
                <h2 style='color:#1b5e20;'>{row["Current"]}</h2>
            </div>
        """, unsafe_allow_html=True)

# --- WEATHER FORECAST CHART ---
st.markdown("## ☀️ Weather Forecast (Next 7 Days)")
days = pd.date_range(dt.date.today(), periods=7)
weather_df = pd.DataFrame({
    "Date": days,
    "Temperature (°C)": np.random.uniform(25, 33, 7),
    "Humidity (%)": np.random.uniform(60, 80, 7),
})
fig = px.line(
    weather_df,
    x="Date",
    y=["Temperature (°C)", "Humidity (%)"],
    markers=True,
    title="Weekly Temperature and Humidity Trend",
    color_discrete_sequence=["#2e7d32", "#81c784"]
)
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=14, color='#1b5e20'),
)
st.plotly_chart(fig, use_container_width=True)

# --- CROP HEALTH SECTION ---
st.markdown("## 🌾 Crop Health Overview")
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
    title="Crop Health Index"
)
fig_bar.update_traces(textposition="outside")
fig_bar.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=14, color='#1b5e20'),
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- FOOTER ---
st.markdown("""
    <div class='footer'>
        👩‍🌾 Developed with 💚 for sustainable agriculture.<br>
        © 2025 SmartAgri Dashboard
    </div>
""", unsafe_allow_html=True)
