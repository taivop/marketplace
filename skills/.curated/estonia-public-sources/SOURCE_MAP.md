# Source Map

This is the canonical routing catalog for both Codex and Claude. Every source recipe must appear here, and every path listed here must exist.

## Quick Chooser

| If user asks about... | Start with source skill(s) |
|---|---|
| "official stats", "time series", "national indicators", macro/financial statistics | `sources/statistics-api`, `sources/bank-of-statistics`, `sources/open-data` |
| Parliament votes, MPs, sittings, agendas, stenograms | `sources/riigikogu-open-data` |
| Draft law lifecycle and ministry coordination | `sources/legislation-workflow-eis`, `sources/riigikogu-draft-laws`, `sources/riigiteataja-draft-acts` |
| Final laws and legal texts | `sources/legal-acts-data` |
| President decisions and decrees | `sources/president-decisions-decrees` |
| Cabinet/government meeting agendas | `sources/government-session-agendas` |
| Government document trails and registries | `sources/ministry-document-registries`, `sources/government-office-document-register`, `sources/government-journal-records` |
| Government action programme tracking | `sources/government-action-programme` |
| Estonia 2035 action plan updates | `sources/estonia-2035-action-plan` |
| Registry of active strategic development documents | `sources/strategic-development-documents-registry` |
| Lobbying transparency | `sources/lobby-meetings` |
| Public consultations and participation windows | `sources/public-consultations-osale`, `sources/public-consultations-feed` |
| Procurement/tenders/contracts | `sources/procurement-data` |
| Procurement review disputes and supervisory actions | `sources/procurement-review`, `sources/procurement-state-supervision` |
| Party finance and party membership | `sources/party-funding-data`, `sources/political-party-membership` |
| State audits/constitutional oversight | `sources/state-audit-reports`, `sources/ombudsman-opinions` |
| Supreme Court and court case flows | `sources/supreme-court-judgments`, `sources/court-proceedings-data`, `sources/court-system-statistics` |
| Prosecution and police operational context | `sources/prosecution-statistics`, `sources/police-operational-statistics` |
| Justice case-flow analytics | `sources/e-file-statistics` |
| Prison system annual operations | `sources/prison-annual-reviews` |
| Official notices, insolvency announcements, summons | `sources/official-notices` |
| Business entities and company baseline data | `sources/business-register-open-data` |
| Property rights / land register | `sources/land-register-kinnistusraamat` |
| Licensed economic activity (MTR) | `sources/economic-activities-register-mtr` |
| State assets / state ownership | `sources/state-assets-register`, `sources/state-ownership-data` |
| State real-estate register open data (RKVR) | `sources/state-assets-register` |
| Agriculture support recipients / EU funded projects | `sources/agricultural-subsidies-pria`, `sources/eu-funded-projects` |
| Taxes and public tax inquiries | `sources/tax-customs-data`, `sources/tax-public-inquiries` |
| Budget, public finance, municipal benchmarking | `sources/public-finance-data`, `sources/local-government-finance-benchmarks` |
| State budget strategy (RES), annual budget packages, liabilities, investor relations, consolidated accounting | `sources/public-finance-data` |
| Public-sector workforce/admin statistics | `sources/public-sector-statistics-fin` |
| Civil-service pay governance and salary disclosure templates | `sources/civil-service-pay-governance` |
| Health stats, medicines, health supervision | `sources/health-statistics`, `sources/medicines-register`, `sources/health-supervision-decisions` |
| Communicable disease bulletins and vaccination monitoring | `sources/communicable-disease-bulletins`, `sources/vaccination-statistics` |
| Healthcare professional registration context | `sources/healthcare-professionals-register` |
| Health insurance financing and service volumes | `sources/health-insurance-fund-reports` |
| Medicines market and regulatory annual statistics | `sources/medicines-agency-statistics` |
| Welfare and unemployment | `sources/social-insurance-statistics`, `sources/unemployment-statistics`, `sources/health-welfare-open-data` |
| Environment, permits, weather | `sources/environmental-data`, `sources/environmental-permit-decisions`, `sources/weather-data` |
| Environmental charge supervision statistics | `sources/environmental-charge-statistics` |
| Forestry register records | `sources/forest-register` |
| Planning, construction, cadaster/geospatial | `sources/planning-decisions`, `sources/construction-register`, `sources/geospatial-open-data` |
| Transport/traffic and energy system operations | `sources/transport-traffic-data`, `sources/energy-data` |
| National public transport routes/stops and Peatus API | `sources/transport-traffic-data` |
| Vehicle, aircraft, ship, and port registry checks | `sources/vehicle-background-check`, `sources/aircraft-register`, `sources/ship-registers`, `sources/state-port-register`, `sources/e-ship-register-rik` |
| Published aviation safety reports | `sources/aviation-safety-reports` |
| Maritime economy indicators and fairway dues | `sources/maritime-economy-statistics`, `sources/fairway-dues` |
| Cyber incidents and digital government operations | `sources/cyber-incidents-cert-ee`, `sources/public-sector-it-systems-riha`, `sources/x-road-usage-statistics`, `sources/digital-government-studies` |
| e-Residency operational dashboard metrics | `sources/e-residency-dashboard` |
| Labour inspection statistics and enforcement | `sources/labour-inspectorate-statistics`, `sources/labour-inspectorate-enforcement` |
| Labour dispute committee process and outcomes context | `sources/work-dispute-committee` |
| Municipal operations (Tallinn/Tartu/VOLIS) | `sources/local-council-volis`, `sources/tallinn-open-data`, `sources/tallinn-legal-acts-register`, `sources/tallinn-council-documents`, `sources/tartu-open-data`, `sources/tartu-webaktid`, `sources/tartu-document-register` |
| Elections and political process outcomes | `sources/election-results-data` |
| National Electoral Committee (VVK) decisions | `sources/election-results-data` |
| Cultural heritage / monuments | `sources/cultural-heritage-register` |
| Museum collections and objects (MuIS RDF) | `sources/muis-open-data` |
| Cultural grants and allocation rounds | `sources/kultuurkapital-grants-data` |
| Historical governance archives | `sources/national-archives-governance-records` |
| Internal security annual reviews (KAPO) | `sources/internal-security-annual-reviews` |
| Consumer, competition, data-protection, financial supervision enforcement | `sources/consumer-technical-regulator-decisions`, `sources/competition-authority-decisions`, `sources/data-protection-enforcement`, `sources/financial-supervision-decisions` |
| State services catalog and public-service delivery | `sources/state-services-catalog` |
| Rescue incidents and emergency operations | `sources/rescue-incident-data` |
| Migration governance and published migration records | `sources/migration-management` |
| Language-law supervision and annual activity reports | `sources/language-law-supervision` |
| Civil-status and succession property registries | `sources/marital-property-register`, `sources/succession-register` |
| Patent and trademark registers | `sources/patent-and-trademark-registers` |
| Crime-policy statistical studies | `sources/crime-policy-statistics` |
| Education registries and EHIS extracts | `sources/education-data` |
| Research projects/publications/institutions (ETIS) | `sources/etis-research-information-system` |
| Animal-keeper registration process | `sources/animal-keeper-registering` |
| Food and plant supervision operations | `sources/food-supervision`, `sources/food-business-approvals`, `sources/plant-protection-supervision`, `sources/animal-disease-control` |
| MFA development cooperation and humanitarian aid records | `sources/mfa-development-cooperation-aid` |
| MFA sanctions implementation and sanctions backend endpoint | `sources/mfa-sanctions` |
| Defence public-opinion surveys | `sources/defence-public-opinion-surveys` |
| Defence policy/legal baseline and defence budget documents | `sources/defence-policy-budget-documents` |
| Tourism information system dataset (andmed.eesti.ee) | `sources/tourism-information-system-dataset` |

## Routing notes

- Prefer source-specific skills over generic discovery when user intent is clear.
- Use `sources/open-data` first when the user gives only a vague topic.
- If a source is UI-only or access-controlled, pick the skill that includes human-guided export steps and continue from user-provided files.
