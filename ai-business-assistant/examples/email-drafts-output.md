# Example: Email Draft Outputs

Three incoming emails, three reply drafts in different tones.

---

## Email 1: Client asking about pricing

**Incoming:**
> Hi Natalia, we spoke last week about automating our review responses. Can you send over your pricing? We're also talking to another agency that quoted 50K for a similar setup. Thanks, Dmitry

**Draft (direct, confident):**

Hi Dmitry,

The review responder setup is 30,000 rub one-time. That covers configuration, voice tuning with your actual past responses, testing on 50 real reviews, and 30 days of async support if anything breaks.

The difference from a 50K quote is usually scope. Most agencies bundle things you don't need yet (dashboards, analytics, multi-platform). We start with the one thing that saves you the most hours, make sure it works, then add from there.

I can walk through the specifics on a call if that helps. When works for you?

Natalia

---

## Email 2: Someone asking for free advice

**Incoming:**
> Hey, I saw your video about WB review bots. Can you tell me how to set up n8n to connect to WB API? I'm trying to do it myself but keep getting 403 errors.

**Draft (helpful but boundaried):**

Hi,

The 403 usually means your WB API token doesn't have the "Reviews and Questions" permission. Go to your seller dashboard, Settings, API Access, check which permissions are enabled on your token. If "Reviews" is missing, create a new token with that scope.

If it's still 403 after that, the token might have expired. WB tokens have a 180-day limit.

For the full n8n setup, the video description has a link to the template file. That should get you most of the way.

Natalia

---

## Email 3: Angry client

**Incoming:**
> Natalia, the bot sent a weird response to one of my customers yesterday. It said "we will process your refund within 24 hours" but I NEVER promised that. I had to apologize to the customer manually. This is not OK.

**Draft (empathetic, takes responsibility, concrete fix):**

Hi,

That should not have happened and I'm sorry it did.

The bot should never promise timelines or refunds. I checked the response log and the issue was a missing guardrail in the prompt. The word "refund" in the customer's review triggered a response pattern that wasn't blocked.

I've already added "refund timeline" and "processing time" to the restricted phrases list. From now on, any review mentioning refunds will be routed to you directly without an AI draft.

Can we do a quick 10-minute call today so I can walk you through the updated settings? I want to make sure you're comfortable before the bot runs again.

Natalia
