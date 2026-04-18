# Bankruptcy Deal Finder

Scans Russian bankruptcy auction platforms daily, finds assets selling below market value, sends you a Telegram alert.

## Quick Start (5 minutes)

1. Clone:
```bash
git clone https://github.com/nibrovkina-cyber/natalia-ai-workflows.git
cd natalia-ai-workflows/bankruptcy-deal-finder
```

2. Install:
```bash
pip install -r requirements.txt
```

3. Configure:
```bash
cp config.example.env config.env
# Edit config.env: add your ANTHROPIC_API_KEY and TELEGRAM_BOT_TOKEN
```

4. Test:
```bash
python run_daily.py --dry-run
```

5. Run for real:
```bash
python run_daily.py
```

## When this is worth it

If you actively bid on bankruptcy auctions and check torgi.gov.ru manually more than 3 times per week, this saves 2-4 hours daily.

If you check auctions once a month or less, this is overkill. Stick with manual search.

## What good output looks like

See [examples/edge-cases.md](examples/edge-cases.md) for how the agent handles unusual situations.

A typical morning alert in Telegram:
- 5 deals above 25% discount
- Each with: price, estimated market value, discount %, deadline, link
- Tracked lots: price changes and approaching deadlines

## What to expect week 1

- Day 1-2: tune filters. Many irrelevant lots. Adjust regions, asset types, MIN_DISCOUNT in config.
- Day 3-5: estimates stabilize. Mark lots you would actually bid on.
- Day 6-7: agent runs reliably. You check alerts in 2 minutes.

## What this doesn't do

- Doesn't bid on auctions for you
- Doesn't verify legal status of lots (encumbrances, liens)
- Doesn't guarantee market price estimates are accurate
- Doesn't cover non-Russian platforms

## Cost

Claude API: ~$1-3/month. Telegram: free. torgi.gov.ru: free.

## More

- [Full documentation](SKILL.md)
- [Edge cases](examples/edge-cases.md)
- [How to measure if it's working](OBSERVABILITY.md)
- [Privacy and data flow](PRIVACY.md)
