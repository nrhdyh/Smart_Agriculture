import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np # Needed for correlation calculation

# --- Configuration ---
st.set_page_config(
    page_title="Freehold Household Head Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set the URL for the raw CSV data on GitHub
DATA_URL = 'https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/freehold_data_on_Climate_Smart_Agriculture.csv'
PLOTLY_TEMPLATE = 'plotly_dark' # Set a blue-ish template

# Define a comprehensive encoding mapping based on the columns used in all objectives
encoding_mapping = {
    'Level of education': ['No formal education', 'Primary school', 'Secondary school', 'College/University', 'Vocational'],
    'Water harvesting': ['No Adoption', 'Adopted'],
    'Agroforestry': ['None', 'Low', 'Medium', 'High'],
    'Marital status': ['Single', 'Married', 'Divorced', 'Widowed'],
    'Perception of climate change': ['Low Perception', 'Medium Perception', 'High Perception'],
    'If household has a land use plan': ['No Plan', 'Has Plan'],
    'Membership to community organization/Group': ['No Membership', 'Member'],
    'Access to training': ['No Access', 'Has Access'],
    'Trend in soil condition': ['Deteriorated', 'Not Changed', 'Improved']
    # 'Gender of household head' is also used but is cleaned during loading
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

# --- Helper Function for Plotly Label Mapping ---
def map_numeric_axis(fig, axis_key, column_name):
    """Applies custom tick labels to a Plotly figure axis based on encoding_mapping."""
    if column_name in encoding_mapping:
        labels = encoding_mapping[column_name]
        try:
            # Get the unique numeric values present in the column
            unique_vals = sorted([v for v in freehold_df[column_name].unique() if v is not None])
            # Filter labels to only those present in the data and map to ticks
            valid_labels = [labels[int(v)] for v in unique_vals if int(v) < len(labels)]

            # Update the specific axis
            update_dict = {
                'tickvals': unique_vals,
                'ticktext': valid_labels,
                'categoryorder': 'array',
                'categoryarray': unique_vals
            }
            if axis_key == 'xaxis':
                fig.update_layout(xaxis=update_dict)
            elif axis_key == 'yaxis':
                fig.update_layout(yaxis=update_dict)
        except Exception as e:
            st.warning(f"Could not apply custom axis labels for {column_name}: {e}")
            
# --- Streamlit App Layout ---
st.title("📊 Freehold Household Head Data Analysis")

if freehold_df.empty:
    st.warning("Could not load data. Please check the URL and file format.")
else:
    # --- Objective 3 Visualizations ---
    st.header("🔗 Objective 3: Deeper Correlations and Status Quo")

    # 1. Relationship between Land Size and Water Harvesting Adoption (Scatter Plot)
    st.subheader("1. Land Size vs. Water Harvesting Adoption")
    
    water_harvesting_col = 'Water harvesting'
    
    fig_land_water = px.scatter(
        freehold_df, 
        x='Land size', 
        y=water_harvesting_col,
        title='Land Size vs. Water Harvesting Adoption',
        template=PLOTLY_TEMPLATE
    )
    
    # Apply custom labels for the Y-axis (Water Harvesting)
    map_numeric_axis(fig_land_water, 'yaxis', water_harvesting_col)

    st.plotly_chart(fig_land_water, use_container_width=True)
    st.markdown("""
    * **Explanation:** This scatter plot visualizes the relationship between the **size of land** owned by household heads and whether they have **adopted water harvesting** practices.
    * **Key Insight:** Investigate if land size plays a role in the adoption of water harvesting (e.g., are larger farms more likely to adopt?).
    """)

    st.markdown("---")

    # 2. Access to Training by Membership to Community Organization (Grouped Bar Chart)
    st.subheader("2. Access to Training by Membership to Community Organization")
    
    membership_col = 'Membership to community organization/Group'
    training_col = 'Access to training'
    
    fig_membership_training = px.histogram(
        freehold_df, 
        x=membership_col, 
        color=training_col,
        title='Access to Training by Membership to Community Organization',
        template=PLOTLY_TEMPLATE, 
        barmode='group'
    )
    
    # Apply custom labels for X-axis (Membership)
    map_numeric_axis(fig_membership_training, 'xaxis', membership_col)

    # Apply custom labels for legend (Training)
    training_labels = encoding_mapping[training_col]
    fig_membership_training.for_each_trace(lambda t: t.update(name = training_labels[int(t.name)]) if t.name.isdigit() and int(t.name) < len(training_labels) else t)
    
    # Update legend layout
    fig_membership_training.update_layout(
        legend=dict(title='Access to Training', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig_membership_training, use_container_width=True)
    st.markdown("""
    * **Explanation:** This grouped bar chart illustrates the **access to training** among freehold households, categorized by whether they are **members of a community organization**.
    * **Key Insight:** Examine if membership in community organizations is associated with increased access to training, suggesting organizations serve as a knowledge-sharing channel.
    """)

    st.markdown("---")

    # 3. Distribution of Trend in Soil Condition (Pie Chart)
    st.subheader("3. Distribution of Trend in Soil Condition among Freehold Households")
    
    soil_condition_col = 'Trend in soil condition'
    soil_condition_labels = encoding_mapping[soil_condition_col]
    
    # Create a temporary DF with mapped labels for a cleaner pie chart
    temp_df_soil = freehold_df[soil_condition_col].value_counts().reset_index()
    temp_df_soil.columns = [soil_condition_col, 'Count']
    temp_df_soil[soil_condition_col] = temp_df_soil[soil_condition_col].apply(lambda x: soil_condition_labels[int(x)] if int(x) < len(soil_condition_labels) else f"Code {x}")

    fig_soil_condition = px.pie(
        temp_df_soil, 
        values='Count', 
        names=soil_condition_col,
        title='Distribution of Trend in Soil Condition among Freehold Households', 
        template=PLOTLY_TEMPLATE
    )
    
    fig_soil_condition.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig_soil_condition, use_container_width=True)
    st.markdown("""
    * **Explanation:** This pie chart shows the proportion of freehold households reporting different **trends in soil condition** (e.g., deteriorated, not changed, improved).
    * **Key Insight:** Understand the general perception of **soil health trends** within this population, which can indicate the long-term impact of farming practices.
    """)

    st.markdown("---")
    
    # 4. Correlation Heatmap of Selected Variables (Complex Visualization)
    st.header("4. 🔥 Correlation Heatmap of Key Variables")

    correlation_columns = [
        'Age', 'Household size', 'Land size', 'Level of education', 'Income ',
        'Water harvesting', 'Agroforestry', 'Perception of climate change',
        'Use of biofertilizers', 'Use of biopesticides', 'Trend in soil condition'
    ]

    # Calculate the correlation matrix
    try:
        # Ensure all columns exist before calculating correlation
        available_cols = [col for col in correlation_columns if col in freehold_df.columns]
        correlation_matrix = freehold_df[available_cols].corr()

        # Create the heatmap using Plotly Graph Objects (go)
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='Blues',
            colorbar=dict(title='Correlation Coefficient'),
            hovertemplate="Correlation of %{y} and %{x}: %{z:.2f}<extra></extra>"
        ))

        fig_heatmap.update_layout(
            title='Correlation Heatmap of Selected Variables',
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            yaxis_autorange='reversed',
            template=PLOTLY_TEMPLATE,
            height=700 # Give it some space
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown("""
        * **Explanation:** This **Heatmap** displays the Pearson correlation coefficients between all pairs of selected numerical and encoded categorical variables.
        * **Key Insight:** Look for values close to **+1** (strong positive correlation) or **-1** (strong negative correlation) to identify key relationships in the data. For example, a high positive correlation between 'Agroforestry' and 'Water harvesting' would suggest they are adopted together. 
        """)
        
    except Exception as e:
        st.error(f"Could not generate Correlation Heatmap. Check column names and data types: {e}")

    st.markdown("---")
    st.success("✅ Dashboard Complete: All objectives visualized.")
