# GCP Tech Summit 2026 - System Architecture

This document describes the software architecture, design patterns, and data flow of the Google Cloud Tech Summit 2026 web application.

---

## 1. System Overview

The application is a lightweight, high-performance 1-day technical conference informational site built on a decoupled client-server architecture:

```
                  +-----------------------------------+
                  |          Client (Browser)         |
                  |  Vanilla HTML5 / CSS3 / ES6 JS    |
                  +-----------------+-----------------+
                                    |
                                    | HTTP / REST API (JSON)
                                    v
                  +-----------------+-----------------+
                  |          Server (Python)          |
                  |          Flask Framework          |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  |      In-Memory Data Models        |
                  |    CONFERENCE_INFO, TALKS,        |
                  |            SPEAKERS               |
                  +-----------------------------------+
```

---

## 2. Directory Structure

```
conference-website/
├── app.py                  # Server application entry point & API routes
├── test_app.py             # Automated unit testing suite
├── README.md               # Quick start & project summary
├── docs/                   # Detailed documentation suite
│   ├── ARCHITECTURE.md     # System architecture & component design
│   ├── API_SPECIFICATION.md# REST API documentation
│   └── DEVELOPER_GUIDE.md  # Developer & deployment handbook
├── templates/
│   └── index.html          # Server-rendered HTML shell & modal template
└── static/
    ├── css/
    │   └── style.css       # Design system, CSS variables, dark mode styling
    └── js/
        └── app.js          # Client-side state, API fetching, DOM rendering
```

---

## 3. Core Components

### 3.1 Server Backend (`app.py`)
- **Framework**: Flask (Python)
- **Role**: Serves the index HTML page and provides REST API JSON endpoints for talks, categories, speakers, and event metadata.
- **Hydration Logic**: The `get_hydrated_talks()` helper joins speaker IDs in `TALKS` with the full `SPEAKERS` dictionary before serving API payloads.

### 3.2 Frontend UI (`static/css/style.css`, `templates/index.html`)
- **Theme**: Dark tech aesthetic inspired by Google Cloud Next & Material Design, featuring HSL color variables (`#4285F4`, `#EA4335`, `#FBBC04`, `#34A853`), glassmorphism backdrop filters, and custom scrollbars.
- **Typography**: Inter (body text) & Outfit (display headers) via Google Fonts.

### 3.3 Client State & Logic (`static/js/app.js`)
- **State Object**:
  ```js
  let state = {
      talks: [],
      categories: [],
      speakers: [],
      lunchBreak: null,
      selectedCategory: '',
      selectedSpeaker: '',
      searchQuery: ''
  };
  ```
- **Asynchronous Fetching**: Fetch API executes asynchronous requests to `/api/categories`, `/api/speakers`, and `/api/talks`.
- **Debounced Search**: Text search input incorporates a 300ms debounce timer to prevent redundant API queries during rapid keypresses.

---

## 4. Sequence Diagram (Data Flow)

```
User               Browser (app.js)            Server (app.py)
 |                        |                           |
 |--- Access Website ---->|                           |
 |                        |--- GET / ---------------->|
 |                        |<-- 200 OK (index.html) ---|
 |                        |                           |
 |                        |--- GET /api/categories -->|
 |                        |<-- 200 OK (JSON) ---------|
 |                        |                           |
 |                        |--- GET /api/speakers ----->|
 |                        |<-- 200 OK (JSON) ---------|
 |                        |                           |
 |                        |--- GET /api/talks ------->|
 |                        |<-- 200 OK (JSON) ---------|
 |                        |                           |
 |<-- Renders Timetable --|                           |
 |                        |                           |
 |-- Filter/Search input->|                           |
 |                        |--- GET /api/talks?q=... ->|
 |                        |<-- 200 OK (JSON) ---------|
 |<-- Re-renders Schedule-|                           |
```
