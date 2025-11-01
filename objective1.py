import streamlit as st
import pandas as pd
import plotly.express as px

# ===========================
# Streamlit Page Configuration
# ===========================
st.set_page_config(
    page_title="Objective 1 - Freehold Household Analysis",
    layout="wide"
)

PLOTLY_TEMPLATE = "plotly_white"

# ===========================
# Example: Load Your Dataset
# ===========================
# Replace this with your actual dataset loading
# Example: freehold_df = pd.read_csv("your_dataset.csv")

# Example dummy data for testing
data = {
    'Age': [35, 42, 50, 28, 39, 46, 52, 37, 41, 55, 60, 33, 48, 29, 44],
    'Level of education': [1, 2, 2, 0, 1, 3, 2, 1, 0, 2, 3, 1, 2, 1, 0]
}
freehold_df = pd.DataFrame(data)

# Mapping (replace this with your own)
encoding_mapping = {
    'Level of education': ['No Education', 'Primary', 'Secondary', 'Tertiary']
}

# ===========================
# Objective 1 Visualizations
# ===========================
st.header("🎯 Objective 1: Key Data Distributions and Relationships")

# -----------------------------------
# 1. Distribution of Age (Histogram)
# -----------------------------------
st.subheader("1. Distribution of Age among Freehold Household Heads")

fig_age = px.histogram(
    freehold_df,
    x='Age',
    title='Distribution of Age among Freehold Household Heads',
    template=PLOTLY_TEMPLATE
)

fig_age.update_layout(bargap=0.2)
st.plotly_chart(fig_age, use_container_width=True)

st.markdown("""
**Explanation:**  
This histogram shows the age distribution of freehold household heads. It helps visualize which age groups are most common in the dataset.

**Key Insight:**  
You can observe the most frequent age ranges and overall spread. The mean and quartiles (Q1–Q3) can be used to understand the central tendency and variation within this group.
""")

st.markdown("---")

# ------------------------------------------------
# 2. Distribution of Level of Education (Bar Chart)
# ------------------------------------------------
st.subheader("2. Distribution of Level of Education among Freehold Household Heads")

education_labels = encoding_mapping.get('Level of education', [])

# Calculate percentages
education_counts = freehold_df['Level of education'].value_counts().sort_index()
education_percent = (education_counts / education_counts.sum()) * 100

education_df = pd.DataFrame({
    'Level of education': education_percent.index,
    'Percentage': education_percent.values
})

# Replace numeric codes with labels (if available)
if education_labels:
    try:
        education_df['Level of education'] = education_df['Level of education'].astype(int)
        education_df['Level of education'] = education_df['Level of education'].apply(
            lambda x: education_labels[x] if x < len(education_labels) else str(x)
        )
    except:
        pass

# Create bar chart (percentage)
fig_education = px.bar(
    education_df,
    x='Percentage',
    y='Level of education',
    orientation='h',
    title='Distribution of Level of Education among Freehold Household Heads (Percentage)',
    labels={'Percentage': 'Percentage (%)', 'Level of education': 'Education Level'},
    text=education_df['Percentage'].round(1).astype(str) + '%',
    template=PLOTLY_TEMPLATE
)

fig_education.update_traces(textposition='outside')
st.plotly_chart(fig_education, use_container_width=True)

st.markdown("""
**Explanation:**  
This bar chart shows the **percentage** of freehold household heads at each level of education.  
It helps in identifying the educational background distribution within the population.

**Key Insight:**  
The chart highlights which education levels are most common among freehold household heads, showing the share of each group as a percentage of the total.
""")

st.markdown("---")

