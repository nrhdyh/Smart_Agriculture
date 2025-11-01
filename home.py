import streamlit as st
import pandas as pd
import plotly.express as px

# ===========================
# LOAD DATA DIRECTLY FROM GITHUB
# ===========================
DATA_URL = "https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/freehold_data_on_Climate_Smart_Agriculture.csv"

@st.cache_data
def load_data(path):
    """Load dataset safely with error handling"""
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

# Load the data
freehold_df = load_data(DATA_URL)

# ===========================
# STREAMLIT UI SETUP
# ===========================
st.set_page_config(page_title="Climate Smart Agriculture Dashboard", page_icon="🌿", layout="wide")

st.title("🌿 Climate Smart Agriculture Dashboard")

st.markdown("""
### 📊 Dashboard Overview
- **Objective 1:** Freehold Household Demographics  
- **Objective 2:** Climate-Smart Agriculture Insights
- **Objective 3:** Deeper Correlations and Status Quo
""")

st.image(
    "https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/main/sustainable-agriculture.jpg"
)

st.markdown("---")

# ===========================
# SUMMARY STATISTICS
# ===========================
if not freehold_df.empty:
    st.subheader("🌱 Key Summary Statistics")

    # --- Helper Functions ---
    def safe_mean(df, col):
        return df[col].mean() if col in df.columns else 0

    def safe_percentage(df, col, value):
        if col in df.columns:
            return df[col].value_counts(normalize=True).get(value, 0) * 100
        return 0

    # --- Metrics ---
    water_adoption = safe_percentage(freehold_df, 'Water harvesting', 1)
    avg_land_size = safe_mean(freehold_df, 'Land size')
    training_rate = safe_percentage(freehold_df, 'Access to training', 1)
    high_perception = safe_percentage(freehold_df, 'Perception of climate change', 2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💧 CSA Adoption", f"{water_adoption:.1f}%", "Water Harvesting")
    col2.metric("🌾 Avg Land Size", f"{avg_land_size:.2f}", "Hectares")
    col3.metric("🎓 Training Rate", f"{training_rate:.1f}%", "Participation")
    col4.metric("🌍 High Awareness", f"{high_perception:.1f}%", "Climate Change")

    st.markdown("---")

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
st.header("🔬 Objective 1: Freehold Household Demographics")

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
   The histogram for **“Distribution of Age among Freehold Household Heads”** shows how the ages of people who own freehold land are spread out.
   Most household heads are between age **45 and 60 years old** with the highest number around age **50 years old**. 
   This means that freehold land is mostly owned by middle-aged individuals. The average (mean) and middle (median) ages are both around the age of **50 years**, showing that most data is centered in this range.
   The **first quartile (Q1)** is about **40 years** and the **third quartile (Q3)** is about **60 years** also giving an **interquartile range (IQR)** of around **20 years**. 
   This tells that half of the household heads are between 40 and 60 years old. The chart also shows a few older owners above 70 years, but very few younger ones below 35. Overall, the data suggests that middle-aged people are the main holders of freehold land.
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
    The chart shows that most freehold household heads are from low levels of education. 
    Over half (55.1%) have no formal education while about 1/3 (32.3%) completed only the primary school. 
    A smaller group (7.3%) reached secondary school and just minor (5.4%) have college or university education. 
    This indicates that the majority of household heads have limited educational attainment with very few achieving higher education levels.
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
   The scatter plot shows the relationship between the age of freehold household heads and the size of their owned land. 
   Overall, there is no clear correlation between age and land size. 
   Most household heads, regardless of age own relatively small plots of land, typically below 2 units in size. 
   A few outliers can be seen where some individuals at mostly in their 30s to 60s that own larger plots but these cases are rare. 
   This suggests that land ownership size does not strongly depend on age among freehold household heads.
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
   The chart shows the distribution of household sizes by the gender of household heads and the overall the **male-headed households** are more common across all household sizes compared to female-headed ones. 
   Most households have **4 to 6 members**, with male-headed households peaking around these sizes. 
   Female-headed households are fewer and show a more even spread across smaller and medium household sizes. 
   This suggests that **men are more likely to head larger households** while the **women tend to lead smaller households**.
    """)

    st.markdown("---")

