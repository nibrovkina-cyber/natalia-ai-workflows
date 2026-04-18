---
name: wb-review-responder
description: AI agent that monitors Wildberries/Ozon reviews, drafts brand-voice responses to negative feedback, sends to Telegram for approval, posts approved replies via API
version: 1.0.0
author: Natalia Brovkina (@NataliyaBrovk)
---

# WB Review Responder

AI agent for marketplace sellers. Reads negative reviews, writes human-sounding responses in your brand voice, sends drafts to Telegram for approval, posts approved replies back to the platform.

## The problem

A WB/Ozon seller with 100+ reviews per month spends 2-4 hours daily on responses. Most responses are similar. Missing negative reviews drops your rating; a drop from 4.8 to 4.5 on WB means ~15% less search traffic.

## What it does

Every 30 minutes:
1. Pulls unanswered reviews from WB API (rating 1-3 stars)
2. Checks for trigger words (legal threats, injury claims) and routes those directly to you without AI draft
3. For regular negative reviews: generates a response in your brand voice (2-4 sentences, warm but honest, no corporate speak)
4. Sends draft to your Telegram with three buttons: Send as is / Edit / Skip
5. Posts approved response back to WB via API

## Results (from real usage)

- Review response time: from 3 hours to 10 minutes daily
- Rating recovery: 4.5 to 4.8 in 3 weeks (one seller)
- Approval rate without edits: 85-90% after voice tuning (day 5+)
- Cost: ~500 rub/month (Claude API) vs 40,000 rub/month (human assistant)

## When this is worth it

If your store does 200+ reviews per month with 20%+ negative, this pays for itself in week 1. Under 100 reviews per month, setup time exceeds the saving. Wait until volume grows or handle manually.

## Architecture

```
Cron (every 30 min)
  |
  GET /api/v1/feedbacks?isAnswered=false (WB API)
  |
  Filter: rating <= 3 AND not yet processed
  |
  For each review:
    |
    IF trigger_words detected (legal, injury, fraud):
      -> Send to Telegram WITHOUT AI draft ("Manual review needed")
    ELSE:
      -> Claude API: generate response using brand voice + few-shot examples
      -> Send to Telegram WITH draft
        |
        Manager response:
          [Send] -> POST /api/v1/feedbacks/answer (WB API)
          [Edit] -> Manager edits, then POST
          [Skip] -> Log as skipped
```

## Setup (30-60 minutes)

### Prerequisites

- n8n (self-hosted free or n8n.cloud $20/month)
- WB API key (free, from seller dashboard: Settings > API Access > "Reviews and Questions")
- Claude API key (anthropic.com)
- Telegram bot token (from @BotFather, free)

### Step 1: Import workflow

Import `workflow/wb-review-responder.n8n.json` into n8n:
Workflows > + New > Menu > Import from File

### Step 2: Configure credentials

| Node | What to set |
|---|---|
| HTTP Request (Get Reviews) | `Authorization: Bearer YOUR_WB_TOKEN` |
| Claude API | API key in n8n credentials |
| Telegram Notify | Bot token + Chat ID |
| HTTP Request (Send Answer) | Same WB Token |

### Step 3: Add your brand voice

Copy 5-10 of your actual past review responses into `voice-samples/`. The agent uses these as few-shot examples to match your tone.

### Step 4: Customize trigger words

Edit `trigger-words/ru.txt` to add industry-specific terms. Default list covers legal threats, injury claims, fraud accusations.

### Step 5: Activate and test

1. Run workflow manually once to verify it connects to WB API
2. Check Telegram for test message
3. Approve one response and verify it posts to WB
4. Switch to automatic (cron every 30 min)

## Response prompt

The core prompt instructs Claude to write responses that:
- Address the customer by name (if available)
- Acknowledge the specific problem (not generic "sorry for inconvenience")
- State a concrete next step (what happens next for the customer)
- Stay under 4 sentences
- Never promise specific timelines, refunds, or things outside your control
- Never use corporate phrases: "we value your feedback", "we apologize for any inconvenience"

Full prompt with few-shot examples: `prompts/response-prompt-ru.md`

## Trigger words (safety layer)

Reviews containing these words bypass AI and go directly to you for manual response:

**Legal:** мошенники, обман, полиция, суд, роспотребнадзор, претензия, ЗПП, прокуратура, адвокат, иск, компенсация морального

**Health/Safety:** травма, ожог, отравление, аллергия, больница, ребёнок

**Fraud:** подделка, контрафакт, несертифицированный, бракованный, истёк срок годности

Full list in `trigger-words/ru.txt` (30+ words) and `trigger-words/en.txt` (for Etsy/Shopify sellers).

## Edge cases

| Case | How agent handles |
|---|---|
| Review is only emoji/1 word | Generates generic acknowledgment, flags for review |
| Review in a foreign language | Detects language, responds in same language or flags |
| Customer threatens lawsuit | Skips AI, sends to manager as "LEGAL: manual review" |
| Product injury claim | Skips AI, sends as "SAFETY: manual review" |
| Review about delivery (not product) | Responds about delivery process, not product quality |
| Repeat complaint from same customer | Detects by name, flags "recurring complaint" |
| Review already answered (race condition) | Checks before posting, skips if answered |

## Adapting for other platforms

| Platform | What to change |
|---|---|
| Ozon | Replace API endpoints (check seller API docs), adjust field names |
| Etsy | Use Etsy Open API, switch to English prompts (`prompts/response-prompt-en.md`) |
| Shopify | Shopify Reviews API or Judge.me/Yotpo API |
| Amazon | Amazon SP-API (requires approval) |

## What this agent doesn't do

- Doesn't respond to positive reviews (4-5 stars). You should still thank customers personally for genuine praise.
- Doesn't analyze review trends. If 50 customers complain about the same seam, this agent answers each one individually. You need a separate analytics step to spot patterns.
- Doesn't auto-send without approval. Every response goes through Telegram first. You can switch to auto-send after 2 weeks of 90%+ approval rate, but we don't recommend it.
- Doesn't handle refund decisions. Flags and drafts, never commits to money.

## Cost

- Claude API: ~0.003 rub per review response, ~500 rub/month for 200 reviews/day store
- n8n: free (self-hosted) or $20/month (cloud)
- Telegram bot: free
- WB API: free

Compare: human assistant for the same task costs 40,000-60,000 rub/month.

## Privacy

- Review text and customer names pass through Claude API. Review Anthropic's data retention policy.
- For stores processing 1000+ reviews/day with Russian customer PII: 152-FZ data localization may apply. Consider self-hosted n8n + Claude API with EU endpoint.
- All processed review IDs and responses are logged locally in n8n. No data is sent to third parties beyond Claude API.

---

**Made by [Natalia Brovkina](https://t.me/FinanceNatasha)** — former Big 4 finance, now building AI agents for small business.
