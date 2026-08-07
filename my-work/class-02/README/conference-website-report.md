# GCP Tech Summit 2026 — Conference Web App

This report documents the web application served by Flask, its data constraints, API specifications, and styling.

---

## 📡 REST API Specifications

The backend serves static HTML templates and exposes REST endpoints for schedule filtering:

### 1. Main UI Page
* **Route**: `GET /`
* **Template**: `templates/index.html`
* **Response**: Main layout populated with static conference metadata and talk entries.

### 2. Search & Filter Endpoint
* **Route**: `GET /api/talks`
* **Query Parameters**:
  - `q` (string): Search query matching titles, descriptions, speaker names, or companies.
  - `category` (string): Filter by talk category chip.
  - `speaker` (string): Filter by individual speaker.
* **Response Format**: `application/json` array of talk dictionaries matching constraints:
  ```json
  [
    {
      "id": 1,
      "title": "Scaling Gemini LLMs on GKE Autopilot",
      "speakers": [
        {
          "first_name": "Dr. Sarah",
          "last_name": "Chen",
          "role": "Principal AI Architect",
          "company": "Google",
          "linkedin": "https://linkedin.com/in/sarah-chen"
        }
      ],
      "categories": ["AI/ML", "Containers"],
      "description": "Deep dive into orchestration patterns for low-latency inference...",
      "time": "09:00 AM - 10:00 AM"
    }
  ]
  ```

---

## 🏗️ Architectural Rules & Constraints

The application enforces specific structural guidelines verified by unit tests:

1. **Schedule Cap**: Contains exactly **10 technical talks** covering Google Cloud technologies.
2. **Speaker Constraints**: Every talk must have **1 or 2 speakers** (no empty speakers lists, no more than 2).
3. **Mid-Day Break**: A mandatory **60-minute Lunch & Networking Break** must be scheduled from `12:00 PM` to `01:00 PM`.
4. **Speaker Profiles**: Every speaker must have a validated LinkedIn URL structure.

---

## 🎨 GCP Summit Visual Design & Aesthetic

The frontend utilizes a dark technical styling inspired by Google Cloud Next:
- **HSL Color Variables**: Palette tailored around slate blues (`#080b11`), clean blues, and bright accents for category chips.
- **Glassmorphic Cards**: Talk items are enclosed in borders with a high-contrast hover state and backdrop filter blur.
- **Responsive Schedule Timetable**: Interactive grids that scale for mobile, highlighting the mid-day lunch break in custom amber styling.
- **Details Modal Dialog**: Transition animations for opening/closing detailed speaker profiles.
