"""
==================== REQUIREMENTS ====================
pip install python-telegram-bot==20.3
======================================================
"""

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = "8522287264:AAG3f1B87DN2BOUzBh1YKHXAerYLh2Blxoo"
ADMINS = [7764057183]

# CHANNELS WITH YOUR INVITE LINKS
CHANNELS = [
    {"name": " BackUp Channel", "link": "https://t.me/+5VpjgantffdlOWM1"},
    {"name": "Channel 2", "link": "https://t.me/+QL7HaAXjTeNmNWVl"},
    {"name": "Channel 3", "link": "https://t.me/+jmiP8aD4jSs4ZGY1"},
    {"name": "Channel 4", "link": "https://t.me/+Gm80WqnuhD82ZTU1"},
    {"name": "Channel 5", "link": "https://t.me/+V8RJPD1xigdlM2Q1"},
    {"name": "Channel 6", "link": "https://t.me/+FrHG5Zz433NkNzY1"},
    {"name": "Free Bots 7", "link": "https://t.me/+kL_XzrqrcOlhN2M1"},
]

TOTAL_USERS = set()
logging.basicConfig(level=logging.INFO)

# BUTTON GENERATOR
def force_buttons():
    btns = []
    for ch in CHANNELS:
        btns.append([InlineKeyboardButton(ch["name"], url=ch["link"])])
    btns.append([InlineKeyboardButton("✔ Joined", callback_data="joined")])
    return InlineKeyboardMarkup(btns)

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    TOTAL_USERS.add(user)

    await update.message.reply_text(
        "⚠ Please join all channels first:",
        reply_markup=force_buttons()
    )

# JOIN BUTTON CALLBACK
async def joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.message.edit_text(
        "🎉 Access Granted!\nHere are all channel links:",
        reply_markup=force_buttons()
    )

# BROADCAST
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Broadcast ke liye reply karo.")
        return

    msg = update.message.reply_to_message
    success = 0
    fail = 0

    for user in list(TOTAL_USERS):
        try:
            await context.bot.copy_message(
                chat_id=user,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )
            success += 1
        except:
            fail += 1

    await update.message.reply_text(
        f"📢 Broadcast completed!\nSuccess: {success}\nFail: {fail}"
    )

# STATS
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return

    await update.message.reply_text(
        f"📊 Stats:\nTotal Users: {len(TOTAL_USERS)}"
    )

# MAIN RUN
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(joined, pattern="joined"))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.idle()

import asyncio
if __name__ == "__main__":
    asyncio.run(main())