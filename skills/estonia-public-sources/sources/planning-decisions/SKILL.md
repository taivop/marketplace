---
name: planning-decisions
description: Query Estonia's national planning-register JSON API for plans, lifecycle status, authorities, geometry links, related plans, and public documents.
---

# Estonia Planning Decisions

## Access

- Application: `https://www.planeeringud.ee/plank-web/`
- API base: `https://www.planeeringud.ee/plank-web/api/`
- Public JSON requests require no authentication.

## Search

POST JSON to `planeering/otsing`; control the result page in the URL:

```http
POST /plank-web/api/planeering/otsing?page=0&size=25&sort=kehtestkp,desc
Content-Type: application/json

{"otsistring":"Vanalinna"}
```

`otsistring` is the verified free-text filter. The response is a Spring page with `content`, `totalElements`, `totalPages`, and page metadata. Search records include `sysid`, `planid`, `plannim`, abbreviated plan type, authority, lifecycle status, relevant dates, purpose, and map link.

## Detail

Fetch `GET planeering/{sysid}` using `sysid` from search results. Do not substitute `planid`; it is a different identifier and is not accepted by this route.

Return at least `sysid`, `planid`, name, type, status, organizing authority, purpose, lifecycle dates, `planviide`, `bbox`, related plans, and every public `planDokuments` item with its type, original filename, size, and `filePublicUrl`.

## Limits

- Status is lifecycle data. Keep the original `planseisNimi` or `klPlanseisByPlanseis`, and do not collapse draft, established, repealed, or paused plans.
- Search/export request bodies support more UI filters, but use only fields verified from the live application; use `otsistring` unless another exact filter contract has been checked.
- Document links may be PDF, ASiC-E, or another original file type.

## Verify

Require a paged JSON response, ensure detail `sysid` matches the selected search record, and accept documents only when `filePublicUrl` is present.
