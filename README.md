# 💼 Job Market Analyzer

Analyzes job postings to identify in-demand skills, salaries, locations, and experience requirements — as an interactive **Streamlit** dashboard, a **Google Colab** notebook, and reusable **pandas + SQL** analysis code.

**Technologies:** Python, Pandas, SQL, Data Visualization (Plotly / Matplotlib), Streamlit

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krischan820/krischan820/blob/main/job-market-analyzer/notebooks/Job_Market_Analyzer_Colab.ipynb)
[![Deploy on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=krischan820/krischan820&branch=main&mainModule=job-market-analyzer/app.py)

> The badges above assume this folder has been merged into `main`. Until then, swap `main` for your branch name (e.g. `claude/job-market-analyzer-app-1eqpll`) in the URLs.

---

## What it does

- **Skills analysis** — parses the `skills` column and ranks the most in-demand skills across postings.
- **Salary analysis** — average/min/max salary by location and experience level, plus salary distribution.
- **Location & experience breakdowns** — where the jobs are and what seniority they require.
- **SQL explorer** — run ad-hoc `SELECT` queries against the postings (SQLite in-memory), both in the app and the notebook.
- **Bring your own data** — upload any CSV with the same columns to analyze real job postings instead of the bundled sample.

## Project structure

```
job-market-analyzer/
├── app.py                              # Streamlit dashboard (entry point)
├── analyzer.py                         # Shared pandas/SQL analysis functions
├── requirements.txt                    # Python dependencies
├── .streamlit/config.toml              # Streamlit theme
├── data/
│   └── job_postings_sample.csv         # 150-row synthetic sample dataset
├── scripts/
│   └── generate_sample_data.py         # Regenerates the sample dataset
├── sql/
│   └── analysis_queries.sql            # Example SQL analyses
└── notebooks/
    └── Job_Market_Analyzer_Colab.ipynb # Google Colab notebook
```

## Data schema

Any CSV you load (sample or your own) needs these columns:

| Column              | Type   | Example                          |
|---------------------|--------|-----------------------------------|
| `job_id`            | string | `JP-1042`                         |
| `job_title`         | string | `Data Analyst`                    |
| `company`           | string | `Northwind Analytics`             |
| `location`          | string | `Austin, TX` or `Remote`          |
| `remote`            | string | `Yes` / `No`                      |
| `experience_level`  | string | `Entry Level`, `Mid Level`, `Senior`, `Lead/Principal` |
| `employment_type`   | string | `Full-time`, `Contract`, ...      |
| `salary_min`        | number | `70000`                           |
| `salary_max`        | number | `95000`                           |
| `skills`            | string | `Python, SQL, Power BI`           |
| `date_posted`       | date   | `2026-08-01`                      |

---

## Step 1: Get the files onto GitHub

You have two options — pick whichever is easier for you.

### Option A — Upload through the GitHub website (no terminal needed)

1. Go to your repository on GitHub (e.g. `https://github.com/krischan820/krischan820`).
2. Click **Add file → Upload files**.
3. Create/enter the `job-market-analyzer` folder by typing `job-market-analyzer/` at the start of a dragged file's path, or upload files and then use **Add file → Create new file** to place them (GitHub lets you type a full path like `job-market-analyzer/app.py` as the filename, which creates the folder automatically).
4. Drag in all the files from this project: `app.py`, `analyzer.py`, `requirements.txt`, `.streamlit/config.toml`, `data/job_postings_sample.csv`, `scripts/generate_sample_data.py`, `sql/analysis_queries.sql`, `notebooks/Job_Market_Analyzer_Colab.ipynb`, and this `README.md`.
5. Scroll down, add a commit message like `Add Job Market Analyzer app`, and click **Commit changes** (commit directly to your branch, or open a pull request if prompted).

### Option B — Push with Git (recommended if you already have the folder locally)

```bash
cd job-market-analyzer
git init                                   # skip if already inside a git repo
git remote add origin https://github.com/krischan820/krischan820.git   # skip if already set
git checkout -b claude/job-market-analyzer-app-1eqpll   # or your branch of choice
git add .
git commit -m "Add Job Market Analyzer app"
git push -u origin claude/job-market-analyzer-app-1eqpll
```

Then open a pull request into `main` on GitHub when you're ready to merge.

---

## Step 2: Deploy on Streamlit Community Cloud (streamlit.app)

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with your GitHub account.
2. Click **Create app** → **From existing repo**.
3. Fill in:
   - **Repository:** `krischan820/krischan820`
   - **Branch:** `main` (or your working branch, e.g. `claude/job-market-analyzer-app-1eqpll`)
   - **Main file path:** `job-market-analyzer/app.py`
4. Click **Deploy**. Streamlit Cloud installs `job-market-analyzer/requirements.txt` automatically and starts the app.
5. Once live, your app gets a public URL like `https://<your-app-name>.streamlit.app` — share it or add it to your GitHub profile README.
6. To update the live app later, just push new commits to the branch it's deployed from — Streamlit Cloud redeploys automatically.

## Step 3: Run it in Google Colab

**Fastest way:** click the "Open in Colab" badge at the top of this README (update `main` to your branch name if the folder isn't merged yet).

**Manual way:**

1. Go to **[colab.research.google.com](https://colab.research.google.com)**.
2. **File → Open notebook → GitHub tab**.
3. Enter the repo `krischan820/krischan820` and select `job-market-analyzer/notebooks/Job_Market_Analyzer_Colab.ipynb`.
4. Run all cells (**Runtime → Run all**). The first cell clones the repo and installs dependencies, so no local setup is required.
5. To analyze your own data instead of the sample, uncomment the file-upload cell in section 2 of the notebook.

---

## Run it locally (optional)

```bash
cd job-market-analyzer
python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Regenerating the sample dataset

The bundled `data/job_postings_sample.csv` (150 synthetic postings) was generated with:

```bash
cd job-market-analyzer
python scripts/generate_sample_data.py
```

Edit `scripts/generate_sample_data.py` to change the job titles, skills, locations, or salary ranges used to generate it.

## Using real data

Replace `data/job_postings_sample.csv` with your own export (or upload a CSV directly in the app/notebook) as long as it matches the [data schema](#data-schema) above. Good sources: job board exports, a scraped dataset, or a public jobs API/dataset.
