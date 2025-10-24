import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="🌿 Climate Smart Agriculture", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv("married_data_on_Climate_Smart_Agriculture.csv")

df = load_data()

# --- GLOBAL STYLE ---
st.markdown("""
    <style>
    body {
        background-color: #f4f9f4;
    }
    .main {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    h1, h2, h3, h4 {
        color: #2E7D32;
    }
    .stPlotlyChart {
        border-radius: 15px;
        background: #ffffff;
        box-shadow: 0 4px 10px rgba(0,0,0,0.07);
        padding: 15px;
    }
    .metric-box {
        background: linear-gradient(135deg, #A8E6CF, #DCEDC1);
        border-radius: 15px;
        padding: 15px 25px;
        text-align: center;
        color: #2E7D32;
        font-weight: bold;
        font-size: 22px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🌿 Climate-Smart Agriculture Dashboard")
st.markdown("""
### 🎯 Objective
To visualize how **married individuals** engage in **Climate-Smart Agriculture (CSA)** practices — focusing on awareness, adoption, education, and income trends.
""")

# --- KPI SUMMARY ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-box'>👩‍🌾 Total Records<br>{len(df)}</div>", unsafe_allow_html=True)
with col2:
    if "Gender" in df.columns:
        female = len(df[df["Gender"].str.lower() == "female"])
        st.markdown(f"<div class='metric-box'>♀ Female Participants<br>{female}</div>", unsafe_allow_html=True)
with col3:
    if "Region" in df.columns:
        st.markdown(f"<div class='metric-box'>🌍 Regions Covered<br>{df['Region'].nunique()}</div>", unsafe_allow_html=True)

st.markdown("---")

# --- SECTION 1: Awareness Level by Gender ---
st.subheader("🌱 Awareness Level by Gender")
if "Gender" in df.columns and "Awareness_Level" in df.columns:
    fig1 = px.bar(
        df, x="Gender", color="Awareness_Level",
        title="CSA Awareness Distribution by Gender",
        color_discrete_sequence=px.colors.qualitative.G10,
        barmode="group"
    )
    fig1.update_layout(
        template="plotly_white",
        title_font_size=18,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig1, use_container_width=True)

# --- SECTION 2: Education vs CSA Adoption ---
st.subheader("📘 Education Level and CSA Adoption")
if "Education_Level" in df.columns and "Adoption_of_CSA" in df.columns:
    fig2 = px.box(
        df, x="Education_Level", y="Adoption_of_CSA",
        color="Education_Level",
        title="Impact of Education on CSA Adoption",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2.update_layout(template="plotly_white", title_font_size=18, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

# --- SECTION 3: Income vs Awareness ---
st.subheader("💰 Income Level vs CSA Awareness")
if "Income_Level" in df.columns and "Awareness_Level" in df.columns:
    fig3 = px.histogram(
        df, x="Income_Level", color="Awareness_Level",
        barmode="group",
        title="CSA Awareness by Income Category",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig3.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

# --- SECTION 4: Regional Participation ---
st.subheader("📍 Regional Participation in CSA")
if "Region" in df.columns and "Adoption_of_CSA" in df.columns:
    region_summary = df.groupby("Region")["Adoption_of_CSA"].mean().reset_index()
    fig4 = px.bar(
        region_summary, x="Region", y="Adoption_of_CSA",
        title="Average CSA Adoption Rate by Region",
        color="Region",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    fig4.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig4, use_container_width=True)

# --- FOOTER ---
st.markdown("""
---
<p style='text-align:center; color:gray;'>
🌾 <b>Developed with ❤️ using Streamlit + Plotly</b><br>
Empowering sustainable agriculture through data insight
</p>
""", unsafe_allow_html=True)
