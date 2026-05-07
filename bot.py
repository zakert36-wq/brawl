import telebot
import json
import os

from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)

TOKEN = "8647304633:AAF6Pvt-HFlkKyO6sy6moooAiEE4LKFCX10"
ADMIN_ID = 1821646861

WEBAPP_URL = "https://web-production-bb83c.up.railway.app/"

bot = telebot.TeleBot(TOKEN)

user_state = {}
temp_data = {}

# СОЗДАЁМ products.json ЕСЛИ ЕГО НЕТ
if not os.path.exists("products.json"):
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump([], f)

# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()

    # КНОПКА МАГАЗИНА
    markup.add(
        InlineKeyboardButton(
            "🛒 Открыть магазин",
            web_app=WebAppInfo(WEBAPP_URL)
        )
    )

    # АДМИНКА ТОЛЬКО ТЕБЕ
    if message.from_user.id == ADMIN_ID:
        markup.add(
            InlineKeyboardButton(
                "⚙️ Админка",
                callback_data="admin"
            )
        )

    bot.send_message(
        message.chat.id,
        "🔥 Добро пожаловать в магазин аккаунтов Brawl Stars!",
        reply_markup=markup
    )

# АДМИН ПАНЕЛЬ
@bot.callback_query_handler(func=lambda call: call.data == "admin")
def admin_panel(call):

    if call.from_user.id != ADMIN_ID:
        return

    user_state[call.from_user.id] = "photo"
    temp_data[call.from_user.id] = {}

    bot.send_message(
        call.message.chat.id,
        "📸 Отправь фото аккаунта"
    )

# ПОЛУЧЕНИЕ ФОТО
@bot.message_handler(content_types=['photo'])
def get_photo(message):

    uid = message.from_user.id

    if user_state.get(uid) != "photo":
        return

    file_id = message.photo[-1].file_id

    temp_data[uid]["photo"] = file_id

    user_state[uid] = "name"

    bot.send_message(
        message.chat.id,
        "📝 Введи название"
    )

# ОБРАБОТКА ТЕКСТА
@bot.message_handler(func=lambda m: True)
def handle_text(message):

    uid = message.from_user.id

    if uid != ADMIN_ID:
        return

    state = user_state.get(uid)

    # НАЗВАНИЕ
    if state == "name":

        temp_data[uid]["name"] = message.text

        user_state[uid] = "desc"

        bot.send_message(
            message.chat.id,
            "📄 Введи описание"
        )

        return

    # ОПИСАНИЕ
    if state == "desc":

        temp_data[uid]["desc"] = message.text

        user_state[uid] = "price"

        bot.send_message(
            message.chat.id,
            "💰 Введи цену"
        )

        return

    # ЦЕНА
    if state == "price":

        temp_data[uid]["price"] = message.text

        with open("products.json", "r", encoding="utf-8") as f:
            products = json.load(f)

        products.append(temp_data[uid])

        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

        bot.send_message(
            message.chat.id,
            "✅ Аккаунт добавлен"
        )

        user_state[uid] = None
        temp_data[uid] = {}

print("BOT STARTED")

bot.infinity_polling()