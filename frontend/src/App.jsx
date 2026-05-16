import { useMemo, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

const defaultSkills = [
  "Python",
  "SQL",
  "Pandas",
  "NumPy",
  "Scikit-learn",
  "Machine Learning",
  "Statistics",
  "Data Preprocessing",
  "Feature Engineering",
  "Model Evaluation",
  "NLP",
  "Docker",
  "Git",
  "FastAPI",
  "AWS",
  "Azure",
  "Power BI",
  "Tableau",
  "XGBoost",
  "Linux",
].join(", ");

const sampleResume = `I am an AI Systems student with experience in Python, SQL, pandas, NumPy, scikit-learn and machine learning. I have built projects for credit card fraud detection, customer segmentation, and NLP text classification. I used logistic regression, random forest, XGBoost, TF-IDF, data preprocessing, feature engineering, model evaluation, precision, recall, F1-score and ROC-AUC. I also have basic experience with Git, Linux, FastAPI and Docker.`;

const sampleJob = `We are looking for a Junior Data Scientist Intern to support data analysis and machine learning projects. The candidate should have knowledge of Python, SQL, pandas, NumPy, scikit-learn and statistics. Experience with machine learning models, data preprocessing, feature engineering and model evaluation is required. Familiarity with NLP, Docker, Git, FastAPI, cloud platforms such as AWS or Azure, and data visualization tools such as Power BI or Tableau would be a plus.`;

function parseSkills(text) {
  return text
    .split(",")
    .map((skill) => skill.trim())
    .filter(Boolean);
}

function ScoreCard({ title, score }) {
  const value = Number.isFinite(Number(score)) ? Number(score) : 0;

  return (
    <div className="score-card">
      <p className="score-title">{title}</p>
      <p className="score-value">{value.toFixed(2)}%</p>

      <div className="progress-bg">
        <div
          className="progress-fill"
          style={{ width: `${Math.max(0, Math.min(100, value))}%` }}
        />
      </div>
    </div>
  );
}

function SkillList({ title, skills, emptyText }) {
  return (
    <div className="result-card">
      <h3>{title}</h3>

      {skills && skills.length > 0 ? (
        <div className="skill-list">
          {skills.map((skill) => (
            <span className="skill-pill" key={skill}>
              {skill}
            </span>
          ))}
        </div>
      ) : (
        <p className="muted">{emptyText}</p>
      )}
    </div>
  );
}

export default function App() {
  const [mode, setMode] = useState("text");
  const [resumeText, setResumeText] = useState(sampleResume);
  const [jobText, setJobText] = useState(sampleJob);
  const [skillsText, setSkillsText] = useState(defaultSkills);
  const [file, setFile] = useState(null);

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const skills = useMemo(() => parseSkills(skillsText), [skillsText]);

  async function analyzeText() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/match`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_text: jobText,
          skills: skills,
        }),
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  async function analyzePdf() {
    if (!file) {
      setError("Please upload a PDF resume first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("job_text", jobText);
      formData.append("skills", skillsText);

      const response = await fetch(`${API_BASE_URL}/match-pdf`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function handleAnalyze() {
    if (mode === "pdf") {
      analyzePdf();
    } else {
      analyzeText();
    }
  }

  return (
    <div className="page">
      <header className="header">
        <p className="badge">FastAPI + NLP Project</p>
        <h1>Resume vs Job Description Matcher</h1>
        <p className="subtitle">
          Compare a resume with a job description, calculate match scores,
          detect matched skills, and show missing skills.
        </p>
      </header>

      <main className="layout">
        <section className="panel">
          <h2>Input</h2>

          <div className="mode-switch">
            <button
              className={mode === "text" ? "active" : ""}
              onClick={() => setMode("text")}
            >
              Resume Text
            </button>

            <button
              className={mode === "pdf" ? "active" : ""}
              onClick={() => setMode("pdf")}
            >
              PDF Resume
            </button>
          </div>

          {mode === "text" ? (
            <div className="field">
              <label>Resume text</label>
              <textarea
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Paste resume text here..."
              />
            </div>
          ) : (
            <div className="field">
              <label>Resume PDF</label>
              <input
                type="file"
                accept="application/pdf"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              {file && <p className="muted">Selected file: {file.name}</p>}
            </div>
          )}

          <div className="field">
            <label>Job description</label>
            <textarea
              value={jobText}
              onChange={(e) => setJobText(e.target.value)}
              placeholder="Paste job description here..."
            />
          </div>

          <div className="field">
            <label>Target skills, comma-separated</label>
            <textarea
              className="skills-area"
              value={skillsText}
              onChange={(e) => setSkillsText(e.target.value)}
              placeholder="Python, SQL, Docker, AWS..."
            />
            <p className="muted">Detected {skills.length} target skills.</p>
          </div>

          {error && <div className="error-box">{error}</div>}

          <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Match"}
          </button>
        </section>

        <section className="results">
          {!result ? (
            <div className="empty-card">
              <h2>Results will appear here</h2>
              <p>
                Submit resume text or upload a PDF resume to receive match
                scores and missing skills.
              </p>
            </div>
          ) : (
            <>
              <div className="scores-grid">
                <ScoreCard title="Final Score" score={result.final_score} />
                <ScoreCard title="Skill Score" score={result.skill_score} />
                <ScoreCard title="TF-IDF Score" score={result.tfidf_score} />
                <ScoreCard title="Semantic Score" score={result.semantic_score} />
              </div>

              <div className="result-card">
                <h3>Suggestion</h3>
                <p>{result.suggestion}</p>
              </div>

              <SkillList
                title="Matched Skills"
                skills={result.matched_skills}
                emptyText="No matched skills found."
              />

              <SkillList
                title="Missing Skills"
                skills={result.missing_skills}
                emptyText="No missing skills found."
              />

              <SkillList
                title="Resume Skills Found"
                skills={result.resume_skills}
                emptyText="No resume skills found."
              />

              <SkillList
                title="Job Skills Found"
                skills={result.job_skills}
                emptyText="No job skills found."
              />
            </>
          )}
        </section>
      </main>
    </div>
  );
}