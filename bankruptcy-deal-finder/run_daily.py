"""
Bankruptcy Deal Finder — Daily Pipeline
Runs the full scan -> analyze -> alert cycle.

Usage:
    python run_daily.py              # Full pipeline, send Telegram alert
    python run_daily.py --dry-run    # Full pipeline, print only
"""

import sys
import argparse
from datetime import datetime

from scraper import scan_all, save_results
from analyzer import analyze_lots, save_analyzed
from alerter import run as send_alerts


def main():
    parser = argparse.ArgumentParser(description="Run full daily pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Print results without sending Telegram")
    parser.add_argument("--top", type=int, default=5, help="Number of deals in alert")
    parser.add_argument("--min-discount", type=int, help="Override minimum discount %%")
    args = parser.parse_args()

    start = datetime.now()
    print(f"\n{'='*60}")
    print(f"Bankruptcy Deal Finder — Daily Run")
    print(f"Started: {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    # Step 1: Scan
    print("\n[Step 1/3] Scanning auction platforms...")
    lots = scan_all()
    if lots:
        save_results(lots)
    else:
        print("No lots found. Check your config.env criteria.")

    # Step 2: Analyze
    print("\n[Step 2/3] Analyzing deals...")
    deals = analyze_lots(min_discount=args.min_discount)
    if deals:
        save_analyzed(deals)

    # Step 3: Alert
    print("\n[Step 3/3] Sending alert...")
    send_alerts(top_n=args.top, dry_run=args.dry_run)

    elapsed = (datetime.now() - start).total_seconds()
    print(f"\nPipeline complete in {elapsed:.1f} seconds.")
    print(f"Lots scanned: {len(lots)}")
    print(f"Deals found: {len(deals)}")


if __name__ == "__main__":
    main()
