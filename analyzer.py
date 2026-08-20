"""
Core analysis functions for the Job Market Analyzer.

Shared by app.py (Streamlit) and notebooks/Job_Market_Analyzer_Colab.ipynb
so both surfaces run the exact same logic against the exact same data.
"""

import sqlite3

import pandas as pd

REQUIRED_COLUMNS = [
    "job_title", "company", "location", "remote", "experience_level",
    "employment_type", "salary_min", "salary_max", "skills", "date_posted",
]


def load_data(path_or_buffer) -> pd.DataFrame:
    """Load a job-postings CSV and coerce dtypes used throughout the app."""
    df = pd.read_csv(path_or_buffer)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
    df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
    df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    df["skills"] = df["skills"].fillna("")
    return df


def explode_skills(df: pd.DataFrame) -> pd.DataFrame:
    """One row per (posting, skill) pair, for skill-frequency analysis."""
    exploded = df.assign(skill=df["skills"].str.split(",")).explode("skill")
    exploded["skill"] = exploded["skill"].str.strip()
    return exploded[exploded["skill"] != ""]


def top_skills(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    exploded = explode_skills(df)
    counts = (
        exploded.groupby("skill")
        .size()
        .reset_index(name="postings")
        .sort_values("postings", ascending=False)
        .head(n)
    )
    return counts


def salary_by_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    return (
        df.groupby(group_col)
        .agg(
            postings=("job_title", "count"),
            avg_salary=("salary_avg", "mean"),
            min_salary=("salary_min", "min"),
            max_salary=("salary_max", "max"),
        )
        .reset_index()
        .sort_values("avg_salary", ascending=False)
    )


def experience_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("experience_level")
        .size()
        .reset_index(name="postings")
        .sort_values("postings", ascending=False)
    )


def to_sqlite(df: pd.DataFrame, table_name: str = "job_postings") -> sqlite3.Connection:
    """Load a dataframe into an in-memory SQLite DB for ad-hoc SQL queries."""
    conn = sqlite3.connect(":memory:")
    df.to_sql(table_name, conn, index=False, if_exists="replace")
    return conn


def run_select_query(conn: sqlite3.Connection, sql: str) -> pd.DataFrame:
    """Run a read-only SQL query. Only single SELECT statements are allowed."""
    cleaned = sql.strip().rstrip(";")
    if not cleaned.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    if ";" in cleaned:
        raise ValueError("Only a single statement is allowed.")
    return pd.read_sql_query(cleaned, conn)
