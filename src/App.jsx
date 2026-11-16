"use client";

import React, {
  useState,
  useEffect,
  useMemo,
  useRef,
  useCallback,
  createContext,
  useContext,
} from "react";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  Bookmark,
  BookOpen,
  Calculator,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  ChevronsDownUp,
  ChevronsUpDown,
  Clock,
  Eye,
  EyeOff,
  FileText,
  Folder,
  FolderOpen,
  HelpCircle,
  Highlighter,
  Lightbulb,
  List,
  Moon,
  PanelLeft,
  RotateCcw,
  Search,
  Sparkles,
  Stethoscope,
  Sun,
  Trash2,
  X,
  XCircle,
  Zap,
} from "lucide-react";

// ============================================================================
// 1. MEDICAL GLOSSARY (Smart Tooltips & Cross-Article Navigation)
// ============================================================================

const MEDICAL_GLOSSARY = {
  troponin: {
    id: "troponin",
    title: "Cardiac Troponin (cTnI / cTnT)",
    category: "Biomarker",
    definition:
      "Regulatory proteins of the myocardial contractile apparatus released into circulation upon cardiomyocyte necrosis. High-sensitivity assays (hs-cTn) are the gold-standard biomarker for diagnosing acute myocardial infarction.",
    pearl:
      "Rises within 2–3 hours (hs-cTn), peaks at 24–48 hours, and remains elevated for 7–10 days.",
    articleId: "acs",
    sectionId: "acs-diag-biomarkers",
  },
  stemi: {
    id: "stemi",
    title: "ST-Elevation Myocardial Infarction (STEMI)",
    category: "Condition",
    definition:
      "Acute coronary syndrome caused by complete, transmural coronary artery occlusion resulting in myocardial necrosis and characteristic ST-segment elevations (or new LBBB/STEMI equivalents) on 12-lead ECG.",
    pearl: "Time is myocardium: immediate reperfusion (PCI ≤ 90 min) is mandatory without waiting for troponin results.",
    articleId: "acs",
    sectionId: "acs-mgmt-reperfusion",
  },
  nstemi: {
    id: "nstemi",
    title: "Non-ST-Elevation Myocardial Infarction (NSTEMI)",
    category: "Condition",
    definition:
      "Acute myocardial infarction characterized by elevated cardiac troponin levels without persistent ST-segment elevation, typically resulting from partial or transient coronary occlusion causing subendocardial necrosis.",
    pearl: "Fibrinolytics are contraindicated in NSTEMI—manage with DAPT, anticoagulation, and risk-stratified PCI.",
    articleId: "acs",
    sectionId: "acs-overview",
  },
  ua: {
    id: "ua",
    title: "Unstable Angina (UA)",
    category: "Condition",
    definition:
      "Myocardial ischemia at rest, of new onset (< 2 months), or accelerating in frequency/severity (crescendo) WITHOUT detectable cardiomyocyte necrosis (normal serial troponins).",
    pearl: "Distinguished from NSTEMI solely by negative serial cardiac troponins.",
    articleId: "acs",
    sectionId: "acs-overview",
  },
  pci: {
    id: "pci",
    title: "Percutaneous Coronary Intervention (PCI)",
    category: "Procedure",
    definition:
      "Catheter-based mechanical revascularization (balloon angioplasty and drug-eluting stent placement) used to restore coronary blood flow in ACS.",
    pearl: "Preferred over fibrinolysis for STEMI when First Medical Contact-to-device time is ≤ 90 min (or ≤ 120 min with transfer).",
    articleId: "acs",
    sectionId: "acs-mgmt-reperfusion",
  },
  dapt: {
    id: "dapt",
    title: "Dual Antiplatelet Therapy (DAPT)",
    category: "Pharmacology",
    definition:
      "Combined administration of low-dose aspirin (COX-1 inhibitor) plus a P2Y12 receptor inhibitor (ticagrelor, prasugrel, or clopidogrel) to prevent stent thrombosis and recurrent ischemic events.",
    pearl: "Ticagrelor or prasugrel is generally preferred over clopidogrel in ACS patients undergoing PCI (avoid prasugrel if prior stroke/TIA).",
    articleId: "acs",
    sectionId: "acs-mgmt-secondary",
  },
  wellens: {
    id: "wellens",
    title: "Wellens Syndrome",
    category: "ECG Sign",
    definition:
      "Biphasic (Type A) or deeply symmetric inverted T waves (Type B) in leads V2–V3 observed during a pain-free interval, indicating critical proximal LAD stenosis.",
    pearl: "Stress testing is strictly contraindicated—patients require urgent coronary angiography due to imminent risk of massive anterior STEMI.",
    articleId: "acs",
    sectionId: "acs-diag-localization",
  },
  dewinter: {
    id: "dewinter",
    title: "de Winter T-Wave Pattern",
    category: "ECG Sign",
    definition:
      "Upsloping ST-segment depression (> 1 mm) at the J-point in precordial leads V1–V6 continuing into tall, prominent, symmetric T waves, often with ST elevation in aVR.",
    pearl: "A high-risk STEMI equivalent indicating acute proximal LAD occlusion—treat with emergent PCI.",
    articleId: "acs",
    sectionId: "acs-diag-localization",
  },
  prinzmetal: {
    id: "prinzmetal",
    title: "Vasospastic (Prinzmetal) Angina",
    category: "Condition",
    definition:
      "Transient, focal coronary artery vasospasm causing rest angina (typically midnight to early morning) accompanied by transient ST-segment elevations that resolve with vasodilators.",
    pearl: "Strongly associated with smoking; treat with calcium channel blockers and nitrates, and avoid non-selective beta-blockers.",
    articleId: "acs",
    sectionId: "acs-etiology",
  },
  killip: {
    id: "killip",
    title: "Killip Classification",
    category: "Risk Score",
    definition:
      "Bedside physical exam classification stratifying acute MI severity: Class I (no HF), Class II (rales/S3/JVD), Class III (acute pulmonary edema), Class IV (cardiogenic shock).",
    pearl: "Higher Killip class correlates linearly with 30-day mortality.",
    articleId: "acs",
    sectionId: "acs-clinical",
  },
  ckmb: {
    id: "ckmb",
    title: "Creatine Kinase-MB (CK-MB)",
    category: "Biomarker",
    definition:
      "Cardiac-enriched isoenzyme of creatine kinase that rises 4–6 hours after myocardial injury, peaks at 24 hours, and normalizes within 48–72 hours.",
    pearl: "Because troponin remains elevated for up to 10 days, CK-MB is useful for detecting acute reinfarction occurring days after an index MI.",
    articleId: "acs",
    sectionId: "acs-diag-biomarkers",
  },
  dressler: {
    id: "dressler",
    title: "Dressler Syndrome",
    category: "Complication",
    definition:
      "Delayed immune-mediated (autoimmune) pericarditis occurring 2–10 weeks post-MI due to myocardial neoantigen exposure, presenting with pleuritic pain, fever, and friction rub.",
    pearl: "Treat with high-dose aspirin + colchicine; avoid systemic glucocorticoids initially unless refractory (impairs myocardial scar healing).",
    articleId: "acs",
    sectionId: "acs-complications",
  },
  grace: {
    id: "grace",
    title: "GRACE Risk Score",
    category: "Risk Score",
    definition:
      "Validated scoring model predicting in-hospital and 6-month mortality in ACS using age, HR, SBP, creatinine, Killip class, cardiac arrest, ST deviation, and elevated biomarkers.",
    pearl: "GRACE score > 140 mandates an early invasive strategy (< 24 hours) in NSTEMI/UA.",
    articleId: "acs",
    sectionId: "acs-mgmt-reperfusion",
  },
  fondaparinux: {
    id: "fondaparinux",
    title: "Fondaparinux",
    category: "Pharmacology",
    definition:
      "Indirect synthetic Factor Xa inhibitor (pentasaccharide) used for anticoagulation in NSTEMI/UA, particularly when an ischemia-guided (conservative) approach is chosen.",
    pearl: "Do NOT use as sole anticoagulant during PCI due to risk of catheter thrombosis—supplement with UFH if proceeding to PCI.",
    articleId: "acs",
    sectionId: "acs-mgmt-initial",
  },
  scad: {
    id: "scad",
    title: "Spontaneous Coronary Artery Dissection (SCAD)",
    category: "Etiology",
    definition:
      "Non-atherosclerotic, non-traumatic separation of the coronary arterial wall creating an intramural hematoma that compresses the true lumen.",
    pearl: "Classic board presentation: young/middle-aged woman without traditional cardiovascular risk factors (associated with fibromuscular dysplasia & pregnancy).",
    articleId: "acs",
    sectionId: "acs-etiology",
  },
  curb65: {
    id: "curb65",
    title: "CURB-65 Score",
    category: "Risk Score",
    definition:
      "Clinical prediction rule for community-acquired pneumonia severity: Confusion, Urea (BUN > 19 mg/dL), Respiratory rate ≥ 30/min, BP < 90/60 mmHg, Age ≥ 65 years.",
    pearl: "Score 0–1: outpatient; 2: consider inpatient/short stay; ≥ 3: inpatient + assess for ICU.",
    articleId: "cap",
    sectionId: "cap-mgmt",
  },
  macrolide: {
    id: "macrolide",
    title: "Macrolide Antibiotics",
    category: "Pharmacology",
    definition:
      "Bacteriostatic protein synthesis inhibitors (50S ribosomal subunit) including azithromycin and clarithromycin with potent coverage against atypical respiratory pathogens.",
    pearl: "Monitor for QTc prolongation and torsades de pointes; rising S. pneumoniae macrolide resistance limits monotherapy in areas with > 25% resistance.",
    articleId: "cap",
    sectionId: "cap-mgmt",
  },
  procalcitonin: {
    id: "procalcitonin",
    title: "Procalcitonin",
    category: "Biomarker",
    definition:
      "Peptide precursor of calcitonin upregulated in response to bacterial endotoxins and pro-inflammatory cytokines (IL-1β, TNF-α), suppressed by interferon-γ in viral infections.",
    pearl: "Used to guide antibiotic de-escalation/discontinuation rather than withholding initial empiric therapy in suspected CAP.",
    articleId: "cap",
    sectionId: "cap-diag",
  },
  gdmt: {
    id: "gdmt",
    title: "Guideline-Directed Medical Therapy (GDMT)",
    category: "Pharmacology",
    definition:
      "Four foundational mortality-reducing drug classes in HFrEF: ARNI (or ACEi/ARB), evidence-based beta-blocker, mineralocorticoid receptor antagonist (MRA), and SGLT2 inhibitor.",
    pearl: "Initiate all four pillars early at low doses and titrate upward as tolerated.",
    articleId: "hf",
    sectionId: "hf-mgmt",
  },
  aniongap: {
    id: "aniongap",
    title: "Serum Anion Gap",
    category: "Lab Calculation",
    definition:
      "Calculated as Na⁺ − (Cl⁻ + HCO₃⁻), normally 8–12 mEq/L, representing unmeasured serum anions (primarily albumin, plus ketoacids or lactate in metabolic acidosis).",
    pearl: "In DKA, insulin therapy continues until the anion gap closes (< 12 mEq/L)—not merely until blood glucose normalizes.",
    articleId: "dka",
    sectionId: "dka-mgmt",
  },
};

// ============================================================================
// 2. NAVIGATION LIBRARY TREE
// ============================================================================

const LIBRARY_TREE = [
  {
    id: "im",
    label: "Internal Medicine",
    children: [
      {
        id: "cardio",
        label: "Cardiology",
        children: [
          {
            id: "acs",
            label: "Acute Coronary Syndrome (ACS)",
            articleId: "acs",
            badge: "High-Yield",
          },
          {
            id: "hf",
            label: "Heart Failure (HFrEF & HFpEF)",
            articleId: "hf",
          },
        ],
      },
      {
        id: "pulm",
        label: "Pulmonology",
        children: [
          {
            id: "cap",
            label: "Community-Acquired Pneumonia",
            articleId: "cap",
            badge: "High-Yield",
          },
        ],
      },
      {
        id: "endo",
        label: "Endocrinology",
        children: [
          {
            id: "dka",
            label: "Diabetic Ketoacidosis (DKA)",
            articleId: "dka",
          },
        ],
      },
    ],
  },
];

// ============================================================================
// 3. ARTICLE CONTENT DATA (3-Level Nested Bullets, Callouts, Tables)
// ============================================================================

