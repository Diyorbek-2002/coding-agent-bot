"""
bot.py — Telegram bot: foydalanuvchi vazifa yuboradi, agent javob beradi
"""
import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
from dotenv import load_dotenv
from agent_core import run_agent

load_dotenv()

MAX_MSG = 4000


def _split(text: str, limit: int = MAX_MSG) -> list[str]:
    """Uzun matnni Telegram limit bo'yicha bo'ladi."""
    if len(text) <= limit:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + limit])
        start += limit
    return chunks


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Salom! Men coding agentman.\n\n"
        "Menga istalgan vazifa yuboring — kod yozib, ishga tushirib, natijani qaytaraman.\n\n"
        "Misollar:\n"
        "• fibonacci funksiya yoz\n"
        "• bubble sort algoritmini yoz va test qil\n"
        "• ro'yxatdan dublikatlarni olib tashla\n\n"
        "/help — yordam"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Ishlash tartibi:\n"
        "1. Menga vazifa yozing\n"
        "2. Agent kod yozadi va ishga tushiradi\n"
        "3. Xato bo'lsa o'zi tuzatadi (max 3 urinish)\n"
        "4. Kod va natija yuboriladi\n\n"
        "/start — boshlash\n"
        "/help — yordam"
    )


async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task = update.message.text.strip()

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_text("⏳ Ishlayapman...")

    try:
        result = await asyncio.to_thread(run_agent, task)
    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")
        return

    for chunk in _split(result):
        try:
            await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception:
            await update.message.reply_text(chunk)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("TELEGRAM_BOT_TOKEN .env da topilmadi!")
        return

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task))

    print("Bot ishga tushdi. To'xtatish uchun Ctrl+C")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
