# Source Map

This is the canonical routing catalog for both Codex and Claude. Every source recipe must appear here, and every path listed here must exist.

## Quick Chooser

| If user asks about... | Start with source skill(s) |
|---|---|
| "official stats", "time series", "national indicators", macro/financial statistics | `sources/statistics-api`, `sources/bank-of-statistics`, `sources/open-data` |
| Parliament votes, MPs, sittings, agendas, stenograms | `sources/riigikogu-open-data` |
| Draft law lifecycle, ministry coordination, and public consultations | `sources/legislation-workflow-eis`, `sources/riigikogu-open-data`, `sources/riigiteataja-draft-acts` |
| Final laws and legal texts | `sources/legal-acts-data` |
| President decisions and decrees | `sources/president-decisions-decrees` |
| Cabinet/government meeting agendas | `sources/government-session-agendas` |
| Government document trails and registries | `sources/ministry-document-registries`, `sources/government-journal-records` |
| Government action programme tracking | `sources/government-action-programme` |
| Estonia 2035 action plan updates | `sources/estonia-2035-action-plan` |
| Registry of active strategic development documents | `sources/strategic-development-documents-registry` |
| Lobbying transparency | `sources/lobby-meetings` |
| Procurement/tenders/contracts | `sources/procurement-data` |
| Party finance and party membership | `sources/party-funding-data`, `sources/political-party-membership` |
| State audits and Chancellor of Justice annual oversight | `sources/state-audit-reports`, `sources/ombudsman-opinions` |
| Supreme Court judgments, all-court decisions/hearings, court-system statistics | `sources/supreme-court-judgments`, `sources/court-proceedings-data`, `sources/court-system-statistics` |
| Prison and probation annual/current indicators | `sources/prison-annual-reviews` |
| Official notices, insolvency announcements, summons (HTML/XML/RDF/TXT) | `sources/official-notices` |
| Business entities and company baseline data | `sources/business-register-open-data` |
| Licensed economic activity (MTR) | `sources/economic-activities-register-mtr` |
| State assets / state ownership | `sources/state-assets-register`, `sources/state-ownership-data` |
| State real-estate register open data (RKVR) | `sources/state-assets-register` |
| Agriculture support recipients / EU funded projects | `sources/agricultural-subsidies-pria`, `sources/eu-funded-projects` |
| Taxes and public tax inquiries | `sources/tax-customs-data`, `sources/tax-public-inquiries` |
| Budget and public finance | `sources/public-finance-data` |
| State budget strategy (RES), annual budget packages, liabilities, investor relations, consolidated accounting | `sources/public-finance-data` |
| Public-sector workforce/admin statistics | `sources/public-sector-statistics-fin` |
| Civil-service pay governance and salary disclosure templates | `sources/civil-service-pay-governance` |
| Health stats, medicines, health supervision | `sources/health-statistics`, `sources/medicines-register`, `sources/health-supervision-decisions` |
| Communicable disease bulletins and vaccination monitoring | `sources/communicable-disease-bulletins`, `sources/vaccination-statistics` |
| Seasonal COVID-19 hospitalization and risk-group vaccination aggregates | `sources/health-welfare-open-data` |
| Healthcare professionals and registration codes | `sources/healthcare-professionals-register` |
| Health insurance financing and service volumes | `sources/health-insurance-fund-reports` |
| Medicines market and regulatory annual statistics | `sources/medicines-agency-statistics` |
| Welfare and unemployment | `sources/social-insurance-statistics`, `sources/unemployment-statistics` |
| Environment permits and weather observations | `sources/environmental-permit-decisions`, `sources/weather-data` |
| Environmental charge supervision statistics | `sources/environmental-charge-statistics` |
| Forestry register records | `sources/forest-register` |
| Planning, construction, cadaster/geospatial | `sources/planning-decisions`, `sources/construction-register`, `sources/geospatial-open-data` |
| Transport/traffic and energy system operations | `sources/transport-traffic-data`, `sources/energy-data` |
| National public transport routes/stops and Peatus API | `sources/transport-traffic-data` |
| Aircraft and port registry checks | `sources/aircraft-register`, `sources/state-port-register` |
| Published aviation safety reports | `sources/aviation-safety-reports` |
| Maritime economy indicators | `sources/maritime-economy-statistics` |
| Cyber incidents and digital government operations | `sources/cyber-incidents-cert-ee`, `sources/public-sector-it-systems-riha`, `sources/x-road-usage-statistics`, `sources/digital-government-studies` |
| e-Residency operational dashboard metrics | `sources/e-residency-dashboard` |
| Municipal operations and datasets (Tallinn/Tartu) | `sources/tallinn-open-data`, `sources/tallinn-council-documents`, `sources/tartu-document-register`, `sources/open-data` |
| Elections and political process outcomes | `sources/election-results-data` |
| National Electoral Committee (VVK) decisions | `sources/election-results-data` |
| Cultural heritage / monuments | `sources/cultural-heritage-register` |
| Museum collections and objects (MuIS RDF) | `sources/muis-open-data` |
| Cultural grants and allocation rounds | `sources/kultuurkapital-grants-data` |
| Internal security annual reviews (KAPO) | `sources/internal-security-annual-reviews` |
| Consumer Disputes Committee decisions | `sources/consumer-technical-regulator-decisions` |
| Rescue incidents and emergency operations | `sources/rescue-incident-data` |
| Language-law supervision and annual activity reports | `sources/language-law-supervision` |
| Marital property registry | `sources/marital-property-register` |
| Patent and trademark registers | `sources/patent-and-trademark-registers` |
| Crime-policy studies, historical annual reports, selected research datasets | `sources/crime-policy-statistics` |
| Education registries and EHIS extracts | `sources/education-data` |
| Research projects/publications/institutions (ETIS) | `sources/etis-research-information-system` |
| Registered and approved food or feed business operators | `sources/food-business-approvals` |
| MFA development cooperation and humanitarian aid records | `sources/mfa-development-cooperation-aid` |
| Estonia-specific sanctions regulations and MFA subject-list links | `sources/mfa-sanctions` |
| Defence policy, budget, programme, and public-opinion documents | `sources/defence-policy-budget-documents` |
| Tourism information system dataset (andmed.eesti.ee) | `sources/tourism-information-system-dataset` |

## Routing notes

- Prefer source-specific skills over generic discovery when user intent is clear.
- Use `sources/open-data` first when the user gives only a vague topic.
- If a source is UI-only or access-controlled, pick the skill that includes human-guided export steps and continue from user-provided files.
