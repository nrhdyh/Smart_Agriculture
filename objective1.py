import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Education & Demographics", layout="wide")

# Load dataset
url = "https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/married_data_on_Climate_Smart_Agriculture.csv"
df = pd.read_csv(url)

st.title("📘 Education & Demographics of Married Households")

st.markdown("""
This page explores demographic and education-related insights among married household heads 
participating in Climate Smart Agriculture (CSA) programs.
""")

# --- Visualization 1: Level of education distribution
if "Level of education" in df.columns:
    edu_counts = df["Level of education"].value_counts().reset_index()
    edu_counts.columns = ["Level of education", "Count"]
    fig1 = px.bar(
        edu_counts,
        x="Level of education",
        y="Count",
        title="Distribution of Level of Education among Married Household Heads",
        color="Level of education",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig1.update_layout(xaxis_title="Level of Education", yaxis_title="Count")
    st.plotly_chart(fig1, use_container_width=True)

# --- Visualization 2: Age distribution
if "Age" in df.columns:
    fig2 = px.histogram(
        df,
        x="Age",
        nbins=20,
        title="Distribution of Age among Married Household Heads",
        color_discrete_sequence=["skyblue"]
    )
    fig2.update_layout(xaxis_title="Age", yaxis_title="Frequency")
    st.plotly_chart(fig2, use_container_width=True)

# --- Visualization 3: Access to training
if "Access to training" in df.columns:
    train_counts = df["Access to training"].value_counts().reset_index()
    train_counts.columns = ["Access to training", "Count"]
    fig3 = px.bar(
        train_counts,
        x="Access to training",
        y="Count",
        title="Access to Training among Married Households",
        color="Access to training",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- Visualization 4: Age distribution by education level
if "Level of education" in df.columns and "Age" in df.columns:
    fig4 = px.box(
        df,
        x="Level of education",
        y="Age",
        title="Age Distribution by Level of Education",
        color="Level of education",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig4.update_layout(xaxis_title="Level of Education", yaxis_title="Age")
    st.plotly_chart(fig4, use_container_width=True)
