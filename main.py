import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("married_data_on_Climate_Smart_Agriculture.csv")
    return df

df = load_data()

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Climate Smart Agriculture", layout="wide")

# ==============================
# CUSTOM STYLES
# ==============================
st.markdown("""
    <style>
        body {
            background-color: #F6FFF7;
        }
        .main-title {
            text-align: center;
            font-size: 36px;
            color: #1B5E20;
            font-weight: bold;
        }
        .nav-container {
            display: flex;
            justify-content: center;
            background-color: #A5D6A7;
            border-radius: 12px;
            margin-bottom: 25px;
            padding: 8px;
        }
        .nav-item {
            margin: 0 25px;
            font-size: 18px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: color 0.3s;
        }
        .nav-item:hover {
            color: #004D40;
        }
        .active {
            color: #004D40;
            text-decoration: underline;
        }
        h2, h3 {
            color: #2E7D32;
        }
        .summary-box {
            background-color: #E8F5E9;
            border-left: 6px solid #43A047;
            padding: 15px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# NAVIGATION BAR (TOP)
# ==============================
pages = ["Overview", "Objective 1", "Objective 2", "Objective 3"]
query_params = st.experimental_get_query_params()
current_page = query_params.get("page", ["Overview"])[0]

# Render nav bar
nav_html = '<div class="nav-container">'
for p in pages:
    active_class = "active" if p == current_page else ""
    nav_html += f'<a class="nav-item {active_class}" href="?page={p}">{p}</a>'
nav_html += '</div>'
st.markdown(nav_html, unsafe_allow_html=True)

# ==============================
# PAGE CONTENTS
# ==============================
if current_page == "Overview":
    st.markdown('<div class="main-title">🌿 Climate-Smart Agriculture Dashboard</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🎯 Objective
    To analyze how married individuals engage in climate-smart agriculture (CSA) practices 
    and understand the factors influencing adoption and awareness.
    """)

    st.markdown('<div class="summary-box">This dashboard explores participation levels, education, income, and awareness of CSA practices. Visualizations highlight key trends, relationships, and factors that promote or hinder sustainable farming.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "Gender" in df.columns and "Awareness_Level" in df.columns:
            fig1 = px.bar(df, x="Gender", color="Awareness_Level", 
                          title="Awareness Level by Gender",
                          color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if "Education_Level" in df.columns and "Adoption_of_CSA" in df.columns:
            fig2 = px.box(df, x="Education_Level", y="Adoption_of_CSA",
                          title="CSA Adoption by Education Level",
                          color_discrete_sequence=["#81C784"])
            st.plotly_chart(fig2, use_container_width=True)

# ==============================
# OBJECTIVE 1
# ==============================
elif current_page == "Objective 1":
    st.markdown('<div class="main-title">📘 Objective 1: Awareness & Education Impact</div>', unsafe_allow_html=True)

    st.markdown("**Objective:** To examine how education level influences awareness and adoption of CSA practices among married individuals.")
    st.markdown('<div class="summary-box">Higher education is often linked with increased awareness and better adoption of climate-smart techniques. These visualizations illustrate patterns between education and CSA awareness/adoption levels.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        fig = px.histogram(df, x="Education_Level", color="Awareness_Level",
                           title="Awareness by Education Level",
                           color_discrete_sequence=px.colors.sequential.Greens)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(df, x="Education_Level", y="Adoption_of_CSA",
                         color="Awareness_Level", title="Adoption vs Education",
                         color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        fig = px.density_heatmap(df, x="Awareness_Level", y="Adoption_of_CSA",
                                 title="Heatmap: Awareness vs Adoption",
                                 color_continuous_scale="Greens")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Interpretation:** Farmers with higher education tend to have greater CSA awareness and adoption, suggesting education is a key factor in sustainable practice diffusion.")

# ==============================
# OBJECTIVE 2
# ==============================
elif current_page == "Objective 2":
    st.markdown('<div class="main-title">🚜 Objective 2: Income & Participation</div>', unsafe_allow_html=True)

    st.markdown("**Objective:** To investigate the relationship between income levels and participation in CSA programs.")
    st.markdown('<div class="summary-box">Financial stability influences the ability to invest in sustainable technologies. The charts below explore how income affects participation and adoption of CSA programs.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        fig = px.violin(df, x="Income_Level", y="Participation_in_CSA", box=True,
                        color="Income_Level", title="Participation by Income Level",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(df, x="Income_Level", y="Adoption_of_CSA",
                         color="Participation_in_CSA", title="Adoption vs Income",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        fig = px.box(df, x="Income_Level", y="Awareness_Level",
                     title="Awareness by Income",
                     color_discrete_sequence=px.colors.sequential.Greens)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Interpretation:** Middle-income farmers often show the highest participation rates due to better access to training and financial stability.")

# ==============================
# OBJECTIVE 3
# ==============================
elif current_page == "Objective 3":
    st.markdown('<div class="main-title">🌍 Objective 3: Geospatial & Environmental Insights</div>', unsafe_allow_html=True)

    st.markdown("**Objective:** To analyze regional variations in CSA adoption and awareness.")
    st.markdown('<div class="summary-box">Mapping regional data reveals which areas lead or lag in adoption of CSA practices. This helps in designing targeted awareness campaigns and resource allocation.</div>', unsafe_allow_html=True)

    if "Region" in df.columns and "Adoption_of_CSA" in df.columns:
        fig = px.choropleth(df, locations="Region", locationmode="country names",
                            color="Adoption_of_CSA", hover_name="Region",
                            title="CSA Adoption by Region",
                            color_continuous_scale="Greens")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df, x="Region", y="Awareness_Level",
                     title="Awareness Level by Region",
                     color_discrete_sequence=["#43A047"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(df, x="Region", y="Participation_in_CSA",
                         size="Adoption_of_CSA", title="Participation vs Region",
                         color_discrete_sequence=["#66BB6A"])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Interpretation:** Some regions show lower adoption, suggesting need for stronger outreach and support programs.")
