---
name: estonian-store-search
description: Search Estonian building supply stores (Bauhof, Ehituse ABC, Decora, K-Rauta, Bauhaus, Depo), grocery stores (Prisma, Rimi, Selver), home furnishing (IKEA), and second-hand marketplaces (Vinted, Yaga) for products, prices, and stock. USE WHEN user asks to find products at Estonian stores, compare prices across them, or check availability.
metadata:
  distribution:
    publish_anthropic: true
    plugin_name: estonian-store-search
    plugin_version: 0.5.1
    plugin_author: Taivo Marketplace
---


Run `curl` searches across stores in parallel. By default, filter out out-of-stock items.

Building supply stores: Bauhof, Ehituse ABC, Decora, K-Rauta, Bauhaus, Depo.
Grocery stores: Prisma, Rimi, Selver.
Home furnishing: IKEA.
Second-hand marketplaces: Vinted, Yaga.

## Verify every product link before returning it

Search APIs are candidate discovery, not final proof that a product page or its
availability is current. Before returning a product URL:

1. Open the final public URL, follow redirects, and verify that the rendered
   product name or stable identifier (SKU, EAN, item number) matches the search
   record. Also check the requested variant, dimensions, and pack size.
2. Reject 404 pages, generic storefront shells that never hydrate, product pages
   that say the item is unavailable, and pages that only show substitute items.
3. Let the detail page override a stale search index when price or availability
   conflicts. Record the date checked for price/stock comparisons.
4. Never invent a public URL from a slug or replace an API/staging hostname
   without applying the store-specific rule below and verifying the result.
5. Some sites block command-line clients. If `curl` reaches an anti-bot page or
   a JavaScript shell, use an available browser-capable tool and inspect the
   rendered title/name and availability. If no browser is available, omit the
   link or label it explicitly as unverified; do not call it verified.

For dynamic pages, an initial generic `<title>` is not sufficient. Wait for the
product view to render, then verify the visible product identity.

## Bauhof — Magento GraphQL

```bash
curl -s -X POST "https://www.bauhof.ee/api/magento/customQuery" \
  -H "Content-Type: application/json" \
  -d '{"query":"query{products(search:\"SEARCH_TERM\",pageSize:10){items{sku name stock_status price_range{minimum_price{final_price{value currency}regular_price{value currency}}}url_key}total_count}}","queryVariables":{}}'
```

Product URL: `https://www.bauhof.ee/et/p/{sku}/{url_key}`. The bare
`https://www.bauhof.ee/{url_key}` form redirects to the English site and can
produce a 404. Verify the rendered heading and `Tootekood` against `name` and
`sku`. Stock: `stock_status` (`IN_STOCK` / `OUT_OF_STOCK`); this is aggregate
availability, so use the detail page's purchase controls or store-availability
view when location-specific stock matters. Price: `final_price.value`.

## Ehituse ABC — Klevu Search

```bash
curl -s -X POST "https://eucs32v2.ksearchnet.com/cs/v2/search" \
  -H "Content-Type: application/json" \
  -d '{"context":{"apiKeys":["klevu-168180264665813326"]},"recordQueries":[{"id":"productSearch","typeOfRequest":"SEARCH","settings":{"query":{"term":"SEARCH_TERM"},"typeOfRecords":["KLEVU_PRODUCT"],"limit":10,"sort":"RELEVANCE"}}]}'
```

Product URL: `url`. Stock: `inStock` (`yes`/`no`). Price: `salePrice`. Results
in `queryResults[0].records`. Open the returned URL and verify its product name
or SKU before including it; Klevu records can outlive the storefront page.

## Decora — Klevu Search

```bash
curl -s -X POST "https://decoracsv2.ksearchnet.com/cs/v2/search" \
  -H "Content-Type: application/json" \
  -d '{"context":{"apiKeys":["klevu-159479682665411675"]},"recordQueries":[{"id":"productSearch","typeOfRequest":"SEARCH","settings":{"query":{"term":"SEARCH_TERM"},"typeOfRecords":["KLEVU_PRODUCT"],"limit":10,"sort":"RELEVANCE"}}]}'
```

Same response format as Ehituse ABC. Extra fields: `stock_availability` (store
locations), `volume_l`, `shortDesc`, `usage_indoor_outdoor`. Verify the returned
URL's rendered product name/SKU and do not rely on a successful HTTP status
alone, because some storefronts serve branded not-found pages with status 200.

## K-Rauta — LupaSearch

```bash
curl -s -X POST "https://api.lupasearch.com/v1/query/j9gky3z0nx3z" \
  -H "Content-Type: application/json" \
  -d '{"searchText":"SEARCH_TERM","limit":10}'
```

Results are in `.items[]` (the top level is an object with `items`, `facets`,
`filters`, `total`, and other search metadata). Useful fields include:

