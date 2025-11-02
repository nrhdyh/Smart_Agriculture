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

st.title("🌿 Climate Smart Agriculture from Kakamega County, Kenya Dashboard")



st.image(
    "https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/main/The-Applications-of-Drones-in-the-Agriculture-Industry-2-1024x536.jpg"
)



# ===========================
# OBJECTIVE 1: INTERACTIVE SUMMARY BOXES
# ===========================
if not freehold_df.empty:
    st.subheader("📈 Summary Highlights")

    # ---- Calculations with safety checks ----
    avg_age = round(freehold_df["Age"].mean(), 1) if "Age" in freehold_df.columns else 0
    avg_land = round(freehold_df["Land size"].mean(), 2) if "Land size" in freehold_df.columns else 0
    avg_household = round(freehold_df["Household size"].mean(), 1) if "Household size" in freehold_df.columns else 0

    # --- Most Common Education ---
    edu_labels = ['No formal education', 'Primary school', 'Secondary school', 'College/University', 'Vocational']
    if "Level of education" in freehold_df.columns:
        try:
            mode_edu_code = int(freehold_df["Level of education"].mode()[0])
            most_common_edu = edu_labels[mode_edu_code] if mode_edu_code < len(edu_labels) else "Unknown"
        except:
            most_common_edu = "N/A"
    else:
        most_common_edu = "N/A"

    # --- Gender Ratio ---
    if "Gender of household head" in freehold_df.columns:
        gender_col = freehold_df["Gender of household head"].astype(str).str.lower()

        male_count = gender_col[gender_col.str.contains("1|male")].count()
        female_count = gender_col[gender_col.str.contains("2|female")].count()
        total_gender = male_count + female_count

        if total_gender > 0:
            male_ratio = (male_count / total_gender) * 100
            female_ratio = 100 - male_ratio
        else:
            male_ratio, female_ratio = 0, 0
    else:
        male_ratio, female_ratio, total_gender, female_count = 0, 0, 0, 0

    # ---- Layout ----
    col1, col2, col3, col4 = st.columns(4)

    # --- Column 1: Average Age ---
    with col1:
        st.markdown("### 🧓 Average Age")
        st.metric(label="", value=f"{avg_age} yrs")
        st.progress(min(avg_age / 100, 1.0))
        st.caption("Most household heads are middle-aged (45–60 yrs).")

    # --- Column 2: Average Land Size ---
    with col2:
        st.markdown("### 🌾 Average Land Size")
        st.metric(label="", value=f"{avg_land} ha")
        st.progress(min(avg_land / 10, 1.0))
        st.caption("Land sizes mostly below 2 hectares.")

    # --- Column 3: Education Level ---
    with col3:
        st.markdown("### 🎓 Common Education Level")
        st.success(most_common_edu)
        st.caption("Most household heads have lower education levels.")

    #     # --- Column 4: Gender Ratio ---
    # with col4:
    #     st.markdown("### 👨‍🌾 Gender Distribution")

    #     if "Gender of household head" in freehold_df.columns:
    #         gender_col = freehold_df["Gender of household head"]

    #         # Dataset uses 0 = Male, 1 = Female
    #         male_count = (gender_col == 0).sum()
    #         female_count = (gender_col == 1).sum()
    #         total_gender = male_count + female_count

    #         if total_gender > 0:
    #             male_ratio = (male_count / total_gender) * 100
    #             female_ratio = 100 - male_ratio
    #         else:
    #             male_ratio, female_ratio = 0, 0
    #     else:
    #         male_ratio, female_ratio, total_gender, female_count = 0, 0, 0, 0

    #     # Display metrics dynamically
    #     st.metric(label="Male Heads", value=f"{male_ratio:.1f}%")
    #     st.progress(male_ratio / 100)

    #     if total_gender > 0:
    #         st.caption(f"Female Heads: {female_ratio:.1f}% ({female_count} of {total_gender})")
    #     else:
    #         st.caption("No gender data available.")

else:
    st.warning("⚠️ No data available. Please check the dataset URL or file format.")
    st.markdown("---")

# --- Data URL and Template ---
DATA_URL = 'https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/freehold_data_on_Climate_Smart_Agriculture.csv'
PLOTLY_TEMPLATE = 'plotly_dark'


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
st.markdown("---")
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

