import streamlit as st

st.set_page_config(
    page_title="Drive Time Analytics",
    page_icon="📊",
    layout="wide"
)

executive_overview = st.Page(
    "pages/executive_overview.py",
    title="Executive Overview",
    icon="📊",
    default=True
)

retail_event_explorer = st.Page(
    "pages/retail_event_explorer.py",
    title="Retail Event Explorer",
    icon="📅"
)

relationship_explorer = st.Page(
    "pages/relationship_explorer.py",
    title="Relationship Explorer",
    icon="🔎"
)

model_results = st.Page(
    "pages/model_results.py",
    title="Model Results",
    icon="📈"
)

about_project = st.Page(
    "pages/about_project.py",
    title="About the Project",
    icon="ℹ️"
)

pg = st.navigation(
    [
        executive_overview,
        retail_event_explorer,
        relationship_explorer,
        model_results,
        about_project
    ]
)

pg.run()