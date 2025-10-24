import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Land & Economic Factors", layout="wide")

url = "https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/married_data_on_Climate_Smart_Agriculture.csv"
df = pd.read_csv(url)

st.title("🌾 Land & Economic Factors")

st.markdown("""
**Objective:**  
To explore how land tenure, land size, and land-use planning affect agricultural productivity and sustainability.
""")

# Land tenure
tenure_counts = df["Land tenure"].value_counts().reset_index()
tenure_counts.columns = ["Land tenure", "Count"]
fig1 = px.bar(tenure_counts, x="Land tenure", y="Count",
              color="Land tenure", title="Distribution of Land Tenure",
              color_discrete_sequence=px.colors.qualitative.Prism)
st.plotly_chart(fig1, use_container_width=True)

# Land size distribution
fig2 = px.histogram(df, x="Land size", nbins=20,
                    title="Distribution of Land Size",
                    color_discrete_sequence=["#AED581"])
st.plotly_chart(fig2, use_container_width=True)

# Land size by tenure
fig3 = px.box(df, x="Land tenure", y="Land size",
              title="Land Size Distribution by Tenure",
              color="Land tenure", color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig3, use_container_width=True)

# Land use plan
plan_counts = df["If household has a land use plan"].value_counts().reset_index()
plan_counts.columns = ["Has Land Use Plan", "Count"]
fig4 = px.bar(plan_counts, x="Has Land Use Plan", y="Count",
              color="Has Land Use Plan", title="Households with Land Use Plan",
              color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig4, use_container_width=True)
