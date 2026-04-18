# MAX/VK Bot Migration

Telegram blocked in Russia. Your business bot stopped working. This template rebuilds it on MAX messenger in one evening.

## Quick Start (15-30 minutes)

### Prerequisites
- ИП or ООО (MAX requires business verification)
- Register at business.max.ru/self, create bot, pass moderation, get token
- Node.js 18+

### Install and run

```bash
git clone https://github.com/nibrovkina-cyber/natalia-ai-workflows.git
cd natalia-ai-workflows/max-vk-bot-migration
npm install
cp config.example.env config.env
# Edit config.env: add your BOT_TOKEN and ADMIN_CHAT_ID
BOT_TOKEN="your_token" node bot.js
```

### Customize your FAQ

Edit `faq.json` with your business questions and answers.

## When this is worth it

If you had a working Telegram bot for your business (appointments, FAQ, lead collection) and lost it due to the block. If you never had a bot, start here as your first one.

Not worth it if you have fewer than 10 customer messages per day. At that volume, answer manually.

## What this bot does

- Welcome message with inline keyboard menu (4 buttons)
- FAQ: customer taps a question, gets instant answer from your faq.json
- Appointment booking: date, time, phone number, confirmation, admin notification
- Lead collection: customer writes a question, you get notified in admin chat
- Smart responses (optional): connect Claude API for AI answers to unknown questions

## What to expect week 1

- Day 1: set up bot, add your FAQ (5-10 questions), test with yourself
- Day 2-3: share bot link with 5-10 regular customers, collect feedback
- Day 4-7: expand FAQ based on real questions, adjust responses

## What this doesn't do

- Doesn't process payments
- Doesn't integrate with CRM automatically (export leads.json manually)
- Doesn't support voice/video calls
- Doesn't work without business verification on MAX (ИП/ООО required)

## Cost

Everything free. MAX Bot API, Node.js hosting on free tier (Railway/Render).
Optional: Claude API for smart responses (~$1-3/month).

## More

- [Full documentation with migration guide](SKILL.md)
- [Privacy](SKILL.md#privacy)
