/**
 * MAX Business Bot — Template
 *
 * Features: welcome menu, FAQ, appointment booking, lead collection, admin notifications.
 *
 * Setup:
 *   npm install @maxhub/max-bot-api dotenv
 *   BOT_TOKEN="your_token" node bot.js
 */

const { Bot, Keyboard } = require('@maxhub/max-bot-api');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: 'config.env' });

const bot = new Bot(process.env.BOT_TOKEN);

// Load FAQ
const FAQ_FILE = path.join(__dirname, 'faq.json');
let faq = [];
if (fs.existsSync(FAQ_FILE)) {
    faq = JSON.parse(fs.readFileSync(FAQ_FILE, 'utf-8'));
}

// Admin chat ID for notifications
const ADMIN_CHAT_ID = process.env.ADMIN_CHAT_ID;

// Simple state storage (in production, use Redis or DB)
const userState = {};

// Leads file
const LEADS_FILE = path.join(__dirname, 'data', 'leads.json');
const BOOKINGS_FILE = path.join(__dirname, 'data', 'bookings.json');

function ensureDataDir() {
    const dir = path.join(__dirname, 'data');
    if (!fs.existsSync(dir)) fs.mkdirSync(dir);
}

function saveLead(lead) {
    ensureDataDir();
    let leads = [];
    if (fs.existsSync(LEADS_FILE)) {
        leads = JSON.parse(fs.readFileSync(LEADS_FILE, 'utf-8'));
    }
    leads.push({ ...lead, timestamp: new Date().toISOString() });
    fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2), 'utf-8');
}

function saveBooking(booking) {
    ensureDataDir();
    let bookings = [];
    if (fs.existsSync(BOOKINGS_FILE)) {
        bookings = JSON.parse(fs.readFileSync(BOOKINGS_FILE, 'utf-8'));
    }
    bookings.push({ ...booking, timestamp: new Date().toISOString() });
    fs.writeFileSync(BOOKINGS_FILE, JSON.stringify(bookings, null, 2), 'utf-8');
}

// Main menu keyboard
function mainMenu() {
    return Keyboard.inlineKeyboard([
        [
            Keyboard.button.callback('FAQ / Частые вопросы', 'faq'),
            Keyboard.button.callback('Записаться', 'book'),
        ],
        [
            Keyboard.button.callback('Задать вопрос', 'ask'),
            Keyboard.button.callback('Контакты', 'contacts'),
        ],
    ]);
}

// /start command
bot.command('start', async (ctx) => {
    const name = ctx.user?.name || 'друг';
    await ctx.reply(
        `Привет, ${name}! Я бот-помощник. Выберите что вас интересует:`,
        { attachments: [mainMenu()] }
    );
});

// FAQ button
bot.on('message_callback', async (ctx) => {
    const payload = ctx.update?.callback?.payload;

    if (payload === 'faq') {
        if (faq.length === 0) {
            return ctx.reply('FAQ пока не настроен. Задайте вопрос напрямую.', {
                attachments: [mainMenu()]
            });
        }
        const faqButtons = faq.slice(0, 7).map(item =>
            [Keyboard.button.callback(item.question.slice(0, 50), `faq_${faq.indexOf(item)}`)]
        );
        faqButtons.push([Keyboard.button.callback('Назад в меню', 'menu')]);
        return ctx.reply('Выберите вопрос:', {
            attachments: [Keyboard.inlineKeyboard(faqButtons)]
        });
    }

    if (payload?.startsWith('faq_')) {
        const idx = parseInt(payload.replace('faq_', ''));
        if (faq[idx]) {
            return ctx.reply(faq[idx].answer, { attachments: [mainMenu()] });
        }
    }

    if (payload === 'book') {
        userState[ctx.user?.user_id] = { step: 'booking_date' };
        return ctx.reply('На какую дату хотите записаться? (например, 25 апреля)');
    }

    if (payload === 'ask') {
        userState[ctx.user?.user_id] = { step: 'ask_question' };
        return ctx.reply('Напишите ваш вопрос, и я передам его менеджеру:');
    }

    if (payload === 'contacts') {
        return ctx.reply(
            'Наши контакты:\n' +
            'Телефон: +7 (999) 123-45-67\n' +
            'Адрес: Москва, ул. Пушкина 10\n' +
            'Время работы: 10:00-20:00 ежедневно',
            { attachments: [mainMenu()] }
        );
    }

    if (payload === 'menu') {
        return ctx.reply('Главное меню:', { attachments: [mainMenu()] });
    }
});

