import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("Executive Overview")

st.write(
    "Interactive overview of Drive Time performance during the "
    "2 PM to 5 PM peak shopping period."
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


st.subheader("Filters")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)


with filter_col1:
    fiscal_year = st.selectbox(
        "Fiscal Year",
        ["All Years"] + sorted(open_store["FiscalYear"].dropna().unique().tolist())
    )


with filter_col2:
    retail_event = st.selectbox(
        "Retail Event",
        ["All Events"] + sorted(
            open_store["RetailEvent"].dropna().unique().tolist()
        )
    )


with filter_col3:
    day_of_week = st.selectbox(
        "Day of Week",
        [
            "All Days",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
    )


with filter_col4:
    day_type = st.selectbox(
        "Day Type",
        [
            "All",
            "Weekday",
            "Weekend"
        ]
    )
filtered_data = open_store.copy()


if fiscal_year != "All Years":
    filtered_data = filtered_data[
        filtered_data["FiscalYear"] == fiscal_year
    ]


if retail_event != "All Events":
    filtered_data = filtered_data[
        filtered_data["RetailEvent"] == retail_event
    ]


if day_of_week != "All Days":
    filtered_data = filtered_data[
        filtered_data["DayOfWeek"] == day_of_week
    ]


if day_type == "Weekday":
    filtered_data = filtered_data[
        filtered_data["WeekendFlag"] == 0
    ]

elif day_type == "Weekend":
    filtered_data = filtered_data[
        filtered_data["WeekendFlag"] == 1
    ]


st.caption(
    f"Showing {len(filtered_data):,} open-store observations"
)
st.subheader("Key Performance Indicators")


avg_sales = filtered_data["Sales"].mean()
avg_transactions = filtered_data["Transactions"].mean()
avg_service_health = filtered_data["DriveTimeServiceHealth"].mean()
avg_nps = filtered_data["DriveTimeNPS"].mean()
avg_staffing = filtered_data["StaffingPercent"].mean()
avg_sco_wait = filtered_data["SCOWaitTime"].mean()


kpi_row1 = st.columns(3)

with kpi_row1[0]:
    st.metric(
        "Average Daily Sales",
        f"${avg_sales:,.0f}"
    )

with kpi_row1[1]:
    st.metric(
        "Average Daily Transactions",
        f"{avg_transactions:,.0f}"
    )

with kpi_row1[2]:
    st.metric(
        "Drive Time Service Health",
        f"{avg_service_health:.1f}%"
    )


kpi_row2 = st.columns(3)

with kpi_row2[0]:
    st.metric(
        "Drive Time NPS",
        f"{avg_nps:.1f}%"
    )

with kpi_row2[1]:
    st.metric(
        "Staffing Percent",
        f"{avg_staffing:.1f}%"
    )

with kpi_row2[2]:
    st.metric(
        "SCO Wait Time",
        f"{avg_sco_wait:.2f} sec"
    )
st.subheader("Drive Time Performance Trend")


metric_options = {
    "Drive Time Service Health": "DriveTimeServiceHealth",
    "Drive Time NPS": "DriveTimeNPS",
    "Drive Time Sales": "DriveTimeSales",
    "Drive Time Transactions": "DriveTimeTransactions",
    "Staffing Percent": "StaffingPercent",
    "SCO Wait Time": "SCOWaitTime"
}


selected_metric_label = st.selectbox(
    "Metric to Explore",
    list(metric_options.keys())
)


selected_metric = metric_options[selected_metric_label]
trend_data = filtered_data.sort_values("Date").copy()


trend_fig = px.line(
    trend_data,
    x="Date",
    y=selected_metric,
    labels={
        "Date": "Date",
        selected_metric: selected_metric_label
    },
    hover_data={
        "RetailEvent": True,
        "DayOfWeek": True,
        "StaffingPercent": ":.1f",
        "SCOWaitTime": ":.2f"
    }
)


trend_fig.update_traces(
    mode="lines"
)


trend_fig.update_layout(
    xaxis_title="Date",
    yaxis_title=selected_metric_label,
    hovermode="x",
    showlegend=False
)


st.plotly_chart(
    trend_fig,
    width="stretch",
    alt=f"{selected_metric_label} trend across the filtered Drive Time dataset."
)