# ------------------ FLASK SERVER (Render ke liye) ------------------
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running on Render!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)


# ------------------ TELEGRAM BOT CODE ------------------
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = "8522287264:AAG3f1B87DN2BOUzBh1YKHXAerYLh2Blxoo"
ADMINS = [7764057183]

CHANNELS = [
    {"name": "BackUp Channel", "link": "https://t.me/+5VpjgantffdlOWM1"},
    {"name": "Channel 2", "link": "https://t.me/+QL7HaAXjTeNmNWVl"},
    {"name": "Channel 3", "link": "https://t.me/+jmiP8aD4jSs4ZGY1"},
    {"name": "Channel 4", "link": "https://t.me/+Gm80WqnuhD82ZTU1"},
    {"name": "Channel 5", "link": "https://t.me/+V8RJPD1xigdlM2Q1"},
    {"name": "Channel 6", "link": "https://t.me/+FrHG5Zz433NkNzY1"},
    {"name": "Free Bots 7", "link": "https://t.me/+kL_XzrqrcOlhN2M1"},
]

TOTAL_USERS = set()
logging.basicConfig(level=logging.INFO)


# ------------------ BUTTONS ------------------
def force_buttons():
    btns = []
    for c in CHANNELS:
        btns.append([InlineKeyboardButton(c["name"], url=c["link"])])
    btns.append([InlineKeyboardButton("✔ Joined", callback_data="joined")])
    return InlineKeyboardMarkup(btns)


# ------------------ START ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    TOTAL_USERS.add(user)

    await update.message.reply_text(
        "⚠ Please join all channels first:",
        reply_markup=force_buttons()
    )


# ------------------ JOINED ------------------
async def joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.message.edit_text(
        "🎉 Access Granted!\nHere are all channel links:",
        reply_markup=force_buttons()
    )


# ------------------ BROADCAST ------------------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Broadcast ke liye reply karo.")
        return

    msg = update.message.reply_to_message
    ok, fail = 0, 0

    for uid in list(TOTAL_USERS):
        try:
            await context.bot.copy_message(
                chat_id=uid, from_chat_id=msg.chat_id, message_id=msg.message_id
            )
            ok += 1
        except:
            fail += 1

    await update.message.reply_text(f"Broadcast Done!\nSuccess: {ok}\nFail: {fail}")


# ------------------ STATS ------------------
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return

    await update.message.reply_text(f"Total Users: {len(TOTAL_USERS)}")


# ------------------ MAIN BOT RUN ------------------
async def run_bot():
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("broadcast", broadcast))
    bot.add_handler(CommandHandler("stats", stats))
    bot.add_handler(CallbackQueryHandler(joined, pattern="joined"))

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()
    await bot.idle()


# ------------------ COMBINED RUNNER ------------------
import asyncio

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(run_bot())
