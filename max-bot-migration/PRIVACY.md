# Privacy

## Data flow

```
Customer in MAX messenger
  |
  MAX Bot API (platform-api.max.ru)
  |
  Your server (Node.js bot)
  |
  ├── FAQ responses: no external calls, local faq.json
  ├── Bookings: saved locally to data/bookings.json
  ├── Leads: saved locally to data/leads.json
  └── Smart responses (optional): Claude API (Anthropic servers)
```

## What data is stored

- Customer name (from MAX profile)
- Phone number (from booking flow, entered by customer)
- Questions text (from lead collection)
- Booking dates and times

## 152-FZ (Russia)

Customer phone numbers and names are personal data under 152-FZ.

If self-hosted on a Russian server: compliant by default.
If hosted on Railway/Render (EU/US servers): consult a lawyer for stores processing 1000+ customers/month.

For most small businesses (under 1000 customers/month): risk is low, standard business practices apply.

## Recommendations

- Host on a Russian server if possible (any VPS with Docker)
- Don't share data/leads.json or data/bookings.json publicly
- Delete old booking data after 6 months (GDPR best practice)
- If using Claude API for smart responses: customer question text passes through Anthropic servers
- Rotate your MAX bot token if compromised

## No tracking

Bot does not send data anywhere except:
- MAX Bot API (for sending responses)
- Claude API (optional, for smart responses)
- Your admin Telegram chat (for notifications)
