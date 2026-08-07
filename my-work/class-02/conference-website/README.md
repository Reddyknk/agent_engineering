# GCP Tech Summit 2026 - Google Cloud Technical Conference Site

A modern, high-performance 1-day technical conference web application built with **Python & Flask** on the backend and **vanilla HTML5, modern CSS3, and JavaScript (ES6)** on the frontend.

Designed around a Google Cloud Next inspired dark tech aesthetic with glassmorphic UI elements, dynamic timeline timetable, live search filters, speaker profiles, and modal dialogs.

---

## Features & Functional Highlights

1. **Home Page & Event Metadata**: Displays conference date (`Wednesday, October 14, 2026`), location, stats, and chronological schedule timetable.
2. **10 Technical Talks**: 10 deep-dive sessions focusing on Google Cloud Technologies (Gemini LLMs, GKE Autopilot, Zero-Trust Security, BigQuery & Dataflow, Cloud Run, Cloud Spanner, Terraform, Cloud TPUs/GPUs, Binary Authorization, and Quantum Infrastructure).
3. **1 to 2 Speakers per Talk**: Every talk is hosted by 1 or max 2 industry expert speakers.
4. **Complete Session Schema**: Each talk includes `ID`, `Title`, `Speakers`, `Category` (1 or 2 per talk), `Description`, and `Time`.
5. **Detailed Speaker Metadata**: Speakers include `First Name`, `Last Name`, `Role`, `Company`, and verified `LinkedIn URL`.
6. **Multi-Criteria Search & Filtering**:
   - Real-time instant search input (matches title, description, speaker name, or company).
   - Category filtering via interactive chips.
   - Speaker filtering via dropdown menu.
   - Active filter summary and one-click reset.
7. **60-Minute Lunch & Networking Break**: Clearly highlighted in the middle of the schedule (12:00 PM – 1:00 PM) with custom visual styling.
8. **Interactive Modal Dialogs**: Click any talk card or "View Details" to open a detailed modal view with full session details and speaker contact links.

---

## Complete Project Architecture & File Hierarchy

```
conference-website/
├── app.py                      # Flask server, data models, and RESTful API endpoints
├── test_app.py                 # Automated unit test suite verifying all requirements
├── README.md                   # Primary documentation and setup guide
├── docs/                       # Comprehensive documentation suite
│   ├── ARCHITECTURE.md         # System architecture, sequence diagrams, and design system
│   ├── API_SPECIFICATION.md    # Complete REST API endpoint reference and JSON schemas
│   └── DEVELOPER_GUIDE.md      # Developer handbook, testing guide, and cloud deployment
├── templates/
│   └── index.html              # Main HTML landing page layout and modal markup
└── static/
    ├── css/
    │   └── style.css           # Custom GCP-themed design system, CSS variables & animations
    └── js/
        └── app.js              # Client-side API fetching, debounced search, & modal logic
```

---

## Prerequisites

- **Python 3.8+** (Tested on Python 3.11 / 3.13)
- **Flask 2.x / 3.x**

---

## Quick Setup & Running Locally

1. **Navigate to project folder**:
   ```bash
   cd conference-website
   ```

2. **(Optional) Create and activate a Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Flask**:
   ```bash
   pip install flask
   ```

4. **Run the Flask Development Server**:
   ```bash
   python app.py
   ```
   Access the web application at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## Running Automated Unit Tests

To run the automated test suite verifying all 10 talks, 1-2 speakers constraint, 60-minute lunch break, and search API filters:

```bash
python -m unittest test_app.py -v
```

---

## Detailed Documentation Suite

- 📖 **[System Architecture](docs/ARCHITECTURE.md)**: Breakdown of backend models, frontend state management, CSS tokens, and sequence diagrams.
- 📡 **[REST API Specification](docs/API_SPECIFICATION.md)**: Full API parameters, JSON request/response formats, and endpoint details.
- 🛠️ **[Developer & Deployment Guide](docs/DEVELOPER_GUIDE.md)**: Step-by-step instructions for adding talks/speakers, modifying styles, and deploying to Google Cloud Run or App Engine.

---

## API Summary

- `GET /` : Renders the home page.
- `GET /api/talks` : Returns filtered or complete list of talks + lunch break info.
  - Query parameters: `q`, `category`, `speaker`.
- `GET /api/categories` : Returns list of unique categories.
- `GET /api/speakers` : Returns complete list of speakers.
- `GET /api/info` : Returns top-level conference metadata.
