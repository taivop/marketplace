---
name: weather-data
description: Retrieve current Estonian weather observations and forecasts from Environment Agency XML feeds.
---

# Estonian Weather XML

## Access

Public XML feeds. No authentication. Send a normal user agent if Cloudflare rejects the default client.

## Endpoints

- Observations: https://www.ilmateenistus.ee/ilma_andmed/xml/observations.php
- English forecast: https://www.ilmateenistus.ee/ilma_andmed/xml/forecast.php?lang=eng
- Estonian forecast: https://www.ilmateenistus.ee/ilma_andmed/xml/forecast.php?lang=est

## Retrieve

1. Fetch observations for station measurements or forecasts for daily/night/day outlooks.
2. Parse XML; read the observation root `timestamp` as Unix time.
3. Select stations by `name`, `wmocode`, or coordinates.
4. Preserve missing/empty measurements rather than converting them to zero.

## Return

For observations keep station name/code, longitude, latitude, phenomenon, visibility, precipitation, pressure, humidity, temperature, wind direction/speed/gust, water level/temperature, UV, radiation fields, source URL, observation timestamp, and retrieval time. For forecasts keep date plus night/day place, phenomenon, temperature, wind, sea, and text fields present.

## Limits

- These feeds describe current observations and near-term forecasts, not a historical archive.
- Station fields vary by sensor availability.
- Forecast text and place labels depend on `lang`.

## Verify

Require HTTP 200 XML. Observations must have root `observations`, a numeric `timestamp`, and at least one `station` with `name`, coordinates, and a measurement field. Forecasts must have root `forecasts` and at least one dated `forecast` containing `night` and `day`.
