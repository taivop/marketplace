#!/usr/bin/env python3
"""Run content-level smoke checks for audited Estonia public-data recipes."""

from __future__ import annotations

import argparse
from html import unescape
from http.cookiejar import CookieJar
import json
import re
import sys
from typing import Callable
from urllib.parse import urlencode, urljoin
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


def state_ownership() -> None:
    body, content_type = fetch(
        "https://www.fin.ee/en/public-procurement-state-aid-and-assets/"
        "state-assets/state-stakeholdings"
    )
    text = body.decode("utf-8", "replace")
    assert content_type == "text/html"
    assert "State-owned companies" in text and "Share of state" in text
    assert "Foundations" in text and "AS ALARA" in text
    assert re.search(r"As of (?:December|the end of) 20\d{2}", text)


def communicable_diseases() -> None:
    page_url = (
        "https://www.terviseamet.ee/en/communicable-diseases/statistics/"
        "communicable-disease-bulletins"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    links = re.findall(r'href="([^"]+\.pdf[^"]*)"', text, re.IGNORECASE)
    bulletin_links = [link for link in links if "EEpiR" in link]
    assert content_type == "text/html" and len(bulletin_links) >= 12
    pdf, pdf_type = fetch(urljoin(page_url, bulletin_links[0]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def health_supervision() -> None:
    page_url = "https://www.terviseamet.ee/ettekirjutused"
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    links = re.findall(r'href="([^"]+\.pdf[^"]*)"', text, re.IGNORECASE)
    precepts = [link for link in links if "ettekirjutus" in link.lower()]
    assert content_type == "text/html" and len(precepts) >= 5
    pdf, pdf_type = fetch(urljoin(page_url, precepts[0]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def healthcare_professionals() -> None:
    data = fetch_json(
        "https://medre.tehik.ee/api-common/public/persons/filter",
        data=b'{"page":0,"size":2}',
        headers={"Content-Type": "application/json"},
    )
    assert isinstance(data, dict) and data.get("content")
    assert {"page", "size", "totalElements", "totalPages"} <= data.keys()
    assert {
        "id",
        "firstName",
        "lastName",
        "occupationCodes",
        "specialities",
    } <= data["content"][0].keys()


def vaccinations() -> None:
    body, content_type = fetch(
        "https://www.terviseamet.ee/en/nakkushaigused/statistika/vaktsineerimine"
    )
    text = body.decode("utf-8", "replace")
    assert content_type == "text/html"
    assert "Covid-19vaccination/Vaccinationmap" in text
    assert "Influenzavaccination/Mapview" in text

    csv, csv_type = fetch(
        "https://tableauapp.tehik.ee/t/Terviseamet/views/"
        "Influenzavaccination/Mapview.csv?:showVizHome=no"
    )
    rows = csv.decode("utf-8-sig", "replace").splitlines()
    assert csv_type == "text/csv" and len(rows) >= 2
    assert "Coverage" in rows[0] and "202" in rows[1]


def marital_property() -> None:
    params = {
        "SearchFilter.AlgusKp": "01.01.2025",
        "SearchFilter.LoppKp": "31.01.2025",
        "SearchFilter.Kehtivad": "true",
        "SearchFilter.Suletud": "true",
        "SearchFilter.VarasuhteLiik.VaralahutusStat": "true",
        "SearchFilter.VarasuhteLiik.VarayhisusStat": "true",
        "SearchFilter.VarasuhteLiik.VaraJuurdekasvuStat": "true",
        "SearchFilter.VarasuhteLiik.ValisriigiOiguseStat": "true",
        "SearchFilter.Dokumendid.AbiellumisAvaldus": "true",
        "SearchFilter.Dokumendid.Abieluvaraleping": "true",
        "SearchFilter.Dokumendid.Kohtulahend": "true",
        "SearchFilter.Dokumendid.Kooseluleping": "true",
        "SearchFilter.Dokumendid.MuuDokument": "true",
    }
    body, content_type = fetch(
        "https://abieluvararegister.rik.ee/Statistika/Otsi?" + urlencode(params),
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://abieluvararegister.rik.ee/Statistika",
        },
    )
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert "01.01.2025 - 31.01.2025" in text
    assert "Kehtivaid kaarte kokku" in text and "Suletud kaarte kokku" in text
    assert "Varalahusus" in text and "Varaühisus" in text


def ministry_documents() -> None:
    body, content_type = fetch(
        "https://adr.rik.ee/jm/kiirotsing",
        data=urlencode({"input": "riigieelarve", "pageNumber": "1"}).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    text = body.decode("utf-8", "replace")
    assert content_type == "text/html"
    for heading in ("Viit", "Reg. kpv", "Pealkiri", "Dokumendi liik"):
        assert heading in text
    assert re.search(r'/jm/dokument/\d+', text)
    assert "riigieelarve" in text.lower()


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


def maritime_economy() -> None:
    body, content_type = fetch(
        "https://public.tableau.com/views/Surveyofmaritimeeconomy/"
        "THEIMPACTOFTHEMARITIMESECTORONTHEESTONIANECONOMY.csv"
        "?:showVizHome=no"
    )
    text = body.decode("utf-8-sig", "replace")
    assert content_type == "text/csv"
    header, *rows = text.splitlines()
    assert rows and "sektor" in header
    assert "MÜÜGITULU" in header and "TÖÖTAJATE ARV" in header


def state_ports() -> None:
    settings = fetch_json("https://www.sadamaregister.ee/settings")
    assert isinstance(settings, dict) and settings.get("ApiBaseUrl")
    ports = fetch_json(settings["ApiBaseUrl"] + "/ports/public-active")
    assert isinstance(ports, list) and ports
    assert {
        "publicId",
        "name",
        "address",
        "bodyOfWaterName",
        "additionalServices",
    } <= ports[0].keys()


def riha() -> None:
    data = fetch_json("https://www.riha.ee/api/v1/systems?page=0&size=2")
    assert isinstance(data, dict) and data.get("content")
    assert {"totalElements", "size", "page", "totalPages"} <= data.keys()
    details = data["content"][0].get("details", {})
    assert {"name", "uuid", "owner", "meta", "purpose"} <= details.keys()


def x_road() -> None:
    current = fetch_json("https://x-tee.ee/stats/EE/environmentData.json")
    assert isinstance(current, dict) and current.get("instanceIdentifier") == "EE"
    assert re.fullmatch(r"20\d{2}-\d{2}-\d{2}", current.get("date", ""))
    assert all(current.get(key, 0) > 0 for key in ("members", "subsystems", "securityServers"))
    assert current.get("memberClasses")

    history = fetch_json("https://x-tee.ee/stats/EE/history.json")
    assert isinstance(history, list) and len(history) >= 12
    assert {"date", "members", "subsystems", "securityServers"} <= history[-1].keys()


def cyber_incidents() -> None:
    page_url = (
        "https://www.ria.ee/en/cyber-security/cyberspace-analysis-and-prevention/"
        "situation-cyberspace"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert "Monthly summaries 2026" in text and "Quarterly Assessments 2023" in text
    assert "Cyber Security in Estonia 2026" in text
    pdf_links = re.findall(r'href="([^"]+\.pdf[^"]*)"', text, re.IGNORECASE)
    situation_pdfs = [link for link in pdf_links if "situation" in link.lower()]
    assert len(situation_pdfs) >= 12
    pdf, pdf_type = fetch(urljoin(page_url, situation_pdfs[0]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def ria_studies() -> None:
    page_url = (
        "https://www.ria.ee/en/authority-news-and-contact/news-media-contact/"
        "studies-analyses-overviews"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert len(re.findall(r'id="datatable-[^"]+"', text)) >= 3
    encoded_links = re.findall(
        r'https:\\/\\/www\.ria\.ee\\/[^" ]+\.pdf',
        text,
    )
    pdf_links = [link.replace(r"\/", "/") for link in encoded_links]
    assert len(set(pdf_links)) >= 10
    pdf, pdf_type = fetch(pdf_links[0], limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def lobby_meetings() -> None:
    page_url = (
        "https://www.riigikantselei.ee/asutus-uudised-ja-kontakt/lobitegevus/"
        "lobistidega-kohtumised"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    links = re.findall(r'href="([^"]+\.xlsx[^"]*)"', text, re.IGNORECASE)
    assert content_type == "text/html" and len(links) >= 4
    workbook, workbook_type = fetch(urljoin(page_url, links[0]), limit=4)
    assert workbook_type in {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/octet-stream",
    }
    assert workbook == b"PK\x03\x04"


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
    "communicable-disease-bulletins": communicable_diseases,
    "cyber-incidents-cert-ee": cyber_incidents,
    "digital-government-studies": ria_studies,
    "election-results-data": elections,
    "energy-data": energy,
    "food-business-approvals": food_businesses,
    "geospatial-open-data": geospatial,
    "health-supervision-decisions": health_supervision,
    "healthcare-professionals-register": healthcare_professionals,
    "legal-acts-data": legal_acts,
    "legislation-workflow-eis": legislation_workflow,
    "lobby-meetings": lobby_meetings,
    "marital-property-register": marital_property,
    "maritime-economy-statistics": maritime_economy,
    "ministry-document-registries": ministry_documents,
    "muis-open-data": muis,
    "open-data": open_data,
    "public-finance-data": public_finance,
    "public-sector-it-systems-riha": riha,
    "riigikogu-open-data": riigikogu,
    "statistics-api": statistics,
    "state-ownership-data": state_ownership,
    "state-port-register": state_ports,
    "tallinn-open-data": tallinn,
    "tartu-document-register": tartu_documents,
    "tax-customs-data": tax_customs,
    "transport-traffic-data": transport,
    "vaccination-statistics": vaccinations,
    "weather-data": weather,
    "x-road-usage-statistics": x_road,
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
