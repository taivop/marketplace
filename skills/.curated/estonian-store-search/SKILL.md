---
name: estonian-store-search
description: Search Estonian building supply stores (Bauhof, Ehituse ABC, Decora, K-Rauta, Bauhaus, Depo) and grocery stores (Prisma, Rimi, Selver) for products, prices, and stock. USE WHEN user asks to find products at Estonian stores, compare prices across them, or check availability.
metadata:
  distribution:
    tier: curated
    publish_anthropic: true
    plugin_name: estonian-store-search
    plugin_version: 0.2.0
    plugin_author: Taivo Marketplace
---


Run `curl` searches across stores in parallel. By default, filter out out-of-stock items.

Building supply stores: Bauhof, Ehituse ABC, Decora, K-Rauta, Bauhaus, Depo.
Grocery stores: Prisma, Rimi, Selver.

## Bauhof — Magento GraphQL

```bash
curl -s -X POST "https://www.bauhof.ee/api/magento/customQuery" \
  -H "Content-Type: application/json" \
  -d '{"query":"query{products(search:\"SEARCH_TERM\",pageSize:10){items{sku name stock_status price_range{minimum_price{final_price{value currency}regular_price{value currency}}}url_key}total_count}}","queryVariables":{}}'
```

Product URL: `https://www.bauhof.ee/{url_key}`. Stock: `stock_status` (`IN_STOCK` / `OUT_OF_STOCK`). Price: `final_price.value`.

## Ehituse ABC — Klevu Search

```bash
curl -s -X POST "https://eucs32v2.ksearchnet.com/cs/v2/search" \
  -H "Content-Type: application/json" \
  -d '{"context":{"apiKeys":["klevu-168180264665813326"]},"recordQueries":[{"id":"productSearch","typeOfRequest":"SEARCH","settings":{"query":{"term":"SEARCH_TERM"},"typeOfRecords":["KLEVU_PRODUCT"],"limit":10,"sort":"RELEVANCE"}}]}'
```

Product URL: `url`. Stock: `inStock` (`yes`/`no`). Price: `salePrice`. Results in `queryResults[0].records`.

## Decora — Klevu Search

```bash
curl -s -X POST "https://decoracsv2.ksearchnet.com/cs/v2/search" \
  -H "Content-Type: application/json" \
  -d '{"context":{"apiKeys":["klevu-159479682665411675"]},"recordQueries":[{"id":"productSearch","typeOfRequest":"SEARCH","settings":{"query":{"term":"SEARCH_TERM"},"typeOfRecords":["KLEVU_PRODUCT"],"limit":10,"sort":"RELEVANCE"}}]}'
```

Same response format as Ehituse ABC. Extra fields: `stock_availability` (store locations), `volume_l`, `shortDesc`, `usage_indoor_outdoor`.

## K-Rauta — LupaSearch

```bash
curl -s -X POST "https://api.lupasearch.com/v1/query/j9gky3z0nx3z" \
  -H "Content-Type: application/json" \
  -d '{"searchText":"SEARCH_TERM","limit":10}'
```

Returns name, price, URL, product code, brand, categories, images. Results in top-level array. Stock: items with `tags: []` are out of stock; in-stock items have tags like `"in-warehouse"`, `"online-only"`, or `"new-product"`.

## Bauhaus — Magento REST (2-step)

Step 1 — search (returns product IDs):
```bash
curl -s "https://secure.qs-m2web.bauhaus.ee/rest/V1/search?searchCriteria[pageSize]=10&searchCriteria[requestName]=quick_search_container&searchCriteria[filterGroups][0][filters][0][field]=search_term&searchCriteria[filterGroups][0][filters][0][value]=SEARCH_TERM"
```

Step 2 — get details (entity IDs from step 1):
```bash
curl -s "https://secure.qs-m2web.bauhaus.ee/rest/V1/products-render-info?searchCriteria[filterGroups][0][filters][0][field]=entity_id&searchCriteria[filterGroups][0][filters][0][value]=ID1,ID2,ID3&searchCriteria[filterGroups][0][filters][0][condition_type]=in&storeId=13&currencyCode=EUR"
```

Returns name (from image label), price, image URLs. No stock status, no product URL slug, no description.

## Depo — GraphQL

```bash
curl -s 'https://online.depo.ee/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ products(searchString: \"SEARCH_TERM\", start: 0, rows: 10) { edges { node { id name primaryBarcode specificationBrand prices { yellow { priceWithVat unit } orange { priceWithVat priceQuantity unit } } stockItems { locationAddress quantity } } } } }"}'
```

Name, brand, barcode, per-store stock quantities (1 Estonian store: Tallinn Veskiposti). Two price tiers: `yellow` (retail), `orange` (bulk/loyalty with `priceQuantity` threshold). Prices include 24% VAT.

