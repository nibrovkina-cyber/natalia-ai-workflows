"""
Bankruptcy Deal Finder — Analyzer
Reads scraped lots, estimates market price via Claude, calculates discount.

Usage:
    python analyzer.py                      # Analyze all lots from last scan
    python analyzer.py --min-discount 30    # Only show 30%+ discount
    python analyzer.py --top 10             # Show top 10 deals
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("config.env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MIN_DISCOUNT = int(os.getenv("MIN_DISCOUNT", "25"))

# Use urllib for Claude API to avoid extra dependencies
import urllib.request
import urllib.error


def estimate_market_price(lot):
    """Ask Claude to estimate market price based on lot details."""
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY.startswith("sk-ant-your"):
        # Fallback: rough estimate based on area and region
        return estimate_market_price_fallback(lot)

    prompt = f"""You are a Russian real estate market analyst. Estimate the market price for this asset.

Asset details:
- Type: {lot.get('asset_type', 'Unknown')}
- Location: {lot.get('address', lot.get('region', 'Unknown'))}
- Area: {lot.get('area_sqm', 'Unknown')} sqm
- Description: {lot.get('description', 'No description')[:300]}
- Auction starting price: {lot.get('price', 0):,} rubles

Based on current market data for this region and asset type in April 2026, provide:
1. Estimated market price in rubles (single number, your best estimate)
2. Confidence: high/medium/low
3. One sentence explaining your reasoning

