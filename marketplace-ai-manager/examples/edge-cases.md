# Edge Cases

### Case: Review is emoji only
**Input:** Rating 1 star, text: "👎"
**Agent:** Generates generic: "Жаль что не понравилось. Напишите что именно не так, разберемся." Flags as "low-context review" in log.

### Case: Legal threat
**Input:** "Мошенники, подам в суд, Роспотребнадзор"
**Agent:** Skips AI draft. Sends to Telegram: "LEGAL: manual review. Keywords: мошенники, суд, Роспотребнадзор."

### Case: Product injury
**Input:** "У ребенка аллергия, были в больнице"
**Agent:** Skips AI. "SAFETY URGENT: аллергия + ребенок + больница. Manual response only."

### Case: Competitor drops price 30%
**Input:** Competitor #67890 price: 1800 → 1260 rub
**Agent:** Alert: "PRICE DROP: competitor #67890, SKU 12345, -30% (1800→1260). Your price: 1650. You're now 31% higher. Action needed?"

### Case: Inventory runs out in 2 days
**Input:** SKU 12345: 16 units left, selling 8/day
**Agent:** "URGENT RESTOCK: SKU 12345 (Blue T-shirt XL), 2 days supply left. Order 200 units to cover 25 days."

### Case: Same customer complains twice
**Input:** Same name appears in two reviews within a week
**Agent:** Flags: "REPEAT: customer Dmitry, 2nd complaint this week. Previous: delivery (resolved). Current: sizing. Consider personal outreach."

### Case: Review in foreign language
**Input:** Turkish review on Russian marketplace
**Agent:** "FOREIGN: Turkish detected. Translation: 'Quality good, shipping slow.' Draft in Russian or Turkish?"

### Case: WB API returns 429 (rate limit)
**Agent:** Waits 60 seconds, retries 3x. If still failing: "Scan incomplete. WB API rate limited. 23 of 45 reviews processed. Will retry next cycle."