// Handle text messages (for booking flow and questions)
bot.on('message_created', async (ctx) => {
    const userId = ctx.user?.user_id;
    const text = ctx.message?.body?.text;
    if (!text || !userId) return;

    const state = userState[userId];

    // Booking flow
    if (state?.step === 'booking_date') {
        userState[userId] = { step: 'booking_time', date: text };
        return ctx.reply(`Дата: ${text}. На какое время? (например, 14:00)`);
    }

    if (state?.step === 'booking_time') {
        userState[userId] = { ...state, step: 'booking_contact', time: text };
        return ctx.reply(`Дата: ${state.date}, время: ${text}. Ваш телефон для подтверждения?`);
    }

    if (state?.step === 'booking_contact') {
        const phone = text.replace(/\s/g, '');
        if (!/^[\+]?[78]\d{10}$/.test(phone) && !/^\d{10,11}$/.test(phone)) {
            return ctx.reply('Пожалуйста, введите телефон в формате +7XXXXXXXXXX или 8XXXXXXXXXX');
        }

        const booking = {
            user_id: userId,
            user_name: ctx.user?.name || 'Unknown',
            date: state.date,
            time: state.time,
            phone: phone,
        };
        saveBooking(booking);
        delete userState[userId];

        // Notify admin
        if (ADMIN_CHAT_ID) {
            await bot.api.sendMessageToChat(
                parseInt(ADMIN_CHAT_ID),
                `Новая запись!\nКлиент: ${booking.user_name}\nДата: ${booking.date}\nВремя: ${booking.time}\nТелефон: ${booking.phone}`
            );
        }

        return ctx.reply(
            `Записали! ${booking.date} в ${booking.time}. Подтверждение придёт на ${booking.phone}.`,
            { attachments: [mainMenu()] }
        );
    }

    // Question flow
    if (state?.step === 'ask_question') {
        const lead = {
            user_id: userId,
            user_name: ctx.user?.name || 'Unknown',
            question: text,
        };
        saveLead(lead);
        delete userState[userId];

        // Notify admin
        if (ADMIN_CHAT_ID) {
            await bot.api.sendMessageToChat(
                parseInt(ADMIN_CHAT_ID),
                `Новый вопрос!\nОт: ${lead.user_name}\nВопрос: ${lead.question}`
            );
        }

        return ctx.reply(
            'Спасибо! Менеджер ответит в течение часа.',
            { attachments: [mainMenu()] }
        );
    }

    // Default: try FAQ search, then show menu
    const match = findFaqMatch(text);
    if (match) {
        return ctx.reply(match.answer, { attachments: [mainMenu()] });
    }

    return ctx.reply(
        'Не нашёл ответа. Выберите из меню или задайте вопрос менеджеру:',
        { attachments: [mainMenu()] }
    );
});

// Simple FAQ search (fuzzy)
function findFaqMatch(query) {
    if (!query || faq.length === 0) return null;
    const q = query.toLowerCase();

    // Exact keyword match
    for (const item of faq) {
        const keywords = item.question.toLowerCase().split(/\s+/);
        const queryWords = q.split(/\s+/);
        const overlap = queryWords.filter(w => keywords.some(k => k.includes(w) || w.includes(k)));
        if (overlap.length >= 2 || (overlap.length === 1 && queryWords.length <= 2)) {
            return item;
        }
    }
    return null;
}

// Start the bot
console.log('Bot starting...');
bot.start().then(() => {
    console.log('Bot is running! Send /start in MAX messenger.');
}).catch(err => {
    console.error('Failed to start bot:', err.message);
});