- Product name: `title.et`
- Relative product URL: `url.et` (join with `https://www.k-rauta.ee`)
- Product code: `product_code`
- Prices: `price_groups.default.price` and `price_groups.loyalty.price`
- Search availability hints: `in_stock`, `tags`, and `delivery_methods`

Do **not** treat `tags`, including `"in-shops"`, or `in_stock` as final stock
truth. Search records can remain positive while the rendered product page says
`Vabandame, antud toode pole hetkel saadaval` and shows substitutes. Open the
detail URL and exclude the item if that message appears or no purchase option is
available. Keep regular and loyalty prices clearly distinguished.

## Bauhaus — Magento REST (2-step)

Step 1 — search (returns product IDs):
```bash
curl -s "https://secure.qs-m2web.bauhaus.ee/rest/V1/search?searchCriteria[pageSize]=10&searchCriteria[requestName]=quick_search_container&searchCriteria[filterGroups][0][filters][0][field]=search_term&searchCriteria[filterGroups][0][filters][0][value]=SEARCH_TERM"
```

Step 2 — get details (entity IDs from step 1):
```bash
curl -s "https://secure.qs-m2web.bauhaus.ee/rest/V1/products-render-info?searchCriteria[filterGroups][0][filters][0][field]=entity_id&searchCriteria[filterGroups][0][filters][0][value]=ID1,ID2,ID3&searchCriteria[filterGroups][0][filters][0][condition_type]=in&storeId=13&currencyCode=EUR"
```

Results are in `.items[]`. Each item currently includes `name`,
`price_info.final_price`, `price_info.regular_price`, `is_salable`, `images`, and
`url`. The returned `url` may use the non-public
`https://headless-staging.bauhaus.ee` hostname. Build the public candidate by
keeping its path and using `https://www.bauhaus.ee`, then verify the rendered
page before returning it. Do not expose the staging URL.

`is_salable == "1"` means the item can be sold; it is not a quantity. The public
detail page may expose stronger signals such as `Laos (N)`, delivery status, and
Click & Collect availability. Command-line requests may receive a Vercel
security response, so use a browser-capable tool for verification when needed.

## Depo — GraphQL

```bash
curl -s 'https://online.depo.ee/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ products(searchString: \"SEARCH_TERM\", start: 0, rows: 10) { edges { node { id name primaryBarcode specificationBrand prices { yellow { priceWithVat unit } orange { priceWithVat priceQuantity unit } } stockItems { locationAddress quantity } } } } }"}'
```

Name, brand, barcode, and stock counters associated with Tallinn Veskiposti.
Two price tiers: `yellow` (retail), `orange` (bulk price with `priceQuantity`
threshold). Prices include 24% VAT.

Product URL: `https://online.depo.ee/product/{id}`. The page is client-rendered,
so wait for hydration and verify the visible name/barcode. DEPO's product page
explicitly says its availability information applies to online orders and does
not guarantee the corresponding quantity in the physical store. Report
`stockItems.quantity` as online availability associated with the location, not
as confirmed shelf stock. The detail page's `Saadaval`/purchase state is the
final online-availability check.

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

## IKEA (home furnishing) — Search API

```bash
curl -s "https://sik.search.blue.cdtapps.com/ee/et/search-result-page?types=PRODUCT&q=SEARCH_TERM&size=10&c=sr&v=20240110" \
  -H "User-Agent: Mozilla/5.0"
```

Results in `searchResultPage.products.main.items[].product`. Per product: `name`, `typeName` (e.g. "Põrandalamp"), `itemMeasureReferenceText` (size), `id`/`itemNo` (article number), `pipUrl` (product URL), `mainImageUrl`. Price: `salesPrice.numeral` + `salesPrice.currencyCode` (EUR, incl. VAT). The search response's `availability[]` is coarse (delivery flags only); for real stock use the availability API below. Total hit count is `searchResultPage.products.badge`.

### IKEA — in-store + delivery stock

For actual stock, query the availability API with the `itemNo` from search. The Tallinn store (the only IKEA in Estonia) is store id **648**.

```bash
curl -s "https://api.salesitem.ingka.com/availabilities/ru/ee?itemNos=ITEM_NO&expand=StoresList,Restocks,SalesLocations" \
  -H "X-Client-ID: ef382663-a2a5-40d4-8afe-f0634821c0ed" \
  -H "Accept: application/json;version=2" \
  -H "User-Agent: Mozilla/5.0"
```

Results in `availabilities[]`, one entry per store (`classUnitKey.classUnitType` == `STO`, `classUnitCode` == store id; `648` = Tallinn). Per store:
- `availableForCashCarry` — whether it can be bought in-store now.
- `buyingOption.cashCarry.availability.quantity` — units physically in the Tallinn store.
- `buyingOption.cashCarry.availability.probability.thisDay.messageType` — `HIGH_IN_STOCK` / `LOW_IN_STOCK` / `OUT_OF_STOCK` (with a colour token).
- `buyingOption.homeDelivery.range.inRange` — whether home delivery is offered.

