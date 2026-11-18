import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px


st.title("Relationship Explorer")

st.write(
    "Explore how operational conditions relate to "
    "Drive Time Service Health across the five-year dataset."
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


relationship_data = open_store[
    [
        "Date",
        "FiscalYear",
        "RetailEvent",
        "StaffingPercent",
        "DriveTimeServiceHealth",
        "SCOWaitTime",
        "CallOffCount",
        "Sales"
    ]
].dropna().copy()


relationship_data["FiscalYear"] = (
    relationship_data["FiscalYear"]
    .astype(int)
    .astype(str)
)


st.subheader(
    "Staffing Percent vs. Drive Time Service Health"
)

st.caption(
    f"Showing {len(relationship_data):,} open-store observations"
)
x_min = relationship_data["StaffingPercent"].min()
x_max = relationship_data["StaffingPercent"].max()

y_min = relationship_data["DriveTimeServiceHealth"].min()
y_max = relationship_data["DriveTimeServiceHealth"].max()


staffing_fig = px.scatter(
    relationship_data,
    x="StaffingPercent",
    y="DriveTimeServiceHealth",
    animation_frame="FiscalYear",
    labels={
        "StaffingPercent": "Staffing Percent",
        "DriveTimeServiceHealth": "Drive Time Service Health",
        "FiscalYear": "Fiscal Year"
    },
    hover_data={
        "Date": True,
        "RetailEvent": True,
        "SCOWaitTime": ":.2f",
        "CallOffCount": True,
        "Sales": ":$,.0f"
    },
    range_x=[x_min - 1, x_max + 1],
    range_y=[y_min - 1, y_max + 1]
)


staffing_fig.update_traces(
    marker=dict(
        size=8,
        opacity=0.60
    )
)


staffing_fig.update_layout(
    xaxis_title="Staffing Percent",
    yaxis_title="Drive Time Service Health",
    height=650,
    showlegend=False
)


staffing_fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
staffing_fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 700


st.plotly_chart(
    staffing_fig,
    width="stretch",
    alt=(
        "Animated scatterplot of Staffing Percent versus "
        "Drive Time Service Health by fiscal year."
    )
)
st.divider()

st.subheader(
    "SCO Wait Time vs. Drive Time Service Health"
)

st.write(
    "Explore the relationship between SCO Wait Time and "
    "Drive Time Service Health across all open-store observations."
)


sco_fig = px.scatter(
    relationship_data,
    x="SCOWaitTime",
    y="DriveTimeServiceHealth",
    labels={
        "SCOWaitTime": "SCO Wait Time (sec)",
        "DriveTimeServiceHealth": "Drive Time Service Health"
    },
    hover_data={
        "Date": True,
        "FiscalYear": True,
        "RetailEvent": True,
        "StaffingPercent": ":.1f",
        "CallOffCount": True,
        "Sales": ":$,.0f"
    }
)


sco_fig.update_traces(
    marker=dict(
        size=8,
        opacity=0.55
    )
)


sco_fig.update_layout(
    xaxis_title="SCO Wait Time (sec)",
    yaxis_title="Drive Time Service Health",
    height=600,
    showlegend=False
)


st.plotly_chart(
    sco_fig,
    width="stretch",
    alt=(
        "Scatterplot of SCO Wait Time versus "
        "Drive Time Service Health."
    )
)