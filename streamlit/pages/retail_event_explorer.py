import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("Retail Event Explorer")

st.write(
    "Explore how Retail Event performance changes across the "
    "five-year synthetic dataset."
)


data_file = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "DriveTime_Analytics_AI_Corrected_v1.3.xlsx"
)


df = pd.read_excel(
    data_file,
    sheet_name="Drive Time Data"
)


open_store = df[df["StoreOpenFlag"] == 1].copy()


retail_events = open_store[
    open_store["RetailEventFlag"] == 1
].copy()


retail_events["SalesPerOperatingHour"] = (
    retail_events["Sales"] / retail_events["OperatingHours"]
)


st.subheader("Animated Retail Event Performance")


metric_options = {
    "Sales per Operating Hour": "SalesPerOperatingHour",
    "Transactions": "Transactions",
    "Average Basket": "AverageBasket",
    "Drive Time Service Health": "DriveTimeServiceHealth"
}


selected_metric_label = st.selectbox(
    "Metric to Explore",
    list(metric_options.keys())
)


selected_metric = metric_options[selected_metric_label]
event_summary = (
    retail_events
    .groupby(
        ["FiscalYear", "RetailEvent"],
        as_index=False
    )
    .agg(
        SalesPerOperatingHour=("SalesPerOperatingHour", "mean"),
        Transactions=("Transactions", "mean"),
        AverageBasket=("AverageBasket", "mean"),
        DriveTimeServiceHealth=("DriveTimeServiceHealth", "mean")
    )
)


event_summary["FiscalYear"] = (
    event_summary["FiscalYear"].astype(int).astype(str)
)


metric_formats = {
    "Sales per Operating Hour": ":$,.0f",
    "Transactions": ":,.0f",
    "Average Basket": ":$,.2f",
    "Drive Time Service Health": ":.1f"
}


max_value = event_summary[selected_metric].max()


animation_fig = px.bar(
    event_summary,
    x=selected_metric,
    y="RetailEvent",
    orientation="h",
    animation_frame="FiscalYear",
    animation_group="RetailEvent",
    labels={
        selected_metric: selected_metric_label,
        "RetailEvent": "Retail Event",
        "FiscalYear": "Fiscal Year"
    },
    hover_data={
        selected_metric: metric_formats[selected_metric_label],
        "FiscalYear": True
    },
    range_x=[0, max_value * 1.10]
)


animation_fig.update_layout(
    xaxis_title=selected_metric_label,
    yaxis_title="Retail Event",
    showlegend=False,
    height=650
)


event_order = (
    event_summary
    .groupby("RetailEvent")[selected_metric]
    .mean()
    .sort_values(ascending=True)
    .index
    .tolist()
)


animation_fig.update_yaxes(
    categoryorder="array",
    categoryarray=event_order
)


animation_fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
animation_fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 700


st.plotly_chart(
    animation_fig,
    width="stretch",
    alt=(
        f"Animated Retail Event comparison of "
        f"{selected_metric_label} by fiscal year."
    )
)
st.divider()

st.subheader("Retail Event Detail")


event_options = sorted(
    retail_events["RetailEvent"]
    .dropna()
    .unique()
    .tolist()
)


selected_event = st.selectbox(
    "Select Retail Event",
    event_options
)


event_detail = retail_events[
    retail_events["RetailEvent"] == selected_event
].copy()


detail_sales_per_hour = event_detail["SalesPerOperatingHour"].mean()
detail_transactions = event_detail["Transactions"].mean()
detail_average_basket = event_detail["AverageBasket"].mean()
detail_service_health = event_detail["DriveTimeServiceHealth"].mean()
detail_nps = event_detail["DriveTimeNPS"].mean()


detail_row1 = st.columns(3)

with detail_row1[0]:
    st.metric(
        "Sales per Operating Hour",
        f"${detail_sales_per_hour:,.0f}"
    )

with detail_row1[1]:
    st.metric(
        "Average Transactions",
        f"{detail_transactions:,.0f}"
    )

with detail_row1[2]:
    st.metric(
        "Average Basket",
        f"${detail_average_basket:,.2f}"
    )


detail_row2 = st.columns(2)

with detail_row2[0]:
    st.metric(
        "Drive Time Service Health",
        f"{detail_service_health:.1f}%"
    )

with detail_row2[1]:
    st.metric(
        "Drive Time NPS",
        f"{detail_nps:.1f}%"
    )