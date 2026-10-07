"""Local-first SQLite persistence and deterministic seed data for PRISM."""
import json
import os
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("PRISM_DB_PATH", Path(__file__).parents[1] / "prism.db"))

CAREERS = [
    ("product", "Product Designer", "Creative technology", 94, "$92k–$145k", "You translate human needs into useful, beautiful products.", "Design research,Prototyping,Storytelling", "Very strong", "Technology", 180000, 88, 84, 82, "High", "B.Des / BFA in Product or UX Design", "NID DAT, UCEED", "Design & Technology"),
    ("software", "Software Engineer", "Computing", 92, "$105k–$175k", "You enjoy turning ideas into systems that work.", "Python,JavaScript,Systems thinking", "Very strong", "Technology", 220000, 95, 92, 90, "Very high", "B.Tech / B.E. Computer Science", "JEE Main, JEE Advanced, BITSAT", "Technology"),
    ("data", "Data Scientist", "Analytics", 90, "$96k–$160k", "You turn patterns into clear decisions and enjoy asking why.", "Python,Statistics,Visualization", "Strong", "Mathematics", 200000, 91, 89, 87, "High", "B.Tech / B.Sc. Data Science or Statistics", "JEE Main, CUET", "Data & Analytics"),
    ("robotics", "Robotics Engineer", "Engineering", 87, "$88k–$145k", "Your curiosity fits the loop of building, testing, and improving.", "CAD,Controls,Electronics", "Strong", "Engineering", 240000, 86, 83, 82, "High", "B.Tech in Robotics / Mechanical / Electronics", "JEE Main, JEE Advanced", "Engineering"),
    ("biomedical", "Biomedical Engineer", "Life science", 85, "$78k–$125k", "You connect science and empathy to make health better.", "Biology,Prototyping,Research", "Strong", "Science", 210000, 78, 80, 76, "Moderate", "B.Tech Biomedical Engineering", "JEE Main, NEET (for allied programs)", "Healthcare & Science"),
    ("climate", "Climate Systems Analyst", "Impact & science", 84, "$71k–$118k", "Your values align with work that improves the world at scale.", "Systems thinking,GIS,Policy", "Strong", "Science", 150000, 85, 82, 74, "High", "B.Sc. Environmental Science / B.Tech Climate Studies", "CUET, JEE Main", "Climate & Sustainability"),
    ("cybersecurity", "Cybersecurity Analyst", "Computing", 81, "$82k–$140k", "You notice risks, ask sharp questions, and protect what matters.", "Networks,Threat modeling,Communication", "Very strong", "Technology", 190000, 93, 88, 85, "Very high", "B.Tech Computer Science / Cybersecurity", "JEE Main, CUET", "Technology"),
    ("architect", "Sustainable Architect", "Built environment", 79, "$70k–$120k", "You balance creative vision with constraints and community impact.", "Sketching,CAD,Materials", "Moderate", "Engineering", 260000, 75, 78, 73, "Moderate", "B.Arch with sustainable design focus", "NATA, JEE Main Paper 2", "Architecture & Design"),
    ("game", "Game Developer", "Creative technology", 78, "$68k–$130k", "You combine narrative, logic, and play to create memorable worlds.", "Unity,C#,Narrative design", "Strong", "Technology", 170000, 83, 80, 77, "High", "B.Des / B.Tech Game Design or Computer Science", "UCEED, NID DAT, JEE Main", "Creative Technology"),
    ("environment", "Environmental Scientist", "Earth systems", 76, "$58k–$98k", "You want evidence-led work that protects people and planet.", "Field research,Data analysis,Ecology", "Strong", "Science", 130000, 80, 74, 70, "High", "B.Sc. Environmental Science / Ecology", "CUET, state university entrance", "Environment & Science"),
    ("ai-ml-engineer", "AI / ML Engineer", "Computing", 93, "$110k–$185k", "You build intelligent systems that learn from data and improve decisions.", "Python,Machine learning,Linear algebra", "Very strong", "Mathematics", 230000, 97, 94, 93, "Very high", "B.Tech / B.Sc. Computer Science, AI, or Data Science", "JEE Main, CUET, BITSAT", "AI & Technology"),
    ("data-scientist", "Data Scientist", "Analytics", 90, "$96k–$160k", "You turn patterns into clear decisions and enjoy asking why.", "Python,Statistics,Visualization", "Strong", "Mathematics", 200000, 91, 89, 87, "High", "B.Tech / B.Sc. Data Science or Statistics", "JEE Main, CUET", "Data & Analytics"),
    ("software-engineer", "Software Engineer", "Computing", 92, "$105k–$175k", "You enjoy turning ideas into systems that work.", "Python,JavaScript,Systems thinking", "Very strong", "Technology", 220000, 95, 92, 90, "Very high", "B.Tech / B.E. Computer Science", "JEE Main, JEE Advanced, BITSAT", "Technology"),
    ("cybersecurity-analyst", "Cybersecurity Analyst", "Computing", 81, "$82k–$140k", "You notice risks, ask sharp questions, and protect what matters.", "Networks,Threat modeling,Communication", "Very strong", "Technology", 190000, 93, 88, 85, "Very high", "B.Tech Computer Science / Cybersecurity", "JEE Main, CUET", "Technology"),
    ("robotics-engineer", "Robotics Engineer", "Engineering", 87, "$88k–$145k", "Your curiosity fits the loop of building, testing, and improving.", "CAD,Controls,Electronics", "Strong", "Engineering", 240000, 86, 83, 82, "High", "B.Tech in Robotics / Mechanical / Electronics", "JEE Main, JEE Advanced", "Engineering"),
    ("biomedical-engineer", "Biomedical Engineer", "Life science", 85, "$78k–$125k", "You connect science and empathy to make health better.", "Biology,Prototyping,Research", "Strong", "Science", 210000, 78, 80, 76, "Moderate", "B.Tech Biomedical Engineering", "JEE Main, NEET (for allied programs)", "Healthcare & Science"),
    ("renewable-energy-engineer", "Renewable Energy Engineer", "Energy & sustainability", 84, "$80k–$135k", "You design cleaner energy systems for a resilient future.", "Thermodynamics,Power systems,Modeling", "Strong", "Engineering", 200000, 89, 86, 80, "High", "B.Tech Renewable Energy / Electrical / Mechanical Engineering", "JEE Main, state engineering entrance", "Climate & Sustainability"),
    ("ui-ux-designer", "UI/UX Designer", "Creative technology", 88, "$82k–$140k", "You make complex technology intuitive, inclusive, and useful.", "User research,Prototyping,Visual design", "Very strong", "Technology", 180000, 88, 84, 82, "High", "B.Des / BFA in UI/UX or Product Design", "NID DAT, UCEED", "Design & Technology"),
    ("biotechnology-researcher", "Biotechnology Researcher", "Life science", 82, "$70k–$118k", "You use biology and experimentation to solve meaningful problems.", "Biology,Laboratory methods,Statistics", "Strong", "Science", 190000, 82, 81, 75, "Moderate", "B.Sc. / B.Tech Biotechnology or Life Sciences", "CUET, NEET, university entrance", "Healthcare & Science"),
    ("environmental-data-analyst", "Environmental Data Analyst", "Earth systems", 83, "$65k–$110k", "You turn environmental evidence into action for healthier communities.", "GIS,Data analysis,Ecology", "Strong", "Science", 150000, 85, 82, 74, "High", "B.Sc. Environmental Science / Data Science / GIS", "CUET, state university entrance", "Environment & Science"),
]
OPPORTUNITIES = [
    ("o1", "FutureMakers Design Sprint", "Civic Lab", "Sprint", "Remote", "Oct 22", "Design,Team"),
    ("o2", "AI for Good Fellowship", "Northstar Foundation", "Fellowship", "Hybrid · Boston", "Nov 4", "AI,Impact"),
    ("o3", "Open Data Challenge", "DataKind", "Challenge", "Remote", "Nov 16", "Data,Portfolio"),
    ("o4", "Build with NASA Open Data", "NASA Community", "Project", "Remote", "Dec 2", "Science,Data"),
    ("o5", "Young Inventors Lab", "City Makerspace", "Workshop", "Local", "Dec 12", "Robotics,Build"),
]
CAREER_ALIASES = {
    "product": "ui-ux-designer",
    "software": "software-engineer",
    "data": "data-scientist",
    "robotics": "robotics-engineer",
    "biomedical": "biomedical-engineer",
    "climate": "renewable-energy-engineer",
    "cybersecurity": "cybersecurity-analyst",
    "environment": "environmental-data-analyst",
}

