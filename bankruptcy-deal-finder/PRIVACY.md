# Privacy

## Data flow

```
torgi.gov.ru (public auction data)
  |
  scraper.py (your machine)
  |
  Lot descriptions + prices (NO personal data)
  |
  Claude API (Anthropic servers) — for market price estimation
  |
  Analyzed deals (your machine, data/ folder)
  |
  Telegram Bot API — sends alert to YOUR chat only
```

## What data is processed

- Lot descriptions (asset type, address, area, starting price)
- Auction dates and deadlines
- Status changes (active, cancelled, postponed)

## What data is NOT processed

- No personal data of debtors (names, passport numbers, etc.)
- No bidder information
- No financial details beyond publicly listed starting prices

## Legal basis

All auction data on torgi.gov.ru and bankrot.fedresurs.ru is public by law:
- Federal Law 44-FZ (government procurement)
- Federal Law 127-FZ (bankruptcy proceedings)
- EFRSB regulations require public disclosure of all bankruptcy auction lots

Scraping public auction data for personal use does not violate Russian law. However:
- Do not redistribute scraped data at commercial scale without legal review
- Do not scrape at rates that could be considered a denial-of-service attack (the agent uses 1 req/sec)
- torgi.gov.ru terms of service may change; check periodically

## Where data is stored

- All data stays on your machine in the `data/` folder
- Claude API processes lot descriptions for market price estimation (review Anthropic's data retention policy)
- Telegram alerts go only to your configured chat ID
- No data is sent to any other third party

## Recommendations

- Don't share your `data/deals_analyzed.json` publicly if it contains your investment criteria (competitors could use it)
- Rotate your Telegram bot token if you suspect it's compromised
- The `config.env` file contains your API keys; keep it in .gitignore (already configured)
