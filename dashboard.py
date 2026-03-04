import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Infrastructure Isolation Risk Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# STYLING
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color:#f7f8fa;
}

h1 {
    font-weight:700;
}

.metric-card {
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.05);
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
        "Geographic Distribution",
        "Incident Trends",
        "Dataset"
    ]
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("osha_severe_injuries.csv", low_memory=False)

    df.columns = df.columns.str.lower()

    if "eventdate" in df.columns:
        df["eventdate"] = pd.to_datetime(df["eventdate"], errors="coerce")
        df["year"] = df["eventdate"].dt.year

    return df


df = load_data()

# ---------------------------------------------------
# NAICS FILTER
# ---------------------------------------------------

TARGET_NAICS = [
    "221121",
    "221122",
    "238210",
    "517311",
    "518210",
    "236220"
]

df["primary naics"] = df["primary naics"].astype(str)

df = df[df["primary naics"].isin(TARGET_NAICS)]

# ---------------------------------------------------
# NAICS → ENVIRONMENT
# ---------------------------------------------------

def map_environment(code):

    if code == "221121":
        return "Electric Power Generation"

    if code == "221122":
        return "Electric Power Distribution"

    if code == "238210":
        return "Electrical Contractors"

    if code == "517311":
        return "Telecommunications Infrastructure"

    if code == "518210":
        return "Data Centers"

    if code == "236220":
        return "Commercial Infrastructure Construction"

    return "Other"


df["environment"] = df["primary naics"].apply(map_environment)

# ---------------------------------------------------
# EXECUTIVE OVERVIEW
# ---------------------------------------------------

if page == "Executive Overview":

    st.title("Operational Risk in Complex Electrical Infrastructure")

    st.markdown("""
Electrical infrastructure environments such as power generation facilities, telecommunications networks, data centers, and large commercial power systems rely on complex energy architectures.

During maintenance operations, technicians must isolate every active energy source before work begins. As infrastructure complexity increases, verifying that all energy sources have been properly isolated becomes more operationally challenging.

This dashboard highlights patterns in severe electrical incidents across key infrastructure sectors in the United States.
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Incident Records", len(df))

    with col2:
        st.metric("Infrastructure Environments", df["environment"].nunique())

    with col3:
        st.metric("States Represented", df["state"].nunique())

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
# GEOGRAPHIC DISTRIBUTION
# ---------------------------------------------------

if page == "Geographic Distribution":

    st.title("Geographic Distribution of Severe Incidents")

    state_counts = df.groupby("state").size().reset_index(name="Incidents")

    fig = px.choropleth(
        state_counts,
        locations="state",
        locationmode="USA-states",
        color="Incidents",
        scope="usa",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# INCIDENT TRENDS
# ---------------------------------------------------

if page == "Incident Trends":

    st.title("Incident Trends Over Time")

    if "year" in df.columns:

        trend = df.groupby("year").size().reset_index(name="Incidents")

        fig = px.line(
            trend,
            x="year",
            y="Incidents",
            markers=True
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# DATASET
# ---------------------------------------------------

if page == "Dataset":

    st.title("Dataset Preview")

    st.write("Total Records:", len(df))

    st.dataframe(df.head(100))
