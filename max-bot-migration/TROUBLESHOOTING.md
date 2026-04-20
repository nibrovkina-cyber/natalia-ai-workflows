# Troubleshooting

10 most common problems and their fixes.

---

## Problem: npm install fails with "@maxhub/max-bot-api not found"

**Cause:** Wrong package version in package.json or npm registry issue.

**Fix:** Check that package.json has `"@maxhub/max-bot-api": "^0.2.2"` (not ^1.0.0). Then:
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## Problem: Bot starts but doesn't reply to messages

**Cause:** BOT_TOKEN is wrong, expired, or the bot hasn't passed moderation on MAX.

**Fix:**
1. Check token: go to business.max.ru > Чат-боты > Интеграция > compare the token
2. If token looks right, check bot status: it should show "Активен" (not "На модерации")
3. Test the token manually:
```bash
curl -s -H "Authorization: YOUR_TOKEN" https://platform-api.max.ru/me
```
If you get `{"user_id": ...}` the token works. If 401, regenerate it.

---

## Problem: ADMIN_CHAT_ID not found (where to get it)

**Cause:** You need the numeric chat ID of the conversation where admin notifications go.

**Fix:**
1. Send any message to your bot in MAX messenger
2. Look at the bot console output. You'll see a log like:
```
Received message from chat_id: 123456789
```
3. Copy that number into config.env as ADMIN_CHAT_ID
4. Restart the bot

Alternative: create a group in MAX, add the bot as admin, send a message in the group. The group chat_id will appear in logs.

---

## Problem: Admin notifications don't arrive

**Cause:** ADMIN_CHAT_ID is set but wrong format, or the bot doesn't have permission to send to that chat.

**Fix:**
1. Verify ADMIN_CHAT_ID is a plain number (no quotes, no spaces): `ADMIN_CHAT_ID=123456789`
2. Make sure you've sent at least one message to the bot first (MAX requires the user to initiate)
3. Check bot console for errors like "Failed to notify admin"
4. If using a group: make sure the bot is added as admin to that group

---

## Problem: FAQ doesn't match user questions

**Cause:** The fuzzy search needs at least 2 overlapping keywords between the user's message and the FAQ question.

**Fix:**
1. Open faq.json
2. For each question, add common synonyms. Example: instead of just "Сколько стоит стрижка", add variations:
```json
{"question": "Сколько стоит стрижка цена прайс", "answer": "..."}
```
3. The search matches by keywords, so "стрижка цена" and "сколько стрижка" will both hit
4. If a question keeps missing: add it as a new entry with the exact wording customers use

---

## Problem: Bot works locally but not on Railway

**Cause:** Environment variables not set in Railway dashboard.

**Fix:**
1. Go to Railway dashboard > your project > Variables
2. Add: `BOT_TOKEN=your_token_here`
3. Add: `ADMIN_CHAT_ID=your_chat_id`
4. Click "Deploy" to restart with new variables
5. Check logs in Railway for errors

Common Railway mistake: adding quotes around values. Wrong: `BOT_TOKEN="abc"`. Right: `BOT_TOKEN=abc`

---

## Problem: Bot crashes overnight (or randomly)

**Cause:** Unhandled API error or memory issue on free tier.

**Fix:**
1. In Railway: Settings > Deploy > set Restart Policy to "On Failure" (should be default)
2. Check Railway logs for the error message
3. Most common crash: MAX API returns 429 (rate limit). The bot doesn't retry and crashes. Workaround: reduce message frequency or add a 1-second delay between API calls
4. Free tier memory: 512 MB should be enough. If you see OOM errors, check for memory leaks in custom code

---

## Problem: Phone number validation rejects valid numbers

**Cause:** The regex in bot.js (line ~155) only accepts +7XXXXXXXXXX or 8XXXXXXXXXX format.

**Fix:** If your customers use other formats (like 7XXXXXXXXXX without +, or with spaces/dashes), edit the regex in bot.js:
```javascript
// Current (strict):
if (!/^[\+]?[78]\d{10}$/.test(phone) && !/^\d{10,11}$/.test(phone))

// More permissive (accepts spaces, dashes, parentheses):
const cleaned = text.replace(/[\s\-\(\)]/g, '');
if (!/^[\+]?[78]?\d{10,11}$/.test(cleaned))
```

---

## Problem: "401 Unauthorized" from MAX API

**Cause:** Token expired or bot deleted on business.max.ru.

**Fix:**
1. Go to business.max.ru > Чат-боты > your bot
2. Check status: "Активен" means OK, "Заблокирован" means problem
3. Go to Интеграция > Получить токен
4. If the token changed: copy new token to config.env, restart bot
5. If bot is blocked: check moderation comments, fix issues, resubmit

---

## Problem: Bot responds to its own messages (infinite loop)

**Cause:** The bot receives its own messages as events and tries to reply to them.

**Fix:** Add a filter at the top of the message handler in bot.js:
```javascript
bot.on('message_created', async (ctx) => {
    // Skip messages from bots (including self)
    if (ctx.user?.is_bot) return;
    
    // ... rest of handler
});
```

If `is_bot` field is not available in MAX API, filter by user_id:
```javascript
if (ctx.user?.user_id === BOT_USER_ID) return;
```
Get BOT_USER_ID from the `/me` endpoint response.
