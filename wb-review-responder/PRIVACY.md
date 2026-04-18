# Privacy

## Data flow

```
WB API (customer reviews)
  |
  n8n (your server or n8n.cloud)
  |
  Review text + customer name + product info
  |
  Claude API (Anthropic servers) — generates response draft
  |
  Telegram Bot API — sends draft to your chat
  |
  You approve/edit
  |
  WB API — posts response
```

## What data touches Claude API

- Customer's review text (may include their name, order details)
- Product name and article number
- Your brand voice samples

## Customer PII

Customer reviews on WB contain:
- Customer first name (always)
- Their review text (may mention personal details)
- Product they purchased

This data passes through Claude API for response generation. Review Anthropic's data retention policy.

## 152-FZ considerations (Russia)

For stores processing 1000+ reviews per day with Russian customer PII:
- 152-FZ data localization requirements may apply
- Consider self-hosted n8n (Docker, Russian server) instead of n8n.cloud (EU servers)
- Claude API processes data on Anthropic servers (US/EU). For strict 152-FZ compliance, consult a lawyer.

For stores under 1000 reviews/day: risk is low, standard WB seller agreement already covers review processing.

## GDPR (if you sell on Etsy/Shopify to EU customers)

- Customer reviews from EU buyers are subject to GDPR
- You are the data controller, Anthropic is the processor
- Check if your use case requires a signed DPA with Anthropic

## No tracking

This agent does not phone home or send data anywhere except:
- Claude API (for response generation)
- Telegram Bot API (for your approval workflow)
- WB API (for posting approved responses)

All logs stay in your n8n instance.
