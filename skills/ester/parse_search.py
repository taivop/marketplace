#!/usr/bin/env python3
"""Parse ESTER search results HTML from stdin. Output: JSON with results.
Handles both search result lists and direct record pages (e.g. ISBN search)."""
import sys, re, json, html

raw = sys.stdin.read()

# Detect if this is a direct record page (has holdings table, no search result list)
if 'class="bibItems"' in raw and 'class="hidden recordnumber"' not in raw:
    # Extract record ID from the page
    m = re.search(r'record=b(\d+)', raw)
    rid = m.group(1) if m else ""
    # Extract title from bibInfoData
    m = re.search(r'class="bibInfoLabel">Pealkiri</td>\s*<td class="bibInfoData">\s*(.*?)\s*</td>', raw, re.DOTALL)
    title = ""
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        title = html.unescape(title)
    print(json.dumps({"total": 1, "direct_record": True, "results": [{"id": rid, "title": title}]}, ensure_ascii=False, indent=2))
else:
    # Standard search results list
    m = re.search(r'Leiti\s+(\d+)\s+kirje', raw)
    total = int(m.group(1)) if m else 0

    ids = re.findall(r'class="hidden recordnumber">\s*(\d+)', raw)
    titles = re.findall(r'<h2 class="title">\s*<a[^>]*>([^<]+)</a>', raw)

    results = []
    for i, rid in enumerate(ids):
        title = html.unescape(titles[i].strip()) if i < len(titles) else ""
        results.append({"id": rid, "title": title})

    print(json.dumps({"total": total, "results": results}, ensure_ascii=False, indent=2))
