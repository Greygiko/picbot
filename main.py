import os
import requests
from bs4 import BeautifulSoup
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توکن بات از متغیر محیطی (برای رندر و گیت هاب امن)
TELEGRAM_TOKEN = os.environ.get(8235825259:AAHSq8W11LBZbw-p84WJqcONrU72ciufk6U)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "سلام! برای جستجوی عکس پینترست، بنویس:\n@Pinterest <کلمه>\n"
        "مثال: @Pinterest cat"
    )

def pinterest_search(query, max_results=5):
    """
    جستجوی پینترست و گرفتن چند عکس اول
    """
    url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # گرفتن چند تصویر
    img_tags = soup.find_all("img", limit=max_results)
    img_urls = [img["src"] for img in img_tags if img.get("src")]
    return img_urls

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text.startswith("@Pinterest "):
        query = text[len("@Pinterest "):]
        image_urls = pinterest_search(query, max_results=5)  # تعداد عکس‌ها رو اینجا تنظیم کن
        if image_urls:
            media = [InputMediaPhoto(url) for url in image_urls]
            update.message.reply_media_group(media)
        else:
            update.message.reply_text("عکسی پیدا نشد.")

def main():
    if not TELEGRAM_TOKEN:
        print("لطفاً توکن بات را در متغیر محیطی TELEGRAM_TOKEN قرار دهید!")
        return

    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("بات شروع شد...")
    updater.start_polling()
    updater.idle()

if name == "main":
    main()
