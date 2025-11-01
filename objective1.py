import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(
    page_title="Freehold Household Head Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set the URL for the raw CSV data on GitHub
DATA_URL = 'https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/freehold_data_on_Climate_Smart_Agriculture.csv'
PLOTLY_TEMPLATE = 'plotly_dark'  # Dark theme

# Define encoding mapping
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
        # Fix encoding issue for gender column
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

    # ------------------------------------------------
    # 1. Distribution of Age (Histogram)
    # ------------------------------------------------
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
    The histogram shows how the ages of freehold household heads are spread out. 
    Most are between **45 and 60 years old**, meaning middle-aged individuals are the main landowners.
    """)

    st.markdown("---")

    # ------------------------------------------------
    # 2. Distribution of Level of Education (Bar Chart - Percentage)
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

    # Replace numeric codes with readable labels
    if education_labels:
        try:
            education_df['Level of education'] = education_df['Level of education'].astype(int)
            education_df['Level of education'] = education_df['Level of education'].apply(
                lambda x: education_labels[x] if x < len(education_labels) else str(x)
            )
        except:
            pass

    # Create percentage bar chart
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

    **Key Insight:**  
    It highlights the most common education level among freehold household heads.
    """)

    st.markdown("---")

    # ------------------------------------------------
    # 3. Relationship between Age and Land Size (Scatter Plot)
    # ------------------------------------------------
    st.subheader("3. Age vs. Land Size for Freehold Household Heads")

    fig_age_land = px.scatter(
        freehold_df,
        x='Age',
        y='Land size',
        title='Age vs. Land Size for Freehold Household Heads',
        template=PLOTLY_TEMPLATE
    )
    st.plotly_chart(fig_age_land, use_container_width=True)

    st.markdown("""
    **Explanation:**  
    This scatter plot visualizes the relationship between the **age** of household heads and the **size of their land**.  

    **Key Insight:**  
    Look for any trend or pattern that may suggest older household heads tend to own larger lands.
    """)

    st.markdown("---")

    # ------------------------------------------------
    # 4. Distribution of Household Size by Gender (Grouped Bar)
    # ------------------------------------------------
    st.subheader("4. Distribution of Household Size by Gender of Household Head")

    gender_labels = encoding_mapping.get('ï»¿Gender of household head', ['Male', 'Female'])
    gender_column = 'Gender of household head'

    fig_household_gender = px.histogram(
        freehold_df,
        x='Household size',
        color=gender_column,
        title='Distribution of Household Size by Gender of Household Head',
        template=PLOTLY_TEMPLATE,
        barmode='group'
    )

    fig_household_gender.update_layout(
        legend=dict(
            title='Gender',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Fix gender labels if numeric
    try:
        if pd.api.types.is_numeric_dtype(freehold_df[gender_column]):
            fig_household_gender.for_each_trace(lambda t: t.update(name=gender_labels[int(t.name)]))
    except:
        pass

    st.plotly_chart(fig_household_gender, use_container_width=True)

    st.markdown("""
    **Explanation:**  
    This grouped bar chart shows household sizes based on gender of the household head.  

    **Key Insight:**  
    Compare typical household sizes between male- and female-headed households.
    """)

    st.markdown("---")
    st.info("✅ End of Visualization Dashboard.")
