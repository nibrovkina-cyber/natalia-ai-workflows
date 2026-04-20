# MAX Bot Migration — перенос Telegram-бота на MAX за вечер

> Готовый шаблон Node.js-бота для платформы MAX (VK Group). Перенесла несколько клиентских ботов по этому коду за неделю. Вся технологическая сложность — уже в репо.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/nibrovkina-cyber/natalia-ai-workflows/tree/main/max-bot-migration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org)

---

## 1. Что это

Open-source шаблон рабочего Telegram-style бота на платформе MAX от VK Group. Включает welcome menu, FAQ-автоответчик, booking flow (запись клиентов), lead collection, admin notifications. Типичное время установки: **2-4 часа** если знаете `npm`, **один вечер** если работаете по чеклисту.

## 2. Кому для

**Владельцы малого бизнеса.** Telegram заблокировали, бот перестал работать, клиенты не могут записаться. Клонируете, редактируете FAQ, деплоите. Ваш бизнес снова на связи.

**Фрилансеры-разработчики.** Продавайте migration как услугу. Типичная сделка: 15-30К ₽ за клиента, 2-4 часа вашего времени. 6-шаговый сервисный фреймворк описан в [templates/README.md](templates/README.md).

**Агентства автоматизации.** Базовый шаблон для серии клиентских проектов. Можно форкнуть под свою брендировку.

## 3. Quick Start (5 шагов, ~5 минут)

### Шаг 1. Клон и установка зависимостей

```bash
git clone https://github.com/nibrovkina-cyber/natalia-ai-workflows.git
cd natalia-ai-workflows/max-bot-migration
npm install
```

### Шаг 2. Выбрать FAQ-шаблон

```bash
cp templates/salon-beauty.json faq.json        # Салон красоты, ногтевая студия
cp templates/cafe-restaurant.json faq.json     # Кафе, ресторан, бар
cp templates/autoservice.json faq.json         # Автосервис, шиномонтаж
cp templates/blank-template.json faq.json      # С нуля под свой бизнес
```

Откройте `faq.json`, замените примеры на свои ответы. 15 минут.

### Шаг 3. Конфиг

```bash
cp config.example.env config.env
```

