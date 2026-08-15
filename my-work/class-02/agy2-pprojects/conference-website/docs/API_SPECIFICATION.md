# GCP Tech Summit 2026 - REST API Specification

This document provides a detailed reference for all API endpoints exposed by the Flask backend application.

---

## Base URL
`http://127.0.0.1:5000/`

---

## Endpoints

### 1. `GET /`
Renders the primary single-page web interface.

- **Response Header**: `Content-Type: text/html; charset=utf-8`
- **Status Code**: `200 OK`

---

### 2. `GET /api/talks`
Returns a list of scheduled conference sessions and lunch break metadata. Supports filtering via URL query parameters.

#### Query Parameters
| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `q` | `string` | No | Case-insensitive search string matching title, description, speaker name, or company. | `/api/talks?q=Kubernetes` |
| `category` | `string` | No | Filter sessions containing the specified category string. | `/api/talks?category=AI+%26+Machine+Learning` |
| `speaker` | `string` | No | Filter sessions matching a speaker ID or speaker name. | `/api/talks?speaker=spk_1` |

#### Response Schema (`200 OK`)
```json
{
  "total": 10,
  "lunch_break": {
    "title": "Lunch Break & Networking Expo",
    "time": "12:00 PM - 1:00 PM",
    "duration_minutes": 60,
    "description": "Enjoy complimentary gourmet lunch, connect with Google Cloud experts..."
  },
  "talks": [
    {
      "id": 1,
      "title": "Keynote: Next-Gen AI Applications with Gemini & Vertex AI",
      "time": "09:00 AM - 09:45 AM",
      "start_minutes": 540,
      "categories": [
        "AI & Machine Learning"
      ],
      "description": "Discover how enterprise teams are building autonomous AI agents...",
      "speaker_ids": [
        "spk_1",
        "spk_6"
      ],
      "speakers": [
        {
          "id": "spk_1",
          "first_name": "Sundar",
          "last_name": "Ramanathan",
          "role": "Principal AI Architect",
          "company": "Google Cloud",
          "linkedin": "https://www.linkedin.com/in/sundar-ramanathan-gcp"
        },
        {
          "id": "spk_6",
          "first_name": "Priya",
          "last_name": "Sharma",
          "role": "Senior ML Solutions Architect",
          "company": "Vertex AI Labs",
          "linkedin": "https://www.linkedin.com/in/priya-sharma-vertexai"
        }
      ]
    }
  ]
}
```

---

### 3. `GET /api/categories`
Returns a sorted JSON array of all unique categories across all scheduled talks.

#### Response Schema (`200 OK`)
```json
[
  "AI & Machine Learning",
  "App Modernization",
  "Cloud Infrastructure",
  "Data & Analytics",
  "DevOps",
  "Security & Governance"
]
```

---

### 4. `GET /api/speakers`
Returns a JSON array of all featured speakers with their professional metadata and LinkedIn profile URLs.

#### Response Schema (`200 OK`)
```json
[
  {
    "company": "Google Cloud",
    "first_name": "Sundar",
    "id": "spk_1",
    "last_name": "Ramanathan",
    "linkedin": "https://www.linkedin.com/in/sundar-ramanathan-gcp",
    "role": "Principal AI Architect"
  },
  {
    "company": "Enterprise Cloud Systems",
    "first_name": "Elena",
    "id": "spk_2",
    "last_name": "Rostova",
    "linkedin": "https://www.linkedin.com/in/elena-rostova-cloud",
    "role": "Lead Cloud Infrastructure Engineer"
  }
]
```

---

### 5. `GET /api/info`
Returns high-level metadata regarding the conference title, subtitle, date, location, and lunch break details.

#### Response Schema (`200 OK`)
```json
{
  "date": "Wednesday, October 14, 2026",
  "location": "San Francisco Tech Convention Center & Hybrid Live Stream",
  "lunch_break": {
    "description": "Enjoy complimentary gourmet lunch, connect with Google Cloud experts...",
    "duration_minutes": 60,
    "time": "12:00 PM - 1:00 PM",
    "title": "Lunch Break & Networking Expo"
  },
  "subtitle": "Architecting the Future with GenAI, Kubernetes, and Modern Cloud Infrastructure",
  "timezone": "PST (UTC-8)",
  "title": "Google Cloud Tech Summit 2026"
}
```