## Prisma (grocery) — GraphQL

Search is store-specific, so pick a `storeId` first:
```bash
curl -s -X POST "https://graphql-api.prismamarket.ee" \
  -H "Content-Type: application/json" -H "x-client-name: skaupat-web" \
  -d '{"query":"{ stores{ id name } }"}'
```
Stores (as of 2026-06): Mustamäe `542855267`, Annelinna `697951770`, Sikupilli `613763242`, Lasnamäe `660914326`, Rocca Al Mare `634972293`, Sõbra (Tartu) `685847808`, Kristiine `542860184`. Default to Mustamäe if unspecified.

Then search:
```bash
curl -s -X POST "https://graphql-api.prismamarket.ee" \
  -H "Content-Type: application/json" -H "x-client-name: skaupat-web" \
  -d '{"variables":{"storeId":"542855267","queryString":"SEARCH_TERM","limit":10,"from":0},"query":"query($storeId: ID!, $queryString: String!, $limit: Int, $from: Int){ store(id:$storeId){ products(queryString:$queryString, limit:$limit, from:$from){ total items{ ean name brandName price priceUnit comparisonPrice comparisonUnit slug } } } }"}'
```
Results in `data.store.products.items`. `price` (per `priceUnit`, e.g. KPL/KG), `comparisonPrice` per `comparisonUnit` (e.g. €/L). Product URL: `https://www.prismamarket.ee/et/tuote/{slug}/{ean}`. Prices include VAT. `total` is the full hit count for pagination via `from`.

Single product details — root field `product(id, storeId)` where `id` is the EAN:
```bash
curl -s -X POST "https://graphql-api.prismamarket.ee" \
  -H "Content-Type: application/json" -H "x-client-name: skaupat-web" \
  -d '{"variables":{"storeId":"542855267","id":"EAN"},"query":"query($storeId: ID!, $id: ID!){ product(id:$id, storeId:$storeId){ ean name brandName price priceUnit comparisonPrice comparisonUnit slug productType countryName{ et } description ingredientStatement } }"}'
```
Adds `description`, `ingredientStatement` (ingredients), `countryName{ et }` (country of origin) on top of the search fields.

## Rimi (grocery) — server-rendered search page

```bash
curl -s "https://www.rimi.ee/epood/ee/otsing?query=SEARCH_TERM&pageSize=80"
```
Returns an HTML page (locale `ee`, not `et`). Each product card embeds JSON:
`data-gtm-eec-product='{"id":"200280","name":"...","price":1.39,"currency":"EUR"}'`.
Extract those with grep/regex. Product URL: the `href` of the sibling `<a class="card__url" ...>` (pattern `/epood/ee/tooted/.../p/{id}`). Per-unit price (e.g. `0,93 €/l`) is in the card text. Out-of-stock cards carry an `out-of-stock` class. `pageSize` controls result count (80 works); page through with `&page=N`.

For lightweight autocomplete (max 5 results) instead:
```bash
curl -s "https://www.rimi.ee/epood/api/v1/search/suggestions/products?query=SEARCH_TERM" \
  -H "X-Requested-With: XMLHttpRequest"
```

Single product details — fetch the product page and parse its JSON-LD:
```bash
curl -s "https://www.rimi.ee/epood/ee/tooted/.../p/PRODUCT_ID"
```
The `<script type="application/ld+json">` block gives `name`, `description`, `sku`, `image`, `offers.price`, `offers.priceCurrency`, `offers.availability` (`InStock`/`OutOfStock`). Ingredients live in the HTML under the "Koostisosad" heading (no clean JSON — parse the section if needed).

## Selver (grocery) — Klevu Search

```bash
curl -s -X POST "https://eucs3v2.ksearchnet.com/cs/v2/search" \
  -H "Content-Type: application/json" \
  -d '{"context":{"apiKeys":["klevu-14410928010151845"]},"recordQueries":[{"id":"productSearch","typeOfRequest":"SEARCH","settings":{"query":{"term":"SEARCH_TERM"},"typeOfRecords":["KLEVU_PRODUCT"],"limit":10,"sort":"RELEVANCE"}}]}'
```

Same Klevu response format as Ehituse ABC / Decora. Results in `queryResults[0].records`; `totalResultsFound` for paging (via `offset` in settings). Per record: `name`, `sku`, `price`/`salePrice`, `inStock` (`yes`/`no`), `url` (full product URL), `image`, `klevu_category`.

Single product details — fetch the product page (`url` from the search record) and parse the server-rendered HTML:
```bash
curl -s "PRODUCT_URL"
```
No JSON-LD; ingredients are under the "Koostisosad" heading and the marketing copy under the description section. Price/stock/name are already in the Klevu record, so only hit the page when you need ingredients or description.
