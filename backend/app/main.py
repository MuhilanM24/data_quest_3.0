from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AliasChoices, BaseModel, Field
from .db import init_db, rows, get_student, get_career, save_student, save_parent
from .engine import conflict_analysis, solve_financial_budget, recommendations, recommendations_for_student, career_dna, roadmap_for

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield

app = FastAPI(title="PRISM Engine API", version="0.2.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ConflictRequest(BaseModel):
    student: str = Field(min_length=1, validation_alias=AliasChoices("student", "student_input"))
    parent: str = Field(min_length=1, validation_alias=AliasChoices("parent", "parent_input"))
class BudgetRequest(BaseModel):
    tuition: float = Field(default=0, ge=0, validation_alias=AliasChoices("tuition", "education_cost"))
    aid: float = Field(default=0, ge=0, validation_alias=AliasChoices("aid", "scholarship"))
    living: float = Field(default=0, ge=0, validation_alias=AliasChoices("living", "living_cost"))
    years: int = Field(default=4, ge=1, le=10)
    family_budget: float = Field(default=0, ge=0, validation_alias=AliasChoices("family_budget", "annual_budget", "budget", "parent_budget"))
    career_id: str | None = None
class StudentRequest(BaseModel):
    id: str = Field(default="demo-student", min_length=1); name: str = Field(default="Arun Kumar", min_length=1)
    email: str = ""; age: int = Field(default=12, ge=1, le=100); grade: str = "12"
    location: str = Field(default="Chennai", validation_alias=AliasChoices("location", "city"))
    interests: list[str] = []; constraints: list[str] = []; education_cost: float = Field(default=0, ge=0)
class ParentRequest(BaseModel):
    id: str = Field(default="demo-parent", min_length=1); student_id: str = "demo-student"; name: str = Field(default="Alex Chen", min_length=1)
    email: str = ""; budget: float = Field(default=0, ge=0, validation_alias=AliasChoices("budget", "family_budget", "annual_budget", "parent_budget")); priorities: list[str] = []
class MentorRequest(BaseModel):
    student_id: str = "demo-student"; career_id: str = "product"; message: str = Field(default="I would like guidance.", min_length=1)
class AnswersRequest(BaseModel):
    answers: list[str] = Field(default_factory=list, max_length=30)

@app.get("/health")
def health(): return {"status": "ok", "engine": "deterministic"}
@app.get("/api/careers")
def careers():
    result = rows("careers")
    for item in result: item["skills"] = item["skills"].split(",")
    return result
@app.get("/api/careers/{career_id}")
def career(career_id: str):
    item = get_career(career_id)
    if item:
        item["skills"] = item["skills"].split(",")
    if not item: raise HTTPException(status_code=404, detail="Career not found")
    return item
@app.get("/api/opportunities")
def opportunities():
    result = rows("opportunities")
    for item in result: item["tags"] = item["tags"].split(",")
    return result
@app.get("/api/market")
def market():
    return {"updated": "October 2026", "sectors": [{"name": "Technology", "growth": 18, "signal": "Hiring for adaptable builders"}, {"name": "Science", "growth": 14, "signal": "More climate and health investment"}, {"name": "Engineering", "growth": 12, "signal": "Infrastructure meets automation"}], "note": "Seeded local signals for demo exploration."}
@app.get("/api/roadmap")
def roadmap(career_id: str = "product"): return roadmap_for(career_id)
@app.get("/api/mentors")
def mentors(): return [{"id": "m1", "name": "Jordan Kim", "role": "Product design · 7 yrs", "initials": "JK", "focus": "Portfolio storytelling"}, {"id": "m2", "name": "Samira Patel", "role": "Climate data · 5 yrs", "initials": "SP", "focus": "Science and impact careers"}, {"id": "m3", "name": "Alex Rivera", "role": "Creative technology · 9 yrs", "initials": "AR", "focus": "First projects and confidence"}]
@app.get("/api/student")
def student(student_id: str = "demo-student"): return get_student(student_id)
@app.post("/api/student")
def student_save(payload: StudentRequest): return save_student(payload.model_dump())
@app.post("/api/students")
def students_save(payload: StudentRequest): return save_student(payload.model_dump())
@app.get("/api/students/{student_id}")
def student_by_id(student_id: str): return get_student(student_id)
@app.post("/api/parent")
def parent_save(payload: ParentRequest): return save_parent(payload.model_dump())
@app.post("/api/parents")
def parents_save(payload: ParentRequest): return save_parent(payload.model_dump())
@app.get("/api/parents/{parent_id}")
def parent_by_id(parent_id: str):
    item = next((p for p in rows("parents") if p["id"] == parent_id), None)
    if not item: raise HTTPException(status_code=404, detail="Parent not found")
    import json
    item["priorities"] = json.loads(item["priorities"] or "[]")
    return item
@app.post("/api/analyze/conflict")
def analyze_conflict(request: ConflictRequest): return conflict_analysis(request.student, request.parent)
@app.post("/api/solve/financial")
def solve_financial(request: BudgetRequest):
    return solve_financial_budget(request.tuition, request.aid, request.living, request.years, request.family_budget, request.career_id)
@app.post("/api/financial/check")
def financial_check(request: BudgetRequest):
    return solve_financial_budget(request.tuition, request.aid, request.living, request.years, request.family_budget, request.career_id)
@app.post("/api/assessment")
def assessment(payload: AnswersRequest):
    answers = payload.answers
    return {"completed": True, "signal_strength": min(99, 70 + len(answers) * 4), "next_step": "Try one small experiment this week.", "dna": career_dna(answers), "recommendations": recommendations(answers)["matches"]}
@app.post("/api/recommendations")
def recommend(payload: AnswersRequest = AnswersRequest()): return recommendations(payload.answers)
@app.post("/api/recommendations/{student_id}")
def recommend_for_student(student_id: str, payload: AnswersRequest = AnswersRequest()):
    return recommendations_for_student(student_id, payload.answers)
@app.post("/api/career-dna")
def dna(payload: AnswersRequest = AnswersRequest()): return career_dna(payload.answers)
@app.get("/api/career-dna/{student_id}")
def dna_for_student(student_id: str):
    student = get_student(student_id)
    return career_dna(student.get("interests", []))
@app.post("/api/conflict")
def conflict_alias(request: ConflictRequest): return conflict_analysis(request.student, request.parent)
@app.get("/api/market/{career_id}")
def market_for_career(career_id: str):
    item = get_career(career_id)
    if not item: raise HTTPException(status_code=404, detail="Career not found")
    return {"career_id": career_id, "market_demand": item["market_demand"], "growth_score": item["growth_score"], "salary_score": item["salary_score"], "geographic_demand": item["geographic_demand"]}
@app.get("/api/roadmap/{career_id}")
def roadmap_for_career(career_id: str): return roadmap_for(career_id)
@app.post("/api/mentor")
def mentor(request: MentorRequest):
    mentors_list = mentors()
    mentor_item = mentors_list[0] if request.career_id in {"product", "ui-ux-designer"} else mentors_list[1 if request.career_id in {"data", "data-scientist", "climate", "renewable-energy-engineer", "environment", "environmental-data-analyst"} else 2]
    return {"status": "requested", "mentor": mentor_item, "student_id": request.student_id, "career_id": request.career_id, "message": request.message}
