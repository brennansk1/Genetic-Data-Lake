import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# ---------------------------
# Page Configuration & Custom Styling
# ---------------------------
st.set_page_config(page_title="Genetic Data Lake Dashboard", layout="wide")
st.markdown(
    """
    <style>
    .main { background-color: #F8F9FA; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2c3e50, #3498db); color: white; }
    .stButton>button { background-color: #3498db; color: white; border: none; border-radius: 4px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Database Connection
# ---------------------------
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_NAME = "datalake"
DB_HOST = "db"  # Use "db" if running in Docker; otherwise "localhost"
DB_PORT = "5432"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

@st.cache_resource(show_spinner=False)
def get_engine():
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Error creating engine: {e}")
        return None

engine = get_engine()

# ---------------------------
# Utility Functions for Efficient Data Loading
# ---------------------------
@st.cache_data(show_spinner=False)
def run_query(query):
    """Execute a SQL query and return a DataFrame."""
    try:
        df = pd.read_sql_query(text(query), engine)
        return df
    except SQLAlchemyError as e:
        st.error(f"SQLAlchemy error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Query error: {e}")
        return pd.DataFrame()

def load_table_full(table_name):
    """Load an entire table using SQL query."""
    query = f"SELECT * FROM {table_name}"
    return run_query(query)

def load_table_sample(table_name, limit=1000):
    """Load a sample of rows from a table."""
    query = f"SELECT * FROM {table_name} LIMIT {limit}"
    return run_query(query)

def safe_plot(plot_func, *args, **kwargs):
    try:
        fig = plot_func(*args, **kwargs)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Plot error: {e}")

# ---------------------------
# Dashboard Pages
# ---------------------------
def dashboard_overview():
    st.title("Genetic Data Lake Dashboard")
    st.markdown("### Overview")
    st.markdown("This dashboard provides a comprehensive view of synthetic genetic, health, and lifestyle data.")
    
    # List of tables excluding the snps dataset
    tables = ["individuals", "relationships", "marriages", "snp_definitions",
              "indel_definitions", "indels", "structural_variants", "health_phenotypes", "lifestyle"]
    summary = []
    for tbl in tables:
        df = load_table_sample(tbl, limit=100)
        summary.append({"Table": tbl, "Rows (sampled)": len(df)})
    summary_df = pd.DataFrame(summary)
    st.markdown("#### Table Summary (Sampled Rows)")
    st.dataframe(summary_df)
    safe_plot(px.bar, summary_df, x="Table", y="Rows (sampled)", title="Sample Row Counts per Table", color="Table")
    st.info("Caching and database indexes are used to optimize performance.")

def individuals_page():
    st.title("Individuals")
    df = load_table_full("individuals")
    if df.empty:
        st.warning("No individual data available.")
        return
    st.markdown("### Demographics")
    try:
        genders = df["gender"].dropna().unique().tolist()
    except Exception:
        genders = []
    selected_gender = st.sidebar.multiselect("Filter by Gender", options=genders, default=genders)
    filtered_df = df[df["gender"].isin(selected_gender)]
    st.dataframe(filtered_df.head(100))
    try:
        df["birth_year"] = pd.to_datetime(df["birth_date"], errors="coerce").dt.year
        safe_plot(px.histogram, df, x="birth_year", nbins=50, title="Birth Year Distribution")
    except Exception as e:
        st.error(f"Error generating birth year plot: {e}")

def health_lifestyle_page():
    st.title("Health & Lifestyle")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Health & Phenotype")
        health_df = load_table_full("health_phenotypes")
        if health_df.empty:
            st.warning("No health data available.")
        else:
            st.dataframe(health_df.head(100))
            safe_plot(px.histogram, health_df, x="bmi", nbins=50, title="BMI Distribution")
            safe_plot(px.scatter, health_df, x="height_cm", y="weight_kg", title="Height vs Weight", trendline="ols")
    with col2:
        st.markdown("#### Lifestyle")
        lifestyle_df = load_table_full("lifestyle")
        if lifestyle_df.empty:
            st.warning("No lifestyle data available.")
        else:
            st.dataframe(lifestyle_df.head(100))
            try:
                occ_counts = lifestyle_df["occupation"].value_counts().reset_index()
                occ_counts.columns = ["Occupation", "Count"]
                safe_plot(px.bar, occ_counts, x="Occupation", y="Count", title="Occupation Distribution")
            except Exception as e:
                st.error(f"Error generating occupation plot: {e}")

def genetics_page():
    st.title("Genetic Markers Overview")
    # Only using SNP definitions, not the snps (genotype) dataset
    marker_type = st.sidebar.radio("Select Marker Type", ["SNP Definitions", "Indel Definitions", "Indel Genotypes"])
    if marker_type == "SNP Definitions":
        df = load_table_full("snp_definitions")
        if df.empty:
            st.warning("No SNP definition data available.")
        else:
            st.dataframe(df.head(100))
            safe_plot(px.histogram, df, x="allele1_freq", nbins=50, title="SNP Allele1 Frequency Distribution")
    elif marker_type == "Indel Definitions":
        df = load_table_full("indel_definitions")
        if df.empty:
            st.warning("No Indel definition data available.")
        else:
            st.dataframe(df.head(100))
            safe_plot(px.histogram, df, x="frequency", nbins=50, title="Indel Frequency Distribution")
    elif marker_type == "Indel Genotypes":
        st.markdown("### Indel Genotype Sample")
        df = load_table_sample("indels", limit=200)
        if df.empty:
            st.warning("No Indel genotype data available.")
        else:
            st.dataframe(df.head(100))

def advanced_genetics_page():
    st.title("Advanced Genetic Analysis")
    snp_defs = load_table_full("snp_definitions")
    if snp_defs.empty:
        st.warning("No SNP definition data available for advanced analysis.")
        return
    chromosomes = sorted(snp_defs["chromosome"].dropna().unique())
    selected_chr = st.sidebar.selectbox("Select Chromosome", chromosomes)
    filtered_snp_defs = snp_defs[snp_defs["chromosome"] == selected_chr]
    st.subheader(f"SNP Definitions on Chromosome {selected_chr}")
    st.dataframe(filtered_snp_defs.head(100))
    safe_plot(px.histogram, filtered_snp_defs, x="allele1_freq", nbins=50,
              title=f"Allele1 Frequency Distribution (Chr {selected_chr})")
    # Remove SNP genotype details entirely from advanced analysis
    st.info("SNP genotype details are omitted for performance. Focus is on SNP definitions and other datasets.")

def relationships_page():
    st.title("Family Relationships")
    df = load_table_full("relationships")
    if df.empty:
        st.warning("No relationship data available.")
    else:
        st.dataframe(df.head(100))
        try:
            summary = df.groupby("father_id").size().reset_index(name="Count").head(10)
            st.markdown("#### Relationship Summary")
            st.dataframe(summary)
        except Exception as e:
            st.error(f"Error generating relationships summary: {e}")

def marriages_page():
    st.title("Marriages")
    df = load_table_full("marriages")
    if df.empty:
        st.warning("No marriage data available.")
    else:
        st.dataframe(df.head(100))
        try:
            df["marriage_date"] = pd.to_datetime(df["marriage_date"], errors="coerce")
            safe_plot(px.histogram, df, x="marriage_date", nbins=50, title="Marriage Date Distribution")
        except Exception as e:
            st.error(f"Error generating marriage plot: {e}")

def structural_variants_page():
    st.title("Structural Variants")
    df = load_table_full("structural_variants")
    if df.empty:
        st.warning("No structural variant data available.")
    else:
        st.dataframe(df.head(100))
        safe_plot(px.pie, df, names="variant_type", title="Structural Variant Type Distribution")

def detailed_tables_page():
    st.title("Detailed Data Tables")
    # Exclude the snps table from the list to speed up loading
    tables = ["individuals", "relationships", "marriages", "snp_definitions",
              "indel_definitions", "indels", "structural_variants",
              "health_phenotypes", "lifestyle"]
    selected_table = st.sidebar.selectbox("Select Table", tables)
    df = load_table_full(selected_table)
    st.markdown(f"### {selected_table.capitalize()} (first 200 rows)")
    st.dataframe(df.head(200))

# ---------------------------
# Sidebar Navigation & Page Rendering
# ---------------------------
st.sidebar.title("Navigation")
pages = [
    "Dashboard Overview", "Individuals", "Health & Lifestyle", "Genetic Analysis",
    "Advanced Genetics", "Family Relationships", "Marriages", "Structural Variants", "Detailed Tables"
]
selected_page = st.sidebar.selectbox("Select Page", pages)

if selected_page == "Dashboard Overview":
    dashboard_overview()
elif selected_page == "Individuals":
    individuals_page()
elif selected_page == "Health & Lifestyle":
    health_lifestyle_page()
elif selected_page == "Genetic Analysis":
    genetics_page()
elif selected_page == "Advanced Genetics":
    advanced_genetics_page()
elif selected_page == "Family Relationships":
    relationships_page()
elif selected_page == "Marriages":
    marriages_page()
elif selected_page == "Structural Variants":
    structural_variants_page()
elif selected_page == "Detailed Tables":
    detailed_tables_page()