Respond in JSON format:
{{"market_price": 7000000, "confidence": "medium", "reasoning": "54 sqm apartment in Krasnogorsk, avg price 120-140k/sqm in Q1 2026"}}
"""

    body = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = result["content"][0]["text"]

            # Extract JSON from response
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                estimate = json.loads(text[start:end])
                return {
                    "market_price": int(estimate.get("market_price", 0)),
                    "confidence": estimate.get("confidence", "low"),
                    "reasoning": estimate.get("reasoning", ""),
                    "method": "claude"
                }
    except Exception as e:
        print(f"  Claude API error: {e}")

    return estimate_market_price_fallback(lot)


def estimate_market_price_fallback(lot):
    """Rough estimate without API. Based on average regional prices per sqm."""
    # Average prices per sqm in rubles (Q1 2026, rough)
    avg_prices = {
        "Москва": 350000,
        "Санкт-Петербург": 220000,
        "Московская область": 150000,
        "Екатеринбург": 120000,
        "Казань": 130000,
        "Новосибирск": 110000,
        "Самара": 95000,
    }

    # Commercial multiplier (usually 0.8-1.2x residential)
    commercial_mult = 0.9

    area = lot.get("area_sqm")
    region = lot.get("region", "")
    asset_type = lot.get("asset_type", "").lower()

    if not area or area <= 0:
        return {"market_price": 0, "confidence": "none", "reasoning": "No area data", "method": "fallback"}

    price_per_sqm = 150000  # default
    for region_name, price in avg_prices.items():
        if region_name.lower() in region.lower():
            price_per_sqm = price
            break

    if "нежил" in asset_type or "коммерч" in asset_type or "офис" in asset_type:
        price_per_sqm = int(price_per_sqm * commercial_mult)

    market_price = int(area * price_per_sqm)

    return {
        "market_price": market_price,
        "confidence": "low",
        "reasoning": f"Fallback estimate: {area} sqm * {price_per_sqm:,} rub/sqm (avg for {region})",
        "method": "fallback"
    }


def calculate_discount(lot_price, market_price):
    """Calculate discount percentage."""
    if market_price <= 0 or lot_price <= 0:
        return 0
    return round((1 - lot_price / market_price) * 100, 1)


def score_deal(discount, confidence, days_until_deadline):
    """Score a deal: higher = better opportunity."""
    confidence_mult = {"high": 1.0, "medium": 0.7, "low": 0.4, "none": 0.1}
    urgency_mult = 1.0
    if days_until_deadline and 0 < days_until_deadline <= 3:
        urgency_mult = 1.3  # urgent, might be underpriced
    elif days_until_deadline and days_until_deadline > 30:
        urgency_mult = 0.8  # plenty of time, others will find it too

    return round(discount * confidence_mult.get(confidence, 0.5) * urgency_mult, 1)


def days_until(date_str):
    """Calculate days until a date string."""
    if not date_str:
        return None
    try:
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%d.%m.%Y"):
            try:
                dt = datetime.strptime(date_str[:19], fmt)
                return (dt - datetime.now()).days
            except ValueError:
                continue
    except Exception:
        pass
    return None


def analyze_lots(input_file="data/lots_raw.json", min_discount=None):
    """Analyze all lots: estimate market price, calculate discount, rank."""
    if min_discount is None:
        min_discount = MIN_DISCOUNT

    if not Path(input_file).exists():
        print(f"No scan data found at {input_file}. Run scraper.py first.")
        return []

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    lots = data.get("lots", [])
    print(f"\nAnalyzing {len(lots)} lots (min discount: {min_discount}%)...\n")

    analyzed = []
    for i, lot in enumerate(lots):
        print(f"  [{i+1}/{len(lots)}] {lot.get('title', 'Unknown')[:50]}...")

        estimate = estimate_market_price(lot)
        discount = calculate_discount(lot.get("price", 0), estimate["market_price"])
        deadline_days = days_until(lot.get("auction_date"))

        deal = {
            **lot,
            "market_price": estimate["market_price"],
            "market_confidence": estimate["confidence"],
            "market_reasoning": estimate["reasoning"],
            "estimate_method": estimate["method"],
            "discount_pct": discount,
            "days_until_deadline": deadline_days,
            "deal_score": score_deal(discount, estimate["confidence"], deadline_days),
        }

        if discount >= min_discount:
            analyzed.append(deal)
            print(f"    Price: {lot.get('price', 0):>12,} rub")
            print(f"    Market: {estimate['market_price']:>11,} rub ({estimate['confidence']})")
            print(f"    Discount: {discount}%  |  Score: {deal['deal_score']}")
        else:
            print(f"    Discount {discount}% < {min_discount}% threshold, skipping")

    # Sort by deal_score descending
    analyzed.sort(key=lambda x: x["deal_score"], reverse=True)

    print(f"\n{'='*60}")
    print(f"Analysis complete: {len(analyzed)} deals above {min_discount}% discount")
    print(f"{'='*60}")

    return analyzed


def save_analyzed(deals, filepath="data/deals_analyzed.json"):
    """Save analyzed deals to JSON."""
    Path("data").mkdir(exist_ok=True)

    output = {
        "analysis_date": datetime.now().isoformat(),
        "min_discount": MIN_DISCOUNT,
        "total_deals": len(deals),
        "deals": deals,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Analyzed deals saved to {filepath}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze scanned bankruptcy lots")
    parser.add_argument("--min-discount", type=int, help="Minimum discount %%")
    parser.add_argument("--top", type=int, default=20, help="Show top N deals")
    parser.add_argument("--input", default="data/lots_raw.json", help="Input file")
    args = parser.parse_args()

    deals = analyze_lots(args.input, args.min_discount)

    if deals:
        save_analyzed(deals)
        print(f"\nTop {min(args.top, len(deals))} deals:")
        for i, deal in enumerate(deals[:args.top]):
            print(f"\n  #{i+1} | Score: {deal['deal_score']} | Discount: {deal['discount_pct']}%")
            print(f"  {deal.get('title', 'Unknown')[:70]}")
            print(f"  {deal.get('address', '')[:70]}")
            print(f"  Price: {deal.get('price', 0):,} rub | Market: ~{deal['market_price']:,} rub")
            print(f"  Deadline: {deal.get('days_until_deadline', '?')} days | {deal.get('url', '')}")
