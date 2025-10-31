import streamlit as st
import pandas as pd

# ===========================
# LOAD DATA DIRECTLY FROM GITHUB
# ===========================
DATA_URL = "https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/freehold_data_on_Climate_Smart_Agriculture.csv"

@st.cache_data
def load_data(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load the data
freehold_df = load_data(DATA_URL)

# ===========================
# STREAMLIT UI
# ===========================
st.set_page_config(page_title="Climate Smart Agriculture Dashboard", page_icon="🌿", layout="wide")

st.title("🌿 Climate Smart Agriculture Dashboard")

st.markdown("""
Welcome to the **Climate Smart Agriculture (CSA)** data visualization platform.  
This dashboard analyzes insights from **married household heads** on various factors influencing CSA adoption.
""")

st.image(
    "https://images.unsplash.com/photo-1599498771460-26c1b2e2f743?auto=format&fit=crop&w=1200&q=60",
    caption="Sustainable Agriculture"
)

st.markdown("---")

# ===========================
# SUMMARY STATISTICS
# ===========================
if not freehold_df.empty:
    st.subheader("Key Summary Statistics")

    def safe_mean(df, col):
        return df[col].mean() if col in df.columns else 0

    def safe_percentage(df, col, value):
        if col in df.columns:
            return df[col].value_counts(normalize=True).get(value, 0) * 100
        return 0

    # --- Metric Calculations ---
    water_adoption = safe_percentage(freehold_df, 'Water harvesting', 1)
    avg_land_size = safe_mean(freehold_df, 'Land size')
    training_rate = safe_percentage(freehold_df, 'Training', 1)
    high_perception = safe_percentage(freehold_df, 'Perception of climate change', 2)

    # --- Display Metrics ---
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
        label="Training Participation Rate",
        value=f"{training_rate:.1f}%",
        help="Percentage of households that participated in agricultural training.",
        delta_color="normal",
        delta="Training"
    )
    col4.metric(
        label="High Climate Change Perception",
        value=f"{high_perception:.1f}%",
        help="Percentage of households reporting a high perception/awareness of climate change.",
        delta_color="normal",
        delta="Awareness"
    )

    st.markdown("---")

    with st.expander("📄 View Raw Dataset"):
        st.dataframe(freehold_df.head())

else:
    st.warning("⚠️ Unable to load data. Please check the dataset URL or connection.")
