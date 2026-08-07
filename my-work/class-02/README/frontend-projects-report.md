# Frontend Web Applications — Aesthetics & UI Engineering

This report covers the design architecture, styling languages, and script modularity of the two static frontend projects in Class 02.

---

## 📈 1. Finviz Market Intelligence Dashboard (`news-highlights`)

Located at `my-work/class-02/news-highlights/index.html`, this dashboard combines financial metrics with news intelligence.

### 🎨 Visual & Aesthetic Design
- **Grid Layout**: Dual-column container separating market movers (tickers) from news highlights.
- **Glassmorphism Panels**: Uses `rgba` backgrounds, thin semi-transparent borders, and backdrop-filter blurs to float elements over a dark space-inspired background.
- **Sentiment Indicators**: News articles feature indicator tags colored dynamically (Green: bullish, Red: bearish, Gray: neutral) with custom glows (`box-shadow: 0 0 12px var(--green-glow)`).
- **Typography**: Paired heavy headers (`Outfit` font) with monospaced ticker lists (`JetBrains Mono`).

---

## ⏱️ 2. AuraFocus Mindful Productivity Suite (`pomodoro-timer`)

Located at `my-work/class-02/pomodoro-timer/`, this application showcases modular script design, complex CSS theme switching, and ambient SVG micro-animations.

### 🧩 Modular JavaScript Engine (`js/`)
The JS files are divided by capability:
- **`app.js`**: Core page event listener, tab selector manager, and initial setup.
- **`timer.js`**: Controls the Pomodoro clock intervals (Focus, Short Break, Long Break) and handles audio/visual triggers.
- **`breathing.js`**: Orchestrates the mindful breathing overlay, pulsing SVG guidance paths, and inhale/exhale timeline loops.
- **`tasks.js`**: Manages the persistent local storage checklist with category tags.
- **`stats.js`**: Renders analytical charts (session counts, focus minutes) using custom SVG bars.
- **`audio.js`**: Integrates ambient soundscapes (white noise, rain, forest, waves) and session completion bells.

### 🌈 Selectable Theme System
AuraFocus stores 5 custom themes using CSS variables assigned to custom attributes on the `<html>` node (`html[data-theme="..."]`):
1. **Sage Forest (`sage`)**: Muted pine greens, offering a grounding, calming environment.
2. **Nordic Fog (`fog`)**: Deep steel blues and slate greys, optimized for concentration.
3. **Sunset Glow (`sunset`)**: Rich purples and warm embers, reducing blue-light exposure in evening sessions.
4. **Deep Midnight (`midnight`)**: High-contrast, pure black and dark indigo hues.
5. **Warm Sand (`sand`)**: Soft terracotta tones for a warm look.
