export type Career = { id: string; title: string; category: string; fit: number; salary: string; why: string; skills: string[]; outlook: string; discipline?: string; education_cost?: number; market_demand?: number; growth_score?: number; salary_score?: number; geographic_demand?: string; education_path?: string; exam_options?: string; career_domain?: string; student_fit?: number; financial_fit?: number; market_fit?: number; parent_alignment?: number; geographic_fit?: number; prism_score?: number };
export type Opportunity = { id: string; title: string; org: string; type: string; location: string; deadline: string; tags: string[] };
export type Roadmap = { phase: string; title: string; detail: string; weeks: string };
export type Mentor = { id: string; name: string; role: string; initials: string; focus: string };
export type Dna = { headline: string; summary: string; confidence: number; traits: { name: string; score: number }[] };
// In Vercel services mode, the frontend reaches FastAPI through the same-origin
// /api rewrite. Keep the explicit URL override for local development.
const base = process.env.NEXT_PUBLIC_API_URL || "";
const fallbackCareers: Career[] = [
  ["product","Product Designer","Creative technology",94,"$92k–$145k","You translate human needs into useful, beautiful products.","Design research,Prototyping,Storytelling","Very strong","Technology"],
  ["software","Software Engineer","Computing",92,"$105k–$175k","You enjoy turning ideas into systems that work.","Python,JavaScript,Systems thinking","Very strong","Technology"],
  ["data","Data Scientist","Analytics",90,"$96k–$160k","You turn patterns into clear decisions and enjoy asking why.","Python,Statistics,Visualization","Strong","Mathematics"],
  ["robotics","Robotics Engineer","Engineering",87,"$88k–$145k","Your curiosity fits the loop of building, testing, and improving.","CAD,Controls,Electronics","Strong","Engineering"],
  ["biomedical","Biomedical Engineer","Life science",85,"$78k–$125k","You connect science and empathy to make health better.","Biology,Prototyping,Research","Strong","Science"],
  ["climate","Climate Systems Analyst","Impact & science",84,"$71k–$118k","Your values align with work that improves the world at scale.","Systems thinking,GIS,Policy","Strong","Science"],
  ["cybersecurity","Cybersecurity Analyst","Computing",81,"$82k–$140k","You notice risks, ask sharp questions, and protect what matters.","Networks,Threat modeling,Communication","Very strong","Technology"],
  ["architect","Sustainable Architect","Built environment",79,"$70k–$120k","You balance creative vision with constraints and community impact.","Sketching,CAD,Materials","Moderate","Engineering"],
  ["game","Game Developer","Creative technology",78,"$68k–$130k","You combine narrative, logic, and play to create memorable worlds.","Unity,C#,Narrative design","Strong","Technology"],
  ["environment","Environmental Scientist","Earth systems",76,"$58k–$98k","You want evidence-led work that protects people and planet.","Field research,Data analysis,Ecology","Strong","Science"],
].map(([id,title,category,fit,salary,why,skills,outlook,discipline]) => ({ id: String(id), title: String(title), category: String(category), fit: Number(fit), salary: String(salary), why: String(why), skills: String(skills).split(","), outlook: String(outlook), discipline: String(discipline) }));
const fallbackOpps: Opportunity[] = [
  { id:"o1", title:"FutureMakers Design Sprint", org:"Civic Lab", type:"Sprint", location:"Remote", deadline:"Oct 22", tags:["Design","Team"] },
  { id:"o2", title:"AI for Good Fellowship", org:"Northstar Foundation", type:"Fellowship", location:"Hybrid · Boston", deadline:"Nov 4", tags:["AI","Impact"] },
  { id:"o3", title:"Open Data Challenge", org:"DataKind", type:"Challenge", location:"Remote", deadline:"Nov 16", tags:["Data","Portfolio"] },
];
async function get<T>(path: string, fallback: T): Promise<T> { try { const r = await fetch(`${base}${path}`); if (r.ok) return await r.json(); } catch {} return fallback; }
async function post<T>(path: string, body: unknown, fallback: T): Promise<T> { try { const r = await fetch(`${base}${path}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }); if (r.ok) return await r.json(); } catch {} return fallback; }
export const getCareers = () => get<Career[]>("/api/careers", fallbackCareers);
export const getOpportunities = () => get<Opportunity[]>("/api/opportunities", fallbackOpps);
export const getRoadmap = (careerId = "product") => get<Roadmap[]>(`/api/roadmap?career_id=${careerId}`, [
  { phase:"01", title:"Try it", detail:"Complete a 90-minute design sprint and interview one working practitioner.", weeks:"Weeks 1–2" },
  { phase:"02", title:"Build proof", detail:"Publish a case study connecting a real user need to your solution.", weeks:"Weeks 3–6" },
  { phase:"03", title:"Get signal", detail:"Find a mentor, practice your story, and apply to two stretch opportunities.", weeks:"Weeks 7–10" },
]);
export const getMentors = () => get<Mentor[]>("/api/mentors", [{id:"m1",name:"Jordan Kim",role:"Product design · 7 yrs",initials:"JK",focus:"Portfolio storytelling"},{id:"m2",name:"Samira Patel",role:"Climate data · 5 yrs",initials:"SP",focus:"Science and impact careers"},{id:"m3",name:"Alex Rivera",role:"Creative technology · 9 yrs",initials:"AR",focus:"First projects and confidence"}]);
export const submitAssessment = (answers: string[]) => post("/api/assessment", { answers }, { completed:true, signal_strength:84, next_step:"Try one small experiment this week.", dna: fallbackDna, recommendations: fallbackCareers.slice(0,5) });
export const getRecommendations = (answers: string[]) => post<{ dna: Dna; matches: Career[]; explanation: string }>("/api/recommendations", { answers }, { dna:fallbackDna, matches:fallbackCareers.slice(0,5), explanation:"Matches combine your stated interests with transferable STEAM signals." });
export const analyzeConflict = (student: string, parent: string) => post("/api/analyze/conflict", {student,parent}, {score:72,shared:["Want a fulfilling future","Care about financial independence"],tensions:["Speed vs. exploration","Title vs. transferable skills"],bridge:"Run a low-risk experiment: keep a stable learning path while building creative proof on the side."});
export const saveStudent = (payload: unknown) => post("/api/student", payload, payload);
export const saveParent = (payload: unknown) => post("/api/parent", payload, payload);
export const getMarket = () => get("/api/market", {updated:"October 2026",sectors:[{name:"Technology",growth:18,signal:"Hiring for adaptable builders"},{name:"Science",growth:14,signal:"More climate and health investment"},{name:"Engineering",growth:12,signal:"Infrastructure meets automation"}]});
const fallbackDna: Dna = { headline:"The curious builder", summary:"You learn by making, asking better questions, and connecting ideas to people.", confidence:84, traits:[{name:"Curiosity",score:88},{name:"Empathy",score:82},{name:"Builder energy",score:79},{name:"Systems thinking",score:74}] };
export { fallbackCareers as careers, fallbackOpps as opportunities };
