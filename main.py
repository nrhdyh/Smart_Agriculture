import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Climate Smart Agriculture", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("married_data_on_Climate_Smart_Agriculture.csv")

df = load_data()

st.sidebar.success("Select a page to explore 👈")

st.title("🌿 Climate-Smart Agriculture Dashboard")
st.markdown("""
### 🎯 Objective
To analyze how married individuals engage in climate-smart agriculture (CSA) practices 
and understand the factors influencing adoption and awareness.
""")

st.info("This dashboard presents insights about awareness, income, education, and regional participation in CSA programs using interactive visualizations.")

col1, col2 = st.columns(2)

with col1:
    if "Gender" in df.columns and "Awareness_Level" in df.columns:
        fig = px.bar(df, x="Gender", color="Awareness_Level",
                     title="Awareness Level by Gender",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if "Education_Level" in df.columns and "Adoption_of_CSA" in df.columns:
        fig = px.box(df, x="Education_Level", y="Adoption_of_CSA",
                     title="CSA Adoption by Education Level",
                     color_discrete_sequence=["#81C784"])
        st.plotly_chart(fig, use_container_width=True)
