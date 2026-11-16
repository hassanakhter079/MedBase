# 🩺 MedBase — AMBOSS-Style Clinical Knowledge Library

> **A high-density, interactive clinical decision support and study application inspired by AMBOSS.**  
> Built as a single-page standalone web application with zero external runtime dependencies, 100% offline capability, responsive mobile/tablet layout, tactile embossed cards, and Universal GitHub Cloud Sync.

---

## 🌐 Live Web Application
- **Live URL:** https://hassanakhter079.github.io/MedBase/
- **Architecture:** Zero-dependency standalone HTML5, CSS3, vanilla JavaScript engine, and SVG icon suite.
- **Offline / On-Device:** Compatible with Android WebView, HotPages container, WebCraft container, Safari, Chrome, and Firefox.

---

## ✨ Features & Capabilities

### 1. 3-Column Clinical Workspace
- **Top Sticky Utility Bar:**
  - **Global Command Search (`Ctrl+K` / `⌘K`):** Real-time fuzzy index search across articles, subsections, clinical glossary terms, and calculators.
  - **⚡ High-Yield Mode:** Dynamically filters secondary theory and low-yield paragraphs, revealing an active banner showing hidden count.
  - **🖍️ Key Exam Highlights:** Toggles yellow/amber highlights on critical buzzwords, pathognomonic findings, and diagnostic thresholds (`[[hl:...]]`).
  - **❓ Quiz / Blank Mode:** Obscures high-yield exam terms into clickable blurred pills (`blur(5px)`); tapping reveals the term with a live progress tracker (`Revealed X / Y`), "Reveal All", and "Reset".
  - **🚨 On-Duty / ER Mode:** One-click acute mode that collapses pathophysiology and background etiology while automatically expanding emergency diagnostics, resuscitation protocols, and drug prescription tables.
  - **🌓 Theme Engine:** High-contrast Dark Mode (midnight slate `#0b1120` / `#111827`) and Day/Light Mode (slate-white `#f4f6f9`), saved in `localStorage` under `dod_theme`.
- **Left Sidebar:**
  - **Article Outline:** Active scrollspy that tracks section reading progress and enables 1-click jumps.
  - **Library Tree:** Multi-level folder navigation across medical specialties (Internal Medicine > Cardiology, Pulmonology, Endocrinology).
- **Center Article Area:**
  - Breadcrumb navigation, metadata pills (update timestamp, reading time, shelf exam tags).
  - Tactile, slightly embossed collapsible cards with 12px rounded corners and smooth hover elevation.
  - 3-level nested bullet hierarchies (discs, circles, squares).
  - Comparison tables with zebra striping and sticky headers.
  - **Color-Coded Callout Boxes:**
    - 🟡 **Clinical Pearl / High-Yield** (Amber/Gold border & tint)
    - 🔴 **Red Flag / Emergency Contraindication** (Crimson/Rose border & tint)
    - 🟢 **Pakistani Brand Rx / Pharmacotherapy** (Emerald/Green border & monospace badges)
    - 🔵 **Diagnostic Algorithm** (Ocean Blue/Cyan border & tint)
  - **Clinical Photo & Figure Gallery:** Embedded high-resolution clinical images, interactive "+ Upload / Preview" local file slot, and fullscreen Lightbox modal.
- **Right Contextual Sidebar:**
  - **🧮 Interactive Calculators:**
    - **HEART Score (ACS):** Dynamic calculation of History, ECG, Age, Risk Factors, and Troponin with 6-week MACE percentage.
    - **CURB-65 (CAP):** Dynamic pneumonia severity scoring with 30-day mortality risk and disposition guidance.
  - **🩺 Clinical Vignette Qbank:** USMLE Step 2 CK board-style clinical scenarios with distractor elimination pencil (✏️), instant feedback, and detailed explanations for every option.
  - **📝 Clinical Scratchpad (My Notes):** Auto-saving bedside notes persisted to local storage and synced to cloud.

### 2. Universal GitHub Cloud Sync
Includes automatic cloud synchronization via:
```html
<script src="https://hassanakhter079.github.io/After-Salah-Zikr/cloud-sync.js" data-app="amboss-clinical-guide"></script>
```
All reading progress, scratchpad notes, quiz reveals, and theme preferences sync across phone, tablet, and PC automatically via GitHub Gist.

---

## 💾 Storage & Scalability: Notes & Images

| Category | Storage Location | Capacity & Scale |
| :--- | :--- | :--- |
| **Clinical Notes & Text** | Embedded in `index.html` / `data/` | Easily stores thousands of pages of notes without lag (< 10 MB). |
| **Permanent Clinical Images** | `img/` directory on GitHub | GitHub repos comfortably hold up to 1 GB (1,000+ compressed images). |
| **Interactive Photos (On Duty)** | Browser memory / Base64 preview | Immediate zero-latency bedside preview on phone/tablet. |
| **User State & Scratchpad** | `localStorage` + GitHub Gist | Auto-persists across devices without manual export. |

---

## 📂 Project Structure
```
medbase/
├── index.html              # Main standalone AMBOSS-style web application (root)
├── medbase.html            # Standalone distribution copy
├── .nojekyll               # Disables Jekyll processing on GitHub Pages
├── build_standalone.py     # Reproducible HTML generator script
├── data/
│   └── medbase_data.json   # Extracted clinical knowledge base
├── img/                    # High-resolution clinical images & diagnostic scans
│   ├── acs_ecg.jpg
│   ├── cap_cxr.jpg
│   ├── dka_algorithm.jpg
│   └── hf_echo.jpg
└── README.md
```

---

_Authored for Dr. Hassan Akhtar — Clinical Knowledge & Decision Support._
