---
name: public-finance-data
description: Retrieve Estonian Ministry of Finance budget, strategy, liabilities, payments, and consolidated-accounting documents from fin.ee.
---

# Ministry of Finance Records

## Access

Public HTML document tables and direct PDF, DOCX, and XLSX downloads. No login. Use a normal user agent if the VPortal/Cloudflare edge returns 403 to a generic client.

## Entry pages

- Annual budgets: https://www.fin.ee/riigi-rahandus-ja-maksud/riigieelarve-ja-eelarvestrateegia/riigieelarved
- State budget strategy: https://www.fin.ee/riigi-rahandus-ja-maksud/riigieelarve-ja-eelarvestrateegia/riigi-eelarvestrateegia
- Liabilities: https://www.fin.ee/riigi-rahandus-ja-maksud/riigikassa/riigi-finantskohustised
- Investor relations: https://www.fin.ee/riigi-rahandus-ja-maksud/riigikassa/investorsuhted
- Government payments: https://www.fin.ee/riigi-rahandus-ja-maksud/riigi-raamatupidamine/valitsussektori-maksed
- Consolidated reports: https://www.fin.ee/riigi-rahandus-ja-maksud/riigi-raamatupidamine/riigi-raamatupidamise-koondaruanded

## Retrieve

1. Fetch the narrowest entry page for the topic and year.
2. Extract linked records from the HTML, including links inside `script type="application/json"` datatable blocks when present.
3. Resolve `/sites/default/files/...` links against `https://www.fin.ee` and download the exact official file.
4. Preserve the page label, publication date, file title, direct URL, and file type.
5. Treat Power BI/Tableau sections as browser-only unless a documented download is exposed.

## Return

Keep `topic`, `year`, `source_page_url`, `record_title`, `publication_date`, `record_type`, `download_or_view_url`, language, retrieval time, and the extracted fiscal fields with original units.

## Limits

- Pages mix drafts, explanatory memoranda, approved laws, execution reports, and historical years; label document status explicitly.
- Embedded dashboard visuals are not equivalent to a bulk-data API.
- Do not rely on a hard-coded datatable ID; locate current datatable blocks or file anchors in the fetched page.

## Verify

Require the page to contain official `/sites/default/files/` links and the selected file to return the expected signature/content type. For an XLSX require ZIP magic bytes and a valid workbook; do not treat a rendered 404 HTML page as a document.
