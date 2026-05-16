# Resume vs Job Description Matcher

A web application for comparing a resume with a job description using NLP techniques. The system calculates match scores, extracts skills, identifies missing skills, and provides suggestions for improving the resume.

The project includes a FastAPI backend, a React frontend, and Docker Compose configuration for local containerized execution.

## Features

- Resume and job description comparison
- Text resume input
- PDF resume upload
- Skill extraction from resume and job description
- Matched and missing skills detection
- TF-IDF similarity score
- Semantic similarity score
- Final match score
- Improvement suggestions
- FastAPI backend
- React frontend
- Docker Compose setup

## Project Structure

```text
resume-vs-job-description-matcher/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── preprocessing.py
│   │   ├── skill_extraction.py
│   │   ├── similarity.py
│   │   ├── scoring.py
│   │   └── utils.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── index.html
│   └── Dockerfile
│
|── docker-compose.dev.yml
├── docker-compose.yml
└── README.md
```

## Technologies

Backend:

- Python
- FastAPI
- PyMuPDF
- scikit-learn
- Sentence Transformers
- Uvicorn

Frontend:

- React
- Vite
- JavaScript
- CSS

Infrastructure:

- Docker
- Docker Compose

## How It Works

The application accepts a resume, a job description, and a list of target skills.

The backend:

1. Extracts text from a PDF if a file is uploaded.
2. Cleans and normalizes the text.
3. Extracts skills from the resume and job description.
4. Finds matched and missing skills.
5. Calculates TF-IDF similarity.
6. Calculates semantic similarity.
7. Combines the scores into a final match score.
8. Returns the results to the frontend.

## API Endpoints

### Root

```http
GET /
```

Returns a message confirming that the API is running.

### Match Text Resume

```http
POST /match
```

Example request:

```json
{
  "resume_text": "I have experience with Python, SQL, pandas and machine learning.",
  "job_text": "We are looking for a Data Scientist with Python, SQL, machine learning, Docker and AWS.",
  "skills": [
    "Python",
    "SQL",
    "Pandas",
    "Machine Learning",
    "Docker",
    "AWS"
  ]
}
```

### Match PDF Resume

```http
POST /match-pdf
```

Form fields:

```text
file: PDF resume
job_text: job description text
skills: Python, SQL, Machine Learning, Docker, AWS
```

## Running with Docker Compose

From the project root:

```bash
docker compose up --build
```

Open:

```text
Frontend:
http://127.0.0.1:5173

Backend API docs:
http://127.0.0.1:8000/docs
```

Stop the containers:

```bash
docker compose down
```

## Running Backend Only

```bash
docker build -t resume-matcher-backend ./backend
docker run -p 8000:8000 resume-matcher-backend
```

Backend API docs:

```text
http://127.0.0.1:8000/docs
```

## Running Frontend Only

From the `frontend` directory:

```bash
npm install
npm run dev
```

Frontend:

```text
http://127.0.0.1:5173
```

The backend should also be running on:

```text
http://127.0.0.1:8000
```

## Example Inputs

Skill list:

```text
Python, SQL, Pandas, NumPy, Scikit-learn, Machine Learning, Statistics, Data Preprocessing, Feature Engineering, Model Evaluation, NLP, Docker, Git, FastAPI, AWS, Azure, Power BI, Tableau, XGBoost, Linux
```

Resume text:

```text
I am an AI Systems student with experience in Python, SQL, pandas, NumPy, scikit-learn and machine learning. I have built projects for credit card fraud detection, customer segmentation, and NLP text classification. I used logistic regression, random forest, XGBoost, TF-IDF, data preprocessing, feature engineering, model evaluation, precision, recall, F1-score and ROC-AUC. I also have basic experience with Git, Linux, FastAPI and Docker.
```

Job description:

```text
We are looking for a Junior Data Scientist Intern to support data analysis and machine learning projects. The candidate should have knowledge of Python, SQL, pandas, NumPy, scikit-learn and statistics. Experience with machine learning models, data preprocessing, feature engineering and model evaluation is required. Familiarity with NLP, Docker, Git, FastAPI, cloud platforms such as AWS or Azure, and data visualization tools such as Power BI or Tableau would be a plus.
```

## Scoring

The system calculates:

- Skill score
- TF-IDF similarity score
- Semantic similarity score
- Final combined score

The final score is intended as guidance and should not be treated as an objective hiring decision.

## Limitations

- Skill extraction depends on the provided skill list.
- The system may miss skills written in uncommon formats.
- It does not evaluate years of experience or skill level.
- PDF extraction works best with text-based PDFs.
- Scanned PDFs may require OCR.
- Semantic similarity requires more memory because it uses transformer-based models.

## Deployment Note

The project is containerized and can be run locally with Docker Compose.

The full version uses transformer-based semantic similarity, which may require more memory than some free hosting platforms provide. A lighter deployment version can be created by using only TF-IDF similarity and skill matching.

## Future Improvements

- Add OCR support for scanned PDFs
- Add database storage for previous analyses
- Add DOCX resume upload

## Author

Kirill Postrehan
