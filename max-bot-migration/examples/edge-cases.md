# Edge Cases

How the bot handles unusual inputs.

---

### Case: User sends voice message

**Input:** Voice message (audio file) instead of text.

**Bot behavior:** "Я пока понимаю только текстовые сообщения. Напишите ваш вопрос текстом или выберите из меню."

**Why:** MAX Bot API delivers voice as an attachment. The bot checks for text field first; if empty, sends the fallback. Adding speech-to-text is possible but adds complexity and cost (Whisper API).

---

### Case: User sends image or sticker

**Input:** Photo of a broken product, sticker, or GIF.

**Bot behavior:** "Спасибо за фото. Для вопросов используйте кнопки меню или напишите текстом. Если нужно показать фото менеджеру, нажмите 'Задать вопрос'."

**Why:** Same logic as voice. Bot routes the message to admin if the user is in the "ask question" flow, but doesn't try to analyze images.

---

### Case: User books for a past date

**Input:** "20 марта" (a date that already passed).

**Bot behavior:** "Эта дата уже прошла. Выберите дату начиная с сегодняшнего дня."

**Why:** The bot parses common date formats (DD.MM, DD месяца) and compares with current date. If parsing fails (ambiguous input like "послезавтра"), the bot accepts it and lets the admin sort it out.

---

### Case: User enters invalid phone number

**Input:** "мой номер 1234" or "позвони мне".

**Bot behavior:** "Пожалуйста, введите номер телефона в формате +7XXXXXXXXXX или 8XXXXXXXXXX (11 цифр)."

**Why:** Regex validation: `/^[\+]?[78]\d{10}$/` or `/^\d{10,11}$/`. Rejects anything that doesn't look like a Russian phone number. Asks again, doesn't skip the step.

---

### Case: Bot added to a group chat (not DM)

**Input:** Someone adds the bot to a group with 50 people.

**Bot behavior:** Bot ignores all messages unless directly mentioned or a /start command is sent. In group mode, it only responds to commands, not free text.

**Why:** Responding to every message in a group would be spam. MAX bot settings control this: business.max.ru > bot settings > allow/disallow group chats.

---

### Case: FAQ search finds no match

**Input:** "А вы принимаете биткоин?" (no FAQ entry about crypto).

**Bot behavior:** "Не нашла ответ на этот вопрос. Передала менеджеру, ответит в течение часа." Admin receives notification with the full question text.

**Why:** Better to escalate honestly than to hallucinate an answer. The admin can later add this question to faq.json if it repeats.

---

### Case: Duplicate webhook delivery (same message arrives twice)

**Input:** MAX server retries a webhook due to timeout, sending the same message event twice.

**Bot behavior:** TODO v2. Currently the bot will process both events, potentially creating a duplicate booking or sending a duplicate admin notification.

**Why this is not yet fixed:** Long polling mode (current) rarely has this problem. Webhook mode (planned for v2) will need idempotency via message timestamp + user_id hash. For now, the risk is low and the workaround is: admin checks for obvious duplicates in bookings.json manually.
