import os
import random
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

TOKEN = os.getenv("8980664445:AAFTu5JTFP6FX2S1tti55wLKpiTI7May1lA")


GIFS_DIR = Path(__file__).parent / "gifs"
GIFS_DIR.mkdir(exist_ok=True)


VIDEO_DIR = Path(__file__).parent / "videos"
VIDEO_DIR.mkdir(exist_ok=True)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Привет"), KeyboardButton("Как дела?")],
        [KeyboardButton("Помощь"), KeyboardButton("Пока")],
        [KeyboardButton("Гифки")],
    ],
    resize_keyboard=True,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой телеграм-бот. Как могу помочь?",
        reply_markup=MAIN_KEYBOARD,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды:\n"
        "/start - начать\n"
        "/help - помощь\n"
        "/about - обо мне\n"
        "/gif - случайная гифка\n"
        "/bye - попрощаться\n"
        "/gifvid - случайная гифка как видео\n\n"
        "Также можно нажимать кнопки на клавиатуре.\n"
        "Кнопка «Гифки» пришлёт случайную гифку из каталога."
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я учебный бот на python-telegram-bot v21.")


async def send_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gifs = [
        p for p in GIFS_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".gif", ".mp4"}
    ]
    if not gifs:
        await update.message.reply_text(
            f"Пока нет гифок. Положи .gif (или .mp4) файлы в папку:\n{GIFS_DIR}"
        )
        return
    gif = random.choice(gifs)
    await update.message.reply_animation(animation=str(gif))



async def send_gif_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
 
    videos = [
        p for p in VIDEO_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".m4v"}
    ]
  
    if not videos:
        videos = [
            p for p in GIFS_DIR.iterdir()
            if p.is_file() and p.suffix.lower() in {".gif", ".mp4"}
        ]
    if not videos:
        await update.message.reply_text(
            "Пока нет видео/гифок. Положи .mp4 в папку:\n"
            f"{VIDEO_DIR}\n"
            "или .gif/.mp4 в папку:\n"
            f"{GIFS_DIR}"
        )
        return
    video = random.choice(videos)
    with open(video, "rb") as f:
        await update.message.reply_video(video=f)


async def gif_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_gif(update, context)


async def bye_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("До встречи! Хорошего дня!")



async def gifvid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_gif_video(update, context)


async def handler_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    if "привет" in text:
        await update.message.reply_text("Привет! Как твои дела?")
    elif "как дела" in text:
        await update.message.reply_text("У меня всё отлично, спасибо!")
    elif "помощь" in text:
        await help_command(update, context)
    elif "пока" in text:
        await update.message.reply_text("До встречи! Хорошего дня!")
    elif "гифк" in text:
        await send_gif(update, context)
    else:
        await update.message.reply_text("Извини, я пока это не понимаю")



async def handler_video_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()

    if "видео" in text and ("гиф" in text or text.strip() == "видео"):
        await send_gif_video(update, context)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("gif", gif_command))
    app.add_handler(CommandHandler("bye", bye_command))
    app.add_handler(CommandHandler("gifvid", gifvid_command))


    app.add_handler(MessageHandler(filters.Regex(r"(?i)видео"), handler_video_text))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_text))

    app.run_polling()