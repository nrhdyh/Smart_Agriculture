import streamlit as st

st.set_page_config(
    page_title="Climate Smart Agriculture - Married Data",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #e9f7ef 0%, #f9fff5 100%);
            font-family: 'Poppins', sans-serif;
        }
        .header {
            background: linear-gradient(90deg, #1b5e20, #43a047);
            color: white;
            padding: 35px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        }
        h1 { font-size: 42px; margin: 0; letter-spacing: 1px; }
        .subtitle { font-size: 18px; opacity: 0.9; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header">
        <h1>🌾 Climate Smart Agriculture Dashboard</h1>
        <div class="subtitle">Exploring Awareness, Economic Factors, and Training among Married Farmers</div>
    </div>
""", unsafe_allow_html=True)

st.write("Welcome to the **Climate Smart Agriculture Dashboard**. Navigate using the sidebar to explore three analytical sections:")
st.markdown("""
1️⃣ **Awareness and Education Impact** – How education affects awareness of CSA practices.  
2️⃣ **Economic and Farm Characteristics** – Relationship between income, farm size, and adoption.  
3️⃣ **Training and Satisfaction** – Influence of training on satisfaction levels.  
""")
st.info("📘 Select a page from the sidebar to start exploring the dataset.")
