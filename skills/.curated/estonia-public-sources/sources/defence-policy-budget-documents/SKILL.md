---
name: defence-policy-budget-documents
description: Retrieve current Estonian defence budget figures, policy documents, programme reports, and public-opinion survey PDFs from the Ministry of Defence.
---

# Defence Budget, Policy, and Surveys

Use this source for Ministry of Defence budget figures, policy/legal baselines, defence programmes, result reports, and public-opinion-on-defence surveys. Use `procurement-data` for individual tenders or contracts.

## Index pages

- Current defence budget: `https://kaitseministeerium.ee/poliitikad-ja-planeerimine/kaitsevoime-areng/kaitse-eelarve`
- Policy documents and legal acts: `https://kaitseministeerium.ee/poliitikad-ja-planeerimine/poliitikad/alusdokumendid-ja-oigusaktid`
- Public-opinion surveys: `https://www.kaitseministeerium.ee/trukised-uuringud`

## Workflow

1. For current budget totals and percentages, parse the budget page's headings and surrounding HTML text; cite the page and its `Viimati uuendatud` date.
2. For policy and programme documents, collect PDF and Riigi Teataja links from the policy page. Preserve each anchor label because it contains the document title, period, size, and format.
3. For surveys, collect the PDF links under `Avaliku arvamuse uuringud` on the publications page. The link labels give the survey month/year and file size; the archive runs from 2001 onward.
4. Download only the required PDFs and preserve the report's question wording, sample, fieldwork period, and methodology when comparing indicators over time.
5. Record index URL, direct document URL, label/date, and retrieval time.

Do not reuse the obsolete `/et/eesmargid-tegevused/...` routes. Flag links on the `prelive.vportal.ee` host as legacy rather than treating them as current canonical files.

## Verification

- The budget page contains a current `Kaitse-eelarve {year}` heading.
- The policy page exposes multiple official PDFs and Riigi Teataja links.
- The publications page exposes many dated opinion-survey PDFs; valid files start with `%PDF-`.
