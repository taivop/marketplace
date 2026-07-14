#!/usr/bin/env python3
"""Run content-level smoke checks for audited Estonia public-data recipes."""

from __future__ import annotations

import argparse
import base64
from html import unescape
from http.cookiejar import CookieJar
import json
import re
import subprocess
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


def fetch_with_curl(
    url: str,
    *,
    headers: dict[str, str] | None = None,
) -> tuple[bytes, str]:
    # Some legacy government hosts omit intermediates that urllib's CA bundle expects.
    command = [
        "curl",
        "--fail",
        "--location",
        "--silent",
        "--show-error",
        "--max-time",
        "45",
        "--user-agent",
        USER_AGENT,
    ]
    for name, value in (headers or {}).items():
        command.extend(["--header", f"{name}: {value}"])
    command.extend(["--write-out", "\n%{content_type}", url])
    output = subprocess.check_output(command)
    body, content_type = output.rsplit(b"\n", 1)
    return body, content_type.decode().split(";", 1)[0]


def embedded_file_urls(text: str, host: str, extension: str) -> list[str]:
    encoded = re.findall(
        rf'https:\\/\\/{re.escape(host)}\\/[^" ]+\.{re.escape(extension)}',
        text,
    )
    return [url.replace(r"\/", "/") for url in encoded]


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
    pdf_links = embedded_file_urls(text, "www.ria.ee", "pdf")
    prelive_links = embedded_file_urls(text, "ria.prelive.vportal.ee", "pdf")
    pdf_links.extend(
        link.replace("https://ria.prelive.vportal.ee/", "https://www.ria.ee/")
        for link in prelive_links
    )
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


def government_journal() -> None:
    query = urlencode(
        {"open": "", "path": "12-10 Lepingud ja lepingutega seotud dokumendid"}
    )
    body, content_type = fetch_with_curl(
        "https://dhs.riigikantselei.ee/avalikteave.nsf/byjournalkey?" + query
    )
    root = ET.fromstring(body)
    assert content_type == "text/xml" and root.tag == "entries"
    assert int(root.get("totalhits", "0")) > 0
    document = root.find("document")
    assert document is not None and document.get("noteid") and document.get("href")
    fields = {field.get("name"): field.text or "" for field in document.findall("field")}
    assert {"date", "docid", "subject"} <= fields.keys()


def government_agendas() -> None:
    query = urlencode(
        {
            "query": "Istungi päevakord",
            "filters[type]": "Uudis",
            "sort_by": "created",
            "page": 1,
            "limit": 2,
            "langcode": "et",
            "timezone": "Europe/Tallinn",
        }
    )
    body, content_type = fetch_with_curl(
        "https://search.service.eu-live.vportal.ee/v1/search/valitsus?" + query,
        headers={"Origin": "https://valitsus.ee", "Referer": "https://valitsus.ee/"},
    )
    assert content_type == "application/json"
    data = json.loads(body)
    response = data.get("response", {}) if isinstance(data, dict) else {}
    assert response.get("numFound", 0) > 0 and response.get("docs")
    assert {"title", "uri", "created", "content"} <= response["docs"][0].keys()
    assert any(
        "istungi" in item["title"].lower() and "päevakord" in item["title"].lower()
        for item in response["docs"]
    )


def government_action_programme() -> None:
    body, content_type = fetch(
        "https://www.valitsus.ee/valitsuse-eesmargid-ja-tegevused/"
        "valitsemise-alused/tegevusprogramm-0"
    )
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert text.count("https://app.powerbi.com/view?") >= 2
    assert "pageName=06bb907844ed3bab3769" in text
    assert "pageName=80b7f5658c06fa5ad0c1" in text
    assert "töödeldaval kujul" in text


