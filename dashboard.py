import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Isolation Intelligence",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------
# ENTERPRISE STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color:#F5F7FA;
}

h1 {
    font-weight:700;
}

.section-box {
    background:white;
    padding:25px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("⚡ Isolation Intelligence")
st.caption("Infrastructure Complexity and Operational Isolation Risk")

# ---------------------------------------------------
# NAVIGATION
# ---------------------------------------------------

tabs = st.tabs([
    "Executive Overview",
    "Infrastructure Complexity",
    "Operational Isolation Risk",
    "Severe Incident Locations Across Infrastructure Environments",
    "Sales Opportunity Signals"
])

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("osha_severe_injuries.csv", low_memory=False)

    df.columns = df.columns.str.lower()

    df["eventdate"] = pd.to_datetime(df["eventdate"], errors="coerce")

    return df


df = load_data()

# ---------------------------------------------------
# TARGET NAICS
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

with tabs[0]:

    st.header("Infrastructure Complexity and Isolation Risk")

    col1, col2, col3 = st.columns(3)

    col1.metric("Severe Incident Records", len(df))
    col2.metric("Infrastructure Sectors", df["environment"].nunique())
    col3.metric("Organizations Represented", df["employer"].nunique())

    st.markdown("""
Modern infrastructure environments — including **data centers, telecommunications networks, power systems, and commercial facilities** — rely on complex electrical architectures that include redundant power feeds, backup generation, and layered distribution systems.

During maintenance operations, technicians must isolate every active energy source before work begins. As infrastructure complexity increases, verifying complete energy isolation becomes significantly more difficult.
""")

# ---------------------------------------------------
# INFRASTRUCTURE COMPLEXITY
# ---------------------------------------------------

with tabs[1]:

    st.header("Infrastructure Environments with Complex Electrical Systems")

    env_counts = df["environment"].value_counts().reset_index()
    env_counts.columns = ["Environment","Incidents"]

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
# OPERATIONAL RISK
# ---------------------------------------------------

with tabs[2]:

    st.header("Operational Isolation Risk")

    env_counts = df["environment"].value_counts()

    highest = env_counts.idxmax()

    st.info(
        f"The highest concentration of severe incidents occurs in **{highest}** environments. "
        "These environments typically operate layered electrical infrastructure that includes "
        "backup generation, UPS systems, and redundant distribution paths."
    )

# ---------------------------------------------------
# INCIDENT MAP (UNCHANGED)
# ---------------------------------------------------

with tabs[3]:

    st.header("Severe Incident Locations Across Infrastructure Environments")

    geo_df = df.dropna(subset=["latitude","longitude"])

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
# SALES OPPORTUNITY SIGNALS
# ---------------------------------------------------

with tabs[4]:

    st.header("Organizations Operating Complex Infrastructure Environments")

    st.markdown("""
The organizations below operate infrastructure environments where electrical isolation procedures must be managed carefully during maintenance operations.

These environments often contain layered electrical systems including backup generation, UPS infrastructure, and redundant distribution paths.
""")

    lead_df = df[["employer","environment","city","state"]]
    lead_df = lead_df.drop_duplicates()

    st.dataframe(lead_df.head(100))

    st.subheader("Organizations with Highest Incident Exposure")

    top_companies = df["employer"].value_counts().reset_index()
    top_companies.columns = ["Organization","Incident Records"]

    st.dataframe(top_companies.head(20))