const ARTICLES = {
  acs: {
    id: "acs",
    title: "Acute Coronary Syndrome (ACS)",
    breadcrumbs: ["Internal Medicine", "Cardiology", "Coronary Artery Disease"],
    lastUpdated: "Nov 2026",
    readTime: "12 min read",
    highYieldTag: "Core Shelf & Step 2 CK",
    calculatorDefault: "heart",
    qbankCount: 14,
    summary:
      "**Acute Coronary Syndrome (ACS)** encompasses a clinical spectrum of acute myocardial ischemia resulting from sudden reduction in coronary blood flow—most commonly due to atherosclerotic plaque disruption and superimposed thrombosis. It comprises [[hl:{{term:ua|Unstable Angina (UA)}}]], [[hl:{{term:nstemi|NSTEMI}}]], and [[hl:{{term:stemi|STEMI}}]].",
    sections: [
      {
        id: "acs-overview",
        title: "1. Overview & Classification",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**ACS Spectrum**: Driven by acute coronary plaque rupture/erosion leading to thrombus formation and myocardial ischemia.",
                children: [
                  {
                    yield: "high",
                    text: "**NSTE-ACS** (Non-ST-Elevation ACS): Includes {{term:ua|Unstable Angina}} and {{term:nstemi|NSTEMI}}; typically caused by [[hl:partial or intermittent coronary occlusion]] producing subendocardial ischemia.",
                    children: [
                      {
                        yield: "high",
                        text: "**Unstable Angina (UA)**: Clinical ischemia with [[hl:normal serial cardiac troponins]] (no cardiomyocyte necrosis).",
                      },
                      {
                        yield: "high",
                        text: "**NSTEMI**: Clinical ischemia with [[hl:elevated cardiac troponins]] (> 99th percentile URL) indicating myocardial necrosis.",
                      },
                    ],
                  },
                  {
                    yield: "high",
                    text: "**STEMI**: Caused by [[hl:complete, persistent coronary occlusion]] resulting in transmural myocardial injury/necrosis with persistent ST-segment elevation.",
                  },
                ],
              },
              {
                yield: "low",
                text: "**Universal Classification of MI (4th Universal Definition)**: Categorizes myocardial infarction into 5 mechanistic subtypes.",
                children: [
                  {
                    yield: "high",
                    text: "**Type 1 MI**: Spontaneous MI due to atherosclerotic plaque rupture, ulceration, or dissection with intraluminal thrombus.",
                  },
                  {
                    yield: "high",
                    text: "**Type 2 MI**: Secondary to [[hl:ischemic oxygen supply–demand mismatch]] without acute atherothrombosis (e.g., severe anemia, sepsis, tachyarrhythmia, hypertensive crisis).",
                  },
                  {
                    yield: "low",
                    text: "**Type 3 MI**: Cardiac death with symptoms suggestive of ischemia before biomarkers could be obtained.",
                  },
                  {
                    yield: "low",
                    text: "**Type 4 / Type 5 MI**: Procedure-related MI associated with {{term:pci|PCI}} (Type 4a/b/c) or CABG (Type 5).",
                  },
                ],
              },
            ],
          },
          {
            type: "callout",
            variant: "pearl",
            yield: "high",
            title: "Clinical Pearl: Distinguishing UA vs. NSTEMI",
            text: "At initial presentation, UA and NSTEMI are clinically indistinguishable because both present with ischemic chest pain and non-diagnostic or ST-depression/T-wave inversion ECG changes. Only [[hl:serial {{term:troponin|troponin}} measurements]] (at 0h and 1–3h) differentiate NSTEMI (elevated) from UA (normal).",
          },
          {
            type: "table",
            yield: "high",
            caption: "Comparison of Acute Coronary Syndrome Subtypes",
            headers: ["Feature", "Unstable Angina (UA)", "NSTEMI", "STEMI"],
            rows: [
              [
                "**Pathophysiology**",
                "Partial/transient thrombus; ischemia without necrosis",
                "Partial/intermittent occlusion; [[hl:subendocardial necrosis]]",
                "Complete occlusion; [[hl:transmural necrosis]]",
              ],
              [
                "**{{term:troponin|Cardiac Troponin}}**",
                "[[hl:Normal / Negative]]",
                "[[hl:Elevated]] (rise and/or fall > 99th %ile)",
                "[[hl:Elevated]] (do NOT delay PCI waiting for result)",
              ],
              [
                "**12-Lead ECG**",
                "Normal, ST depression, or T-wave inversion",
                "ST depression, T-wave inversion, or normal",
                "[[hl:Persistent ST elevation]] in ≥ 2 contiguous leads or new LBBB",
              ],
              [
                "**Fibrinolytics**",
                "Contraindicated",
                "[[hl:Contraindicated]] (increases mortality/bleeding)",
                "Indicated if PCI delay > 120 min (door-to-needle ≤ 30 min)",
              ],
              [
                "**Invasive Timing**",
                "Risk-stratified (GRACE/TIMI): early (< 24h) vs. ischemia-guided",
                "Urgent/early invasive (< 24h) if high risk (GRACE > 140)",
                "[[hl:Emergent primary PCI]] (FMC-to-device ≤ 90 min)",
              ],
            ],
          },
        ],
      },
      {
        id: "acs-etiology",
        title: "2. Etiology & Risk Factors",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Atherosclerotic Plaque Disruption (~90% of Type 1 ACS)**:",
                children: [
                  {
                    yield: "high",
                    text: "**Plaque rupture**: Thin fibrous cap ruptures, exposing thrombogenic lipid core and tissue factor.",
                    children: [
                      {
                        yield: "low",
                        text: "Vulnerable plaques typically feature a large necrotic lipid core, macrophage infiltration, matrix metalloproteinase (MMP) degradation, and a fibrous cap < 65 µm.",
                      },
                    ],
                  },
                  {
                    yield: "low",
                    text: "**Plaque erosion**: Endothelial denudation over a proteoglycan-rich plaque (increasingly recognized in women and younger smokers).",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Non-Atherosclerotic Causes of ACS**:",
                children: [
                  {
                    yield: "high",
                    text: "**{{term:prinzmetal|Vasospastic (Prinzmetal) Angina}}**: Focal epicardial coronary vasospasm causing transient ST elevations, often in smokers or triggered by cocaine/triptans.",
                  },
                  {
                    yield: "high",
                    text: "**{{term:scad|Spontaneous Coronary Artery Dissection (SCAD)}}**: Intramural hematoma compressing the true lumen; classic in [[hl:young/peripartum women without traditional CAD risk factors]] (associated with fibromuscular dysplasia).",
                  },
                  {
                    yield: "low",
                    text: "**Coronary Embolism & Arteritis**: Infective endocarditis vegetations, paradoxical emboli, atrial myxoma, Kawasaki disease, or Takayasu arteritis.",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Major Cardiovascular Risk Factors**:",
                children: [
                  {
                    yield: "high",
                    text: "**Modifiable**: Hypertension, hyperlipidemia (elevated LDL-C), [[hl:diabetes mellitus]] (considered a CAD risk equivalent), smoking, obesity, sedentary lifestyle.",
                  },
                  {
                    yield: "low",
                    text: "**Non-Modifiable**: Advanced age (men ≥ 45 yrs, women ≥ 55 yrs), male sex, premature family history (1st-degree male relative < 55 yrs or female < 65 yrs).",
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        id: "acs-pathophys",
        title: "3. Pathophysiology",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Thrombotic Cascade**: Plaque rupture exposes subendothelial collagen and von Willebrand factor → platelet adhesion (GpIb) and activation → conformational change in [[hl:GpIIb/IIIa receptors]] → fibrinogen cross-linking and fibrin clot stabilization.",
              },
              {
                yield: "high",
                text: "**Ischemic Progression (Wavefront Phenomenon)**:",
                children: [
                  {
                    yield: "high",
                    text: "Necrosis begins in the [[hl:subendocardium]] (highest wall tension and oxygen demand, furthest from epicardial vessels) within 20–30 minutes of complete occlusion.",
                  },
                  {
                    yield: "high",
                    text: "Progresses outward toward the epicardium over 3–6 hours until becoming transmural unless collateral flow or reperfusion intervenes.",
                  },
                ],
              },
              {
                yield: "low",
                text: "**Adaptive & Post-Ischemic Myocardial States**:",
                children: [
                  {
                    yield: "low",
                    text: "**Myocardial stunning**: Reversible contractile dysfunction persisting for hours to days after brief ischemia despite restoration of normal blood flow.",
                  },
                  {
                    yield: "low",
                    text: "**Hibernating myocardium**: Chronic downregulation of contractile function in response to chronic hypoperfusion that recovers after revascularization.",
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        id: "acs-clinical",
        title: "4. Clinical Features",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Typical Anginal Chest Pain**:",
                children: [
                  {
                    yield: "high",
                    text: "**Quality & Location**: Substernal squeezing, heaviness, or pressure (**Levine sign**: clenched fist over sternum) lasting [[hl:> 20 minutes]] and unrelieved by rest or sublingual nitroglycerin.",
                  },
                  {
                    yield: "high",
                    text: "**Radiation**: Left arm/shoulder, neck, jaw, epigastrium, or interscapular region.",
                  },
                  {
                    yield: "high",
                    text: "**Autonomic Symptoms**: Diaphoresis (strongest positive predictor), nausea/vomiting, dyspnea, presyncope.",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Atypical Presentations (\"Anginal Equivalents\")**:",
                children: [
                  {
                    yield: "high",
                    text: "Isolated unexplained dyspnea, epigastric discomfort, fatigue, syncope, or acute confusion without chest pain.",
                  },
                  {
                    yield: "high",
                    text: "Most common in [[hl:older adults, women, and patients with diabetes mellitus]] (autonomic neuropathy blunts visceral pain sensation).",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Physical Examination Findings**:",
                children: [
                  {
                    yield: "high",
                    text: "**Auscultation**: [[hl:S4 gallop]] (stiff, non-compliant ischemic ventricle), S3 gallop (systolic dysfunction/HF), or new holosystolic murmur at apex (papillary muscle dysfunction → mitral regurgitation).",
                  },
                  {
                    yield: "high",
                    text: "**{{term:killip|Killip Classification}}**: Assesses acute heart failure severity (Class I: clear lungs → Class IV: cardiogenic shock with SBP < 90 mmHg and pulmonary edema).",
                  },
                  {
                    yield: "low",
                    text: "**Vascular Signs**: Bilateral radial pulse/BP discrepancies (> 20 mmHg) should immediately prompt evaluation for acute aortic dissection.",
                  },
                ],
              },
            ],
          },
          {
            type: "callout",
            variant: "redflag",
            yield: "high",
            title: "Red Flag: Silent / Atypical MI in Diabetics",
            text: "Never rule out ACS based solely on absence of chest pain in elderly or diabetic patients. Acute unexplained dyspnea, diaphoresis, or new-onset pulmonary edema warrants an immediate 12-lead ECG.",
          },
        ],
      },
      {
        id: "acs-diag",
        title: "5. Diagnostics",
        blocks: [
          {
            type: "paragraph",
            yield: "high",
            text: "Rapid diagnostic triage centers on immediate 12-lead ECG interpretation combined with serial high-sensitivity cardiac troponin assays and targeted bedside evaluation.",
          },
        ],
        subsections: [
          {
            id: "acs-diag-ecg",
            title: "5.1 Initial Assessment & 12-Lead ECG Criteria",
            blocks: [
              {
                type: "bullets",
                items: [
                  {
                    yield: "high",
                    text: "**Door-to-ECG Time**: Obtain and interpret a 12-lead ECG within [[hl:10 minutes]] of emergency department arrival.",
                  },
                  {
                    yield: "high",
                    text: "**STEMI ECG Diagnostic Criteria** (new ST elevation at the J-point in ≥ 2 anatomically contiguous leads):",
                    children: [
                      {
                        yield: "high",
                        text: "**Limb & lateral/other chest leads**: ≥ 1 mm (0.1 mV) in all leads except V2–V3.",
                      },
                      {
                        yield: "high",
                        text: "**Leads V2–V3 (sex/age-specific thresholds)**: [[hl:≥ 2.0 mm in men ≥ 40 yrs]], ≥ 2.5 mm in men < 40 yrs, and [[hl:≥ 1.5 mm in women]].",
                      },
                      {
                        yield: "low",
                        text: "Repeat ECGs every 15–30 minutes if initial tracing is non-diagnostic but clinical suspicion remains high.",
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            id: "acs-diag-localization",
            title: "5.2 Coronary Territory Localization & High-Risk Equivalents",
            blocks: [
              {
                type: "bullets",
                items: [
                  {
                    yield: "high",
                    text: "**Anatomical ECG Territories**:",
                    children: [
                      {
                        yield: "high",
                        text: "**Anterior / Anteroseptal (LAD)**: V1–V4 (highest risk for LV systolic failure & cardiogenic shock).",
                      },
                      {
                        yield: "high",
                        text: "**Inferior (RCA ~80%, LCx ~20%)**: [[hl:II, III, aVF]] → always obtain [[hl:right-sided lead V4R]] to evaluate for right ventricular MI.",
                      },
                      {
                        yield: "high",
                        text: "**Lateral (LCx / Diagonal LAD)**: I, aVL, V5–V6.",
                      },
                      {
                        yield: "high",
                        text: "**Posterior (LCx / RCA)**: [[hl:ST depression + tall R waves in V1–V3]] → confirm with posterior leads **V7–V9** showing ST elevation ≥ 0.5 mm.",
                      },
                    ],
                  },
                  {
                    yield: "high",
                    text: "**Critical STEMI Equivalents (Treat as Emergent Occlusion)**:",
                    children: [
                      {
                        yield: "high",
                        text: "**{{term:wellens|Wellens Syndrome}}**: Deeply inverted or biphasic T waves in V2–V3 when pain-free (proximal LAD stenosis) → [[hl:avoid stress testing]].",
                      },
                      {
                        yield: "high",
                        text: "**{{term:dewinter|de Winter T Waves}}**: Upsloping ST depression at J-point in V1–V6 with tall symmetric T waves.",
                      },
                      {
                        yield: "low",
                        text: "**Modified Sgarbossa Criteria** (in pre-existing LBBB or ventricular paced rhythm): Concordant ST elevation ≥ 1 mm, concordant ST depression ≥ 1 mm in V1–V3, or discordant ST elevation ≥ 25% of preceding S wave depth.",
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            id: "acs-diag-biomarkers",
            title: "5.3 Cardiac Biomarkers",
            blocks: [
              {
                type: "bullets",
                items: [
                  {
                    yield: "high",
                    text: "**{{term:troponin|High-Sensitivity Cardiac Troponin (hs-cTn)}}**: Preferred biomarker of myocardial injury.",
                    children: [
                      {
                        yield: "high",
                        text: "Rises within [[hl:2–3 hours]], peaks at 24–48 hours, and remains elevated for [[hl:7–10 days]].",
                      },
                      {
                        yield: "low",
                        text: "Non-ACS causes of troponin elevation include myocarditis, PE, Takotsubo cardiomyopathy, sepsis, renal failure (reduced clearance), and hypertensive emergency.",
                      },
                    ],
                  },
                  {
                    yield: "high",
                    text: "**{{term:ckmb|CK-MB}}**: Normalizes within 48–72 hours; useful primarily for detecting [[hl:acute reinfarction]] occurring several days after an index MI.",
                  },
                ],
              },
            ],
          },
          {
            id: "acs-diag-imaging",
            title: "5.4 Additional Workup & Imaging",
            blocks: [
              {
                type: "bullets",
                items: [
                  {
                    yield: "high",
                    text: "**Portable Chest X-Ray**: Rule out pneumothorax, pneumonia, pulmonary edema, and [[hl:widened mediastinum (aortic dissection)]] before giving antithrombotics.",
                  },
                  {
                    yield: "low",
                    text: "**Bedside Transthoracic Echocardiography (TTE)**: Identifies regional wall motion abnormalities, LVEF, pericardial effusion, and mechanical complications.",
                  },
                  {
                    yield: "high",
                    text: "**Baseline Labs**: CBC (check hemoglobin/platelets before anticoagulation), BMP (renal function & K⁺/Mg²⁺ to prevent arrhythmias), lipid panel, and coagulation profile.",
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        id: "acs-mgmt",
        title: "6. Management",
        blocks: [
          {
            type: "callout",
            variant: "pearl",
            yield: "high",
            title: "High-Yield Exam Tip: Revisit the Classic 'MONA' Mnemonic",
            text: "Modern guidelines no longer support routine **O**xygen or **M**orphine for all ACS patients. Only administer oxygen if [[hl:SpO₂ < 90%]] (hyperoxia causes coronary vasoconstriction), and reserve morphine for refractory pain because it delays oral P2Y12 absorption.",
          },
        ],
        subsections: [
          {
            id: "acs-mgmt-initial",
            title: "6.1 Immediate Stabilization & Medical Therapy",
            blocks: [
              {
                type: "bullets",
                items: [
                  {
                    yield: "high",
                    text: "**Antiplatelet Therapy (Immediate)**:",
                    children: [
                      {
                        yield: "high",
                        text: "**Aspirin**: [[hl:162–325 mg non-enteric coated, chewed]] immediately in all patients without true anaphylaxis.",
                      },
                      {
                        yield: "high",
                        text: "**P2Y12 Inhibitor ({{term:dapt|DAPT}})**: Add loading dose of [[hl:ticagrelor]] (180 mg), prasugrel (60 mg, only after coronary anatomy known & no prior stroke/TIA), or clopidogrel (300–600 mg).",
                      },
                    ],
                  },
                  {
                    yield: "high",
                    text: "**Anticoagulation**: Initiate [[hl:unfractionated heparin (UFH)]] or low-molecular-weight heparin (enoxaparin); {{term:fondaparinux|fondaparinux}} is preferred in ischemia-guided NSTEMI with high bleeding risk (never sole agent during PCI).",
                  },
                  {
                    yield: "high",
                    text: "**Anti-Ischemic & Hemodynamic Therapy**:",
                    children: [
                      {
                        yield: "high",
                        text: "**Nitrates (Sublingual/IV Nitroglycerin)**: Relieves ischemic pain via preload reduction and coronary vasodilation; [[hl:contraindicated if SBP < 90 mmHg, PDE-5 inhibitor use within 24–48h, or RV infarction]].",
                      },
                      {
                        yield: "high",
                        text: "**Oral Beta-Blocker** (e.g., metoprolol): Initiate within 24 hours if hemodynamically stable to reduce myocardial oxygen demand; avoid in acute decompensated HF, bradycardia, heart block, or cocaine-induced ACS.",
                      },
                      {
                        yield: "high",
                        text: "**High-Intensity Statin**: Atorvastatin 40–80 mg or rosuvastatin 20–40 mg initiated immediately for plaque stabilization regardless of baseline LDL.",
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            id: "acs-mgmt-reperfusion",
            title: "6.2 Reperfusion & Invasive Strategy",
            blocks: [
              {
                type: "bullets",
                items: [
                  {
                    yield: "high",
                    text: "**STEMI (Emergent Reperfusion — Target Ischemic Time < 12 Hours)**:",
                    children: [
                      {
                        yield: "high",
                        text: "**Primary {{term:pci|PCI}} (Preferred)**: First medical contact (FMC)-to-device time [[hl:≤ 90 minutes]] at PCI-capable center (or ≤ 120 min if transfer required).",
                      },
                      {
                        yield: "high",
                        text: "**Fibrinolysis (Alteplase / Tenecteplase)**: Indicated ONLY if PCI cannot be achieved within 120 minutes; target door-to-needle time [[hl:≤ 30 minutes]].",
                        children: [
                          {
                            yield: "high",
                            text: "**Absolute Contraindications**: [[hl:Prior intracranial hemorrhage (anytime)]], ischemic stroke within 3 months, active internal bleeding, suspected aortic dissection, CNS neoplasm/AVM, or severe head trauma within 3 months.",
                          },
                        ],
                      },
                    ],
                  },
                  {
                    yield: "high",
                    text: "**NSTE-ACS (NSTEMI / UA) — Risk-Stratified Invasive Approach**:",
                    children: [
                      {
                        yield: "high",
                        text: "**Immediate Invasive (< 2 hours)**: Refractory angina, hemodynamic instability/cardiogenic shock, life-threatening ventricular arrhythmias, or acute mechanical complications.",
                      },
                      {
                        yield: "high",
                        text: "**Early Invasive (< 24 hours)**: Elevated troponin, dynamic ST/T changes, or [[hl:{{term:grace|GRACE score}} > 140]].",
                      },
                      {
                        yield: "high",
                        text: "**Fibrinolytics**: Strictly [[hl:contraindicated in NSTEMI/UA]] (no benefit and increased hemorrhagic risk).",
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            id: "acs-mgmt-special",
            title: "6.3 Special Clinical Scenarios",
            blocks: [
              {
                type: "callout",
                variant: "redflag",
                yield: "high",
                title: "Red Flag: Right Ventricular (RV) Infarction",
                text: "Suspect RV infarction in any patient with an inferior STEMI presenting with the triad of [[hl:hypotension, elevated JVP (Kussmaul sign), and clear lung fields]] (+ ST elevation in V4R). Management requires [[hl:IV normal saline boluses]] to maintain RV preload; **strictly avoid nitrates and diuretics**, which precipitate severe shock.",
              },
              {
                type: "bullets",
                items: [
                  {
                    yield: "high",
                    text: "**Cocaine-Induced ACS**: Treat acutely with [[hl:IV benzodiazepines]] (reduces sympathetic outflow) + aspirin + nitrates; use phentolamine or calcium channel blockers for refractory hypertension/vasospasm; [[hl:avoid non-selective beta-blockers]] acutely (risk of unopposed α-adrenergic coronary vasoconstriction).",
                  },
                  {
                    yield: "high",
                    text: "**{{term:prinzmetal|Vasospastic Angina}}**: First-line therapy is [[hl:calcium channel blockers]] (amlodipine/diltiazem) + long-acting nitrates + smoking cessation.",
                  },
                ],
              },
            ],
          },
          {
            id: "acs-mgmt-secondary",
            title: "6.4 Long-Term Secondary Prevention",
            blocks: [
              {
                type: "bullets",
                items: [
                  {
                    yield: "high",
                    text: "**{{term:dapt|DAPT}}**: Aspirin 81 mg daily indefinitely + P2Y12 inhibitor for at least [[hl:12 months]] post-ACS (shorter duration only if high bleeding risk).",
                  },
                  {
                    yield: "high",
                    text: "**Neurohormonal Blockade**:",
                    children: [
                      {
                        yield: "high",
                        text: "**ACE Inhibitor (or ARB)**: Initiate within 24 hours for anterior MI, LVEF ≤ 40%, hypertension, or diabetes to prevent adverse LV remodeling.",
                      },
                      {
                        yield: "high",
                        text: "**MRA (Eplerenone / Spironolactone)**: Add for patients already on ACEi + beta-blocker with [[hl:LVEF ≤ 40%]] and symptomatic HF or diabetes (monitor K⁺ and Cr).",
                      },
                    ],
                  },
                  {
                    yield: "low",
                    text: "**Lifestyle & Vaccination**: Structured cardiac rehabilitation, complete smoking cessation, and annual influenza vaccination (reduces recurrent CV events).",
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        id: "acs-complications",
        title: "7. Complications & Prognosis",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Arrhythmias (Most Common Cause of Early Death)**:",
                children: [
                  {
                    yield: "high",
                    text: "[[hl:Ventricular fibrillation (VF)]]: Leading cause of pre-hospital and first-24h mortality post-MI; manage with immediate unsynchronized defibrillation.",
                  },
                  {
                    yield: "high",
                    text: "**Conduction Blocks**: Inferior MI (RCA → AV nodal artery) causes transient sinus bradycardia/Mobitz I (responds to atropine); anterior MI causes infranodal Mobitz II/complete heart block (requires temporary pacing).",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Mechanical Complications (Typically 3–7 Days Post-MI due to Macrophage Weakening)**:",
                children: [
                  {
                    yield: "high",
                    text: "**[[hl:Papillary Muscle Rupture]]**: Often posteromedial papillary muscle (single blood supply from PDA in inferior MI) → acute severe mitral regurgitation, flash pulmonary edema, new holosystolic murmur.",
                  },
                  {
                    yield: "high",
                    text: "**Interventricular Septal Rupture**: Holosystolic murmur at left lower sternal border + [[hl:O₂ step-up from right atrium to right ventricle]] on Swan-Ganz catheterization.",
                  },
                  {
                    yield: "high",
                    text: "**Left Ventricular Free Wall Rupture**: Sudden hemodynamic collapse, [[hl:cardiac tamponade, and pulseless electrical activity (PEA)]] (highest mortality).",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Pericardial & Mural Complications**:",
                children: [
                  {
                    yield: "low",
                    text: "**Early Fibrinous Pericarditis (1–3 days)**: Pleuritic chest pain relieved by leaning forward + friction rub; treat with aspirin (avoid NSAIDs like ibuprofen/indomethacin due to impaired scar healing).",
                  },
                  {
                    yield: "high",
                    text: "**{{term:dressler|Dressler Syndrome}} (2–10 weeks)**: Autoimmune pericarditis + fever + elevated ESR; treat with [[hl:high-dose aspirin + colchicine]].",
                  },
                  {
                    yield: "high",
                    text: "**True LV Aneurysm (> 2 weeks)**: Outpouching of thinned scarred wall (often anterior) showing [[hl:persistent ST elevation weeks after MI]] + risk of mural thrombus (treat with anticoagulation if thrombus present).",
                  },
                ],
              },
            ],
          },
        ],
      },
    ],
  },

  cap: {
    id: "cap",
    title: "Community-Acquired Pneumonia (CAP)",
    breadcrumbs: ["Internal Medicine", "Pulmonology", "Lower Respiratory Infections"],
    lastUpdated: "Nov 2026",
    readTime: "8 min read",
    highYieldTag: "Core Shelf & Step 2 CK",
    calculatorDefault: "curb65",
    qbankCount: 11,
    summary:
      "**Community-Acquired Pneumonia (CAP)** is an acute infection of the pulmonary parenchyma acquired outside the hospital (or < 48 hours after admission). Management relies on severity stratification ({{term:curb65|CURB-65}} / PSI) and targeted empiric antibiotic therapy.",
    sections: [
      {
        id: "cap-etiology",
        title: "1. Etiology & Microbiologic Spectrum",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Typical Bacterial Pathogens**:",
                children: [
                  {
                    yield: "high",
                    text: "**Streptococcus pneumoniae**: [[hl:Overall most common bacterial cause of CAP]]; rusty sputum, lobar consolidation, lancet-shaped gram-positive diplococci.",
                  },
                  {
                    yield: "high",
                    text: "**Haemophilus influenzae**: Common in [[hl:COPD and active smokers]]; pleomorphic gram-negative coccobacilli.",
                  },
                  {
                    yield: "high",
                    text: "**Staphylococcus aureus (MRSA/MSSA)**: Classic [[hl:post-influenza pneumonia]] causing severe necrotizing cavitary infiltrates.",
                  },
                  {
                    yield: "low",
                    text: "**Klebsiella pneumoniae**: Alcohol use disorder / aspiration; currant-jelly sputum and bulging interlobar fissure.",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Atypical Pathogens (\"Walking Pneumonia\" — No Cell Wall / Intracellular)**:",
                children: [
                  {
                    yield: "high",
                    text: "**Mycoplasma pneumoniae**: Young adults in crowded settings (dorms/military); dry cough, bilateral interstitial infiltrates, [[hl:cold agglutinins (IgM) & bullous myringitis]].",
                  },
                  {
                    yield: "high",
                    text: "**Legionella pneumophila**: Contaminated water systems (AC cooling towers); pneumonia + [[hl:GI symptoms (watery diarrhea), hyponatremia, and relative bradycardia]].",
                  },
                ],
              },
            ],
          },
          {
            type: "table",
            yield: "high",
            caption: "Typical vs. Atypical vs. Aspiration Pneumonia",
            headers: ["Feature", "Typical CAP", "Atypical CAP", "Aspiration Pneumonia"],
            rows: [
              [
                "**Key Pathogens**",
                "*S. pneumoniae*, *H. influenzae*, *S. aureus*",
                "*M. pneumoniae*, *C. pneumoniae*, *Legionella*",
                "Oral anaerobes (*Prevotella*, *Fusobacterium*) + mixed flora",
              ],
              [
                "**Presentation**",
                "Sudden onset, high fever, rigors, productive purulent sputum",
                "Insidious onset, low-grade fever, dry cough, extrapulmonary signs",
                "Foul-smelling sputum in patients with dysphagia / alcohol / seizure",
              ],
              [
                "**Chest X-Ray**",
                "[[hl:Lobar or segmental consolidation]]",
                "[[hl:Bilateral patchy/interstitial]] (\"worse than patient looks\")",
                "[[hl:Dependent lung zones]] (RLL upright; posterior RUL/RLL supine)",
              ],
            ],
          },
        ],
      },
      {
        id: "cap-diag",
        title: "2. Diagnostics",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Chest Radiography (Gold Standard for Confirmation)**: Required to demonstrate a new parenchymal infiltrate alongside clinical symptoms.",
              },
              {
                yield: "high",
                text: "**Microbiologic Testing**:",
                children: [
                  {
                    yield: "high",
                    text: "**Outpatient CAP**: Routine sputum/blood cultures are [[hl:NOT recommended]] (treat empirically).",
                  },
                  {
                    yield: "high",
                    text: "**Severe Inpatient / ICU CAP**: Obtain blood cultures, sputum Gram stain/culture, and [[hl:Legionella & pneumococcal urinary antigen tests]].",
                  },
                  {
                    yield: "low",
                    text: "**{{term:procalcitonin|Procalcitonin}}**: Helps guide antibiotic discontinuation once clinically stable, not initial withholding.",
                  },
                ],
              },
            ],
          },
          {
            type: "callout",
            variant: "pearl",
            yield: "high",
            title: "Clinical Pearl: Elderly / Volume-Depleted CXR",
            text: "Severely dehydrated or neutropenic patients may initially have a falsely normal chest radiograph that develops a visible infiltrate only after IV fluid resuscitation.",
          },
        ],
      },
      {
        id: "cap-mgmt",
        title: "3. Risk Stratification & Empiric Management",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Disposition via {{term:curb65|CURB-65 Score}}**: Score 0–1 → outpatient; Score 2 → inpatient admission; Score ≥ 3 → inpatient/evaluate for ICU.",
              },
              {
                yield: "high",
                text: "**Outpatient Empiric Regimens**:",
                children: [
                  {
                    yield: "high",
                    text: "**Healthy (no comorbidities, no recent abx)**: [[hl:Amoxicillin 1 g TID]] (preferred) or doxycycline (or {{term:macrolide|macrolide}} ONLY if local pneumococcal resistance < 25%).",
                  },
                  {
                    yield: "high",
                    text: "**With Comorbidities** (chronic heart/lung/liver/renal disease, DM, alcoholism): [[hl:Amoxicillin-clavulanate (or cephalosporin) + macrolide/doxycycline]], OR respiratory fluoroquinolone (levofloxacin/moxifloxacin) monotherapy.",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Inpatient Non-ICU Regimens**: [[hl:IV β-lactam (ceftriaxone) + macrolide (azithromycin)]] OR respiratory fluoroquinolone monotherapy.",
              },
              {
                yield: "high",
                text: "**ICU / Severe CAP**: IV β-lactam + either macrolide or respiratory fluoroquinolone; add [[hl:vancomycin or linezolid]] if prior MRSA, or antipseudomonal β-lactam (piperacillin-tazobactam / cefepime) if *Pseudomonas* risk factors.",
              },
            ],
          },
          {
            type: "callout",
            variant: "redflag",
            yield: "high",
            title: "Red Flag: Empyema & Parapneumonic Effusion",
            text: "Persistent fever or leukocytosis after 48–72 hours of appropriate antibiotics warrants repeat imaging to evaluate for parapneumonic effusion/empyema. Perform diagnostic thoracentesis; [[hl:pH < 7.20, glucose < 60 mg/dL, or frank pus]] mandates urgent tube thoracostomy drainage.",
          },
        ],
      },
    ],
  },

  hf: {
    id: "hf",
    title: "Heart Failure (HFrEF & HFpEF)",
    breadcrumbs: ["Internal Medicine", "Cardiology", "Myocardial Disease"],
    lastUpdated: "Nov 2026",
    readTime: "7 min read",
    highYieldTag: "Core Shelf",
    calculatorDefault: "heart",
    qbankCount: 9,
    summary:
      "**Heart Failure (HF)** is a complex clinical syndrome resulting from structural or functional impairment of ventricular filling or ejection of blood, categorized primarily into **HFrEF** (LVEF ≤ 40%) and **HFpEF** (LVEF ≥ 50%).",
    sections: [
      {
        id: "hf-class",
        title: "1. Classification & Clinical Presentation",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**LVEF Categories**: [[hl:HFrEF (LVEF ≤ 40%)]], HFmrEF (41–49%), and [[hl:HFpEF (LVEF ≥ 50%)]].",
              },
              {
                yield: "high",
                text: "**Left- vs. Right-Sided Congestion**:",
                children: [
                  {
                    yield: "high",
                    text: "**Left HF**: Dyspnea, orthopnea, paroxysmal nocturnal dyspnea (PND), bibasilar crackles, [[hl:S3 gallop]] (volume overload).",
                  },
                  {
                    yield: "high",
                    text: "**Right HF**: Elevated JVP, hepatojugular reflux, hepatomegaly, ascites, bilateral pitting edema (most commonly caused by left-sided HF).",
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        id: "hf-mgmt",
        title: "2. Guideline-Directed Medical Therapy (GDMT)",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Four Pillars of Mortality-Reducing {{term:gdmt|GDMT}} in HFrEF**:",
                children: [
                  {
                    yield: "high",
                    text: "**ARNI (Sacubitril/Valsartan)** (preferred over ACEi/ARB; wait [[hl:36-hour washout]] when switching from ACEi to avoid angioedema).",
                  },
                  {
                    yield: "high",
                    text: "**Evidence-Based Beta-Blocker**: [[hl:Carvedilol, metoprolol succinate, or bisoprolol]] (initiate only when euvolemic/compensated).",
                  },
                  {
                    yield: "high",
                    text: "**MRA**: Spironolactone or eplerenone (if NYHA II–IV, eGFR > 30, K⁺ < 5.0).",
                  },
                  {
                    yield: "high",
                    text: "**SGLT2 Inhibitor**: [[hl:Dapagliflozin or empagliflozin]] (reduces mortality & hospitalizations in BOTH HFrEF and HFpEF regardless of diabetes status).",
                  },
                ],
              },
              {
                yield: "low",
                text: "**Loop Diuretics (Furosemide / Torsemide)**: Essential for symptom relief of congestion, though they do not independently reduce mortality.",
              },
            ],
          },
          {
            type: "callout",
            variant: "redflag",
            yield: "high",
            title: "Red Flag: Drugs to Avoid in HFrEF",
            text: "Avoid [[hl:non-dihydropyridine calcium channel blockers]] (verapamil, diltiazem), NSAIDs, and thiazolidinediones (pioglitazone), as they worsen fluid retention and precipitate decompensation.",
          },
        ],
      },
    ],
  },

  dka: {
    id: "dka",
    title: "Diabetic Ketoacidosis (DKA)",
    breadcrumbs: ["Internal Medicine", "Endocrinology", "Diabetes Mellitus"],
    lastUpdated: "Nov 2026",
    readTime: "6 min read",
    highYieldTag: "Core Shelf",
    calculatorDefault: "heart",
    qbankCount: 8,
    summary:
      "**Diabetic Ketoacidosis (DKA)** is a life-threatening acute metabolic complication of severe insulin deficiency and counter-regulatory hormone excess characterized by the triad of **hyperglycemia**, **ketonemia**, and **high-{{term:aniongap|anion gap}} metabolic acidosis**.",
    sections: [
      {
        id: "dka-diag",
        title: "1. Diagnostic Criteria & Pathophysiology",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Diagnostic Triad**: Glucose > 250 mg/dL (note: SGLT2 inhibitors can cause [[hl:euglycemic DKA]] with glucose < 250 mg/dL), arterial pH < 7.30 / HCO₃⁻ < 18 mEq/L, and positive serum/urine ketones (β-hydroxybutyrate predominant).",
              },
              {
                yield: "high",
                text: "**Clinical Features**: Polyuria/polydipsia, abdominal pain/vomiting, [[hl:Kussmaul respirations]] (deep, rapid compensatory hyperventilation), fruity acetone breath, severe volume depletion.",
              },
            ],
          },
        ],
      },
      {
        id: "dka-mgmt",
        title: "2. Management Protocol",
        blocks: [
          {
            type: "bullets",
            items: [
              {
                yield: "high",
                text: "**Step 1 — Aggressive IV Fluids**: Begin with [[hl:0.9% normal saline]] (1–1.5 L in first hour) before insulin to restore perfusion and lower counter-regulatory hormones.",
              },
              {
                yield: "high",
                text: "**Step 2 — Check Potassium BEFORE Starting Insulin**:",
                children: [
                  {
                    yield: "high",
                    text: "K⁺ < 3.3 mEq/L: [[hl:HOLD insulin]] and aggressively replete K⁺ first (insulin drives K⁺ intracellularly → fatal arrhythmias).",
                  },
                  {
                    yield: "high",
                    text: "K⁺ 3.3–5.2 mEq/L: Start IV regular insulin AND add 20–30 mEq KCl per liter of IV fluid.",
                  },
                ],
              },
              {
                yield: "high",
                text: "**Step 3 — Close the Anion Gap**: Add [[hl:D5W (dextrose)]] when serum glucose falls below 200–250 mg/dL while continuing IV insulin until the [[hl:{{term:aniongap|anion gap}} closes (< 12 mEq/L)]].",
              },
            ],
          },
          {
            type: "callout",
            variant: "pearl",
            yield: "high",
            title: "Clinical Pearl: Subcutaneous Transition Overlap",
            text: "Once the anion gap normalizes and the patient can tolerate oral intake, administer subcutaneous long-acting insulin and overlap with the IV insulin infusion for [[hl:1–2 hours]] before stopping the drip to prevent rebound ketoacidosis.",
          },
        ],
      },
    ],
  },
};

// ============================================================================
// 4. QBANK VIGNETTE DATA
// ============================================================================

const QBANK_QUESTIONS = {
  acs: [
    {
      id: "q-acs-1",
      difficulty: "Step 2 CK • High-Yield",
      stem: "A 66-year-old man with hypertension and hyperlipidemia is brought to the emergency department 45 minutes after developing severe crushing substernal chest pain radiating to his left shoulder, accompanied by diaphoresis and nausea. Vital signs are temperature 36.8°C, pulse 54/min, respirations 20/min, blood pressure 82/50 mmHg, and SpO₂ 96% on room air. Physical examination reveals jugular venous distension that increases on inspiration and clear lung fields bilaterally. A 12-lead ECG shows 3-mm ST-segment elevations in leads II, III, and aVF, with ST depression in aVL. Which of the following is the most appropriate immediate pharmacologic intervention alongside aspirin and heparin?",
      options: [
        { id: "A", text: "Sublingual nitroglycerin" },
        { id: "B", text: "IV normal saline bolus" },
        { id: "C", text: "IV metoprolol" },
        { id: "D", text: "IV furosemide" },
        { id: "E", text: "IV alteplase prior to obtaining chest X-ray" },
      ],
      correctId: "B",
      explanation:
        "This patient presents with an **inferior STEMI (leads II, III, aVF)** complicated by **right ventricular (RV) infarction**, evidenced by the classic triad of **hypotension, elevated JVP (with Kussmaul sign), and clear lung fields**. The ischemic right ventricle is acutely preload-dependent; therefore, immediate **IV normal saline fluid resuscitation** is required alongside emergent PCI. **Nitrates (A)** and **diuretics (D)** abruptly reduce preload and can precipitate fatal cardiogenic shock. **Beta-blockers (C)** worsen bradycardia and hypotension. **Alteplase (E)** is only considered if primary PCI is delayed > 120 min and contraindications (like aortic dissection) are excluded.",
    },
    {
      id: "q-acs-2",
      difficulty: "Internal Medicine Shelf",
      stem: "A 58-year-old man presents after experiencing two 15-minute episodes of severe substernal pressure at rest earlier this morning. He is currently completely pain-free. His vital signs are BP 136/82 mmHg, HR 72/min, SpO₂ 98%. A 12-lead ECG obtained while pain-free reveals deeply symmetric, inverted T waves in leads V2 and V3 without pathologic Q waves. Initial high-sensitivity troponin is mildly elevated. Which of the following is the next best step in management?",
      options: [
        { id: "A", text: "Exercise treadmill stress test prior to discharge" },
        { id: "B", text: "Dobutamine stress echocardiography" },
        { id: "C", text: "Urgent coronary angiography with PCI readiness" },
        { id: "D", text: "Outpatient Holter monitoring and statin initiation" },
        { id: "E", text: "Immediate IV tenecteplase" },
      ],
      correctId: "C",
      explanation:
        "Deeply inverted (or biphasic) T waves in V2–V3 during a pain-free interval represent **Wellens syndrome**, which is highly specific for critical stenosis of the **proximal left anterior descending (LAD)** coronary artery. Patients require **urgent coronary angiography** for revascularization. **Stress testing (A, B)** is strictly contraindicated because inducing myocardial oxygen demand can precipitate a massive, fatal anterior STEMI. **Tenecteplase (E)** is contraindicated in NSTE-ACS without ST elevation.",
    },
    {
      id: "q-acs-3",
      difficulty: "Step 2 CK",
      stem: "A 71-year-old woman who underwent medical management for an inferoposterior STEMI 5 days ago suddenly develops acute dyspnea and profound hypotension (BP 76/48 mmHg). Cardiac auscultation reveals a new, harsh grade 3/6 holosystolic murmur best heard at the cardiac apex radiating to the axilla, along with diffuse bilateral pulmonary crackles. Which of the following mechanical complications is most likely responsible?",
      options: [
        { id: "A", text: "Left ventricular free wall rupture" },
        { id: "B", text: "Posteromedial papillary muscle rupture" },
        { id: "C", text: "Dressler autoimmune pericarditis" },
        { id: "D", text: "Interventricular septal rupture" },
        { id: "E", text: "Left ventricular apical aneurysm" },
      ],
      correctId: "B",
      explanation:
        "Acute severe mitral regurgitation (new apical holosystolic murmur radiating to the axilla) and flash pulmonary edema 3–7 days after an inferior MI is classic for **posteromedial papillary muscle rupture**. The posteromedial papillary muscle is especially vulnerable because it has a single blood supply from the posterior descending artery (PDA), whereas the anterolateral muscle has dual supply (LAD + LCx). **Ventricular septal rupture (D)** causes a harsh holosystolic murmur at the left lower sternal border with an O₂ step-up in the RV. **Free wall rupture (A)** causes cardiac tamponade and PEA without a murmur.",
    },
  ],
  cap: [
    {
      id: "q-cap-1",
      difficulty: "Step 2 CK • High-Yield",
      stem: "A 68-year-old man with a history of well-controlled hypertension presents with 3 days of fever, productive cough, and pleuritic chest pain. Vitals: T 38.9°C, BP 104/68 mmHg, HR 102/min, RR 32/min, SpO₂ 91% on room air. He is alert and oriented to person, place, and time. Labs show BUN 24 mg/dL and WBC 15,800/mm³. Chest X-ray demonstrates a right lower lobe consolidation. Based on his CURB-65 score, what is the most appropriate disposition and empiric antibiotic regimen?",
      options: [
        { id: "A", text: "Outpatient discharge with oral amoxicillin" },
        { id: "B", text: "Outpatient discharge with oral azithromycin" },
        { id: "C", text: "Inpatient admission with IV ceftriaxone plus azithromycin" },
        { id: "D", text: "Inpatient admission with IV vancomycin plus piperacillin-tazobactam" },
        { id: "E", text: "Immediate ICU admission with oral doxycycline" },
      ],
      correctId: "C",
      explanation:
        "Calculating **CURB-65**: Confusion (0), Urea/BUN > 19 mg/dL (+1: BUN is 24), RR ≥ 30/min (+1: RR is 32), BP < 90/60 (0), Age ≥ 65 (+1: age 68). Total **CURB-65 = 3**, indicating severe CAP requiring **inpatient admission** (and evaluation for ICU level of care). Standard empiric inpatient non-ICU therapy is an **IV β-lactam (ceftriaxone) plus a macrolide (azithromycin)** or respiratory fluoroquinolone monotherapy. Broad MRSA/Pseudomonas coverage (D) is reserved for ICU severity with specific risk factors.",
    },
  ],
  hf: [
    {
      id: "q-hf-1",
      difficulty: "Internal Medicine Shelf",
      stem: "A 62-year-old woman with HFrEF (LVEF 30%) currently taking lisinopril, carvedilol, and furosemide is seen in clinic with NYHA Class II dyspnea. Vital signs show BP 122/74 mmHg, HR 66/min, Cr 1.1 mg/dL, K⁺ 4.3 mEq/L. Her cardiologist decides to switch lisinopril to sacubitril/valsartan. Which instruction is critical during this transition?",
      options: [
        { id: "A", text: "Discontinue carvedilol 24 hours prior" },
        { id: "B", text: "Observe a 36-hour washout period after stopping lisinopril" },
        { id: "C", text: "Overlap lisinopril and sacubitril/valsartan for 3 days" },
        { id: "D", text: "Stop furosemide indefinitely before starting ARNI" },
      ],
      correctId: "B",
      explanation:
        "Switching from an ACE inhibitor (lisinopril) to an ARNI (sacubitril/valsartan) requires a mandatory **36-hour washout period** because dual inhibition of ACE and neprilysin markedly elevates bradykinin levels and precipitates life-threatening **angioedema**.",
    },
  ],
  dka: [
    {
      id: "q-dka-1",
      difficulty: "Step 2 CK",
      stem: "A 22-year-old man with type 1 diabetes is admitted with DKA (glucose 520 mg/dL, pH 7.16, anion gap 26 mEq/L, initial K⁺ 3.0 mEq/L). After initiating a 1 L bolus of 0.9% normal saline, what is the next most appropriate step?",
      options: [
        { id: "A", text: "Begin IV regular insulin bolus and drip immediately" },
        { id: "B", text: "Administer IV sodium bicarbonate to raise pH > 7.25" },
        { id: "C", text: "Hold insulin and administer IV potassium chloride first" },
        { id: "D", text: "Switch IV fluids immediately to D5W" },
      ],
      correctId: "C",
      explanation:
        "In DKA, total body potassium is severely depleted despite often normal/high initial serum levels. Because this patient is already hypokalemic (**K⁺ < 3.3 mEq/L**), starting insulin immediately would drive potassium intracellularly and trigger fatal ventricular arrhythmias. **Hold insulin and replete IV potassium first** until K⁺ ≥ 3.3 mEq/L.",
    },
  ],
};

// ============================================================================
// 5. STUDY CONTEXT & INLINE RICH TEXT ENGINE (Highlights, Blanks, Tooltips)
// ============================================================================

const StudyContext = createContext(null);

function parseInlineNodes(text, keyPrefix = "n") {
  if (!text) return [];
  const nodes = [];
  let remaining = text;
  let idx = 0;

  while (remaining.length > 0) {
    const hlPos = remaining.indexOf("[[hl:");
    const termPos = remaining.indexOf("{{term:");
    const boldPos = remaining.indexOf("**");

    const candidates = [
      { type: "hl", pos: hlPos },
      { type: "term", pos: termPos },
      { type: "bold", pos: boldPos },
    ].filter((c) => c.pos !== -1);

    if (candidates.length === 0) {
      nodes.push({
        type: "text",
        content: remaining,
        key: `${keyPrefix}-${idx++}`,
      });
      break;
    }

    candidates.sort((a, b) => a.pos - b.pos);
    const next = candidates[0];

    if (next.pos > 0) {
      nodes.push({
        type: "text",
        content: remaining.slice(0, next.pos),
        key: `${keyPrefix}-${idx++}`,
      });
    }

    if (next.type === "hl") {
      const start = next.pos + 5;
      const end = remaining.indexOf("]]", start);
      if (end === -1) {
        nodes.push({
          type: "text",
          content: remaining.slice(next.pos),
          key: `${keyPrefix}-${idx++}`,
        });
        break;
      }
      const inner = remaining.slice(start, end);
      const nodeKey = `${keyPrefix}-${idx++}`;
      nodes.push({
        type: "hl",
        key: nodeKey,
        children: parseInlineNodes(inner, `${nodeKey}-in`),
      });
      remaining = remaining.slice(end + 2);
    } else if (next.type === "term") {
      const start = next.pos + 7;
      const end = remaining.indexOf("}}", start);
      if (end === -1) {
        nodes.push({
          type: "text",
          content: remaining.slice(next.pos),
          key: `${keyPrefix}-${idx++}`,
        });
        break;
      }
      const inner = remaining.slice(start, end);
      const pipeIdx = inner.indexOf("|");
      const termId =
        pipeIdx !== -1 ? inner.slice(0, pipeIdx).trim() : inner.trim();
      const label = pipeIdx !== -1 ? inner.slice(pipeIdx + 1) : inner;
      const nodeKey = `${keyPrefix}-${idx++}`;
      nodes.push({
        type: "term",
        termId,
        key: nodeKey,
        children: parseInlineNodes(label, `${nodeKey}-tm`),
      });
      remaining = remaining.slice(end + 2);
    } else if (next.type === "bold") {
      const start = next.pos + 2;
      const end = remaining.indexOf("**", start);
      if (end === -1) {
        nodes.push({
          type: "text",
          content: remaining.slice(next.pos),
          key: `${keyPrefix}-${idx++}`,
        });
        break;
      }
      const inner = remaining.slice(start, end);
      const nodeKey = `${keyPrefix}-${idx++}`;
      nodes.push({
        type: "bold",
        key: nodeKey,
        children: parseInlineNodes(inner, `${nodeKey}-bd`),
      });
      remaining = remaining.slice(end + 2);
    }
  }
  return nodes;
}

function collectBlankIdsFromText(text, keyPrefix, outIds) {
  const nodes = parseInlineNodes(text, keyPrefix);
  const walk = (arr) => {
    for (const node of arr) {
      if (node.type === "hl") {
        outIds.push(node.key);
      }
      if (node.children) walk(node.children);
    }
  };
  walk(nodes);
}

function getArticleStats(article, highYieldOnly) {
  const visibleBlankIds = [];
  let hiddenLowYieldCount = 0;

  const walkBullets = (items, prefix, parentHidden = false) => {
    items.forEach((item, i) => {
      const isLow = item.yield === "low";
      const hidden = parentHidden || (highYieldOnly && isLow);
      if (highYieldOnly && isLow && !parentHidden) {
        hiddenLowYieldCount += 1;
      }
      if (!hidden) {
        collectBlankIdsFromText(item.text, `${prefix}-b${i}`, visibleBlankIds);
      }
      if (item.children) {
        walkBullets(item.children, `${prefix}-b${i}-c`, hidden);
      }
    });
  };

  const walkBlocks = (blocks, prefix) => {
    blocks.forEach((block, bi) => {
      const isLow = block.yield === "low";
      if (highYieldOnly && isLow) {
        hiddenLowYieldCount += 1;
        return;
      }
      if (block.type === "paragraph") {
        collectBlankIdsFromText(block.text, `${prefix}-p${bi}`, visibleBlankIds);
      } else if (block.type === "callout") {
        collectBlankIdsFromText(block.text, `${prefix}-co${bi}`, visibleBlankIds);
      } else if (block.type === "bullets") {
        walkBullets(block.items, `${prefix}-ul${bi}`, false);
      } else if (block.type === "table") {
        block.rows.forEach((row, ri) => {
          row.forEach((cell, ci) => {
            collectBlankIdsFromText(
              cell,
              `${prefix}-t${bi}-r${ri}-c${ci}`,
              visibleBlankIds
            );
          });
        });
      }
    });
  };

  if (article.summary) {
    collectBlankIdsFromText(article.summary, `${article.id}-summary`, visibleBlankIds);
  }
  article.sections.forEach((sec) => {
    if (sec.blocks) walkBlocks(sec.blocks, sec.id);
    if (sec.subsections) {
      sec.subsections.forEach((sub) => {
        if (sub.blocks) walkBlocks(sub.blocks, sub.id);
      });
    }
  });

  return { visibleBlankIds, hiddenLowYieldCount };
}

function RichNodes({ nodes, suppressTooltip = false }) {
  const {
    highlightsOn,
    quizModeOn,
    revealedBlanks,
    toggleBlank,
    isDark,
    openTooltip,
    scheduleCloseTooltip,
    pinTooltip,
  } = useContext(StudyContext);

  return nodes.map((node) => {
    if (node.type === "text") {
      return <React.Fragment key={node.key}>{node.content}</React.Fragment>;
    }

    if (node.type === "bold") {
      return (
        <strong
          key={node.key}
          className={`font-semibold ${isDark ? "text-slate-100" : "text-slate-900"}`}
        >
          <RichNodes nodes={node.children} suppressTooltip={suppressTooltip} />
        </strong>
      );
    }

    if (node.type === "term") {
      const termData = MEDICAL_GLOSSARY[node.termId];
      if (!termData || suppressTooltip) {
        return (
          <span key={node.key}>
            <RichNodes nodes={node.children} suppressTooltip={suppressTooltip} />
          </span>
        );
      }

      return (
        <span
          key={node.key}
          role="button"
          tabIndex={0}
          onMouseEnter={(e) => openTooltip(node.termId, e.currentTarget)}
          onMouseLeave={() => scheduleCloseTooltip()}
          onClick={(e) => {
            e.stopPropagation();
            pinTooltip(node.termId, e.currentTarget);
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              pinTooltip(node.termId, e.currentTarget);
            }
          }}
          className={`underline decoration-dotted underline-offset-[3px] cursor-pointer transition-colors ${
            isDark
              ? "decoration-sky-400/80 text-sky-300 hover:text-sky-200 hover:bg-sky-500/10 rounded px-0.5 -mx-0.5"
              : "decoration-sky-600/75 text-sky-800 hover:text-sky-700 hover:bg-sky-50 rounded px-0.5 -mx-0.5"
          }`}
        >
          <RichNodes nodes={node.children} suppressTooltip={false} />
        </span>
      );
    }

    if (node.type === "hl") {
      const isRevealed = revealedBlanks.has(node.key);
      const isBlurred = quizModeOn && !isRevealed;

      if (isBlurred) {
        return (
          <span
            key={node.key}
            role="button"
            tabIndex={0}
            title="Click to reveal answer"
            onClick={(e) => {
              e.stopPropagation();
              toggleBlank(node.key);
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                toggleBlank(node.key);
              }
            }}
            className={`inline-block blur-sm select-none cursor-pointer rounded px-1.5 py-0.5 mx-0.5 transition-all border ${
              isDark
                ? "bg-slate-700 border-slate-600 text-slate-300 hover:bg-slate-600"
                : "bg-slate-200 border-slate-300/80 text-slate-700 hover:bg-slate-300/80"
            }`}
          >
            <RichNodes nodes={node.children} suppressTooltip={true} />
          </span>
        );
      }

      const highlightClasses = highlightsOn
        ? isDark
          ? "bg-amber-400/25 text-amber-100 ring-1 ring-amber-400/40 px-1 rounded-sm"
          : "bg-yellow-200/70 text-slate-900 px-1 rounded-sm"
        : quizModeOn && isRevealed
        ? isDark
          ? "bg-emerald-500/20 text-emerald-200 ring-1 ring-emerald-500/40 px-1 rounded-sm cursor-pointer"
          : "bg-emerald-100/80 text-emerald-950 ring-1 ring-emerald-300 px-1 rounded-sm cursor-pointer"
        : "";

      return (
        <span
          key={node.key}
          onClick={
            quizModeOn && isRevealed
              ? (e) => {
                  e.stopPropagation();
                  toggleBlank(node.key);
                }
              : undefined
          }
          title={quizModeOn && isRevealed ? "Click to hide again" : undefined}
          className={`transition-colors ${highlightClasses}`}
        >
          <RichNodes nodes={node.children} suppressTooltip={false} />
        </span>
      );
    }

    return null;
  });
}

function RichText({ text, pathPrefix }) {
  const nodes = useMemo(
    () => parseInlineNodes(text, pathPrefix),
    [text, pathPrefix]
  );
  return <RichNodes nodes={nodes} />;
}

// ============================================================================
// 6. ARTICLE BUILDING BLOCKS (Bullets, Callouts, Tables, Accordions)
// ============================================================================

function BulletTree({ items, prefix, level = 0, highYieldOnly, isDark }) {
  const visibleItems = highYieldOnly
    ? items.filter((item) => item.yield !== "low")
    : items;

  if (visibleItems.length === 0) return null;

  return (
    <ul
      className={
        level === 0
          ? "space-y-2.5"
          : `mt-2 space-y-2 pl-4 ml-1.5 border-l ${
              isDark ? "border-slate-700/80" : "border-slate-200"
            }`
      }
    >
      {items.map((item, idx) => {
        if (highYieldOnly && item.yield === "low") return null;
        const itemPrefix = `${prefix}-b${idx}`;

        return (
          <li key={itemPrefix} className="relative flex items-start gap-2.5">
            <span className="shrink-0 mt-[9px]">
              {level === 0 ? (
                <span
                  className={`block w-1.5 h-1.5 rounded-full ${
                    isDark ? "bg-sky-400" : "bg-sky-600"
                  }`}
                />
              ) : level === 1 ? (
                <span
                  className={`block w-1.5 h-1.5 rounded-full border ${
                    isDark
                      ? "border-teal-400 bg-slate-900"
                      : "border-teal-600 bg-white"
                  }`}
                />
              ) : (
                <span
                  className={`block w-1.5 h-[2px] mt-[2px] ${
                    isDark ? "bg-slate-400" : "bg-slate-400"
                  }`}
                />
              )}
            </span>

            <div className="flex-1 min-w-0 leading-[1.6]">
              <span
                className={
                  item.yield === "low"
                    ? isDark
                      ? "text-slate-300"
                      : "text-slate-700"
                    : isDark
                    ? "text-slate-200"
                    : "text-slate-800"
                }
              >
                <RichText text={item.text} pathPrefix={itemPrefix} />
              </span>
              {item.yield === "low" && !highYieldOnly && (
                <span
                  className={`ml-2 inline-flex items-center px-1.5 py-0.5 text-[10px] font-medium rounded ${
                    isDark
                      ? "bg-slate-800 text-slate-400 border border-slate-700"
                      : "bg-slate-100 text-slate-500 border border-slate-200"
                  }`}
                >
                  Detail
                </span>
              )}
              {item.children && (
                <BulletTree
                  items={item.children}
                  prefix={`${itemPrefix}-c`}
                  level={level + 1}
                  highYieldOnly={highYieldOnly}
                  isDark={isDark}
                />
              )}
            </div>
          </li>
        );
      })}
    </ul>
  );
}

function CalloutBox({ block, prefix, isDark }) {
  const isRed = block.variant === "redflag";

  const styles = isRed
    ? isDark
      ? "bg-red-950/40 border-l-4 border-red-500 border-y border-r border-y-red-900/60 border-r-red-900/60"
      : "bg-[#FEF2F2] border-l-4 border-[#EF4444] border-y border-r border-y-red-200/70 border-r-red-200/70"
    : isDark
    ? "bg-amber-950/35 border-l-4 border-amber-500 border-y border-r border-y-amber-900/60 border-r-amber-900/60"
    : "bg-[#FEFCE8] border-l-4 border-[#EAB308] border-y border-r border-y-yellow-200/80 border-r-yellow-200/80";

  const titleColor = isRed
    ? isDark
      ? "text-red-300"
      : "text-red-800"
    : isDark
    ? "text-amber-300"
    : "text-amber-900";

  const iconColor = isRed
    ? isDark
      ? "text-red-400"
      : "text-[#EF4444]"
    : isDark
    ? "text-amber-400"
    : "text-[#CA8A04]";

  const bodyColor = isRed
    ? isDark
      ? "text-red-100/90"
      : "text-red-950/90"
    : isDark
    ? "text-amber-100/90"
    : "text-amber-950/90";

  return (
    <div className={`rounded-r-lg p-4 my-4 ${styles}`}>
      <div className="flex items-start gap-3">
        <div className={`shrink-0 mt-0.5 ${iconColor}`}>
          {isRed ? (
            <AlertTriangle className="w-5 h-5" />
          ) : (
            <Lightbulb className="w-5 h-5" />
          )}
        </div>
        <div className="min-w-0 flex-1">
          <h4 className={`text-sm font-bold tracking-tight mb-1 ${titleColor}`}>
            {block.title}
          </h4>
          <p className={`text-sm leading-[1.6] ${bodyColor}`}>
            <RichText text={block.text} pathPrefix={prefix} />
          </p>
        </div>
      </div>
    </div>
  );
}

function ComparisonTable({ block, prefix, isDark }) {
  return (
    <div className="my-5">
      {block.caption && (
        <div
          className={`text-xs font-semibold uppercase tracking-wider mb-2 ${
            isDark ? "text-slate-400" : "text-slate-500"
          }`}
        >
          {block.caption}
        </div>
      )}
      <div
        className={`overflow-x-auto rounded-lg border ${
          isDark ? "border-slate-700" : "border-slate-200"
        }`}
      >
        <table className="w-full text-left border-collapse text-sm">
          <thead>
            <tr
              className={
                isDark
                  ? "bg-slate-800/90 text-slate-200 border-b border-slate-700"
                  : "bg-slate-50 text-slate-800 border-b border-slate-200"
              }
            >
              {block.headers.map((header, hi) => (
                <th
                  key={hi}
                  className={`py-2.5 px-3.5 font-semibold tracking-tight whitespace-nowrap ${
                    hi > 0
                      ? isDark
                        ? "border-l border-slate-700"
                        : "border-l border-slate-200"
                      : ""
                  }`}
                >
                  <RichText text={header} pathPrefix={`${prefix}-th-${hi}`} />
                </th>
              ))}
            </tr>
          </thead>
          <tbody
            className={`divide-y ${
              isDark ? "divide-slate-800" : "divide-slate-200"
            }`}
          >
            {block.rows.map((row, ri) => (
              <tr
                key={ri}
                className={
                  isDark
                    ? "bg-slate-900/50 hover:bg-slate-800/40 transition-colors"
                    : "bg-white hover:bg-slate-50/80 transition-colors"
                }
              >
                {row.map((cell, ci) => (
                  <td
                    key={ci}
                    className={`py-2.5 px-3.5 align-top leading-relaxed ${
                      ci === 0
                        ? isDark
                          ? "bg-slate-800/30 text-slate-200 font-medium"
                          : "bg-slate-50/50 text-slate-800 font-medium"
                        : isDark
                        ? "text-slate-300"
                        : "text-slate-700"
                    } ${
                      ci > 0
                        ? isDark
                          ? "border-l border-slate-800"
                          : "border-l border-slate-200"
                        : ""
                    }`}
                  >
                    <RichText
                      text={cell}
                      pathPrefix={`${prefix}-r${ri}-c${ci}`}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function BlockRenderer({ blocks, prefix, highYieldOnly, isDark }) {
  return (
    <div className="space-y-4">
      {blocks.map((block, bi) => {
        if (highYieldOnly && block.yield === "low") return null;

        if (block.type === "paragraph") {
          return (
            <p
              key={`${prefix}-p${bi}`}
              className={`text-[15px] leading-[1.65] ${
                isDark ? "text-slate-300" : "text-slate-700"
              }`}
            >
              <RichText text={block.text} pathPrefix={`${prefix}-p${bi}`} />
            </p>
          );
        }

        if (block.type === "bullets") {
          return (
            <BulletTree
              key={`${prefix}-ul${bi}`}
              items={block.items}
              prefix={`${prefix}-ul${bi}`}
              highYieldOnly={highYieldOnly}
              isDark={isDark}
            />
          );
        }

        if (block.type === "callout") {
          return (
            <CalloutBox
              key={`${prefix}-co${bi}`}
              block={block}
              prefix={`${prefix}-co${bi}`}
              isDark={isDark}
            />
          );
        }

        if (block.type === "table") {
          return (
            <ComparisonTable
              key={`${prefix}-t${bi}`}
              block={block}
              prefix={`${prefix}-t${bi}`}
              isDark={isDark}
            />
          );
        }

        return null;
      })}
    </div>
  );
}

function SubAccordion({ sub, isOpen, onToggle, highYieldOnly, isDark }) {
  return (
    <div
      id={`section-${sub.id}`}
      className={`scroll-mt-24 rounded-lg border transition-colors ${
        isDark
          ? "border-slate-700/80 bg-slate-900/60"
          : "border-slate-200 bg-slate-50/60"
      }`}
    >
      <button
        type="button"
        onClick={() => onToggle(sub.id)}
        className={`w-full flex items-center justify-between gap-3 px-4 py-3 text-left transition-colors rounded-lg ${
          isDark
            ? "hover:bg-slate-800/70 text-slate-100"
            : "hover:bg-slate-100/80 text-slate-800"
        }`}
      >
        <span className="text-[15px] font-semibold tracking-tight flex items-center gap-2">
          <span
            className={`w-1.5 h-4 rounded-full ${
              isOpen
                ? isDark
                  ? "bg-teal-400"
                  : "bg-teal-600"
                : isDark
                ? "bg-slate-600"
                : "bg-slate-300"
            }`}
          />
          {sub.title}
        </span>
        <ChevronDown
          className={`w-4 h-4 shrink-0 transition-transform duration-200 ${
            isOpen ? "rotate-180" : ""
          } ${isDark ? "text-slate-400" : "text-slate-500"}`}
        />
      </button>

      {isOpen && (
        <div
          className={`px-4 pb-4 pt-2 border-t ${
            isDark ? "border-slate-800" : "border-slate-200/80"
          }`}
        >
          <BlockRenderer
            blocks={sub.blocks}
            prefix={sub.id}
            highYieldOnly={highYieldOnly}
            isDark={isDark}
          />
        </div>
      )}
    </div>
  );
}

function AccordionSection({
  section,
  openSections,
  onToggleSection,
  highYieldOnly,
  isDark,
  highlightedAnchor,
}) {
  const isOpen = !!openSections[section.id];
  const isAnchorHighlight = highlightedAnchor === section.id;

  return (
    <section
      id={`section-${section.id}`}
      className={`scroll-mt-20 rounded-xl border transition-all duration-300 ${
        isAnchorHighlight
          ? isDark
            ? "border-sky-500 ring-2 ring-sky-500/30 bg-slate-900"
            : "border-sky-500 ring-2 ring-sky-400/30 bg-white"
          : isDark
          ? "border-slate-800 bg-slate-900/40"
          : "border-slate-200/90 bg-white"
      }`}
    >
      <button
        type="button"
        onClick={() => onToggleSection(section.id)}
        className={`w-full flex items-center justify-between gap-3 px-5 py-4 text-left transition-colors ${
          isOpen
            ? isDark
              ? "border-b border-slate-800 bg-slate-800/40 rounded-t-xl"
              : "border-b border-slate-100 bg-slate-50/70 rounded-t-xl"
            : isDark
            ? "hover:bg-slate-800/40 rounded-xl"
            : "hover:bg-slate-50/70 rounded-xl"
        }`}
      >
        <div className="flex items-center gap-3 min-w-0">
          <h2
            className={`text-lg font-bold tracking-tight truncate ${
              isDark ? "text-slate-100" : "text-slate-900"
            }`}
          >
            {section.title}
          </h2>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {section.subsections && (
            <span
              className={`hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium ${
                isDark
                  ? "bg-slate-800 text-slate-400"
                  : "bg-slate-100 text-slate-500"
              }`}
            >
              {section.subsections.length} subsections
            </span>
          )}
          <ChevronDown
            className={`w-5 h-5 transition-transform duration-200 ${
              isOpen ? "rotate-180" : ""
            } ${isDark ? "text-slate-400" : "text-slate-500"}`}
          />
        </div>
      </button>

      {isOpen && (
        <div className="p-5 space-y-4">
          {section.blocks && (
            <BlockRenderer
              blocks={section.blocks}
              prefix={section.id}
              highYieldOnly={highYieldOnly}
              isDark={isDark}
            />
          )}

          {section.subsections && (
            <div className="space-y-3 pt-1">
              {section.subsections.map((sub) => (
                <SubAccordion
                  key={sub.id}
                  sub={sub}
                  isOpen={!!openSections[sub.id]}
                  onToggle={onToggleSection}
                  highYieldOnly={highYieldOnly}
                  isDark={isDark}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
}

// ============================================================================
// 7. RIGHT SIDEBAR TOOLS: CLINICAL CALCULATORS, QBANK, NOTES
// ============================================================================

function HeartScoreCalculator({ isDark }) {
  const [scores, setScores] = useState({
    history: 1,
    ecg: 1,
    age: 1,
    risk: 1,
    troponin: 0,
  });

  const total =
    scores.history + scores.ecg + scores.age + scores.risk + scores.troponin;

  const riskInfo =
    total <= 3
      ? {
          label: "Low Risk (0–3)",
          mace: "0.9–1.7% 6-wk MACE",
          action: "Consider early discharge with outpatient follow-up.",
          badge: isDark
            ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
            : "bg-emerald-50 text-emerald-700 border-emerald-200",
        }
      : total <= 6
      ? {
          label: "Moderate Risk (4–6)",
          mace: "12–16.6% 6-wk MACE",
          action: "Admit for clinical observation, serial troponins & testing.",
          badge: isDark
            ? "bg-amber-500/20 text-amber-300 border-amber-500/40"
            : "bg-amber-50 text-amber-800 border-amber-200",
        }
      : {
          label: "High Risk (7–10)",
          mace: "50–65% 6-wk MACE",
          action: "Early invasive strategy / urgent cardiology intervention.",
          badge: isDark
            ? "bg-red-500/20 text-red-300 border-red-500/40"
            : "bg-red-50 text-red-700 border-red-200",
        };

  const criteria = [
    {
      key: "history",
      label: "History",
      opts: [
        { val: 0, text: "Slightly susp." },
        { val: 1, text: "Moderately" },
        { val: 2, text: "Highly susp." },
      ],
    },
    {
      key: "ecg",
      label: "ECG",
      opts: [
        { val: 0, text: "Normal" },
        { val: 1, text: "Non-spec." },
        { val: 2, text: "ST dev." },
      ],
    },
    {
      key: "age",
      label: "Age",
      opts: [
        { val: 0, text: "< 45" },
        { val: 1, text: "45–64" },
        { val: 2, text: "≥ 65" },
      ],
    },
    {
      key: "risk",
      label: "Risk Factors",
      opts: [
        { val: 0, text: "None" },
        { val: 1, text: "1–2 RFs" },
        { val: 2, text: "≥ 3 / CAD" },
      ],
    },
    {
      key: "troponin",
      label: "Initial Troponin",
      opts: [
        { val: 0, text: "≤ Normal" },
        { val: 1, text: "1–3x ULN" },
        { val: 2, text: "> 3x ULN" },
      ],
    },
  ];

  return (
    <div className="space-y-3">
      <div className="space-y-2.5">
        {criteria.map((row) => (
          <div key={row.key}>
            <div
              className={`text-[11px] font-semibold mb-1 flex justify-between ${
                isDark ? "text-slate-300" : "text-slate-600"
              }`}
            >
              <span>{row.label}</span>
              <span className="text-sky-600 dark:text-sky-400">
                +{scores[row.key]}
              </span>
            </div>
            <div className="grid grid-cols-3 gap-1">
              {row.opts.map((opt) => {
                const active = scores[row.key] === opt.val;
                return (
                  <button
                    key={opt.val}
                    type="button"
                    onClick={() =>
                      setScores((prev) => ({ ...prev, [row.key]: opt.val }))
                    }
                    className={`px-1.5 py-1 rounded text-[11px] font-medium border transition-all truncate ${
                      active
                        ? isDark
                          ? "bg-sky-600 text-white border-sky-500 shadow-sm"
                          : "bg-[#0284C7] text-white border-[#0284C7] shadow-sm"
                        : isDark
                        ? "bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700"
                        : "bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100"
                    }`}
                  >
                    {opt.text}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <div className={`p-3 rounded-lg border ${riskInfo.badge}`}>
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-bold">{riskInfo.label}</span>
          <span className="text-base font-extrabold">{total} / 10</span>
        </div>
        <div className="text-[11px] font-semibold opacity-90 mb-1">
          {riskInfo.mace}
        </div>
        <p className="text-[11px] leading-snug opacity-90">{riskInfo.action}</p>
      </div>
    </div>
  );
}

function Curb65Calculator({ isDark }) {
  const [checks, setChecks] = useState({
    c: false,
    u: false,
    r: false,
    b: false,
    age: true,
  });

  const total = Object.values(checks).filter(Boolean).length;

  const items = [
    { key: "c", label: "Confusion (new onset)" },
    { key: "u", label: "Urea / BUN > 19 mg/dL (7 mmol/L)" },
    { key: "r", label: "Respiratory rate ≥ 30 /min" },
    { key: "b", label: "BP < 90 systolic or ≤ 60 diastolic" },
    { key: "age", label: "Age ≥ 65 years" },
  ];

  const interp =
    total <= 1
      ? {
          label: "Low Risk (0–1)",
          rec: "Outpatient treatment (~1.5% 30-day mortality).",
          cls: isDark
            ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
            : "bg-emerald-50 text-emerald-700 border-emerald-200",
        }
      : total === 2
      ? {
          label: "Moderate Risk (2)",
          rec: "Consider short inpatient stay or close outpatient monitoring.",
          cls: isDark
            ? "bg-amber-500/20 text-amber-300 border-amber-500/40"
            : "bg-amber-50 text-amber-800 border-amber-200",
        }
      : {
          label: "Severe CAP (3–5)",
          rec: "Inpatient admission; assess for ICU level care (score 4–5).",
          cls: isDark
            ? "bg-red-500/20 text-red-300 border-red-500/40"
            : "bg-red-50 text-red-700 border-red-200",
        };

  return (
    <div className="space-y-3">
      <div className="space-y-1.5">
        {items.map((item) => (
          <label
            key={item.key}
            className={`flex items-center gap-2 p-2 rounded-md border text-xs cursor-pointer transition-colors ${
              checks[item.key]
                ? isDark
                  ? "bg-sky-950/50 border-sky-700 text-sky-200"
                  : "bg-sky-50 border-sky-300 text-sky-900"
                : isDark
                ? "bg-slate-800/60 border-slate-700 text-slate-300 hover:bg-slate-800"
                : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
            }`}
          >
            <input
              type="checkbox"
              checked={checks[item.key]}
              onChange={() =>
                setChecks((prev) => ({ ...prev, [item.key]: !prev[item.key] }))
              }
              className="rounded accent-sky-600"
            />
            <span className="leading-tight">{item.label}</span>
          </label>
        ))}
      </div>

      <div className={`p-3 rounded-lg border ${interp.cls}`}>
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-bold">{interp.label}</span>
          <span className="text-base font-extrabold">{total} / 5</span>
        </div>
        <p className="text-[11px] leading-snug opacity-90">{interp.rec}</p>
      </div>
    </div>
  );
}

// ============================================================================
// 8. INTERACTIVE MODALS (Qbank Session, Command Search, Tooltip Popover)
// ============================================================================

function QbankModal({ article, onClose, isDark }) {
  const questions = QBANK_QUESTIONS[article.id] || QBANK_QUESTIONS.acs;
  const [qIdx, setQIdx] = useState(0);
  const [selectedByQ, setSelectedByQ] = useState({});
  const [submittedByQ, setSubmittedByQ] = useState({});
  const [struckByQ, setStruckByQ] = useState({});

  const currentQ = questions[qIdx];
  const selected = selectedByQ[currentQ.id];
  const isSubmitted = !!submittedByQ[currentQ.id];
  const struckSet = struckByQ[currentQ.id] || new Set();

  const toggleStrike = (optId, e) => {
    e.stopPropagation();
    if (isSubmitted) return;
    setStruckByQ((prev) => {
      const next = new Set(prev[currentQ.id] || []);
      if (next.has(optId)) next.delete(optId);
      else next.add(optId);
      return { ...prev, [currentQ.id]: next };
    });
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className={`w-full max-w-2xl max-h-[88vh] flex flex-col rounded-2xl border shadow-2xl overflow-hidden ${
          isDark
            ? "bg-slate-900 border-slate-700 text-slate-100"
            : "bg-white border-slate-200 text-slate-800"
        }`}
      >
        <div
          className={`px-5 py-3.5 border-b flex items-center justify-between ${
            isDark ? "border-slate-800 bg-slate-800/50" : "border-slate-200 bg-slate-50"
          }`}
        >
          <div className="flex items-center gap-2.5">
            <span className="p-1.5 rounded-lg bg-teal-600 text-white">
              <HelpCircle className="w-4 h-4" />
            </span>
            <div>
              <h3 className="text-sm font-bold tracking-tight">
                Qbank Vignette Practice — {article.title}
              </h3>
              <p
                className={`text-xs ${
                  isDark ? "text-slate-400" : "text-slate-500"
                }`}
              >
                Question {qIdx + 1} of {questions.length} • {currentQ.difficulty}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className={`p-1.5 rounded-lg transition-colors ${
              isDark
                ? "hover:bg-slate-700 text-slate-400"
                : "hover:bg-slate-200 text-slate-500"
            }`}
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 overflow-y-auto space-y-4">
          <p className="text-[14.5px] leading-relaxed">{currentQ.stem}</p>

          <div className="space-y-2">
            {currentQ.options.map((opt) => {
              const isSelected = selected === opt.id;
              const isCorrect = opt.id === currentQ.correctId;
              const isStruck = struckSet.has(opt.id);

              let optClass = isDark
                ? "border-slate-700 bg-slate-800/50 hover:bg-slate-800"
                : "border-slate-200 bg-white hover:bg-slate-50";

              if (isSubmitted) {
                if (isCorrect) {
                  optClass = isDark
                    ? "border-emerald-500 bg-emerald-950/50 text-emerald-200"
                    : "border-emerald-500 bg-emerald-50 text-emerald-950";
                } else if (isSelected && !isCorrect) {
                  optClass = isDark
                    ? "border-red-500 bg-red-950/50 text-red-200"
                    : "border-red-400 bg-red-50 text-red-950";
                }
              } else if (isSelected) {
                optClass = isDark
                  ? "border-sky-500 bg-sky-950/50 ring-1 ring-sky-500"
                  : "border-sky-600 bg-sky-50 ring-1 ring-sky-600";
              }

              return (
                <div
                  key={opt.id}
                  role="button"
                  tabIndex={0}
                  onClick={() => {
                    if (isSubmitted) return;
                    setSelectedByQ((prev) => ({
                      ...prev,
                      [currentQ.id]: opt.id,
                    }));
                  }}
                  onKeyDown={(e) => {
                    if ((e.key === "Enter" || e.key === " ") && !isSubmitted) {
                      e.preventDefault();
                      setSelectedByQ((prev) => ({
                        ...prev,
                        [currentQ.id]: opt.id,
                      }));
                    }
                  }}
                  className={`flex items-center justify-between gap-3 px-3.5 py-2.5 rounded-xl border text-sm cursor-pointer transition-all ${optClass}`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span
                      className={`w-6 h-6 shrink-0 rounded-full flex items-center justify-center text-xs font-bold border ${
                        isSelected
                          ? "bg-sky-600 text-white border-sky-600"
                          : isDark
                          ? "border-slate-600 text-slate-300"
                          : "border-slate-300 text-slate-600"
                      }`}
                    >
                      {opt.id}
                    </span>
                    <span
                      className={
                        isStruck && !isSubmitted ? "line-through opacity-45" : ""
                      }
                    >
                      {opt.text}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    {isSubmitted && isCorrect && (
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    )}
                    {isSubmitted && isSelected && !isCorrect && (
                      <XCircle className="w-4 h-4 text-red-500" />
                    )}
                    {!isSubmitted && (
                      <button
                        type="button"
                        title="Cross out option"
                        onClick={(e) => toggleStrike(opt.id, e)}
                        className={`text-[11px] px-1.5 py-0.5 rounded border ${
                          isDark
                            ? "border-slate-700 text-slate-400 hover:text-slate-200"
                            : "border-slate-200 text-slate-400 hover:text-slate-700"
                        }`}
                      >
                        S̶
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {isSubmitted && (
            <div
              className={`p-4 rounded-xl border text-sm leading-relaxed ${
                isDark
                  ? "bg-slate-800/70 border-slate-700 text-slate-200"
                  : "bg-sky-50/70 border-sky-200 text-slate-800"
              }`}
            >
              <div className="font-bold text-xs uppercase tracking-wider mb-1.5 text-sky-600 dark:text-sky-400">
                High-Yield Explanation
              </div>
              <RichText text={currentQ.explanation} pathPrefix={`qexp-${currentQ.id}`} />
            </div>
          )}
        </div>

        <div
          className={`px-5 py-3 border-t flex items-center justify-between ${
            isDark ? "border-slate-800 bg-slate-800/30" : "border-slate-200 bg-slate-50"
          }`}
        >
          <div className="flex items-center gap-2">
            <button
              type="button"
              disabled={qIdx === 0}
              onClick={() => setQIdx((i) => Math.max(0, i - 1))}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border disabled:opacity-40 ${
                isDark
                  ? "border-slate-700 hover:bg-slate-800"
                  : "border-slate-300 bg-white hover:bg-slate-100"
              }`}
            >
              Previous
            </button>
            <button
              type="button"
              disabled={qIdx === questions.length - 1}
              onClick={() => setQIdx((i) => Math.min(questions.length - 1, i + 1))}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border disabled:opacity-40 ${
                isDark
                  ? "border-slate-700 hover:bg-slate-800"
                  : "border-slate-300 bg-white hover:bg-slate-100"
              }`}
            >
              Next
            </button>
          </div>

          {!isSubmitted ? (
            <button
              type="button"
              disabled={!selected}
              onClick={() =>
                setSubmittedByQ((prev) => ({ ...prev, [currentQ.id]: true }))
              }
              className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-[#0284C7] hover:bg-sky-700 text-white disabled:opacity-40 transition-colors"
            >
              Check Answer
            </button>
          ) : (
            <span
              className={`text-xs font-semibold ${
                selected === currentQ.correctId
                  ? "text-emerald-500"
                  : "text-red-500"
              }`}
            >
              {selected === currentQ.correctId
                ? "Correct Answer!"
                : `Incorrect — Correct is ${currentQ.correctId}`}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

function CommandSearchModal({
  isOpen,
  onClose,
  activeArticle,
  onSelectArticle,
  onJumpToSection,
  isDark,
}) {
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setQuery("");
      setActiveIndex(0);
      setTimeout(() => inputRef.current?.focus(), 20);
    }
  }, [isOpen]);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    const list = [];

    // 1. Articles
    Object.values(ARTICLES).forEach((art) => {
      if (
        !q ||
        art.title.toLowerCase().includes(q) ||
        art.breadcrumbs.join(" ").toLowerCase().includes(q)
      ) {
        list.push({
          type: "Article",
          id: `art-${art.id}`,
          title: art.title,
          subtitle: art.breadcrumbs.join(" › "),
          action: () => onSelectArticle(art.id),
        });
      }
    });

    // 2. Sections & Subsections of current article
    activeArticle.sections.forEach((sec) => {
      if (!q || sec.title.toLowerCase().includes(q)) {
        list.push({
          type: "Section",
          id: `sec-${sec.id}`,
          title: sec.title,
          subtitle: `In ${activeArticle.title}`,
          action: () => onJumpToSection(sec.id, null),
        });
      }
      if (sec.subsections) {
        sec.subsections.forEach((sub) => {
          if (!q || sub.title.toLowerCase().includes(q)) {
            list.push({
              type: "Subsection",
              id: `sub-${sub.id}`,
              title: sub.title,
              subtitle: sec.title,
              action: () => onJumpToSection(sub.id, sec.id),
            });
          }
        });
      }
    });

    // 3. Medical Glossary Terms
    Object.values(MEDICAL_GLOSSARY).forEach((term) => {
      if (
        !q ||
        term.title.toLowerCase().includes(q) ||
        term.category.toLowerCase().includes(q) ||
        term.definition.toLowerCase().includes(q)
      ) {
        list.push({
          type: term.category,
          id: `term-${term.id}`,
          title: term.title,
          subtitle: term.definition,
          action: () => {
            onSelectArticle(term.articleId, term.sectionId);
          },
        });
      }
    });

    return list.slice(0, 14);
  }, [query, activeArticle, onSelectArticle, onJumpToSection]);

  useEffect(() => {
    setActiveIndex(0);
  }, [query]);

  if (!isOpen) return null;

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIndex((i) => (results.length ? (i + 1) % results.length : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((i) =>
        results.length ? (i - 1 + results.length) % results.length : 0
      );
    } else if (e.key === "Enter" && results[activeIndex]) {
      e.preventDefault();
      results[activeIndex].action();
      onClose();
    } else if (e.key === "Escape") {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center pt-[10vh] px-4 bg-slate-950/60 backdrop-blur-xs"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
        className={`w-full max-w-xl rounded-2xl border shadow-2xl overflow-hidden ${
          isDark
            ? "bg-slate-900 border-slate-700 text-slate-100"
            : "bg-white border-slate-200 text-slate-800"
        }`}
      >
        <div
          className={`flex items-center gap-3 px-4 py-3 border-b ${
            isDark ? "border-slate-800" : "border-slate-200"
          }`}
        >
          <Search
            className={`w-4 h-4 shrink-0 ${
              isDark ? "text-slate-400" : "text-slate-500"
            }`}
          />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search articles, ECG signs, medications, sections..."
            className="w-full bg-transparent text-sm outline-none placeholder:text-slate-400"
          />
          <button
            type="button"
            onClick={onClose}
            className={`px-1.5 py-0.5 text-[11px] font-medium rounded border ${
              isDark
                ? "border-slate-700 text-slate-400"
                : "border-slate-200 text-slate-500"
            }`}
          >
            ESC
          </button>
        </div>

        <div className="max-h-[55vh] overflow-y-auto p-2 space-y-1">
          {results.length === 0 ? (
            <div
              className={`py-8 text-center text-sm ${
                isDark ? "text-slate-400" : "text-slate-500"
              }`}
            >
              No matching clinical topics or terms found.
            </div>
          ) : (
            results.map((item, idx) => {
              const selected = idx === activeIndex;
              return (
                <button
                  key={item.id}
                  type="button"
                  onMouseEnter={() => setActiveIndex(idx)}
                  onClick={() => {
                    item.action();
                    onClose();
                  }}
                  className={`w-full flex items-center justify-between gap-3 px-3 py-2.5 rounded-xl text-left transition-colors ${
                    selected
                      ? isDark
                        ? "bg-sky-600/20 text-sky-200"
                        : "bg-sky-50 text-sky-950"
                      : isDark
                      ? "hover:bg-slate-800/70"
                      : "hover:bg-slate-50"
                  }`}
                >
                  <div className="min-w-0 flex-1">
                    <div className="text-sm font-semibold truncate">
                      {item.title}
                    </div>
                    <div
                      className={`text-xs truncate ${
                        isDark ? "text-slate-400" : "text-slate-500"
                      }`}
                    >
                      {item.subtitle}
                    </div>
                  </div>
                  <span
                    className={`shrink-0 px-2 py-0.5 text-[10px] font-semibold rounded-full ${
                      isDark
                        ? "bg-slate-800 text-slate-300 border border-slate-700"
                        : "bg-slate-100 text-slate-600 border border-slate-200"
                    }`}
                  >
                    {item.type}
                  </span>
                </button>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}

function TooltipPopover({
  tooltipState,
  onMouseEnter,
  onMouseLeave,
  onClose,
  onGoToArticle,
  isDark,
}) {
  if (!tooltipState) return null;
  const term = MEDICAL_GLOSSARY[tooltipState.termId];
  if (!term) return null;

  const { rect, pinned } = tooltipState;
  const width = 320;
  const vw = typeof window !== "undefined" ? window.innerWidth : 1200;
  const vh = typeof window !== "undefined" ? window.innerHeight : 800;

  const left = Math.max(
    12,
    Math.min(vw - width - 12, rect.left + rect.width / 2 - width / 2)
  );
  const openAbove = rect.bottom + 230 > vh && rect.top > 230;
  const style = openAbove
    ? { left, bottom: vh - rect.top + 8, width }
    : { left, top: rect.bottom + 8, width };

  return (
    <div
      style={style}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onClick={(e) => e.stopPropagation()}
      className={`fixed z-50 rounded-xl border p-4 shadow-xl transition-opacity ${
        isDark
          ? "bg-slate-900 border-slate-700 text-slate-100 shadow-slate-950/80"
          : "bg-white border-slate-200 text-slate-800 shadow-slate-300/60"
      }`}
    >
      <div className="flex items-start justify-between gap-2 mb-1.5">
        <div>
          <span
            className={`inline-block px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded mb-1 ${
              isDark
                ? "bg-teal-500/20 text-teal-300"
                : "bg-teal-50 text-teal-700"
            }`}
          >
            {term.category}
          </span>
          <h4 className="text-sm font-bold leading-snug">{term.title}</h4>
        </div>
        {pinned && (
          <button
            type="button"
            onClick={onClose}
            className={`p-1 rounded-md ${
              isDark
                ? "hover:bg-slate-800 text-slate-400"
                : "hover:bg-slate-100 text-slate-400"
            }`}
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      <p
        className={`text-xs leading-relaxed mb-2.5 ${
          isDark ? "text-slate-300" : "text-slate-600"
        }`}
      >
        {term.definition}
      </p>

      {term.pearl && (
        <div
          className={`text-[11px] leading-snug p-2 rounded-lg mb-3 border-l-2 ${
            isDark
              ? "bg-amber-950/40 border-amber-500 text-amber-200"
              : "bg-[#FEFCE8] border-[#EAB308] text-amber-950"
          }`}
        >
          <span className="font-bold">Exam Pearl: </span>
          {term.pearl}
        </div>
      )}

      <div className="flex items-center justify-end">
        <button
          type="button"
          onClick={() => {
            onGoToArticle(term.articleId, term.sectionId);
            onClose();
          }}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#0284C7] hover:text-sky-500 transition-colors"
        >
          Go to article
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}

// ============================================================================
// 9. LEFT SIDEBAR (Outline & Nested Library Tree)
// ============================================================================

function LibraryTreeNode({
  node,
  depth = 0,
  expandedFolders,
  toggleFolder,
  activeArticleId,
  onSelectArticle,
  isDark,
}) {
  const hasChildren = !!node.children;
  const isExpanded = !!expandedFolders[node.id];
  const isActive = node.articleId === activeArticleId;

  if (hasChildren) {
    return (
      <div>
        <button
          type="button"
          onClick={() => toggleFolder(node.id)}
          style={{ paddingLeft: `${depth * 12 + 8}px` }}
          className={`w-full flex items-center gap-2 py-1.5 pr-2 rounded-lg text-xs font-semibold transition-colors ${
            isDark
              ? "text-slate-300 hover:bg-slate-800/80"
              : "text-slate-700 hover:bg-slate-100"
          }`}
        >
          <ChevronRight
            className={`w-3.5 h-3.5 shrink-0 transition-transform ${
              isExpanded ? "rotate-90" : ""
            } ${isDark ? "text-slate-500" : "text-slate-400"}`}
          />
          {isExpanded ? (
            <FolderOpen className="w-3.5 h-3.5 shrink-0 text-sky-500" />
          ) : (
            <Folder className="w-3.5 h-3.5 shrink-0 text-slate-400" />
          )}
          <span className="truncate">{node.label}</span>
        </button>

        {isExpanded && (
          <div className="mt-0.5 space-y-0.5">
            {node.children.map((child) => (
              <LibraryTreeNode
                key={child.id}
                node={child}
                depth={depth + 1}
                expandedFolders={expandedFolders}
                toggleFolder={toggleFolder}
                activeArticleId={activeArticleId}
                onSelectArticle={onSelectArticle}
                isDark={isDark}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <button
      type="button"
      onClick={() => onSelectArticle(node.articleId)}
      style={{ paddingLeft: `${depth * 12 + 12}px` }}
      className={`w-full flex items-center justify-between gap-2 py-1.5 pr-2.5 rounded-lg text-xs text-left transition-colors ${
        isActive
          ? isDark
            ? "bg-sky-600/20 text-sky-300 font-semibold border border-sky-500/30"
            : "bg-sky-50 text-[#0284C7] font-semibold border border-sky-200/80"
          : isDark
          ? "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
          : "text-slate-600 hover:text-slate-900 hover:bg-slate-100/80"
      }`}
    >
      <span className="flex items-center gap-2 min-w-0">
        <FileText className="w-3.5 h-3.5 shrink-0 opacity-75" />
        <span className="truncate">{node.label}</span>
      </span>
      {node.badge && (
        <span
          className={`shrink-0 text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ${
            isDark
              ? "bg-teal-500/20 text-teal-300"
              : "bg-teal-50 text-teal-700"
          }`}
        >
          HY
        </span>
      )}
    </button>
  );
}

// ============================================================================
// 10. MAIN APPLICATION COMPONENT
// ============================================================================

export default function App() {
  // Core Navigation & UI State
  const [activeArticleId, setActiveArticleId] = useState("acs");
  const [leftTab, setLeftTab] = useState("outline"); // "outline" | "library"
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [mobileLeftOpen, setMobileLeftOpen] = useState(false);
  const [mobileToolsOpen, setMobileToolsOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [qbankOpen, setQbankOpen] = useState(false);
  const [highlightedAnchor, setHighlightedAnchor] = useState(null);

  // Study Toolbar Toggles
  const [highYieldOnly, setHighYieldOnly] = useState(false);
  const [highlightsOn, setHighlightsOn] = useState(true);
  const [quizModeOn, setQuizModeOn] = useState(false);
  const [isDark, setIsDark] = useState(false);

  // Quiz Mode Blank Tracking
  const [revealedBlanks, setRevealedBlanks] = useState(() => new Set());

  // Bookmarks
  const [bookmarks, setBookmarks] = useState(() => new Set(["acs"]));

  // Nested Accordions Open State
  const [openSections, setOpenSections] = useState(() => {
    const init = {};
    ARTICLES.acs.sections.forEach((s) => {
      init[s.id] = true;
      if (s.subsections) {
        s.subsections.forEach((sub) => {
          init[sub.id] = true;
        });
      }
    });
    return init;
  });

  // Library Tree Expanded Folders
  const [expandedFolders, setExpandedFolders] = useState({
    im: true,
    cardio: true,
    pulm: true,
    endo: true,
  });

  // Active Calculator Tab
  const [calcTab, setCalcTab] = useState("heart");

  // My Notes Scratchpad (persisted safely per article)
  const [notesMap, setNotesMap] = useState(() => {
    const initial = {};
    Object.keys(ARTICLES).forEach((id) => {
      try {
        const saved = window.localStorage.getItem(`medbase_notes_${id}`);
        if (saved !== null) initial[id] = saved;
      } catch {
        // Ignore restricted storage
      }
    });
    return initial;
  });

  // Smart Tooltip Popover State
  const [tooltipState, setTooltipState] = useState(null);
  const closeTimerRef = useRef(null);

  const activeArticle = ARTICLES[activeArticleId];

  // Collect all section & subsection IDs for current article
  const allSectionIds = useMemo(() => {
    const ids = [];
    activeArticle.sections.forEach((s) => {
      ids.push(s.id);
      if (s.subsections) {
        s.subsections.forEach((sub) => ids.push(sub.id));
      }
    });
    return ids;
  }, [activeArticle]);

  const allExpanded = useMemo(
    () => allSectionIds.every((id) => !!openSections[id]),
    [allSectionIds, openSections]
  );

  // Compute visible blanks & hidden low-yield count
  const { visibleBlankIds, hiddenLowYieldCount } = useMemo(
    () => getArticleStats(activeArticle, highYieldOnly),
    [activeArticle, highYieldOnly]
  );

  const revealedVisibleCount = useMemo(
    () => visibleBlankIds.filter((id) => revealedBlanks.has(id)).length,
    [visibleBlankIds, revealedBlanks]
  );

  // Global Cmd+K / Ctrl+K Listener & Escape for Tooltips
  useEffect(() => {
    const onKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setSearchOpen((prev) => !prev);
      } else if (e.key === "Escape") {
        setTooltipState(null);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  // Close pinned tooltip on outside click
  useEffect(() => {
    const onClickOutside = () => setTooltipState(null);
    window.addEventListener("click", onClickOutside);
    return () => window.removeEventListener("click", onClickOutside);
  }, []);

  // Tooltip handlers
  const openTooltip = useCallback((termId, element) => {
    if (closeTimerRef.current) clearTimeout(closeTimerRef.current);
    const rect = element.getBoundingClientRect();
    setTooltipState((prev) => {
      if (prev?.pinned && prev.termId === termId) return prev;
      return { termId, rect, pinned: false };
    });
  }, []);

  const scheduleCloseTooltip = useCallback(() => {
    if (closeTimerRef.current) clearTimeout(closeTimerRef.current);
    closeTimerRef.current = setTimeout(() => {
      setTooltipState((prev) => (prev?.pinned ? prev : null));
    }, 180);
  }, []);

  const cancelCloseTooltip = useCallback(() => {
    if (closeTimerRef.current) clearTimeout(closeTimerRef.current);
  }, []);

  const pinTooltip = useCallback((termId, element) => {
    if (closeTimerRef.current) clearTimeout(closeTimerRef.current);
    const rect = element.getBoundingClientRect();
    setTooltipState((prev) => {
      if (prev?.pinned && prev.termId === termId) return null;
      return { termId, rect, pinned: true };
    });
  }, []);

  // Quiz Blank Toggle
  const toggleBlank = useCallback((blankId) => {
    setRevealedBlanks((prev) => {
      const next = new Set(prev);
      if (next.has(blankId)) next.delete(blankId);
      else next.add(blankId);
      return next;
    });
  }, []);

  // Toggle Section Accordion
  const toggleSection = useCallback((id) => {
    setOpenSections((prev) => ({ ...prev, [id]: !prev[id] }));
  }, []);

  // Expand / Collapse All
  const handleToggleExpandAll = () => {
    const targetState = !allExpanded;
    setOpenSections((prev) => {
      const next = { ...prev };
      allSectionIds.forEach((id) => {
        next[id] = targetState;
      });
      return next;
    });
  };

  // Switch Article & Optional Section Jump
  const handleSelectArticle = useCallback((articleId, targetSectionId = null) => {
    const targetArticle = ARTICLES[articleId];
    if (!targetArticle) return;

    setActiveArticleId(articleId);
    setCalcTab(targetArticle.calculatorDefault || "heart");
    setTooltipState(null);
    setMobileLeftOpen(false);

    // Ensure target article's sections are expanded
    setOpenSections((prev) => {
      const next = { ...prev };
      targetArticle.sections.forEach((s) => {
        next[s.id] = true;
        if (s.subsections) {
          s.subsections.forEach((sub) => {
            next[sub.id] = true;
          });
        }
      });
      return next;
    });

    setTimeout(() => {
      if (targetSectionId) {
        const el = document.getElementById(`section-${targetSectionId}`);
        if (el) {
          el.scrollIntoView({ behavior: "smooth", block: "start" });
          setHighlightedAnchor(targetSectionId);
          setTimeout(() => setHighlightedAnchor(null), 1600);
          return;
        }
      }
      window.scrollTo({ top: 0, behavior: "smooth" });
    }, 60);
  }, []);

  // Jump to Section in Current Article
  const handleJumpToSection = useCallback((targetId, parentId = null) => {
    setOpenSections((prev) => {
      const next = { ...prev, [targetId]: true };
      if (parentId) next[parentId] = true;
      return next;
    });
    setMobileLeftOpen(false);

    setTimeout(() => {
      const el = document.getElementById(`section-${targetId}`);
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        setHighlightedAnchor(targetId);
        setTimeout(() => setHighlightedAnchor(null), 1500);
      }
    }, 50);
  }, []);

  // Update Notes
  const handleNoteChange = (val) => {
    setNotesMap((prev) => ({ ...prev, [activeArticleId]: val }));
    try {
      window.localStorage.setItem(`medbase_notes_${activeArticleId}`, val);
    } catch {
      // Ignore storage errors
    }
  };

  // Toggle Bookmark
  const toggleBookmark = () => {
    setBookmarks((prev) => {
      const next = new Set(prev);
      if (next.has(activeArticleId)) next.delete(activeArticleId);
      else next.add(activeArticleId);
      return next;
    });
  };

  const studyCtxValue = useMemo(
    () => ({
      highlightsOn,
      quizModeOn,
      revealedBlanks,
      toggleBlank,
      isDark,
      openTooltip,
      scheduleCloseTooltip,
      pinTooltip,
    }),
    [
      highlightsOn,
      quizModeOn,
      revealedBlanks,
      toggleBlank,
      isDark,
      openTooltip,
      scheduleCloseTooltip,
      pinTooltip,
    ]
  );

  const isBookmarked = bookmarks.has(activeArticleId);
  const currentNote = notesMap[activeArticleId] || "";

  // Sidebar Content Shared by Desktop & Mobile Drawer
  const renderLeftSidebarContent = () => (
    <div className="flex flex-col h-full">
      <div
        className={`p-2 border-b grid grid-cols-2 gap-1 ${
          isDark ? "border-slate-800" : "border-slate-200"
        }`}
      >
        <button
          type="button"
          onClick={() => setLeftTab("outline")}
          className={`flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-semibold transition-colors ${
            leftTab === "outline"
              ? isDark
                ? "bg-slate-800 text-sky-400 shadow-xs"
                : "bg-sky-50 text-[#0284C7]"
              : isDark
              ? "text-slate-400 hover:text-slate-200"
              : "text-slate-500 hover:text-slate-800"
          }`}
        >
          <List className="w-3.5 h-3.5" />
          Article Outline
        </button>
        <button
          type="button"
          onClick={() => setLeftTab("library")}
          className={`flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-semibold transition-colors ${
            leftTab === "library"
              ? isDark
                ? "bg-slate-800 text-sky-400 shadow-xs"
                : "bg-sky-50 text-[#0284C7]"
              : isDark
              ? "text-slate-400 hover:text-slate-200"
              : "text-slate-500 hover:text-slate-800"
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" />
          Library
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        {leftTab === "outline" ? (
          <nav className="space-y-1">
            <button
              type="button"
              onClick={() => {
                window.scrollTo({ top: 0, behavior: "smooth" });
                setMobileLeftOpen(false);
              }}
              className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                isDark
                  ? "text-slate-300 hover:bg-slate-800"
                  : "text-slate-700 hover:bg-slate-100"
              }`}
            >
              Summary & Overview
            </button>

            {activeArticle.sections.map((sec) => (
              <div key={sec.id} className="space-y-0.5">
                <button
                  type="button"
                  onClick={() => handleJumpToSection(sec.id, null)}
                  className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors truncate ${
                    highlightedAnchor === sec.id
                      ? isDark
                        ? "bg-sky-500/20 text-sky-300"
                        : "bg-sky-50 text-[#0284C7]"
                      : isDark
                      ? "text-slate-300 hover:bg-slate-800/80"
                      : "text-slate-700 hover:bg-slate-100"
                  }`}
                >
                  {sec.title}
                </button>
                {sec.subsections && (
                  <div
                    className={`ml-3 pl-2.5 border-l space-y-0.5 ${
                      isDark ? "border-slate-800" : "border-slate-200"
                    }`}
                  >
                    {sec.subsections.map((sub) => (
                      <button
                        key={sub.id}
                        type="button"
                        onClick={() => handleJumpToSection(sub.id, sec.id)}
                        className={`w-full text-left px-2 py-1 rounded-md text-[11.5px] transition-colors truncate ${
                          highlightedAnchor === sub.id
                            ? isDark
                              ? "text-sky-300 bg-sky-500/15 font-medium"
                              : "text-[#0284C7] bg-sky-50 font-medium"
                            : isDark
                            ? "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                            : "text-slate-500 hover:text-slate-800 hover:bg-slate-100/70"
                        }`}
                      >
                        {sub.title}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </nav>
        ) : (
          <div className="space-y-1">
            {LIBRARY_TREE.map((node) => (
              <LibraryTreeNode
                key={node.id}
                node={node}
                expandedFolders={expandedFolders}
                toggleFolder={(id) =>
                  setExpandedFolders((prev) => ({ ...prev, [id]: !prev[id] }))
                }
                activeArticleId={activeArticleId}
                onSelectArticle={(artId) => handleSelectArticle(artId)}
                isDark={isDark}
              />
            ))}
          </div>
        )}
      </div>

      {/* Bookmarked Articles Footer */}
      <div
        className={`p-3 border-t text-xs ${
          isDark ? "border-slate-800 bg-slate-900/60" : "border-slate-200 bg-slate-50/70"
        }`}
      >
        <div
          className={`text-[10px] font-bold uppercase tracking-wider mb-1.5 ${
            isDark ? "text-slate-500" : "text-slate-400"
          }`}
        >
          Saved Bookmarks ({bookmarks.size})
        </div>
        {bookmarks.size === 0 ? (
          <p className={isDark ? "text-slate-500" : "text-slate-400"}>
            No bookmarked articles yet.
          </p>
        ) : (
          <div className="flex flex-wrap gap-1.5">
            {Array.from(bookmarks).map((bId) => (
              <button
                key={bId}
                type="button"
                onClick={() => handleSelectArticle(bId)}
                className={`px-2 py-0.5 rounded-md text-[11px] font-medium truncate max-w-full border transition-colors ${
                  bId === activeArticleId
                    ? isDark
                      ? "bg-sky-500/20 text-sky-300 border-sky-500/40"
                      : "bg-sky-50 text-[#0284C7] border-sky-200"
                    : isDark
                    ? "bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700"
                    : "bg-white text-slate-600 border-slate-200 hover:bg-slate-100"
                }`}
              >
                {ARTICLES[bId]?.title.split(" (")[0]}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  // Right Sidebar Contextual Cards
  const renderRightSidebarContent = () => (
    <div className="space-y-4">
      {/* 1. Related Qbank Card */}
      <div
        className={`rounded-xl border p-4 shadow-xs ${
          isDark ? "bg-slate-900 border-slate-800" : "bg-white border-slate-200"
        }`}
      >
        <div className="flex items-start justify-between gap-2 mb-2.5">
          <div className="flex items-center gap-2">
            <span
              className={`p-1.5 rounded-lg ${
                isDark ? "bg-teal-500/20 text-teal-300" : "bg-teal-50 text-[#0D9488]"
              }`}
            >
              <Stethoscope className="w-4 h-4" />
            </span>
            <div>
              <h3
                className={`text-sm font-bold tracking-tight ${
                  isDark ? "text-slate-100" : "text-slate-900"
                }`}
              >
                Related Qbank Questions ({activeArticle.qbankCount})
              </h3>
              <p
                className={`text-[11px] ${
                  isDark ? "text-slate-400" : "text-slate-500"
                }`}
              >
                {activeArticle.highYieldTag}
              </p>
            </div>
          </div>
        </div>

        <div
          className={`w-full h-1.5 rounded-full overflow-hidden mb-3 ${
            isDark ? "bg-slate-800" : "bg-slate-100"
          }`}
        >
          <div className="h-full bg-[#0D9488] w-[28%] rounded-full" />
        </div>

        <button
          type="button"
          onClick={() => setQbankOpen(true)}
          className="w-full py-2 px-3 rounded-lg text-xs font-semibold text-white bg-[#0D9488] hover:bg-teal-700 transition-colors flex items-center justify-center gap-1.5 shadow-xs"
        >
          <Sparkles className="w-3.5 h-3.5" />
          Start Practice Vignettes
        </button>
      </div>

      {/* 2. Clinical Calculators Card */}
      <div
        className={`rounded-xl border p-4 shadow-xs ${
          isDark ? "bg-slate-900 border-slate-800" : "bg-white border-slate-200"
        }`}
      >
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <span
              className={`p-1.5 rounded-lg ${
                isDark ? "bg-sky-500/20 text-sky-300" : "bg-sky-50 text-[#0284C7]"
              }`}
            >
              <Calculator className="w-4 h-4" />
            </span>
            <h3
              className={`text-sm font-bold tracking-tight ${
                isDark ? "text-slate-100" : "text-slate-900"
              }`}
            >
              Clinical Calculators
            </h3>
          </div>
        </div>

        <div
          className={`grid grid-cols-2 gap-1 p-1 rounded-lg mb-3 ${
            isDark ? "bg-slate-800" : "bg-slate-100"
          }`}
        >
          <button
            type="button"
            onClick={() => setCalcTab("heart")}
            className={`py-1 rounded-md text-[11px] font-semibold transition-colors ${
              calcTab === "heart"
                ? isDark
                  ? "bg-slate-700 text-white"
                  : "bg-white text-slate-900 shadow-xs"
                : isDark
                ? "text-slate-400"
                : "text-slate-500"
            }`}
          >
            HEART Score
          </button>
          <button
            type="button"
            onClick={() => setCalcTab("curb65")}
            className={`py-1 rounded-md text-[11px] font-semibold transition-colors ${
              calcTab === "curb65"
                ? isDark
                  ? "bg-slate-700 text-white"
                  : "bg-white text-slate-900 shadow-xs"
                : isDark
                ? "text-slate-400"
                : "text-slate-500"
            }`}
          >
            CURB-65
          </button>
        </div>

        {calcTab === "heart" ? (
          <HeartScoreCalculator isDark={isDark} />
        ) : (
          <Curb65Calculator isDark={isDark} />
        )}
      </div>

      {/* 3. My Notes Scratchpad */}
      <div
        className={`rounded-xl border p-4 shadow-xs ${
          isDark ? "bg-slate-900 border-slate-800" : "bg-white border-slate-200"
        }`}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <FileText
              className={`w-4 h-4 ${
                isDark ? "text-amber-400" : "text-amber-600"
              }`}
            />
            <h3
              className={`text-sm font-bold tracking-tight ${
                isDark ? "text-slate-100" : "text-slate-900"
              }`}
            >
              My Notes
            </h3>
          </div>
          {currentNote && (
            <button
              type="button"
              onClick={() => handleNoteChange("")}
              title="Clear notes"
              className={`p-1 rounded hover:bg-red-500/10 text-slate-400 hover:text-red-500 transition-colors`}
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        <textarea
          value={currentNote}
          onChange={(e) => handleNoteChange(e.target.value)}
          rows={5}
          placeholder={`Jot down high-yield mnemonics or weak points for ${
            activeArticle.title.split(" (")[0]
          }...`}
          className={`w-full rounded-lg border p-2.5 text-xs leading-relaxed outline-none resize-y transition-colors ${
            isDark
              ? "bg-slate-800/70 border-slate-700 text-slate-200 placeholder:text-slate-500 focus:border-sky-500"
              : "bg-slate-50 border-slate-200 text-slate-700 placeholder:text-slate-400 focus:border-[#0284C7] focus:bg-white"
          }`}
        />
        <div
          className={`mt-1.5 flex items-center justify-between text-[10.5px] ${
            isDark ? "text-slate-500" : "text-slate-400"
          }`}
        >
          <span>Auto-saved locally</span>
          <span>{currentNote.length} chars</span>
        </div>
      </div>
    </div>
  );

  return (
    <StudyContext.Provider value={studyCtxValue}>
      <div
        className={`min-h-screen flex flex-col font-sans antialiased transition-colors duration-200 ${
          isDark
            ? "bg-slate-950 text-slate-200"
            : "bg-[#F8FAFC] text-[#1E293B]"
        }`}
      >
        {/* ================================================================ */}
        {/* TOP STICKY NAVIGATION BAR                                        */}
        {/* ================================================================ */}
        <header
          className={`sticky top-0 z-30 border-b backdrop-blur-md transition-colors ${
            isDark
              ? "bg-slate-900/95 border-slate-800"
              : "bg-white/95 border-slate-200"
          }`}
        >
          <div className="max-w-[1600px] mx-auto px-3 sm:px-5 h-14 flex items-center justify-between gap-3">
            {/* Left: Sidebar Toggle + Logo */}
            <div className="flex items-center gap-2.5 shrink-0">
              <button
                type="button"
                aria-label="Toggle navigation sidebar"
                onClick={() => {
                  if (window.innerWidth < 1024) {
                    setMobileLeftOpen((v) => !v);
                  } else {
                    setLeftSidebarOpen((v) => !v);
                  }
                }}
                className={`p-2 rounded-lg border transition-colors ${
                  isDark
                    ? "border-slate-700 hover:bg-slate-800 text-slate-300"
                    : "border-slate-200 hover:bg-slate-100 text-slate-600"
                }`}
              >
                <PanelLeft className="w-4 h-4" />
              </button>

              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#0284C7] to-[#0D9488] flex items-center justify-center text-white shadow-xs">
                  <Activity className="w-4.5 h-4.5" />
                </div>
                <div className="leading-tight">
                  <span
                    className={`font-extrabold tracking-tight text-base ${
                      isDark ? "text-white" : "text-slate-900"
                    }`}
                  >
                    MedBase
                  </span>
                  <span
                    className={`hidden sm:block text-[10px] font-semibold uppercase tracking-widest ${
                      isDark ? "text-teal-400" : "text-[#0D9488]"
                    }`}
                  >
                    Clinical Library
                  </span>
                </div>
              </div>
            </div>

            {/* Center: Global Command Search */}
            <button
              type="button"
              onClick={() => setSearchOpen(true)}
              className={`flex-1 max-w-md flex items-center justify-between gap-2 px-3 py-1.5 rounded-xl border text-xs sm:text-sm transition-colors ${
                isDark
                  ? "bg-slate-800/80 border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-200"
                  : "bg-slate-100/80 border-slate-200 text-slate-500 hover:border-slate-300 hover:bg-slate-100"
              }`}
            >
              <span className="flex items-center gap-2 truncate">
                <Search className="w-3.5 h-3.5 shrink-0" />
                <span className="truncate">
                  Search conditions, ECG signs, drugs...
                </span>
              </span>
              <kbd
                className={`hidden sm:inline-flex items-center px-1.5 py-0.5 text-[10px] font-bold rounded border ${
                  isDark
                    ? "bg-slate-900 border-slate-700 text-slate-400"
                    : "bg-white border-slate-300 text-slate-500"
                }`}
              >
                ⌘K
              </kbd>
            </button>

            {/* Right: Study Toolbar */}
            <div className="flex items-center gap-1.5 shrink-0">
              {/* Desktop Study Mode Toggles */}
              <div className="hidden md:flex items-center gap-1.5">
                <button
                  type="button"
                  onClick={() => setHighYieldOnly((v) => !v)}
                  title="Show only High-Yield exam facts"
                  className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                    highYieldOnly
                      ? "bg-[#0D9488] text-white border-[#0D9488] shadow-xs"
                      : isDark
                      ? "bg-slate-800/70 text-slate-300 border-slate-700 hover:bg-slate-800"
                      : "bg-white text-slate-600 border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  <Zap className="w-3.5 h-3.5" />
                  <span>High-Yield</span>
                </button>

                <button
                  type="button"
                  onClick={() => setHighlightsOn((v) => !v)}
                  title="Toggle yellow Key Exam Highlights"
                  className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                    highlightsOn
                      ? isDark
                        ? "bg-amber-500/20 text-amber-300 border-amber-500/50"
                        : "bg-yellow-100 text-amber-900 border-yellow-300"
                      : isDark
                      ? "bg-slate-800/70 text-slate-300 border-slate-700 hover:bg-slate-800"
                      : "bg-white text-slate-600 border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  <Highlighter className="w-3.5 h-3.5" />
                  <span>Highlights</span>
                </button>

                <button
                  type="button"
                  onClick={() => setQuizModeOn((v) => !v)}
                  title="Blur key terms for active recall"
                  className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                    quizModeOn
                      ? "bg-[#0284C7] text-white border-[#0284C7] shadow-xs"
                      : isDark
                      ? "bg-slate-800/70 text-slate-300 border-slate-700 hover:bg-slate-800"
                      : "bg-white text-slate-600 border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  {quizModeOn ? (
                    <EyeOff className="w-3.5 h-3.5" />
                  ) : (
                    <Eye className="w-3.5 h-3.5" />
                  )}
                  <span>Quiz Mode</span>
                </button>
              </div>

              {/* Mobile Study Tools Drawer Button */}
              <button
                type="button"
                onClick={() => setMobileToolsOpen(true)}
                className={`xl:hidden flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold border transition-colors ${
                  isDark
                    ? "border-slate-700 bg-slate-800 text-slate-200"
                    : "border-slate-200 bg-white text-slate-700"
                }`}
              >
                <Calculator className="w-3.5 h-3.5 text-[#0284C7]" />
                <span className="hidden sm:inline">Tools</span>
              </button>

              {/* Dark Mode Toggle */}
              <button
                type="button"
                aria-label="Toggle dark mode"
                onClick={() => setIsDark((d) => !d)}
                className={`p-2 rounded-lg border transition-colors ${
                  isDark
                    ? "border-slate-700 bg-slate-800 text-amber-300 hover:bg-slate-700"
                    : "border-slate-200 bg-white text-slate-600 hover:bg-slate-100"
                }`}
              >
                {isDark ? (
                  <Sun className="w-4 h-4" />
                ) : (
                  <Moon className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile Compact Study Toolbar */}
          <div
            className={`md:hidden px-3 py-2 border-t flex items-center justify-between gap-1.5 overflow-x-auto ${
              isDark ? "border-slate-800 bg-slate-900" : "border-slate-100 bg-slate-50/90"
            }`}
          >
            <button
              type="button"
              onClick={() => setHighYieldOnly((v) => !v)}
              className={`flex-1 flex items-center justify-center gap-1 px-2 py-1 rounded-md text-[11px] font-semibold border ${
                highYieldOnly
                  ? "bg-[#0D9488] text-white border-[#0D9488]"
                  : isDark
                  ? "bg-slate-800 text-slate-300 border-slate-700"
                  : "bg-white text-slate-600 border-slate-200"
              }`}
            >
              <Zap className="w-3 h-3" />
              High-Yield
            </button>
            <button
              type="button"
              onClick={() => setHighlightsOn((v) => !v)}
              className={`flex-1 flex items-center justify-center gap-1 px-2 py-1 rounded-md text-[11px] font-semibold border ${
                highlightsOn
                  ? isDark
                    ? "bg-amber-500/20 text-amber-300 border-amber-500/40"
                    : "bg-yellow-100 text-amber-900 border-yellow-300"
                  : isDark
                  ? "bg-slate-800 text-slate-300 border-slate-700"
                  : "bg-white text-slate-600 border-slate-200"
              }`}
            >
              <Highlighter className="w-3 h-3" />
              Highlights
            </button>
            <button
              type="button"
              onClick={() => setQuizModeOn((v) => !v)}
              className={`flex-1 flex items-center justify-center gap-1 px-2 py-1 rounded-md text-[11px] font-semibold border ${
                quizModeOn
                  ? "bg-[#0284C7] text-white border-[#0284C7]"
                  : isDark
                  ? "bg-slate-800 text-slate-300 border-slate-700"
                  : "bg-white text-slate-600 border-slate-200"
              }`}
            >
              <EyeOff className="w-3 h-3" />
              Quiz Mode
            </button>
          </div>
        </header>

        {/* ================================================================ */}
        {/* 3-COLUMN WORKSPACE                                               */}
        {/* ================================================================ */}
        <div className="flex-1 max-w-[1600px] w-full mx-auto flex items-start gap-6 px-3 sm:px-5 py-5">
          {/* LEFT SIDEBAR (Desktop) */}
          {leftSidebarOpen && (
            <aside
              className={`hidden lg:flex flex-col w-72 shrink-0 sticky top-[76px] h-[calc(100vh-96px)] rounded-xl border overflow-hidden shadow-xs ${
                isDark
                  ? "bg-slate-900 border-slate-800"
                  : "bg-white border-slate-200"
              }`}
            >
              {renderLeftSidebarContent()}
            </aside>
          )}

          {/* CENTER MAIN CONTENT AREA (THE ARTICLE CARD) */}
          <main className="flex-1 min-w-0">
            <article
              className={`rounded-2xl border shadow-xs p-5 sm:p-8 ${
                isDark
                  ? "bg-slate-900 border-slate-800"
                  : "bg-white border-slate-200/90"
              }`}
            >
              {/* Breadcrumbs */}
              <nav
                aria-label="Breadcrumb"
                className={`flex flex-wrap items-center gap-1.5 text-xs font-medium mb-3 ${
                  isDark ? "text-slate-400" : "text-slate-500"
                }`}
              >
                {activeArticle.breadcrumbs.map((crumb, idx) => (
                  <React.Fragment key={crumb}>
                    {idx > 0 && <ChevronRight className="w-3.5 h-3.5 opacity-60" />}
                    <span
                      className={
                        idx === activeArticle.breadcrumbs.length - 1
                          ? isDark
                            ? "text-sky-400"
                            : "text-[#0284C7]"
                          : ""
                      }
                    >
                      {crumb}
                    </span>
                  </React.Fragment>
                ))}
              </nav>

              {/* Title & Actions Header */}
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-slate-200 dark:border-slate-800">
                <div>
                  <h1
                    className={`text-2xl sm:text-3xl font-extrabold tracking-tight mb-2.5 ${
                      isDark ? "text-white" : "text-slate-900"
                    }`}
                  >
                    {activeArticle.title}
                  </h1>
                  <div className="flex flex-wrap items-center gap-2 text-xs">
                    <span
                      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-medium border ${
                        isDark
                          ? "bg-slate-800 border-slate-700 text-slate-300"
                          : "bg-slate-100 border-slate-200 text-slate-600"
                      }`}
                    >
                      <Clock className="w-3 h-3" />
                      Updated {activeArticle.lastUpdated}
                    </span>
                    <span
                      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-semibold ${
                        isDark
                          ? "bg-teal-500/15 text-teal-300 border border-teal-500/30"
                          : "bg-teal-50 text-[#0D9488] border border-teal-200"
                      }`}
                    >
                      {activeArticle.highYieldTag}
                    </span>
                    <span
                      className={isDark ? "text-slate-400" : "text-slate-500"}
                    >
                      • {activeArticle.readTime}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={toggleBookmark}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors ${
                      isBookmarked
                        ? isDark
                          ? "bg-amber-500/15 border-amber-500/40 text-amber-300"
                          : "bg-amber-50 border-amber-300 text-amber-800"
                        : isDark
                        ? "bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700"
                        : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
                    }`}
                  >
                    <Bookmark
                      className={`w-3.5 h-3.5 ${
                        isBookmarked ? "fill-current" : ""
                      }`}
                    />
                    {isBookmarked ? "Saved" : "Bookmark"}
                  </button>

                  <button
                    type="button"
                    onClick={handleToggleExpandAll}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors ${
                      isDark
                        ? "bg-slate-800 border-slate-700 text-slate-200 hover:bg-slate-700"
                        : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                    }`}
                  >
                    {allExpanded ? (
                      <>
                        <ChevronsDownUp className="w-3.5 h-3.5" />
                        Collapse All
                      </>
                    ) : (
                      <>
                        <ChevronsUpDown className="w-3.5 h-3.5" />
                        Expand All
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Active Study Mode Status Banners */}
              {(highYieldOnly || quizModeOn) && (
                <div className="mt-4 flex flex-wrap items-center gap-2.5">
                  {highYieldOnly && (
                    <div
                      className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium border ${
                        isDark
                          ? "bg-teal-950/50 border-teal-800 text-teal-200"
                          : "bg-teal-50 border-teal-200 text-teal-900"
                      }`}
                    >
                      <Zap className="w-3.5 h-3.5 text-[#0D9488]" />
                      <span>
                        <strong>High-Yield Filter Active:</strong>{" "}
                        {hiddenLowYieldCount} supporting detail block
                        {hiddenLowYieldCount === 1 ? "" : "s"} hidden
                      </span>
                    </div>
                  )}

                  {quizModeOn && (
                    <div
                      className={`inline-flex flex-wrap items-center gap-2.5 px-3 py-1.5 rounded-lg text-xs font-medium border ${
                        isDark
                          ? "bg-sky-950/50 border-sky-800 text-sky-200"
                          : "bg-sky-50 border-sky-200 text-sky-900"
                      }`}
                    >
                      <EyeOff className="w-3.5 h-3.5 text-[#0284C7]" />
                      <span>
                        <strong>Quiz Mode:</strong> Click blurred terms to
                        reveal ({revealedVisibleCount} /{" "}
                        {visibleBlankIds.length})
                      </span>
                      <button
                        type="button"
                        onClick={() =>
                          setRevealedBlanks(new Set(visibleBlankIds))
                        }
                        className="inline-flex items-center gap-1 underline font-semibold hover:opacity-80"
                      >
                        <Check className="w-3 h-3" />
                        Reveal All
                      </button>
                      <button
                        type="button"
                        onClick={() => setRevealedBlanks(new Set())}
                        className="inline-flex items-center gap-1 underline font-semibold hover:opacity-80"
                      >
                        <RotateCcw className="w-3 h-3" />
                        Reset
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* Article Summary Lead */}
              <div
                className={`mt-5 p-4 rounded-xl border text-[15px] leading-[1.65] ${
                  isDark
                    ? "bg-slate-800/40 border-slate-800 text-slate-200"
                    : "bg-[#F8FAFC] border-slate-200/80 text-slate-700"
                }`}
              >
                <RichText
                  text={activeArticle.summary}
                  pathPrefix={`${activeArticle.id}-summary`}
                />
              </div>

              {/* Nested Collapsible Article Sections */}
              <div className="mt-6 space-y-4">
                {activeArticle.sections.map((section) => (
                  <AccordionSection
                    key={section.id}
                    section={section}
                    openSections={openSections}
                    onToggleSection={toggleSection}
                    highYieldOnly={highYieldOnly}
                    isDark={isDark}
                    highlightedAnchor={highlightedAnchor}
                  />
                ))}
              </div>
            </article>
          </main>

          {/* RIGHT CONTEXTUAL SIDEBAR (Desktop) */}
          <aside className="hidden xl:block w-80 shrink-0 sticky top-[76px]">
            {renderRightSidebarContent()}
          </aside>
        </div>

        {/* ================================================================ */}
        {/* MOBILE DRAWERS (LEFT NAV & RIGHT STUDY TOOLS)                    */}
        {/* ================================================================ */}
        {mobileLeftOpen && (
          <div
            className="fixed inset-0 z-40 lg:hidden bg-slate-950/60 backdrop-blur-xs flex"
            onClick={() => setMobileLeftOpen(false)}
          >
            <div
              onClick={(e) => e.stopPropagation()}
              className={`w-72 max-w-[85vw] h-full border-r shadow-2xl flex flex-col ${
                isDark
                  ? "bg-slate-900 border-slate-800"
                  : "bg-white border-slate-200"
              }`}
            >
              <div
                className={`px-4 py-3 border-b flex items-center justify-between ${
                  isDark ? "border-slate-800" : "border-slate-200"
                }`}
              >
                <span className="text-sm font-bold">Navigation</span>
                <button
                  type="button"
                  onClick={() => setMobileLeftOpen(false)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              <div className="flex-1 overflow-hidden">
                {renderLeftSidebarContent()}
              </div>
            </div>
          </div>
        )}

        {mobileToolsOpen && (
          <div
            className="fixed inset-0 z-40 xl:hidden bg-slate-950/60 backdrop-blur-xs flex justify-end"
            onClick={() => setMobileToolsOpen(false)}
          >
            <div
              onClick={(e) => e.stopPropagation()}
              className={`w-80 max-w-[90vw] h-full border-l shadow-2xl flex flex-col ${
                isDark
                  ? "bg-slate-950 border-slate-800"
                  : "bg-[#F8FAFC] border-slate-200"
              }`}
            >
              <div
                className={`px-4 py-3 border-b flex items-center justify-between ${
                  isDark
                    ? "border-slate-800 bg-slate-900"
                    : "border-slate-200 bg-white"
                }`}
              >
                <span className="text-sm font-bold">Clinical Study Tools</span>
                <button
                  type="button"
                  onClick={() => setMobileToolsOpen(false)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-4">
                {renderRightSidebarContent()}
              </div>
            </div>
          </div>
        )}

        {/* ================================================================ */}
        {/* SMART TOOLTIP POPOVER & INTERACTIVE MODALS                       */}
        {/* ================================================================ */}
        <TooltipPopover
          tooltipState={tooltipState}
          onMouseEnter={cancelCloseTooltip}
          onMouseLeave={scheduleCloseTooltip}
          onClose={() => setTooltipState(null)}
          onGoToArticle={(artId, secId) => handleSelectArticle(artId, secId)}
          isDark={isDark}
        />

        <CommandSearchModal
          isOpen={searchOpen}
          onClose={() => setSearchOpen(false)}
          activeArticle={activeArticle}
          onSelectArticle={handleSelectArticle}
          onJumpToSection={handleJumpToSection}
          isDark={isDark}
        />

        {qbankOpen && (
          <QbankModal
            article={activeArticle}
            onClose={() => setQbankOpen(false)}
            isDark={isDark}
          />
        )}
      </div>
    </StudyContext.Provider>
  );
}