def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db() -> None:
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS careers (id TEXT PRIMARY KEY,title TEXT,category TEXT,fit INTEGER,salary TEXT,why TEXT,skills TEXT,outlook TEXT,discipline TEXT,education_cost INTEGER DEFAULT 0,market_demand INTEGER DEFAULT 0,growth_score INTEGER DEFAULT 0,salary_score INTEGER DEFAULT 0,geographic_demand TEXT DEFAULT 'Moderate',education_path TEXT DEFAULT '',exam_options TEXT DEFAULT '',career_domain TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS opportunities (id TEXT PRIMARY KEY,title TEXT,org TEXT,type TEXT,location TEXT,deadline TEXT,tags TEXT);
        CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY,name TEXT,email TEXT,age INTEGER,grade TEXT,location TEXT,interests TEXT NOT NULL DEFAULT '[]',constraints TEXT NOT NULL DEFAULT '[]',education_cost INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS parents (id TEXT PRIMARY KEY,student_id TEXT,name TEXT,email TEXT,budget INTEGER DEFAULT 0,priorities TEXT NOT NULL DEFAULT '[]');
        CREATE TABLE IF NOT EXISTS assessments (id INTEGER PRIMARY KEY AUTOINCREMENT,student_id TEXT,answers TEXT NOT NULL,signal_strength INTEGER,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        """)
        career_columns = [row[1] for row in con.execute("PRAGMA table_info(careers)").fetchall()]
        for name, definition in {
            "discipline": "TEXT DEFAULT 'Technology'", "education_cost": "INTEGER DEFAULT 0",
            "market_demand": "INTEGER DEFAULT 0", "growth_score": "INTEGER DEFAULT 0",
            "salary_score": "INTEGER DEFAULT 0", "geographic_demand": "TEXT DEFAULT 'Moderate'",
            "education_path": "TEXT DEFAULT ''", "exam_options": "TEXT DEFAULT ''",
            "career_domain": "TEXT DEFAULT ''",
        }.items():
            if name not in career_columns:
                con.execute(f"ALTER TABLE careers ADD COLUMN {name} {definition}")
        student_columns = [row[1] for row in con.execute("PRAGMA table_info(students)").fetchall()]
        for name, definition in {"age": "INTEGER", "location": "TEXT", "education_cost": "INTEGER DEFAULT 0"}.items():
            if name not in student_columns:
                con.execute(f"ALTER TABLE students ADD COLUMN {name} {definition}")
        parent_columns = [row[1] for row in con.execute("PRAGMA table_info(parents)").fetchall()]
        if "budget" not in parent_columns:
            con.execute("ALTER TABLE parents ADD COLUMN budget INTEGER DEFAULT 0")
        con.executemany("""INSERT INTO careers
            (id,title,category,fit,salary,why,skills,outlook,discipline,education_cost,market_demand,growth_score,salary_score,geographic_demand,education_path,exam_options,career_domain)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET title=excluded.title,category=excluded.category,fit=excluded.fit,salary=excluded.salary,why=excluded.why,skills=excluded.skills,outlook=excluded.outlook,discipline=excluded.discipline,education_cost=excluded.education_cost,market_demand=excluded.market_demand,growth_score=excluded.growth_score,salary_score=excluded.salary_score,geographic_demand=excluded.geographic_demand,education_path=excluded.education_path,exam_options=excluded.exam_options,career_domain=excluded.career_domain""", CAREERS)
        con.executemany("INSERT OR IGNORE INTO opportunities VALUES (?,?,?,?,?,?,?)", OPPORTUNITIES)
        con.execute("""INSERT INTO students(id,name,email,age,grade,location,interests,constraints,education_cost)
            VALUES ('demo-student','Arun Kumar','arun@example.test',12,'12','Chennai','[]','[]',0)
            ON CONFLICT(id) DO UPDATE SET name='Arun Kumar',email='arun@example.test',age=12,grade='12',location='Chennai'""")
        con.execute("""INSERT INTO parents(id,student_id,name,email,budget,priorities)
            VALUES ('demo-parent','demo-student','Arun Kumar Family','family@example.test',200000,'["Affordability","Career stability"]')
            ON CONFLICT(id) DO UPDATE SET student_id='demo-student',budget=200000,priorities='["Affordability","Career stability"]'""")

def rows(table: str) -> list[dict[str, Any]]:
    with connect() as con:
        return [dict(row) for row in con.execute(f"SELECT * FROM {table}").fetchall()]

def get_career(career_id: str) -> dict[str, Any] | None:
    resolved_id = CAREER_ALIASES.get(career_id, career_id)
    with connect() as con:
        row = con.execute("SELECT * FROM careers WHERE id=?", (resolved_id,)).fetchone()
    return dict(row) if row else None

def get_student(student_id: str = "demo-student") -> dict[str, Any]:
    with connect() as con:
        row = con.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        if not row:
            con.execute("INSERT INTO students(id,name,email,age,grade,location) VALUES (?,?,?,?,?,?)", (student_id, "Arun Kumar", "arun@example.test", 12, "12", "Chennai"))
            con.commit()
            row = con.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        result = dict(row)
    for key in ("interests", "constraints"):
        result[key] = json.loads(result[key] or "[]")
    return result

def save_student(payload: dict[str, Any]) -> dict[str, Any]:
    student_id = payload.get("id", "demo-student")
    with connect() as con:
        con.execute("""INSERT INTO students(id,name,email,age,grade,location,interests,constraints,education_cost) VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(id) DO UPDATE SET name=excluded.name,email=excluded.email,age=excluded.age,grade=excluded.grade,location=excluded.location,interests=excluded.interests,constraints=excluded.constraints,education_cost=excluded.education_cost""",
                    (student_id, payload.get("name", "Arun Kumar"), payload.get("email", ""), payload.get("age", 12), payload.get("grade", "12"), payload.get("location", "Chennai"),
                     json.dumps(payload.get("interests", [])), json.dumps(payload.get("constraints", [])), payload.get("education_cost", 0)))
        con.commit()
    return get_student(student_id)

def save_parent(payload: dict[str, Any]) -> dict[str, Any]:
    with connect() as con:
        con.execute("""INSERT INTO parents(id,student_id,name,email,budget,priorities) VALUES (?,?,?,?,?,?)
        ON CONFLICT(id) DO UPDATE SET student_id=excluded.student_id,name=excluded.name,email=excluded.email,budget=excluded.budget,priorities=excluded.priorities""",
                    (payload.get("id", "demo-parent"), payload.get("student_id", "demo-student"), payload.get("name", "Alex Chen"),
                     payload.get("email", ""), payload.get("budget", 0), json.dumps(payload.get("priorities", []))))
        con.commit()
        row = con.execute("SELECT * FROM parents WHERE id=?", (payload.get("id", "demo-parent"),)).fetchone()
    result = dict(row)
    result["priorities"] = json.loads(result["priorities"])
    return result