def estonia_2035() -> None:
    body, content_type = fetch(
        "https://www.valitsus.ee/strateegia-eesti-2035-arengukavad-ja-planeering/"
        "eesti-2035-tegevuskava"
    )
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html" and 'type="application/json" id="datatable-' in text
    pdf_links = embedded_file_urls(text, "www.valitsus.ee", "pdf")
    assert len(set(pdf_links)) >= 3
    pdf, pdf_type = fetch(pdf_links[0], limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def strategic_documents() -> None:
    page_url = (
        "https://www.valitsus.ee/strateegia-eesti-2035-arengukavad-ja-planeering/"
        "strateegilised-arengudokumendid/kehtivad"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html" and 'type="application/json" id="datatable-' in text
    blocks = re.findall(
        r'<script[^>]+type="application/json"[^>]+id="datatable-[^"]+"[^>]*>'
        r"(.*?)</script>",
        text,
        re.DOTALL,
    )
    tables = [json.loads(block) for block in blocks]
    rows = next(table for table in tables if isinstance(table, list))
    assert len(rows) >= 20 and all(len(row) == 3 for row in rows)
    links = {
        link
        for row in rows
        for link in re.findall(r'href="([^"]+)"', "".join(row))
    }
    pdf_links = [link for link in links if link.lower().endswith(".pdf")]
    assert len(pdf_links) >= 10
    assert any("riigiteataja.ee" in link for link in links)
    pdf, pdf_type = fetch(urljoin(page_url, pdf_links[0]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def court_proceedings() -> None:
    general = {
        "searchInText": False,
        "searchInTitle": False,
        "searchText": "",
        "searchText2": "",
        "logicalOperator": "AND",
        "morphSearch": False,
    }
    decisions = fetch_json(
        "https://www.riigiteataja.ee/public-api/api/v1/"
        "kohtuteave/otsing/kohtulahendid",
        data=json.dumps(
            {
                "general": {
                    **general,
                    "sort": "toiminguNr",
                    "sortAscending": False,
                },
                "precise": {"kohus": [], "seaduseSatted": {}},
            }
        ).encode(),
        headers={"Content-Type": "application/json"},
    )
    assert isinstance(decisions, dict) and decisions.get("kokku", 0) > 0
    assert decisions.get("tulemused")
    assert {
        "objektId",
        "kohtuasjaNumber",
        "lahendiKuulutamiseAeg",
    } <= decisions["tulemused"][0].keys()

    hearings = fetch_json(
        "https://www.riigiteataja.ee/public-api/api/v1/"
        "kohtuteave/otsing/kohtuistungid",
        data=json.dumps(
            {
                "general": {
                    **general,
                    "sort": "kehtivuseAlgus",
                    "sortAscending": True,
                },
                "precise": {"kohus": []},
            }
        ).encode(),
        headers={"Content-Type": "application/json"},
    )
    assert isinstance(hearings, dict) and hearings.get("kokku", 0) > 0
    assert hearings.get("tulemused")
    assert {"kohtuasjaNr", "kohus", "istungiAeg"} <= hearings["tulemused"][0].keys()


def court_statistics() -> None:
    body, content_type = fetch(
        "https://www.kohus.ee/eesti-kohtud/kohtute-menetlusstatistika"
    )
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert "OWVjNWMxY2ItMDgwMS00NzhiLWIzOTctMDM5NTFlNjczNGE4" in text
    assert "OGQ5MmY3YWItZjM0Zi00OWNlLThjZWYtZDIzN2IyY2YwNmYw" in text
    assert "https://www.riigikohus.ee/et/riigikohus/statistika" in text


def supreme_court() -> None:
    query = urlencode({"tekst": "põhiseadus", "pageSize": 5})
    body, content_type = fetch("https://rikos.rik.ee/?" + query)
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    match = re.search(r"Tulemused:\s*\((\d+)\)", text)
    assert match and int(match.group(1)) > 0
    assert re.search(r'href="/LahendiOtsingEriVaade\?asjaNr=[^"]+"', text)


def official_notices() -> None:
    contract, content_type = fetch(
        "https://www.ametlikudteadaanded.ee/avalik/uriotsing"
    )
    contract_text = unescape(contract.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert all(
        component in contract_text
        for component in ("{andmeandja}", "{pealiik}", "{alaliik}", "{teate_number}")
    )
    assert "advokatuur" in contract_text

    body, xml_type = fetch(
        "https://www.ametlikudteadaanded.ee/ee/-/advokatuur/xml"
    )
    root = ET.fromstring(body)
    namespace = "http://www.ametlikudteadaanded.ee/xsd/2014-06-01/teadaanne.xsd"
    notices = root.findall(f"{{{namespace}}}teadaanne")
    assert xml_type in {"text/xml", "application/xml"} and notices
    assert notices[0].findtext("teate_number")
    assert notices[0].findtext("url", "").startswith("https://")


def draft_acts() -> None:
    payload = {
        "general": {
            "searchInText": False,
            "searchInTitle": False,
            "searchText": "",
            "searchText2": "",
            "logicalOperator": "AND",
            "morphSearch": False,
            "sort": "esimeseEtapiAeg",
            "sortAscending": False,
        },
        "precise": {},
    }
    data = fetch_json(
        "https://www.riigiteataja.ee/public-api/api/v1/otsing/eelnoud",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    assert isinstance(data, dict) and data.get("kokku", 0) > 0
    assert data.get("tulemused")
    result = data["tulemused"][0]
    assert {"id", "pealkiri", "menetlusKaik", "etapid"} <= result.keys()
    assert result["etapid"]
    assert {"etapp", "aeg", "staatus", "menetlusTeave"} <= result["etapid"][0].keys()


def crime_policy() -> None:
    page_url = (
        "https://www.kriminaalpoliitika.ee/et/statistika-ja-uuringud/"
        "kuritegevus-eestis"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    links = re.findall(r'href="([^"]+\.pdf[^"]*)"', text, re.IGNORECASE)
    assert content_type == "text/html" and len(links) >= 10
    assert text.count("Kuritegevus Eestis 20") >= 10
    pdf, pdf_type = fetch(urljoin(page_url, links[0]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def prison_reviews() -> None:
    annual, annual_type = fetch(
        "https://vanglateenistus.ee/meist/uudised-ja-arvud/aasta-ulevaated"
    )
    annual_text = unescape(annual.decode("utf-8", "replace"))
    assert annual_type == "text/html"
    assert len(re.findall(r"20\d{2}\. aasta ülevaade", annual_text)) >= 5
    assert len(re.findall(r'/sites/default/files/[^" ]+\.png', annual_text)) >= 20

    current, current_type = fetch(
        "https://vanglateenistus.ee/meist/uudised-ja-arvud/"
        "paevakohane-arvuline-ulevaade"
    )
    current_text = unescape(current.decode("utf-8", "replace"))
    assert current_type == "text/html"
    assert current_text.count("https://app.fabric.microsoft.com/view?") >= 2
    assert re.search(r"Viimati uuendatud:\s*\d{2}\.\d{2}\.20\d{2}", current_text)


def consumer_decisions() -> None:
    query = urlencode({"_wbbdl": 1, "search[company]": "Telia"})
    data = fetch_json(
        "https://jvis.ttja.ee/modules/"
        "tarbijavaidluskomisjoni-otsused/avalik?" + query,
        headers={
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    assert isinstance(data, dict) and data.get("result") == "success"
    assert data.get("total", 0) > 0 and data.get("items")
    item = data["items"][0]
    assert {
        "company",
        "publishing_date",
        "document_nr",
        "decision",
        "summary",
        "public_pdf_id",
    } <= item.keys()
    pdf, pdf_type = fetch(
        "https://jvis.ttja.ee/modules/media/media/download/"
        f"{item['public_pdf_id']}",
        limit=5,
    )
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def environmental_permits() -> None:
    body, content_type = fetch(
        "https://kotkas.envir.ee/permits/public_index",
        data=urlencode({"search": 1, "owner_name": "Tallinna Vesi"}).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    total = re.search(r"Kokku\s+(\d+)\s+kirjet", text)
    assert total and int(total.group(1)) > 0
    match = re.search(r'/permits/public_view\?[^" ]*permit_id=(\d+)', text)
    assert match and "TALLINNA VESI AS" in text

    detail, detail_type = fetch(
        "https://kotkas.envir.ee/permits/public_view?search=1&permit_id="
        + match.group(1)
    )
    detail_text = unescape(detail.decode("utf-8", "replace"))
    assert detail_type == "text/html" and "Olek" in detail_text
    assert "/permits/public_detail_view?" in detail_text
    assert "/permits/public_permit_documents_index?" in detail_text
    assert "/permits/public_permit_assignments_index?" in detail_text


def environmental_charges() -> None:
    page_url = (
        "https://www.keskkonnaamet.ee/en/supervision-environmental-charge/"
        "environmental-charge/statistics"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    links = re.findall(r'href="([^"]+\.xlsx[^"]*)"', text, re.IGNORECASE)
    assert content_type == "text/html" and links
    workbook, workbook_type = fetch(
        urljoin(page_url, links[0]),
        headers={"Referer": page_url},
        limit=4,
    )
    assert workbook_type == (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert workbook == b"PK\x03\x04"


def forest_register() -> None:
    search = fetch_json(
        "https://register.metsad.ee/portaal/api/rest/eraldis/puu?"
        "kinnistuNr=12345"
    )
    assert isinstance(search, list) and search
    subunits = search[0].get("alamYksused", [])
    assert subunits and subunits[0].get("eraldised")
    stand = subunits[0]["eraldised"][0]
    assert {"id", "katastriNr", "eraldiseNr", "pindala", "alaGeoJson"} <= stand.keys()

    detail = fetch_json(
        "https://register.metsad.ee/portaal/api/rest/eraldis/detail/"
        f"{stand['id']}"
    )
    assert isinstance(detail, dict) and detail.get("id") == stand["id"]
    assert detail.get("katastriNr") == stand["katastriNr"]
    assert {"inventKp", "maakond", "vald", "elemendid", "tood"} <= detail.keys()


def planning_register() -> None:
    search = fetch_json(
        "https://www.planeeringud.ee/plank-web/api/planeering/otsing?"
        "page=0&size=2&sort=kehtestkp,desc",
        data=b'{"otsistring":"Vanalinna"}',
        headers={"Content-Type": "application/json"},
    )
    assert isinstance(search, dict) and search.get("content")
    record = search["content"][0]
    assert {"sysid", "planid", "plannim", "planseisNimi", "korraldaja"} <= record.keys()

    detail = fetch_json(
        "https://www.planeeringud.ee/plank-web/api/planeering/"
        f"{record['sysid']}"
    )
    assert isinstance(detail, dict) and detail.get("sysid") == record["sysid"]
    documents = detail.get("planDokuments", [])
    assert documents and all(item.get("filePublicUrl") for item in documents)


def cultural_heritage() -> None:
    base_url = "https://register.muinas.ee/public.php?menuID=monument"
    body, content_type = fetch(
        base_url,
        data=urlencode({"regnr": "31165"}).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert "Kokku: 1" in text and "Kunda mõisa tööstushoonete kompleks" in text
    match = re.search(
        r'href="([^"]*menuID=monument(?:&amp;|&)action=view(?:&amp;|&)id=31165)"',
        text,
    )
    assert match

    detail, detail_type = fetch(
        urljoin(base_url, match.group(1).replace("&amp;", "&"))
    )
    detail_text = unescape(detail.decode("utf-8", "replace"))
    assert detail_type == "text/html" and "31165 Kunda mõisa" in detail_text
    assert "Mälestise nimi" in detail_text
    assert "Mälestise registri number" in detail_text


def language_supervision() -> None:
    page_url = (
        "https://www.keeleamet.ee/keeleameti-tegevused-ja-eesmargid/"
        "keeleseaduse-ja-teiste-keeleoskust-ja-keelekasutust-3"
    )
    body, content_type = fetch(page_url)
    text = body.decode("utf-8", "replace")
    assert content_type == "text/html"
    assert 'type="application/json" id="datatable-' in text
    links = re.findall(r'\\/sites\\/default\\/files\\/[^" ]+\.pdf', text)
    links = sorted(set(link.replace(r"\/", "/") for link in links))
    assert len(links) >= 10
    assert "Keeleameti%202025.%20aasta%20tegevuse%20aruanne.pdf" in text
    pdf, pdf_type = fetch(urljoin(page_url, links[-1]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def state_audits() -> None:
    body, content_type = fetch("https://www.riigikontroll.ee/en/audits")
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert text.count("node--type-auditid") >= 20
    assert re.search(r'href="/en/audits/[^"]+" class="stretched-link"', text)
    assert "Audit report" in text and "report-title" in text

    detail_url = "https://www.riigikontroll.ee/en/audits/unused-state-budget-funds"
    detail, detail_type = fetch(detail_url)
    detail_text = unescape(detail.decode("utf-8", "replace"))
    links = re.findall(r'href="([^"]+\.pdf[^"]*)"', detail_text, re.IGNORECASE)
    assert detail_type == "text/html" and links
    assert "Unused state budget funds" in detail_text
    assert "The National Audit Office recommends" in detail_text
    pdf, pdf_type = fetch(urljoin(detail_url, links[0]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def ombudsman_reports() -> None:
    index_url = (
        "https://www.oiguskantsler.ee/en/opinions-and-initiatives/annual-reports"
    )
    body, content_type = fetch(index_url)
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert len(re.findall(r"https://www\.oiguskantsler\.ee/annual-report-20\d{2}/", text)) >= 5
    assert len(re.findall(r'href="[^"]+\.pdf"', text, re.IGNORECASE)) >= 10

    report_url = "https://www.oiguskantsler.ee/annual-report-2025/"
    report, report_type = fetch(report_url)
    report_text = unescape(report.decode("utf-8", "replace"))
    assert report_type == "text/html"
    assert "Chancellor’s Year in Review 2024/2025" in report_text
    assert 'href="./overview.pdf"' in report_text
    pdf, pdf_type = fetch(urljoin(report_url, "overview.pdf"), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def aircraft_register() -> None:
    body, content_type = fetch(
        "https://www.transpordiamet.ee/ohusoidukite-register"
    )
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    for label in (
        "Registration mark",
        "Type of the Aircraft",
        "Serial number",
        "Owner of the Aircraft",
        "Operator of the Aircraft",
    ):
        assert label in text
    assert re.search(r"\d{2}\.\d{2}\.20\d{2}/updated", text)
    marks = re.findall(r"ES(?:&nbsp;|\s)*-(?:&nbsp;|\s)*[A-Z0-9]{3,4}", text)
    assert len(marks) >= 100


def aviation_reports() -> None:
    page_url = (
        "https://www.transpordiamet.ee/en/aviation-and-aviation-safety/"
        "aviation-safety/reports"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html"
    assert "ANS and ATM Annual Safety Oversight Reports" in text
    links = re.findall(r'href="([^"]+\.pdf[^"]*)"', text, re.IGNORECASE)
    reports = [link for link in links if "annual" in link or "safety_oversight" in link]
    assert len(reports) >= 6
    pdf, pdf_type = fetch(urljoin(page_url, reports[0]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def construction_register() -> None:
    data = fetch_json(
        "https://livekluster.ehr.ee/api/building/v2/buildingSearchPageable",
        data=json.dumps(
            {"buildingName": "raekoda", "page": 1, "pageSize": 2}
        ).encode(),
        headers={"Content-Type": "application/json"},
    )
    assert isinstance(data, dict) and data.get("total", 0) > 0
    assert data.get("data")
    record = data["data"][0]
    assert {"ehrCode", "buildingId", "buildingAddress", "buildingState"} <= record.keys()

    detail = fetch_json(
        "https://livekluster.ehr.ee/api/building/v3/buildingData?"
        + urlencode({"ehr_code": record["ehrCode"], "json": "true"})
    )
    assert detail["ehitis"]["ehitiseAndmed"]["ehrKood"] == record["ehrCode"]


def economic_activities() -> None:
    jar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar))
    form_request = Request(
        "https://mtr.ttja.ee/juriidiline_isik?m=96",
        headers={"User-Agent": USER_AGENT},
    )
    with opener.open(form_request, timeout=45) as response:
        form = response.read().decode("utf-8", "replace")
    match = re.search(
        r'name="juriidiline_isik_filters\[_csrf_token\]" value="([^"]+)"',
        form,
    )
    assert match
    payload = urlencode(
        [
            ("juriidiline_isik_filters[_csrf_token]", match.group(1)),
            ("juriidiline_isik_filters[registrikood][text]", "14532901"),
            ("juriidiline_isik_filters[fie]", ""),
            ("juriidiline_isik_filters[arhiveeritud_isikud]", ""),
            ("juriidiline_isik_filters[oigsuse_kinnitus]", ""),
            ("juriidiline_isik_filters[tegevusala_tyyp]", ""),
            ("juriidiline_isik_filters[valjund_valjad][]", "nimi"),
            ("juriidiline_isik_filters[valjund_valjad][]", "registrikood"),
        ]
    ).encode()
    search_request = Request(
        "https://mtr.ttja.ee/juriidiline_isik/filter/action",
        data=payload,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    with opener.open(search_request, timeout=45) as response:
        result = unescape(response.read().decode("utf-8", "replace"))
    assert "Registrikood:" in result and "14532901" in result
    detail_match = re.search(r'href="(/juriidiline_isik/\d+)\?backurl=', result)
    assert detail_match and "Bolt Operations OÜ" in result

    detail_request = Request(
        urljoin("https://mtr.ttja.ee", detail_match.group(1)),
        headers={"User-Agent": USER_AGENT},
    )
    with opener.open(detail_request, timeout=45) as response:
        detail = unescape(response.read().decode("utf-8", "replace"))
    assert "Majandustegevusteated" in detail and "Tegevusload" in detail
    assert "Postiteenuse majandustegevusteade" in detail


def patent_registers() -> None:
    trademark_url = (
        "https://andmebaas.epa.ee/avalik/api/trademarks/search/"
        "findBySearchParameters?"
        + urlencode({"verbalElement": "ESTONIA", "page": 0, "size": 1})
    )
    body, content_type = fetch(trademark_url)
    trademarks = json.loads(body)
    assert content_type == "application/hal+json"
    trademark = trademarks["_embedded"]["trademarks"][0]
    assert {"id", "applicationNumber", "currentStatus", "verbalElement"} <= trademark.keys()

    design_url = (
        "https://andmebaas.epa.ee/avalik/api/designApplications/search/"
        "findBySearchParameters?"
        + urlencode({"verbalElement": "tool", "page": 0, "size": 1})
    )
    body, content_type = fetch(design_url)
    designs = json.loads(body)
    assert content_type == "application/hal+json"
    design = designs["_embedded"]["designApplications"][0]
    assert {"id", "applicationNumber", "currentStatus", "verbalElement"} <= design.keys()


def pria_subsidies() -> None:
    jar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar))
    page_url = "https://www.pria.ee/toetused/toetusesaajad?year=2025"
    request = Request(page_url, headers={"User-Agent": USER_AGENT})
    with opener.open(request, timeout=45) as response:
        page = unescape(response.read().decode("utf-8", "replace"))
    match = re.search(r'href="([^"]*/download/file/PRIA_export_[^"]+\.csv[^"]*)"', page)
    assert match and "year=2025" in match.group(1)

    export_request = Request(
        urljoin(page_url, match.group(1)),
        headers={"User-Agent": USER_AGENT},
    )
    with opener.open(export_request, timeout=45) as response:
        csv_text = response.read(4_000_000).decode("utf-8-sig", "replace")
    lines = csv_text.splitlines()
    assert lines[0] == "sep=;"
    assert "Toetusesaaja nimi" in lines[1] and "Finantsaasta" in lines[1]
    assert len(lines) > 2 and any('"2025"' in line for line in lines[2:])


def eu_funded_projects() -> None:
    credentials = base64.b64encode(b"Mig46PpedQosEam:").decode()
    request = Request(
        "https://pilv.rtk.ee/public.php/webdav/",
        headers={
            "User-Agent": USER_AGENT,
            "Authorization": f"Basic {credentials}",
            "Depth": "2",
        },
        method="PROPFIND",
    )
    with urlopen(request, timeout=45) as response:
        assert response.status == 207
        root = ET.fromstring(response.read(1_000_000))
    responses = root.findall("{DAV:}response")
    xlsx = []
    for item in responses:
        href = item.findtext("{DAV:}href", "")
        content_type = item.findtext(".//{DAV:}getcontenttype", "")
        length = item.findtext(".//{DAV:}getcontentlength", "0")
        if href.endswith(".xlsx"):
            xlsx.append((href, content_type, int(length)))
    assert len(xlsx) >= 4
    assert any("Toetatud%20projektide%20tabelid/" in href for href, _, _ in xlsx)
    assert all(
        content_type
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        and length > 10_000
        for _, content_type, length in xlsx
    )


def kultuurkapital_grants() -> None:
    index_url = "https://www.kulka.ee/avalik-teave/eraldused-voorude-kaupa"
    body, content_type = fetch(index_url)
    index = unescape(body.decode("utf-8", "replace"))
    links = set(
        re.findall(
            r'href="(/avalik-teave/eraldused-voorude-kaupa/[^"#]+)',
            index,
        )
    )
    assert content_type == "text/html" and len(links) >= 20

    round_url = urljoin(
        index_url,
        "/avalik-teave/eraldused-voorude-kaupa/2025-a-4-taotlusvoor",
    )
    body, content_type = fetch(round_url)
    page = unescape(body.decode("utf-8", "replace"))
    assert content_type == "text/html" and page.count("<table") >= 10
    assert "Eralduse saaja" in page
    assert "Kasutamise eesmärk" in page or "Eralduse eesmärk" in page
    assert "Eraldatud summa" in page or ">Summa<" in page


def development_cooperation() -> None:
    jar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar))
    search_url = "https://akta.mfa.ee/andmed_otsing.php?language=eng"
    request = Request(search_url, headers={"User-Agent": USER_AGENT})
    with opener.open(request, timeout=45) as response:
        form = response.read().decode("utf-8", "replace")
    match = re.search(r'name="_csrf_token" value="([^"]+)"', form)
    assert match
    payload = urlencode(
        {
            "_csrf_token": match.group(1),
            "aasta_a": "2025",
            "aasta_k": "2025",
            "aastased_projektid": "0",
            "kaasfinantseerija": "0",
            "mitu_riiki": "1",
            "mitu_arenguabi_liiki": "1",
            "otsi": "Otsi",
        }
    ).encode()
    search_request = Request(
        search_url,
        data=payload,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    with opener.open(search_request, timeout=45) as response:
        result = response.read().decode("utf-8", "replace")
        assert response.url.endswith("/andmed.php")
    assert "andmed_vaata.php?id=" in result and ">2025<" in result

    export_request = Request(
        "https://akta.mfa.ee/andmed_csv.php",
        headers={"User-Agent": USER_AGENT},
    )
    with opener.open(export_request, timeout=45) as response:
        csv_text = response.read(4_000_000).decode("windows-1257")
    lines = csv_text.splitlines()
    assert "Aasta" in lines[0] and "Projekti nimi" in lines[0]
    assert "Arvesseminev summa EUR" in lines[0]
    assert len(lines) > 2 and any('="2025"' in line for line in lines[2:])


def civil_service_pay() -> None:
    page_url = (
        "https://www.fin.ee/riigihaldus-ja-avalik-teenistus-kinnisvara/"
        "avalik-teenistus/palgakorraldus"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    xlsx = re.findall(r'href="([^"]+\.xlsx[^"]*)"', text, re.IGNORECASE)
    pdfs = re.findall(r'href="([^"]+\.pdf[^"]*)"', text, re.IGNORECASE)
    assert content_type == "text/html" and xlsx and len(pdfs) >= 4
    assert "palkade avalikustamise juhend" in text.lower()
    workbook, workbook_type = fetch(urljoin(page_url, xlsx[0]), limit=4)
    assert workbook_type == (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert workbook == b"PK\x03\x04"
    pdf, pdf_type = fetch(urljoin(page_url, pdfs[0]), limit=5)
    assert pdf_type == "application/pdf" and pdf == b"%PDF-"


def public_sector_statistics() -> None:
    page_url = (
        "https://www.fin.ee/riigihaldus-ja-avalik-teenistus-kinnisvara/"
        "riigihaldus/avaliku-sektori-statistika"
    )
    body, content_type = fetch_with_curl(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    xlsx = re.findall(r'href="([^"]+\.xlsx[^"]*)"', text, re.IGNORECASE)
    assert content_type == "text/html" and len(xlsx) >= 3
    assert "Ametnike põhipalgad" in text and "Avaliku sektori asutused" in text
    assert text.count("https://app.powerbi.com/view?") >= 3
    workbook, workbook_type = fetch_with_curl(
        urljoin(page_url, xlsx[0]),
        headers={"Referer": page_url},
    )
    assert workbook_type == (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert workbook.startswith(b"PK\x03\x04")


def health_insurance_reports() -> None:
    page_url = "https://www.tervisekassa.ee/en/organisation/annual-reports"
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    links = re.findall(r'href="([^"]+\.pdf[^"]*)"', text, re.IGNORECASE)
    years = set(re.findall(r">(20\d{2})</a>", text))
    assert content_type == "text/html" and len(links) >= 20
    assert len(years) >= 20
    pdf, pdf_type = fetch(urljoin(page_url, links[0]), limit=5)
    assert pdf_type in {"application/pdf", "application/octet-stream"}
    assert pdf == b"%PDF-"


def health_statistics() -> None:
    table_url = (
        "https://statistika.tai.ee/api/v1/et/Andmebaas/"
        "01Rahvastik/02Synnid/SR001.px"
    )
    metadata = fetch_json(table_url)
    assert isinstance(metadata, dict) and metadata.get("title") == "SR001: Sünnid"
    variables = metadata.get("variables", [])
    assert [item.get("code") for item in variables] == ["Aasta", "Elulisus"]

    payload = {
        "query": [
            {
                "code": "Aasta",
                "selection": {"filter": "item", "values": ["2025"]},
            },
            {
                "code": "Elulisus",
                "selection": {"filter": "item", "values": ["1"]},
            },
        ],
        "response": {"format": "json-stat2"},
    }
    data = fetch_json(
        table_url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    assert isinstance(data, dict) and data.get("class") == "dataset"
    assert data.get("id") == ["ContentsCode", "Aasta", "Elulisus"]
    assert data.get("size") == [1, 1, 1] and len(data.get("value", [])) == 1
    assert data.get("source") and data.get("note")


def tehik_covid_open_data() -> None:
    root_url = "https://rest-avaandmed.tehik.ee/covid19/"
    body, content_type = fetch(root_url)
    schema = json.loads(body)
    assert content_type in {"application/json", "application/openapi+json"}
    paths = schema.get("paths", {})
    assert "/opendata_covid19_hospitalization" in paths
    assert (
        "/opendata_covid19_riskgroup_vaccination_season_location_agegroup"
        in paths
    )

    data = fetch_json(
        root_url
        + "opendata_covid19_hospitalization?Valid=eq.true&"
        "order=StatisticsWeek.desc&limit=2"
    )
    assert isinstance(data, list) and data
    assert {
        "StatisticsWeek",
        "HospitalizationCount",
        "Valid",
        "ModifiedAt",
    } <= data[0].keys()
    assert data[0]["Valid"] is True


def social_insurance_statistics() -> None:
    page_url = (
        "https://www.sotsiaalkindlustusamet.ee/asutus-uudised-ja-kontakt/"
        "praktiline-teave/statistika"
    )
    body, content_type = fetch(page_url)
    text = unescape(body.decode("utf-8", "replace"))
    links = re.findall(r'href="([^"]+\.xlsx[^"]*)"', text, re.IGNORECASE)
    rsk = [link for link in links if "RSK_koond" in link]
    assert content_type == "text/html" and len(links) >= 50 and rsk
    assert "Riiklik sotsiaalkindlustus" in text
    workbook, workbook_type = fetch(urljoin(page_url, rsk[0]), limit=4)
    assert workbook_type == (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert workbook == b"PK\x03\x04"


def unemployment_statistics() -> None:
    metadata_url = (
        "https://andmed.eesti.ee/api/datasets/slug/registreeritud-tootud"
    )
    headers = {"Origin": "https://andmed.eesti.ee"}
    data = fetch_json(metadata_url, headers=headers)
    assert isinstance(data, dict) and data.get("slug") == "registreeritud-tootud"
    assert data.get("organization", {}).get("slug") == "eesti-tootukassa"
    distributions = data.get("distributions", [])
    assert len(distributions) >= 10
    xlsx = next(item for item in distributions if item.get("format") == "XLSX")
    assert xlsx.get("accessUrls") and int(xlsx.get("byteSize", 0)) > 10_000
    workbook, workbook_type = fetch(
        xlsx["accessUrls"][0],
        headers=headers,
        limit=4,
    )
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
    "agricultural-subsidies-pria": pria_subsidies,
    "aircraft-register": aircraft_register,
    "aviation-safety-reports": aviation_reports,
    "bank-of-statistics": bank,
    "business-register-open-data": business_register,
    "civil-service-pay-governance": civil_service_pay,
    "communicable-disease-bulletins": communicable_diseases,
    "consumer-technical-regulator-decisions": consumer_decisions,
    "construction-register": construction_register,
    "cultural-heritage-register": cultural_heritage,
    "court-proceedings-data": court_proceedings,
    "court-system-statistics": court_statistics,
    "crime-policy-statistics": crime_policy,
    "cyber-incidents-cert-ee": cyber_incidents,
    "digital-government-studies": ria_studies,
    "election-results-data": elections,
    "energy-data": energy,
    "economic-activities-register-mtr": economic_activities,
    "eu-funded-projects": eu_funded_projects,
    "environmental-charge-statistics": environmental_charges,
    "environmental-permit-decisions": environmental_permits,
    "estonia-2035-action-plan": estonia_2035,
    "food-business-approvals": food_businesses,
    "forest-register": forest_register,
    "geospatial-open-data": geospatial,
    "government-action-programme": government_action_programme,
    "government-journal-records": government_journal,
    "government-session-agendas": government_agendas,
    "health-supervision-decisions": health_supervision,
    "health-insurance-fund-reports": health_insurance_reports,
    "health-statistics": health_statistics,
    "health-welfare-open-data": tehik_covid_open_data,
    "healthcare-professionals-register": healthcare_professionals,
    "legal-acts-data": legal_acts,
    "legislation-workflow-eis": legislation_workflow,
    "lobby-meetings": lobby_meetings,
    "language-law-supervision": language_supervision,
    "kultuurkapital-grants-data": kultuurkapital_grants,
    "marital-property-register": marital_property,
    "maritime-economy-statistics": maritime_economy,
    "ministry-document-registries": ministry_documents,
    "mfa-development-cooperation-aid": development_cooperation,
    "muis-open-data": muis,
    "open-data": open_data,
    "official-notices": official_notices,
    "ombudsman-opinions": ombudsman_reports,
    "patent-and-trademark-registers": patent_registers,
    "planning-decisions": planning_register,
    "prison-annual-reviews": prison_reviews,
    "public-finance-data": public_finance,
    "public-sector-statistics-fin": public_sector_statistics,
    "public-sector-it-systems-riha": riha,
    "riigikogu-open-data": riigikogu,
    "riigiteataja-draft-acts": draft_acts,
    "social-insurance-statistics": social_insurance_statistics,
    "statistics-api": statistics,
    "strategic-development-documents-registry": strategic_documents,
    "state-ownership-data": state_ownership,
    "state-audit-reports": state_audits,
    "state-port-register": state_ports,
    "supreme-court-judgments": supreme_court,
    "tallinn-open-data": tallinn,
    "tartu-document-register": tartu_documents,
    "tax-customs-data": tax_customs,
    "transport-traffic-data": transport,
    "unemployment-statistics": unemployment_statistics,
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
