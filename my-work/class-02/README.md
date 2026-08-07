# Class 02 — Testing, Mocking, and Frontend Engineering

Welcome to the **Class 02** workspace! This folder houses four distinct projects demonstrating backend API development, automated mock testing, dynamic frontends with modern API integrations, and premium web design aesthetics.

---

## Folder Structure

```
my-work/class-02/
├── README.md                      # This master index documentation
├── README/                        # Detailed project reports folder
│   ├── conference-website-report.md
│   ├── mock-tests-report.md
│   └── frontend-projects-report.md
│
├── conference-website/            # 1. Flask backend & GCP summit landing page
│   ├── app.py                     # API endpoints and mock database
│   ├── test_app.py                # Unittest / Pytest suite for API
│   ├── templates/                 # Frontend HTML template
│   └── static/                    # Frontend assets (CSS glassmorphism, JS API calls)
│
├── mock-tests/                    # 2. Automated testing and unit mocking
│   ├── order.py                   # Cart, billing, and checkout logic
│   └── test_order.py              # Pytest suite with MagicMocks
│
├── news-highlights/               # 3. Finviz Market Intelligence Dashboard
│   └── index.html                 # Embedded CSS design system, charts, and articles
│
└── pomodoro-timer/                # 4. AuraFocus Mindful Productivity App
    ├── index.html                 # Main layout & controls
    ├── styles.css                 # Custom HSL design tokens, themes, & keyframes
    └── js/                        # Modular frontend scripts (Timer, Breathe, Tasks, Stats)
```

---

## 🚀 Execution & Verification Summary

### 1. Mock Tests (`mock-tests`)
* **Objective**: Test order checkout logic, cart operations, VIP/Regular discounts, and external mock dependencies (Inventory Service, Payment Gateway).
* **Test Verification**: 21 unit tests executed using `pytest`.
* **Result**: **PASS** (21/21 passed)
* **Command**: `python -m pytest test_order.py`
* **Output**:
  ```
  platform win32 -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0
  collected 21 items
  test_order.py ..................... [100%]
  ============================= 21 passed in 0.06s ==============================
  ```
* 📖 Read the [Mock Tests Report](README/mock-tests-report.md) for logic specs and mocking strategies.

### 2. GCP Tech Summit Website (`conference-website`)
* **Objective**: Serve event metadata, 10 technical talks, speaker lists, search API, and modal dialogs under a GCP-themed dark theme.
* **Test Verification**: 10 REST API and data constraints tests run via `pytest`.
* **Result**: **PASS** (10/10 passed)
* **Command**: `python -m pytest test_app.py`
* **Output**:
  ```
  platform win32 -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0
  collected 10 items
  test_app.py .......... [100%]
  ============================= 10 passed in 0.11s ==============================
  ```
* 📖 Read the [Conference Website Report](README/conference-website-report.md) for route specifications and design systems.

### 3. Market Intelligence Dashboard (`news-highlights`)
* **Objective**: A premium market tracker integrating Finviz-style metrics, sentiment analytics, and custom interactive data panels.
* **Aesthetic**: Nordic space/dark tech palette with custom glassmorphic wrappers, visual sentiment pills, and smooth grid transitions.
* 📖 Read the [Frontend Projects Report](README/frontend-projects-report.md) for design and DOM structures.

### 4. AuraFocus Productivity Suite (`pomodoro-timer`)
* **Objective**: Mindful Pomodoro timer, modular checklists, audio soundscapes, session statistics, and a custom interactive breathing guide.
* **Aesthetic**: Features five gorgeous selectable theme presets (Sage Forest, Nordic Fog, Sunset Glow, Deep Midnight, Warm Sand) with smooth CSS transitions, interactive SVG animations, and ambient particle backgrounds.
* 📖 Read the [Frontend Projects Report](README/frontend-projects-report.md) for details on modular scripts and theme mechanics.

---

## 🛠️ Key Engineering Practices Demonstrated

1. **Strict Mock Isolation**: Employing `unittest.mock.MagicMock` with explicit class `spec` signatures to prevent mock drift and verify external side-effects (e.g. inventory decrements, payment charges) cleanly.
2. **REST API Data Contracts**: Using Flask endpoints responding with typed JSON objects, verified by unit tests (lunch break constraints, 1-2 speakers limits, exact schedule checks).
3. **Advanced CSS Theme Engine**: Storing styling variables inside clean, responsive CSS variables, allowing dynamic themes to apply instantly across the page DOM with custom micro-animations.
