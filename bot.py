import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ChatJoinRequestHandler,
)

# Logging
logging.basicConfig(level=logging.INFO)

# Token from Render ENV
TOKEN = os.getenv("TOKEN")

WELCOME_MSG = """Hey! Welcome ❤️🫶🏼
Aapki join request approve ho jyegi soon ✅

Main channel join kar lo yaha:
https://t.me/+Pi6GvsfYlFUzZTg1

Updates miss mat karna! 🔥
"""

# Store users
users = set()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    await update.message.reply_text(
        "🤖 *Auto Approve Bot*\n\n"
        "Commands:\n"
        "/approve - Accept all pending requests\n"
        "/broadcast <msg> - Send to all users\n"
        "/help - Show commands",
        parse_mode="Markdown"
    )

# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# Join request handler
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    user = req.from_user
    try:
        await context.bot.send_message(chat_id=user.id, text=WELCOME_MSG)
    except:
        pass

# Approve all requests
async def approve_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot
    approved = 0

    try:
        requests = await bot.get_chat_join_requests(chat_id)

        for r in requests:
            try:
                await bot.approve_chat_join_request(chat_id, r.user_chat_id)
                approved += 1
            except:
                pass

        await bot.send_message(
            chat_id=chat_id,
            text=f"✅ Approved: {approved}"
        )

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Admin check
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = await context.bot.get_chat_member(
        update.effective_chat.id, update.effective_user.id
    )
    return chat_member.status in ["administrator", "creator"]

# Broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast message")
        return

    msg = " ".join(context.args)
    sent = 0

    for u in users:
        try:
            await context.bot.send_message(chat_id=u, text=msg)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"📢 Sent to {sent} users")

# Main
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("approve", approve_all))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(ChatJoinRequestHandler(join_request))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
