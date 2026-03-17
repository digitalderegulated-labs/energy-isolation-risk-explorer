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
# STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color:#F6F8FB;
}

h1, h2, h3 {
    font-weight:700;
}

.metric-box {
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("⚡ Isolation Intelligence")
st.caption("Operational Risk Visibility for Complex Electrical Infrastructure")

# ---------------------------------------------------
# NAVIGATION
# ---------------------------------------------------

tabs = st.tabs([
    "Executive Overview",
    "Infrastructure Complexity",
    "Operational Isolation Risk",
    "Severe Incident Locations Across Infrastructure Environments",
    "Market Opportunity Signals",
    "Strategic Insights"
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
# MAP ENVIRONMENT
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
Modern infrastructure environments — including **data centers, telecommunications networks, power systems, and commercial facilities** — rely on increasingly complex electrical architectures.

These environments frequently include redundant power feeds, backup generation, UPS systems, and layered electrical distribution networks.

During maintenance operations, technicians must isolate every active energy source before work begins. As infrastructure complexity increases, verifying complete isolation becomes significantly more challenging.
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

    risk_data = df["environment"].value_counts()

    st.markdown("""
Severe incidents often occur in environments where electrical systems contain multiple active energy paths.

These environments frequently include:
- redundant electrical feeds
- backup generation
- UPS systems
- multi-layered distribution systems
""")

    fig = px.pie(
        names=risk_data.index,
        values=risk_data.values
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# INCIDENT MAP
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
# MARKET OPPORTUNITY SIGNALS
# ---------------------------------------------------

with tabs[4]:

    st.header("Organizations Operating Complex Electrical Infrastructure")

    lead_df = df[["employer","environment","city","state"]]
    lead_df = lead_df.drop_duplicates()

    st.dataframe(lead_df.head(100))

    st.subheader("Top Organizations by Incident Exposure")

    top_companies = df["employer"].value_counts().reset_index()
    top_companies.columns = ["Organization","Incident Records"]

    st.dataframe(top_companies.head(20))

# ---------------------------------------------------
# STRATEGIC INSIGHTS
# ---------------------------------------------------

with tabs[5]:

    st.header("Strategic Observations")

    st.markdown("""
### Infrastructure Complexity Drives Isolation Risk

Across modern infrastructure sectors, electrical systems are increasingly designed with redundancy and distributed energy paths.

This improves reliability but increases the operational complexity of verifying energy isolation during maintenance procedures.

### Environments with Highest Operational Complexity

The data indicates higher concentrations of severe incidents across sectors operating complex electrical infrastructure such as:

• data centers  
• telecommunications infrastructure  
• electric power systems  
• commercial construction projects  

### Implication

Organizations operating these environments must ensure technicians can confidently verify that all energy sources are isolated before maintenance work begins.

Digital lockout/tagout platforms can support these workflows by guiding technicians through structured isolation verification procedures.
""")
