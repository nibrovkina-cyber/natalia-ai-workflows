# AI Business Assistant

A daily operations co-pilot for solo founders and small teams. Handles the 1-2 hours of morning routine you do before actual work starts.

If your mornings look like this: open email, scan calendar, figure out priorities, reply to 5 routine messages, prep for a meeting, check yesterday's numbers... this skill does most of that in one command.

## Prerequisites

- Claude Code (Opus 4.6+)
- Gmail or Outlook access (for email scanning)
- Google Calendar or similar (for schedule)
- A task manager you already use (Notion, Todoist, even a text file)

## Setup (5 minutes)

**Step 1.** Copy the skill folder into your Claude Code project:

```bash
cp -r ai-business-assistant/ ~/.claude/skills/
```

**Step 2.** Create a file called `my-business.md` in the skill folder. Describe your business in 5-10 sentences: what you sell, who your customers are, how many people work with you, what tools you use daily. Claude uses this as context for every briefing.

**Step 3.** Drop 5-10 of your actual sent emails into `voice-samples/`. Claude learns your tone from these. The more samples, the fewer edits you make later.

**Step 4.** Run your first briefing:

```
"Morning briefing"
```

## What good output looks like

See [examples/morning-briefing-output.md](examples/morning-briefing-output.md) for a full realistic sample. The briefing covers:

- Today's calendar with prep notes for each meeting
- Unread emails sorted by "needs you" vs "auto-reply drafted"
- Top 3 priorities with reasoning
- Yesterday's key metrics

## What to expect week 1

- Day 1-2: 50-70% of email drafts need editing. Normal. The skill doesn't know your voice yet.
- Day 3-5: Feed your edits back as voice-samples. Edit rate drops to 20-30%.
- Day 6-7: Most briefings run hands-off. You step in for the 10% flagged "needs you."

If edit rate stays above 50% after day 5, add more voice samples. 10 samples is the minimum for reliable tone matching.

## Troubleshooting

**Briefing is too generic.** Your `my-business.md` is too short. Add specifics: what products you sell, typical customer questions, your pricing, your team's names and roles.

**Email drafts sound wrong.** Add more voice-samples. The skill needs at least 5 real emails to match your tone. 10 is better.

**Calendar prep is empty.** Make sure your calendar entries have attendee names and meeting descriptions. The skill can't prep for "Meeting" with no context.

**Metrics section is blank.** Connect your data source or describe where your numbers live. The skill asks you on first run.

## What this skill doesn't do

- Doesn't send emails automatically. Drafts only. You review and hit send.
- Doesn't make financial decisions. Flags expenses and anomalies, never approves or denies.
- Doesn't access your bank account or payment processor directly. You paste or describe the data.
- Doesn't replace a real CFO or accountant for tax, compliance, or legal questions.
- Doesn't work well for teams over 15 people. Built for solo founders and small teams where one person sees the whole picture.

## Cost

Claude API usage per daily briefing: roughly $0.003-0.01 depending on email volume. That's about $1-3/month for a solo founder running it every weekday.

## Next

- [Edge cases and how the skill handles them](examples/edge-cases.md)
- [Privacy and data flow](PRIVACY.md)
- [How to measure if it's working](OBSERVABILITY.md)
