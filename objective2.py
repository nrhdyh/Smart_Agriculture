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

# Define a placeholder encoding mapping based on the columns used in your code.
# The numeric indices (0, 1, 2, ...) in the data are mapped to these string labels.
encoding_mapping = {
    'Level of education': ['No formal education', 'Primary school', 'Secondary school', 'College/University', 'Vocational'],
    'Water harvesting': ['No Adoption', 'Adopted'],
    'Agroforestry': ['None', 'Low', 'Medium', 'High'],
    'Marital status': ['Single', 'Married', 'Divorced', 'Widowed'],
    'Perception of climate change': ['Low Perception', 'Medium Perception', 'High Perception'],
    'If household has a land use plan': ['No Plan', 'Has Plan']
}

# --- Data Loading ---
@st.cache_data
def load_data(url):
    """Loads and caches the data from the provided URL."""
    try:
        data = pd.read_csv(url)
        # Rename the column to handle the Byte Order Mark (BOM) issue ('ï»¿')
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
    # --- Objective 2 Visualizations ---
    st.header("🔬 Objective 2: Climate-Smart Agriculture Insights")
    st.markdown("""
    The objective is to analyze water harvesting adoption by education level, the relationship between land size and agroforestry, 
    perceptions of climate change by marital status, and the proportion of households with a land use plan.
    """)

    st.subheader("Raw Data Sample")
    st.dataframe(freehold_df.head())


    # 1. Relationship between Level of Education and Water Harvesting Adoption (Grouped Bar Chart)
    st.subheader("1. Water Harvesting Adoption by Level of Education")
    
    education_labels = encoding_mapping['Level of education']
    water_harvesting_labels = encoding_mapping['Water harvesting']
    
    fig_edu_water = px.histogram(
        freehold_df, 
        x='Level of education', 
        color='Water harvesting',
        title='Water Harvesting Adoption by Level of Education',
        template=PLOTLY_TEMPLATE, 
        barmode='group'
    )
    
    # Apply custom labels for the x-axis and legend
    fig_edu_water.update_layout(
        xaxis={'tickvals': list(range(len(education_labels))), 'ticktext': education_labels},
        legend=dict(title='Water Harvesting', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Map legend numbers to text labels (assuming 'Water harvesting' is numeric 0/1)
    fig_edu_water.for_each_trace(lambda t: t.update(name = water_harvesting_labels[int(t.name)]) if t.name.isdigit() and int(t.name) < len(water_harvesting_labels) else t)

    st.plotly_chart(fig_edu_water, use_container_width=True)
    st.markdown("""
    The bar chart shows the relationship between education level and the adoption of water harvesting. 
    The chart can be seen as that people with no formal education have the highest number of adopters and followed by those with primary education. 
    In contrast, the number of adopters decreases as the level of education increases with the lowest adoption seen among individuals with secondary and college or university education. 
    This suggests that people with lower levels of education are more likely to adopt water harvesting practices because they rely more on traditional or self-sufficient methods for water use.
    """)

    st.markdown("---")

   # 2. Relationship between Land Size and Agroforestry Levels (Box Plot)
st.subheader("2. Land Size vs. Agroforestry Levels")

agroforestry_labels = encoding_mapping['Agroforestry']

# Create a box plot instead of a scatter plot
fig_land_agro = px.box(
    freehold_df,
    x='Agroforestry',
    y='Land size',
    title='Land Size vs. Agroforestry Levels',
    template=PLOTLY_TEMPLATE,
    points='all',  # Shows individual data points overlaid on the box
)

# Apply custom labels for the x-axis (Agroforestry level)
fig_land_agro.update_layout(
    xaxis={'tickvals': list(range(len(agroforestry_labels))), 'ticktext': agroforestry_labels},
    yaxis_title="Land Size",
    xaxis_title="Agroforestry Level"
)

st.plotly_chart(fig_land_agro, use_container_width=True)

st.markdown("""
* **Explanation:** This box plot shows the distribution of **land sizes** across different **agroforestry levels**.
* **Interpretation:** Each box represents the spread of land sizes within a specific agroforestry level, with points showing individual households.
* **Key Insight:** Look for differences in median and spread to see if households with larger lands tend to practice more agroforestry.
""")

st.markdown("---")


    # 3. Distribution of Perception of Climate Change by Marital Status (Grouped Bar Chart)
    st.subheader("3. Perception of Climate Change by Marital Status")
    
    marital_labels = encoding_mapping['Marital status']
    perception_labels = encoding_mapping['Perception of climate change']
    
    fig_marital_perception = px.histogram(
        freehold_df, 
        x='Marital status', 
        color='Perception of climate change',
        title='Perception of Climate Change by Marital Status',
        template=PLOTLY_TEMPLATE, 
        barmode='group'
    )
    
    # Apply custom labels for the x-axis and legend
    fig_marital_perception.update_layout(
        xaxis={'tickvals': list(range(len(marital_labels))), 'ticktext': marital_labels},
        legend=dict(title='Perception', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Map legend numbers to text labels (assuming 'Perception of climate change' is numeric 0/1/2)
    fig_marital_perception.for_each_trace(lambda t: t.update(name = perception_labels[int(t.name)]) if t.name.isdigit() and int(t.name) < len(perception_labels) else t)

    st.plotly_chart(fig_marital_perception, use_container_width=True)
    st.markdown("""
    The bar chart shows how the individuals perception of climate change differs based on their marital status. 
    It can be seen that single individuals make up most of the respondents and have both high and low levels of perception about climate change while only a few have a medium level of perception. 
    In contrast, married individuals are fewer in number and generally show lower levels of perception, with very few having a high perception.
    Overall, this suggests that single individuals tend to be more aware or concerned about climate change compared to married individuals.
    """)

    st.markdown("---")

    # 4. Proportion of Households with Land Use Plan (Pie Chart)
    st.subheader("4. Proportion of Households with a Land Use Plan")
    
    land_use_plan_labels = encoding_mapping['If household has a land use plan']
    land_use_plan_counts = freehold_df['If household has a land use plan'].value_counts().reset_index()
    land_use_plan_counts.columns = ['If household has a land use plan', 'Count']
    
    fig_land_use_plan = px.pie(
        land_use_plan_counts, 
        values='Count', 
        names='If household has a land use plan',
        title='Proportion of Households with a Land Use Plan', 
        template=PLOTLY_TEMPLATE
    )
    
    fig_land_use_plan.update_traces(textposition='inside', textinfo='percent+label')
    
    # Map the pie chart slice names (assuming numeric encoding 0/1) to the text labels
    fig_land_use_plan.update_traces(
        # Use the labels defined in the mapping
        labels=[land_use_plan_labels[int(name)] for name in fig_land_use_plan.data[0].labels]
    )

    st.plotly_chart(fig_land_use_plan, use_container_width=True)
    st.markdown("""
    This pie chart shows the percentage of households that have a land use plan and those that has not. 
    The majority of households of **77.8%**, do not have any land use plan, while only **22.2%** have one. 
    This means that most households are not planning or organizing how their land is used. 
    The chart makes it clear that only a small portion of households are taking steps to manage their land properly. 
    This could mean that many people may not be aware of the benefits of land planning or may not have the resources to do it.
    Overall, the chart highlights a need for more support or awareness to help households create land use plans.
    """)
    
    st.markdown("---")
