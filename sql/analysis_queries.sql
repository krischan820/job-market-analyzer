-- Job Market Analyzer — reference SQL queries
--
-- These run against a `job_postings` table loaded from
-- data/job_postings_sample.csv (see analyzer.to_sqlite / the notebook /
-- the app's "SQL Explorer" tab). Schema:
--
--   job_id, job_title, company, location, remote, experience_level,
--   employment_type, salary_min, salary_max, skills, date_posted

-- 1. Average salary by experience level
SELECT
    experience_level,
    COUNT(*) AS postings,
    ROUND(AVG((salary_min + salary_max) / 2.0), 0) AS avg_salary
FROM job_postings
GROUP BY experience_level
ORDER BY avg_salary DESC;

-- 2. Highest-paying locations (min 5 postings)
SELECT
    location,
    COUNT(*) AS postings,
    ROUND(AVG((salary_min + salary_max) / 2.0), 0) AS avg_salary
FROM job_postings
GROUP BY location
HAVING COUNT(*) >= 5
ORDER BY avg_salary DESC
LIMIT 10;

-- 3. Postings by employment type and remote status
SELECT
    employment_type,
    remote,
    COUNT(*) AS postings
FROM job_postings
GROUP BY employment_type, remote
ORDER BY postings DESC;

-- 4. Most common job titles
SELECT
    job_title,
    COUNT(*) AS postings,
    ROUND(AVG((salary_min + salary_max) / 2.0), 0) AS avg_salary
FROM job_postings
GROUP BY job_title
ORDER BY postings DESC
LIMIT 10;

-- 5. Recent postings (last 30 days from the newest posting date)
SELECT job_id, job_title, company, location, salary_min, salary_max, date_posted
FROM job_postings
WHERE date_posted >= DATE((SELECT MAX(date_posted) FROM job_postings), '-30 days')
ORDER BY date_posted DESC;

-- 6. Senior roles above the overall average salary
SELECT job_id, job_title, company, location, salary_min, salary_max
FROM job_postings
WHERE experience_level = 'Senior'
  AND (salary_min + salary_max) / 2.0 > (SELECT AVG((salary_min + salary_max) / 2.0) FROM job_postings)
ORDER BY salary_max DESC;

-- 7. Top skills, split out of the comma-separated `skills` column using a
--    recursive CTE (skill counting itself is easier in pandas — see
--    analyzer.top_skills — but this shows it's doable in pure SQLite too).
WITH RECURSIVE split(job_id, skill, rest) AS (
    SELECT job_id, '', skills || ',' FROM job_postings
    UNION ALL
    SELECT
        job_id,
        TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)),
        SUBSTR(rest, INSTR(rest, ',') + 1)
    FROM split
    WHERE rest != ''
)
SELECT skill, COUNT(*) AS postings
FROM split
WHERE skill != ''
GROUP BY skill
ORDER BY postings DESC
LIMIT 15;
