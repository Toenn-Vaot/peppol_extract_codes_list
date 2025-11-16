#!/usr/bin/env python3
import json
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://docs.peppol.eu/poacc/billing/3.0/"
OUTPUT_FILE = "peppol_codelists.json"


def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url)
    resp.raise_for_status()
    # Force UTF-8 decode
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser", from_encoding="utf-8")
    
def safe_text(el):
    """
    Get the element text, sanitized or return empty
    """
    if not el:
        return ""
        
    import re
    text = el.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_meta_value(soup: BeautifulSoup, label: str) -> str | None:
    """
    Find text like 'Identifier', 'Agency', 'Version' and take the next block's text.
    Works with the Peppol docs layout.
    """
    node = soup.find(string=re.compile(rf"^\s*{re.escape(label)}\s*$"))
    if not node:
        return None
    parent = node.parent
    # The value is usually in the next sibling paragraph or div
    sib = parent.find_next_sibling()
    while sib and not sib.get_text(strip=True):
        sib = sib.find_next_sibling()
    return sib.get_text(strip=True) if sib else None


def extract_codes(soup: BeautifulSoup) -> list[dict]:
    """
    Generic code extractor for Peppol codelist pages.

    Strategy:
      - Find the 'Codes' heading
      - From there, iterate over all <code> tags
      - For each code tag, take following sibling blocks as description
        until the next <code> is encountered
    """
    codes = []

    # Find the "Codes" heading (h2, h3, p, etc.)
    codes_heading = soup.find(string=re.compile(r"^\s*Codes\s*$"))
    if not codes_heading:
        return codes

    # All code tags after the "Codes" heading
    for code_tag in codes_heading.find_parent().find_all_next("code"):
        code_text = safe_text(code_tag)
        if not code_text:
            continue
                              
        title = code_tag.find_next("strong")
        description = code_tag.parent.find_next_sibling("p")
        
        codes.append(
            {
                "code": code_text,
                "title": safe_text(title),
                "description": safe_text(description),
            }
        )

    return codes


def discover_codelist_links() -> dict:
    """
    From the main BIS Billing page, discover all codelist URLs and titles.
    """
    soup = get_soup(BASE_URL)
    codelists = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/codelist/" not in href:
            continue
        url = urljoin(BASE_URL, href)
        identifier = url.rstrip("/").split("/")[-1]
        title = a.get_text(strip=True) or identifier
        codelists[identifier] = {"identifier": identifier, "title": title, "url": url}

    return codelists

def scrape_codelist(identifier: str, meta: dict) -> dict:
    print(f"Scraping {identifier} → {meta['url']}")
    soup = get_soup(meta["url"])

    return {
        "identifier": extract_meta_value(soup, "Identifier") or identifier,
        "title": meta["title"],
        "url": meta["url"],
        "agency": extract_meta_value(soup, "Agency"),
        "version": extract_meta_value(soup, "Version"),
        "codes": extract_codes(soup)
    }


def main():
    codelist_links = discover_codelist_links()
    result = {}

    for ident, meta in sorted(codelist_links.items()):
        result[ident] = scrape_codelist(ident, meta)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Written {len(result)} codelists to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
