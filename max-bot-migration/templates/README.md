# Templates

Ready-made FAQ files for 3 business types. Pick one, copy to project root, edit with your real answers.

## How to use a template

1. Pick the one closest to your business
2. Copy it to the project root:
```bash
cp templates/salon-beauty.json faq.json
```
3. Open faq.json in any text editor
4. Replace example answers with your real ones (keep the format: `{"question": "...", "answer": "..."}`)
5. Add or remove questions as needed
6. Restart the bot: `npm start`

Don't see your business type? Use blank-template.json and write your own. Tip: export past client messages from Telegram or WhatsApp, find 15 that repeat, those are your FAQ.

## Available templates

| Template | Business type | Questions included |
|---|---|---|
| salon-beauty.json | Hair salon, beauty studio, nail bar | 15 (pricing, booking, hours, location, kids, weddings, gifts) |
| cafe-restaurant.json | Cafe, restaurant, bar | 15 (hours, menu, booking, delivery, parking, allergies, events) |
| autoservice.json | Auto repair, tire shop | 15 (pricing, diagnostics, brands, parts, warranty, tow truck) |
| blank-template.json | Any business | 2 (examples only, fill in your own) |

## For freelancers offering this as a service

Typical MAX bot migration engagement:

1. **Discovery call (15 min, free):** ask the client what their Telegram bot did, how many messages per day, what breaks without it
2. **Check prerequisites:** do they have ИП/самозанятость/ООО? Verified on business.max.ru? If not, help them register (add 2-3 days)
3. **Pick template + customize FAQ:** 30 min with the client. Screen share, go through their real customer questions
4. **Deploy and test:** 1-2 hours. Clone, configure, deploy to Railway, test with the client
5. **Handover:** show them how to edit faq.json, how to check leads.json, how to read admin notifications
6. **30-day support:** answer questions, fix issues. After 30 days, they're on their own or renew

**Typical pricing:**
- Simple bot (FAQ + booking): 15,000 RUB
- Bot + Claude AI smart responses: 20,000 RUB
- Bot + custom integrations (CRM, Google Sheets): 25-30,000 RUB

**What "done-for-you" includes that DIY doesn't:**
- Business-specific FAQ (not template, but researched from their actual client messages)
- Custom welcome message matching their brand
- Railway/hosting setup and monitoring
- First-week tuning based on real conversations
