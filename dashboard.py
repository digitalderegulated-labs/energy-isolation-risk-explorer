import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Infrastructure Isolation Risk Intelligence",
    layout="wide"
)

# ---------------------------------------------------
# STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color:#f6f7fb;
}

h1 {
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Isolation Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Industry Risk Landscape",
        "Incident Locations",
        "Incident Trends",
        "Dataset Explorer"
    ]
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("osha_severe_injuries.csv", low_memory=False)

    # normalize column names
    df.columns = df.columns.str.lower()

    # convert date
    df["eventdate"] = pd.to_datetime(df["eventdate"], errors="coerce")
    df["year"] = df["eventdate"].dt.year

    return df


df = load_data()

# ---------------------------------------------------
# TARGET NAICS SECTORS
# ---------------------------------------------------

target_naics = [
    "221121",
    "221122",
    "238210",
    "517311",
    "518210",
    "236220"
]

df["primary naics"] = df["primary naics"].astype(str)

df = df[df["primary naics"].isin(target_naics)]

# ---------------------------------------------------
# NAICS → ENVIRONMENT
# ---------------------------------------------------

def map_environment(code):

    mapping = {

        "221121": "Electric Power Generation",
        "221122": "Electric Power Distribution",
        "238210": "Electrical Contractors",
        "517311": "Telecommunications Infrastructure",
        "518210": "Data Centers",
        "236220": "Commercial Infrastructure Construction"
    }

    return mapping.get(code, "Other")


df["environment"] = df["primary naics"].apply(map_environment)

# ---------------------------------------------------
# EXECUTIVE OVERVIEW
# ---------------------------------------------------

if page == "Executive Overview":

    st.title("Operational Risk in Complex Electrical Infrastructure")

    st.markdown("""
Electrical infrastructure environments such as power generation facilities, telecommunications networks, data centers, and commercial power systems rely on increasingly complex energy architectures.

During maintenance operations, technicians must isolate every active energy source before work begins. As infrastructure complexity increases, verifying that all energy sources have been properly isolated becomes operationally challenging.

This dashboard highlights severe incident patterns across infrastructure sectors where electrical isolation complexity is highest.
""")

    col1, col2, col3 = st.columns(3)

    col1.metric("Incident Records", len(df))
    col2.metric("Infrastructure Sectors", df["environment"].nunique())
    col3.metric("States Represented", df["state"].nunique())

    st.divider()

    st.subheader("Executive Insight")

    env_counts = df["environment"].value_counts()

    highest_risk_sector = env_counts.idxmax()

    st.info(
        f"Severe incidents are most frequently reported in **{highest_risk_sector}** environments, "
        "highlighting the operational complexity involved in maintaining electrical infrastructure "
        "across power systems, telecommunications networks, data centers, and commercial facilities."
    )

# ---------------------------------------------------
# INDUSTRY RISK LANDSCAPE
# ---------------------------------------------------

if page == "Industry Risk Landscape":

    st.title("Incident Distribution by Infrastructure Environment")

    env_counts = df["environment"].value_counts().reset_index()
    env_counts.columns = ["Environment", "Incidents"]

    fig = px.bar(
        env_counts,
        x="Environment",
        y="Incidents",
        color="Environment"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# INCIDENT LOCATION MAP
# ---------------------------------------------------

if page == "Incident Locations":

    st.title("Severe Incident Locations Across Infrastructure Environments")

    geo_df = df.dropna(subset=["latitude", "longitude"])

    fig = px.scatter_mapbox(
        geo_df,
        lat="latitude",
        lon="longitude",
        hover_name="employer",
        hover_data=["environment","city","state"],
        zoom=3,
        height=650
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# INCIDENT TRENDS
# ---------------------------------------------------

if page == "Incident Trends":

    st.title("Incident Trends Over Time")

    trend = df.groupby("year").size().reset_index(name="Incidents")

    fig = px.line(
        trend,
        x="year",
        y="Incidents",
        markers=True
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Year",
        yaxis_title="Incident Count"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# DATASET EXPLORER
# ---------------------------------------------------

if page == "Dataset Explorer":

    st.title("Dataset Explorer")

    st.write("Total Records:", len(df))

    st.dataframe(df.head(100))
