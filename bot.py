from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import schedule
import time
import threading

TOKEN = "BURAYA_TOKEN"

user_data = {}

# Tarih kaydetme komutu
async def setdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    
    if len(context.args) == 0:
        await update.message.reply_text("Tarih gir: /setdate 2026-12-31")
        return
    
    try:
        target_date = datetime.strptime(context.args[0], "%Y-%m-%d")
        user_data[user_id] = target_date
        await update.message.reply_text("Tarih kaydedildi ✅")
    except:
        await update.message.reply_text("Format yanlış! Örnek: 2026-12-31")

# Gün sayısı hesaplama
def days_left(target_date):
    return (target_date - datetime.now()).days

# Her gün mesaj gönderme
async def send_daily(app):
    for user_id, target_date in user_data.items():
        kalan = days_left(target_date)
        await app.bot.send_message(chat_id=user_id, text=f"{kalan} gün kaldı ⏳")

# Scheduler thread
def run_scheduler(app):
    schedule.every().day.at("09:00").do(lambda: app.create_task(send_daily(app)))
    while True:
        schedule.run_pending()
        time.sleep(1)

# Botu başlat
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("setdate", setdate))

    threading.Thread(target=run_scheduler, args=(app,), daemon=True).start()

    print("Bot çalışıyor...")
    await app.run_polling()

import asyncio
asyncio.run(main())
