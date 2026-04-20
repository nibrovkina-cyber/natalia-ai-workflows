---
name: max-bot-migration
description: Migrate your Telegram business bot to MAX messenger. Template bot with menu, FAQ, appointment booking, lead collection. Works without Telegram.
version: 1.1.0
author: Natalia Brovkina (@NataliyaBrovk)
---

# MAX Bot Migration

Telegram blocked in Russia. Your business bot stopped working. This skill helps you rebuild it on MAX messenger in one evening.

## The problem

Telegram is blocked for millions of Russian users. If your business runs on a Telegram bot (orders, FAQ, appointments, notifications), you lost that channel overnight. MAX messenger (max.ru) is the main alternative with an open Bot API.

## What this skill does

1. Provides a ready-made business bot template for MAX with:
   - Welcome message + menu with buttons
   - FAQ auto-responder (reads your questions from a file)
   - Appointment booking (date + time + contact)
   - Lead collection (name, phone, question)
   - Notification forwarding to admin chat
   - AI-powered smart responses via Claude API (optional)

2. Migration guide: how to move your existing Telegram bot logic to MAX

## Architecture

```
User in MAX messenger
  |
  Sends message / taps button
  |
  MAX Bot API (platform-api.max.ru)
    |
    Your bot (Node.js)
      |
      /start - Welcome + inline keyboard menu
      "FAQ" button - Search faq.json, return answer
      "Book appointment" - Collect date, time, contact, save + notify admin
      "Ask question" - Collect text, (optional) Claude API, respond + notify admin
      Unknown input - "I didn't understand. Here's the menu:" + keyboard
```

## MAX Bot API (key info)

- Base URL: `https://platform-api.max.ru`
- Auth: `Authorization: <token>` header (NOT query param)
- Rate limit: 30 requests/second
- Send message: `POST /messages` with `chat_id` and text
- Receive updates: Webhook (HTTPS only) or Long Polling (`GET /updates`)
- Inline keyboard: up to 210 buttons, 30 rows, 7 per row
- Button types: callback, link, request_contact, request_geo_location, message, clipboard
- Text formatting: Markdown or HTML (set `format` field)
- Official JS library: `@maxhub/max-bot-api` (npm)
- Docs: https://dev.max.ru/docs-api

**Important:** MAX bots require a verified business profile (ИП, самозанятость, or ООО). Register at https://business.max.ru/self

## Setup

### Prerequisites
- ИП, самозанятость, or ООО (required by MAX for bot creation)
- Register at https://business.max.ru/self
- Create bot, pass moderation, get token
- Node.js 18+

### Step 1: Install

```bash
git clone https://github.com/nibrovkina-cyber/natalia-ai-workflows.git
cd natalia-ai-workflows/max-bot-migration
npm install
```

### Step 2: Pick a template

```bash
# Choose your business type:
cp templates/salon-beauty.json faq.json        # Hair salon, beauty
cp templates/cafe-restaurant.json faq.json     # Cafe, restaurant
cp templates/autoservice.json faq.json         # Auto repair
cp templates/blank-template.json faq.json      # Start from scratch
```

Edit faq.json with your actual questions and answers.

### Step 3: Configure

```bash
cp config.example.env config.env
# Edit config.env: add BOT_TOKEN and ADMIN_CHAT_ID
```

### Step 4: Test locally

```bash
npm start
```

Open MAX messenger, find your bot, send /start.

### Step 5: Deploy to Railway (one-click)

See README.md for the deploy button.

## Migration from Telegram

If you have an existing Telegram bot, here's what changes:

| Telegram | MAX | What to change |
|---|---|---|
| `api.telegram.org/bot<token>` | `platform-api.max.ru` | Base URL |
| Token in URL path | `Authorization: <token>` header | Auth method |
| `sendMessage` | `POST /messages` | Method name |
| `getUpdates` | `GET /updates` | Same concept |
| `InlineKeyboardMarkup` | `InlineKeyboardAttachment` | Keyboard format |
| `ReplyKeyboardMarkup` | Not supported in MAX | Use inline keyboard instead |
| `callback_data` | `payload` in callback button | Field name |
| `BotFather` | business.max.ru | Bot creation |
| No verification needed | ИП/ООО required | Business requirement |

**Key differences:**
- MAX requires HTTPS for webhooks (including self-signed certs)
- MAX token goes in header, not URL
- MAX has no ReplyKeyboard, only inline
- MAX requires business verification (ИП/самозанятость/ООО)
- MAX rate limit: 30 rps (Telegram: 30 msg/sec per chat)

## What this bot template includes

| Feature | How it works |
|---|---|
| Welcome + menu | Inline keyboard with 4 buttons on /start |
| FAQ | Fuzzy search in faq.json, returns best match |
| Appointment booking | 3-step flow: date, time, contact, confirm + notify admin |
| Lead collection | Name + phone + question, save to leads.json + notify admin |
| AI responses (optional) | If Claude API key set, unknown questions get AI answer based on your FAQ |
| Admin notifications | All bookings and leads forwarded to admin chat |

## What this bot doesn't do

- Doesn't process payments (use separate payment links)
- Doesn't integrate with CRM automatically (you export leads.json manually or add webhook)
- Doesn't support voice/video calls (MAX API limitation)
- Doesn't work without business verification on MAX (ИП/самозанятость/ООО required)
- Doesn't support multiple languages (Russian only in templates, you can translate faq.json)
- Doesn't support real-time availability checking (booking is request-based, not calendar-synced)

## Planned for v2

- [ ] Webhook mode instead of long polling (for production)
- [ ] Rate limiting for admin notifications
- [ ] Duplicate booking detection (idempotency)
- [ ] Winston logging
- [ ] Demo mode (`npm run demo`)
- [ ] Unit and integration tests

## Cost

- MAX Bot API: free
- Claude API (optional, for smart responses): ~$1-3/month for small business
- Hosting: free on Railway/Render starter plan, or your own server

## Privacy

- User messages pass through your server only
- If Claude API enabled: user questions pass through Anthropic servers
- leads.json and bookings stored locally on your server
- No data shared with third parties (except Claude API if enabled)
- 152-FZ: all data stays on your Russian server if self-hosted

---

**[Natalia Brovkina](https://t.me/FinanceNatasha)** - AI Change Manager. Former Big 4 and Big Tech finance.
