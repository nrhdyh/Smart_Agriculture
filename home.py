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

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3593/3593763.png", width=100)
st.sidebar.title("CSA Dashboard")
st.sidebar.markdown("### 🌾 Explore Insights")
st.sidebar.markdown("- Overview")
st.sidebar.markdown("- Demographics")
st.sidebar.markdown("- Awareness & Adoption")
st.sidebar.markdown("- Regional Trends")

st.sidebar.info("Select a section using sidebar navigation 👈")

# --- HEADER ---
st.title("🌿 Climate-Smart Agriculture Dashboard")
st.markdown("""
This dashboard explores **how married individuals** participate in **Climate-Smart Agriculture (CSA)** practices, 
analyzing awareness, education, income, and regional factors that influence adoption.
""")

# --- STYLING HELPERS ---
def card_style():
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 30px !important;
            color: #2E7D32;
        }
        div[data-testid="stHorizontalBlock"] {
            background: #f5fff7;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }
        h1, h2, h3 {
            color: #2E7D32;
        }
        </style>
    """, unsafe_allow_html=True)

card_style()

# --- SECTION 1: Awareness & Gender ---
st.subheader("🌱 Awareness Level by Gender")
col1, col2 = st.columns(2)

with col1:
    if "Gender" in df.columns and "Awareness_Level" in df.columns:
        fig1 = px.bar(
            df, x="Gender", color="Awareness_Level",
            title="CSA Awareness Level by Gender",
            color_discrete_sequence=px.colors.qualitative.G10,
            barmode="group"
        )
        fig1.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", title_font_size=18)
        st.plotly_chart(fig1, use_container_width=True)

# --- SECTION 2: Education & Adoption ---
with col2:
    if "Education_Level" in df.columns and "Adoption_of_CSA" in df.columns:
        fig2 = px.box(
            df, x="Education_Level", y="Adoption_of_CSA",
            color="Education_Level",
            title="CSA Adoption by Education Level",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig2.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", title_font_size=18)
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

# --- SECTION 4: Regional Distribution ---
st.subheader("📍 Regional Participation in CSA")
if "Region" in df.columns and "Adoption_of_CSA" in df.columns:
    region_summary = df.groupby("Region")["Adoption_of_CSA"].mean().reset_index()
    fig4 = px.bar(
        region_summary, x="Region", y="Adoption_of_CSA",
        title="Average CSA Adoption by Region",
        color="Region",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    fig4.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig4, use_container_width=True)

# --- FOOTER ---
st.markdown("""
<hr style="border: 1px solid #ccc;">
<p style='text-align:center; color:gray'>
🌾 Developed with ❤️ using Streamlit & Plotly | ESG-aligned visualization of CSA data
</p>
""", unsafe_allow_html=True)
