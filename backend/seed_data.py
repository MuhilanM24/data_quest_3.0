"""Seed the standalone SQLite demo database.

SQLite is the local fallback used when Supabase is not configured. The API's
normal startup path also seeds this same deterministic dataset.
"""
import json
import os
import sqlite3
from pathlib import Path

from app.db import CAREERS, OPPORTUNITIES

ROOT = Path(__file__).resolve().parent
DATABASE = Path(os.getenv("PRISM_DB_PATH", ROOT / "prism.db"))


def seed() -> None:
    with sqlite3.connect(DATABASE) as connection:
        connection.executescript((ROOT / "database_schema.sql").read_text(encoding="utf-8"))
        connection.executemany(
            """INSERT INTO careers
            (id,title,category,fit,salary,why,skills,outlook,discipline,education_cost,
             market_demand,growth_score,salary_score,geographic_demand,education_path,
             exam_options,career_domain)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET title=excluded.title, category=excluded.category,
            fit=excluded.fit, salary=excluded.salary, why=excluded.why, skills=excluded.skills,
            outlook=excluded.outlook, discipline=excluded.discipline,
            education_cost=excluded.education_cost, market_demand=excluded.market_demand,
            growth_score=excluded.growth_score, salary_score=excluded.salary_score,
            geographic_demand=excluded.geographic_demand, education_path=excluded.education_path,
            exam_options=excluded.exam_options, career_domain=excluded.career_domain""",
            CAREERS,
        )
        connection.executemany("INSERT OR IGNORE INTO opportunities VALUES (?,?,?,?,?,?,?)", OPPORTUNITIES)
        connection.execute(
            """INSERT INTO students
            (id,name,email,age,grade,location,interests,constraints,education_cost)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET name=excluded.name,email=excluded.email,
            age=excluded.age,grade=excluded.grade,location=excluded.location""",
            ("demo-student", "Arun Kumar", "arun@example.test", 12, "12", "Chennai", "[]", "[]", 0),
        )
        connection.execute(
            """INSERT INTO parents (id,student_id,name,email,budget,priorities)
            VALUES (?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET student_id=excluded.student_id,
            budget=excluded.budget,priorities=excluded.priorities""",
            ("demo-parent", "demo-student", "Arun Kumar Family", "family@example.test", 200000,
             json.dumps(["Affordability", "Career stability"])),
        )


if __name__ == "__main__":
    seed()
    print(f"Seeded {DATABASE}")
