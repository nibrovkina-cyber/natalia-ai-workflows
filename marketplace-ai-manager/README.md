# Marketplace AI Manager

AI operations manager for WB/Ozon sellers. Reviews, competitor prices, inventory alerts, daily briefing, customer questions. One Telegram bot replaces a 40K rub/month assistant.

## Quick Start (30-60 minutes)

1. Get your WB API key: seller dashboard > Settings > API Access > all permissions
2. Create a Telegram bot via @BotFather
3. Get a Claude API key from anthropic.com

```bash
git clone https://github.com/nibrovkina-cyber/natalia-ai-workflows.git
cd natalia-ai-workflows/marketplace-ai-manager
cp config.example.env config.env
# Edit config.env with your keys
```

4. Add your brand voice: copy 5-10 of your past review responses into `voice-samples/`
5. Import the n8n workflow (see [SKILL.md](SKILL.md) for setup details)

## When this is worth it

If your store does 200+ reviews per month with 20%+ negative, and you spend 2+ hours daily on operational tasks. Under 100 reviews per month, handle manually.

## Six modules

1. **Review Responder** (every 30 min): AI drafts responses, you approve in Telegram
2. **Competitor Monitor** (every 6 hours): alerts when competitor drops price 10%+
3. **Daily Briefing** (every morning): orders, revenue, rating, issues, inventory
4. **Inventory Alerts** (every 4 hours): low stock warnings with restock recommendations
5. **Customer Questions** (every 30 min): AI drafts answers to buyer questions
6. **Weekly Analytics** (Fridays): full report with action items

Currently implemented: Module 1 (Review Responder) with trigger words safety layer. Modules 2-6 use the same architecture and WB API endpoints described in SKILL.md.

## What to expect week 1

- Day 1-2: 50% of review drafts need editing. Normal.
- Day 3-5: add more voice samples. Edit rate drops to 20%.
- Day 6-7: 85%+ approval rate without edits.

## What this doesn't do

- Doesn't change prices automatically
- Doesn't reorder inventory
- Doesn't auto-send without your approval
- Doesn't analyze product photos or listing SEO

## Cost

Claude API: ~1,500 rub/month. n8n: free (self-hosted). Telegram: free.
Compare: human assistant = 40,000-60,000 rub/month.

## More

- [Full documentation with all 6 modules](SKILL.md)
- [Before/after gallery (10 examples)](examples/before-after-gallery.md)
- [Edge cases](examples/edge-cases.md)
- [Privacy (152-FZ, GDPR)](PRIVACY.md)
