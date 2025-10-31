import streamlit as st

st.set_page_config(page_title="Climate Smart Agriculture Dashboard", layout="wide")

# Pages
home = st.Page("home.py", title="🏠 Home", default=True)
objective1 = st.Page("objective1.py", title="🎓 Objective 1: Education & Demographics")
objective2 = st.Page("objective2.py", title="🌾 Objective 2: Land & Perception")
objective3 = st.Page("objective3.py", title="🌱 Objective 3: Practices & Correlation")

# Navigation
pg = st.navigation({
    "Main Menu": [home, objective1, objective2, objective3]
})

pg.run()
