"""Deterministic scoring helpers: safe to run without model APIs or network access."""
from typing import Any
from .db import rows, get_student, get_career

def solve_financial_budget(tuition: float, aid: float, living: float, years: int = 4,
                           family_budget: float = 0, career_id: str | None = None):
    career = get_career(career_id) if career_id else None
    if career:
        tuition = float(career.get("education_cost", tuition))
    net = max(0, tuition - aid); annual = net + living
    total = annual * years
    # Seeded career education_cost values are already full-program estimates;
    # ad-hoc tuition inputs retain the solver's existing annual-cost semantics.
    effective_cost = (max(0, tuition - aid) + living * years) if career else total
    budget = max(0, family_budget)
    feasible = not budget or effective_cost <= budget
    remaining_budget = budget - effective_cost if budget else 0
    financial_fit = 100 if not budget else max(0, min(100, round((budget - effective_cost) / budget * 100)))
    risk_level = "Low" if not budget or financial_fit >= 40 else "Moderate" if financial_fit >= 15 else "High"
    return {"annual_cost": annual, "total_cost": total, "monthly_target": round(annual / 12, 2),
            "financial_fit": financial_fit, "feasible": feasible, "effective_cost": effective_cost,
            "remaining_budget": remaining_budget, "risk_level": risk_level,
            "assumptions": ["Aid is applied before living costs.", "Use as a planning estimate, not financial advice."]}

def conflict_analysis(student: str, parent: str):
    creative = "creative" in student.lower() or "explore" in student.lower()
    stable = "stable" in parent.lower() or "safe" in parent.lower()
    return {"score": 72 if creative and stable else 78, "shared": ["Want a fulfilling future", "Care about financial independence"],
            "tensions": ["Speed vs. exploration", "Title vs. transferable skills"],
            "bridge": "Run a low-risk experiment: keep a stable learning path while building creative proof on the side." if creative and stable
            else "Name the shared goal first, then compare options using evidence rather than labels."}

def career_dna(answers: list[Any]):
    text = " ".join(str(a).lower() for a in answers)
    traits = [("Curiosity", 88), ("Empathy", 82), ("Builder energy", 79), ("Systems thinking", 74)]
    if "data" in text or "puzzle" in text: traits[3] = ("Systems thinking", 91)
    return {"headline": "The curious builder", "summary": "You learn by making, asking better questions, and connecting ideas to people.", "traits": [{"name": n, "score": s} for n, s in traits], "confidence": min(96, 68 + len(answers) * 4)}

def recommendations(answers: list[Any]):
    careers = rows("careers")
    dna = career_dna(answers)
    return match_careers(careers, answers, None, None, dna)

def match_careers(careers: list[dict[str, Any]], answers: list[Any], student: dict[str, Any] | None, parent: dict[str, Any] | None, dna: dict[str, Any] | None = None):
    text = " ".join(str(a).lower() for a in answers)
    budget = (parent or {}).get("budget", 0) or 0
    location = ((student or {}).get("location") or "Chennai").lower()
    scored = []
    for career in careers:
        keywords = f"{career['title']} {career['category']} {career['skills']} {career.get('career_domain', '')}".lower()
        interest = min(100, 70 + sum(8 for word in ("design", "build", "data", "science", "system", "creative", "technology") if word in text and word in keywords))
        financial = 100 if not budget or career.get("education_cost", 0) <= budget else max(0, int(budget / max(career.get("education_cost", 1), 1) * 100))
        market = min(100, round((career.get("market_demand", 0) + career.get("growth_score", 0) + career.get("salary_score", 0)) / 3))
        geographic = 90 if location in {"chennai", "india", "remote"} or career.get("geographic_demand") in {"High", "Very high"} else 70
        parent_alignment = 85 if not parent else (90 if career.get("salary_score", 0) >= 80 else 72)
        prism = round(interest * .35 + financial * .25 + market * .2 + parent_alignment * .1 + geographic * .1)
        item = dict(career)
        item.update({"student_fit": interest, "financial_fit": financial, "market_fit": market, "parent_alignment": parent_alignment, "geographic_fit": geographic, "prism_score": prism, "fit": prism})
        item["skills"] = item["skills"].split(",") if isinstance(item["skills"], str) else item["skills"]
        # A hard affordability gate keeps financially infeasible options out of
        # the shortlist; the score remains useful for diagnostics.
        if not budget or career.get("education_cost", 0) <= budget:
            scored.append(item)
    scored.sort(key=lambda c: (-c["prism_score"], c["id"]))
    return {"dna": dna or career_dna(answers), "matches": scored[:5], "explanation": "Deterministic PRISM matches balance student fit, affordability, market demand, parent alignment, and geography."}

def recommendations_for_student(student_id: str, answers: list[Any] | None = None):
    student = get_student(student_id)
    parent = next((p for p in rows("parents") if p["student_id"] == student_id), None)
    answers = answers if answers is not None else student.get("interests", [])
    return match_careers(rows("careers"), answers, student, parent)

def roadmap_for(career_id: str):
    career = get_career(career_id)
    title = career["title"] if career else "your leading match"
    return [{"phase": "01", "title": "Try it", "detail": f"Complete a 90-minute {title} mini-project and interview one practitioner.", "weeks": "Weeks 1–2"},
            {"phase": "02", "title": "Build proof", "detail": "Publish a small case study showing the problem, your process, and what changed.", "weeks": "Weeks 3–6"},
            {"phase": "03", "title": "Get signal", "detail": "Find a mentor, practice your story, and apply to two stretch opportunities.", "weeks": "Weeks 7–10"}]
