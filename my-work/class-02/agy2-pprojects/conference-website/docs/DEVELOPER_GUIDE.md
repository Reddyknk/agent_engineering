# GCP Tech Summit 2026 - Developer & Deployment Guide

This guide provides step-by-step instructions for setting up the local development environment, adding new schedule items, customizing styles, running automated tests, and deploying the application to production cloud environments (Google Cloud Run / App Engine / Docker).

---

## 1. Local Environment Setup

### Prerequisites
- **Python 3.8+**
- **pip** (Python package installer)

### Quick Start Commands
```bash
# Navigate to project directory
cd conference-website

# (Optional) Create virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install Flask dependency
pip install flask

# Start local server in debug mode
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## 2. Running Automated Unit Tests

The project includes an automated test suite using Python's built-in `unittest` module in `test_app.py`.

```bash
python -m unittest test_app.py -v
```

### Test Coverage Checklist
- `test_talk_count`: Verifies total number of talks match schedule length.
- `test_talk_speakers_limit`: Asserts every talk has between 1 and 2 speakers max.
- `test_talk_fields`: Checks presence of required fields (`id`, `title`, `categories`, `description`, `time`, `speaker_ids`).
- `test_speaker_fields`: Checks presence of `first_name`, `last_name`, and valid `linkedin` URL format.
- `test_lunch_break_60_minutes`: Validates 60-minute lunch break requirement.
- `test_index_route`: Validates HTML landing page renders properly.
- `test_api_talks_all`: Validates JSON endpoint output structure.
- `test_api_talks_search_by_category`: Validates category filtering logic.
- `test_api_talks_search_by_speaker`: Validates speaker filtering logic.
- `test_api_talks_search_by_title`: Validates text search query matching.

---

## 3. How to Extend the Application

### Adding a New Talk
In `app.py`, append a dictionary object to the `TALKS` list:

```python
{
    "id": 11,
    "title": "Quantum Computing & Cloud Optimization",
    "time": "05:30 PM - 06:15 PM",
    "start_minutes": 1050,  # 5:30 PM in minutes from midnight (17 * 60 + 30)
    "categories": ["Cloud Infrastructure"],  # 1 or 2 max
    "description": "An introduction to hybrid quantum-classical algorithms on Google Cloud Quantum AI.",
    "speaker_ids": ["spk_1"]  # 1 or 2 max speaker IDs
}
```

### Adding a New Speaker
In `app.py`, add a key-value entry to the `SPEAKERS` dictionary:

```python
"spk_11": {
    "id": "spk_11",
    "first_name": "Alan",
    "last_name": "Turing",
    "role": "Chief Quantum Scientist",
    "company": "Google Quantum AI",
    "linkedin": "https://www.linkedin.com/in/alan-turing-gcp"
}
```

---

## 4. Production Deployment

### Option A: Deploy to Google Cloud Run (Containerized)

1. Create a `Dockerfile` in the project root:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

2. Build & Deploy using Google Cloud CLI (`gcloud`):
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/gcp-tech-summit
gcloud run deploy gcp-tech-summit --image gcr.io/YOUR_PROJECT_ID/gcp-tech-summit --platform managed --region us-central1 --allow-unauthenticated
```

### Option B: Deploy to Google App Engine (GAE)

1. Create an `app.yaml` file:
```yaml
runtime: python311
entrypoint: gunicorn -b :$PORT app:app

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto
```

2. Deploy using `gcloud`:
```bash
gcloud app deploy
```
