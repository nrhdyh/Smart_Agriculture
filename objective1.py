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
PLOTLY_TEMPLATE = 'plotly_dark' # Set a blue-ish template

# Define the encoding mapping (based on the original code's implied structure)
# NOTE: You'll need to confirm these exact labels from your full analysis script
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
        # Rename the 'ï»¿Gender of household head' column to a cleaner name for easier use
        # The 'ï»¿' is a common encoding issue (BOM - Byte Order Mark)
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
    This application visualizes key characteristics of freehold household heads, 
    including age distribution, education level, relationship between age and land size, 
    and household size distribution by gender.
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
    * **Explanation:** This histogram shows the frequency distribution of ages among household heads with freehold land tenure. It helps to understand the age profile of this group.
    * **Key Insight:** Observe the most common age range and the overall spread of ages in the data.
    """)
    
    st.markdown("---")

    # 2. Distribution of Level of Education (Bar Chart)
    st.subheader("2. Distribution of Level of Education among Freehold Household Heads")
    education_labels = encoding_mapping.get('Level of education', [])
    
    # Ensure the column is treated as categorical for correct ordering if needed, or rely on Plotly's default count/order
    fig_education = px.bar(
        freehold_df, 
        y='Level of education', 
        title='Distribution of Level of Education among Freehold Household Heads', 
        template=PLOTLY_TEMPLATE
    )
    
    # Apply tick labels if the list is available
    if education_labels:
        # Assuming the education column in the DataFrame uses the numeric encoding 0, 1, 2, ...
        # The original code's approach to tickvals/ticktext is a bit complex for Plotly Express on categorical data.
        # It's often simpler to ensure the column has the correct string labels *before* plotting, 
        # but sticking close to the original concept using numeric labels:
        try:
             # This attempts to reproduce the original logic which assumes the y-axis values are integers
             # and maps them to the descriptive string labels.
             education_levels_numeric = sorted(freehold_df['Level of education'].unique())
             # Filter labels to only those present in the data
             valid_labels = [education_labels[i] for i in education_levels_numeric if i < len(education_labels)]
             
             fig_education.update_layout(
                 yaxis={'tickvals': education_levels_numeric, 
                        'ticktext': valid_labels, 
                        'categoryorder': 'array', 
                        'categoryarray': education_levels_numeric}
             )
        except:
             # Fallback if the data is not numerically encoded as expected
             pass 

    st.plotly_chart(fig_education, use_container_width=True)
    st.markdown("""
    * **Explanation:** This bar chart illustrates the count of freehold household heads at different levels of education. It provides insights into the educational background of this population.
    * **Key Insight:** Identify which educational levels are most prevalent among freehold household heads.
    """)

    st.markdown("---")

    # 3. Relationship between Age and Land Size (Scatter Plot)
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
    * **Explanation:** This scatter plot visualizes the relationship between the age of household heads and the size of their land. It helps to explore if there is any correlation between these two variables.
    * **Key Insight:** Look for any patterns or trends that suggest a relationship between age and land size.
    """)

    st.markdown("---")

    # 4. Distribution of Household Size by Gender of Household Head (Grouped Bar Chart/Histogram)
    st.subheader("4. Distribution of Household Size by Gender of Household Head")
    gender_labels = encoding_mapping.get('ï»¿Gender of household head', ['Male', 'Female'])
    
    # Ensure the column name used here matches the corrected one from load_data
    gender_column = 'Gender of household head'

    fig_household_gender = px.histogram(
        freehold_df, 
        x='Household size', 
        color=gender_column,
        title='Distribution of Household Size by Gender of Household Head',
        template=PLOTLY_TEMPLATE, 
        barmode='group'
    )
    
    # Update legend title and position
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
    
    # Use the labels in the legend if the data uses numeric encoding
    # If the data uses strings 'Male'/'Female', Plotly Express handles it, but if it uses 0/1,
    # we need to map the values for better display. Assuming Plotly Express is smart enough or the data 
    # already contains the descriptive labels after the initial data cleaning/loading.
    try:
        # Check if the column is numeric (e.g., 0 and 1) and map the legend labels
        if pd.api.types.is_numeric_dtype(freehold_df[gender_column]):
            fig_household_gender.for_each_trace(lambda t: t.update(name = gender_labels[int(t.name)]))
    except:
        # Fallback if mapping fails
        pass


    st.plotly_chart(fig_household_gender, use_container_width=True)
    st.markdown("""
    * **Explanation:** This grouped bar chart shows the distribution of household sizes, separated by the gender of the household head. It allows for a comparison of household sizes between male and female-headed households.
    * **Key Insight:** Compare the typical household sizes for male and female-headed households and observe any differences in their distributions.
    """)
    
    st.markdown("---")
    st.info("End of Visualization Dashboard.")

# --- End of Streamlit Script ---
