---
name: marketplace-ai-manager
description: Full AI operations manager for WB/Ozon sellers — reviews, competitor monitoring, analytics, inventory alerts, daily briefing, question answering. Replaces a 40K rub/month assistant.
version: 2.0.0
author: Natalia Brovkina (@NataliyaBrovk)
---

# Marketplace AI Manager

One AI agent that replaces a marketplace operations assistant. Reviews, competitor prices, analytics, inventory, customer questions, daily report. All in Telegram.

## The problem

A WB/Ozon seller with 200+ orders per day juggles 6 tasks every morning:
1. Answer negative reviews (2-3 hours)
2. Check competitor prices (30 min)
3. Look at yesterday's numbers (20 min)
4. Check inventory levels (15 min)
5. Answer customer questions (1 hour)
6. Decide what to restock, reprice, or promote (30 min)

Total: 4-5 hours before you do any actual product work. A human assistant costs 40,000-60,000 rub/month and still makes mistakes.

## What this agent does

Six modules, one Telegram bot. Each runs on its own schedule.

### Module 1: Review Responder
- Every 30 min: pulls unanswered reviews (1-3 stars) from WB/Ozon API
- Generates human-sounding response in your brand voice
- Trigger words (legal threats, injuries) route directly to you without AI draft
- Sends to Telegram: [Send] [Edit] [Skip] buttons
- Posts approved response back to marketplace

### Module 2: Competitor Monitor
- Every 6 hours: checks prices of your top 10 competitors per SKU
- Alerts when competitor drops price by more than 10%
- Alerts when new competitor appears in your category
- Weekly summary: price position map (you vs top 5)

### Module 3: Daily Briefing
- Every morning at 8:00 MSK:
  - Orders yesterday vs 7-day average
  - Revenue MTD vs target
  - Rating change (up/down/stable)
  - Reviews processed by bot (auto/edited/skipped)
  - Top 3 issues from negative reviews (pattern detection)
  - Inventory alerts (see Module 4)

### Module 4: Inventory Alerts
- Every 4 hours: checks stock levels via WB/Ozon API
- Alerts when SKU stock drops below threshold (configurable per SKU)
- Alerts when a fast-selling SKU will run out in < 5 days (velocity-based prediction)
- Weekly: restock recommendation list with quantities

### Module 5: Customer Questions
- Every 30 min: pulls unanswered questions from WB/Ozon
- Drafts answer based on your product cards + FAQ knowledge base
- Sends to Telegram for approval (same flow as reviews)

### Module 6: Analytics Summary (Weekly)
- Every Friday: full week report
  - Revenue, orders, returns, rating
  - Best/worst performing SKUs
  - Competitor price changes
  - Review sentiment trend (getting better or worse?)
  - Action items for next week

## Architecture

```
Cron schedules (n8n or Claude Routines):
  |
  ├── Every 30 min: Review Responder + Question Answerer
  ├── Every 4 hours: Inventory Check
  ├── Every 6 hours: Competitor Monitor
  ├── Every morning 8:00: Daily Briefing
  └── Every Friday 18:00: Weekly Analytics
  
Each module:
  GET data from WB/Ozon API
    → Process (Claude API for text generation, Python for analytics)
    → Send to Telegram (approval buttons for reviews/questions)
    → POST approved responses back to marketplace
    → Log everything to data/
```

## Setup (1-2 hours)

### Prerequisites
- WB API key (seller dashboard > Settings > API Access > all permissions)
- Claude API key (anthropic.com)
- Telegram bot (@BotFather)
- n8n (self-hosted or cloud) OR Claude Routines
- Python 3.10+ for analytics scripts

### Step 1: Get WB API key with ALL permissions
In WB seller dashboard: Settings > API Access > create new key with:
- Reviews and Questions (for modules 1, 5)
- Analytics (for modules 3, 6)
- Prices (for module 2)
- Warehouse/Stocks (for module 4)

