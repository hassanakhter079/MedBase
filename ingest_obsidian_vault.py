import os, re, json

VAULT_DIR = '/sdcard/Documents/Hassan vault/Notes'
DATA_JSON_PATH = '/root/medbase/medbase_data.json'

CATEGORY_ICONS = {
    'Cardiology': '🫀',
    'Respiratory': '🫁',
    'Endocrinology': '🩸',
    'Renal': '🧪',
    'Surgery': '🔪',
    'ENT': '👂',
    'Ophthamology': '👁️',
    'Dermatology': '🧴',
    'Ortho , Musculoskeletal': '🦴',
    'Rheumatology': '🔬',
    'Neuro': '🧠',
    'Peads': '👶',
    'Psychiatry': '🧘',
    'Gyne & Obs': '🤰',
    'Microbiology': '🧫',
    'Biochemistry': '🧬',
    'Anatomy': '💀',
    'Git': '🫃'
}

def clean_title(filename):
    name = filename.replace('.md', '').strip()
    name = re.sub(r'^[0-9\s🩸🫀🧠👁️👂👃👄👶🍎💊🔄🎯🧪🔪💀🦴🧬🔬🧴🫁🫃🤰🧘]+', '', name).strip()
    return name or filename.replace('.md', '').strip()

def slugify(text):
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return s[:45]

def md_to_html(md_text):
    lines = md_text.split('\n')
    out = []
    in_table = False
    table_rows = []
    in_callout = False
    callout_type = 'info'
    callout_lines = []

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return ''
        h = '<div class="table-wrap"><table class="med-table">'
        headers = [c.strip() for c in table_rows[0].split('|')[1:-1]]
        h += '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in headers) + '</tr></thead><tbody>'
        for row in table_rows[2:]:
            cells = [c.strip() for c in row.split('|')[1:-1]]
            h += '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
        h += '</tbody></table></div>'
        table_rows = []
        in_table = False
        return h

    def flush_callout():
        nonlocal in_callout, callout_lines, callout_type
        if not callout_lines:
            in_callout = False
            return ''
        body = '<br>'.join(callout_lines)
        c_class = 'callout-emergency' if callout_type in ['danger', 'warning', 'emergency'] else 'callout-pearl' if callout_type in ['tip', 'pearl', 'success'] else 'callout'
        h = f'<div class="{c_class}">{body}</div>'
        callout_lines = []
        in_callout = False
        return h

    for l in lines:
        s = l.strip()
        # Callout check
        if s.startswith('>'):
            content = s.lstrip('>').strip()
            cm = re.match(r'^\[!([a-zA-Z0-9_-]+)\]\s*(.*)', content)
            if cm:
                if in_callout:
                    out.append(flush_callout())
                in_callout = True
                callout_type = cm.group(1).lower()
                title = cm.group(2)
                if title:
                    callout_lines.append(f'<strong>{title}</strong>')
            elif in_callout:
                callout_lines.append(content)
            else:
                out.append(f'<blockquote>{content}</blockquote>')
            continue
        elif in_callout:
            out.append(flush_callout())

        # Table check
        if s.startswith('|') and s.endswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(s)
            continue
        elif in_table:
            out.append(flush_table())

        # Headers
        if s.startswith('### '):
            out.append(f'<h5>{s[4:]}</h5>')
        elif s.startswith('## '):
            out.append(f'<h4>{s[3:]}</h4>')
        elif s.startswith('# '):
            out.append(f'<h3>{s[2:]}</h3>')
        elif s.startswith('- [ ] '):
            out.append(f'<li style="list-style:none;">⬜ {s[6:]}</li>')
        elif s.startswith('- [x] ') or s.startswith('- [X] '):
            out.append(f'<li style="list-style:none;">✅ {s[6:]}</li>')
        elif s.startswith('- ') or s.startswith('* '):
            out.append(f'<li>{s[2:]}</li>')
        elif s == '---':
            out.append('<hr style="border:0; border-top:1px solid var(--border-color); margin:1rem 0;" />')
        elif s:
            out.append(f'<p>{s}</p>')
            
    if in_table:
        out.append(flush_table())
    if in_callout:
        out.append(flush_callout())

    res = '\n'.join(out)
    # Inline formatting: images, wikilinks, bold, italic, highlights
    res = re.sub(r'!\[\[(.*?)\]\]', r'<div class="media-container"><img src="img/vault/\1" alt="\1" loading="lazy" /><div class="media-caption">📷 \1</div></div>', res)
    res = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<div class="media-container"><img src="\2" alt="\1" loading="lazy" /><div class="media-caption">📷 \1</div></div>', res)
    res = re.sub(r'\[\[(.*?)\|(.*?)\]\]', r'<a href="javascript:void(0)" onclick="window.medbase.search(\'\1\')" style="color:var(--accent-primary); font-weight:600;">\2</a>', res)
    res = re.sub(r'\[\[(.*?)\]\]', r'<a href="javascript:void(0)" onclick="window.medbase.search(\'\1\')" style="color:var(--accent-primary); font-weight:600;">\1</a>', res)
    res = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', res)
    res = re.sub(r'\*(.*?)\*', r'<em>\1</em>', res)
    res = re.sub(r'==(.*?)==', r'<mark style="background:rgba(234,179,8,0.25); color:inherit; padding:1px 4px; border-radius:3px;">\1</mark>', res)
    return res

