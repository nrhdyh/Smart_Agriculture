import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🎓 Awareness and Education Impact")
df = pd.read_csv("https://github.com/nrhdyh/Smart_Agriculture/blob/main/married_data_on_Climate_Smart_Agriculture.csv")

# Objective
st.subheader("Objective Statement")
st.write("To examine how education level influences awareness of climate-smart agriculture among married farmers.")

# Summary
st.subheader("Summary")
st.info("This visualization investigates how farmers’ education levels influence their awareness of Climate Smart Agriculture (CSA). "
        "Understanding this relationship helps identify how education shapes knowledge and adoption of sustainable practices.")

# --- Visualization 1: Bar Chart ---
st.markdown("### 1️⃣ Average Awareness by Education Level")
edu_awareness = df.groupby("Education")["Awareness_Level"].mean().reset_index()
fig1 = px.bar(
    edu_awareness, x="Education", y="Awareness_Level",
    color="Awareness_Level", color_continuous_scale="Greens",
    title="Average Awareness Level by Education"
)
st.plotly_chart(fig1, use_container_width=True)

# --- Visualization 2: Scatter Plot ---
st.markdown("### 2️⃣ Education vs Awareness by Gender")
fig2 = px.scatter(
    df, x="Education", y="Awareness_Level", color="Gender",
    size="Awareness_Level", title="Education vs Awareness by Gender",
    color_discrete_sequence=px.colors.qualitative.Safe
)
st.plotly_chart(fig2, use_container_width=True)

# --- Visualization 3: Correlation Matrix (Plotly Heatmap) ---
st.markdown("### 3️⃣ Correlation Heatmap (Education, Awareness, Adoption)")
corr = df[["Education", "Awareness_Level", "Adoption_Rate"]].corr()
fig3 = go.Figure(data=go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale="Greens",
    zmin=-1, zmax=1,
))
fig3.update_layout(title="Correlation Heatmap", xaxis_nticks=36)
st.plotly_chart(fig3, use_container_width=True)

# --- Interpretation ---
st.subheader("Interpretation / Discussion")
st.write("The bar and scatter plots reveal that higher education levels are generally linked with stronger awareness of CSA. "
         "The heatmap shows a positive correlation between education and awareness, suggesting that education enhances understanding of sustainable agriculture.")
