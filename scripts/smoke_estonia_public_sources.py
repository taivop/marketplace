#!/usr/bin/env python3
"""Run content-level smoke checks for audited Estonia public-data recipes."""

from __future__ import annotations

import argparse
from http.cookiejar import CookieJar
import json
import re
import sys
from typing import Callable
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener, urlopen
import xml.etree.ElementTree as ET


USER_AGENT = "Mozilla/5.0 (compatible; estonia-public-sources-smoke/1.0)"


def fetch(
    url: str,
    *,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    limit: int = 4_000_000,
) -> tuple[bytes, str]:
    request_headers = {"User-Agent": USER_AGENT, **(headers or {})}
    request = Request(url, data=data, headers=request_headers)
    with urlopen(request, timeout=45) as response:
        if response.status != 200:
            raise AssertionError(f"HTTP {response.status}")
        return response.read(limit), response.headers.get_content_type()


def fetch_json(url: str, **kwargs: object) -> object:
    body, content_type = fetch(url, **kwargs)
    if content_type != "application/json":
        raise AssertionError(f"expected JSON, got {content_type}")
    return json.loads(body)


def statistics() -> None:
    url = "https://andmed.stat.ee/api/v1/en/stat/IA001"
    payload = {
        "query": [
            {
                "code": "Aasta",
                "selection": {"filter": "item", "values": ["2025"]},
            }
        ],
        "response": {"format": "json-stat2"},
    }
    data = fetch_json(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    assert isinstance(data, dict) and data.get("id") == ["Aasta"]
    assert data.get("size") == [1] and len(data.get("value", [])) == 1


def bank() -> None:
    query = urlencode(
        {
            "valuuta1": "USD",
            "valuuta2": "GBP",
            "aegAlg": "1.1.2010",
            "aegLopp": "7.1.2010",
            "lang": "et",
            "step": "DAY",
        }
    )
    data = fetch_json(
        f"https://statistika.eestipank.ee/spring/getValuutaKurssAjaloos?{query}",
        headers={
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://statistika.eestipank.ee/",
        },
    )
    assert isinstance(data, list) and len(data) == 4
    assert {"aeg", "kurss", "teade"} <= data[0].keys()


def legal_acts() -> None:
    data = fetch_json(
        "https://www.riigiteataja.ee/api/oigusakt_otsing/1/otsi"
        "?leht=1&limiit=2&pealkiri=riigieelarve"
    )
    assert isinstance(data, dict) and data.get("staatus") == "OK"
    assert data.get("aktid") and {"globaalID", "pealkiri", "url"} <= data["aktid"][0].keys()


def riigikogu() -> None:
    data = fetch_json(
        "https://api.riigikogu.ee/api/agenda/plenary"
        "?startDate=2025-01-01&endDate=2025-01-31&lang=EN"
    )
    assert isinstance(data, dict) and data.get("sittings")
    assert {"weekStartDate", "weekEndDate", "title", "sittings"} <= data.keys()
    assert {"uuid", "sittingDateTime", "agendaItems"} <= data["sittings"][0].keys()


def business_register() -> None:
    body, content_type = fetch(
        "https://avaandmed.ariregister.rik.ee/sites/default/files/avaandmed/"
        "ettevotja_rekvisiidid__lihtandmed.csv.zip",
        limit=4,
    )
    assert content_type in {"application/zip", "application/octet-stream"}
    assert body == b"PK\x03\x04"


def food_businesses() -> None:
    jar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar))
    home = Request(
        "https://jvis.agri.ee/jvis/avalik.html",
        headers={"User-Agent": USER_AGENT},
    )
    with opener.open(home, timeout=45) as response:
        assert response.status == 200
        response.read(1000)

    token = next(
        (cookie.value for cookie in jar if cookie.name == "XSRF-TOKEN"),
        None,
    )
    assert token
    payload = {
        "filter": {"kaitlejaNimi": "Selver"},
        "sort": [
            {"field": "kaitlejaNimi", "direction": "ascending"},
            {"field": "tegevuskohaNimi", "direction": "ascending"},
        ],
        "page": {"number": 1, "size": 2},
    }
    request = Request(
        "https://jvis.agri.ee/jvis/api/avalik/toidukaitleja/otsing",
        data=json.dumps(payload).encode(),
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
            "X-XSRF-TOKEN": token,
            "Referer": "https://jvis.agri.ee/jvis/avalik.html",
        },
    )
    with opener.open(request, timeout=45) as response:
        assert response.status == 200
        assert response.headers.get_content_type() == "application/json"
        data = json.load(response)
    assert isinstance(data.get("total"), int) and data["total"] > 0
    assert data.get("data")
    assert {
        "kaitlejaNimi",
        "kaitlejaIsikukoodRegkood",
        "tegevuskohaAadress",
    } <= data["data"][0].keys()


def legislation_workflow() -> None:
    body, content_type = fetch(
        "https://eelnoud.valitsus.ee/main/mount/share/home"
    )
    text = body.decode("utf-8", "replace")
    assert content_type == "text/html"
    assert "Eelnõude infosüsteem" in text
    assert "Avalikuks konsulteerimiseks esitatud eelnõud" in text
    assert "Kooskõlastamiseks esitatud eelnõud" in text
    assert "Vabariigi Valitsusele esitatud eelnõud" in text
    assert re.search(r">[A-ZÄÖÜÕ]{2,5}/\d{2}-\d{4}<", text)


