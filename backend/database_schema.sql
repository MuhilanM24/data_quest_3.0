-- SQLite demo schema. This is the local fallback for the hosted Supabase schema.
CREATE TABLE IF NOT EXISTS careers (
  id TEXT PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, fit INTEGER NOT NULL,
  salary TEXT NOT NULL, why TEXT NOT NULL, skills TEXT NOT NULL, outlook TEXT NOT NULL,
  discipline TEXT NOT NULL DEFAULT 'Technology', education_cost INTEGER NOT NULL DEFAULT 0,
  market_demand INTEGER NOT NULL DEFAULT 0, growth_score INTEGER NOT NULL DEFAULT 0,
  salary_score INTEGER NOT NULL DEFAULT 0, geographic_demand TEXT NOT NULL DEFAULT 'Moderate',
  education_path TEXT NOT NULL DEFAULT '', exam_options TEXT NOT NULL DEFAULT '',
  career_domain TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS opportunities (
  id TEXT PRIMARY KEY, title TEXT NOT NULL, org TEXT NOT NULL, type TEXT NOT NULL,
  location TEXT NOT NULL, deadline TEXT NOT NULL, tags TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS students (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, age INTEGER,
  grade TEXT, location TEXT, interests TEXT NOT NULL DEFAULT '[]',
  constraints TEXT NOT NULL DEFAULT '[]', education_cost INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS parents (
  id TEXT PRIMARY KEY, student_id TEXT NOT NULL, name TEXT NOT NULL, email TEXT NOT NULL,
  budget INTEGER NOT NULL DEFAULT 0, priorities TEXT NOT NULL DEFAULT '[]'
);
CREATE TABLE IF NOT EXISTS assessments (
  id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL, answers TEXT NOT NULL,
  signal_strength INTEGER, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_opportunities_deadline ON opportunities(deadline);
CREATE INDEX IF NOT EXISTS idx_assessments_student ON assessments(student_id);
