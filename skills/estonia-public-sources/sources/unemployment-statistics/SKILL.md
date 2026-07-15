---
name: unemployment-statistics
description: Retrieve Estonian Unemployment Insurance Fund datasets and XLSX distributions through the national open-data catalog API.
---

# Unemployment Fund Statistics

## Access

- Dataset chooser: `https://andmed.eesti.ee/information-holders/eesti-tootukassa`
- Dataset metadata API: `https://andmed.eesti.ee/api/datasets/slug/{slug}`
- Send a browser-like `User-Agent` and `Origin: https://andmed.eesti.ee` if the API edge rejects a bare client.

## Retrieve

1. Use the chooser's 17 dataset links to select the subject and copy its slug. Subjects include registered unemployment, daily registered unemployment, vacancies, services, benefits, work-ability assessment, layoffs, work experience, and skills.
2. GET `api/datasets/slug/{slug}`. For registered unemployment, use `registreeritud-tootud`.
3. Read `distributions`; select by `titleEt`, `format`, and coverage rather than array position.
4. Download the chosen URL in `accessUrls`. These API URLs redirect to short-lived signed object-storage URLs, so do not persist the redirect target.

## Return

Preserve dataset slug/title/description, organization, temporal coverage, update time, distribution title, format, byte size, license, stable `accessUrls` URL, retrieval time, and original workbook headers.

## Limits

- The obsolete `https://www.tootukassa.ee/et/statistika-ja-uuringud` route renders an error and must not be used.
- A dataset can contain multiple XLSX distributions for different demographic or geographic cuts.
- Distinguish month-end stocks, during-month flows, and daily snapshots from titles and headers.

## Verify

Require `organization.slug: "eesti-tootukassa"`, public completed metadata, at least one distribution, and a valid XLSX ZIP signature from its stable `accessUrls` endpoint.
