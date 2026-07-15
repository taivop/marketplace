---
name: crime-policy-statistics
description: Retrieve crime-policy studies, annual Crime in Estonia reports, and selected research datasets from the Ministry of Justice portal.
---

# Crime Policy Publications

## Access

- Study index: `https://www.kriminaalpoliitika.ee/et/statistika-ja-uuringud/uuringute-andmebaas`
- Annual reports: `https://www.kriminaalpoliitika.ee/et/statistika-ja-uuringud/kuritegevus-eestis`
- Research datasets: `https://www.kriminaalpoliitika.ee/et/statistika-ja-uuringud/uuringute-andmestikud`
- Public HTML and linked files; no login is required.

## Retrieve

Use the study index for topic discovery, then fetch the linked study page or direct PDF. The annual-report page provides direct PDFs for the historical `Kuritegevus Eestis` series. The dataset page is a small index of study-specific pages; inspect each selected page for its actual downloadable files and methodology.

Extract links from the relevant content section, resolve relative URLs against the page, and preserve the link text. Do not scrape the navigation menu as records.

## Return

- For publications, return title, year/date, topic, authors or publisher when stated, file/page URL, source index, and retrieval time.
- For datasets, also preserve format, variable/codebook links, population, fieldwork period, weighting, and access restrictions.
- Keep survey indicators separate from police, prosecution, court, or prison administrative statistics.

## Limits

- This is a publication index, not a current statistical API or real-time crime feed.
- Coverage and metadata are inconsistent; many records are reports only, and the annual series on this portal is historical.
- A linked study page does not guarantee an openly downloadable microdataset.

## Verify

- Require the study index to contain study record links and direct PDF links.
- Require the annual-report page to contain multiple `Kuritegevus Eestis` PDF links. Verify selected files begin with `%PDF-` before parsing.
