import os
import asyncio
from io import BytesIO

import yt_dlp
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أرسل رابط TikTok وسأحاول استخراج الصور فقط من المنشور."
    )


def extract_images(url: str):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # TikTok photo posts commonly expose image URLs in thumbnails/formats.
    images = []

    # Prefer slideshow entries when available.
    for entry in (info.get("entries") or []):
        if not entry:
            continue
        u = entry.get("url") or entry.get("thumbnail")
        if u and u not in images:
            images.append(u)

    # Some extractors expose images through thumbnails.
    thumbs = info.get("thumbnails") or []
    for t in thumbs:
        u = t.get("url")
        if u and u not in images:
            images.append(u)

    return images


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = (update.message.text or "").strip()

    if "tiktok.com" not in url and "vt.tiktok.com" not in url:
        await update.message.reply_text("أرسل رابط TikTok صحيح.")
        return

    msg = await update.message.reply_text("⏳ جاري استخراج الصور...")

    try:
        images = await asyncio.to_thread(extract_images, url)

        if not images:
            await msg.edit_text(
                "❌ لم أجد صورًا في هذا المنشور. تأكد أنه منشور صور وليس فيديو."
            )
            return

        await msg.edit_text(f"🖼️ تم العثور على {len(images)} صورة.")

        for image_url in images:
            try:
                await update.message.reply_photo(photo=image_url)
            except Exception:
                # Skip an individual image if Telegram cannot fetch it.
                continue

    except Exception as e:
        await msg.edit_text("❌ حدث خطأ أثناء استخراج الصور. جرّب رابط TikTok آخر.")
        print("ERROR:", repr(e))


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
