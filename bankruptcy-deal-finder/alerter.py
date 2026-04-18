"""
Bankruptcy Deal Finder — Telegram Alerter
Sends top deals to your Telegram chat.

Usage:
    python alerter.py                    # Send top deals from last analysis
    python alerter.py --top 3            # Send only top 3
    python alerter.py --dry-run          # Print message without sending
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("config.env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def format_deal(deal, index):
    """Format a single deal for Telegram message."""
    price = deal.get("price", 0)
    market = deal.get("market_price", 0)
    discount = deal.get("discount_pct", 0)
    days = deal.get("days_until_deadline")
    confidence = deal.get("market_confidence", "?")

    deadline_str = f"{days} days" if days else "unknown"
    if days and days <= 3:
        deadline_str = f"URGENT: {days} days"

    area_str = ""
    if deal.get("area_sqm"):
        area_str = f", {deal['area_sqm']} sqm"

    lines = [
        f"{index}. {deal.get('title', 'Unknown')[:80]}{area_str}",
        f"   Price: {price:,} rub",
        f"   Market: ~{market:,} rub ({confidence})",
        f"   Discount: ~{discount}%",
        f"   Deadline: {deadline_str}",
        f"   {deal.get('url', '')}",
    ]

    return "\n".join(lines)


def format_message(deals, top_n=5):
    """Format full Telegram message with top deals."""
    today = datetime.now().strftime("%d %B %Y")

    header = f"Top {min(top_n, len(deals))} deals — {today}\n"
    separator = ""

    deal_texts = []
    for i, deal in enumerate(deals[:top_n], 1):
        deal_texts.append(format_deal(deal, i))

    footer_parts = [
        f"\nScanned: {datetime.now().strftime('%H:%M MSK')}",
        f"Total deals found: {len(deals)}",
    ]

    # Check for tracked lots updates
    tracked_updates = check_tracked_lots(deals)
    if tracked_updates:
        footer_parts.append(f"\nTracked lots:")
        footer_parts.extend(tracked_updates)

    message = header + separator + "\n\n".join(deal_texts) + "\n" + "\n".join(footer_parts)
    return message


def check_tracked_lots(current_deals):
    """Compare with previous scan to find price changes and deadline warnings."""
    history_file = "data/deals_history.json"
    updates = []

    if not Path(history_file).exists():
        return updates

    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)

        prev_deals = {d["id"]: d for d in history.get("deals", []) if d.get("id")}
        curr_deals = {d["id"]: d for d in current_deals if d.get("id")}

        for lot_id, curr in curr_deals.items():
            if lot_id in prev_deals:
                prev = prev_deals[lot_id]

                # Price changed
                if prev.get("price", 0) != curr.get("price", 0) and prev.get("price", 0) > 0:
                    old_p = prev["price"]
                    new_p = curr["price"]
                    direction = "dropped" if new_p < old_p else "increased"
                    updates.append(
                        f"  - Lot {lot_id[:8]}: price {direction} to {new_p:,} (was {old_p:,})"
                    )

                # Deadline approaching
                days = curr.get("days_until_deadline")
                if days and days <= 2:
                    updates.append(
                        f"  - Lot {lot_id[:8]}: deadline in {days} day(s)!"
                    )
    except Exception as e:
        updates.append(f"  (history check error: {e})")

    return updates


def save_to_history(deals):
    """Save current deals as history for next comparison."""
    Path("data").mkdir(exist_ok=True)
    history_file = "data/deals_history.json"

    output = {
        "date": datetime.now().isoformat(),
        "deals": deals,
    }

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


def send_telegram(message, dry_run=False):
    """Send message via Telegram Bot API."""
    if dry_run:
        print("\n[DRY RUN] Would send to Telegram:\n")
        print(message)
        return True

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in config.env")
        print("Create a bot via @BotFather, get the token, and find your chat ID.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    # Split long messages (Telegram limit: 4096 chars)
    chunks = []
    if len(message) > 4000:
        lines = message.split("\n")
        chunk = ""
        for line in lines:
            if len(chunk) + len(line) + 1 > 4000:
                chunks.append(chunk)
                chunk = line
            else:
                chunk += "\n" + line if chunk else line
        if chunk:
            chunks.append(chunk)
    else:
        chunks = [message]

    success = True
    for chunk in chunks:
        body = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }).encode("utf-8")

        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if not result.get("ok"):
                    print(f"Telegram API error: {result}")
                    success = False
        except Exception as e:
            print(f"Telegram send error: {e}")
            success = False

    if success:
        print(f"Telegram alert sent ({len(chunks)} message(s))")

    return success


def run(top_n=5, dry_run=False):
    """Load analyzed deals and send alert."""
    analyzed_file = "data/deals_analyzed.json"

    if not Path(analyzed_file).exists():
        print(f"No analyzed data at {analyzed_file}. Run analyzer.py first.")
        return

    with open(analyzed_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    deals = data.get("deals", [])

    if not deals:
        message = f"No deals above {data.get('min_discount', 25)}% discount today."
        send_telegram(message, dry_run)
        return

    message = format_message(deals, top_n)
    sent = send_telegram(message, dry_run)

    if sent and not dry_run:
        save_to_history(deals)
        print("History updated for next comparison.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Send deal alerts to Telegram")
    parser.add_argument("--top", type=int, default=5, help="Number of top deals to send")
    parser.add_argument("--dry-run", action="store_true", help="Print message without sending")
    args = parser.parse_args()

    run(top_n=args.top, dry_run=args.dry_run)
