import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(
    page_title="Freehold Household Head Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Constants ---
DATA_URL = 'https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/freehold_data_on_Climate_Smart_Agriculture.csv'
PLOTLY_TEMPLATE = 'plotly_dark'

encoding_mapping = {
    'Level of education': ['No formal education', 'Primary school', 'Secondary school', 'College/University', 'Vocational'],
    'ï»¿Gender of household head': ['Male', 'Female']
}

# --- Data Loading ---
@st.cache_data
def load_data(url):
    """Loads and caches the data from the provided URL."""
    try:
        data = pd.read_csv(url)
        # Fix encoding issue in the gender column name
        data = data.rename(columns={'ï»¿Gender of household head': 'Gender of household head'})
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

freehold_df = load_data(DATA_URL)

# --- Streamlit App Layout ---
st.title("📊 Freehold Household Head Data Analysis")

if freehold_df.empty:
    st.warning("Could not load data. Please check the URL and file format.")
else:
    st.markdown("""
    The objective is to analyze the distribution of age and education levels among freehold household heads, 
    examine the relationship between age and land size, 
    and explore the distribution of household size by gender of the household head.
    """)
    
    st.subheader("Raw Data Sample")
    st.dataframe(freehold_df.head())
    
    st.markdown("---")

    # --- Objective 1 Visualizations ---
    st.header("🎯 Objective 1: Key Data Distributions and Relationships")

    # 1. Distribution of Age (Histogram)
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
    The histogram for **“Distribution of Age among Freehold Household Heads”** shows how the ages of people who own freehold land are spread out. 
    Most household heads are between **45 and 60 years old**, with the highest number around **50 years old**. 
    The **mean** and **median** are both around **50 years**, with **Q1 ≈ 40 years** and **Q3 ≈ 60 years**, giving an **IQR ≈ 20 years**. 
    This suggests that middle-aged people are the main holders of freehold land.
    """)
    st.markdown("---")

    # 2. Distribution of Level of Education (Bar Chart)
    st.subheader("2. Distribution of Level of Education among Freehold Household Heads")

    education_labels = encoding_mapping.get('Level of education', [])

    # --- Calculate percentage distribution ---
    education_counts = freehold_df['Level of education'].value_counts()
    education_percent = (education_counts / education_counts.sum()) * 100

    # Convert to DataFrame
    education_df = pd.DataFrame({
        'Level of education': education_percent.index,
        'Percentage': education_percent.values
    })

    # --- Replace numeric codes with labels (if mapping exists) ---
    if education_labels:
        try:
            education_df['Level of education'] = education_df['Level of education'].astype(int)
            education_df['Level of education'] = education_df['Level of education'].apply(
                lambda x: education_labels[x] if x < len(education_labels) else str(x)
            )
        except:
            pass

    # --- Create percentage bar chart ---
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
    * **Explanation:** This bar chart shows the **percentage** of freehold household heads at each education level.
    * **Key Insight:** Observe which education level has the highest proportion among freehold household heads.
    """)
    st.markdown("-
