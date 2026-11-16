import json
import os
import re

# Load extracted MedBase data
with open("/root/medbase/medbase_data.json", "r", encoding="utf-8") as f:
    med_data = json.load(f)

html_template = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />
  <title>MedBase — AMBOSS Clinical Knowledge Library</title>
  
  <!-- Universal GitHub Cloud Sync Rule -->
  <script src="https://hassanakhter079.github.io/After-Salah-Zikr/cloud-sync.js" data-app="amboss-clinical-guide"></script>

  <!-- Google Fonts Inter & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />

  <style>
    /* ==========================================================================
       1. COLOR SYSTEM & CSS VARIABLES (LIGHT & DARK THEMES)
       ========================================================================== */
    :root {
      --bg-app: #f4f6f9;
      --bg-surface: #ffffff;
      --bg-surface-elevated: #ffffff;
      --bg-surface-subtle: #f8fafc;
      --bg-surface-muted: #edf2f7;
      --border-subtle: #e2e8f0;
      --border-medium: #cbd5e1;
      --border-strong: #94a3b8;
      --text-main: #0f172a;
      --text-soft: #334155;
      --text-muted: #64748b;
      --text-faint: #94a3b8;
      
      --accent-primary: #0284c7;
      --accent-primary-hover: #0369a1;
      --accent-primary-subtle: #e0f2fe;
      
      --card-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 10px 25px -5px rgba(15, 23, 42, 0.04);
      --card-shadow-hover: 0 4px 6px -1px rgba(0,0,0,0.06), 0 16px 32px -4px rgba(15, 23, 42, 0.08);
      --card-emboss: inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 1px 2px rgba(0, 0, 0, 0.04);

      /* Callout Box Colors */
      --pearl-bg: #fffbeb;
      --pearl-border: #f59e0b;
      --pearl-text: #78350f;
      --pearl-badge: #d97706;

      --danger-bg: #fff1f2;
      --danger-border: #f43f5e;
      --danger-text: #881337;
      --danger-badge: #e11d48;

      --rx-bg: #ecfdf5;
      --rx-border: #10b981;
      --rx-text: #064e3b;
      --rx-badge: #059669;

      --diag-bg: #f0f9ff;
      --diag-border: #0ea5e9;
      --diag-text: #0c4a6e;
      --diag-badge: #0284c7;

      /* Highlights & Study */
      --hy-highlight-bg: #fef08a;
      --hy-highlight-text: #713f12;
      --blank-bg: #e2e8f0;
      --blank-border: #cbd5e1;
    }

    [data-theme="dark"] {
      --bg-app: #0b1120;
      --bg-surface: #111827;
      --bg-surface-elevated: #1e293b;
      --bg-surface-subtle: #172033;
      --bg-surface-muted: #1e293b;
      --border-subtle: #1e293b;
      --border-medium: #334155;
      --border-strong: #475569;
      --text-main: #f8fafc;
      --text-soft: #cbd5e1;
      --text-muted: #94a3b8;
      --text-faint: #64748b;

      --accent-primary: #38bdf8;
      --accent-primary-hover: #7dd3fc;
      --accent-primary-subtle: rgba(56, 189, 248, 0.12);

      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
      --card-shadow-hover: 0 8px 30px -4px rgba(0, 0, 0, 0.7);
      --card-emboss: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 1px 2px rgba(0, 0, 0, 0.3);

      /* Callout Box Colors */
      --pearl-bg: rgba(245, 158, 11, 0.08);
      --pearl-border: #f59e0b;
      --pearl-text: #fef3c7;
      --pearl-badge: #fbbf24;

      --danger-bg: rgba(244, 63, 94, 0.08);
      --danger-border: #f43f5e;
      --danger-text: #ffe4e6;
      --danger-badge: #fb7185;

      --rx-bg: rgba(16, 185, 129, 0.08);
      --rx-border: #10b981;
      --rx-text: #d1fae5;
      --rx-badge: #34d399;

      --diag-bg: rgba(14, 165, 233, 0.08);
      --diag-border: #0ea5e9;
      --diag-text: #e0f2fe;
      --diag-badge: #38bdf8;

      /* Highlights & Study */
      --hy-highlight-bg: rgba(250, 204, 21, 0.22);
      --hy-highlight-text: #fef08a;
      --blank-bg: #334155;
      --blank-border: #475569;
    }

    /* ==========================================================================
       2. RESET & BASE TYPOGRAPHY
       ========================================================================== */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
      font-size: 15px;
    }

    body {
      background-color: var(--bg-app);
      color: var(--text-main);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      transition: background-color 0.2s ease, color 0.2s ease;
      min-height: 100vh;
      overflow-x: hidden;
    }

    a {
      color: var(--accent-primary);
      text-decoration: none;
    }

    button {
      font-family: inherit;
      cursor: pointer;
      border: none;
      background: none;
    }

    /* ==========================================================================
       3. AMBOSS EMBOSSED CARDS & ACCORDIONS
       ========================================================================== */
    .amboss-card {
      background-color: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      box-shadow: var(--card-emboss), var(--card-shadow);
      transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.15s ease;
      margin-bottom: 1.25rem;
      overflow: hidden;
    }

    .amboss-card:hover {
      box-shadow: var(--card-emboss), var(--card-shadow-hover);
      border-color: var(--border-medium);
    }

    .accordion-header {
      width: 100%;
      padding: 1rem 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      background: var(--bg-surface);
      border: none;
      text-align: left;
      font-weight: 700;
      font-size: 1.05rem;
      color: var(--text-main);
      cursor: pointer;
      user-select: none;
      transition: background-color 0.15s ease;
    }

    .accordion-header:hover {
      background-color: var(--bg-surface-subtle);
    }

    .accordion-header .title-wrap {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      flex: 1;
    }

    .accordion-header .section-badge {
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.15rem 0.5rem;
      border-radius: 6px;
      background: var(--bg-surface-muted);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
    }

    .chevron-icon {
      transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      color: var(--text-muted);
      flex-shrink: 0;
    }

    .amboss-card.collapsed .chevron-icon {
      transform: rotate(-90deg);
    }

    .amboss-card.collapsed .accordion-body {
      display: none;
    }

    .accordion-body {
      padding: 0.75rem 1.25rem 1.25rem 1.25rem;
      border-top: 1px solid var(--border-subtle);
      background: var(--bg-surface);
    }

    /* Sub-accordions */
    .sub-accordion {
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      margin-top: 0.85rem;
      background: var(--bg-surface-subtle);
      overflow: hidden;
    }

    .sub-accordion-header {
      width: 100%;
      padding: 0.75rem 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-weight: 600;
      font-size: 0.95rem;
      color: var(--text-main);
      cursor: pointer;
      background: var(--bg-surface-subtle);
      border: none;
      text-align: left;
      transition: background-color 0.15s ease;
    }

    .sub-accordion-header:hover {
      background: var(--bg-surface-muted);
    }

    .sub-accordion.collapsed .sub-accordion-body {
      display: none;
    }

    .sub-accordion.collapsed .sub-chevron {
      transform: rotate(-90deg);
    }

    .sub-chevron {
      transition: transform 0.2s ease;
      color: var(--text-muted);
    }

    .sub-accordion-body {
      padding: 0.85rem 1rem;
      border-top: 1px solid var(--border-subtle);
      background: var(--bg-surface);
    }

    /* ==========================================================================
       4. 3-LEVEL NESTED BULLET TREES
       ========================================================================== */
    .bullet-tree {
      list-style: none;
      padding-left: 0;
      margin: 0.5rem 0;
    }

    .bullet-item {
      position: relative;
      padding-left: 1.35rem;
      margin-bottom: 0.45rem;
      line-height: 1.6;
      color: var(--text-soft);
    }

    .bullet-item::before {
      content: "";
      position: absolute;
      left: 0.35rem;
      top: 0.65em;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background-color: var(--accent-primary);
    }

    /* Level 1 nesting */
    .bullet-item > .bullet-tree {
      margin-top: 0.35rem;
      padding-left: 0.5rem;
      border-left: 1px solid var(--border-subtle);
    }

    .bullet-item > .bullet-tree > .bullet-item::before {
      background-color: transparent;
      border: 1.5px solid var(--text-muted);
      width: 5px;
      height: 5px;
    }

    /* Level 2 nesting */
    .bullet-item > .bullet-tree > .bullet-item > .bullet-tree > .bullet-item::before {
      background-color: var(--text-faint);
      border-radius: 1px;
      width: 4px;
      height: 4px;
    }

    /* ==========================================================================
       5. CALLOUT BOXES (PEARL, DANGER, RX, DIAGNOSTIC)
       ========================================================================== */
    .callout-box {
      border-left: 4px solid;
      border-radius: 0 8px 8px 0;
      padding: 0.85rem 1.15rem;
      margin: 0.9rem 0;
      font-size: 0.93rem;
      line-height: 1.6;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .callout-box .callout-head {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 700;
      margin-bottom: 0.35rem;
      font-size: 0.95rem;
    }

    .callout-pearl {
      background: var(--pearl-bg);
      border-color: var(--pearl-border);
      color: var(--pearl-text);
    }
    .callout-pearl .callout-head { color: var(--pearl-badge); }

    .callout-danger {
      background: var(--danger-bg);
      border-color: var(--danger-border);
      color: var(--danger-text);
    }
    .callout-danger .callout-head { color: var(--danger-badge); }

    .callout-rx {
      background: var(--rx-bg);
      border-color: var(--rx-border);
      color: var(--rx-text);
    }
    .callout-rx .callout-head { color: var(--rx-badge); }

    .callout-diagnostic {
      background: var(--diag-bg);
      border-color: var(--diag-border);
      color: var(--diag-text);
    }
    .callout-diagnostic .callout-head { color: var(--diag-badge); }

    /* ==========================================================================
       6. COMPARISON TABLES
       ========================================================================== */
    .table-container {
      width: 100%;
      overflow-x: auto;
      margin: 1rem 0;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      box-shadow: var(--card-emboss);
    }

    .table-caption {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      padding: 0.6rem 0.85rem;
      background: var(--bg-surface-subtle);
      border-bottom: 1px solid var(--border-subtle);
    }

    .amboss-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      text-align: left;
    }

    .amboss-table th {
      background: var(--bg-surface-subtle);
      color: var(--text-main);
      font-weight: 700;
      padding: 0.65rem 0.85rem;
      border-bottom: 2px solid var(--border-medium);
      white-space: nowrap;
    }

    .amboss-table td {
      padding: 0.65rem 0.85rem;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-soft);
      vertical-align: top;
    }

    .amboss-table tr:nth-child(even) {
      background: var(--bg-surface-subtle);
    }

    .amboss-table tr:hover {
      background: var(--bg-surface-muted);
    }

    .amboss-table td:first-child {
      font-weight: 600;
      color: var(--text-main);
      border-right: 1px solid var(--border-subtle);
      background: var(--bg-surface-subtle);
    }

    /* ==========================================================================
       7. STUDY MODES: HIGHLIGHTS, QUIZ / BLANKS, TOOLTIPS, BRAND PILLS
       ========================================================================== */
    /* High-Yield Highlights */
    .hy-mark {
      background: transparent;
      color: inherit;
      transition: background-color 0.15s ease, color 0.15s ease;
    }

    body.highlights-active .hy-mark {
      background: var(--hy-highlight-bg);
      color: var(--hy-highlight-text);
      border-bottom: 2px solid #eab308;
      border-radius: 3px;
      padding: 0 3px;
      margin: 0 -1px;
    }

    /* Quiz / Blank Mode */
    .quiz-blank {
      display: inline-block;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    body.quiz-active .quiz-blank:not(.unblanked) {
      filter: blur(5px);
      user-select: none;
      cursor: pointer;
      background: var(--blank-bg);
      border: 1px solid var(--blank-border);
      border-radius: 4px;
      padding: 0 4px;
      margin: 0 2px;
    }

    body.quiz-active .quiz-blank:not(.unblanked):hover {
      filter: blur(3.5px);
    }

    body.quiz-active .quiz-blank.unblanked {
      filter: none;
      background: var(--accent-primary-subtle);
      border-bottom: 2px solid var(--accent-primary);
      border-radius: 3px;
      padding: 0 3px;
      margin: 0 -1px;
    }

    /* Smart Medical Tooltips */
    .glossary-term {
      text-decoration: underline dotted 1.5px var(--accent-primary);
      text-underline-offset: 3px;
      cursor: pointer;
      font-weight: 500;
      color: var(--accent-primary);
      transition: background-color 0.15s ease;
      border-radius: 3px;
      padding: 0 2px;
    }

    .glossary-term:hover {
      background: var(--accent-primary-subtle);
    }

    /* Pakistani Brand Pills */
    .pk-brand {
      display: inline-flex;
      align-items: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 600;
      padding: 0.15rem 0.5rem;
      border-radius: 9999px;
      background: rgba(16, 185, 129, 0.12);
      color: #059669;
      border: 1px solid rgba(16, 185, 129, 0.25);
      margin: 0 2px;
      white-space: nowrap;
    }

    [data-theme="dark"] .pk-brand {
      background: rgba(16, 185, 129, 0.18);
      color: #34d399;
      border-color: rgba(52, 211, 153, 0.35);
    }

    /* High-Yield Banner */
    .hy-banner {
      display: none;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      background: linear-gradient(90deg, rgba(234, 179, 8, 0.15), rgba(245, 158, 11, 0.15));
      border: 1px solid #f59e0b;
      border-radius: 8px;
      padding: 0.65rem 1rem;
      margin-bottom: 1.25rem;
      font-size: 0.88rem;
      color: var(--text-main);
    }

    body.hy-filter-active .hy-banner {
      display: flex;
    }

    body.hy-filter-active .yield-low {
      display: none !important;
    }

    /* ==========================================================================
       8. MANUAL CLINICAL PHOTO & FIGURE SYSTEM
       ========================================================================== */
    .clinical-figure {
      margin: 1.25rem 0;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      background: var(--bg-surface-subtle);
      overflow: hidden;
      box-shadow: var(--card-emboss);
    }

    .clinical-img-wrap {
      position: relative;
      width: 100%;
      min-height: 180px;
      max-height: 460px;
      background: var(--bg-surface-muted);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      cursor: zoom-in;
    }

    .clinical-img-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.25s ease;
    }

    .clinical-img-wrap:hover img {
      transform: scale(1.02);
    }

    .clinical-caption {
      padding: 0.75rem 1rem;
      font-size: 0.85rem;
      color: var(--text-muted);
      border-top: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }

    .photo-upload-slot {
      margin-top: 0.75rem;
      border: 2px dashed var(--border-medium);
      border-radius: 8px;
      padding: 0.85rem;
      text-align: center;
      background: var(--bg-surface-subtle);
      cursor: pointer;
      transition: border-color 0.2s ease, background 0.2s ease;
      font-size: 0.82rem;
      color: var(--text-muted);
    }

    .photo-upload-slot:hover {
      border-color: var(--accent-primary);
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
    }

    /* ==========================================================================
       9. TOP STICKY UTILITY NAVBAR
       ========================================================================== */
    .top-navbar {
      position: sticky;
      top: 0;
      z-index: 100;
      height: 64px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-subtle);
      box-shadow: 0 1px 4px rgba(0,0,0,0.04);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.25rem;
      gap: 0.75rem;
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.02em;
    }

    .nav-brand .logo-icon {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: linear-gradient(135deg, #0284c7, #0369a1);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
    }

    .search-btn {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.45rem 0.85rem;
      font-size: 0.88rem;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      min-width: 220px;
    }

    .search-btn:hover {
      border-color: var(--border-medium);
      background: var(--bg-surface-muted);
      color: var(--text-main);
    }

    .search-btn .kbd-badge {
      margin-left: auto;
      font-size: 0.72rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 0.1rem 0.35rem;
      font-weight: 600;
      color: var(--text-faint);
    }

    .study-toolbar {
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .tool-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.4rem;
      padding: 0.45rem 0.75rem;
      border-radius: 7px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-soft);
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .tool-btn:hover {
      background: var(--bg-surface-subtle);
      border-color: var(--border-medium);
      color: var(--text-main);
    }

    .tool-btn.active {
      background: var(--accent-primary-subtle);
      border-color: var(--accent-primary);
      color: var(--accent-primary);
    }

    .tool-btn.btn-hy.active {
      background: rgba(234, 179, 8, 0.18);
      border-color: #eab308;
      color: #ca8a04;
    }
    [data-theme="dark"] .tool-btn.btn-hy.active {
      color: #fde047;
    }

    .tool-btn.btn-highlights.active {
      background: rgba(245, 158, 11, 0.18);
      border-color: #f59e0b;
      color: #d97706;
    }

    .tool-btn.btn-quiz.active {
      background: rgba(14, 165, 233, 0.18);
      border-color: #0ea5e9;
      color: #0284c7;
    }

    .tool-btn.btn-er.active {
      background: rgba(244, 63, 94, 0.18);
      border-color: #f43f5e;
      color: #e11d48;
    }

    .icon-only-btn {
      width: 36px;
      height: 36px;
      padding: 0;
      border-radius: 7px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: var(--text-soft);
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      transition: all 0.15s ease;
    }

    .icon-only-btn:hover {
      background: var(--bg-surface-subtle);
      color: var(--text-main);
    }

    /* ==========================================================================
       10. 3-COLUMN WORKSPACE GRID
       ========================================================================== */
    .workspace-grid {
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr) 340px;
      max-width: 1720px;
      margin: 0 auto;
      min-height: calc(100vh - 64px);
    }

    /* Left Sidebar */
    .left-sidebar {
      position: sticky;
      top: 64px;
      height: calc(100vh - 64px);
      overflow-y: auto;
      border-right: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      display: flex;
      flex-direction: column;
    }

    .sidebar-tabs {
      display: flex;
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-surface-subtle);
    }

    .sidebar-tab-btn {
      flex: 1;
      padding: 0.75rem;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      text-align: center;
      border-bottom: 2px solid transparent;
      transition: all 0.15s ease;
    }

    .sidebar-tab-btn.active {
      color: var(--accent-primary);
      border-bottom-color: var(--accent-primary);
      background: var(--bg-surface);
    }

    .sidebar-tab-content {
      padding: 1rem 0.85rem;
      flex: 1;
      overflow-y: auto;
    }

    /* Table of contents outline */
    .toc-item {
      display: block;
      padding: 0.45rem 0.65rem;
      border-radius: 6px;
      font-size: 0.85rem;
      color: var(--text-soft);
      margin-bottom: 0.2rem;
      transition: all 0.15s ease;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .toc-item:hover {
      background: var(--bg-surface-subtle);
      color: var(--text-main);
    }

    .toc-item.active {
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
      font-weight: 600;
    }

    /* Library tree */
    .library-node {
      margin-bottom: 0.35rem;
    }

    .library-node-title {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.4rem 0.5rem;
      border-radius: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-soft);
      cursor: pointer;
    }

    .library-node-title:hover {
      background: var(--bg-surface-subtle);
      color: var(--text-main);
    }

    .library-children {
      padding-left: 1rem;
      border-left: 1px solid var(--border-subtle);
      margin-left: 0.65rem;
      margin-top: 0.2rem;
    }

    .library-article-link {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.4rem;
      padding: 0.4rem 0.5rem;
      border-radius: 6px;
      font-size: 0.82rem;
      color: var(--text-soft);
      cursor: pointer;
      margin-bottom: 0.2rem;
    }

    .library-article-link:hover {
      background: var(--bg-surface-subtle);
      color: var(--text-main);
    }

    .library-article-link.active {
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
      font-weight: 600;
    }

    /* Center Main Article */
    .center-content {
      padding: 2rem 2.5rem;
      max-width: 960px;
      margin: 0 auto;
      width: 100%;
    }

    .article-header {
      margin-bottom: 1.75rem;
    }

    .breadcrumbs {
      display: flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-bottom: 0.6rem;
    }

    .article-title {
      font-size: 2.15rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.2;
      color: var(--text-main);
      margin-bottom: 0.85rem;
    }

    .article-meta-row {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.6rem;
      margin-bottom: 1.25rem;
    }

    .meta-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      background: var(--bg-surface-subtle);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
    }

    .meta-pill.pill-hy {
      background: rgba(234, 179, 8, 0.15);
      color: #ca8a04;
      border-color: rgba(234, 179, 8, 0.3);
    }
    [data-theme="dark"] .meta-pill.pill-hy {
      color: #fde047;
    }

    .article-summary-card {
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--accent-primary);
      border-radius: 0 10px 10px 0;
      padding: 1rem 1.25rem;
      font-size: 0.96rem;
      line-height: 1.65;
      color: var(--text-soft);
      margin-bottom: 1.5rem;
    }

    /* Right Sticky Contextual Sidebar */
    .right-sidebar {
      position: sticky;
      top: 64px;
      height: calc(100vh - 64px);
      overflow-y: auto;
      border-left: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      display: flex;
      flex-direction: column;
    }

    .right-sidebar-body {
      padding: 1.25rem;
      flex: 1;
      overflow-y: auto;
    }

    /* Interactive Calculators */
    .calc-segmented {
      display: flex;
      background: var(--bg-surface-subtle);
      border-radius: 8px;
      padding: 3px;
      margin-bottom: 1.25rem;
      border: 1px solid var(--border-subtle);
    }

    .calc-seg-btn {
      flex: 1;
      padding: 0.45rem;
      font-size: 0.8rem;
      font-weight: 600;
      border-radius: 6px;
      color: var(--text-muted);
      text-align: center;
      transition: all 0.15s ease;
    }

    .calc-seg-btn.active {
      background: var(--bg-surface);
      color: var(--text-main);
      box-shadow: 0 1px 2px rgba(0,0,0,0.06);
    }

    .calc-group {
      margin-bottom: 1rem;
    }

    .calc-group-label {
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-soft);
      margin-bottom: 0.4rem;
      display: block;
    }

    .calc-radio-label {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.82rem;
      color: var(--text-soft);
      padding: 0.35rem 0.5rem;
      border-radius: 6px;
      cursor: pointer;
      margin-bottom: 0.2rem;
    }

    .calc-radio-label:hover {
      background: var(--bg-surface-subtle);
    }

    .calc-result-box {
      border: 1px solid var(--border-medium);
      border-radius: 10px;
      padding: 1rem;
      background: var(--bg-surface-subtle);
      text-align: center;
      margin-top: 1rem;
    }

    .calc-score-num {
      font-size: 2.25rem;
      font-weight: 800;
      line-height: 1;
      color: var(--accent-primary);
      margin-bottom: 0.35rem;
    }

    /* Qbank in Sidebar & Modal */
    .qbank-card {
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 1.15rem;
      background: var(--bg-surface-subtle);
      margin-bottom: 1rem;
    }

    .qbank-stem {
      font-size: 0.92rem;
      line-height: 1.6;
      color: var(--text-main);
      margin-bottom: 1rem;
    }

    .qbank-option {
      display: flex;
      align-items: flex-start;
      gap: 0.65rem;
      padding: 0.65rem 0.85rem;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      margin-bottom: 0.5rem;
      font-size: 0.85rem;
      color: var(--text-soft);
      cursor: pointer;
      transition: all 0.15s ease;
      position: relative;
    }

    .qbank-option:hover {
      border-color: var(--border-medium);
      background: var(--bg-surface-subtle);
    }

    .qbank-option.selected-correct {
      border-color: #10b981;
      background: rgba(16, 185, 129, 0.12);
      color: #065f46;
      font-weight: 600;
    }
    [data-theme="dark"] .qbank-option.selected-correct {
      color: #a7f3d0;
    }

    .qbank-option.selected-wrong {
      border-color: #f43f5e;
      background: rgba(244, 63, 94, 0.12);
      color: #9f1239;
      font-weight: 600;
    }
    [data-theme="dark"] .qbank-option.selected-wrong {
      color: #fecdd3;
    }

    .qbank-option.struck-through {
      text-decoration: line-through;
      opacity: 0.45;
    }

    .strike-btn {
      margin-left: auto;
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
      font-size: 0.72rem;
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
    }
    .strike-btn:hover {
      background: var(--bg-surface-muted);
      color: var(--text-main);
    }

    .qbank-explanation {
      margin-top: 0.85rem;
      padding: 0.85rem;
      border-radius: 8px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      font-size: 0.85rem;
      line-height: 1.55;
    }

    /* Notes Scratchpad */
    .scratchpad-textarea {
      width: 100%;
      min-height: 240px;
      padding: 0.85rem;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface-subtle);
      color: var(--text-main);
      font-family: inherit;
      font-size: 0.88rem;
      line-height: 1.6;
      resize: vertical;
      outline: none;
    }

    .scratchpad-textarea:focus {
      border-color: var(--accent-primary);
      box-shadow: 0 0 0 3px var(--accent-primary-subtle);
    }

    /* ==========================================================================
       11. MODALS & SMART FLOATING TOOLTIP
       ========================================================================== */
    /* Floating Tooltip Popover */
    #tooltip-popover {
      position: fixed;
      z-index: 1000;
      width: 320px;
      max-width: 90vw;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-medium);
      border-radius: 10px;
      box-shadow: 0 20px 35px -5px rgba(0,0,0,0.25);
      padding: 1rem;
      font-size: 0.88rem;
      display: none;
      animation: popoverFadeIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes popoverFadeIn {
      from { opacity: 0; transform: translateY(4px) scale(0.97); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .tooltip-category {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--accent-primary);
      margin-bottom: 0.25rem;
    }

    .tooltip-title {
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 0.45rem;
    }

    .tooltip-desc {
      color: var(--text-soft);
      line-height: 1.55;
      margin-bottom: 0.65rem;
    }

    .tooltip-pearl {
      background: var(--pearl-bg);
      border-left: 3px solid var(--pearl-border);
      padding: 0.45rem 0.65rem;
      border-radius: 0 6px 6px 0;
      font-size: 0.82rem;
      color: var(--pearl-text);
      margin-bottom: 0.75rem;
    }

    .tooltip-jump-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--accent-primary);
      padding: 0.3rem 0.6rem;
      border-radius: 6px;
      background: var(--accent-primary-subtle);
    }

    /* Modal Backdrop */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      z-index: 1050;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px);
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 10vh 1.25rem 2rem 1.25rem;
      overflow-y: auto;
    }

    .modal-content {
      width: 100%;
      max-width: 620px;
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      border-radius: 12px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
      overflow: hidden;
      animation: modalSlide 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes modalSlide {
      from { opacity: 0; transform: translateY(-12px) scale(0.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .search-input-wrap {
      padding: 1rem 1.25rem;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .search-modal-input {
      width: 100%;
      border: none;
      background: transparent;
      color: var(--text-main);
      font-size: 1.1rem;
      outline: none;
      font-family: inherit;
    }

    .search-results-list {
      max-height: 400px;
      overflow-y: auto;
      padding: 0.75rem;
    }

    .search-result-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.65rem 0.85rem;
      border-radius: 8px;
      color: var(--text-soft);
      cursor: pointer;
      margin-bottom: 0.25rem;
    }

    .search-result-item:hover, .search-result-item.selected {
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
    }

    /* Lightbox Modal */
    #lightbox-modal {
      position: fixed;
      inset: 0;
      z-index: 2000;
      background: rgba(0, 0, 0, 0.92);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      flex-direction: column;
    }

    #lightbox-img {
      max-width: 90vw;
      max-height: 80vh;
      border-radius: 8px;
      box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8);
      object-fit: contain;
    }

    #lightbox-caption {
      color: #f1f5f9;
      font-size: 0.95rem;
      margin-top: 1rem;
      text-align: center;
      max-width: 800px;
    }

    /* Responsive Breakpoints */
    @media (max-width: 1200px) {
      .workspace-grid {
        grid-template-columns: 260px minmax(0, 1fr);
      }
      .right-sidebar {
        display: none;
      }
    }

    @media (max-width: 840px) {
      .workspace-grid {
        grid-template-columns: minmax(0, 1fr);
      }
      .left-sidebar {
        display: none;
      }
      .center-content {
        padding: 1.25rem 1rem;
      }
      .search-btn {
        min-width: unset;
      }
      .search-btn span {
        display: none;
      }
    }
  </style>
