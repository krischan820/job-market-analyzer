"""
Generates data/job_postings_sample.csv — a synthetic job-postings dataset
used to demo the Job Market Analyzer. All companies and postings are
fictitious; only the shape of the data (titles, skills, locations, salary
bands) is meant to resemble a real job market.

Run:
    python scripts/generate_sample_data.py
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "job_postings_sample.csv")

random.seed(42)
np.random.seed(42)

JOB_TITLES = [
    "Data Analyst", "Data Scientist", "Data Engineer", "Business Analyst",
    "Software Engineer", "Machine Learning Engineer", "BI Developer",
    "Product Manager", "DevOps Engineer", "Full Stack Developer",
    "Backend Developer", "Frontend Developer", "Analytics Manager",
    "Database Administrator", "Cloud Engineer",
]

SKILLS_BY_TITLE = {
    "Data Analyst": ["SQL", "Excel", "Python", "Power BI", "Tableau", "Statistics", "Data Analysis", "Communication"],
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Statistics", "TensorFlow", "R", "Data Analysis", "AWS"],
    "Data Engineer": ["Python", "SQL", "Spark", "Airflow", "AWS", "Docker", "Hadoop", "Snowflake"],
    "Business Analyst": ["SQL", "Excel", "Power BI", "Communication", "Project Management", "Data Analysis", "Agile"],
    "Software Engineer": ["Python", "Java", "JavaScript", "Git", "REST APIs", "Docker", "SQL", "React"],
    "Machine Learning Engineer": ["Python", "TensorFlow", "Machine Learning", "SQL", "Docker", "AWS", "Statistics", "Kubernetes"],
    "BI Developer": ["SQL", "Power BI", "Tableau", "Excel", "ETL", "Data Analysis", "Snowflake"],
    "Product Manager": ["Communication", "Agile", "Project Management", "SQL", "Leadership", "Data Analysis"],
    "DevOps Engineer": ["AWS", "Docker", "Kubernetes", "Azure", "Git", "CI/CD", "Python", "Linux"],
    "Full Stack Developer": ["JavaScript", "React", "Node.js", "SQL", "Python", "REST APIs", "Git", "AWS"],
    "Backend Developer": ["Python", "Java", "SQL", "REST APIs", "Docker", "AWS", "C#", ".NET"],
    "Frontend Developer": ["JavaScript", "React", "CSS", "HTML", "Git", "REST APIs", "TypeScript"],
    "Analytics Manager": ["SQL", "Power BI", "Leadership", "Data Analysis", "Communication", "Project Management", "Python"],
    "Database Administrator": ["SQL", "SQL Server", "Azure", "Database Design", "Python", "Linux"],
    "Cloud Engineer": ["AWS", "Azure", "Docker", "Kubernetes", "Terraform", "Python", "Linux", "CI/CD"],
}

LOCATIONS = [
    "Remote", "New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA",
    "Chicago, IL", "Boston, MA", "Atlanta, GA", "Denver, CO", "Los Angeles, CA",
    "Jacksonville, FL", "Miami, FL", "Dallas, TX", "Charlotte, NC", "Raleigh, NC",
]

# Rough cost-of-living / market salary multiplier by location
LOCATION_MULTIPLIER = {
    "Remote": 1.00, "New York, NY": 1.25, "San Francisco, CA": 1.35,
    "Austin, TX": 1.05, "Seattle, WA": 1.20, "Chicago, IL": 1.05,
    "Boston, MA": 1.15, "Atlanta, GA": 0.98, "Denver, CO": 1.02,
    "Los Angeles, CA": 1.18, "Jacksonville, FL": 0.92, "Miami, FL": 0.97,
    "Dallas, TX": 1.00, "Charlotte, NC": 0.95, "Raleigh, NC": 0.97,
}

EXPERIENCE_LEVELS = ["Entry Level", "Mid Level", "Senior", "Lead/Principal"]
EXPERIENCE_BASE_SALARY = {
    "Entry Level": (50000, 70000),
    "Mid Level": (70000, 100000),
    "Senior": (100000, 140000),
    "Lead/Principal": (135000, 190000),
}

EMPLOYMENT_TYPES = ["Full-time", "Full-time", "Full-time", "Contract", "Part-time", "Internship"]

COMPANY_PREFIXES = [
    "Northwind", "BlueOrbit", "Summit", "Horizon", "Cascade", "Ironwood",
    "Brightline", "Vertex", "Lumen", "Meridian", "Silverline", "Redwood",
    "Bluepeak", "Clearwater", "Anchorpoint", "Nova", "Granite", "Skyline",
    "Riverbend", "Fieldstone",
]
COMPANY_SUFFIXES = [
    "Analytics", "Technologies", "Systems", "Labs", "Solutions", "Software",
    "Data Co.", "Digital", "Consulting", "Group",
]
COMPANIES = sorted({f"{p} {s}" for p in COMPANY_PREFIXES for s in COMPANY_SUFFIXES})
random.shuffle(COMPANIES)
COMPANIES = COMPANIES[:60]

N_ROWS = 150
TODAY = datetime(2026, 8, 19)

rows = []
for i in range(N_ROWS):
    title = random.choice(JOB_TITLES)
    location = random.choice(LOCATIONS)
    experience = random.choices(EXPERIENCE_LEVELS, weights=[0.25, 0.35, 0.28, 0.12])[0]
    employment_type = random.choice(EMPLOYMENT_TYPES)
    company = random.choice(COMPANIES)

    base_low, base_high = EXPERIENCE_BASE_SALARY[experience]
    multiplier = LOCATION_MULTIPLIER[location]
    salary_min = int(base_low * multiplier * np.random.uniform(0.95, 1.05) / 500) * 500
    salary_max = int(base_high * multiplier * np.random.uniform(0.95, 1.10) / 500) * 500
    if salary_max <= salary_min:
        salary_max = salary_min + 10000

    pool = SKILLS_BY_TITLE[title]
    k = random.randint(4, min(6, len(pool)))
    skills = random.sample(pool, k)

    days_ago = random.randint(0, 90)
    date_posted = (TODAY - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    is_remote = "Yes" if location == "Remote" else random.choices(["No", "Yes"], weights=[0.75, 0.25])[0]

    rows.append({
        "job_id": f"JP-{1000 + i}",
        "job_title": title,
        "company": company,
        "location": location,
        "remote": is_remote,
        "experience_level": experience,
        "employment_type": employment_type,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "skills": ", ".join(skills),
        "date_posted": date_posted,
    })

df = pd.DataFrame(rows).sort_values("date_posted", ascending=False).reset_index(drop=True)
df.to_csv(OUTPUT_PATH, index=False)
print(f"Wrote {OUTPUT_PATH} with {len(df)} rows")
