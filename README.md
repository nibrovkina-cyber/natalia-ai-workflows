# natalia-ai-workflows

Free AI agents for small business. Built with Claude Code. Each agent solves one specific pain.

---

## Agents

| Agent | What pain it solves | Who it's for | Time saved |
|---|---|---|---|
| [MAX Bot Migration](max-bot-migration/) | Telegram blocked, your business bot stopped working | Any Russian business that ran on Telegram | 1 evening to migrate |
| [Marketplace AI Manager](marketplace-ai-manager/) | Reviews, competitors, inventory, analytics, questions, daily briefing | WB/Ozon sellers with 200+ orders/day | 4-5 hours/day |
| [Bankruptcy Deal Finder](bankruptcy-deal-finder/) | Scanning 1000s of auction lots daily for undervalued assets | Investors, flippers, anyone buying at bankruptcy auctions | 2-4 hours/day |
| [AI Business Assistant](ai-business-assistant/) | Morning routine: email triage, calendar prep, task priorities | Solo founders, small teams | 1-2 hours/day |

Each agent includes: setup guide, working code, example outputs, edge cases, privacy notes.

---

## How to use

```bash
git clone https://github.com/nibrovkina-cyber/natalia-ai-workflows.git
cd natalia-ai-workflows

# Pick an agent, read its README
cd bankruptcy-deal-finder/
cat SKILL.md

# Configure
cp config.example.env config.env
# Edit config.env with your API keys

# Run
pip install -r requirements.txt
python run_daily.py --dry-run
```

---

## What to expect week 1

- Day 1-2: 50-70% of AI outputs need editing. Normal.
- Day 3-5: Feed your edits back as examples. Output quality improves.
- Day 6-7: Most workflows run with minimal oversight.

If output quality stays low after day 5, you need more voice samples or clearer business context.

---

## About

Built by **Natalia Brovkina**. Former Big 4 and Big Tech finance. Now building AI agents for small business.

I use these agents for my own business every day. Giving them away because watching how other people use them teaches me more than writing another post.

If you run a small business and want help setting these up:

- Telegram: [@FinanceNatasha](https://t.me/FinanceNatasha)
- YouTube: [@nataliyabrovk](https://youtube.com/@nataliyabrovk)
- Twitter: [@NataliyaBrovk](https://twitter.com/NataliyaBrovk)

I run free 30-min audits where I look at your processes and find 3 to automate. No pitch, just the analysis.

---

## License

MIT
