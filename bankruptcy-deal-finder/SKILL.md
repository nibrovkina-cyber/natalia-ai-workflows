---
name: bankruptcy-deal-finder
description: AI agent that monitors torgi.gov.ru for bankruptcy auction deals, finds undervalued assets, calculates discount to market price, and alerts via Telegram
version: 1.0.0
author: Natalia Brovkina (@NataliyaBrovk)
---

# Bankruptcy Deal Finder

AI agent that scans Russian bankruptcy auction platforms daily, finds assets selling below market value, and sends you a Telegram alert with the analysis.

## What problem this solves

Thousands of lots appear on torgi.gov.ru every day. Apartments, commercial real estate, vehicles, equipment. Many sell at 30-60% below market price. But finding the good deals manually takes 2-4 hours of scrolling, comparing, and calculating.

This agent does it in 5 minutes every morning.

## What it does

1. **Scans** torgi.gov.ru for new lots matching your criteria (region, asset type, price range)
2. **Filters** by your parameters: only apartments in Moscow, only commercial real estate in SPb, only vehicles under 2M rub
3. **Estimates market price** by comparing with Cian, Avito, or DomClick listings in the same area
4. **Calculates discount**: lot price vs estimated market price
5. **Ranks** deals by discount percentage (best deals first)
6. **Alerts you** via Telegram: "Apartment in Krasnogorsk, 54 sqm, starting price 3.2M, market est. 7.1M, discount ~55%, auction deadline April 25"
7. **Tracks** lots you marked as interesting and alerts when price changes or deadline approaches

## Architecture

```
Daily at 8:00 AM (cron):
  
  scraper.py
    ├── GET torgi.gov.ru/new/public/lots/reg (filtered by criteria)
    └── Parse: lot_id, title, location, price, deadline, asset_type
  
  analyzer.py (Claude API)
    ├── For each lot: estimate market price
    ├── Calculate discount percentage
    ├── Score: discount * liquidity * deadline_urgency
    └── Filter: only discount > 25%
  
  alerter.py
    ├── Format top 5 deals as Telegram message
    ├── Send via Telegram Bot API
    └── Log to deals_history.json (track what was sent)
```

## Data sources

| Source | URL | What it has | Access |
|---|---|---|---|
| torgi.gov.ru | torgi.gov.ru/new/public/lots/reg | All government auctions: real estate, land, vehicles, equipment | Public, no auth needed |
| bankrot.fedresurs.ru | bankrot.fedresurs.ru | Bankruptcy-specific lots, debtor info, court decisions | Public, parser-api.com has API ($). Not implemented in v1, planned for v2 |
| Cian (for price comparison) | cian.ru | Apartment/commercial real estate market prices | Public listings |
| Avito (for price comparison) | avito.ru | Vehicles, equipment market prices | Public listings |

## Setup

### Prerequisites

- Python 3.10+
- Claude API key (for market price analysis)
- Telegram bot token (from @BotFather)
- (Optional, v2) parser-api.com account for bankrot.fedresurs.ru (not yet implemented)

### Configuration

Copy `config.example.env` and fill in:

```bash
ANTHROPIC_API_KEY=sk-ant-...          # Claude API for analysis
TELEGRAM_BOT_TOKEN=123456:ABC...      # Your Telegram bot
TELEGRAM_CHAT_ID=123456789            # Your Telegram chat/group
REGIONS=moscow,spb,krasnogorsk        # Regions to monitor
ASSET_TYPES=apartment,commercial      # Asset types
MIN_DISCOUNT=25                       # Minimum discount % to alert
MAX_PRICE=15000000                    # Maximum lot price in rubles
SCAN_INTERVAL=daily                   # daily or twice_daily
```

### Install and run

```bash
pip install -r requirements.txt
python scraper.py          # Test: scan once and print results
python analyzer.py         # Test: analyze found lots
python alerter.py          # Test: send Telegram alert

# Or run full pipeline:
python run_daily.py
```

### Set up daily schedule

Option A (Claude Routines): create a Remote Trigger with cron `0 5 * * *` (8:00 MSK)

Option B (cron on your server):
```bash
crontab -e
0 5 * * * cd /path/to/bankruptcy-deal-finder && python run_daily.py
```

## Example output (Telegram alert)

```
🏠 Top 5 deals - April 18, 2026

1. Apartment, Krasnogorsk, 54 sqm
   Starting price: 3,200,000 rub
   Market estimate: ~7,100,000 rub
   Discount: ~55%
   Auction deadline: April 25
   Link: torgi.gov.ru/lot/123456

2. Commercial space, Moscow, Taganka, 120 sqm
   Starting price: 8,500,000 rub
   Market estimate: ~15,000,000 rub
   Discount: ~43%
   Auction deadline: April 28
   Link: torgi.gov.ru/lot/789012

3. Parking space, SPb, Primorsky, 18 sqm
   Starting price: 450,000 rub
   Market estimate: ~900,000 rub
   Discount: ~50%
   Auction deadline: April 22
   Link: torgi.gov.ru/lot/345678

[3 more deals...]

Tracked lots update:
- Lot #112233 (apartment Mytishchi): price dropped to 2.8M (was 3.1M)
- Lot #445566 (commercial Samara): deadline tomorrow!
```

## Edge cases

| Case | How agent handles it |
|---|---|
| No lots match criteria today | Sends "No deals above 25% discount today. 47 lots scanned." |
| Lot has no clear asset description | Skips, logs as "unclassified" |
| Market price impossible to estimate (rare asset type) | Flags as "manual review needed", sends raw data |
| Auction cancelled/postponed | Detects status change, alerts "Lot #X cancelled" |
| Same lot appears on both platforms | Deduplicates by address + price |
| API rate limit on torgi.gov.ru | Respects 1 req/sec, retries with backoff |

## What this agent doesn't do

- Doesn't bid on auctions for you. Analysis only.
- Doesn't verify legal status of the lot (encumbrances, liens). You need a lawyer for that.
- Doesn't guarantee market price estimates are accurate. They're based on comparable listings, not appraisals.
- Doesn't work for non-Russian auction platforms. Currently torgi.gov.ru only. bankrot.fedresurs.ru planned for v2.
- Doesn't handle auctions requiring special permits (military property, cultural heritage sites).

## Cost

- Claude API: ~$0.01-0.05 per daily scan (depends on lot count)
- parser-api.com (v2, not yet): from 1,500 rub/month for fedresurs data
- Telegram bot: free
- Total: ~$3-10/month

## Privacy

- Auction data is public by law (Federal Law 44-FZ, 127-FZ)
- No personal data is processed (lot descriptions only)
- Your search criteria stored locally in config.env
- Telegram alerts go only to your chat

---

**[Natalia Brovkina](https://t.me/FinanceNatasha)** - AI Change Manager. Former Big 4 and Big Tech finance.
