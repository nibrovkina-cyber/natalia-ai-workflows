# Observability

How to know if the Bankruptcy Deal Finder is working well.

## What to log

Every daily run produces:

| What | File | Purpose |
|---|---|---|
| Raw scan results | `data/lots_raw.json` | All lots found before filtering |
| Analyzed deals | `data/deals_analyzed.json` | Lots that passed discount threshold |
| Deal history | `data/deals_history.json` | Previous day's deals for comparison |
| Telegram messages sent | `data/alerts_log.json` | What was sent, when |

## Three metrics that matter

### 1. Scan coverage
**What:** How many lots did the scanner find vs how many exist on the platform?
**How to check:** Compare your `total_lots` in lots_raw.json with the number shown on torgi.gov.ru when you search manually with the same filters.
**Target:** 80%+ coverage. If your scanner finds 40 lots but the website shows 55, you have a filter or pagination issue.

### 2. Estimate accuracy
**What:** How close are the market price estimates to reality?
**How to check:** For 5-10 lots per month, manually look up the actual market price on Cian/Avito. Compare with the agent's estimate.
**Target:** Within 20% for apartments, within 30% for commercial. If estimates are consistently off by 40%+, the regional price data needs updating.

### 3. Actionable deal rate
**What:** Of the deals the agent flags, how many did you actually consider bidding on?
**How to check:** Track "viewed" vs "serious interest" vs "bid" for each alert.
**Target:** At least 1 in 5 flagged deals should be worth investigating further. If you're dismissing 95% of alerts, either the discount threshold is too low or the quality filters need tightening.

## Week-by-week expectations

| Week | What to expect |
|---|---|
| Week 1 | Tune filters. Many irrelevant lots. Adjust regions, asset types, MIN_DISCOUNT. |
| Week 2 | Estimates stabilize. Mark lots you'd actually bid on. |
| Week 3 | Pattern emerges: which regions and asset types have best deals. |
| Week 4 | Agent runs reliably. You check alerts in 2 minutes and act on 1-2 per week. |

## What to do if it's not working

- **Too many alerts:** Raise MIN_DISCOUNT from 25% to 35%.
- **Too few alerts:** Add more regions or lower MAX_PRICE.
- **Estimates way off:** Check if the avg_prices in analyzer.py match current market. Update quarterly.
- **Scanner finds 0 lots:** Check if torgi.gov.ru changed their API. Test the URL manually in browser.
