# Privacy and Data Flow

## How data moves

```
Your email inbox
  |
  [read by Claude Code via Gmail MCP / manual paste]
  |
  Claude API (Anthropic servers)
  |
  AI-generated briefing + email drafts
  |
  Your local machine (logs/ folder)
```

## What data touches Claude API

- Email subjects and bodies (for drafting replies)
- Calendar event titles, times, and attendee names (for meeting prep)
- Task list items (for prioritization)
- Your business context file (`my-business.md`)
- Your voice samples (for tone matching)

## What data stays local

- Full briefing output (in `logs/`)
- Your edits and corrections (in `logs/`)
- Configuration and API keys (in `config.env`)
- Voice samples (in `voice-samples/`)

## Customer PII

If your emails contain customer names, emails, phone numbers, or financial details, those will pass through Claude API. Review Anthropic's data retention policy before using for:

- **EU customers:** GDPR applies. Anthropic processes data under their DPA. Check if your use case requires a signed Data Processing Agreement.
- **Russian customers:** 152-FZ (data localization). If you process personal data of Russian citizens at scale (1000+ contacts/month), consult a lawyer about localization requirements.
- **US customers:** No federal data privacy law, but check state-specific requirements (CCPA for California).

## Recommendations

1. Don't paste full customer credit card numbers or passwords into emails that the skill will process.
2. If you work with healthcare data (HIPAA) or financial data (PCI-DSS), use the skill only for non-sensitive communications.
3. Logs are stored locally by default. If you deploy to a server, encrypt the logs/ directory.
4. Rotate your API keys every 90 days.

## No tracking

This skill does not phone home, send analytics, or communicate with any server other than the Claude API (for AI processing) and your configured email/calendar services.
