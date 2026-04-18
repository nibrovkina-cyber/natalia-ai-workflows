# Observability

## Three metrics

### 1. Approval rate (without edits)
**What:** Percentage of AI-drafted responses you send as-is.
**Target:** 85%+ by day 7.
**If too low:** Add more voice samples. Check if the prompt guardrails are too strict or too loose.

### 2. Response time
**What:** Time from review posted to response sent.
**Before agent:** 4-24 hours (manual).
**Target:** Under 1 hour (agent draft + your approval).
**If too slow:** Check cron interval. Default 30 min might be enough, but peak hours (10:00-14:00 MSK) may need 15 min.

### 3. Rating trend
**What:** Your store rating over 2 weeks.
**Target:** Stable or improving. If rating drops after agent starts, check response quality.
**How to check:** WB seller dashboard, Analytics section.

## What to log

n8n logs all executions by default. Additionally track:

| What | Where | Why |
|---|---|---|
| AI draft text | n8n execution log | Compare with what you actually sent |
| Your edits | Telegram chat history | Shows where AI misses your voice |
| Skipped reviews | n8n log (skip button) | Patterns in what you skip = prompt improvement |
| Trigger word hits | n8n log (manual route) | Frequency of legal/safety escalations |