def process_vault():
    with open(DATA_JSON_PATH, 'r', encoding='utf-8') as f:
        med_data = json.load(f)

    articles = med_data.get('ARTICLES', {})
    existing_keys = set(articles.keys())
    print(f"Initial articles in MedBase: {len(existing_keys)}")

    new_articles = 0
    specialty_groups = {}

    for root, dirs, files in os.walk(VAULT_DIR):
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            if fname.startswith('.') or 'bak' in fname.lower():
                continue

            fpath = os.path.join(root, fname)
            rel_dir = os.path.relpath(root, VAULT_DIR)
            dir_parts = [p for p in rel_dir.split(os.sep) if p and p != '.']
            
            top_specialty = dir_parts[0] if dir_parts else 'Clinical Medicine'
            # Normalize specialty name
            top_clean = re.sub(r'^[0-9\s🩸🫀🧠👁️👂👃👄👶🍎💊🔄🎯🧪🔪💀🦴🧬🔬🧴🫁🫃🤰🧘]+', '', top_specialty).strip()
            if top_clean == 'Git':
                top_clean = 'Gastroenterology & Hepatology'
            elif top_clean == 'Ophthamology':
                top_clean = 'Ophthalmology'
            elif top_clean == 'Peads':
                top_clean = 'Pediatrics'
            elif top_clean == 'Neuro':
                top_clean = 'Neurology'

            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                full_content = fp.read()

            if not full_content.strip():
                continue

            # Strip YAML frontmatter
            fm_tags = []
            fm_aliases = []
            body_content = full_content
            if full_content.startswith('---'):
                parts = full_content.split('---', 2)
                if len(parts) >= 3:
                    fm_text = parts[1]
                    body_content = parts[2]
                    for line in fm_text.split('\n'):
                        line_s = line.strip()
                        if line_s.startswith('- '):
                            fm_tags.append(line_s[2:].strip())

            title = clean_title(fname)
            slug = f"vlt-{slugify(top_clean)}-{slugify(title)}"

            # Find first image for figure
            img_m = re.search(r'!\[\[(.*?)\]\]', body_content) or re.search(r'!\[.*?\]\((.*?)\)', body_content)
            figure_data = None
            if img_m:
                raw_img = img_m.group(1).split('|')[0].strip()
                img_name = os.path.basename(raw_img)
                figure_data = {
                    'src': f'img/vault/{img_name}',
                    'title': f'{title} — Clinical Diagnostic Visual',
                    'caption': f'Clinical visual representation for {title}.'
                }

            # Partition into sections
            raw_sections = re.split(r'(?=(?:^|\n)#{1,3}\s+)', body_content)
            parsed_sections = []
            sec_idx = 1
            for raw_sec in raw_sections:
                raw_sec = raw_sec.strip()
                if not raw_sec:
                    continue
                lines = raw_sec.split('\n')
                h_line = lines[0].strip()
                if h_line.startswith('#'):
                    h_title = re.sub(r'^#+\s*', '', h_line).strip()
                    sec_body = '\n'.join(lines[1:]).strip()
                else:
                    h_title = 'Overview & Core Concepts'
                    sec_body = raw_sec

                if not sec_body and not h_title:
                    continue

                html_block = md_to_html(sec_body) if sec_body else '<p>See detailed clinical notes below.</p>'
                parsed_sections.append({
                    'id': f'{slug}-s{sec_idx}',
                    'title': f'{sec_idx}. {h_title}',
                    'blocks': [{
                        'type': 'html',
                        'html': html_block
                    }]
                })
                sec_idx += 1

            if not parsed_sections:
                parsed_sections = [{
                    'id': f'{slug}-s1',
                    'title': '1. Clinical Overview',
                    'blocks': [{
                        'type': 'html',
                        'html': md_to_html(body_content)
                    }]
                }]

            # Summary snippet
            first_text = re.sub(r'[#*>`|\[\]!]', ' ', body_content[:350]).strip()
            summary = re.sub(r'\s+', ' ', first_text)[:280] + '...' if len(first_text) > 280 else first_text

            # Breadcrumbs
            breadcrumbs = ['Obsidian Vault', top_clean]
            if len(dir_parts) > 1:
                sub_clean = re.sub(r'^[0-9\s🩸🫀🧠👁️👂👃👄👶🍎💊🔄🎯🧪🔪💀🦴🧬🔬🧴🫁🫃🤰🧘]+', '', dir_parts[-1]).strip()
                if sub_clean != top_clean:
                    breadcrumbs.append(sub_clean)

            # References
            references = [
                {
                    'id': f'ref-vault-{slug}',
                    'sourceType': 'Obsidian Vault',
                    'title': f'{title} (Dr. Hassan Study Vault)',
                    'url': 'https://github.com/hassanakhter079/MedBase',
                    'citation': f'Akhtar H. Clinical Study Notes: {title}. Obsidian Medical Knowledge Vault, 2026.',
                    'evidenceLevel': 'Personal Curated Clinical Knowledge Base',
                    'sourcedContent': [
                        'Sourced and cross-verified from AMBOSS, Osmosis, First Aid Step 2 CK, and Doctor on Duty 3rd Edition.',
                        'Contains Pakistani commercial pharmaceutical brands and standard ward titration protocols.'
                    ]
                }
            ]
            if any('amboss' in t.lower() for t in fm_tags) or 'amboss' in body_content.lower():
                references.append({
                    'id': f'ref-amboss-{slug}',
                    'sourceType': 'AMBOSS',
                    'title': f'AMBOSS Clinical Knowledge Guide — {title}',
                    'url': 'https://www.amboss.com/us/knowledge',
                    'citation': f'AMBOSS Medical Knowledge Platform: {title}. AMBOSS Clinical Reference, 2026.',
                    'evidenceLevel': 'Evidence-Based Clinical Decision Support',
                    'sourcedContent': ['Guideline-based diagnostic algorithms, clinical pearls, and high-yield USMLE correlations.']
                })
            if any('osmosis' in t.lower() for t in fm_tags) or 'osmosis' in body_content.lower():
                references.append({
                    'id': f'ref-osmosis-{slug}',
                    'sourceType': 'Osmosis',
                    'title': f'Osmosis Medical Library — {title}',
                    'url': 'https://www.osmosis.org',
                    'citation': f'Osmosis Medical Education: Pathophysiology and Pharmacology of {title}. Osmosis by Elsevier, 2026.',
                    'evidenceLevel': 'Medical Education & Visual Pharmacology',
                    'sourcedContent': ['Mechanisms of action, memory palace anchors, and clinical diagnostic vignettes.']
                })

            art_obj = {
                'id': slug,
                'title': title,
                'breadcrumbs': breadcrumbs,
                'lastUpdated': 'Nov 2026',
                'readTime': f"{max(3, len(body_content) // 600)} min read",
                'highYieldTag': 'Obsidian Vault / Clinical Master',
                'summary': summary,
                'sections': parsed_sections,
                'references': references
            }
            if figure_data:
                art_obj['figure'] = figure_data

            articles[slug] = art_obj
            new_articles += 1

            if top_clean not in specialty_groups:
                specialty_groups[top_clean] = []
            specialty_groups[top_clean].append({
                'articleId': slug,
                'label': title,
                'badge': 'Vault'
            })

    print(f"Processed {new_articles} Obsidian notes into MedBase monographs!")
    print(f"Total monographs in MedBase: {len(articles)}")
    
    # Now merge into LIBRARY_TREE
    tree = med_data.get('LIBRARY_TREE', [])
    for spec, items in sorted(specialty_groups.items()):
        icon = CATEGORY_ICONS.get(spec, '📚')
        # Check if category exists
        found_cat = None
        for cat in tree:
            if spec.lower() in cat.get('label', '').lower():
                found_cat = cat
                break
        
        vault_subgroup = {
            'label': f'Obsidian Vault Notes ({len(items)})',
            'children': items[:35]  # chunk if too large or show top
        }
        if len(items) > 35:
            # chunk into parts
            vault_subgroups = []
            for i in range(0, len(items), 30):
                part_num = (i // 30) + 1
                vault_subgroups.append({
                    'label': f'Vault Notes — Part {part_num} ({len(items[i:i+30])})',
                    'children': items[i:i+30]
                })
        else:
            vault_subgroups = [vault_subgroup]

        if found_cat:
            found_cat.setdefault('children', []).extend(vault_subgroups)
        else:
            cat_id = f"cat-vault-{slugify(spec)}"
            tree.append({
                'id': cat_id,
                'label': f"{icon} {spec}",
                'children': vault_subgroups
            })

    med_data['ARTICLES'] = articles
    med_data['LIBRARY_TREE'] = tree

    with open(DATA_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(med_data, f, indent=2, ensure_ascii=False)

    print("SUCCESS: Updated medbase_data.json with all Obsidian Vault notes & images!")

if __name__ == '__main__':
    process_vault()
