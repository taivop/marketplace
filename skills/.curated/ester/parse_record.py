#!/usr/bin/env python3
"""Parse ESTER record/holdings page HTML from stdin. Output: JSON with bib info + holdings.
Detects truncation and outputs the full holdings URL if available."""
import sys, re, json, html

raw = sys.stdin.read()

# Bibliographic info: label -> data pairs
bib = {}
for label, data in re.findall(
    r'class="bibInfoLabel">([^<]+)</td>\s*<td class="bibInfoData">\s*(.*?)\s*</td>',
    raw, re.DOTALL
):
    clean = re.sub(r'<[^>]+>', '', data).strip()
    clean = html.unescape(clean)
    if clean:
        bib[html.unescape(label.strip())] = clean

# Holdings table rows
holdings = []
for row in re.findall(r'<tr\s+class="bibItemsEntry">(.*?)</tr>', raw, re.DOTALL):
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    if len(cells) >= 3:
        def clean(c):
            c = re.sub(r'<!--[^>]*-->', '', c)
            c = re.sub(r'<[^>]+>', '', c)
            return html.unescape(c).strip().lstrip('\xa0').strip()
        holdings.append({
            "location": clean(cells[0]),
            "call_number": clean(cells[1]),
            "status": clean(cells[2]),
            "notes": clean(cells[3]) if len(cells) > 3 else ""
        })

# Check for truncation: look for "VAATA KÕIKI EKSEMPLARE" button with holdings URL
holdings_url = ""
m = re.search(r'action="([^"]*holdings[^"]*)"', raw)
if m:
    holdings_url = "https://www.ester.ee" + html.unescape(m.group(1))

result = {
    "title": bib.get("Pealkiri", ""),
    "author": bib.get("Autor", ""),
    "published": bib.get("Ilmunud", ""),
    "isbn": bib.get("ISBN", ""),
    "holdings_count": len(holdings),
    "holdings": holdings
}
if holdings_url:
    result["truncated"] = True
    result["full_holdings_url"] = holdings_url

print(json.dumps(result, ensure_ascii=False, indent=2))
