import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ChatJoinRequestHandler,
)

import os
TOKEN = os.getenv("TOKEN")

WELCOME_MSG = """Hey! Welcome ❤️🫶🏼
Aapki join request approve ho jyegi soon ✅

Main channel join kar lo yaha:
https://t.me/+Pi6GvsfYlFUzZTg1

Updates miss mat karna! 🔥
"""

logging.basicConfig(level=logging.INFO)

# Store users for broadcast
users = set()

# /start → show all commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    await update.message.reply_text(
        "🤖 *Auto Approve Bot*\n\n"
        "Available Commands:\n"
        "/approve - Accept all pending requests\n"
        "/broadcast <message> - Send message to all users\n"
        "/help - Show commands\n",
        parse_mode="Markdown"
    )

# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# When join request comes → instant DM
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    user = req.from_user
    try:
        await context.bot.send_message(chat_id=user.id, text=WELCOME_MSG)
    except:
        pass

# /approve → accept all pending
async def approve_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot
    approved = 0
    rejected = 0

    try:
        requests = await bot.get_chat_join_requests(chat_id)

        for r in requests:
            try:
                await bot.approve_chat_join_request(chat_id, r.user_chat_id)
                approved += 1
            except:
                rejected += 1

        await bot.send_message(
            chat_id=chat_id,
            text=(
                f"✅ ALL REQUEST APPROVED DONE ✓\n\n"
                f"👍 Approved: {approved}\n"
                f"❌ Rejected: {rejected}\n\n"
                f"RG - @SAVAN_JOD / @UR_SAVAN\n\n"
                f"Feedback dena na bhoolen ❤️"
            )
        )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Check admin
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = await context.bot.get_chat_member(
        update.effective_chat.id, update.effective_user.id
    )
    return chat_member.status in ["administrator", "creator"]

# /broadcast → admin only
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

    await update.message.reply_text(f"📢 Broadcast sent to {sent} users")

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
  
