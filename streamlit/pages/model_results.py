import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px


st.title("Model Results")

st.write(
    "Review the preferred Drive Time Service Health model, "
    "coefficients, multicollinearity diagnostics, and model comparison."
)


outputs_dir = (
    Path(__file__).resolve().parent.parent
    / "outputs"
)


model_comparison = pd.read_csv(
    outputs_dir / "Python_Model_Comparison.csv"
)

coefficients = pd.read_csv(
    outputs_dir / "Python_ServiceHealth_Coefficients.csv"
)

vif_results = pd.read_csv(
    outputs_dir / "Python_VIF_Preferred_Model.csv"
)



preferred_model = model_comparison[
    model_comparison["Model"] == "7-Feature Preferred Model"
].iloc[0]


predictor_vif = vif_results[
    vif_results["Variable"] != "const"
]


highest_vif = predictor_vif["VIF"].max()


st.subheader("Preferred Model")

st.caption(
    "Seven-predictor explanatory model for Drive Time Service Health"
)


model_kpis = st.columns(5)


with model_kpis[0]:
    st.metric(
        "R²",
        f"{preferred_model['R_Squared']:.3f}"
    )


with model_kpis[1]:
    st.metric(
        "Adjusted R²",
        f"{preferred_model['Adjusted_R_Squared']:.3f}"
    )


with model_kpis[2]:
    st.metric(
        "AIC",
        f"{preferred_model['AIC']:,.1f}"
    )


with model_kpis[3]:
    st.metric(
        "BIC",
        f"{preferred_model['BIC']:,.1f}"
    )


with model_kpis[4]:
    st.metric(
        "Highest VIF",
        f"{highest_vif:.2f}"
    )
st.subheader("Preferred Model Coefficients")


coef_plot = coefficients[
    coefficients["Variable"] != "const"
].copy()


coef_plot["CI_Plus"] = (
    coef_plot["CI_Upper_95"]
    - coef_plot["Coefficient"]
)


coef_plot["CI_Minus"] = (
    coef_plot["Coefficient"]
    - coef_plot["CI_Lower_95"]
)


coef_plot["Direction"] = coef_plot["Coefficient"].apply(
    lambda x: "Positive" if x >= 0 else "Negative"
)


coef_plot = coef_plot.sort_values(
    "Coefficient",
    ascending=True
)


coefficient_fig = px.bar(
    coef_plot,
    x="Coefficient",
    y="Variable",
    orientation="h",
    color="Direction",
    color_discrete_map={
        "Positive": "#2E86AB",
        "Negative": "#C44E52"
    },
    error_x="CI_Plus",
    error_x_minus="CI_Minus",
    hover_data={
        "P_Value": ":.4f",
        "CI_Lower_95": ":.3f",
        "CI_Upper_95": ":.3f",
        "Direction": False
    },
    labels={
        "Coefficient": "Regression Coefficient",
        "Variable": "Predictor"
    }
)


coefficient_fig.add_vline(
    x=0,
    line_width=1,
    line_dash="dash",
    line_color="gray"
)


coefficient_fig.update_layout(
    height=500,
    showlegend=True,
    xaxis_title="Regression Coefficient",
    yaxis_title="Predictor"
)


st.plotly_chart(
    coefficient_fig,
    width="stretch",
    alt=(
        "Preferred model regression coefficients with "
        "95 percent confidence intervals."
    )
)
st.divider()

st.subheader("Model Comparison")


comparison_display = model_comparison.copy()

comparison_display["R_Squared"] = (
    comparison_display["R_Squared"].round(3)
)

comparison_display["Adjusted_R_Squared"] = (
    comparison_display["Adjusted_R_Squared"].round(3)
)

comparison_display["AIC"] = (
    comparison_display["AIC"].round(1)
)

comparison_display["BIC"] = (
    comparison_display["BIC"].round(1)
)


comparison_display = comparison_display.rename(
    columns={
        "Observations": "N",
        "R_Squared": "R²",
        "Adjusted_R_Squared": "Adjusted R²"
    }
)


st.dataframe(
    comparison_display,
    width="stretch",
    hide_index=True
)


st.subheader("Multicollinearity Diagnostics")


vif_display = vif_results[
    vif_results["Variable"] != "const"
].copy()


vif_display["VIF"] = vif_display["VIF"].round(2)


vif_display = vif_display.sort_values(
    "VIF",
    ascending=False
)


st.dataframe(
    vif_display,
    width="stretch",
    hide_index=True
)


st.caption(
    "The preferred seven-predictor model reduced the highest "
    "remaining VIF to approximately 2.70."
)
st.divider()

st.subheader("Model Diagnostics")

st.write(
    "Residual diagnostics provide additional context for evaluating "
    "the preferred seven-predictor regression model."
)


diagnostic_col1, diagnostic_col2 = st.columns(2)


residual_image = (
    outputs_dir
    / "Chart_Residuals_vs_Predicted_Values.png"
)

qq_image = next(
    outputs_dir.glob("Chart_Q-Q*")
)


with diagnostic_col1:
    st.markdown("#### Residuals vs. Predicted Values")

    st.image(
        residual_image,
        width="stretch"
    )


with diagnostic_col2:
    st.markdown("#### Q-Q Plot of Regression Residuals")

    st.image(
        qq_image,
        width="stretch"
    )