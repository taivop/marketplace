---
name: government-journal-records
description: Query the Government Office's public Lotus Notes XML views for classified document series, dates, document numbers, subjects, and record details.
---

# Government Office Journal Records

## Access

- Series view: `GET https://dhs.riigikantselei.ee/avalikteave.nsf/byjournalkey?open`
- Public XML; no login or browser JavaScript is required.

## Retrieve

The root response is an `<entries>` document containing `<category>` rows. Follow a category's URL or send its exact label as the `path` parameter:

`?open&path=12-10%20Lepingud%20ja%20lepingutega%20seotud%20dokumendid`

Use `start` for pagination. Read `totalhits`, `start`, `count`, `from`, `to`, and the `next`/`end` links from `<entries>` rather than assuming a page size.

Category results contain `<document noteid="..." href="...">` rows and named `<field>` children. The root `fieldtitles` block maps field names to Estonian labels. Follow `/avalikteave.nsf/documents/<noteid>?open` for the public detail record.

## Return

- Preserve category path, `noteid`, detail URL, every named field, source URL, and retrieval time.
- Common fields include `date`, `docid`, `subject`, `from`, `receivedfrom`, `sentto`, document type, issuer, keywords, protocol number, meeting place, and contract dates.
- Keep absent fields null; available fields vary by document series.

## Limits

- This is an older Government Office document system and may overlap newer ADR records.
- Category labels have historical variants; do not merge them solely by numeric prefix.
- Detail records can omit restricted document content while retaining public metadata.

## Verify

- Require HTTP 200 `text/xml` whose root is `entries`, with category links and paging attributes.
- Require a known populated category to return document rows with `noteid`, `href`, `date`, `docid`, and `subject`.
