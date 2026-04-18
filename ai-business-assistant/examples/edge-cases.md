# Edge Cases

How the AI Business Assistant handles unusual inputs.

---

### Case: Empty inbox
**Input:** No unread emails at briefing time.
**Skill output:** Skips email section entirely. Shows: "Inbox clear. No unread emails since yesterday 18:00."
**Why:** Don't waste the reader's attention on "0 emails found." Absence of data is still information.

### Case: Calendar with no events
**Input:** Completely empty calendar for the day.
**Skill output:** "No meetings today. Full focus day. Suggested: tackle the highest-priority task from yesterday's list that didn't get done."
**Why:** An empty calendar is an opportunity, not a blank space.

### Case: Spam or phishing email
**Input:** Email from "Amazon Security" asking to verify account via suspicious link.
**Skill output:** Flags as "[SPAM] Do not click. Sender domain doesn't match amazon.com." Does not draft a reply.
**Why:** Auto-replying to phishing confirms the email is active. Skill should protect, not engage.

### Case: Email in a foreign language
**Input:** Email in German from a supplier.
**Skill output:** "[FOREIGN: German] Subject appears to be an invoice confirmation. Auto-translate available, or flag for manual review?"
**Why:** Don't assume the user speaks the language. Detect and offer options.

### Case: Scheduled/sent email from yourself appears as unread
**Input:** Gmail sometimes shows your own scheduled emails as "unread" after they send.
**Skill output:** Filters out emails where sender = your configured email address. Logs: "1 self-sent email filtered."
**Why:** Nobody wants to be told to reply to their own email.

### Case: Calendar conflict (two meetings at the same time)
**Input:** 14:00 client call AND 14:00 team standup.
**Skill output:** "CONFLICT at 14:00: Client call vs Team standup. Client call is external and was booked first. Suggest: move standup to 14:30 or delegate to Lena. Draft reschedule message?"
**Why:** Don't just list both. Suggest a resolution based on priority (external > internal, first-booked wins).

### Case: Metrics data source not connected
**Input:** User hasn't set up revenue tracking or doesn't have an API connection.
**Skill output:** Skips metrics section. Shows: "Metrics not configured. To add daily revenue tracking, describe where your numbers live (spreadsheet, dashboard URL, or manual input)."
**Why:** Failing silently is worse than asking. But only ask once, not every morning.
