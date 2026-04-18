---
name: ai-business-assistant
description: Daily AI assistant for entrepreneurs — morning briefing, task prioritization, email drafts, meeting prep, expense tracking, weekly review
version: 1.0.0
author: Natalia Brovkina (@NataliyaBrovk)
---

# AI Business Assistant

Your daily AI co-pilot that handles the morning routine you hate.

**The problem:** You spend 1-2 hours every morning on emails, calendar, task sorting, and prep before you do any actual work.

**The solution:** One command. Your AI assistant reads your inbox, calendar, and task list — gives you a 2-minute briefing and handles the rest.

## What it does

### Morning Briefing (daily, 2 min read)
- Scans today's calendar — flags conflicts, prep needed
- Reads unread emails — drafts replies for routine ones
- Checks task list — suggests top 3 priorities based on deadlines and impact
- Summarizes yesterday's metrics (revenue, orders, support tickets)

### Email Drafts
- Reads incoming email context
- Drafts professional replies matching your voice
- Flags emails that need your personal attention vs auto-replies

### Meeting Prep
- Reads calendar invite + attendee info
- Pulls relevant docs/notes from previous meetings
- Generates 3 talking points and 2 questions to ask

### Weekly Review (Fridays)
- Revenue vs last week
- Tasks completed vs planned
- Top 3 wins, top 3 blockers
- Suggested focus for next week

### Expense Quick-Check
- Paste a receipt or invoice description
- Categorizes expense (operational, marketing, software, etc.)
- Flags unusual spending vs monthly average

## How to use

### Setup (5 minutes)
1. Clone this repo or copy the SKILL.md into your Claude Code skills folder
2. Tell Claude about your business context:
   ```
   My business: [describe in 2-3 sentences]
   My tools: [Gmail/Outlook, Google Calendar, Notion/Todoist, etc.]
   My voice: [formal/casual/direct]
   My timezone: [e.g., MSK, PST]
   ```

### Daily use
```
"Morning briefing"
"Draft replies to my 5 unread emails"
"Prep me for the 2pm meeting with [client]"
"Categorize these 3 expenses"
"Weekly review"
```

## Example output

### Morning Briefing
```
Good morning. Thursday April 18.

CALENDAR (3 events):
- 10:00 Team standup (15 min) — no prep needed
- 14:00 Client call: Maria, WB seller, 150 orders/day — PREP BELOW
- 16:30 Dentist — personal, blocked

EMAILS (7 unread, 3 need you):
- [AUTO-REPLY DRAFTED] Supplier invoice confirmation
- [AUTO-REPLY DRAFTED] Meeting reschedule request  
- [AUTO-REPLY DRAFTED] Newsletter subscription
- [NEEDS YOU] Client asking about pricing — draft ready for review
- [NEEDS YOU] Partner proposal — complex, read yourself
- [NEEDS YOU] Tax accountant question — forwarded context

TOP 3 TODAY:
1. Finish client proposal (deadline tomorrow, 2 hours)
2. Review agent test results (30 min)  
3. Record video intro (1 hour, can push to tomorrow)

METRICS:
- Orders yesterday: 47 (+12% vs avg)
- Support tickets: 3 open (1 urgent)
- Revenue MTD: $4,200 (on track for $6K target)
```

## Who this is for

- Solo founders doing everything themselves
- Small business owners (1-10 people) drowning in operational tasks
- Freelancers juggling multiple clients
- Anyone who spends more than 30 minutes on morning routine

## Built with

- Claude Code (Claude Opus 4.6/4.7)
- Works with Gmail, Google Calendar, Notion, Todoist, Slack via MCP
- No external APIs required for basic features

---

**Made by [Natalia Brovkina](https://t.me/FinanceNatasha)** — AI Change Manager. Former Big 4 & Big Tech finance. Now building AI agents for small business between feedings and LEGO.
