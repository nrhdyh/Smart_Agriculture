import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Climate-Smart Practices", layout="wide")

url = "https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/married_data_on_Climate_Smart_Agriculture.csv"
df = pd.read_csv(url)

st.title("🌱 Climate-Smart Practices & Perceptions")

st.markdown("""
**Objective:**  
To assess adoption rates of climate-smart agricultural practices and the perceptions of climate change among married households.
""")

# Water harvesting
fig1 = px.bar(df, x="Water harvesting", color="Water harvesting",
              title="Adoption of Water Harvesting Practices",
              color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(fig1, use_container_width=True)

# Agroforestry
fig2 = px.bar(df, x="Agroforestry", color="Agroforestry",
              title="Adoption of Agroforestry Practices",
              color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig2, use_container_width=True)

# Biofertilizers
fig3 = px.bar(df, x="Use of biofertilizers", color="Use of biofertilizers",
              title="Use of Biofertilizers among Married Households",
              color_discrete_sequence=px.colors.qualitative.Safe)
st.plotly_chart(fig3, use_container_width=True)

# Perception of climate change
fig4 = px.bar(df, y="Perception of climate change", color="Perception of climate change",
              title="Perception of Climate Change",
              color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig4, use_container_width=True)

# Community membership
fig5 = px.bar(df, x="Membership to community organization/Group", color="Membership to community organization/Group",
              title="Community Group Membership among Married Households",
              color_discrete_sequence=px.colors.qualitative.Prism)
st.plotly_chart(fig5, use_container_width=True)
