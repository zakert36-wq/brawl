import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "PASTE_BOT_TOKEN"
ADMIN_ID = 1821646861
WEBAPP_URL = "https://YOUR-SITE.up.railway.app/"

bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            "🛒 Открыть магазин",
            web_app=WebAppInfo(WEBAPP_URL)
        )
    )

    if message.from_user.id == ADMIN_ID:
        markup.add(
            InlineKeyboardButton("⚙️ Админка", callback_data="admin")
        )

    bot.send_message(
        message.chat.id,
        "🔥 Добро пожаловать в магазин аккаунтов Brawl Stars!",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda c: c.data == "admin")
def admin(callback):
    bot.send_message(callback.message.chat.id, "📸 Отправь фото аккаунта")
    user_data[callback.from_user.id] = {"step": "photo"}

@bot.message_handler(content_types=["photo"])
def photo(message):
    uid = message.from_user.id

    if uid not in user_data:
        return

    if user_data[uid]["step"] == "photo":
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)

        photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        user_data[uid]["photo"] = photo_url
        user_data[uid]["step"] = "title"

        bot.send_message(message.chat.id, "📝 Введи название")

@bot.message_handler(func=lambda m: True)
def text(message):
    uid = message.from_user.id

    if uid not in user_data:
        return

    step = user_data[uid]["step"]

    if step == "title":
        user_data[uid]["title"] = message.text
        user_data[uid]["step"] = "description"
        bot.send_message(message.chat.id, "📄 Введи описание")

    elif step == "description":
        user_data[uid]["description"] = message.text
        user_data[uid]["step"] = "price"
        bot.send_message(message.chat.id, "💰 Введи цену")

    elif step == "price":
        user_data[uid]["price"] = message.text

        data = {
            "title": user_data[uid]["title"],
            "description": user_data[uid]["description"],
            "price": user_data[uid]["price"],
            "photo": user_data[uid]["photo"]
        }

        requests.post(f"{WEBAPP_URL}add", json=data)

        bot.send_message(message.chat.id, "✅ Аккаунт добавлен")

        del user_data[uid]

print("BOT STARTED")
bot.infinity_polling()
