"""
Bankruptcy Deal Finder — Scraper
Scans torgi.gov.ru for auction lots matching user criteria.

Usage:
    python scraper.py                    # Scan with default config
    python scraper.py --region moscow    # Override region
    python scraper.py --type apartment   # Override asset type
    python scraper.py --max-price 5000000
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# Load config
from dotenv import load_dotenv
load_dotenv("config.env")

REGIONS = os.getenv("REGIONS", "moscow").split(",")
ASSET_TYPES = os.getenv("ASSET_TYPES", "apartment,commercial").split(",")
MAX_PRICE = int(os.getenv("MAX_PRICE", "15000000"))
MIN_DISCOUNT = int(os.getenv("MIN_DISCOUNT", "25"))

# torgi.gov.ru public search endpoint
TORGI_BASE = "https://torgi.gov.ru/new/api/public/lotcards/search"

# Asset type mapping for torgi.gov.ru
ASSET_TYPE_MAP = {
    "apartment": "Квартира",
    "commercial": "Нежилое помещение",
    "land": "Земельный участок",
    "vehicle": "Транспортное средство",
    "equipment": "Оборудование",
    "house": "Жилой дом",
    "parking": "Машино-место",
    "office": "Офис",
}

# Region mapping (simplified, expand as needed)
REGION_MAP = {
    "moscow": "77",
    "spb": "78",
    "mo": "50",         # Moscow Oblast
    "krasnogorsk": "50", # part of MO
    "ekb": "66",
    "kazan": "16",
    "nsk": "54",         # Novosibirsk
    "samara": "63",
}


def build_search_url(region_code, asset_type_ru, max_price, page=0, size=50):
    """Build search URL for torgi.gov.ru API."""
    params = {
        "catCode": "2",  # Property from bankruptcy
        "withFacets": "true",
        "size": str(size),
        "page": str(page),
        "sort": "firstVersionPublicationDate,desc",
    }
    if region_code:
        params["ownership.region.code"] = region_code
    if max_price:
        params["priceTo"] = str(max_price)

    query = urllib.parse.urlencode(params)
    return f"{TORGI_BASE}?{query}"


def fetch_lots(region, asset_type, max_price):
    """Fetch lots from torgi.gov.ru for given criteria."""
    region_code = REGION_MAP.get(region.strip(), "")
    asset_type_ru = ASSET_TYPE_MAP.get(asset_type.strip(), "")

    url = build_search_url(region_code, asset_type_ru, max_price)
    print(f"  Scanning: region={region}, type={asset_type}, max_price={max_price:,}")
    print(f"  URL: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BankruptcyDealFinder/1.0)",
        "Accept": "application/json",
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            lots = data.get("content", [])
            total = data.get("totalElements", 0)
            print(f"  Found: {len(lots)} lots (total matching: {total})")
            return lots, total
    except urllib.error.HTTPError as e:
        print(f"  Error {e.code}: {e.reason}")
        return [], 0
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return [], 0
    except Exception as e:
        print(f"  Unexpected error: {e}")
        return [], 0


def parse_lot(raw_lot):
    """Extract relevant fields from a raw lot object."""
    try:
        return {
            "id": raw_lot.get("id", ""),
            "title": raw_lot.get("lotName", "No title"),
            "description": raw_lot.get("lotDescription", "")[:500],
            "price": raw_lot.get("priceMin") or raw_lot.get("startPrice") or 0,
            "region": raw_lot.get("estateAddress", {}).get("region", {}).get("name", "Unknown"),
            "address": raw_lot.get("estateAddress", {}).get("addressString", ""),
            "asset_type": raw_lot.get("category", {}).get("name", "Unknown"),
            "area_sqm": raw_lot.get("characteristics", {}).get("area", None),
            "auction_date": raw_lot.get("biddEndTime", ""),
            "publication_date": raw_lot.get("firstVersionPublicationDate", ""),
            "status": raw_lot.get("biddForm", {}).get("name", ""),
            "url": f"https://torgi.gov.ru/new/public/lots/lot/{raw_lot.get('id', '')}",
            "source": "torgi.gov.ru",
        }
    except Exception as e:
        return {
            "id": str(raw_lot.get("id", "unknown")),
            "title": "Parse error",
            "description": str(e),
            "price": 0,
            "source": "torgi.gov.ru",
        }


def scan_all():
    """Scan all configured regions and asset types."""
    all_lots = []
    total_scanned = 0

    print(f"\n{'='*60}")
    print(f"Bankruptcy Deal Finder — Scan started {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Regions: {', '.join(REGIONS)}")
    print(f"Asset types: {', '.join(ASSET_TYPES)}")
    print(f"Max price: {MAX_PRICE:,} rub")
    print(f"{'='*60}\n")

    for region in REGIONS:
        for asset_type in ASSET_TYPES:
            lots, total = fetch_lots(region, asset_type, MAX_PRICE)
            total_scanned += total

            for raw in lots:
                parsed = parse_lot(raw)
                if parsed["price"] > 0:
                    all_lots.append(parsed)

            time.sleep(1)  # Respect rate limits: 1 req/sec

    # Deduplicate by ID
    seen = set()
    unique_lots = []
    for lot in all_lots:
        if lot["id"] not in seen:
            seen.add(lot["id"])
            unique_lots.append(lot)

    print(f"\nScan complete: {len(unique_lots)} unique lots found ({total_scanned} total matches)")
    return unique_lots


def save_results(lots, filepath="data/lots_raw.json"):
    """Save scan results to JSON file."""
    Path("data").mkdir(exist_ok=True)

    output = {
        "scan_date": datetime.now().isoformat(),
        "regions": REGIONS,
        "asset_types": ASSET_TYPES,
        "max_price": MAX_PRICE,
        "total_lots": len(lots),
        "lots": lots,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Results saved to {filepath}")
    return filepath


if __name__ == "__main__":
    # Parse CLI args
    import argparse
    parser = argparse.ArgumentParser(description="Scan bankruptcy auctions")
    parser.add_argument("--region", help="Override region (e.g., moscow, spb)")
    parser.add_argument("--type", help="Override asset type (e.g., apartment, commercial)")
    parser.add_argument("--max-price", type=int, help="Max lot price in rubles")
    args = parser.parse_args()

    if args.region:
        REGIONS = [args.region]
    if args.type:
        ASSET_TYPES = [args.type]
    if args.max_price:
        MAX_PRICE = args.max_price

    lots = scan_all()

    if lots:
        save_results(lots)
        print(f"\nTop 5 by price (lowest first):")
        for lot in sorted(lots, key=lambda x: x["price"])[:5]:
            print(f"  {lot['price']:>12,} rub | {lot['title'][:60]}")
            print(f"  {'':>12}     | {lot['address'][:60]}")
            print(f"  {'':>12}     | {lot['url']}")
            print()
    else:
        print("\nNo lots found matching criteria.")