Отредактируйте `config.env`:
- `BOT_TOKEN` — из кабинета [business.max.ru](https://business.max.ru)
- `ADMIN_CHAT_ID` — ваш chat_id в MAX (как получить — [TROUBLESHOOTING.md](TROUBLESHOOTING.md#problem-admin_chat_id-not-found))

### Шаг 4. Локальный тест

```bash
npm start
```

Откройте MAX на телефоне, найдите своего бота, отправьте `/start`. Должно прийти welcome-меню с 4 кнопками.

### Шаг 5. Деплой на Railway (one-click)

Нажмите кнопку Deploy on Railway в начале README. Заполните `BOT_TOKEN` и `ADMIN_CHAT_ID` в Railway dashboard. Deploy. Бот живой.

**⚠️ Перед Шагом 1:** нужен статус ИП, самозанятого или ООО + верификация на business.max.ru (1-2 рабочих дня). Для самозанятости — регистрация за день через приложение Мой Налог. Для ИП — 3-5 рабочих дней.

---

## 4. 5 Key Differences: Telegram Bot API → MAX Bot API

Эти пять архитектурных отличий объясняют 80% миграционной работы. Остальное — FAQ и тестирование.

### 4.1. Аутентификация

Telegram передаёт токен **в URL пути**:
```
GET https://api.telegram.org/bot12345:ABCD/sendMessage
```

MAX требует токен **в HTTP-заголовке Authorization**:
```
POST https://platform-api.max.ru/messages
Authorization: 12345:ABCD
```

Если копируете логику из Telegram-бота — любой API-вызов будет валиться с 401 пока не перепишете аутентификацию.

### 4.2. Базовый URL

| Platform | Base URL |
|----------|----------|
| Telegram | `api.telegram.org` |
| **MAX** | `platform-api.max.ru` |

Тривиальное изменение, но легко пропустить в нескольких местах клиентского кода.

### 4.3. Типы клавиатур

Telegram поддерживает **InlineKeyboard** (кнопки под сообщением) **и ReplyKeyboard** (кнопки под полем ввода, остаются между сообщениями).

MAX поддерживает **только InlineKeyboard**. ReplyKeyboard **не существует**.

Если клиент использовал ReplyKeyboard для меню — переделать на inline + callback handlers со стейтом.

### 4.4. Поле callback data

| Platform | Field name |
|----------|------------|
| Telegram | `callback_data` |
| **MAX** | `payload` |

Концептуально то же — данные которые приходят боту при нажатии inline-кнопки. Но переименовать надо везде в коде.

### 4.5. Webhook требует HTTPS

Telegram допускал HTTP webhook. **MAX требует HTTPS**.

Если бот работал на HTTP webhook — нужен HTTPS-сертификат. Решается за 30 минут через Let's Encrypt или автоматически на Railway / Render / Vercel (где сертификат включён из коробки).

---

## 5. FAQ Templates (4 готовых JSON)

В папке `templates/`:

| Шаблон | Бизнес-ниша | Вопросов | Закрывает |
|--------|-------------|----------|-----------|
| `salon-beauty.json` | Парикмахерская, ногтевая студия, бьюти-бар | 15 | Прайс, запись, адрес, доступность мастеров |
| `cafe-restaurant.json` | Кафе, ресторан, бар | 15 | Меню, бронь столика, часы работы, доставка |
| `autoservice.json` | Автосервис, шиномонтаж | 15 | Виды работ, запись, прайс, склад шин |
| `blank-template.json` | Любой бизнес с нуля | 0 | Пустая структура, заполняете под себя |

**Как пользоваться:** даёте клиенту ближайший по нише шаблон, просите заменить 5-10 ответов на свои. Не надо составлять FAQ с нуля — сильно ускоряет работу с клиентом.

Полная инструкция кастомизации: [templates/README.md](templates/README.md).

---

## 6. Railway Deploy (3 минуты)

Railway даёт бесплатный план для ботов **100-500 сообщений/день**. Для большинства SMB с запасом.

### Путь

1. Нажмите `Deploy on Railway` кнопку в начале этого README
2. Авторизуйтесь через GitHub
3. В Railway dashboard введите 2 переменных:
   - `BOT_TOKEN` (без кавычек!)
   - `ADMIN_CHAT_ID` (число, без кавычек)
4. Нажмите Deploy
5. Через ~90 секунд получите URL и логи. Протестируйте через MAX на телефоне.

### Если нагрузка вырастет

Railway автоматически масштабируется. Платный тариф от **$5/мес** для постоянного uptime с запасом ресурсов.

### Альтернативы Railway

- **Render.com** — аналогично, бесплатный tier, поддерживает Node.js
- **Vercel** — для serverless варианта, нужна переделка на webhook mode
- **Свой VPS** — минимум Ubuntu 22.04 + Node.js 18 + pm2/systemd

---

## 7. Troubleshooting (10 типичных ошибок)

Полный список с фиксами — [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Краткий индекс:

1. `npm install fails with "@maxhub/max-bot-api not found"` — версия пакета
2. Бот стартует, но не отвечает — BOT_TOKEN / модерация
3. `ADMIN_CHAT_ID not found` — где взять chat_id
4. Admin-уведомления не приходят — формат ID / permissions
5. FAQ не матчит вопросы пользователей — ключевые слова
6. Бот работает локально, не работает на Railway — env vars
7. Бот падает ночью / случайно — rate limit / OOM
8. Валидация телефона отвергает валидные номера — regex
9. `401 Unauthorized` от MAX API — токен / бан
10. Бот отвечает на свои сообщения (infinite loop) — is_bot фильтр

---

## 8. License

**MIT License**

```
Copyright (c) 2026 Natalia Brovkina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Используйте в коммерческих проектах без ограничений. Форкайте, меняйте под себя, продавайте установку клиентам. Если нашли улучшение — PR welcome.

---

## 9. Contact

### Вопросы по шаблону

- **GitHub Issues:** [natalia-ai-workflows/issues](https://github.com/nibrovkina-cyber/natalia-ai-workflows/issues) — ответ в течение 3 дней
- **Telegram DM:** [@FinanceNatasha](https://t.me/FinanceNatasha) — быстрее для срочных вопросов

### Платная настройка (если нет времени делать самому)

Typical engagement: **10-30К ₽** в зависимости от сложности.

Процесс:
1. 30-мин аудит через Zoom/MAX → понимаем fit
2. Если подходит — сетапим под ключ (включая ИП-регистрацию помощь если нужно)
3. Передаём готовый живой бот + 30 дней поддержки

[Записаться на аудит → @FinanceNatasha](https://t.me/FinanceNatasha)

---

## What this doesn't do (ограничения)

- Не обрабатывает платежи (используйте платежные ссылки вашего банка отдельно)
- Не синхронизируется с CRM (экспорт `leads.json` вручную или webhook дописать)
- Не поддерживает voice/video звонки (ограничение MAX API)
- Не работает без бизнес-верификации на MAX (ИП/самозанятость/ООО)
- Пока без мультиязычности (шаблоны только на русском)

---

## More

- [SKILL.md](SKILL.md) — полная техническая документация
- [examples/edge-cases.md](examples/edge-cases.md) — 7 edge cases с фиксами
- [PRIVACY.md](PRIVACY.md) — что хранит бот, что не хранит
- [OBSERVABILITY.md](OBSERVABILITY.md) — логи, метрики, мониторинг

---

## Родственные артикли

- **Habr (технический разбор):** в ожидании модерации в песочнице
- **Дзен (бизнес-ракурс):** опубликовано 2026-04-19
- **vc.ru (короткая практическая версия):** опубликовано 2026-04-19

---

*Built by [Natalia Brovkina](https://t.me/FinanceNatasha) — AI Change Manager для малого бизнеса. 2026.*
