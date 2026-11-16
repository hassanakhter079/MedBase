import json

with open('/root/medbase/medbase_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ==============================================================================
# REFERENCES DEFINITIONS
# ==============================================================================

ACS_REFERENCES = [
    {
        "id": "ref-amboss-acs",
        "sourceType": "AMBOSS Knowledge",
        "title": "AMBOSS Clinical Knowledge: Acute Coronary Syndrome",
        "url": "https://www.amboss.com/us/knowledge/acute-coronary-syndrome",
        "citation": "AMBOSS Editorial Board. Acute Coronary Syndrome (ACS). AMBOSS Knowledge Platform, 2024.",
        "evidenceLevel": "Guideline Consensus & Systematic Review",
        "sourcedContent": [
            "12-Lead ECG STEMI elevation criteria: ≥1 mm in all leads, except V2–V3 (≥1.5 mm women, ≥2.0 mm men ≥40, ≥2.5 mm men <40).",
            "Reciprocal leads localization matrix: Anterior (LAD: V1–V4), Lateral (LCx: I, aVL, V5–V6), Inferior (RCA: II, III, aVF).",
            "Modified Sgarbossa criteria for diagnosing acute MI in the presence of LBBB or paced ventricular rhythm.",
            "High-risk equivalents: Wellens syndrome (critical proximal LAD stenosis) and De Winter T-wave patterns.",
            "Absolute and relative contraindications checklist for fibrinolytic therapy."
        ]
    },
    {
        "id": "ref-osmosis-acs",
        "sourceType": "Osmosis Clinical",
        "title": "Osmosis by Elsevier: Acute Coronary Syndrome (Pathology & Management)",
        "url": "https://www.osmosis.org/learn/Acute_coronary_syndrome",
        "citation": "Osmosis by Elsevier. Acute Coronary Syndrome: Clinical Review and Illustrated Pathology, 2024.",
        "evidenceLevel": "Illustrated Clinical & Pathophysiological Review",
        "sourcedContent": [
            "Pathophysiological mechanism: Atherosclerotic fibrous cap rupture vs superficial plaque erosion.",
            "Distinction between subendocardial ischemia (NSTEMI / UA) and transmural transmural necrosis (STEMI).",
            "Histological MI timeline: Coagulative necrosis (4–24h), peak neutrophilic infiltration (1–3d), macrophage clearance (3–7d), granulation (1–3w), collagen scar (>2w).",
            "Anatomical basis of papillary muscle rupture: Posteromedial papillary muscle has single blood supply from PDA (RCA), predisposing to acute severe MR."
        ]
    },
    {
        "id": "ref-fa-acs",
        "sourceType": "First Aid USMLE Step 2 CK",
        "title": "First Aid for the USMLE Step 2 CK: Cardiovascular — Ischemic Heart Disease",
        "url": "https://www.usmle.org/",
        "citation": "Tao Le, Vikas Bhushan, et al. First Aid for the USMLE Step 2 CK (11th & 12th Eds). McGraw-Hill Medical.",
        "evidenceLevel": "USMLE Core Curriculum Synthesis",
        "sourcedContent": [
            "Right Ventricular Infarction high-yield rule: Inferior MI (II, III, aVF) with ST-elevation in V4R -> extreme preload dependence -> strictly avoid nitrates, opioids, and diuretics; treat with IV fluid boluses.",
            "Post-MI mechanical complications timeline: Days 3–5 (papillary muscle rupture with acute severe MR, interventricular septal rupture with oxygen step-up), Days 5–14 (LV free wall rupture with tamponade), Weeks 2–10 (Dressler autoimmune pericarditis).",
            "Discharge secondary prevention 'BASH' mnemonic: Beta-blocker, ACEi/ARB, Statin (high-intensity), and dual Antiplatelet therapy."
        ]
    },
    {
        "id": "ref-esc-acs",
        "sourceType": "2023 ESC Guidelines",
        "title": "2023 ESC Guidelines for the Management of Acute Coronary Syndromes",
        "url": "https://academic.oup.com/eurheartj/article/44/38/3720/7243217",
        "citation": "Byrne RA, et al. 2023 ESC Guidelines for the management of acute coronary syndromes. Eur Heart J. 2023;44(38):3720-3826. DOI: 10.1093/eurheartj/ehad191.",
        "evidenceLevel": "Class 1A International Guideline",
        "sourcedContent": [
            "Oxygen therapy restriction: Indicated ONLY if SaO2 < 90% or PaO2 < 60 mmHg (Class I); routine O2 in normoxemic patients causes hyperoxic coronary vasoconstriction and increases infarct size (Class III: Harm).",
            "Rapid 0h/1h and 0h/2h hs-cTn rule-in/rule-out diagnostic algorithms.",
            "Radial artery access preferred over femoral access for primary PCI (Class IA) to reduce major bleeding and 30-day mortality.",
            "DAPT duration: 12 months standard, with individualized shortening (1–3 months) for high bleeding risk (HBR) patients."
        ]
    },
    {
        "id": "ref-acc-aha-acs",
        "sourceType": "2021 ACC/AHA Guidelines",
        "title": "2021 ACC/AHA/SCAI Guideline for Coronary Artery Revascularization & NSTE-ACS Standards",
        "url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001038",
        "citation": "Lawton JS, et al. 2021 ACC/AHA/SCAI Guideline for Coronary Artery Revascularization. Circulation. 2022;145(3):e18-e114.",
        "evidenceLevel": "Class 1A Societal Practice Guideline",
        "sourcedContent": [
            "Reperfusion benchmarks: Door-to-balloon time ≤ 90 minutes for Primary PCI; Door-to-needle time ≤ 30 minutes for fibrinolysis when PCI transfer delay exceeds 120 minutes.",
            "Early invasive strategy (< 24h) criteria in NSTE-ACS: GRACE risk score > 140, dynamic ST changes, or elevated troponin.",
            "Immediate invasive strategy (< 2h) for refractory chest pain, hemodynamic instability, acute heart failure, or life-threatening ventricular arrhythmias."
        ]
    },
    {
        "id": "ref-dod-acs",
        "sourceType": "Doctor on Duty 3rd Ed",
        "title": "Doctor on Duty (3rd Edition - Acute Emergency Protocols) & House Job Ward Regimens",
        "url": "https://github.com/hassanakhter079/doctor-on-duty",
        "citation": "Doctor on Duty: A Comprehensive Emergency and Ward Practice Manual (3rd Ed), adapted with Pakistani commercial brand guidelines.",
        "evidenceLevel": "Bedside Emergency & Clinical Ward Protocol",
        "sourcedContent": [
            "Emergency ward admission loading regimen: Cap. Ascard (Aspirin 300 mg chewable stat), Tab. Loplat / Plavix (Clopidogrel 300–600 mg stat), Tab. Atorva / Lipiget (Atorvastatin 80 mg stat).",
            "Anticoagulation: Inj. Clexane (Enoxaparin 1 mg/kg SC BD or 30 mg IV bolus in STEMI).",
            "Nitrate dosing: Tab. Angised (Nitroglycerin 0.5 mg sublingual PRN, BP permitting, strictly contraindicated in RV infarction).",
            "Pakistani hospital thrombolysis protocol: Inj. Streptokinase (SK) 1.5 million IU in 100 mL Normal Saline IV over 60 minutes with pre-medication Inj. Hydrocortisone 100 mg IV."
        ]
    },
    {
        "id": "ref-statpearls-acs",
        "sourceType": "StatPearls & NCBI Bookshelf",
        "title": "StatPearls (NCBI/NIH): Acute Coronary Syndrome & Myocardial Infarction",
        "url": "https://www.ncbi.nlm.nih.gov/books/NBK459157/",
        "citation": "Singh A, Museedi AS, Grossman SA. Acute Coronary Syndrome. StatPearls Publishing; 2024.",
        "evidenceLevel": "Peer-Reviewed Systematic Compendium",
        "sourcedContent": [
            "Differential diagnosis of cardiac troponin elevation without ACS (acute pulmonary embolism, myocarditis, renal failure, sepsis).",
            "TIMI and GRACE risk score calculators and validated mortality odds ratios."
        ]
    },
    {
        "id": "ref-litfl-acs",
        "sourceType": "LITFL ECG Compendium",
        "title": "Life in the Fast Lane (LITFL): STEMI & High-Risk ECG Patterns",
        "url": "https://litfl.com/st-elevation-myocardial-infarction-stemi/",
        "citation": "Burns E, Buttner R. ST Elevation Myocardial Infarction. Life in the Fast Lane (LITFL), 2023.",
        "evidenceLevel": "Emergency Electrocardiography Standard",
        "sourcedContent": [
            "Diagnostic criteria for subtle STEMI presentations: Posterior STEMI (tall R waves and ST depression in V1–V3 with ST-elevation in V7–V9).",
            "De Winter T-wave patterns: 1–3 mm ST depression at J-point with upsloping tall, symmetrical T-waves in precordial leads.",
            "Wellens Syndrome Type A (biphasic T-waves) and Type B (deep symmetrical inverted T-waves in V2–V3)."
        ]
    }
]

CAP_REFERENCES = [
    {
        "id": "ref-amboss-cap",
        "sourceType": "AMBOSS Knowledge",
        "title": "AMBOSS Clinical Knowledge: Community-Acquired Pneumonia",
        "url": "https://www.amboss.com/us/knowledge/community-acquired-pneumonia",
        "citation": "AMBOSS Editorial Board. Community-Acquired Pneumonia (CAP). AMBOSS Knowledge Platform, 2024.",
        "evidenceLevel": "Guideline Consensus & Systematic Review",
        "sourcedContent": [
            "Diagnostic confirmation criteria: Acute cough, fever, dyspnea, or pleuritic chest pain with demonstrable new focal consolidation on chest imaging.",
            "Microbiological epidemiology: Streptococcus pneumoniae (most common typical pathogen), Mycoplasma pneumoniae, Chlamydia pneumoniae, and Legionella pneumophila.",
            "Procalcitonin utilization guidelines: Recommended to guide antibiotic de-escalation/discontinuation, NOT to withhold initial empiric antibiotic therapy in suspected pneumonia.",
            "Indications for blood cultures, sputum Gram stain, and urine antigen testing (reserved for severe CAP or risk factors for MRSA/Pseudomonas)."
        ]
    },
    {
        "id": "ref-osmosis-cap",
        "sourceType": "Osmosis Clinical",
        "title": "Osmosis by Elsevier: Pneumonia (Pathophysiology & Physical Diagnosis)",
        "url": "https://www.osmosis.org/learn/Pneumonia",
        "citation": "Osmosis by Elsevier. Pneumonia: Clinical Features, Pathology, and Auscultation Findings, 2024.",
        "evidenceLevel": "Illustrated Clinical & Pathophysiological Review",
        "sourcedContent": [
            "Physical examination consolidation signs: Bronchial breath sounds, dullness to percussion, increased tactile vocal fremitus, crackles/rales, and egophony ('E' to 'A' transition).",
            "Pathological stages of lobar pneumonia: Congestion (days 1–2), Red hepatization (days 3–4), Gray hepatization (days 5–7), and Resolution (day 8+).",
            "Atypical pneumonia extrapulmonary manifestations: Erythema multiforme and cold agglutinin hemolytic anemia with Mycoplasma; hyponatremia and neurologic symptoms with Legionella."
        ]
    },
    {
        "id": "ref-fa-cap",
        "sourceType": "First Aid USMLE Step 2 CK",
        "title": "First Aid for the USMLE Step 2 CK: Respiratory — Pulmonary Infections",
        "url": "https://www.usmle.org/",
        "citation": "Tao Le, Vikas Bhushan, et al. First Aid for the USMLE Step 2 CK (11th & 12th Eds). McGraw-Hill Medical.",
        "evidenceLevel": "USMLE Core Curriculum Synthesis",
        "sourcedContent": [
            "CURB-65 calculation mnemonic and risk-stratified triage:",
            "  * Confusion (AMTS ≤ 8 or disorientation)",
            "  * Urea > 7 mmol/L (BUN > 19 mg/dL)",
            "  * Respiratory rate ≥ 30 breaths/min",
            "  * Blood pressure (Systolic < 90 mmHg or Diastolic ≤ 60 mmHg)",
            "  * 65: Age ≥ 65 years",
            "Triage cutoffs: 0–1 points (low risk, outpatient); 2 points (moderate risk, inpatient ward); ≥ 3 points (high risk, inpatient admission, evaluate for ICU).",
            "Pathogen buzzwords: Alcoholics with currant-jelly sputum -> Klebsiella pneumoniae; Post-viral influenza -> Staphylococcus aureus necrotizing pneumonia; Cystic fibrosis -> Pseudomonas aeruginosa."
        ]
    },
    {
        "id": "ref-ats-idsa-cap",
        "sourceType": "ATS/IDSA 2019 Guidelines",
        "title": "ATS/IDSA 2019 Guideline: Diagnosis and Treatment of Adults with Community-Acquired Pneumonia",
        "url": "https://www.atsjournals.org/doi/10.1164/rccm.201908-1581ST",
        "citation": "Metlay JP, et al. Diagnosis and Treatment of Adults with Community-acquired Pneumonia. Am J Respir Crit Care Med. 2019;200(8):e45-e67. DOI: 10.1164/rccm.201908-1581ST.",
        "evidenceLevel": "Class 1A International Guideline",
        "sourcedContent": [
            "Outpatient empiric regimen: Amoxicillin 1g TID OR Doxycycline 100mg BID for healthy adults; Beta-lactam (Amox-Clav or Cefuroxime) + Macrolide (Azithromycin) OR Respiratory Fluoroquinolone monotherapy (Levofloxacin 750mg / Moxifloxacin 400mg) for patients with comorbidities.",
            "Inpatient non-severe empiric regimen: Beta-lactam (Ampicillin-sulbactam 1.5–3g IV q6h or Ceftriaxone 1–2g IV OD) + Macrolide (Azithromycin 500mg IV/PO OD) OR Respiratory Fluoroquinolone.",
            "Guideline recommendation against routine empiric coverage for MRSA or Pseudomonas unless validated prior isolation or recent hospitalization with IV antibiotics within 90 days.",
            "Duration of antimicrobial therapy: Minimum 5 days, continuing until the patient is afebrile for 48–72 hours and clinically stable."
        ]
    },
    {
        "id": "ref-dod-cap",
        "sourceType": "Doctor on Duty 3rd Ed",
        "title": "Doctor on Duty (3rd Edition - Respiratory Infections & Ward Antibiotic Protocols)",
        "url": "https://github.com/hassanakhter079/doctor-on-duty",
        "citation": "Doctor on Duty: A Comprehensive Emergency and Ward Practice Manual (3rd Ed), adapted with Pakistani commercial brand guidelines.",
        "evidenceLevel": "Bedside Emergency & Clinical Ward Protocol",
        "sourcedContent": [
            "Pakistani commercial brand formulations and hospital dosing:",
            "  * Inj. Augmentin (Co-amoxiclav 1.2 g IV TDS) or Tab. Augmentin (1 g BD)",
            "  * Tab. Azomax / Zithro (Azithromycin 500 mg OD)",
            "  * Tab. / Inj. Leflox (Levofloxacin 750 mg or 500 mg OD)",
            "  * Inj. Rocephin / Epicephin (Ceftriaxone 1 g - 2 g IV OD)",
            "  * Tab. Klaricid (Clarithromycin 500 mg BD)",
            "  * Syp. / Tab. Panadol (Paracetamol 1 g TDS PRN) for fever, steam inhalation, and supplemental O2 via Venturi mask."
        ]
    },
    {
        "id": "ref-statpearls-cap",
        "sourceType": "StatPearls & NCBI Bookshelf",
        "title": "StatPearls (NCBI/NIH): Community-Acquired Pneumonia",
        "url": "https://www.ncbi.nlm.nih.gov/books/NBK430749/",
        "citation": "Rider AC, Modi P. Community-Acquired Pneumonia. StatPearls Publishing; 2024.",
        "evidenceLevel": "Peer-Reviewed Systematic Compendium",
        "sourcedContent": [
            "Diagnostic thoracentesis criteria for parapneumonic effusion vs complicated empyema (pleural fluid pH < 7.20, glucose < 60 mg/dL, positive Gram stain/culture -> prompt tube thoracostomy drainage).",
            "Predictive value of CURB-65 vs Pneumonia Severity Index (PSI) in 30-day mortality."
        ]
    }
]

HF_REFERENCES = [
    {
        "id": "ref-amboss-hf",
        "sourceType": "AMBOSS Knowledge",
        "title": "AMBOSS Clinical Knowledge: Heart Failure (HFrEF & HFpEF)",
        "url": "https://www.amboss.com/us/knowledge/heart-failure",
        "citation": "AMBOSS Editorial Board. Heart Failure (HF). AMBOSS Knowledge Platform, 2024.",
        "evidenceLevel": "Guideline Consensus & Systematic Review",
        "sourcedContent": [
            "NYHA functional classification (Classes I–IV) and ACC/AHA staging (Stages A–D).",
            "Framingham diagnostic criteria: 2 major OR 1 major + 2 minor criteria required for clinical diagnosis.",
            "Natriuretic peptide cutoff values: BNP < 35 pg/mL (outpatient) or < 100 pg/mL (acute); NT-proBNP < 125 pg/mL (outpatient) or < 300 pg/mL (acute) has > 98% negative predictive value.",
            "Phenotypic classification by ejection fraction: HFrEF (LVEF ≤ 40%), HFmrEF (LVEF 41–49%), HFpEF (LVEF ≥ 50%)."
        ]
    },
    {
        "id": "ref-osmosis-hf",
        "sourceType": "Osmosis Clinical",
        "title": "Osmosis by Elsevier: Heart Failure (Pathophysiology & Pharmacology)",
        "url": "https://www.osmosis.org/learn/Heart_failure",
        "citation": "Osmosis by Elsevier. Heart Failure: Pathophysiology, Neurohormonal Compensation, and GDMT, 2024.",
        "evidenceLevel": "Illustrated Clinical & Pathophysiological Review",
        "sourcedContent": [
            "Neurohormonal maladaptation pathways: RAAS cascade, chronic sympathetic nervous system toxicity, and the counter-regulatory natriuretic peptide system.",
            "Distinction between forward failure (decreased cardiac output, fatigue, prerenal azotemia) and backward failure (venous congestion, pulmonary edema, elevated JVP, peripheral edema).",
            "Cellular mechanism of Neprilysin inhibition (Sacubitril) combined with AT1 receptor blockade (Valsartan) to prevent degradation of vasoactive peptides."
        ]
    },
    {
        "id": "ref-fa-hf",
        "sourceType": "First Aid USMLE Step 2 CK",
        "title": "First Aid for the USMLE Step 2 CK: Cardiovascular — Congestive Heart Failure",
        "url": "https://www.usmle.org/",
        "citation": "Tao Le, Vikas Bhushan, et al. First Aid for the USMLE Step 2 CK (11th & 12th Eds). McGraw-Hill Medical.",
        "evidenceLevel": "USMLE Core Curriculum Synthesis",
        "sourcedContent": [
            "The 'Fantastic Four' GDMT pillars proven to reduce mortality in HFrEF: 1. ARNI (Sacubitril/Valsartan) or ACEi/ARB; 2. Beta-blockers (Bisoprolol, Carvedilol, Metoprolol succinate); 3. MRA (Spironolactone, Eplerenone); 4. SGLT2 inhibitors (Dapagliflozin, Empagliflozin).",
            "Symptomatic relief without mortality reduction: Loop diuretics (Furosemide) and Digoxin.",
            "Mandatory 36-hour washout period when transitioning from an ACE inhibitor to Sacubitril/Valsartan to prevent life-threatening angioedema.",
            "Contraindication: Beta-blockers must NOT be started or up-titrated during acute decompensated wet pulmonary edema (wait until euvolemic)."
        ]
    },
    {
        "id": "ref-aha-acc-hf",
        "sourceType": "2022 AHA/ACC/HFSA Guidelines",
        "title": "2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure",
        "url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001063",
        "citation": "Heidenreich PA, et al. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. Circulation. 2022;145(18):e895-e1032.",
        "evidenceLevel": "Class 1A Societal Practice Guideline",
        "sourcedContent": [
            "Class 1A recommendation for quadruple GDMT initiation in all patients with HFrEF.",
            "Target titration dosing:",
            "  * Sacubitril/Valsartan target 97/103 mg BID (equivalent to 200 mg BID)",
            "  * Carvedilol target 25 mg BID (50 mg BID if > 85 kg); Metoprolol succinate target 200 mg OD; Bisoprolol target 10 mg OD",
            "  * Spironolactone target 25–50 mg OD (monitor K+ and creatinine)",
            "  * Dapagliflozin 10 mg OD or Empagliflozin 10 mg OD (fixed single dose).",
            "Device therapy criteria: Primary prevention ICD (LVEF ≤ 35% after ≥ 3 months of optimal GDMT, NYHA II–III) and CRT-D (LVEF ≤ 35%, sinus rhythm, LBBB with QRS ≥ 150 ms)."
        ]
    },
    {
        "id": "ref-esc-hf",
        "sourceType": "2023 ESC Guidelines",
        "title": "2023 Focused Update of the 2021 ESC Heart Failure Guidelines",
        "url": "https://academic.oup.com/eurheartj/article/44/37/3627/7246288",
        "citation": "McDonagh TA, et al. 2023 Focused Update of the 2021 ESC Guidelines for the diagnosis and treatment of acute and chronic heart failure. Eur Heart J. 2023;44(37):3627-3639.",
        "evidenceLevel": "Class 1A International Guideline",
        "sourcedContent": [
            "Class 1A recommendation extending SGLT2 inhibitors (Dapagliflozin and Empagliflozin) to the entire spectrum of LVEF, including HFmrEF (LVEF 41–49%) and HFpEF (LVEF ≥ 50%).",
            "Strong emphasis on rapid in-hospital GDMT initiation and aggressive up-titration prior to hospital discharge with early clinical follow-up within 6 weeks."
        ]
    },
    {
        "id": "ref-dod-hf",
        "sourceType": "Doctor on Duty 3rd Ed",
        "title": "Doctor on Duty (3rd Edition - Cardiology & Diuretic Protocols) & House Job Ward Manual",
        "url": "https://github.com/hassanakhter079/doctor-on-duty",
        "citation": "Doctor on Duty: A Comprehensive Emergency and Ward Practice Manual (3rd Ed), adapted with Pakistani commercial brand guidelines.",
        "evidenceLevel": "Bedside Emergency & Clinical Ward Protocol",
        "sourcedContent": [
            "Pakistani commercial brand formulations and clinical titration schedules:",
            "  * Tab. Entresto (Sacubitril/Valsartan 50 mg, 100 mg, 200 mg)",
            "  * Tab. Concor (Bisoprolol 2.5 mg, 5 mg, 10 mg) / Tab. Carvitor (Carvedilol 3.125 mg, 6.25 mg, 12.5 mg, 25 mg)",
            "  * Tab. Aldactone (Spironolactone 25 mg)",
            "  * Tab. Jardiance (Empagliflozin 10 mg) / Tab. Forxiga (Dapagliflozin 10 mg)",
            "  * Inj. / Tab. Lasix (Furosemide 20 mg, 40 mg) titrated to dry weight and daily fluid restriction (1.5–2 L/day)."
        ]
    }
]

DKA_REFERENCES = [
    {
        "id": "ref-amboss-dka",
        "sourceType": "AMBOSS Knowledge",
        "title": "AMBOSS Clinical Knowledge: Diabetic Ketoacidosis & HHS",
        "url": "https://www.amboss.com/us/knowledge/diabetic-ketoacidosis-and-hyperosmolar-hyperglycemic-state",
        "citation": "AMBOSS Editorial Board. Diabetic Ketoacidosis (DKA) and Hyperosmolar Hyperglycemic State (HHS). AMBOSS Knowledge Platform, 2024.",
        "evidenceLevel": "Guideline Consensus & Systematic Review",
        "sourcedContent": [
            "Classic diagnostic triad: Hyperglycemia (> 250 mg/dL), Anion gap metabolic acidosis (pH < 7.30, serum bicarbonate < 18 mEq/L, anion gap > 12), and positive Ketonemia (serum beta-hydroxybutyrate > 3.0 mmol/L) / Ketonuria.",
            "Severity classification: Mild (pH 7.25–7.30, HCO3 15–18, alert); Moderate (pH 7.00–7.24, HCO3 10–<15, drowsy); Severe (pH < 7.00, HCO3 < 10, stupor/coma).",
            "Resolution criteria: Blood glucose < 200 mg/dL AND two of the following: serum bicarbonate ≥ 15 mEq/L, venous pH > 7.3, and calculated anion gap ≤ 12 mEq/L."
        ]
    },
    {
        "id": "ref-osmosis-dka",
        "sourceType": "Osmosis Clinical",
        "title": "Osmosis by Elsevier: Diabetic Ketoacidosis (Pathophysiology & Fluid Dynamics)",
        "url": "https://www.osmosis.org/learn/Diabetic_ketoacidosis",
        "citation": "Osmosis by Elsevier. Diabetic Ketoacidosis: Pathophysiology, Osmotic Diuresis, and Insulin Action, 2024.",
        "evidenceLevel": "Illustrated Clinical & Pathophysiological Review",
        "sourcedContent": [
            "Intracellular starvation cascade: Absolute insulin lack combined with glucagon/epinephrine excess stimulates hormone-sensitive lipase -> hepatic beta-oxidation of free fatty acids generates acetoacetate and beta-hydroxybutyrate.",
            "Electrolyte shift paradox: Total body potassium is depleted from osmotic diuresis and vomiting, yet serum potassium may appear normal or elevated (due to acidosis and insulin lack); insulin drives potassium back into cells, creating high risk for fatal hypokalemia.",
            "Pathophysiological risk of cerebral edema from rapid reduction in serum effective osmolality during resuscitation."
        ]
    },
    {
        "id": "ref-fa-dka",
        "sourceType": "First Aid USMLE Step 2 CK",
        "title": "First Aid for the USMLE Step 2 CK: Endocrinology — Diabetic Emergencies",
        "url": "https://www.usmle.org/",
        "citation": "Tao Le, Vikas Bhushan, et al. First Aid for the USMLE Step 2 CK (11th & 12th Eds). McGraw-Hill Medical.",
        "evidenceLevel": "USMLE Core Curriculum Synthesis",
        "sourcedContent": [
            "The 'Triple Priority Rule' of DKA resuscitation:",
            "  1. Fluids FIRST: Rapid IV isotonic normal saline (0.9% NaCl 1000–1500 mL in the first hour) to restore perfusion.",
            "  2. Check Potassium BEFORE insulin: Never give insulin if K+ < 3.3 mEq/L (replete K+ first to avoid fatal arrhythmia / respiratory arrest).",
            "  3. Continuous IV Regular Insulin infusion (0.1 units/kg/h).",
            "The Dextrose Switch Rule: When blood glucose drops to 200–250 mg/dL, add 5% Dextrose to IV fluids (D5W / 0.45% Saline) to allow continued insulin administration until the anion gap closes.",
            "Subcutaneous bridging: Administer subcutaneous basal insulin 1–2 hours before stopping the IV insulin infusion to prevent rebound ketoacidosis."
        ]
    },
    {
        "id": "ref-ada-dka",
        "sourceType": "ADA Standards of Care 2024",
        "title": "ADA Standards of Care in Diabetes (2024): Management of Hyperglycemic Crises",
        "url": "https://diabetesjournals.org/care/issue/47/Supplement_1",
        "citation": "American Diabetes Association. Standards of Care in Diabetes—2024. Diabetes Care 2024;47(Suppl. 1):S1-S343.",
        "evidenceLevel": "Class 1A Societal Practice Guideline",
        "sourcedContent": [
            "Fluid resuscitation: 0.9% NaCl at 15–20 mL/kg/h for the first hour; switch to 0.45% NaCl if corrected serum sodium is normal or elevated; switch to 5% Dextrose with 0.45% NaCl once blood glucose < 200 mg/dL.",
            "Insulin infusion: Fixed rate 0.1 U/kg/h IV infusion; target blood glucose reduction rate of 50–75 mg/dL per hour (if glucose does not decline by 50 mg/dL in the first hour, double the insulin infusion rate).",
            "Potassium dosing: Add 20–30 mEq K+ per liter of IV fluid once serum K+ is 3.3–5.2 mEq/L to maintain serum K+ between 4.0–5.0 mEq/L.",
            "Sodium bicarbonate indication: Indicated only if arterial pH < 6.90 (100 mmol sodium bicarbonate in 400 mL sterile water with 20 mEq KCl infused over 2 hours)."
        ]
    },
    {
        "id": "ref-dod-dka",
        "sourceType": "Doctor on Duty 3rd Ed",
        "title": "Doctor on Duty (3rd Edition - DKA Ward Flowsheet) & House Job Clinical Notes (Dr. Hassan Akhtar)",
        "url": "https://github.com/hassanakhter079/doctor-on-duty",
        "citation": "Doctor on Duty: A Comprehensive Emergency and Ward Practice Manual (3rd Ed), adapted with Pakistani commercial brand guidelines.",
        "evidenceLevel": "Bedside Emergency & Clinical Ward Protocol",
        "sourcedContent": [
            "Pakistani emergency ward DKA syringe pump recipe and bedside orders:",
            "  * Inj. Regular Humulin R / Actrapid: 50 units in 50 mL 0.9% Normal Saline on syringe pump run at calculated mL/hr (1 mL = 1 unit).",
            "  * Hourly Capillary Blood Glucose (CBG / Accu-Chek) bedside monitoring sheet.",
            "  * Fluid rotation: Normal Saline (0.9% N/S) -> D5S (5% Dextrose Saline) when CBG < 250 mg/dL.",
            "  * Inj. Potassium Chloride (KCl ampoules): Strict IV safety rule: NEVER give IV bolus / push; dilute in IV fluid bag, maximum 20 mEq/hour in peripheral line with cardiac monitor.",
            "  * Catheterization for hourly urine output monitoring (target > 0.5 mL/kg/hr).",
            "  * Subcutaneous bridging: Inj. Lantus (Insulin Glargine) 0.2 U/kg SC + Humulin R 0.5–1.0 U/kg/day split TDS given with food 1-2 hours before stopping pump."
        ]
    },
    {
        "id": "ref-statpearls-dka",
        "sourceType": "StatPearls & NCBI Bookshelf",
        "title": "StatPearls (NCBI/NIH): Diabetic Ketoacidosis",
        "url": "https://www.ncbi.nlm.nih.gov/books/NBK430769/",
        "citation": "Lizzo JM, Goyal A, Gupta V. Adult Diabetic Ketoacidosis. StatPearls Publishing; 2024.",
        "evidenceLevel": "Peer-Reviewed Systematic Compendium",
        "sourcedContent": [
            "Comprehensive review of precipitating factors (the 5 'I's: Infection, Infarction, Infant/Pregnancy, Indiscretion/Diet, Insulin omission).",
            "Corrected sodium calculation formula: Measured Na + 1.6 * ((Glucose - 100) / 100) mg/dL.",
            "Euglycemic DKA awareness in patients taking SGLT2 inhibitors (normal or minimally elevated blood glucose with severe anion gap acidosis)."
        ]
    }
]

# Assign references to articles
data['ARTICLES']['acs']['references'] = ACS_REFERENCES
data['ARTICLES']['cap']['references'] = CAP_REFERENCES
data['ARTICLES']['hf']['references'] = HF_REFERENCES
data['ARTICLES']['dka']['references'] = DKA_REFERENCES

# Add source tags to summaries
data['ARTICLES']['acs']['summary'] = (
    "**Acute Coronary Syndrome (ACS)** encompasses a clinical spectrum of acute myocardial ischemia resulting from sudden reduction in coronary blood flow—most commonly due to atherosclerotic plaque disruption and superimposed thrombosis [[ref:ref-amboss-acs|AMBOSS]] [[ref:ref-esc-acs|ESC 2023]]. "
    "It comprises [[hl:{{term:ua|Unstable Angina (UA)}}]], [[hl:{{term:nstemi|NSTEMI}}]], and [[hl:{{term:stemi|STEMI}}]] [[ref:ref-fa-acs|First Aid CK]]."
)

data['ARTICLES']['cap']['summary'] = (
    "**Community-Acquired Pneumonia (CAP)** is an acute infection of the pulmonary parenchyma acquired outside the hospital (or < 48 hours after admission) [[ref:ref-amboss-cap|AMBOSS]]. "
    "Management relies on severity stratification ({{term:curb65|CURB-65}} / PSI) [[ref:ref-fa-cap|First Aid]] and targeted empiric antibiotic therapy [[ref:ref-ats-idsa-cap|ATS/IDSA 2019]] [[ref:ref-dod-cap|Doctor on Duty]]."
)

data['ARTICLES']['hf']['summary'] = (
    "**Heart Failure (HF)** is a complex clinical syndrome resulting from structural or functional impairment of ventricular filling or ejection of blood, categorized primarily into **HFrEF** (LVEF ≤ 40%) and **HFpEF** (LVEF ≥ 50%) [[ref:ref-amboss-hf|AMBOSS]] [[ref:ref-osmosis-hf|Osmosis]]. "
    "Cornerstone management requires quadruple Guideline-Directed Medical Therapy (GDMT) [[ref:ref-aha-acc-hf|AHA/ACC 2022]] [[ref:ref-esc-hf|ESC 2023]] [[ref:ref-dod-hf|Doctor on Duty]]."
)

data['ARTICLES']['dka']['summary'] = (
    "**Diabetic Ketoacidosis (DKA)** is a life-threatening acute metabolic complication of severe insulin deficiency and counter-regulatory hormone excess characterized by the triad of **hyperglycemia**, **ketonemia**, and **high-{{term:aniongap|anion gap}} metabolic acidosis** [[ref:ref-amboss-dka|AMBOSS]] [[ref:ref-osmosis-dka|Osmosis]]. "
    "Resuscitation mandates aggressive fluid rehydration, pre-emptive potassium repletion, and continuous IV insulin [[ref:ref-ada-dka|ADA 2024]] [[ref:ref-dod-dka|Doctor on Duty]]."
)

with open('/root/medbase/medbase_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated /root/medbase/medbase_data.json with rich references!")
for aid, art in data['ARTICLES'].items():
    print(f"Article {aid}: {len(art.get('references', []))} references attached.")
