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
PLOTLY_TEMPLATE = 'plotly_dark'

# Define encoding mapping
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
    try:
        data = pd.read_csv(url)
        data = data.rename(columns={'ï»¿Gender of household head': 'Gender of household head'})
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

freehold_df = load_data(DATA_URL)

# --- Streamlit Layout ---
st.title("📊 Freehold Household Head Data Analysis")

if freehold_df.empty:
    st.warning("Could not load data. Please check the URL and file format.")
else:
    # --- Objective 2 ---
    st.header("🔬 Objective 2: Climate-Smart Agriculture Insights")
    st.markdown("""
    The objective is to analyze water harvesting adoption by education level, the relationship between land size and agroforestry, 
    perceptions of climate change by marital status, and the proportion of households with a land use plan.
    """)

    st.subheader("Raw Data Sample")
    st.dataframe(freehold_df.head())
    st.markdown("---")

    # 1. Water Harvesting Adoption by Level of Education
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

    fig_edu_water.update_layout(
        xaxis={'tickvals': list(range(len(education_labels))), 'ticktext': education_labels},
        legend=dict(title='Water Harvesting', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_edu_water.for_each_trace(
        lambda t: t.update(name=water_harvesting_labels[int(t.name)]) if t.name.isdigit() and int(t.name) < len(water_harvesting_labels) else t
    )

    st.plotly_chart(fig_edu_water, use_container_width=True)
    st.markdown("""
    People with lower education levels tend to adopt water harvesting more, likely due to reliance on traditional or self-sufficient practices.
    """)
    st.markdown("---")

    # 2. Land Size vs. Agroforestry Levels
    st.subheader("2. Land Size vs. Agroforestry Levels")

    agroforestry_labels = encoding_mapping['Agroforestry']

    fig_land_agro = px.box(
        freehold_df,
        x='Agroforestry',
        y='Land size',
        title='Land Size vs. Agroforestry Levels',
        template=PLOTLY_TEMPLATE,
        points='all'
    )

    fig_land_agro.update_layout(
        xaxis={'tickvals': list(range(len(agroforestry_labels))), 'ticktext': agroforestry_labels},
        yaxis_title="Land Size",
        xaxis_title="Agroforestry Level"
    )

    st.plotly_chart(fig_land_agro, use_container_width=True)
    st.markdown("""
    Larger landholders often engage more in agroforestry, showing a link between land size and sustainable practice levels.
    """)
    st.markdown("---")

    # 3. Perception of Climate Change by Marital Status
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

    fig_marital_perception.update_layout(
        xaxis={'tickvals': list(range(len(marital_labels))), 'ticktext': marital_labels},
        legend=dict(title='Perception', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_marital_perception.for_each_trace(
        lambda t: t.update(name=perception_labels[int(t.name)]) if t.name.isdigit() and int(t.name) < len(perception_labels) else t
    )

    st.plotly_chart(fig_marital_perception, use_container_width=True)
    st.markdown("""
    Single individuals tend to show higher awareness of climate change compared to married ones.
    """)
    st.markdown("---")

    # 4. Proportion of Households with a Land Use Plan
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

    st.plotly_chart(fig_land_use_plan, use_container_width=True)
    st.markdown("""
    Most households (around 78%) lack a land use plan, showing low adoption of structured land management.
    """)
    st.markdown("---")
