import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("https://github.com/nrhdyh/Smart_Agriculture/blob/main/married_data_on_Climate_Smart_Agriculture.csv")

df = load_data()

st.title("📘 Objective 1: Awareness & Education Impact")
st.markdown("""
**Objective:** To examine how education level influences awareness and adoption of CSA practices among married individuals.
""")

st.info("Higher education is linked with increased awareness and adoption of CSA techniques. These visualizations show patterns between education, awareness, and adoption.")

col1, col2, col3 = st.columns(3)

with col1:
    fig = px.histogram(df, x="Education_Level", color="Awareness_Level",
                       title="Awareness by Education Level",
                       color_discrete_sequence=px.colors.sequential.Greens)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(df, x="Education_Level", y="Adoption_of_CSA",
                     color="Awareness_Level", title="Adoption vs Education",
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = px.density_heatmap(df, x="Awareness_Level", y="Adoption_of_CSA",
                             title="Heatmap: Awareness vs Adoption",
                             color_continuous_scale="Greens")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("**Interpretation:** Farmers with higher education tend to have greater CSA awareness and adoption, showing education’s critical role in sustainable practices.")
