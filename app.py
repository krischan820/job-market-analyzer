"""
Job Market Analyzer — Streamlit app.

Analyzes job postings to surface in-demand skills, salary bands,
locations, and experience requirements.

Run locally:    streamlit run app.py
Deploy:         Streamlit Community Cloud (see README.md)
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from analyzer import (
    experience_distribution,
    load_data,
    run_select_query,
    salary_by_group,
    to_sqlite,
    top_skills,
)

DEFAULT_DATA_PATH = "data/job_postings_sample.csv"

st.set_page_config(
    page_title="Job Market Analyzer",
    page_icon="💼",
    layout="wide",
)

st.title("💼 Job Market Analyzer")
st.caption(
    "Analyzes job postings to identify in-demand skills, salaries, "
    "locations, and experience requirements."
)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload your own job postings CSV", type="csv")
    st.caption("No file? The sample dataset (150 postings) loads automatically.")

try:
    df = load_data(uploaded if uploaded is not None else DEFAULT_DATA_PATH)
except Exception as exc:  # noqa: BLE001 - surface any load/schema error to the user
    st.error(f"Couldn't load that file: {exc}")
    st.stop()

# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Filters")

    locations = sorted(df["location"].dropna().unique())
    selected_locations = st.multiselect("Location", locations, default=[])

    experience_levels = sorted(df["experience_level"].dropna().unique())
    selected_experience = st.multiselect("Experience level", experience_levels, default=[])

    employment_types = sorted(df["employment_type"].dropna().unique())
    selected_employment = st.multiselect("Employment type", employment_types, default=[])

    remote_only = st.checkbox("Remote only", value=False)

filtered = df.copy()
if selected_locations:
    filtered = filtered[filtered["location"].isin(selected_locations)]
if selected_experience:
    filtered = filtered[filtered["experience_level"].isin(selected_experience)]
if selected_employment:
    filtered = filtered[filtered["employment_type"].isin(selected_employment)]
if remote_only:
    filtered = filtered[filtered["remote"] == "Yes"]

if filtered.empty:
    st.warning("No postings match the current filters.")
    st.stop()

# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Job postings", f"{len(filtered):,}")
col2.metric("Avg. salary", f"${filtered['salary_avg'].mean():,.0f}")
col3.metric("Companies", f"{filtered['company'].nunique():,}")
col4.metric("Locations", f"{filtered['location'].nunique():,}")

st.divider()

# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
tab_skills, tab_salary, tab_experience, tab_data, tab_sql = st.tabs(
    ["🧠 Skills", "💰 Salary", "🎯 Experience", "📋 Data", "🗄️ SQL Explorer"]
)

with tab_skills:
    st.subheader("Most in-demand skills")
    n = st.slider("Number of skills to show", 5, 30, 15)
    skills_df = top_skills(filtered, n=n)
    fig = px.bar(
        skills_df.sort_values("postings"),
        x="postings", y="skill", orientation="h",
        labels={"postings": "Job postings", "skill": "Skill"},
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_salary:
    st.subheader("Salary by location")
    by_location = salary_by_group(filtered, "location").head(15)
    fig_loc = px.bar(
        by_location.sort_values("avg_salary"),
        x="avg_salary", y="location", orientation="h",
        labels={"avg_salary": "Average salary ($)", "location": "Location"},
    )
    st.plotly_chart(fig_loc, use_container_width=True)

    st.subheader("Salary by experience level")
    by_exp = salary_by_group(filtered, "experience_level")
    fig_exp = px.bar(
        by_exp, x="experience_level", y="avg_salary",
        labels={"avg_salary": "Average salary ($)", "experience_level": "Experience level"},
    )
    st.plotly_chart(fig_exp, use_container_width=True)

    st.subheader("Salary distribution")
    fig_box = px.box(filtered, x="experience_level", y="salary_avg",
                      labels={"salary_avg": "Salary ($)", "experience_level": "Experience level"})
    st.plotly_chart(fig_box, use_container_width=True)

with tab_experience:
    st.subheader("Postings by experience level")
    exp_dist = experience_distribution(filtered)
    fig_pie = px.pie(exp_dist, names="experience_level", values="postings", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Postings by employment type")
    emp_dist = filtered.groupby("employment_type").size().reset_index(name="postings")
    fig_emp = px.pie(emp_dist, names="employment_type", values="postings", hole=0.4)
    st.plotly_chart(fig_emp, use_container_width=True)

with tab_data:
    st.subheader("Filtered postings")
    st.dataframe(filtered.drop(columns=["salary_avg"]), use_container_width=True)
    st.download_button(
        "Download filtered data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="job_postings_filtered.csv",
        mime="text/csv",
    )

with tab_sql:
    st.subheader("Run SQL against the filtered data")
    st.caption("The filtered postings are loaded into an in-memory SQLite table named `job_postings`. SELECT-only.")
    default_query = "SELECT experience_level, ROUND(AVG(salary_avg), 0) AS avg_salary\nFROM job_postings\nGROUP BY experience_level\nORDER BY avg_salary DESC;"
    query = st.text_area("SQL query", value=default_query, height=140)
    if st.button("Run query"):
        try:
            conn = to_sqlite(filtered)
            result = run_select_query(conn, query)
            st.dataframe(result, use_container_width=True)
        except Exception as exc:  # noqa: BLE001 - show query errors inline
            st.error(f"Query failed: {exc}")

st.divider()
st.caption("Built with Python, pandas, SQL (SQLite), and Plotly · Streamlit")
