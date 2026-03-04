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
    background-color:#f6f7fb;
}

h1 {
    font-weight:700;
}

.block-container {
    padding-top:2rem;
}

.cta-box {
    background:#ffffff;
    padding:25px;
    border-radius:12px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("⚡ Isolation Intelligence")
st.caption("Operational Risk Visibility for Complex Electrical Infrastructure")

# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------

st.sidebar.title("Platform Navigation")

page = st.sidebar.radio(
    "",
    [
        "Executive Overview",
        "Infrastructure Complexity",
        "Operational Risk Exposure",
        "Severe Incident Locations Across Infrastructure Environments",
        "Dataset Explorer"
    ]
)

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
# NAICS FILTER
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
# NAICS → INFRASTRUCTURE TYPE
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

    st.header("Infrastructure Complexity and Isolation Risk")

    st.markdown("""
Modern infrastructure environments — including **data centers, telecommunications networks, power systems, and commercial electrical facilities** — rely on increasingly complex electrical architectures.

These environments frequently include:

• multiple incoming utility feeds  
• backup generators  
• UPS systems  
• layered distribution panels  
• redundant electrical pathways  

During maintenance operations, technicians must isolate **every active energy source** before work begins. As infrastructure complexity increases, verifying complete isolation becomes significantly more difficult.

This dashboard explores where these complex environments exist and how severe incidents appear across them.
""")

    col1, col2, col3 = st.columns(3)

    col1.metric("Severe Incident Records", len(df))
    col2.metric("Infrastructure Sectors", df["environment"].nunique())
    col3.metric("Organizations Represented", df["employer"].nunique())

# ---------------------------------------------------
# INFRASTRUCTURE COMPLEXITY
# ---------------------------------------------------

if page == "Infrastructure Complexity":

    st.header("Infrastructure Environments with Complex Electrical Systems")

    st.markdown("""
Certain infrastructure sectors operate **highly layered electrical architectures** where multiple energy sources must be managed simultaneously.

These environments often include redundant power distribution designed for reliability — which increases the complexity of isolation procedures during maintenance operations.
""")

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
# OPERATIONAL RISK
# ---------------------------------------------------

if page == "Operational Risk Exposure":

    st.header("Operational Isolation Risk")

    st.markdown("""
In complex electrical environments, verifying that all energy sources have been isolated is a critical safety requirement.

When isolation steps are missed or performed incorrectly, workers can be exposed to live energy sources during maintenance operations.

The presence of redundant infrastructure systems — including backup generation, UPS systems, and multi-layered distribution — increases the number of possible energy paths that must be verified.
""")

    env_counts = df["environment"].value_counts()

    highest = env_counts.idxmax()

    st.info(
        f"Severe incidents are most frequently reported in **{highest}** environments, "
        "highlighting the operational complexity involved in managing electrical isolation procedures "
        "across modern infrastructure systems."
    )

# ---------------------------------------------------
# INCIDENT MAP
# ---------------------------------------------------

if page == "Severe Incident Locations Across Infrastructure Environments":

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
# CTA + SALES LEAD
# ---------------------------------------------------

st.divider()

st.markdown("""
### Managing Isolation Risk in Complex Infrastructure

Organizations operating complex electrical environments must ensure that all energy sources are verified as isolated before maintenance begins.

Digital lockout/tagout platforms provide structured workflows that help technicians confirm isolation steps across complex infrastructure systems.
""")

with st.container():

    st.markdown('<div class="cta-box">', unsafe_allow_html=True)

    st.subheader("Request a Demonstration")

    name = st.text_input("Name")
    company = st.text_input("Company")
    email = st.text_input("Email")

    if st.button("Request Demo"):

        st.success("Thank you. A product specialist will reach out to schedule a demonstration.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# DATASET
# ---------------------------------------------------

if page == "Dataset Explorer":

    st.header("Dataset Explorer")

    st.dataframe(df.head(200))
