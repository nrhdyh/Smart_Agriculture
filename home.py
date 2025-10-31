import streamlit as st
import pandas as pd
# Import necessary utilities to load data and access mappings
from utils import load_data, DATA_URL, ENCODING_MAPPING 

# Load the data
freehold_df = load_data(DATA_URL)

st.title("🌿 Climate Smart Agriculture Dashboard")

st.markdown("""
Welcome to the **Climate Smart Agriculture (CSA)** data visualization platform. 
This dashboard analyzes insights from **married household heads** on various factors influencing CSA adoption.

### 📊 Pages Overview
- **Objective 1:** Explore education, demographics, and training participation.
- **Objective 2:** Analyze land ownership, land size, and economic patterns.
- **Objective 3:** Understand adoption of CSA practices and climate change perceptions.

Use the top navigation menu to explore each section.
""")

st.image("https://images.unsplash.com/photo-1599498771460-26c1b2e2f743?auto=format&fit=crop&w=1200&q=60", caption="Sustainable Agriculture")

st.markdown("---")

if not freehold_df.empty:
    st.subheader("Key Summary Statistics")

    # --- Metric Calculations (assuming default encoding where 1 is "Adopted" or "Yes" and 2 is "High") ---
    
    # 1. Water Harvesting Adoption Rate (Assuming 'Adopted' is encoded as 1)
    # Safely get the count for 'Adopted' (1) and calculate percentage
    water_adoption = (freehold_df['Water harvesting'].value_counts(normalize=True).get(1, 0) * 100)
    
    # 2. Average Land Size
    avg_land_size = freehold_df['Land size'].mean()
    
    # 3. Average Household Income
    avg_income = freehold_df['Income '].mean()
    
    # 4. High Climate Perception Rate (Assuming 'High Perception' is encoded as 2)
    # Safely get the count for 'High Perception' (2) and calculate percentage
    high_perception = (freehold_df['Perception of climate change'].value_counts(normalize=True).get(2, 0) * 100)


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="CSA Adoption (Water Harvesting)", 
        value=f"{water_adoption:.1f}%", 
        help="Percentage of households that have adopted water harvesting practices.", 
        delta_color="normal",
        delta="Target Practice"
    )
    col2.metric(
        label="Average Farm Size", 
        value=f"{avg_land_size:.2f}", 
        help="Mean size of agricultural land (unit assumed to be in Hectares).", 
        delta_color="off",
        delta="Hectares"
    )
    col3.metric(
        label="Average Household Income", 
        value=f"Avg {avg_income:,.0f}", 
        help="Mean monthly or annual household income (unit depends on original data scale).", 
        delta_color="off",
        delta="Income"
    )
    col4.metric(
        label="High Climate Change Perception", 
        value=f"{high_perception:.1f}%", 
        help="Percentage of households reporting a high perception/awareness of climate change.", 
        delta_color="normal",
        delta="Awareness"
    )

st.markdown("---")
