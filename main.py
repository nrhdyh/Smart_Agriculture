import streamlit as st


st.set_page_config(
    page_title="Student Survey"
)

visualise = st.Page('objective1.py', title='Objective 1', icon="::")

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()