</head>
<body>

  <!-- ========================================================================
       TOP STICKY NAVBAR
       ======================================================================== -->
  <header class="top-navbar">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <button id="mobile-nav-toggle" class="icon-only-btn" style="display: none;" title="Toggle Outline">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>

      <div class="nav-brand">
        <div class="logo-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg>
        </div>
        <span>MedBase</span>
      </div>
    </div>

    <!-- Search Button / Shortcut -->
    <button id="open-search-btn" class="search-btn">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <span>Command Search...</span>
      <kbd class="kbd-badge">Ctrl K</kbd>
    </button>

    <!-- Study Toolbar -->
    <div class="study-toolbar">
      <button id="toggle-hy-btn" class="tool-btn btn-hy" title="Filter out low-yield details">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        <span>High-Yield</span>
      </button>

      <button id="toggle-highlights-btn" class="tool-btn btn-highlights" title="Toggle yellow exam highlights">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 11-6 6v3h3l6-6"/><path d="m22 12-4.6 4.6a2 2 0 0 1-2.8 0l-5.2-5.2a2 2 0 0 1 0-2.8L14 4"/></svg>
        <span>Highlights</span>
      </button>

      <button id="toggle-quiz-btn" class="tool-btn btn-quiz" title="Toggle Quiz / Blank mode">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" y1="2" x2="22" y2="22"/></svg>
        <span>Quiz Mode <span id="quiz-count-badge" style="display:none; font-size:0.75rem; background:rgba(2,132,199,0.25); padding:1px 5px; border-radius:999px;">0/0</span></span>
      </button>

      <button id="toggle-er-btn" class="tool-btn btn-er" title="Collapse background, expand acute Rx & Diagnostics">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        <span>ER Mode</span>
      </button>

      <button id="open-qbank-btn" class="tool-btn" title="Open Board Questions">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        <span>Qbank</span>
      </button>

      <button id="toggle-theme-btn" class="icon-only-btn" title="Switch Light/Dark Mode">
        <svg id="theme-icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
      </button>
    </div>
  </header>

  <!-- ========================================================================
       WORKSPACE 3-COLUMN LAYOUT
       ======================================================================== -->
  <div class="workspace-grid">
    
    <!-- LEFT SIDEBAR: Outline & Library -->
    <aside class="left-sidebar">
      <div class="sidebar-tabs">
        <button class="sidebar-tab-btn active" data-tab="outline">Article Outline</button>
        <button class="sidebar-tab-btn" data-tab="library">Library Tree</button>
      </div>

      <div id="tab-outline" class="sidebar-tab-content">
        <div id="toc-container">
          <!-- Dynamically populated TOC items -->
        </div>
      </div>

      <div id="tab-library" class="sidebar-tab-content" style="display: none;">
        <div id="library-container">
          <!-- Dynamically populated Library items -->
        </div>
      </div>
    </aside>

    <!-- CENTER CONTENT: Main Article -->
    <main class="center-content">
      <div class="article-header">
        <div class="breadcrumbs" id="article-breadcrumbs">
          <span>Internal Medicine</span> / <span>Cardiology</span> / <span>Coronary Artery Disease</span>
        </div>
        <h1 class="article-title" id="article-title">Acute Coronary Syndrome (ACS)</h1>
        
        <div class="article-meta-row">
          <span class="meta-pill" id="article-updated">Nov 2026</span>
          <span class="meta-pill" id="article-readtime">12 min read</span>
          <span class="meta-pill pill-hy" id="article-hytag">Core Shelf & Step 2 CK</span>
          <span class="meta-pill" id="article-qcount">Qbank: 3 Cases</span>
          <button id="expand-all-btn" class="tool-btn" style="margin-left: auto; font-size: 0.78rem;">Expand All</button>
        </div>

        <!-- High-Yield Filter Active Banner -->
        <div class="hy-banner" id="hy-banner">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <strong>High-Yield Mode Active:</strong>
            <span id="hy-hidden-count">Detailed theory & secondary items hidden.</span>
          </div>
          <button id="turn-off-hy-btn" style="font-weight: 600; color: #f59e0b; text-decoration: underline;">Show All</button>
        </div>

        <div class="article-summary-card" id="article-summary">
          <!-- Rendered Article Summary -->
        </div>
      </div>

      <!-- Article Sections Container -->
      <div id="article-sections-container">
        <!-- Dynamically rendered collapsible sections -->
      </div>
    </main>

    <!-- RIGHT CONTEXTUAL SIDEBAR: Calculators, Qbank, Notes -->
    <aside class="right-sidebar">
      <div class="sidebar-tabs">
        <button class="sidebar-tab-btn active" data-rtab="calculators">Calculators</button>
        <button class="sidebar-tab-btn" data-rtab="qbank">Qbank</button>
        <button class="sidebar-tab-btn" data-rtab="notes">My Notes</button>
      </div>

      <div class="right-sidebar-body">
        
        <!-- CALCULATORS TAB -->
        <div id="rtab-calculators">
          <div class="calc-segmented">
            <button class="calc-seg-btn active" data-calc="heart">HEART Score (ACS)</button>
            <button class="calc-seg-btn" data-calc="curb65">CURB-65 (CAP)</button>
          </div>

          <!-- HEART Score Calculator -->
          <div id="calc-heart-wrap">
            <div style="margin-bottom: 0.85rem; font-size: 0.85rem; color: var(--text-muted);">
              Validated clinical prediction rule for chest pain emergency risk stratification:
            </div>
            
            <div id="heart-form">
              <!-- Rendered via JS -->
            </div>

            <div class="calc-result-box" id="heart-result-box">
              <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">HEART SCORE</div>
              <div class="calc-score-num" id="heart-score-val">0</div>
              <div id="heart-risk-badge" style="font-weight: 700; font-size: 0.95rem; margin-bottom: 0.25rem;">Low Risk</div>
              <div id="heart-mace-val" style="font-size: 0.82rem; color: var(--text-soft); margin-bottom: 0.5rem;">6-week MACE risk: 0.9–1.7%</div>
              <button id="reset-heart-btn" class="tool-btn" style="margin: 0 auto; font-size: 0.75rem;">Reset Calculator</button>
            </div>
          </div>

          <!-- CURB-65 Calculator -->
          <div id="calc-curb65-wrap" style="display: none;">
            <div style="margin-bottom: 0.85rem; font-size: 0.85rem; color: var(--text-muted);">
              Community-Acquired Pneumonia severity & mortality prediction:
            </div>
            
            <div id="curb65-form">
              <!-- Rendered via JS -->
            </div>

            <div class="calc-result-box" id="curb65-result-box">
              <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">CURB-65 SCORE</div>
              <div class="calc-score-num" id="curb65-score-val">0</div>
              <div id="curb65-risk-badge" style="font-weight: 700; font-size: 0.95rem; margin-bottom: 0.25rem;">Low Risk (Score 0)</div>
              <div id="curb65-mortality-val" style="font-size: 0.82rem; color: var(--text-soft); margin-bottom: 0.5rem;">30-Day Mortality: 0.7% (Outpatient treatment)</div>
              <button id="reset-curb65-btn" class="tool-btn" style="margin: 0 auto; font-size: 0.75rem;">Reset Calculator</button>
            </div>
          </div>
        </div>

        <!-- QBANK TAB -->
        <div id="rtab-qbank" style="display: none;">
          <div id="sidebar-qbank-container">
            <!-- Rendered via JS -->
          </div>
        </div>

        <!-- MY NOTES TAB -->
        <div id="rtab-notes" style="display: none;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-size: 0.82rem; font-weight: 700; color: var(--text-soft);">CLINICAL SCRATCHPAD</span>
            <span id="notes-status" style="font-size: 0.75rem; color: #10b981;">Saved to cloud</span>
          </div>
          <textarea id="my-notes-textarea" class="scratchpad-textarea" placeholder="Type clinical pearls, call notes, or drug dosages here... Auto-saved locally and synced."></textarea>
          <div style="display: flex; gap: 0.5rem; margin-top: 0.65rem;">
            <button id="clear-notes-btn" class="tool-btn" style="font-size: 0.78rem;">Clear Notes</button>
            <button id="download-notes-btn" class="tool-btn" style="font-size: 0.78rem; margin-left: auto;">Export .txt</button>
          </div>
        </div>

      </div>
    </aside>
  </div>

  <!-- ========================================================================
       SMART MEDICAL TOOLTIP POPOVER
       ======================================================================== -->
  <div id="tooltip-popover">
    <div class="tooltip-category" id="tt-category">BIOMARKER</div>
    <div class="tooltip-title" id="tt-title">Term Title</div>
    <div class="tooltip-desc" id="tt-desc">Term description...</div>
    <div class="tooltip-pearl" id="tt-pearl">Clinical pearl...</div>
    <button id="tt-jump-btn" class="tooltip-jump-btn">
      <span>Jump to Section</span>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    </button>
  </div>

  <!-- ========================================================================
       COMMAND SEARCH MODAL (Ctrl+K)
       ======================================================================== -->
  <div id="search-modal" class="modal-backdrop" style="display: none;">
    <div class="modal-content">
      <div class="search-input-wrap">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input type="text" id="modal-search-input" class="search-modal-input" placeholder="Search conditions, algorithms, ECG signs, drugs..." />
        <kbd class="kbd-badge">ESC</kbd>
      </div>
      <div class="search-results-list" id="search-results-list">
        <!-- Results rendered here -->
      </div>
    </div>
  </div>

  <!-- ========================================================================
       FULLSCREEN IMAGE LIGHTBOX MODAL
       ======================================================================== -->
  <div id="lightbox-modal">
    <button id="close-lightbox-btn" class="icon-only-btn" style="position: absolute; top: 1.5rem; right: 1.5rem; color:#fff; background:rgba(255,255,255,0.15); border:none;">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6 6 18M6 6l12 12"/></svg>
    </button>
    <img id="lightbox-img" src="" alt="Clinical Preview" />
    <div id="lightbox-caption"></div>
  </div>

  <!-- EMBEDDED MEDBASE DATA -->
  <script>
    const MEDBASE_DATA = """ + json.dumps(med_data, ensure_ascii=False) + """;
  </script>

  <!-- ========================================================================
       STANDALONE JAVASCRIPT APPLICATION ENGINE
       ======================================================================== -->
  <script>
  (function() {
    'use strict';

    // --- State Management ---
    const state = {
      activeArticleId: 'acs',
      theme: localStorage.getItem('dod_theme') || 'dark',
      highYieldOnly: false,
      highlightsActive: true,
      quizModeActive: false,
      revealedBlanks: new Set(),
      allBlankIds: [],
      onDutyModeActive: false,
      activeCalc: 'heart',
      currentQbankIdx: 0,
      qbankSelections: {},
      qbankStrikethroughs: {},
      userNotes: localStorage.getItem('medbase_notes') || '',
      searchQuery: '',
      activeTooltipTerm: null
    };

    // Apply theme
    document.documentElement.setAttribute('data-theme', state.theme);
    if (state.highlightsActive) document.body.classList.add('highlights-active');

    // --- DOM Elements ---
    const els = {
      themeBtn: document.getElementById('toggle-theme-btn'),
      hyBtn: document.getElementById('toggle-hy-btn'),
      highlightsBtn: document.getElementById('toggle-highlights-btn'),
      quizBtn: document.getElementById('toggle-quiz-btn'),
      quizBadge: document.getElementById('quiz-count-badge'),
      erBtn: document.getElementById('toggle-er-btn'),
      qbankBtn: document.getElementById('open-qbank-btn'),
      searchBtn: document.getElementById('open-search-btn'),
      searchModal: document.getElementById('search-modal'),
      searchInput: document.getElementById('modal-search-input'),
      searchResults: document.getElementById('search-results-list'),
      tooltip: document.getElementById('tooltip-popover'),
      ttCategory: document.getElementById('tt-category'),
      ttTitle: document.getElementById('tt-title'),
      ttDesc: document.getElementById('tt-desc'),
      ttPearl: document.getElementById('tt-pearl'),
      ttJumpBtn: document.getElementById('tt-jump-btn'),
      lightbox: document.getElementById('lightbox-modal'),
      lightboxImg: document.getElementById('lightbox-img'),
      lightboxCap: document.getElementById('lightbox-caption'),
      closeLightboxBtn: document.getElementById('close-lightbox-btn'),
      tocContainer: document.getElementById('toc-container'),
      libraryContainer: document.getElementById('library-container'),
      sectionsContainer: document.getElementById('article-sections-container'),
      expandAllBtn: document.getElementById('expand-all-btn'),
      hyBanner: document.getElementById('hy-banner'),
      turnOffHyBtn: document.getElementById('turn-off-hy-btn'),
      notesTextarea: document.getElementById('my-notes-textarea'),
      notesStatus: document.getElementById('notes-status'),
      clearNotesBtn: document.getElementById('clear-notes-btn'),
      downloadNotesBtn: document.getElementById('download-notes-btn')
    };

    // --- Rich Text Parser ---
    function parseInline(text, keyPrefix) {
      if (!text) return '';
      let res = '';
      let remaining = text;
      let idx = 0;

      while (remaining.length > 0) {
        const hlPos = remaining.indexOf('[[hl:');
        const termPos = remaining.indexOf('{{term:');
        const boldPos = remaining.indexOf('**');

        const candidates = [
          { type: 'hl', pos: hlPos },
          { type: 'term', pos: termPos },
          { type: 'bold', pos: boldPos }
        ].filter(c => c.pos !== -1);

        if (candidates.length === 0) {
          res += escapeHtml(remaining);
          break;
        }

        candidates.sort((a, b) => a.pos - b.pos);
        const next = candidates[0];

        if (next.pos > 0) {
          res += escapeHtml(remaining.slice(0, next.pos));
        }

        if (next.type === 'hl') {
          const start = next.pos + 5;
          const end = remaining.indexOf(']]', start);
          if (end === -1) {
            res += escapeHtml(remaining.slice(next.pos));
            break;
          }
          const inner = remaining.slice(start, end);
          const blankId = `${keyPrefix}-b${idx++}`;
          if (!state.allBlankIds.includes(blankId)) state.allBlankIds.push(blankId);
          
          const isRevealed = state.revealedBlanks.has(blankId);
          const unblankClass = isRevealed ? 'unblanked' : '';
          
          res += `<mark class="hy-mark quiz-blank ${unblankClass}" data-blank-id="${blankId}" onclick="window.medbase.toggleBlank('${blankId}')">${parseInline(inner, blankId)}</mark>`;
          remaining = remaining.slice(end + 2);
        } else if (next.type === 'term') {
          const start = next.pos + 7;
          const end = remaining.indexOf('}}', start);
          if (end === -1) {
            res += escapeHtml(remaining.slice(next.pos));
            break;
          }
          const inner = remaining.slice(start, end);
          const pipeIdx = inner.indexOf('|');
          const termId = pipeIdx !== -1 ? inner.slice(0, pipeIdx).trim() : inner.trim();
          const label = pipeIdx !== -1 ? inner.slice(pipeIdx + 1) : inner;
          
          res += `<span class="glossary-term" data-term-id="${termId}" onclick="window.medbase.showTooltip('${termId}', event)" onmouseenter="window.medbase.showTooltip('${termId}', event)">${parseInline(label, `${keyPrefix}-t`)}</span>`;
          remaining = remaining.slice(end + 2);
        } else if (next.type === 'bold') {
          const start = next.pos + 2;
          const end = remaining.indexOf('**', start);
          if (end === -1) {
            res += escapeHtml(remaining.slice(next.pos));
            break;
          }
          const inner = remaining.slice(start, end);
          res += `<strong>${parseInline(inner, `${keyPrefix}-bd`)}</strong>`;
          remaining = remaining.slice(end + 2);
        }
      }
      return res;
    }

    function escapeHtml(str) {
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // --- Render Bullet Tree ---
    function renderBulletTree(items, prefix) {
      if (!items || items.length === 0) return '';
      let html = '<ul class="bullet-tree">';
      items.forEach((item, i) => {
        const itemKey = `${prefix}-${i}`;
        const yieldClass = item.yield === 'low' ? 'yield-low' : '';
        html += `<li class="bullet-item ${yieldClass}">`;
        html += parseInline(item.text, itemKey);
        if (item.children && item.children.length > 0) {
          html += renderBulletTree(item.children, `${itemKey}-c`);
        }
        html += '</li>';
      });
      html += '</ul>';
      return html;
    }

    // --- Render Comparison Table ---
    function renderTable(tableBlock, prefix) {
      let html = `<div class="table-container ${tableBlock.yield === 'low' ? 'yield-low' : ''}">`;
      if (tableBlock.caption) {
        html += `<div class="table-caption">${tableBlock.caption}</div>`;
      }
      html += '<table class="amboss-table"><thead><tr>';
      tableBlock.headers.forEach(h => {
        html += `<th>${h}</th>`;
      });
      html += '</tr></thead><tbody>';
      tableBlock.rows.forEach((row, ri) => {
        html += '<tr>';
        row.forEach((cell, ci) => {
          html += `<td>${parseInline(cell, `${prefix}-r${ri}-c${ci}`)}</td>`;
        });
        html += '</tr>';
      });
      html += '</tbody></table></div>';
      return html;
    }

    // --- Render Callout Box ---
    function renderCallout(callout, prefix) {
      const variantClass = callout.variant === 'danger' || callout.variant === 'redflag'
        ? 'callout-danger'
        : callout.variant === 'rx'
        ? 'callout-rx'
        : callout.variant === 'diagnostic'
        ? 'callout-diagnostic'
        : 'callout-pearl';

      const iconSvg = callout.variant === 'danger' || callout.variant === 'redflag'
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
        : callout.variant === 'rx'
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg>'
        : callout.variant === 'diagnostic'
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>';

      return `
        <div class="callout-box ${variantClass} ${callout.yield === 'low' ? 'yield-low' : ''}">
          <div class="callout-head">
            ${iconSvg}
            <span>${callout.title || 'Clinical Pearl'}</span>
          </div>
          <div class="callout-body">${parseInline(callout.text, `${prefix}-co`)}</div>
        </div>
      `;
    }

    // --- Render Clinical Image Figure Slot ---
    function renderClinicalFigure(fig, secId) {
      return `
        <figure class="clinical-figure" id="fig-${secId}">
          <div class="clinical-img-wrap" onclick="window.medbase.openLightbox('${fig.src || ''}', '${escapeHtml(fig.caption || 'Clinical Figure')}')">
            ${fig.src ? `<img src="${fig.src}" alt="${escapeHtml(fig.caption || '')}" onerror="this.parentElement.style.display='none'" />` : '<div style="color:var(--text-muted); font-size:0.85rem;">[Clinical Photo Slot] Tap to preview or upload</div>'}
          </div>
          <figcaption class="clinical-caption">
            <span><strong>Figure:</strong> ${fig.caption || 'Clinical presentation & diagnostic scan'}</span>
            <button class="tool-btn" style="font-size:0.75rem;" onclick="document.getElementById('input-file-${secId}').click()">+ Upload / Change</button>
            <input type="file" id="input-file-${secId}" accept="image/*" style="display:none;" onchange="window.medbase.handleImageUpload('${secId}', event)" />
          </figcaption>
        </figure>
      `;
    }

    // --- Render Blocks Inside Section ---
    function renderBlocks(blocks, prefix, secId) {
      if (!blocks) return '';
      let html = '';
      blocks.forEach((b, idx) => {
        const bKey = `${prefix}-b${idx}`;
        if (b.type === 'bullets') {
          html += renderBulletTree(b.items, bKey);
        } else if (b.type === 'callout') {
          html += renderCallout(b, bKey);
        } else if (b.type === 'table') {
          html += renderTable(b, bKey);
        } else if (b.type === 'paragraph') {
          html += `<p style="margin: 0.65rem 0; color:var(--text-soft); line-height:1.65;" class="${b.yield === 'low' ? 'yield-low' : ''}">${parseInline(b.text, bKey)}</p>`;
        }
      });
      return html;
    }

    // --- Render Article ---
    function renderArticle(artId) {
      const art = MEDBASE_DATA.ARTICLES[artId];
      if (!art) return;
      state.activeArticleId = artId;
      state.allBlankIds = [];

      // Header info
      document.getElementById('article-title').textContent = art.title;
      document.getElementById('article-breadcrumbs').innerHTML = (art.breadcrumbs || ['Internal Medicine']).map(b => `<span>${b}</span>`).join(' / ');
      document.getElementById('article-updated').textContent = art.lastUpdated || 'Nov 2026';
      document.getElementById('article-readtime').textContent = art.readTime || '10 min';
      document.getElementById('article-hytag').textContent = art.highYieldTag || 'Core High-Yield';
      document.getElementById('article-summary').innerHTML = parseInline(art.summary || '', 'sum');

      // Sections
      let secHtml = '';
      let tocHtml = '';

      art.sections.forEach((sec, sIdx) => {
        const secKey = `sec-${sec.id}`;
        tocHtml += `<a href="#${secKey}" class="toc-item" data-sec-id="${sec.id}">${sec.title}</a>`;

        secHtml += `
          <div class="amboss-card" id="${secKey}" data-section-id="${sec.id}">
            <button class="accordion-header" onclick="window.medbase.toggleSection('${secKey}')">
              <div class="title-wrap">
                <span class="section-badge">§ ${sIdx + 1}</span>
                <span>${sec.title}</span>
              </div>
              <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <div class="accordion-body">
              ${renderBlocks(sec.blocks, secKey, sec.id)}
              
              <!-- Sub-sections if any -->
              ${(sec.subsections || []).map((sub, subIdx) => `
                <div class="sub-accordion" id="sub-${sub.id}">
                  <button class="sub-accordion-header" onclick="window.medbase.toggleSubAccordion('sub-${sub.id}')">
                    <span>${sub.title}</span>
                    <svg class="sub-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                  </button>
                  <div class="sub-accordion-body">
                    ${renderBlocks(sub.blocks, `sub-${sub.id}`, sub.id)}
                  </div>
                </div>
              `).join('')}

              <!-- Clinical Photo figure slot -->
              ${renderClinicalFigure({ caption: `${sec.title} — Key Clinical Signs & Pathology` }, sec.id)}
            </div>
          </div>
        `;
      });

      els.sectionsContainer.innerHTML = secHtml;
      els.tocContainer.innerHTML = tocHtml;

      // Update TOC scrollspy
      setupScrollspy();

      // Render Qbank questions for article
      renderQbank(artId);

      // Update quiz badge count
      updateQuizBadge();
    }

    // --- Render Library Tree ---
    function renderLibraryTree() {
      let html = '';
      (MEDBASE_DATA.LIBRARY_TREE || []).forEach(cat => {
        html += `<div class="library-node">`;
        html += `<div class="library-node-title"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/></svg> <span>${cat.label}</span></div>`;
        html += `<div class="library-children">`;
        (cat.children || []).forEach(subCat => {
          html += `<div style="font-weight:600; font-size:0.8rem; color:var(--text-muted); margin:0.35rem 0 0.15rem 0.25rem;">${subCat.label}</div>`;
          (subCat.children || []).forEach(art => {
            const isActive = art.articleId === state.activeArticleId ? 'active' : '';
            html += `<div class="library-article-link ${isActive}" onclick="window.medbase.selectArticle('${art.articleId}')">
              <span>${art.label}</span>
              ${art.badge ? `<span class="section-badge" style="background:rgba(234,179,8,0.15); color:#ca8a04;">${art.badge}</span>` : ''}
            </div>`;
          });
        });
        html += `</div></div>`;
      });
      els.libraryContainer.innerHTML = html;
    }

    // --- Scrollspy ---
    function setupScrollspy() {
      const cards = document.querySelectorAll('.amboss-card');
      const tocLinks = document.querySelectorAll('.toc-item');

      window.addEventListener('scroll', () => {
        let currentId = '';
        cards.forEach(card => {
          const top = card.getBoundingClientRect().top;
          if (top <= 120) {
            currentId = card.getAttribute('data-section-id');
          }
        });
        tocLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('data-sec-id') === currentId);
        });
      }, { passive: true });
    }

    // --- Calculators: HEART & CURB-65 ---
    function setupCalculators() {
      // HEART Form
      const heartFormEl = document.getElementById('heart-form');
      const heartGroups = [
        { key: 'h', label: 'History', opts: [{ s: 0, t: 'Slightly suspicious' }, { s: 1, t: 'Moderately suspicious (+1)' }, { s: 2, t: 'Highly suspicious (+2)' }] },
        { key: 'e', label: 'ECG', opts: [{ s: 0, t: 'Normal' }, { s: 1, t: 'Non-specific repol disturbance (+1)' }, { s: 2, t: 'Significant ST deviation (+2)' }] },
        { key: 'a', label: 'Age', opts: [{ s: 0, t: '< 45 years' }, { s: 1, t: '45–64 years (+1)' }, { s: 2, t: '≥ 65 years (+2)' }] },
        { key: 'r', label: 'Risk Factors', opts: [{ s: 0, t: 'No risk factors' }, { s: 1, t: '1–2 risk factors (+1)' }, { s: 2, t: '≥ 3 or prior CAD (+2)' }] },
        { key: 't', label: 'Initial Troponin', opts: [{ s: 0, t: '≤ Normal limit' }, { s: 1, t: '1–3× normal (+1)' }, { s: 2, t: '> 3× normal (+2)' }] }
      ];

      heartFormEl.innerHTML = heartGroups.map(g => `
        <div class="calc-group">
          <label class="calc-group-label">${g.label}</label>
          ${g.opts.map((o, idx) => `
            <label class="calc-radio-label">
              <input type="radio" name="heart_${g.key}" value="${o.s}" ${idx === 0 ? 'checked' : ''} onchange="window.medbase.calcHeart()" />
              <span>${o.t}</span>
            </label>
          `).join('')}
        </div>
      `).join('');

      // CURB-65 Form
      const curbFormEl = document.getElementById('curb65-form');
      const curbItems = [
        { id: 'curb_c', label: 'C — Confusion (AMTS ≤ 8 or disorientation)' },
        { id: 'curb_u', label: 'U — Blood Urea Nitrogen > 19 mg/dL (> 7 mmol/L)' },
        { id: 'curb_r', label: 'R — Respiratory rate ≥ 30 breaths/min' },
        { id: 'curb_b', label: 'B — BP: Systolic < 90 OR Diastolic ≤ 60 mmHg' },
        { id: 'curb_65', label: '65 — Age ≥ 65 years' }
      ];

      curbFormEl.innerHTML = curbItems.map(item => `
        <label class="calc-radio-label" style="margin-bottom: 0.45rem;">
          <input type="checkbox" id="${item.id}" onchange="window.medbase.calcCurb65()" />
          <span>${item.label}</span>
        </label>
      `).join('');

      // Recalculate defaults
      calcHeart();
      calcCurb65();
    }

    function calcHeart() {
      let score = 0;
      ['h', 'e', 'a', 'r', 't'].forEach(k => {
        const checked = document.querySelector(`input[name="heart_${k}"]:checked`);
        if (checked) score += parseInt(checked.value, 10);
      });

      document.getElementById('heart-score-val').textContent = score;
      const riskEl = document.getElementById('heart-risk-badge');
      const maceEl = document.getElementById('heart-mace-val');

      if (score <= 3) {
        riskEl.textContent = 'Low Risk';
        riskEl.style.color = '#10b981';
        maceEl.textContent = '6-week MACE risk: 0.9–1.7% (Outpatient/Early DC)';
      } else if (score <= 6) {
        riskEl.textContent = 'Intermediate Risk';
        riskEl.style.color = '#f59e0b';
        maceEl.textContent = '6-week MACE risk: 12–16.6% (Inpatient Observation)';
      } else {
        riskEl.textContent = 'High Risk';
        riskEl.style.color = '#f43f5e';
        maceEl.textContent = '6-week MACE risk: 50–65% (Urgent Invasive Angiography)';
      }
    }

    function calcCurb65() {
      let score = 0;
      ['curb_c', 'curb_u', 'curb_r', 'curb_b', 'curb_65'].forEach(id => {
        const cb = document.getElementById(id);
        if (cb && cb.checked) score += 1;
      });

      document.getElementById('curb65-score-val').textContent = score;
      const riskEl = document.getElementById('curb65-risk-badge');
      const mortEl = document.getElementById('curb65-mortality-val');

      if (score <= 1) {
        riskEl.textContent = `Low Risk (Score ${score})`;
        riskEl.style.color = '#10b981';
        mortEl.textContent = '30-Day Mortality: 0.7–3% (Outpatient care)';
      } else if (score === 2) {
        riskEl.textContent = 'Moderate Risk (Score 2)';
        riskEl.style.color = '#f59e0b';
        mortEl.textContent = '30-Day Mortality: ~9% (Inpatient or close monitoring)';
      } else {
        riskEl.textContent = `Severe Risk (Score ${score})`;
        riskEl.style.color = '#f43f5e';
        mortEl.textContent = '30-Day Mortality: 15–40% (Hospitalize; assess for ICU)';
      }
    }

    // --- Qbank Renderer ---
    function renderQbank(artId) {
      const questions = (MEDBASE_DATA.QBANK_QUESTIONS && MEDBASE_DATA.QBANK_QUESTIONS[artId]) || [];
      const container = document.getElementById('sidebar-qbank-container');
      if (questions.length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); font-size:0.85rem; text-align:center; padding:1.5rem;">No questions for this topic yet.</div>';
        return;
      }

      const q = questions[state.currentQbankIdx % questions.length];
      const selectedIdx = state.qbankSelections[q.id];
      const striked = state.qbankStrikethroughs[q.id] || {};

      let html = `
        <div class="qbank-card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <span class="section-badge" style="background:rgba(2,132,199,0.15); color:var(--accent-primary);">Case ${state.currentQbankIdx + 1} of ${questions.length}</span>
            <span style="font-size:0.75rem; color:var(--text-muted);">${q.difficulty || 'Step 2 CK'}</span>
          </div>
          <div class="qbank-stem">${q.stem}</div>

          <div class="qbank-options-list">
            ${q.options.map((opt, oi) => {
              const isSelected = selectedIdx === oi;
              const isCorrect = opt.correct;
              let cls = '';
              if (selectedIdx !== undefined) {
                if (isSelected) cls = isCorrect ? 'selected-correct' : 'selected-wrong';
                else if (isCorrect) cls = 'selected-correct';
              }
              const isStriked = striked[oi] ? 'struck-through' : '';

              return `
                <div class="qbank-option ${cls} ${isStriked}" onclick="window.medbase.selectQbankOption('${q.id}', ${oi})">
                  <span style="font-weight:700; width:18px;">${String.fromCharCode(65 + oi)}.</span>
                  <span style="flex:1;">${opt.text}</span>
                  <button class="strike-btn" onclick="event.stopPropagation(); window.medbase.toggleStrike('${q.id}', ${oi})" title="Strike through option">✏️</button>
                </div>
              `;
            }).join('')}
          </div>

          ${selectedIdx !== undefined ? `
            <div class="qbank-explanation">
              <strong>${q.options[selectedIdx].correct ? '✅ Correct Answer!' : '❌ Incorrect'}</strong>
              <div style="margin-top:0.4rem; color:var(--text-soft);">${q.explanation || q.options[selectedIdx].explanation || 'Review the clinical pathophysiology above.'}</div>
            </div>
          ` : ''}

          <div style="display:flex; justify-content:space-between; margin-top:1rem;">
            <button class="tool-btn" onclick="window.medbase.prevQuestion('${artId}', ${questions.length})">Previous</button>
            <button class="tool-btn" onclick="window.medbase.nextQuestion('${artId}', ${questions.length})">Next Case</button>
          </div>
        </div>
      `;

      container.innerHTML = html;
    }

    // --- Tooltip Logic ---
    function showTooltip(termId, event) {
      if (state.quizModeActive) return; // Suppress tooltip in quiz mode to prevent spoilers
      const term = MEDBASE_DATA.MEDICAL_GLOSSARY && MEDBASE_DATA.MEDICAL_GLOSSARY[termId];
      if (!term) return;

      state.activeTooltipTerm = term;
      els.ttCategory.textContent = term.category || 'CLINICAL TERM';
      els.ttTitle.textContent = term.title || termId;
      els.ttDesc.textContent = term.definition || '';
      els.ttPearl.textContent = term.pearl ? `💡 Pearl: ${term.pearl}` : '';
      els.ttPearl.style.display = term.pearl ? 'block' : 'none';

      const rect = event.target.getBoundingClientRect();
      let top = rect.bottom + 8;
      let left = rect.left;

      // Viewport safety
      if (left + 330 > window.innerWidth) left = window.innerWidth - 340;
      if (left < 10) left = 10;
      if (top + 220 > window.innerHeight) top = rect.top - 230;

      els.tooltip.style.top = `${top}px`;
      els.tooltip.style.left = `${left}px`;
      els.tooltip.style.display = 'block';

      els.ttJumpBtn.onclick = () => {
        if (term.articleId && term.articleId !== state.activeArticleId) {
          renderArticle(term.articleId);
        }
        if (term.sectionId) {
          const target = document.getElementById(`sec-${term.sectionId}`);
          if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
            target.classList.remove('collapsed');
          }
        }
        els.tooltip.style.display = 'none';
      };
    }

    // Close tooltip on outside click
    document.addEventListener('click', (e) => {
      if (!e.target.closest('#tooltip-popover') && !e.target.closest('.glossary-term')) {
        els.tooltip.style.display = 'none';
      }
    });

    // --- Search Modal Engine ---
    function performSearch(query) {
      if (!query || query.trim() === '') {
        els.searchResults.innerHTML = '<div style="padding:1rem; color:var(--text-muted); text-align:center;">Type to search articles, sections, ECG signs, and medications...</div>';
        return;
      }
      const q = query.toLowerCase().trim();
      let matches = [];

      // Search articles & sections
      Object.entries(MEDBASE_DATA.ARTICLES || {}).forEach(([aId, art]) => {
        if (art.title.toLowerCase().includes(q)) {
          matches.push({ type: 'Article', title: art.title, desc: art.summary, action: () => { renderArticle(aId); closeSearch(); } });
        }
        (art.sections || []).forEach(sec => {
          if (sec.title.toLowerCase().includes(q)) {
            matches.push({ type: 'Section', title: `${art.title} → ${sec.title}`, desc: 'Article section', action: () => { renderArticle(aId); document.getElementById(`sec-${sec.id}`).scrollIntoView({ behavior: 'smooth' }); closeSearch(); } });
          }
        });
      });

      // Search glossary
      Object.entries(MEDBASE_DATA.MEDICAL_GLOSSARY || {}).forEach(([tId, term]) => {
        if (term.title.toLowerCase().includes(q) || (term.definition && term.definition.toLowerCase().includes(q))) {
          matches.push({
            type: term.category || 'Term',
            title: term.title,
            desc: term.definition,
            action: () => {
              if (term.articleId) renderArticle(term.articleId);
              if (term.sectionId) document.getElementById(`sec-${term.sectionId}`).scrollIntoView({ behavior: 'smooth' });
              closeSearch();
            }
          });
        }
      });

      if (matches.length === 0) {
        els.searchResults.innerHTML = `<div style="padding:1rem; color:var(--text-muted); text-align:center;">No matching clinical results for "${escapeHtml(query)}"</div>`;
        return;
      }

      els.searchResults.innerHTML = matches.slice(0, 10).map((m, idx) => `
        <div class="search-result-item" onclick="window.medbase.execSearchAction(${idx})">
          <div>
            <div style="font-weight:600; font-size:0.95rem; color:var(--text-main);">${m.title}</div>
            <div style="font-size:0.78rem; color:var(--text-muted); max-width:480px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${m.desc}</div>
          </div>
          <span class="section-badge">${m.type}</span>
        </div>
      `).join('');

      window.medbase_current_search_matches = matches;
    }

    function openSearch() {
      els.searchModal.style.display = 'flex';
      els.searchInput.value = '';
      els.searchInput.focus();
      performSearch('');
    }

    function closeSearch() {
      els.searchModal.style.display = 'none';
    }

    // --- Quiz Blank Updates ---
    function updateQuizBadge() {
      if (!state.quizModeActive) {
        els.quizBadge.style.display = 'none';
        return;
      }
      els.quizBadge.style.display = 'inline-block';
      els.quizBadge.textContent = `${state.revealedBlanks.size}/${state.allBlankIds.length}`;
    }

    // --- Event Listeners & Global Exposure ---
    window.medbase = {
      selectArticle: (id) => renderArticle(id),
      toggleSection: (secKey) => {
        const card = document.getElementById(secKey);
        if (card) card.classList.toggle('collapsed');
      },
      toggleSubAccordion: (subKey) => {
        const sub = document.getElementById(subKey);
        if (sub) sub.classList.toggle('collapsed');
      },
      showTooltip: showTooltip,
      toggleBlank: (blankId) => {
        if (!state.quizModeActive) return;
        if (state.revealedBlanks.has(blankId)) {
          state.revealedBlanks.delete(blankId);
        } else {
          state.revealedBlanks.add(blankId);
        }
        document.querySelectorAll(`[data-blank-id="${blankId}"]`).forEach(el => {
          el.classList.toggle('unblanked', state.revealedBlanks.has(blankId));
        });
        updateQuizBadge();
      },
      calcHeart: calcHeart,
      calcCurb65: calcCurb65,
      selectQbankOption: (qId, oIdx) => {
        state.qbankSelections[qId] = oIdx;
        renderQbank(state.activeArticleId);
      },
      toggleStrike: (qId, oIdx) => {
        if (!state.qbankStrikethroughs[qId]) state.qbankStrikethroughs[qId] = {};
        state.qbankStrikethroughs[qId][oIdx] = !state.qbankStrikethroughs[qId][oIdx];
        renderQbank(state.activeArticleId);
      },
      nextQuestion: (artId, len) => {
        state.currentQbankIdx = (state.currentQbankIdx + 1) % len;
        renderQbank(artId);
      },
      prevQuestion: (artId, len) => {
        state.currentQbankIdx = (state.currentQbankIdx - 1 + len) % len;
        renderQbank(artId);
      },
      openLightbox: (src, cap) => {
        if (!src) return;
        els.lightboxImg.src = src;
        els.lightboxCap.textContent = cap || '';
        els.lightbox.style.display = 'flex';
      },
      handleImageUpload: (secId, event) => {
        const file = event.target.files && event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (e) => {
          const fig = document.getElementById(`fig-${secId}`);
          if (fig) {
            const wrap = fig.querySelector('.clinical-img-wrap');
            wrap.innerHTML = `<img src="${e.target.result}" alt="Uploaded image" />`;
            wrap.onclick = () => window.medbase.openLightbox(e.target.result, 'Uploaded Clinical Photo');
          }
        };
        reader.readAsDataURL(file);
      },
      execSearchAction: (idx) => {
        if (window.medbase_current_search_matches && window.medbase_current_search_matches[idx]) {
          window.medbase_current_search_matches[idx].action();
        }
      }
    };

    // --- Toolbar Handlers ---
    // Theme
    els.themeBtn.addEventListener('click', () => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', state.theme);
      localStorage.setItem('dod_theme', state.theme);
      localStorage.setItem('medbase_theme', state.theme);
    });

    // High-Yield Mode
    els.hyBtn.addEventListener('click', () => {
      state.highYieldOnly = !state.highYieldOnly;
      document.body.classList.toggle('hy-filter-active', state.highYieldOnly);
      els.hyBtn.classList.toggle('active', state.highYieldOnly);
    });

    els.turnOffHyBtn.addEventListener('click', () => {
      state.highYieldOnly = false;
      document.body.classList.remove('hy-filter-active');
      els.hyBtn.classList.remove('active');
    });

    // Highlights
    els.highlightsBtn.addEventListener('click', () => {
      state.highlightsActive = !state.highlightsActive;
      document.body.classList.toggle('highlights-active', state.highlightsActive);
      els.highlightsBtn.classList.toggle('active', state.highlightsActive);
    });
    els.highlightsBtn.classList.add('active'); // active by default

    // Quiz Mode
    els.quizBtn.addEventListener('click', () => {
      state.quizModeActive = !state.quizModeActive;
      document.body.classList.toggle('quiz-active', state.quizModeActive);
      els.quizBtn.classList.toggle('active', state.quizModeActive);
      updateQuizBadge();
    });

    // ER Mode
    els.erBtn.addEventListener('click', () => {
      state.onDutyModeActive = !state.onDutyModeActive;
      els.erBtn.classList.toggle('active', state.onDutyModeActive);

      // In ER mode, collapse overview/etiology, expand diagnosis & management
      document.querySelectorAll('.amboss-card').forEach(card => {
        const secId = card.getAttribute('data-section-id') || '';
        if (state.onDutyModeActive) {
          if (secId.includes('overview') || secId.includes('etiology') || secId.includes('pathophys')) {
            card.classList.add('collapsed');
          } else if (secId.includes('diag') || secId.includes('mgmt') || secId.includes('resus') || secId.includes('protocol')) {
            card.classList.remove('collapsed');
          }
        } else {
          card.classList.remove('collapsed');
        }
      });
    });

    // Qbank Button
    els.qbankBtn.addEventListener('click', () => {
      document.querySelector('[data-rtab="qbank"]').click();
    });

    // Expand / Collapse All
    let allExpanded = true;
    els.expandAllBtn.addEventListener('click', () => {
      allExpanded = !allExpanded;
      els.expandAllBtn.textContent = allExpanded ? 'Collapse All' : 'Expand All';
      document.querySelectorAll('.amboss-card').forEach(c => {
        c.classList.toggle('collapsed', !allExpanded);
      });
    });

    // Search Modal Shortcuts
    els.searchBtn.addEventListener('click', openSearch);
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openSearch();
      } else if (e.key === 'Escape' && els.searchModal.style.display === 'flex') {
        closeSearch();
      }
    });

    els.searchInput.addEventListener('input', (e) => performSearch(e.target.value));
    els.searchModal.addEventListener('click', (e) => {
      if (e.target === els.searchModal) closeSearch();
    });

    // Lightbox Close
    els.closeLightboxBtn.addEventListener('click', () => els.lightbox.style.display = 'none');
    els.lightbox.addEventListener('click', (e) => {
      if (e.target === els.lightbox) els.lightbox.style.display = 'none';
    });

    // Left Sidebar Tabs
    document.querySelectorAll('.sidebar-tab-btn[data-tab]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.sidebar-tab-btn[data-tab]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const tab = btn.getAttribute('data-tab');
        document.getElementById('tab-outline').style.display = tab === 'outline' ? 'block' : 'none';
        document.getElementById('tab-library').style.display = tab === 'library' ? 'block' : 'none';
      });
    });

    // Right Sidebar Tabs
    document.querySelectorAll('.sidebar-tab-btn[data-rtab]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.sidebar-tab-btn[data-rtab]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const rtab = btn.getAttribute('data-rtab');
        document.getElementById('rtab-calculators').style.display = rtab === 'calculators' ? 'block' : 'none';
        document.getElementById('rtab-qbank').style.display = rtab === 'qbank' ? 'block' : 'none';
        document.getElementById('rtab-notes').style.display = rtab === 'notes' ? 'block' : 'none';
      });
    });

    // Calculator Segmented Toggle
    document.querySelectorAll('.calc-seg-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.calc-seg-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const calc = btn.getAttribute('data-calc');
        document.getElementById('calc-heart-wrap').style.display = calc === 'heart' ? 'block' : 'none';
        document.getElementById('calc-curb65-wrap').style.display = calc === 'curb65' ? 'block' : 'none';
      });
    });

    document.getElementById('reset-heart-btn').addEventListener('click', () => {
      document.querySelectorAll('#heart-form input[type="radio"]').forEach((r, idx) => {
        if (idx % 3 === 0) r.checked = true;
      });
      calcHeart();
    });

    document.getElementById('reset-curb65-btn').addEventListener('click', () => {
      document.querySelectorAll('#curb65-form input[type="checkbox"]').forEach(cb => cb.checked = false);
      calcCurb65();
    });

    // Notes Scratchpad Persistence
    els.notesTextarea.value = state.userNotes;
    let notesTimer = null;
    els.notesTextarea.addEventListener('input', () => {
      els.notesStatus.textContent = 'Saving...';
      clearTimeout(notesTimer);
      notesTimer = setTimeout(() => {
        localStorage.setItem('medbase_notes', els.notesTextarea.value);
        els.notesStatus.textContent = 'Saved to cloud';
      }, 500);
    });

    els.clearNotesBtn.addEventListener('click', () => {
      if (confirm('Clear clinical scratchpad?')) {
        els.notesTextarea.value = '';
        localStorage.setItem('medbase_notes', '');
        els.notesStatus.textContent = 'Cleared';
      }
    });

    els.downloadNotesBtn.addEventListener('click', () => {
      const blob = new Blob([els.notesTextarea.value], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `MedBase_Notes_${new Date().toISOString().slice(0,10)}.txt`;
      a.click();
      URL.revokeObjectURL(url);
    });

    // Initialize App
    renderArticle('acs');
    renderLibraryTree();
    setupCalculators();

  })();
  </script>
</body>
</html>
"""

with open("/root/medbase/medbase.html", "w", encoding="utf-8") as f:
    f.write(html_template)

# Also write to /sdcard/medbase.html
try:
    with open("/sdcard/medbase.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Wrote to /sdcard/medbase.html successfully!")
except Exception as e:
    print("Could not write directly to /sdcard/medbase.html:", e)

print("Wrote /root/medbase/medbase.html successfully! Size:", len(html_template), "bytes")
