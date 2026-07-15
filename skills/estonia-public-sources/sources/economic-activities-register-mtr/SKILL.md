---
name: economic-activities-register-mtr
description: Search Estonia's legacy Economic Activities Register (MTR) for public operators, activity notices, and licences.
---

# Economic Activities Register (MTR)

## Access

- Operator search form: `GET https://mtr.ttja.ee/juriidiline_isik?m=96`
- Form submission: `POST https://mtr.ttja.ee/juriidiline_isik/filter/action`
- Response: server-rendered HTML using a session cookie and CSRF token; no login is required for public searches.

## Retrieve

1. Create one cookie-preserving HTTP session and fetch the search form.
2. Extract `juriidiline_isik_filters[_csrf_token]`.
3. Submit the form in the same session. Useful fields are:
   - `juriidiline_isik_filters[nimi][text]`
   - `juriidiline_isik_filters[registrikood][text]`
   - `juriidiline_isik_filters[tegevusala_id]`
   - `juriidiline_isik_filters[tegevusala_tyyp]`: `1` for notices or `2` for licences
   - `juriidiline_isik_filters[valjund_valjad][]`: request `nimi`, `registrikood`, and any other output columns needed
4. Follow the redirect to `/juriidiline_isik` and parse rows from `div.sf_admin_list`.
5. Follow each row's `/juriidiline_isik/<id>` link. The detail page contains `Majandustegevusteated` and `Tegevusload` tables with validity and activity fields.

Preserve the operator name, registration code, MTR record number, activity, validity dates, current/archive state, and detail URL.

## Limits

- Since 25 June 2025, notices and licences are being moved from MTR to `https://tarvik.ttja.ee/`; MTR alone is no longer guaranteed to be exhaustive for current activity.
- The public form is stateful. A POST without the cookie and current CSRF token will not reproduce the search.
- Use the dedicated notice (`/majandustegevusteade`) or licence (`/tegevusluba`) forms when the user asks for record-first rather than operator-first results; they use the same session/CSRF pattern.

## Verify

Require the submitted filter value to reappear under `Kasutatud filtrid`, at least one result row containing both name and registration code, and a working `/juriidiline_isik/<id>` detail link.
