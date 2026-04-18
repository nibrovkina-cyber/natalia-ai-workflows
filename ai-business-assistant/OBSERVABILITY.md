# Observability

How to know if the AI Business Assistant is actually working for you.

## What to log

Every time the skill runs, it produces output. Track these:

| What | Where | Format |
|---|---|---|
| Full briefing text | Local file `logs/YYYY-MM-DD_briefing.md` | Markdown |
| Email drafts (AI version) | `logs/YYYY-MM-DD_drafts.json` | JSON with original email + AI draft |
| Your edits to drafts | `logs/YYYY-MM-DD_edits.json` | JSON with AI draft + your final version |
| Time spent reviewing | Self-reported (1 min to note) | "Took me X minutes to review" |

## Three metrics that matter

### 1. Edit rate
**What:** Percentage of email drafts you change before sending.
**Target:** Under 30% by day 7. Under 15% by day 14.
**How to measure:** Count drafts sent as-is vs drafts edited. Check your logs weekly.
**If it's too high:** Add more voice samples. 10 samples minimum. If you have 10+ and edit rate is still above 40%, the issue is usually business context, not voice. Expand your `my-business.md` with more details about how you handle specific situations.

### 2. Briefing usefulness
**What:** Did you act on the top 3 priorities the skill suggested?
**Target:** 2 out of 3 priorities should match what you actually work on that day.
**How to measure:** At end of day, check if your top 3 were the skill's top 3. Note mismatches.
**If it's too low:** Your task list might be stale or your priorities shift during the day. Try giving the skill more context: "I have a client deadline Friday" or "Revenue is the only metric this week."

### 3. Time saved
**What:** How many minutes your morning routine takes now vs before.
**Target:** From 60-120 minutes to 15-30 minutes by week 2.
**How to measure:** Time yourself for one week before, one week after.
**If it's not saving time:** You might be over-checking the skill's work. After the first week, trust the auto-reply drafts and only review "needs you" items.

## Week-by-week expectations

| Week | Edit rate | Briefing match | Time saved |
|---|---|---|---|
| Week 1 | 50-70% | 1 of 3 | 15-30 min |
| Week 2 | 20-30% | 2 of 3 | 30-60 min |
| Week 3 | 10-20% | 2-3 of 3 | 45-90 min |
| Week 4+ | Under 15% | 2-3 of 3 | 60-90 min |

## What to do if metrics don't improve

1. Check voice samples: do they reflect your CURRENT writing style? (People change over months)
2. Check business context: is `my-business.md` still accurate?
3. Check if your business changed: new product line, new team member, new priorities?
4. If all else fails: reset voice samples and start fresh with 10 recent emails.
