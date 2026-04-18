---
name: max-vk-bot-migration
description: Migrate your Telegram business bot to MAX and VK. Template bot with menu, FAQ, appointment booking, lead collection. Works without Telegram.
version: 1.0.0
author: Natalia Brovkina (@NataliyaBrovk)
---

# MAX/VK Bot Migration

Telegram blocked in Russia. Your business bot stopped working. This skill helps you rebuild it on MAX and VK in one evening.

## The problem

Telegram is blocked for millions of Russian users. If your business runs on a Telegram bot (orders, FAQ, appointments, notifications), you lost that channel overnight. MAX messenger (max.ru) and VK are the two main alternatives with open Bot APIs.

## What this skill does

1. Provides a ready-made business bot template for MAX (and VK) with:
   - Welcome message + menu with buttons
   - FAQ auto-responder (reads your questions from a file)
   - Appointment booking (date + time + contact)
   - Lead collection (name, phone, question)
   - Notification forwarding to admin chat
   - AI-powered smart responses via Claude API (optional)

2. Migration guide: how to move your existing Telegram bot logic to MAX/VK

## Architecture

```
User in MAX messenger
  |
  Sends message / taps button
  |
  MAX Bot API (platform-api.max.ru)
    |
    Your bot (Node.js or Python)
      |
      ├── /start → Welcome + inline keyboard menu
      ├── "FAQ" button → Search faq.json, return answer
      ├── "Book appointment" → Collect date, time, contact → save + notify admin
      ├── "Ask question" → Collect text → (optional) Claude API → respond + notify admin
      └── Unknown input → "I didn't understand. Here's the menu:" + keyboard
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

**Important:** MAX bots require a verified business profile (ИП or ООО). Register at https://business.max.ru/self

## VK Bot API (key info)

- Base URL: `https://api.vk.com/method/`
- Auth: access_token parameter
- Send message: `messages.send`
- Receive updates: Long Poll or Callback API
- Keyboard: up to 10 buttons per row, 40 total
- Docs: https://dev.vk.com/api/bots/getting-started

**VK bots work from community (group) pages.** No business verification needed.

## Setup (MAX)

### Prerequisites
- ИП or ООО (required by MAX for bot creation)
- Register at https://business.max.ru/self
- Create bot, pass moderation, get token
- Node.js 18+ or Python 3.10+

### Step 1: Install

```bash
# Node.js
mkdir my-max-bot && cd my-max-bot
npm install @maxhub/max-bot-api dotenv

# Or Python (use requests + polling)
pip install requests python-dotenv
```

### Step 2: Configure

```bash
cp config.example.env config.env
# Edit: add your MAX bot token
```

### Step 3: Add your FAQ

Edit `faq.json`:
```json
[
  {"question": "Как записаться", "answer": "Напишите дату и время, мы подтвердим в течение часа."},
  {"question": "Цены", "answer": "Стрижка от 1500 руб, окрашивание от 3000 руб. Полный прайс: [ссылка]"},
  {"question": "Адрес", "answer": "Москва, ул. Пушкина 10, 2 этаж. Метро Тверская, 5 минут пешком."}
]
```

### Step 4: Run

```bash
# Node.js
BOT_TOKEN="your_token" node bot.js

# Python
BOT_TOKEN="your_token" python bot.py
```

### Step 5: Test

Open MAX messenger, find your bot, send /start. You should see the welcome message with buttons.

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
- MAX requires business verification (ИП/ООО)
- MAX rate limit: 30 rps (Telegram: 30 msg/sec per chat)

## What this bot template includes

| Feature | How it works |
|---|---|
| Welcome + menu | Inline keyboard with 4 buttons on /start |
| FAQ | Fuzzy search in faq.json, returns best match |
| Appointment booking | 3-step flow: date → time → contact → confirm + notify admin |
| Lead collection | Name + phone + question → save to leads.json + notify admin |
| AI responses (optional) | If Claude API key set, unknown questions get AI answer based on your FAQ |
| Admin notifications | All bookings and leads forwarded to admin chat |

## Edge cases

| Case | How bot handles |
|---|---|
| User sends voice message | "I can only read text messages. Please type your question." |
| User sends image | "Thanks for the image. For questions, please use the menu buttons or type your question." |
| FAQ no match found | "I don't have an answer for that. Let me forward your question to our manager." → notify admin |
| Booking with past date | "That date has already passed. Please choose a future date." |
| Phone number invalid format | "Please enter a phone number starting with +7 or 8, 11 digits." |
| Bot added to group chat | Works in groups if enabled in MAX settings. Responds only to direct mentions or /commands. |

## What this bot doesn't do

- Doesn't process payments (use separate payment links)
- Doesn't integrate with CRM automatically (you export leads.json manually or add webhook)
- Doesn't support voice/video calls (MAX API limitation)
- Doesn't work without business verification on MAX (ИП/ООО required)
- VK version doesn't support inline keyboard styling (VK has its own keyboard format)

## Cost

- MAX Bot API: free
- VK Bot API: free
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

**Video tutorial:** [YouTube link - coming soon]