### Step 2: Configure
```bash
cp config.example.env config.env
# Fill in: WB_TOKEN, ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
# Set your SKU list, competitor IDs, stock thresholds
```

### Step 3: Add your brand voice
Copy 5-10 of your past review responses into `voice-samples/`. The agent learns your tone.

### Step 4: Set up competitors
Edit `competitors.json`:
```json
{
  "sku_12345": {
    "name": "Your Blue T-shirt XL",
    "competitors": [67890, 11111, 22222],
    "min_stock": 50,
    "target_price": 1500
  }
}
```

### Step 5: Deploy and test
Run each module once manually to verify API connections. Then activate cron schedules.

## Example: Daily Briefing

```
Good morning. Thursday April 18.

ORDERS: 47 yesterday (avg 42, +12%)
REVENUE MTD: 1,420,000 rub (target 1,800K, on track)
RATING: 4.78 (stable, was 4.77 yesterday)

REVIEWS:
  Processed by bot: 12
  Auto-approved: 10 (83%)
  Edited by you: 1
  Skipped: 1
  LEGAL/SAFETY routed to you: 0

TOP ISSUES FROM REVIEWS:
  1. "Delivery slow" — 4 mentions (logistics, not product)
  2. "Size runs small" — 2 mentions (consider updating size chart)
  3. "Color different from photo" — 1 mention

INVENTORY ALERTS:
  SKU 12345 (Blue T-shirt XL): 23 units left, selling 8/day = 3 days supply. RESTOCK NOW.
  SKU 67890 (Black Pants M): 156 units, 12 days supply. OK.

COMPETITORS:
  SKU 12345: competitor #67890 dropped price from 1800 to 1500 rub yesterday (-17%). Your price: 1650. You're now 10% higher.

ACTION ITEMS:
  1. Restock SKU 12345 (urgent, 3 days left)
  2. Decide on price response to competitor #67890
  3. Update size chart for Blue T-shirt line
```

## Adapting for Ozon

Same architecture, different API endpoints:
- Reviews: `https://api-seller.ozon.ru/v1/review/list`
- Products: `https://api-seller.ozon.ru/v2/product/info/list`
- Stock: `https://api-seller.ozon.ru/v1/product/info/stocks`
- Analytics: `https://api-seller.ozon.ru/v1/analytics/data`

Change API URLs and field names in config. Logic stays the same.

## What this agent doesn't do

- Doesn't change prices automatically. Alerts and recommends, you decide.
- Doesn't reorder inventory. Tells you what and how much, you place the order.
- Doesn't handle returns/refunds. Flags them, you process.
- Doesn't auto-send review responses without your approval (configurable after 90%+ approval rate for 2 weeks).
- Doesn't analyze product photos or listing SEO. Text operations only.

## Cost

- Claude API: ~1,500 rub/month for a 200 orders/day store (all 6 modules)
- n8n: free (self-hosted) or $20/month (cloud)
- Telegram bot: free
- WB/Ozon API: free

Compare: human assistant for the same 6 tasks = 40,000-60,000 rub/month.

ROI: pays for itself in week 1. Literally.

## Trigger words (safety)

Reviews/questions containing these words bypass AI and go to you directly:

Legal: мошенники, обман, полиция, суд, роспотребнадзор, претензия, адвокат, иск, компенсация
Safety: травма, ожог, отравление, аллергия, больница, ребёнок
Fraud: подделка, контрафакт, бракованный, истёк срок годности

Full lists in `trigger-words/ru.txt` and `trigger-words/en.txt`.

## Privacy

- Customer review text and names pass through Claude API for response generation
- Competitor data is public (marketplace listings)
- Your sales analytics stay on your server (data/ folder)
- 152-FZ: for 1000+ reviews/day, consider self-hosted n8n on Russian server
- No data shared with third parties beyond Claude API

---

**Made by [Natalia Brovkina](https://t.me/FinanceNatasha)** — former Big 4 finance, now building AI agents for small business.
