import json

with open('/root/medbase/medbase_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Helper function to replace text safely
def enrich_text(obj):
    if isinstance(obj, str):
        # We can perform targeted replacements
        return obj
    elif isinstance(obj, list):
        return [enrich_text(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: enrich_text(v) for k, v in obj.items()}
    return obj

# --- ACS ENRICHMENT ---
acs = data['ARTICLES']['acs']
for sec in acs['sections']:
    if sec['id'] == 'acs-overview':
        for b in sec.get('blocks', []):
            if b.get('type') == 'callout' and 'Key Distinction' in b.get('title', ''):
                b['text'] = b['text'] + " [[ref:ref-amboss-acs|AMBOSS]] [[ref:ref-osmosis-acs|Osmosis]]"
    elif sec['id'] == 'acs-pathophys':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets' and len(b.get('items', [])) > 0:
                b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-osmosis-acs|Osmosis Pathophysiology]]"
    elif sec['id'] == 'acs-diag':
        for sub in sec.get('subsections', []):
            if sub['id'] == 'acs-diag-ecg':
                for b in sub.get('blocks', []):
                    if b.get('type') == 'bullets':
                        b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-amboss-acs|AMBOSS Criteria]] [[ref:ref-litfl-acs|LITFL]]"
            elif sub['id'] == 'acs-diag-localization':
                for b in sub.get('blocks', []):
                    if b.get('type') == 'bullets':
                        for item in b.get('items', []):
                            if 'High-Risk ECG STEMI Equivalents' in item.get('text', ''):
                                item['text'] = item['text'] + " [[ref:ref-litfl-acs|LITFL]] [[ref:ref-amboss-acs|AMBOSS]]"
            elif sub['id'] == 'acs-diag-biomarkers':
                for b in sub.get('blocks', []):
                    if b.get('type') == 'bullets':
                        b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-esc-acs|ESC 2023 Rapid Protocol]]"
    elif sec['id'] == 'acs-mgmt':
        for b in sec.get('blocks', []):
            if b.get('type') == 'callout' and 'MONA' in b.get('title', ''):
                b['text'] = b['text'] + " [[ref:ref-esc-acs|2023 ESC Guidelines]]"
        for sub in sec.get('subsections', []):
            if sub['id'] == 'acs-mgmt-initial':
                for b in sub.get('blocks', []):
                    if b.get('type') == 'bullets':
                        b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-esc-acs|ESC 2023]] [[ref:ref-dod-acs|Doctor on Duty Regimen]]"
            elif sub['id'] == 'acs-mgmt-reperfusion':
                for b in sub.get('blocks', []):
                    if b.get('type') == 'bullets':
                        b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-acc-aha-acs|ACC/AHA Revascularization 2021]]"
            elif sub['id'] == 'acs-mgmt-special':
                for b in sub.get('blocks', []):
                    if b.get('type') == 'bullets':
                        b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-fa-acs|First Aid CK Rule]] [[ref:ref-dod-acs|Doctor on Duty]]"
            elif sub['id'] == 'acs-mgmt-secondary':
                for b in sub.get('blocks', []):
                    if b.get('type') == 'bullets':
                        b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-esc-acs|ESC 2023]] [[ref:ref-acc-aha-acs|ACC/AHA]] [[ref:ref-dod-acs|Doctor on Duty]]"
    elif sec['id'] == 'acs-complications':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets':
                b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-fa-acs|First Aid CK Timeline]] [[ref:ref-osmosis-acs|Osmosis Mechanical Complications]]"

# --- CAP ENRICHMENT ---
cap = data['ARTICLES']['cap']
for sec in cap['sections']:
    if sec['id'] == 'cap-etiology':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets':
                b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-amboss-cap|AMBOSS]] [[ref:ref-fa-cap|First Aid]]"
    elif sec['id'] == 'cap-diag':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets':
                b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-osmosis-cap|Osmosis Physical Exam]] [[ref:ref-amboss-cap|AMBOSS Diagnostics]]"
            elif b.get('type') == 'callout':
                b['text'] = b['text'] + " [[ref:ref-statpearls-cap|StatPearls]]"
    elif sec['id'] == 'cap-mgmt':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets':
                if len(b.get('items', [])) > 0:
                    b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-fa-cap|First Aid CURB-65]]"
                if len(b.get('items', [])) > 1:
                    b['items'][1]['text'] = b['items'][1]['text'] + " [[ref:ref-ats-idsa-cap|ATS/IDSA 2019]] [[ref:ref-dod-cap|Doctor on Duty]]"

# --- HF ENRICHMENT ---
hf = data['ARTICLES']['hf']
for sec in hf['sections']:
    if sec['id'] == 'hf-class':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets':
                b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-amboss-hf|AMBOSS Classification]] [[ref:ref-osmosis-hf|Osmosis]]"
    elif sec['id'] == 'hf-mgmt':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets':
                b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-aha-acc-hf|2022 AHA/ACC/HFSA]] [[ref:ref-esc-hf|2023 ESC]] [[ref:ref-fa-hf|First Aid Fantastic Four]] [[ref:ref-dod-hf|Doctor on Duty]]"
            elif b.get('type') == 'callout':
                b['text'] = b['text'] + " [[ref:ref-fa-hf|First Aid CK]] [[ref:ref-aha-acc-hf|AHA/ACC]]"

# --- DKA ENRICHMENT ---
dka = data['ARTICLES']['dka']
for sec in dka['sections']:
    if sec['id'] == 'dka-diag':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets':
                b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-amboss-dka|AMBOSS Triad]] [[ref:ref-osmosis-dka|Osmosis Pathophysiology]]"
    elif sec['id'] == 'dka-mgmt':
        for b in sec.get('blocks', []):
            if b.get('type') == 'bullets':
                b['items'][0]['text'] = b['items'][0]['text'] + " [[ref:ref-ada-dka|ADA 2024 Standards]] [[ref:ref-fa-dka|First Aid Triple Priority]] [[ref:ref-dod-dka|Doctor on Duty & House Job Protocol]]"
            elif b.get('type') == 'callout':
                b['text'] = b['text'] + " [[ref:ref-fa-dka|First Aid CK]] [[ref:ref-dod-dka|Doctor on Duty]]"

with open('/root/medbase/medbase_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Enriched medbase_data.json with inline references across all 4 articles!")
