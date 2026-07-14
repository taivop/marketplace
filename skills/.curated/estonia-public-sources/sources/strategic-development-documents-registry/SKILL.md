---
name: strategic-development-documents-registry
description: Retrieve the Government Office table of active strategic development documents with publication dates, PDF downloads, and legal references.
---

# Strategic Development Documents Registry

## Access

- Page: `https://www.valitsus.ee/strateegia-eesti-2035-arengukavad-ja-planeering/strateegilised-arengudokumendid/kehtivad`
- No authentication is required.

## Retrieve

1. Fetch the page HTML.
2. Find `script` elements whose `type` is `application/json` and whose generated `id` starts with `datatable-`.
3. JSON-decode the block that is an array of rows. Ignore the separate datatable configuration object.
4. Parse each three-cell row as title/file metadata HTML, publication-date HTML, and an action link.
5. Extract the anchor text and `href`, the `time[datetime]` value, file size/format when present, and whether the URL is a Government Office file or a Riigi Teataja legal reference.

## Return

Return the source page, title, publication timestamp, document URL, URL type (`file` or `riigiteataja`), file format/size when present, and retrieval time. Preserve the absolute host supplied by the row; both bare and `www` host forms may occur.

## Limits

- This is the current active-document registry, not a complete historical archive.
- Rows are HTML strings inside JSON, so JSON-decode before parsing their HTML.
- The generated datatable ID and file hostname can change when the page is republished; do not hard-code either.

## Verify

Require a non-empty three-column row array, working PDF links with PDF signatures, and at least one `riigiteataja.ee` reference before treating the table as the registry.