def public_finance() -> None:
    body, content_type = fetch(
        "https://www.fin.ee/riigi-rahandus-ja-maksud/"
        "riigieelarve-ja-eelarvestrateegia/riigieelarved"
    )
    text = body.decode("utf-8", "replace")
    assert content_type == "text/html"
    assert "/sites/default/files/" in text and ".xlsx" in text


def tax_customs() -> None:
    body, content_type = fetch(
        "https://ncfailid.emta.ee/s/e4DneiWeKFfje6d/download/"
        "tasutud_maksud_kaesolev_aasta_eng.csv",
        limit=4096,
    )
    text = body.decode("utf-8-sig", "replace")
    assert content_type == "text/csv"
    assert '"Registry code"' in text and '"Data date"' in text


def weather() -> None:
    body, content_type = fetch(
        "https://www.ilmateenistus.ee/ilma_andmed/xml/observations.php"
    )
    root = ET.fromstring(body)
    assert content_type in {"text/xml", "application/xml"}
    assert root.tag == "observations" and root.get("timestamp", "").isdigit()
    station = root.find("station")
    assert station is not None and station.findtext("name")


def energy() -> None:
    data = fetch_json(
        "https://dashboard.elering.ee/api/nps/price"
        "?start=2026-07-01T00%3A00%3A00.000Z&end=2026-07-02T00%3A00%3A00.000Z"
    )
    assert isinstance(data, dict) and data.get("success") is True
    assert data.get("data", {}).get("ee")
    assert {"timestamp", "price"} <= data["data"]["ee"][0].keys()


def transport() -> None:
    data = fetch_json(
        "https://api.peatus.ee/routing/v1/routers/estonia/index/graphql",
        data=b'{"query":"{__typename}"}',
        headers={"Content-Type": "application/json"},
    )
    assert data == {"data": {"__typename": "QueryType"}}


def geospatial() -> None:
    body, _ = fetch(
        "https://kaart.maaamet.ee/wms/alus?SERVICE=WMS&REQUEST=GetCapabilities"
    )
    root = ET.fromstring(body)
    assert root.tag.endswith("Capabilities")
    assert any(element.tag.endswith("Name") and element.text for element in root.iter())


def tallinn() -> None:
    data = fetch_json(
        "https://avaandmed.tallinn.ee/data/"
        "?table=andurid_data&page=1&per_page=2"
    )
    assert isinstance(data, list) and data
    assert {"andurid_id", "name", "ts", "in", "out"} <= data[0].keys()


def tartu_documents() -> None:
    body, content_type = fetch(
        "https://info.raad.tartu.ee/dhs.nsf/dokreg?readform"
    )
    text = body.decode("utf-8", "replace")
    assert content_type == "text/html"
    assert "<title>Dokumendiregister</title>" in text
    for view in ("oigusaktid", "paevakorrad", "protokollid", "lepingud"):
        assert f"/dhs.nsf/{view}?SearchView" in text


def elections() -> None:
    body, content_type = fetch(
        "https://www.valimised.ee/sites/default/files/uploads/misc/"
        "RK2019_election_result_data.zip",
        limit=4,
    )
    assert content_type in {"application/zip", "application/octet-stream"}
    assert body == b"PK\x03\x04"


def open_data() -> None:
    body, content_type = fetch("https://andmed.eesti.ee/api/rss/feed")
    root = ET.fromstring(body)
    assert content_type in {"application/rss+xml", "application/xml", "text/xml"}
    items = root.findall("./channel/item")
    assert root.tag == "rss" and items
    assert items[0].findtext("title") and items[0].findtext("link")


def muis() -> None:
    body, content_type = fetch(
        "https://opendata.muis.ee/object/1522095",
        headers={"Accept": "application/rdf+xml"},
    )
    root = ET.fromstring(body)
    assert content_type == "application/rdf+xml"
    assert root.tag == "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF"
    assert list(root)


CHECKS: dict[str, Callable[[], None]] = {
    "bank-of-statistics": bank,
    "business-register-open-data": business_register,
    "election-results-data": elections,
    "energy-data": energy,
    "food-business-approvals": food_businesses,
    "geospatial-open-data": geospatial,
    "legal-acts-data": legal_acts,
    "legislation-workflow-eis": legislation_workflow,
    "muis-open-data": muis,
    "open-data": open_data,
    "public-finance-data": public_finance,
    "riigikogu-open-data": riigikogu,
    "statistics-api": statistics,
    "tallinn-open-data": tallinn,
    "tartu-document-register": tartu_documents,
    "tax-customs-data": tax_customs,
    "transport-traffic-data": transport,
    "weather-data": weather,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="*", choices=sorted(CHECKS))
    parser.add_argument("--list", action="store_true", help="List available checks")
    args = parser.parse_args()

    if args.list:
        print("\n".join(sorted(CHECKS)))
        return 0

    selected = args.sources or sorted(CHECKS)
    failures = 0
    for name in selected:
        try:
            CHECKS[name]()
            print(f"ok: {name}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"ERROR: {name}: {exc}", file=sys.stderr)

    if failures:
        print(f"failed with {failures} source check(s)", file=sys.stderr)
        return 1
    print(f"ok: {len(selected)} source smoke check(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