Pass multiple `itemNos` comma-separated. `X-Client-ID` is the public web key from the IKEA storefront; the `Accept: application/json;version=2` header is required.

## Vinted (second-hand marketplace) — catalog API (2-step)

The API needs an anonymous session cookie. Fetch the homepage once to get cookies, then call the catalog endpoint with them.

Step 1 — get a session cookie:
```bash
curl -s -c /tmp/vinted_cookies.txt -o /dev/null \
  "https://www.vinted.ee/" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
```

Step 2 — search the catalog:
```bash
curl -s -b /tmp/vinted_cookies.txt \
  "https://www.vinted.ee/api/v2/catalog/items?search_text=SEARCH_TERM&per_page=10&order=newest_first" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" \
  -H "Accept: application/json"
```

Results in `items[]`. Per item: `title`, `brand_title`, `size_title`, `status` (condition in Estonian, e.g. "Hea"/"Rahuldav"), `price.amount` + `price.currency_code` (EUR), `path` (append to `https://www.vinted.ee` for the product URL), `photo.url`, `user.login`. Total hit count is `pagination.total_entries` (`pagination.total_pages` for paging via `&page=N`). `order` accepts `newest_first`, `price_low_to_high`, `price_high_to_low`, `relevance`. A real `User-Agent` is required or the request is blocked. Everything is second-hand/used; there is no "stock" — an item is either listed or sold.

## Yaga (second-hand marketplace) — search API

```bash
curl -s "https://www.yaga.ee/api/product/search/?query=SEARCH_TERM&offset=0&limit=60" \
  -H "User-Agent: Mozilla/5.0" -H "Accept: application/json"
```

Note the **trailing slash** on `/search/` and the param name **`query`** (not `q`). No cookie or auth needed. Do NOT use `/api/product` — that is a generic popularity feed that ignores the query and always returns the same listings.

Results in `data.list[]`. `data.total` is the real match count; `data.searchEngine` names the backend (e.g. `legacy-postgres`). Per item: `brand`, `price` (EUR, incl. VAT), `size`, `slug`, `shop.activeSlug`, `likeCount`, `images[].gallery` (image URL, also `?s=600`/`?s=300` size variants). Product URL: `https://www.yaga.ee/{shop.activeSlug}/product/{slug}`. Page with `offset` (multiples of `limit`).

Listings have no free-text title/description field — they are brand + size + attributes + photos — so matching is on brand/category, not a title string. Gibberish queries correctly return `total: 0`. The search item's own `brand` field is often `null`/unreliable; treat the query term as the brand.

### Filtering the search (avoid the womenswear/off-palette trap)

The search payload has **no category, colour, or gender** per item, so a bare brand query mixes in women's and off-palette listings. Two complementary tools:

1. **Server-side filters** — append as URL-encoded **JSON int-arrays**, format `key=[1,2]` (a wrong format returns a `VALIDATION_ERROR` naming the param + expected shape, which is how to discover more). Working keys: `colors`, `materials`, `brands`, `conditions`. Example (navy+grey+brown wool): `&colors=[9,11,14]&materials=[16]`. The `categories` key exists but uses a bespoke nested union that resisted reverse-engineering — **don't filter by category server-side**; post-filter via the detail API instead.

2. **Detail API** — `https://www.yaga.ee/api/product/{slug}/` (or `/{id}/`) returns the rich fields the search omits: `description` (the only human text — has brand/cut/measurements/colour), `categoryId`, `categoriesMap` (root→leaf path, e.g. `[2,471]`), `colors`, `materials`, `condition.namesMultilang.en`. **Gender = `categoriesMap[0]`: men's `2`, women's `1`, kids `3`.** Pipeline that works: brand query + `colors=[palette]` server-side → fetch each hit's detail (parallelise) → keep `categoriesMap[0]==2` and the leaf categories you want → read `description` to confirm.

### Taxonomy lookups (id ⇄ name)

- `https://www.yaga.ee/api/category/` — full tree; top level is flat, children nest under each node's `categories` key. Men (`2`) leaves incl.: knits `298`, shirts `167`, tees `168`, jeans `300`, trousers `301`, dress-trousers `372`, blazers `306`, coats `305`, suits `471`, loafers/shoes `312`, sneakers `318`, belts `323`.
- `https://www.yaga.ee/api/color/` — colour ids. Palette-relevant: black `1`, blue `3`, navy `9`, grey `11`, white `13`, brown `14`, light-brown `15`, cream `16`, khaki `19`.
- `https://www.yaga.ee/api/brand/` — brand id→name (needed for the `brands` filter).
