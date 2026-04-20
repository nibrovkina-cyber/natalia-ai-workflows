# Observability

## Three metrics

### 1. Response rate
**What:** How many customer messages get a useful response (not "I didn't understand").
**Target:** 80%+ by day 7.
**If too low:** Expand your faq.json. Check what questions trigger the fallback.

### 2. Booking completion rate
**What:** Of customers who start the booking flow, how many finish (date + time + phone).
**Target:** 70%+
**If too low:** Simplify the flow. Check if date format instructions are clear.

### 3. Admin notification latency
**What:** Time from customer message to admin receiving notification.
**Target:** Under 5 seconds.
**If too slow:** Check your server/hosting. MAX webhook might be delayed.

## What to log

All interactions are logged by default in:
- `data/leads.json` (questions and contact info)
- `data/bookings.json` (appointment bookings)
- Bot console output (all messages received/sent)
