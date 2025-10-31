import streamlit as st
import pandas as pd

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
Welcome to the **Climate Smart Agriculture (CSA)** data visualization platform.  
This dashboard explores insights from **married household heads** on factors influencing CSA adoption.

### 📊 Dashboard Overview
- **Objective 1:** Explore education, demographics, and training participation.  
- **Objective 2:** Analyze land ownership, land size, and economic patterns.  
- **Objective 3:** Understand adoption of CSA practices and climate change perceptions.
""")

st.image(
    "https://images.unsplash.com/photo-1599498771460-26c1b2e2f743?auto=format&fit=crop&w=1200&q=60",
    caption="Sustainable Agriculture in Practice 🌾"
)

st.markdown("---")

# ===========================
# SUMMARY STATISTICS SECTION
# ===========================
if not freehold_df.empty:
    st.subheader("🌱 Key Summary Statistics")

    # --- Helper Functions ---
    def safe_mean(df, col):
        """Safely calculate mean for numeric columns"""
        return df[col].mean() if col in df.columns else 0

    def safe_percentage(df, col, value):
        """Safely calculate percentage of a given value"""
        if col in df.columns:
            return df[col].value_counts(normalize=True).get(value, 0) * 100
        return 0

    # --- Metric Calculations ---
    water_adoption = safe_percentage(freehold_df, 'Water harvesting', 1)
    avg_land_size = safe_mean(freehold_df, 'Land size')
    training_rate = safe_percentage(freehold_df, 'Access to training', 1)
    high_perception = safe_percentage(freehold_df, 'Perception of climate change', 2)

    # --- Display Metrics in 4 Columns ---
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="💧 CSA Adoption (Water Harvesting)",
        value=f"{water_adoption:.1f}%",
        help="Percentage of households that adopted water harvesting practices.",
        delta="Target Practice",
        delta_color="normal"
    )
    col2.metric(
        label="🌾 Average Farm Size",
        value=f"{avg_land_size:.2f}",
        help="Mean size of agricultural land (in Hectares).",
        delta="Hectares",
        delta_color="off"
    )
    col3.metric(
        label="🎓 Training Participation Rate",
        value=f"{training_rate:.1f}%",
        help="Percentage of households that participated in agricultural training programs.",
        delta="Training",
        delta_color="normal"
    )
    col4.metric(
        label="🌍 High Climate Change Perception",
        value=f"{high_perception:.1f}%",
        help="Percentage of households with high awareness of climate change.",
        delta="Awareness",
        delta_color="normal"
    )

    st.markdown("---")

    # --- Optional: Dataset Preview ---
    with st.expander("📄 View Raw Dataset"):
        st.dataframe(freehold_df.head())

else:
    st.warning("⚠️ Unable to load data. Please check the dataset URL or your connection.")
