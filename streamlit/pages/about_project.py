import streamlit as st


st.title("About the Project")

st.write(
    "Drive Time Analytics is an end-to-end retail analytics portfolio "
    "project built around a fictional retail operating environment."
)


st.subheader("What is Drive Time?")

st.write(
    "Drive Time is a retail operations concept focused on the "
    "2 PM to 5 PM peak shopping period. The project explores how "
    "customer experience, staffing, checkout conditions, product "
    "availability, store execution, and business performance relate "
    "to one another during this important part of the operating day."
)


st.subheader("Project Purpose")

st.write(
    "I built this project to practice the complete analytical process, "
    "including data validation, exploratory analysis, hypothesis testing, "
    "predictive modeling, statistical diagnostics, visualization, "
    "interactive application development, and final communication."
)


st.subheader("Analytical Workflow")

st.markdown(
    """
**Synthetic Retail Dataset**  
↓  
**Excel Validation and Project Control**  
↓  
**Orange Data Mining: Exploration and Modeling**  
↓  
**Python: Statistical Verification and Diagnostics**  
↓  
**Tableau: Executive Dashboard**  
↓  
**Streamlit: Interactive Exploration**  
↓  
**GitHub: Portfolio and Project Documentation**
"""
)


st.subheader("Key Analytical Lesson")

st.write(
    "One of my original expectations was that additional Drive Time "
    "labor coverage would be associated with better customer outcomes. "
    "The analysis did not support that simple relationship. Raw coverage "
    "remained nearly unrelated to Drive Time Service Health even after "
    "adjusting for transaction workload."
)

st.write(
    "That result changed the direction of the analysis toward staffing "
    "adequacy, checkout conditions, and operational execution rather than "
    "simply asking whether more labor automatically produced better results."
)


st.subheader("Tools Used")

tool_col1, tool_col2 = st.columns(2)

with tool_col1:
    st.markdown(
        """
- Microsoft Excel
- Orange Data Mining
- Python
- pandas
- statsmodels
"""
    )

with tool_col2:
    st.markdown(
        """
- Plotly
- Tableau
- Streamlit
- GitHub
- Microsoft Copilot
"""
    )


st.subheader("Data Disclaimer")

st.info(
    "This project uses fictional, synthetic, and AI-assisted retail data "
    "created for learning and portfolio development. The project does not "
    "contain actual store performance data, customer data, employee data, "
    "or company operational results."
)

st.write(
    "All findings describe relationships within the synthetic analytical "
    "environment and should not be interpreted as evidence about an actual "
    "retail location or organization."
)