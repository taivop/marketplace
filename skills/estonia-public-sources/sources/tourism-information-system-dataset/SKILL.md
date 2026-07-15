---
name: tourism-information-system-dataset
description: Retrieve current XLSX tourism inventory distributions from the official andmed.eesti.ee dataset API.
---

# Tourism Information System Dataset

Use this source for structured tourism inventory records published from puhkaeestis.ee and visitestonia.com.

## Endpoints

- Slug: `turismitoodete-ja-teenuste-andmed-puhkaeestis.ee-ja-visitestonia.com-eesti-riiklikus-turismiinfosusteemis`
- Metadata: `https://andmed.eesti.ee/api/datasets/slug/{slug}`
- Download URL: read each current `distributions[].accessUrls[0]` from metadata.

The canonical download pattern is `https://andmed.eesti.ee/api/v2/datasets/{datasetIdentifier}/distribution/{distribution_id}/file`. It redirects to an expiring signed object URL.

## Workflow

1. GET metadata with `Origin: https://andmed.eesti.ee` and require `status: COMPLETED`.
2. Select current XLSX distributions by `titleEn`. The dataset currently separates accommodation, culture/history, sauna/wellness, nature/active holiday, events, and food places.
3. Download from `accessUrls`; parse the workbook using its current headers.
4. Keep `datasetIdentifier`, distribution ID/title, `updatedAt`, canonical access URL, and retrieval time with each extract.

Never persist the redirected signed URL. Distribution IDs and workbook columns may change, so rediscover them from metadata on every run.

## Verification

- Metadata identifies organization `ettevotluse-ja-innovatsiooni-sihtasutus` and exposes multiple XLSX distributions with nonzero `byteSize`.
- A valid distribution begins with the ZIP/XLSX signature `PK\x03\x04`.
