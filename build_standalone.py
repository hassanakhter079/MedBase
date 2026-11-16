import json
import os

with open("/root/medbase/medbase_data.json", "r", encoding="utf-8") as f:
    med_data = json.load(f)

html_content = r"""<!DOCTYPE html>
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
       1. COLOR SYSTEM & CSS VARIABLES (LIGHT, DARK & SEPIA THEMES)
       ========================================================================== */
    :root {
      /* FONT SCALING VARIABLES */
      --font-scale: 1;
      --base-font-size: 15px;
      --content-font-size: calc(var(--base-font-size) * var(--font-scale));
      --content-line-height: calc(1.65 * var(--font-scale));

      /* LIGHT MODE */
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
      /* DARK MODE */
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
      --pearl-bg: #1c1917;
      --pearl-border: #d97706;
      --pearl-text: #fef3c7;
      --pearl-badge: #f59e0b;

      --danger-bg: #201318;
      --danger-border: #e11d48;
      --danger-text: #ffe4e6;
      --danger-badge: #fb7185;

      --rx-bg: #061c14;
      --rx-border: #059669;
      --rx-text: #d1fae5;
      --rx-badge: #34d399;

      --diag-bg: #0c1a2e;
      --diag-border: #0284c7;
      --diag-text: #e0f2fe;
      --diag-badge: #38bdf8;

      --hy-highlight-bg: #854d0e;
      --hy-highlight-text: #fef08a;
      --blank-bg: #1e293b;
      --blank-border: #334155;
    }

    [data-theme="sepia"] {
      /* SEPIA THEME */
      --bg-app: #f4ecd8;
      --bg-surface: #fbf7ee;
      --bg-surface-elevated: #ffffff;
      --bg-surface-subtle: #efe5cb;
      --bg-surface-muted: #e4d7b6;
      --border-subtle: #e0d1ab;
      --border-medium: #c7b388;
      --border-strong: #9e8a60;
      --text-main: #2d2417;
      --text-soft: #4a3b26;
      --text-muted: #79664c;
      --text-faint: #a08c70;

      --accent-primary: #944d18;
      --accent-primary-hover: #783b10;
      --accent-primary-subtle: rgba(148, 77, 24, 0.12);

      --card-shadow: 0 1px 4px rgba(74, 59, 38, 0.08), 0 8px 20px -4px rgba(74, 59, 38, 0.06);
      --card-shadow-hover: 0 4px 10px rgba(74, 59, 38, 0.12), 0 12px 28px -4px rgba(74, 59, 38, 0.1);
      --card-emboss: inset 0 1px 0 rgba(255, 255, 255, 0.8), 0 1px 2px rgba(74, 59, 38, 0.06);

      --pearl-bg: #f9f0da;
      --pearl-border: #b45309;
      --pearl-text: #572905;
      --pearl-badge: #92400e;

      --danger-bg: #fbede8;
      --danger-border: #be123c;
      --danger-text: #5c0b1e;
      --danger-badge: #9f1239;

      --rx-bg: #eaf3ea;
      --rx-border: #047857;
      --rx-text: #053b2c;
      --rx-badge: #065f46;

      --diag-bg: #e7eff5;
      --diag-border: #0369a1;
      --diag-text: #083c5a;
      --diag-badge: #075985;

      --hy-highlight-bg: #edd382;
      --hy-highlight-text: #452a03;
      --blank-bg: #e6dac1;
      --blank-border: #cfbea0;
    }

    /* ==========================================================================
       2. GLOBAL RESET & BASE TYPOGRAPHY
       ========================================================================== */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg-app);
      color: var(--text-main);
      line-height: var(--content-line-height);
      font-size: var(--content-font-size);
      min-height: 100vh;
      overflow-x: hidden;
      transition: background-color 0.25s ease, color 0.25s ease;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    button {
      font-family: inherit;
      cursor: pointer;
      border: none;
      background: none;
      outline: none;
    }

    input, textarea {
      font-family: inherit;
      outline: none;
    }

    /* ==========================================================================
       3. TOP NAVIGATION & STUDY TOOLBAR
       ========================================================================== */
    .top-navbar {
      position: sticky;
      top: 0;
      z-index: 100;
      height: 64px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-subtle);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.25rem;
      gap: 1rem;
    }

    .brand-link {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      font-weight: 800;
      font-size: 1.25rem;
      color: var(--text-main);
      letter-spacing: -0.02em;
    }

    .logo-icon {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: linear-gradient(135deg, var(--accent-primary), #0284c7);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }

    .search-btn {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.45rem 0.85rem;
      color: var(--text-muted);
      font-size: 0.84rem;
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
      gap: 0.45rem;
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
    [data-theme="dark"] .tool-btn.btn-hy.active { color: #fde047; }
    [data-theme="sepia"] .tool-btn.btn-hy.active { color: #b45309; }

    .tool-btn.btn-highlights.active {
      background: rgba(245, 158, 11, 0.18);
      border-color: #f59e0b;
      color: #d97706;
    }

    .tool-btn.btn-quiz.active {
      background: rgba(16, 185, 129, 0.18);
      border-color: #10b981;
      color: #059669;
    }

    .tool-btn.btn-er.active {
      background: rgba(244, 63, 94, 0.18);
      border-color: #f43f5e;
      color: #e11d48;
    }

    /* Font Size Controls */
    .font-size-group {
      display: inline-flex;
      align-items: center;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 7px;
      padding: 2px;
      gap: 2px;
    }

    .font-tool-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 28px;
      border: none;
      background: transparent;
      color: var(--text-soft);
      border-radius: 5px;
      cursor: pointer;
      font-weight: 700;
      font-size: 0.8rem;
      transition: all 0.15s ease;
    }

    .font-tool-btn:hover {
      background: var(--bg-surface-subtle);
      color: var(--accent-primary);
    }

    .font-tool-btn:active {
      transform: scale(0.92);
    }

    .font-size-indicator {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 0.45rem;
      height: 28px;
      border: none;
      background: var(--bg-surface-subtle);
      color: var(--text-muted);
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .font-size-indicator:hover {
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
    }

    .theme-toggle-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.45rem 0.75rem;
      border-radius: 7px;
      font-size: 0.82rem;
      font-weight: 600;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      color: var(--text-soft);
      transition: all 0.15s ease;
    }

    .theme-toggle-btn:hover {
      background: var(--bg-surface-subtle);
      border-color: var(--border-medium);
      color: var(--text-main);
    }

    /* ==========================================================================
       4. 2-COLUMN WORKSPACE LAYOUT (NO RIGHT PANEL)
       ========================================================================== */
    .workspace-grid {
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
      max-width: 1560px;
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
      transition: transform 0.25s ease;
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

    .sidebar-content-pane {
      padding: 1rem;
      flex: 1;
      overflow-y: auto;
    }

    /* TOC Outline in Sidebar */
    .toc-item {
      display: block;
      padding: 0.45rem 0.65rem;
      font-size: 0.84rem;
      color: var(--text-soft);
      border-radius: 6px;
      margin-bottom: 0.2rem;
      border-left: 2px solid transparent;
      transition: all 0.15s ease;
    }

    .toc-item:hover {
      background: var(--bg-surface-subtle);
      color: var(--accent-primary);
    }

    .toc-item.active {
      color: var(--accent-primary);
      font-weight: 600;
      border-left-color: var(--accent-primary);
      background: var(--accent-primary-subtle);
    }

    /* Library Tree in Sidebar */
    .library-node {
      margin-bottom: 0.65rem;
    }

    .library-node-title {
      font-size: 0.84rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.35rem 0.25rem;
    }

    .library-children {
      margin-left: 0.85rem;
      border-left: 1px solid var(--border-subtle);
      padding-left: 0.65rem;
    }

    .library-article-link {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.4rem 0.5rem;
      font-size: 0.82rem;
      color: var(--text-soft);
      border-radius: 5px;
      margin-bottom: 0.15rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .library-article-link:hover {
      background: var(--bg-surface-subtle);
      color: var(--accent-primary);
    }

    .library-article-link.active {
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
      font-weight: 600;
    }

    /* Center Content Area */
    .center-content {
      padding: 2rem 2.5rem;
      max-width: 1140px;
      margin: 0 auto;
      width: 100%;
      font-size: var(--content-font-size);
    }

    .center-content p,
    .center-content li,
    .center-content .callout-text,
    .center-content .table-wrap td,
    .center-content .table-wrap th,
    .center-content .ref-sourced-list,
    .center-content .article-summary-card {
      font-size: var(--content-font-size);
      line-height: var(--content-line-height);
    }

    /* ==========================================================================
       5. HOME LIBRARY PORTAL VIEW
       ========================================================================== */
    .home-hero {
      padding: 2.5rem 0 1.5rem 0;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 2rem;
    }

    .home-hero h1 {
      font-size: 2.5rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 0.65rem;
      color: var(--text-main);
    }

    .home-hero p {
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 680px;
      line-height: 1.6;
    }

    .home-categories-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }

    .category-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: var(--card-emboss);
      transition: all 0.2s ease;
    }

    .category-card:hover {
      border-color: var(--accent-primary);
      box-shadow: var(--card-shadow-hover);
      transform: translateY(-2px);
    }

    .category-card-header {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1rem;
    }

    .category-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .category-card-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .article-pill-list {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .article-item-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.65rem 0.85rem;
      border-radius: 8px;
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-subtle);
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .article-item-card:hover {
      background: var(--bg-surface-muted);
      border-color: var(--border-medium);
      transform: translateX(3px);
    }

    /* ==========================================================================
       6. CLINICAL MONOGRAPH ARTICLE VIEW & CARDS
       ========================================================================== */
    .article-header {
      margin-bottom: 2rem;
    }

    .breadcrumbs {
      display: flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.84rem;
      color: var(--text-muted);
      margin-bottom: 0.75rem;
    }

    .breadcrumbs a:hover {
      text-decoration: underline;
    }

    .article-title {
      font-size: 2.25rem;
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
      margin-bottom: 1.15rem;
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

    /* Sourced From Header Banner */
    .article-sources-banner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.75rem;
      padding: 0.65rem 0.95rem;
      margin-bottom: 1.5rem;
      border-radius: 10px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      box-shadow: var(--card-emboss);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .article-sources-banner:hover {
      border-color: var(--accent-primary);
      background: var(--bg-surface-subtle);
      transform: translateY(-1px);
    }

    .sources-banner-left {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.5rem;
      font-size: 0.82rem;
    }

    .sources-icon {
      font-size: 1.1rem;
    }

    .sources-label {
      font-weight: 700;
      color: var(--text-main);
    }

    .sources-pill-row {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.35rem;
    }

    .source-tag-chip {
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.15rem 0.45rem;
      border-radius: 9999px;
      background: var(--bg-surface-muted);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
      white-space: nowrap;
    }

    .sources-jump-hint {
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--accent-primary);
      display: flex;
      align-items: center;
      gap: 0.25rem;
      white-space: nowrap;
    }

    .article-summary-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 1.35rem;
      margin-bottom: 2rem;
      box-shadow: var(--card-emboss);
      color: var(--text-soft);
      border-left: 4px solid var(--accent-primary);
    }

    /* Monograph Accordion Section Cards */
    .amboss-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      margin-bottom: 1.5rem;
      box-shadow: var(--card-emboss);
      transition: all 0.2s ease;
      scroll-margin-top: 80px;
      overflow: hidden;
    }

    .amboss-card:hover {
      box-shadow: var(--card-shadow);
      border-color: var(--border-medium);
    }

    .accordion-header {
      width: 100%;
      padding: 1.15rem 1.35rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      text-align: left;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-subtle);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      transition: background 0.15s ease;
    }

    .accordion-header:hover {
      background: var(--bg-surface-subtle);
    }

    .accordion-header .title-wrap {
      display: flex;
      align-items: center;
      gap: 0.65rem;
    }

    .section-badge {
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.15rem 0.5rem;
      border-radius: 9999px;
      background: var(--bg-surface-muted);
      color: var(--text-muted);
    }

    .chevron-icon {
      transition: transform 0.25s ease;
      color: var(--text-muted);
    }

    .amboss-card.collapsed .accordion-body {
      display: none;
    }

    .amboss-card.collapsed .chevron-icon {
      transform: rotate(-90deg);
    }

    .accordion-body {
      padding: 1.5rem 1.65rem;
    }

    /* Subsections */
    .sub-accordion {
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      margin: 1.25rem 0;
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
      background: var(--bg-surface-subtle);
      border-bottom: 1px solid var(--border-subtle);
    }

    .sub-accordion.collapsed .sub-accordion-body {
      display: none;
    }

    .sub-accordion.collapsed .sub-chevron {
      transform: rotate(-90deg);
    }

    .sub-accordion-body {
      padding: 1rem 1.15rem;
      background: var(--bg-surface);
    }

    /* ==========================================================================
       7. BULLETS, CALLOUTS, TABLES & RICH TEXT
       ========================================================================== */
    .content-tree {
      list-style: none;
      padding-left: 0;
    }

    .content-node {
      position: relative;
      padding-left: 1.4rem;
      margin-bottom: 0.55rem;
      color: var(--text-soft);
    }

    .content-node::before {
      content: "•";
      position: absolute;
      left: 0.4rem;
      color: var(--accent-primary);
      font-size: 1.1rem;
      line-height: 1.4;
    }

    .child-tree {
      list-style: none;
      padding-left: 1.25rem;
      margin-top: 0.35rem;
      border-left: 1px dashed var(--border-medium);
    }

    /* Callout Box (Tactile Embossed) */
    .callout-box {
      border-radius: 10px;
      padding: 1rem 1.25rem;
      margin: 1.15rem 0;
      display: flex;
      gap: 0.85rem;
      border: 1px solid transparent;
      box-shadow: var(--card-emboss);
    }

    .callout-pearl {
      background: var(--pearl-bg);
      border-color: var(--pearl-border);
      color: var(--pearl-text);
    }

    .callout-danger {
      background: var(--danger-bg);
      border-color: var(--danger-border);
      color: var(--danger-text);
    }

    .callout-rx {
      background: var(--rx-bg);
      border-color: var(--rx-border);
      color: var(--rx-text);
    }

    .callout-diag {
      background: var(--diag-bg);
      border-color: var(--diag-border);
      color: var(--diag-text);
    }

    .callout-icon {
      font-size: 1.25rem;
      flex-shrink: 0;
      padding-top: 0.1rem;
    }

    .callout-content {
      flex: 1;
    }

    .callout-title {
      font-weight: 700;
      font-size: 0.95rem;
      margin-bottom: 0.25rem;
    }

    /* Clinical Tables */
    .table-wrap {
      overflow-x: auto;
      margin: 1.25rem 0;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
    }

    .clinical-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }

    .clinical-table th {
      background: var(--bg-surface-subtle);
      padding: 0.75rem 1rem;
      font-weight: 700;
      color: var(--text-main);
      border-bottom: 1px solid var(--border-subtle);
    }

    .clinical-table td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-soft);
      vertical-align: top;
    }

    .clinical-table tr:last-child td {
      border-bottom: none;
    }

    .clinical-table tr:hover td {
      background: var(--bg-surface-subtle);
    }

    /* High-Yield Highlights & Quiz Blanks */
    .hy-mark {
      background: transparent;
      color: inherit;
      border-radius: 3px;
      padding: 0 0.2rem;
      transition: background 0.15s ease;
    }

    body.highlights-active .hy-mark {
      background-color: var(--hy-highlight-bg);
      color: var(--hy-highlight-text);
    }

    /* Quiz Mode Blanks */
    body.quiz-active .quiz-blank {
      background-color: var(--blank-bg) !important;
      color: transparent !important;
      user-select: none;
      cursor: pointer;
      border-bottom: 2px dashed var(--accent-primary);
      padding: 0 0.4rem;
      display: inline-block;
      transition: all 0.2s ease;
    }

    body.quiz-active .quiz-blank.unblanked {
      background-color: rgba(16, 185, 129, 0.15) !important;
      color: #10b981 !important;
      border-bottom: 2px solid #10b981;
    }

    /* Glossary Hover Term */
    .glossary-term {
      border-bottom: 1px dotted var(--accent-primary);
      cursor: help;
      color: var(--text-main);
      font-weight: 500;
      transition: color 0.15s ease;
    }

    .glossary-term:hover {
      color: var(--accent-primary);
    }

    /* Inline Reference Tag */
    .inline-ref-tag {
      display: inline-flex;
      align-items: center;
      padding: 0.1rem 0.38rem;
      margin: 0 0.2rem;
      font-family: inherit;
      font-size: 0.72rem;
      font-weight: 700;
      border-radius: 4px;
      border: 1px solid var(--border-medium);
      background: var(--bg-surface-subtle);
      color: var(--accent-primary);
      cursor: pointer;
      vertical-align: middle;
      line-height: 1.2;
      transition: all 0.15s ease;
    }

    .inline-ref-tag:hover {
      background: var(--accent-primary);
      color: #ffffff;
      border-color: var(--accent-primary);
      transform: scale(1.04);
      box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }

    /* External Inline Markdown Link */
    .external-inline-link {
      color: var(--accent-primary);
      font-weight: 600;
      text-decoration: underline;
      text-underline-offset: 3px;
      display: inline-flex;
      align-items: center;
      gap: 0.2rem;
    }

    .external-inline-link:hover {
      color: var(--accent-primary-hover);
    }

    /* ==========================================================================
       8. REFERENCES & EVIDENCE BASE STYLES
       ========================================================================== */
    .references-card {
      border-top: 3px solid var(--accent-primary);
      margin-top: 2.5rem;
    }

    .ref-total-badge {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.2rem 0.55rem;
      border-radius: 9999px;
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
      border: 1px solid var(--accent-primary);
    }

    .ref-disclaimer {
      display: flex;
      gap: 0.75rem;
      padding: 0.85rem 1rem;
      border-radius: 8px;
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-subtle);
      margin-bottom: 1.25rem;
      font-size: 0.84rem;
      color: var(--text-soft);
      line-height: 1.5;
    }

    .ref-disclaimer-icon {
      font-size: 1.25rem;
      flex-shrink: 0;
    }

    .ref-cards-grid {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .ref-item-card {
      padding: 1.15rem;
      border-radius: 10px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      box-shadow: var(--card-emboss);
      transition: all 0.25s ease;
      scroll-margin-top: 130px;
    }

    .ref-item-card:hover {
      border-color: var(--border-medium);
      box-shadow: var(--card-shadow);
    }

    .ref-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 0.5rem;
    }

    .ref-badge-group {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.4rem;
    }

    .ref-num-badge {
      font-size: 0.72rem;
      font-weight: 800;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }

    .ref-source-badge {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.15rem 0.5rem;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      border: 1px solid transparent;
    }

    /* Source Platform Color Schemes */
    .badge-amboss-knowledge {
      background: rgba(2, 132, 199, 0.15);
      color: #0284c7;
      border-color: rgba(2, 132, 199, 0.35);
    }

    .badge-osmosis-clinical {
      background: rgba(13, 148, 136, 0.15);
      color: #0d9488;
      border-color: rgba(13, 148, 136, 0.35);
    }

    .badge-first-aid-usmle-step-2-ck {
      background: rgba(225, 29, 72, 0.15);
      color: #e11d48;
      border-color: rgba(225, 29, 72, 0.35);
    }

    .badge-2023-esc-guidelines,
    .badge-2021-acc-aha-guidelines,
    .badge-ats-idsa-2019-guidelines,
    .badge-2022-aha-acc-hfsa-guidelines,
    .badge-ada-standards-of-care-2024 {
      background: rgba(124, 58, 237, 0.15);
      color: #7c3aed;
      border-color: rgba(124, 58, 237, 0.35);
    }

    .badge-doctor-on-duty-3rd-ed {
      background: rgba(217, 119, 6, 0.15);
      color: #d97706;
      border-color: rgba(217, 119, 6, 0.35);
    }

    .badge-statpearls---ncbi-bookshelf,
    .badge-litfl-ecg-compendium {
      background: rgba(100, 116, 139, 0.15);
      color: #64748b;
      border-color: rgba(100, 116, 139, 0.35);
    }

    .ref-evidence-badge {
      font-size: 0.7rem;
      font-weight: 500;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      background: var(--bg-surface-subtle);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
    }

    .ref-direct-link-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.78rem;
      font-weight: 700;
      padding: 0.25rem 0.65rem;
      border-radius: 6px;
      background: var(--accent-primary-subtle);
      color: var(--accent-primary);
      border: 1px solid var(--accent-primary);
      text-decoration: none;
      transition: all 0.15s ease;
    }

    .ref-direct-link-btn:hover {
      background: var(--accent-primary);
      color: #ffffff;
      transform: translateY(-1px);
      box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }

    .ref-card-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      margin: 0.25rem 0 0.35rem 0;
      line-height: 1.35;
    }

    .ref-card-citation {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-style: italic;
      margin-bottom: 0.75rem;
      line-height: 1.4;
    }

    .ref-sourced-box {
      border-radius: 8px;
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-subtle);
      padding: 0.75rem 0.95rem;
      margin-top: 0.5rem;
    }

    .ref-sourced-label {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.76rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      margin-bottom: 0.4rem;
    }

    .ref-sourced-list {
      margin: 0;
      padding-left: 1.25rem;
      color: var(--text-soft);
    }

    .ref-sourced-list li {
      margin-bottom: 0.25rem;
    }

    /* Jump Pulse Animation */
    @keyframes refPulse {
      0% {
        box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7);
        border-color: var(--accent-primary);
        background: var(--accent-primary-subtle);
      }
      50% {
        box-shadow: 0 0 20px 4px rgba(56, 189, 248, 0.4);
        border-color: var(--accent-primary);
        background: var(--accent-primary-subtle);
      }
      100% {
        box-shadow: none;
      }
    }

    .ref-item-card.ref-card-highlighted {
      animation: refPulse 2s ease-out;
      border-color: var(--accent-primary) !important;
    }

    /* High-Yield Filter Active Mode */
    body.hy-filter-active .yield-low {
      display: none !important;
    }

    .hy-banner {
      display: none;
      align-items: center;
      justify-content: space-between;
      padding: 0.65rem 1rem;
      background: rgba(234, 179, 8, 0.15);
      border: 1px solid rgba(234, 179, 8, 0.3);
      border-radius: 8px;
      margin-bottom: 1.25rem;
      font-size: 0.85rem;
      color: #ca8a04;
    }

    body.hy-filter-active .hy-banner {
      display: flex;
    }

    /* Clinical Photo Figure */
    .clinical-figure {
      margin: 1.5rem 0;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      overflow: hidden;
      background: var(--bg-surface);
      box-shadow: var(--card-emboss);
    }

    .clinical-img-wrap {
      background: #000;
      display: flex;
      align-items: center;
      justify-content: center;
      max-height: 480px;
      overflow: hidden;
      cursor: zoom-in;
    }

    .clinical-img-wrap img {
      width: 100%;
      height: auto;
      object-fit: contain;
      display: block;
      transition: transform 0.2s ease;
    }

    .clinical-img-wrap:hover img {
      transform: scale(1.02);
    }

    .clinical-caption {
      padding: 0.75rem 1rem;
      font-size: 0.84rem;
      color: var(--text-muted);
      border-top: 1px solid var(--border-subtle);
      background: var(--bg-surface-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }

    /* Lightbox Modal */
    .lightbox-modal {
      position: fixed;
      inset: 0;
      z-index: 1000;
      background: rgba(0, 0, 0, 0.88);
      display: none;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      padding: 1.5rem;
    }

    .lightbox-modal img {
      max-width: 90vw;
      max-height: 82vh;
      border-radius: 8px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.8);
      object-fit: contain;
    }

    #lightbox-caption {
      color: #fff;
      margin-top: 1rem;
      font-size: 0.95rem;
      max-width: 700px;
      text-align: center;
    }

    .close-lightbox {
      position: absolute;
      top: 1.25rem;
      right: 1.5rem;
      color: #fff;
      font-size: 2rem;
      cursor: pointer;
    }

    /* Tooltip / Glossary Popover */
    .tooltip-popover {
      position: absolute;
      z-index: 300;
      width: 320px;
      padding: 1rem;
      border-radius: 10px;
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
      display: none;
    }

    .tooltip-header {
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--accent-primary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.25rem;
    }

    .tooltip-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 0.45rem;
    }

    .tooltip-desc {
      font-size: 0.84rem;
      color: var(--text-soft);
      line-height: 1.5;
      margin-bottom: 0.65rem;
    }

    .tooltip-pearl {
      font-size: 0.78rem;
      padding: 0.4rem 0.6rem;
      border-radius: 6px;
      background: var(--pearl-bg);
      color: var(--pearl-text);
      border: 1px solid var(--pearl-border);
    }

    /* Command Search Modal */
    .search-modal {
      position: fixed;
      inset: 0;
      z-index: 500;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px);
      display: none;
      align-items: flex-start;
      justify-content: center;
      padding-top: 5rem;
    }

    .search-modal-box {
      width: 100%;
      max-width: 620px;
      background: var(--bg-surface);
      border: 1px solid var(--border-medium);
      border-radius: 12px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.4);
      overflow: hidden;
      animation: modalSlide 0.2s ease;
    }

    @keyframes modalSlide {
      from { opacity: 0; transform: translateY(-12px) scale(0.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .search-input-wrap {
      padding: 1.1rem 1.35rem;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .search-input-wrap input {
      flex: 1;
      font-size: 1.1rem;
      color: var(--text-main);
      border: none;
      background: transparent;
    }

    .search-results-list {
      max-height: 380px;
      overflow-y: auto;
      padding: 0.5rem;
    }

    .search-result-item {
      padding: 0.75rem 1rem;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      transition: background 0.15s ease;
    }

    .search-result-item:hover {
      background: var(--bg-surface-subtle);
    }

    /* Responsive Mobile Overrides */
    @media (max-width: 860px) {
      .workspace-grid {
        grid-template-columns: minmax(0, 1fr);
      }
      .left-sidebar {
        display: none;
        position: fixed;
        top: 64px;
        left: 0;
        bottom: 0;
        width: 290px;
        z-index: 99;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
      }
      .left-sidebar.mobile-open {
        display: flex !important;
      }
      .center-content {
        padding: 1.5rem 1.15rem;
      }
      .search-btn {
        min-width: unset;
      }
      .search-btn span, .search-btn .kbd-badge {
        display: none;
      }
      #mobile-nav-toggle {
        display: inline-flex !important;
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
      <button id="mobile-nav-toggle" class="icon-only-btn" style="display: none;" title="Toggle Navigation Sidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
      </button>

      <button onclick="window.medbase.goHome()" class="brand-link">
        <div class="logo-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg>
        </div>
        <span>MedBase</span>
      </button>
    </div>

    <!-- Command Search Button -->
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

      <!-- Font Size Controller (A- / 100% / A+) -->
      <div class="font-size-group" title="Adjust Clinical Text Size">
        <button id="font-decrease-btn" class="font-tool-btn" title="Decrease font size (A-)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 19L9.5 4h1L16 19"/><path d="M6.5 13.5h7"/><line x1="18" y1="12" x2="22" y2="12"/></svg>
        </button>
        <button id="font-reset-btn" class="font-size-indicator" title="Reset font size to 100%">
          <span id="font-size-text">100%</span>
        </button>
        <button id="font-increase-btn" class="font-tool-btn" title="Increase font size (A+)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 19L9.5 4h1L16 19"/><path d="M6.5 13.5h7"/><line x1="20" y1="9" x2="20" y2="15"/><line x1="17" y1="12" x2="23" y2="12"/></svg>
        </button>
      </div>

      <!-- 3-Way Theme Switcher (Dark -> Sepia -> Light) -->
      <button id="toggle-theme-btn" class="theme-toggle-btn" title="Cycle Theme: Dark ➔ Sepia ➔ Light">
        <span id="theme-icon-wrap">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
        </span>
        <span id="theme-label" style="text-transform: capitalize;">Dark</span>
      </button>
    </div>
  </header>

  <!-- ========================================================================
       2-COLUMN WORKSPACE (Left Navigation + Center View Area)
       ======================================================================== -->
  <div class="workspace-grid">
    
    <!-- LEFT SIDEBAR: Outline & Library -->
    <aside class="left-sidebar">
      <div class="sidebar-tabs">
        <button class="sidebar-tab-btn active" data-tab="library">Library Tree</button>
        <button class="sidebar-tab-btn" data-tab="outline">Article Outline</button>
      </div>
      
      <div class="sidebar-content-pane" id="pane-library">
        <div id="library-container">
          <!-- Library tree nodes populated via JS -->
        </div>
      </div>

      <div class="sidebar-content-pane" id="pane-outline" style="display: none;">
        <div style="font-size:0.78rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:0.75rem; letter-spacing:0.04em;">TABLE OF CONTENTS</div>
        <div id="toc-container">
          <!-- Populated dynamically per article -->
        </div>
      </div>
    </aside>

    <!-- CENTER CONTENT VIEWPORT -->
    <main class="center-content">
      
      <!-- ====================================================================
           VIEW 1: HOME LIBRARY PORTAL VIEW
           ==================================================================== -->
      <div id="home-view">
        <div class="home-hero">
          <h1>Clinical Knowledge Library</h1>
          <p>Evidence-based clinical monographs, diagnostic algorithms, USMLE Step 2 CK high-yield pearls, and acute emergency management protocols.</p>
        </div>

        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;">
          <h2 style="font-size: 1.35rem; font-weight: 700;">Library Categories</h2>
          <span style="font-size: 0.82rem; color: var(--text-muted);">Select a clinical topic to begin</span>
        </div>

        <div class="home-categories-grid">
          <!-- Internal Medicine Card -->
          <div class="category-card">
            <div class="category-card-header">
              <div class="category-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
              </div>
              <div>
                <h3 class="category-card-title">Cardiology & Vascular</h3>
                <span style="font-size: 0.78rem; color: var(--text-muted);">2 Clinical Monograph Topics</span>
              </div>
            </div>
            <div class="article-pill-list">
              <div class="article-item-card" onclick="window.medbase.selectArticle('acs')">
                <div>
                  <div style="font-weight: 600; font-size: 0.92rem;">Acute Coronary Syndrome (ACS)</div>
                  <div style="font-size: 0.76rem; color: var(--text-muted);">STEMI, NSTEMI, Unstable Angina, ECGs & Primary PCI</div>
                </div>
                <span class="section-badge" style="background: rgba(234,179,8,0.15); color: #ca8a04;">Step 2 Core</span>
              </div>
              <div class="article-item-card" onclick="window.medbase.selectArticle('hf')">
                <div>
                  <div style="font-weight: 600; font-size: 0.92rem;">Heart Failure (HFrEF & HFpEF)</div>
                  <div style="font-size: 0.76rem; color: var(--text-muted);">NYHA, Framingham, GDMT 4-Pillars & Inotropes</div>
                </div>
                <span class="section-badge" style="background: rgba(234,179,8,0.15); color: #ca8a04;">GDMT</span>
              </div>
            </div>
          </div>

          <!-- Pulmonology Card -->
          <div class="category-card">
            <div class="category-card-header">
              <div class="category-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2h8M9 2v4a3 3 0 0 0 6 0V2M12 6v16M6 13a6 6 0 0 0 6 6M18 13a6 6 0 0 1-6 6"/></svg>
              </div>
              <div>
                <h3 class="category-card-title">Pulmonology & Critical Care</h3>
                <span style="font-size: 0.78rem; color: var(--text-muted);">1 Clinical Monograph Topic</span>
              </div>
            </div>
            <div class="article-pill-list">
              <div class="article-item-card" onclick="window.medbase.selectArticle('cap')">
                <div>
                  <div style="font-weight: 600; font-size: 0.92rem;">Community-Acquired Pneumonia</div>
                  <div style="font-size: 0.76rem; color: var(--text-muted);">CURB-65, Typical vs Atypical, Empiric Antibiotics</div>
                </div>
                <span class="section-badge" style="background: rgba(2,132,199,0.15); color: #0284c7;">High Yield</span>
              </div>
            </div>
          </div>

          <!-- Endocrinology Card -->
          <div class="category-card">
            <div class="category-card-header">
              <div class="category-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/></svg>
              </div>
              <div>
                <h3 class="category-card-title">Endocrine Emergencies</h3>
                <span style="font-size: 0.78rem; color: var(--text-muted);">1 Emergency Monograph Topic</span>
              </div>
            </div>
            <div class="article-pill-list">
              <div class="article-item-card" onclick="window.medbase.selectArticle('dka')">
                <div>
                  <div style="font-weight: 600; font-size: 0.92rem;">Diabetic Ketoacidosis (DKA)</div>
                  <div style="font-size: 0.76rem; color: var(--text-muted);">Triad, Fluids, Potassium & Syringe Pump Protocols</div>
                </div>
                <span class="section-badge" style="background: rgba(244,63,94,0.15); color: #f43f5e;">Emergency</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ====================================================================
           VIEW 2: ARTICLE CLINICAL MONOGRAPH VIEW
           ==================================================================== -->
      <div id="article-view" style="display: none;">
        <div class="article-header">
          <div class="breadcrumbs" id="article-breadcrumbs">
            <a href="javascript:void(0)" onclick="window.medbase.goHome()">Library Home</a> / <span>Internal Medicine</span> / <span>Cardiology</span>
          </div>
          <h1 class="article-title" id="article-title">Acute Coronary Syndrome (ACS)</h1>
          
          <div class="article-meta-row">
            <span class="meta-pill" id="article-updated">Nov 2026</span>
            <span class="meta-pill" id="article-readtime">12 min read</span>
            <span class="meta-pill pill-hy" id="article-hytag">Core Shelf & Step 2 CK</span>
            <button id="expand-all-btn" class="tool-btn" style="margin-left: auto; font-size: 0.78rem;">Expand All</button>
          </div>

          <!-- Sourced From & Evidence Base Banner -->
          <div class="article-sources-banner" id="article-sources-banner" onclick="window.medbase.scrollToReferences()">
            <div class="sources-banner-left">
              <span class="sources-icon">📚</span>
              <span class="sources-label">Sourced From:</span>
              <div class="sources-pill-row" id="article-sources-tags">
                <span class="source-tag-chip">AMBOSS</span>
                <span class="source-tag-chip">Osmosis</span>
                <span class="source-tag-chip">First Aid Step 2 CK</span>
                <span class="source-tag-chip">Clinical Guidelines</span>
                <span class="source-tag-chip">Doctor on Duty</span>
              </div>
            </div>
            <span class="sources-jump-hint" id="article-sources-count">View Sources & Direct Links ↗</span>
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

        <!-- Rendered Sections Container -->
        <div id="article-sections-container">
          <!-- Accordion section cards injected dynamically -->
        </div>
      </div>

    </main>
  </div>

  <!-- ========================================================================
       MODALS: SEARCH, TOOLTIP & LIGHTBOX
       ======================================================================== -->
  
  <!-- Command Search Modal (Ctrl+K) -->
  <div id="search-modal" class="search-modal">
    <div class="search-modal-box">
      <div class="search-input-wrap">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input type="text" id="modal-search-input" placeholder="Search conditions, algorithms, ECGs, references..." autocomplete="off" />
        <kbd class="kbd-badge">ESC</kbd>
      </div>
      <div class="search-results-list" id="search-results-list">
        <!-- Results injected dynamically -->
      </div>
    </div>
  </div>

  <!-- Glossary Tooltip Popover -->
  <div id="tooltip-popover" class="tooltip-popover">
    <div class="tooltip-header" id="tt-category">CLINICAL TERM</div>
    <div class="tooltip-title" id="tt-title">Term Title</div>
    <div class="tooltip-desc" id="tt-desc">Term definition...</div>
    <div class="tooltip-pearl" id="tt-pearl" style="display: none;"></div>
    <div style="margin-top: 0.75rem; text-align: right;">
      <button id="tt-jump-btn" style="font-size: 0.78rem; font-weight: 600; color: var(--accent-primary); text-decoration: underline;">Open Topic →</button>
    </div>
  </div>

  <!-- Lightbox Modal -->
  <div id="lightbox-modal" class="lightbox-modal">
    <div class="close-lightbox" id="close-lightbox-btn">&times;</div>
    <img id="lightbox-img" src="" alt="Enlarged clinical photo" />
    <div id="lightbox-caption"></div>
  </div>

  <!-- EMBEDDED MEDBASE DATA (EXPOSED GLOBALLY) -->
  <script>
    window.MEDBASE_DATA = """ + json.dumps(med_data, ensure_ascii=False) + r""";
    var MEDBASE_DATA = window.MEDBASE_DATA;
  </script>

  <!-- ========================================================================
       STANDALONE JAVASCRIPT APPLICATION ENGINE
       ======================================================================== -->
  <script>
  (function() {
    'use strict';

    const themes = ['dark', 'sepia', 'light'];
    let savedTheme = localStorage.getItem('dod_theme') || localStorage.getItem('medbase_theme') || 'dark';
    if (!themes.includes(savedTheme)) savedTheme = 'dark';

    const FONT_SCALES = [0.85, 1.0, 1.15, 1.30, 1.50];
    let savedFontScale = parseFloat(localStorage.getItem('medbase_font_scale')) || 1.0;
    if (!FONT_SCALES.includes(savedFontScale)) savedFontScale = 1.0;

    const state = {
      currentView: 'home', // 'home' or 'article'
      activeArticleId: 'acs',
      theme: savedTheme,
      fontScale: savedFontScale,
      highYieldOnly: false,
      highlightsActive: true,
      quizModeActive: false,
      revealedBlanks: new Set(),
      allBlankIds: [],
      onDutyModeActive: false,
      searchQuery: '',
      activeTooltipTerm: null
    };

    // --- DOM Elements ---
    const els = {
      themeBtn: document.getElementById('toggle-theme-btn'),
      themeLabel: document.getElementById('theme-label'),
      themeIconWrap: document.getElementById('theme-icon-wrap'),
      fontDecBtn: document.getElementById('font-decrease-btn'),
      fontIncBtn: document.getElementById('font-increase-btn'),
      fontResetBtn: document.getElementById('font-reset-btn'),
      fontSizeText: document.getElementById('font-size-text'),
      hyBtn: document.getElementById('toggle-hy-btn'),
      highlightsBtn: document.getElementById('toggle-highlights-btn'),
      quizBtn: document.getElementById('toggle-quiz-btn'),
      quizBadge: document.getElementById('quiz-count-badge'),
      erBtn: document.getElementById('toggle-er-btn'),
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
      homeView: document.getElementById('home-view'),
      articleView: document.getElementById('article-view'),
      mobileNavBtn: document.getElementById('mobile-nav-toggle'),
      leftSidebar: document.querySelector('.left-sidebar')
    };

    // --- Theme Engine ---
    function applyTheme(th) {
      state.theme = th;
      document.documentElement.setAttribute('data-theme', th);
      localStorage.setItem('dod_theme', th);
      localStorage.setItem('medbase_theme', th);

      if (els.themeLabel) {
        els.themeLabel.textContent = th;
      }
      if (els.themeIconWrap) {
        if (th === 'dark') {
          els.themeIconWrap.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>';
        } else if (th === 'sepia') {
          els.themeIconWrap.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>';
        } else {
          els.themeIconWrap.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
        }
      }
    }

    function cycleTheme() {
      const idx = themes.indexOf(state.theme);
      const nextTheme = themes[(idx + 1) % themes.length];
      applyTheme(nextTheme);
    }

    // Apply initial theme
    applyTheme(state.theme);
    if (state.highlightsActive) document.body.classList.add('highlights-active');

    // --- Font Scaling Engine ---
    function applyFontScale(scale) {
      state.fontScale = scale;
      document.documentElement.style.setProperty('--font-scale', scale);
      localStorage.setItem('medbase_font_scale', scale);
      if (els.fontSizeText) {
        els.fontSizeText.textContent = `${Math.round(scale * 100)}%`;
      }
    }

    function changeFontScale(delta) {
      let currentIdx = FONT_SCALES.findIndex(s => Math.abs(s - state.fontScale) < 0.05);
      if (currentIdx === -1) currentIdx = 1;
      let nextIdx = currentIdx + delta;
      if (nextIdx < 0) nextIdx = 0;
      if (nextIdx >= FONT_SCALES.length) nextIdx = FONT_SCALES.length - 1;
      applyFontScale(FONT_SCALES[nextIdx]);
    }

    // Initialize font scale
    applyFontScale(state.fontScale);

    // --- View Navigation ---
    function goHome() {
      state.currentView = 'home';
      els.homeView.style.display = 'block';
      els.articleView.style.display = 'none';

      const libTab = document.querySelector('.sidebar-tab-btn[data-tab="library"]');
      if (libTab) libTab.click();

      if (els.leftSidebar && els.leftSidebar.classList.contains('mobile-open')) {
        els.leftSidebar.classList.remove('mobile-open');
      }

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function selectArticle(id) {
      state.currentView = 'article';
      state.activeArticleId = id;
      els.homeView.style.display = 'none';
      els.articleView.style.display = 'block';

      renderArticle(id);
      renderLibraryTree();

      const outlineTab = document.querySelector('.sidebar-tab-btn[data-tab="outline"]');
      if (outlineTab) outlineTab.click();

      if (els.leftSidebar && els.leftSidebar.classList.contains('mobile-open')) {
        els.leftSidebar.classList.remove('mobile-open');
      }

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

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
        const refPos = remaining.indexOf('[[ref:');

        // Check for markdown links [text](url)
        let linkPos = -1;
        let linkMatch = null;
        let scanPos = 0;
        while (scanPos < remaining.length) {
          const p = remaining.indexOf('[', scanPos);
          if (p === -1) break;
          if (remaining[p + 1] === '[') {
            scanPos = p + 2;
            continue;
          }
          const m = remaining.slice(p).match(/^\[([^\]]+)\]\((https?:[^\s)]+)\)/);
          if (m) {
            linkPos = p;
            linkMatch = m;
            break;
          }
          scanPos = p + 1;
        }

        const candidates = [
          { type: 'hl', pos: hlPos },
          { type: 'term', pos: termPos },
          { type: 'bold', pos: boldPos },
          { type: 'ref', pos: refPos },
          { type: 'link', pos: linkPos, match: linkMatch }
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
        } else if (next.type === 'ref') {
          const start = next.pos + 6;
          const end = remaining.indexOf(']]', start);
          if (end === -1) {
            res += escapeHtml(remaining.slice(next.pos));
            break;
          }
          const inner = remaining.slice(start, end);
          const pipeIdx = inner.indexOf('|');
          const refId = pipeIdx !== -1 ? inner.slice(0, pipeIdx).trim() : inner.trim();
          const label = pipeIdx !== -1 ? inner.slice(pipeIdx + 1).trim() : refId;
          
          res += `<button type="button" class="inline-ref-tag" data-ref-id="${escapeHtml(refId)}" onclick="window.medbase.jumpToRef('${escapeHtml(refId)}', event)" title="Jump to verified source: ${escapeHtml(label)}">[${escapeHtml(label)} ↗]</button>`;
          remaining = remaining.slice(end + 2);
        } else if (next.type === 'link') {
          const label = next.match[1];
          const url = next.match[2];
          res += `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer" class="external-inline-link">${escapeHtml(label)} <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a>`;
          remaining = remaining.slice(next.pos + next.match[0].length);
        }
      }
      return res;
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // --- Render Bullet Tree ---
    function renderBulletTree(items, keyPrefix) {
      if (!items || items.length === 0) return '';
      let html = '<ul class="content-tree">';
      items.forEach((item, idx) => {
        const itemKey = `${keyPrefix}-${idx}`;
        const isLowYield = item.yield === 'low' ? 'yield-low' : '';
        html += `<li class="content-node ${isLowYield}">`;
        html += parseInline(item.text, itemKey);
        if (item.children && item.children.length > 0) {
          html += renderBulletTree(item.children, itemKey);
        }
        html += '</li>';
      });
      html += '</ul>';
      return html;
    }

    // --- Render Callout Box ---
    function renderCallout(block, keyPrefix) {
      const type = block.calloutType || 'pearl';
      let icon = '💡';
      let typeClass = 'callout-pearl';
      if (type === 'danger' || type === 'redflag') {
        icon = '⚠️';
        typeClass = 'callout-danger';
      } else if (type === 'rx' || type === 'pharm') {
        icon = '💊';
        typeClass = 'callout-rx';
      } else if (type === 'diag') {
        icon = '🩺';
        typeClass = 'callout-diag';
      }

      return `
        <div class="callout-box ${typeClass}">
          <div class="callout-icon">${icon}</div>
          <div class="callout-content">
            <div class="callout-title">${escapeHtml(block.title || 'Clinical Pearl')}</div>
            <div class="callout-text">${parseInline(block.text, keyPrefix)}</div>
          </div>
        </div>
      `;
    }

    // --- Render Table ---
    function renderTable(block, keyPrefix) {
      let html = '<div class="table-wrap"><table class="clinical-table">';
      if (block.headers && block.headers.length > 0) {
        html += '<thead><tr>';
        block.headers.forEach(h => {
          html += `<th>${escapeHtml(h)}</th>`;
        });
        html += '</tr></thead>';
      }
      html += '<tbody>';
      (block.rows || []).forEach((row, rIdx) => {
        html += '<tr>';
        row.forEach((cell, cIdx) => {
          html += `<td>${parseInline(cell, `${keyPrefix}-r${rIdx}c${cIdx}`)}</td>`;
        });
        html += '</tr>';
      });
      html += '</tbody></table></div>';
      return html;
    }

    // --- Render Clinical Figure Slot ---
    function renderClinicalFigure(fig, secId) {
      if (!fig || !fig.src) return '';
      return `
        <div class="clinical-figure" id="fig-${secId}">
          <div class="clinical-img-wrap" onclick="window.medbase.openLightbox('${fig.src}', '${escapeHtml(fig.caption || 'Clinical Image')}')">
            <img src="${fig.src}" alt="${escapeHtml(fig.caption || 'Clinical Diagnostic Image')}" loading="lazy" />
          </div>
          <div class="clinical-caption">
            <span>📷 ${escapeHtml(fig.caption || 'Clinical Diagnostic Image')}</span>
            <label style="cursor: pointer; font-size: 0.76rem; color: var(--accent-primary); font-weight: 600;">
              <input type="file" accept="image/*" style="display:none;" onchange="window.medbase.handleImageUpload('${secId}', event)" />
              Replace Photo
            </label>
          </div>
        </div>
      `;
    }

    // --- Render Blocks ---
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
      const art = (window.MEDBASE_DATA && window.MEDBASE_DATA.ARTICLES) ? window.MEDBASE_DATA.ARTICLES[artId] : null;
      if (!art) return;
      state.activeArticleId = artId;
      state.allBlankIds = [];

      // Header info
      document.getElementById('article-title').textContent = art.title;
      document.getElementById('article-breadcrumbs').innerHTML = `<a href="javascript:void(0)" onclick="window.medbase.goHome()">Library Home</a> / ` + (art.breadcrumbs || ['Internal Medicine']).map(b => `<span>${escapeHtml(b)}</span>`).join(' / ');
      document.getElementById('article-updated').textContent = art.lastUpdated || 'Nov 2026';
      document.getElementById('article-readtime').textContent = art.readTime || '10 min read';
      document.getElementById('article-hytag').textContent = art.highYieldTag || 'Core High-Yield';
      document.getElementById('article-summary').innerHTML = parseInline(art.summary || '', 'sum');

      // Update Sources Header Banner
      const refs = art.references || [];
      const sourcesBanner = document.getElementById('article-sources-banner');
      if (sourcesBanner) {
        if (refs.length > 0) {
          sourcesBanner.style.display = 'flex';
          const types = Array.from(new Set(refs.map(r => (r.sourceType || '').split(' ')[0]))).filter(Boolean).slice(0, 5);
          const tagsHtml = types.map(t => `<span class="source-tag-chip">${escapeHtml(t)}</span>`).join('');
          const countEl = document.getElementById('article-sources-count');
          const tagsEl = document.getElementById('article-sources-tags');
          if (tagsEl) tagsEl.innerHTML = tagsHtml;
          if (countEl) countEl.innerHTML = `View ${refs.length} Sources & Direct Links ↗`;
        } else {
          sourcesBanner.style.display = 'none';
        }
      }

      // Sections
      let secHtml = '';
      let tocHtml = '';

      (art.sections || []).forEach((sec, sIdx) => {
        const secKey = `sec-${sec.id}`;
        tocHtml += `<a href="#${secKey}" class="toc-item" data-sec-id="${sec.id}">${sec.title}</a>`;

        const figSrc = sec.id.includes("ecg") || sec.id.includes("acs-diag") ? "img/acs_ecg.jpg" :
                       sec.id.includes("cap") ? "img/cap_cxr.jpg" :
                       sec.id.includes("hf") ? "img/hf_echo.jpg" :
                       sec.id.includes("dka") ? "img/dka_algorithm.jpg" : "";

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
              ${renderClinicalFigure({ src: figSrc, caption: `${sec.title} — Key Diagnostic & Clinical Findings` }, sec.id)}
            </div>
          </div>
        `;
      });

      // Render Dedicated References & Evidence Base Card
      if (refs.length > 0) {
        const refSecKey = 'sec-references';
        tocHtml += `<a href="#${refSecKey}" class="toc-item" data-sec-id="references">📚 References & Evidence (${refs.length})</a>`;

        let refCardsHtml = '';
        refs.forEach((ref, rIdx) => {
          const badgeClass = ref.sourceType ? `badge-${ref.sourceType.toLowerCase().replace(/[^a-z0-9]/g, '-')}` : '';
          refCardsHtml += `
            <div class="ref-item-card" id="${ref.id}">
              <div class="ref-card-header">
                <div class="ref-badge-group">
                  <span class="ref-num-badge">#${rIdx + 1}</span>
                  <span class="ref-source-badge ${badgeClass}">${escapeHtml(ref.sourceType || 'Reference')}</span>
                  ${ref.evidenceLevel ? `<span class="ref-evidence-badge">${escapeHtml(ref.evidenceLevel)}</span>` : ''}
                </div>
                ${ref.url ? `
                  <a href="${escapeHtml(ref.url)}" target="_blank" rel="noopener noreferrer" class="ref-direct-link-btn" title="Open source in new window">
                    <span>Direct Link</span>
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                  </a>
                ` : ''}
              </div>
              <h4 class="ref-card-title">${escapeHtml(ref.title)}</h4>
              ${ref.citation ? `<div class="ref-card-citation">${escapeHtml(ref.citation)}</div>` : ''}
              ${(ref.sourcedContent && ref.sourcedContent.length > 0) ? `
                <div class="ref-sourced-box">
                  <div class="ref-sourced-label">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
                    <span>Exact Information Sourced From Here:</span>
                  </div>
                  <ul class="ref-sourced-list">
                    ${ref.sourcedContent.map(item => `<li>${parseInline(item, `ref-c-${rIdx}`)}</li>`).join('')}
                  </ul>
                </div>
              ` : ''}
            </div>
          `;
        });

        secHtml += `
          <div class="amboss-card references-card" id="${refSecKey}" data-section-id="references">
            <button class="accordion-header" onclick="window.medbase.toggleSection('${refSecKey}')">
              <div class="title-wrap">
                <span class="section-badge" style="background:var(--accent-primary-subtle); color:var(--accent-primary);">§ Ref</span>
                <span>📚 References, Evidence Base & Source Origins</span>
              </div>
              <div style="display:flex; align-items:center; gap:0.6rem;">
                <span class="ref-total-badge">${refs.length} Verified Sources</span>
                <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
            </button>
            <div class="accordion-body">
              <div class="ref-disclaimer">
                <div class="ref-disclaimer-icon">💡</div>
                <div class="ref-disclaimer-text">
                  <strong>Transparent Evidence Attribution:</strong> All clinical facts, diagnostic cutoffs, criteria, and pharmacotherapy dosages in MedBase are cross-referenced with international clinical society guidelines (ACC/AHA, ESC, ATS/IDSA, ADA), leading medical learning platforms (AMBOSS, Osmosis), USMLE Step 2 CK curricula, and bedside emergency ward protocols (Doctor on Duty 3rd Ed). Click any direct link below to verify the primary source.
                </div>
              </div>
              <div class="ref-cards-grid">
                ${refCardsHtml}
              </div>
            </div>
          </div>
        `;
      }

      els.sectionsContainer.innerHTML = secHtml;
      els.tocContainer.innerHTML = tocHtml;

      setupScrollspy();
      updateQuizBadge();
    }

    // --- Render Library Tree ---
    function renderLibraryTree() {
      let html = '';
      const tree = (window.MEDBASE_DATA && window.MEDBASE_DATA.LIBRARY_TREE) || [];
      tree.forEach(cat => {
        html += `<div class="library-node">`;
        html += `<div class="library-node-title"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/></svg> <span>${cat.label}</span></div>`;
        html += `<div class="library-children">`;
        (cat.children || []).forEach(subCat => {
          html += `<div style="font-weight:600; font-size:0.8rem; color:var(--text-muted); margin:0.35rem 0 0.15rem 0.25rem;">${subCat.label}</div>`;
          (subCat.children || []).forEach(art => {
            const isActive = state.currentView === 'article' && art.articleId === state.activeArticleId ? 'active' : '';
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
      if (cards.length === 0 || tocLinks.length === 0) return;

      window.addEventListener('scroll', () => {
        let currentId = '';
        cards.forEach(card => {
          const top = card.getBoundingClientRect().top;
          if (top <= 140) {
            currentId = card.getAttribute('data-section-id');
          }
        });

        if (currentId) {
          tocLinks.forEach(link => {
            link.classList.toggle('active', link.getAttribute('data-sec-id') === currentId);
          });
        }
      });
    }

    // --- Tooltip Logic ---
    function showTooltip(termId, event) {
      if (state.quizModeActive) return;
      const term = window.MEDBASE_DATA && window.MEDBASE_DATA.MEDICAL_GLOSSARY && window.MEDBASE_DATA.MEDICAL_GLOSSARY[termId];
      if (!term) return;

      state.activeTooltipTerm = term;
      els.ttCategory.textContent = term.category || 'CLINICAL TERM';
      els.ttTitle.textContent = term.title || termId;
      els.ttDesc.textContent = term.definition || '';

      if (term.pearl) {
        els.ttPearl.style.display = 'block';
        els.ttPearl.textContent = `💡 Pearl: ${term.pearl}`;
      } else {
        els.ttPearl.style.display = 'none';
      }

      if (term.articleId) {
        els.ttJumpBtn.style.display = 'inline-block';
        els.ttJumpBtn.onclick = () => {
          selectArticle(term.articleId);
          if (term.sectionId) {
            setTimeout(() => {
              const target = document.getElementById(`sec-${term.sectionId}`);
              if (target) target.scrollIntoView({ behavior: 'smooth' });
            }, 100);
          }
          els.tooltip.style.display = 'none';
        };
      } else {
        els.ttJumpBtn.style.display = 'none';
      }

      // Position tooltip near cursor
      const rect = event.target.getBoundingClientRect();
      els.tooltip.style.left = `${Math.min(window.innerWidth - 340, Math.max(10, rect.left))}px`;
      els.tooltip.style.top = `${rect.bottom + window.scrollY + 8}px`;
      els.tooltip.style.display = 'block';
    }

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.glossary-term') && !e.target.closest('.tooltip-popover')) {
        els.tooltip.style.display = 'none';
      }
    });

    // --- Search Modal Engine ---
    function performSearch(query) {
      if (!query || query.trim() === '') {
        els.searchResults.innerHTML = '<div style="padding:1rem; color:var(--text-muted); text-align:center;">Type to search clinical conditions, algorithms, ECG signs, references, and guidelines...</div>';
        return;
      }
      const q = query.toLowerCase().trim();
      let matches = [];

      const arts = (window.MEDBASE_DATA && window.MEDBASE_DATA.ARTICLES) || {};
      Object.entries(arts).forEach(([aId, art]) => {
        if (art.title.toLowerCase().includes(q)) {
          matches.push({ type: 'Article', title: art.title, desc: art.summary, action: () => { selectArticle(aId); closeSearch(); } });
        }
        (art.sections || []).forEach(sec => {
          if (sec.title.toLowerCase().includes(q)) {
            matches.push({ type: 'Section', title: `${art.title} → ${sec.title}`, desc: 'Article section', action: () => { selectArticle(aId); setTimeout(() => { const t = document.getElementById(`sec-${sec.id}`); if (t) t.scrollIntoView({ behavior: 'smooth' }); }, 100); closeSearch(); } });
          }
        });

        // Search references
        (art.references || []).forEach(ref => {
          if (
            (ref.title && ref.title.toLowerCase().includes(q)) ||
            (ref.sourceType && ref.sourceType.toLowerCase().includes(q)) ||
            (ref.citation && ref.citation.toLowerCase().includes(q)) ||
            (ref.sourcedContent && ref.sourcedContent.some(c => c.toLowerCase().includes(q)))
          ) {
            matches.push({
              type: `Reference (${ref.sourceType})`,
              title: `${art.title} → ${ref.title}`,
              desc: (ref.sourcedContent && ref.sourcedContent[0]) ? ref.sourcedContent[0] : (ref.citation || ref.url),
              action: () => {
                selectArticle(aId);
                setTimeout(() => {
                  window.medbase.jumpToRef(ref.id);
                }, 150);
                closeSearch();
              }
            });
          }
        });
      });

      const glossary = (window.MEDBASE_DATA && window.MEDBASE_DATA.MEDICAL_GLOSSARY) || {};
      Object.entries(glossary).forEach(([tId, term]) => {
        if (term.title.toLowerCase().includes(q) || (term.definition && term.definition.toLowerCase().includes(q))) {
          matches.push({
            type: term.category || 'Term',
            title: term.title,
            desc: term.definition,
            action: () => {
              if (term.articleId) selectArticle(term.articleId);
              if (term.sectionId) setTimeout(() => { const t = document.getElementById(`sec-${term.sectionId}`); if (t) t.scrollIntoView({ behavior: 'smooth' }); }, 100);
              closeSearch();
            }
          });
        }
      });

      if (matches.length === 0) {
        els.searchResults.innerHTML = `<div style="padding:1rem; color:var(--text-muted); text-align:center;">No matching clinical results for "${escapeHtml(query)}"</div>`;
        return;
      }

      els.searchResults.innerHTML = matches.slice(0, 12).map((m, idx) => `
        <div class="search-result-item" onclick="window.medbase.execSearchAction(${idx})">
          <div>
            <div style="font-weight:600; font-size:0.95rem; color:var(--text-main);">${escapeHtml(m.title)}</div>
            <div style="font-size:0.78rem; color:var(--text-muted); max-width:480px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${escapeHtml(m.desc)}</div>
          </div>
          <span class="section-badge">${escapeHtml(m.type)}</span>
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

    function updateQuizBadge() {
      if (!state.quizModeActive) {
        els.quizBadge.style.display = 'none';
        return;
      }
      els.quizBadge.style.display = 'inline-block';
      els.quizBadge.textContent = `${state.revealedBlanks.size}/${state.allBlankIds.length}`;
    }

    // --- Global Window API ---
    window.medbase = {
      goHome: goHome,
      selectArticle: (id) => selectArticle(id),
      toggleSection: (secKey) => {
        const card = document.getElementById(secKey);
        if (card) card.classList.toggle('collapsed');
      },
      toggleSubAccordion: (subKey) => {
        const sub = document.getElementById(subKey);
        if (sub) sub.classList.toggle('collapsed');
      },
      showTooltip: showTooltip,
      setFontScale: (scale) => applyFontScale(scale),
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
      jumpToRef: (refId, event) => {
        if (event) {
          event.preventDefault();
          event.stopPropagation();
        }
        const refSec = document.getElementById('sec-references');
        if (refSec && refSec.classList.contains('collapsed')) {
          refSec.classList.remove('collapsed');
        }
        const target = document.getElementById(refId) || document.getElementById(`ref-${refId}`);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
          target.classList.remove('ref-card-highlighted');
          void target.offsetWidth;
          target.classList.add('ref-card-highlighted');
          setTimeout(() => target.classList.remove('ref-card-highlighted'), 2500);
        } else if (refSec) {
          refSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      },
      scrollToReferences: () => {
        const refSec = document.getElementById('sec-references');
        if (refSec) {
          if (refSec.classList.contains('collapsed')) {
            refSec.classList.remove('collapsed');
          }
          refSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      },
      execSearchAction: (idx) => {
        if (window.medbase_current_search_matches && window.medbase_current_search_matches[idx]) {
          window.medbase_current_search_matches[idx].action();
        }
      }
    };

    // --- Toolbar Handlers ---
    // 3-Way Theme Switcher (Dark -> Sepia -> Light)
    els.themeBtn.addEventListener('click', cycleTheme);

    // Font Size Controls
    if (els.fontDecBtn) els.fontDecBtn.addEventListener('click', () => changeFontScale(-1));
    if (els.fontIncBtn) els.fontIncBtn.addEventListener('click', () => changeFontScale(1));
    if (els.fontResetBtn) els.fontResetBtn.addEventListener('click', () => applyFontScale(1.0));

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

    // Highlights Toggle
    els.highlightsBtn.addEventListener('click', () => {
      state.highlightsActive = !state.highlightsActive;
      document.body.classList.toggle('highlights-active', state.highlightsActive);
      els.highlightsBtn.classList.toggle('active', state.highlightsActive);
    });

    // Quiz Mode Toggle
    els.quizBtn.addEventListener('click', () => {
      state.quizModeActive = !state.quizModeActive;
      document.body.classList.toggle('quiz-active', state.quizModeActive);
      els.quizBtn.classList.toggle('active', state.quizModeActive);
      updateQuizBadge();
    });

    // On-Duty / ER Mode
    els.erBtn.addEventListener('click', () => {
      state.onDutyModeActive = !state.onDutyModeActive;
      els.erBtn.classList.toggle('active', state.onDutyModeActive);

      const cards = document.querySelectorAll('.amboss-card');
      cards.forEach(card => {
        const id = card.getAttribute('data-section-id') || '';
        const isAcute = id.includes('mgmt') || id.includes('diag') || id.includes('emergency') || id.includes('references');
        if (state.onDutyModeActive) {
          if (!isAcute) card.classList.add('collapsed');
          else card.classList.remove('collapsed');
        } else {
          card.classList.remove('collapsed');
        }
      });
    });

    // Expand All / Collapse All
    els.expandAllBtn.addEventListener('click', () => {
      const cards = document.querySelectorAll('.amboss-card');
      const anyCollapsed = Array.from(cards).some(c => c.classList.contains('collapsed'));
      cards.forEach(c => c.classList.toggle('collapsed', !anyCollapsed));
      els.expandAllBtn.textContent = anyCollapsed ? 'Collapse All' : 'Expand All';
    });

    // Mobile Navigation Drawer Toggle
    if (els.mobileNavBtn && els.leftSidebar) {
      els.mobileNavBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        els.leftSidebar.classList.toggle('mobile-open');
      });

      document.addEventListener('click', (e) => {
        if (els.leftSidebar.classList.contains('mobile-open') && !els.leftSidebar.contains(e.target) && e.target !== els.mobileNavBtn) {
          els.leftSidebar.classList.remove('mobile-open');
        }
      });
    }

    // Sidebar Tab Switching
    document.querySelectorAll('.sidebar-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.sidebar-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const tab = btn.getAttribute('data-tab');
        document.getElementById('pane-library').style.display = tab === 'library' ? 'block' : 'none';
        document.getElementById('pane-outline').style.display = tab === 'outline' ? 'block' : 'none';
      });
    });

    // Search Modal Listeners
    els.searchBtn.addEventListener('click', openSearch);
    els.searchInput.addEventListener('input', (e) => performSearch(e.target.value));

    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openSearch();
      } else if (e.key === 'Escape') {
        closeSearch();
        els.lightbox.style.display = 'none';
        els.tooltip.style.display = 'none';
      }
    });

    els.searchModal.addEventListener('click', (e) => {
      if (e.target === els.searchModal) closeSearch();
    });

    // Lightbox Modal Listeners
    els.closeLightboxBtn.addEventListener('click', () => els.lightbox.style.display = 'none');
    els.lightbox.addEventListener('click', (e) => {
      if (e.target === els.lightbox) els.lightbox.style.display = 'none';
    });

    // Initialize App: Default to Home Page
    renderLibraryTree();
    goHome();

  })();
  </script>
</body>
</html>
"""

# Write to root project for git and GitHub Pages
with open("/root/medbase/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Single designated offline storage folder (no duplicate loose files)
offline_dir = "/sdcard/HTML_Apps"
os.makedirs(offline_dir, exist_ok=True)
offline_path = os.path.join(offline_dir, "medbase.html")

try:
    with open(offline_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Wrote single offline file successfully to {offline_path}!")
except Exception as e:
    print("Error writing to storage:", e)

print("Generated index.html and /sdcard/HTML_Apps/medbase.html! Size:", len(html_content), "bytes")
