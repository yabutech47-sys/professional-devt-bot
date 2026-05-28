import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler

# --- CONFIGURATION ---
BOT_TOKEN = os.getenv("BOT_TOKEN")

COURSES = [
    {"name": "Edify Ethiopia Overview ", "url": "https://app.mindsmith.ai/learn/cmg7jrxkv01bvlb04ses7x8i6"},
    {"name": "Discovering Your Values: A Guide to Good Choices", "url": "https://app.mindsmith.ai/learn/cmffk2f3303ubk104jqghqex2"},
    {"name": "Effective Teaching Methodologies for Early Childhood Education in Ethiopia", "url": "https://app.mindsmith.ai/learn/cmmduqj3i03gsl504srt6078y"},
    {"name": "Assessment & Classroom Management for Ethiopian Primary Teachers", "url": "https://app.mindsmith.ai/learn/cmo4cwxj4003p04l5gp140980"},
]

app = FastAPI()

# Global variable for the application instance
ptb_app = None

async def get_ptb_app():
    global ptb_app
    if ptb_app is None:
        ptb_app = ApplicationBuilder().token(BOT_TOKEN).build()
        ptb_app.add_handler(CommandHandler("start", start))
        # This is the key: initialize the app before it starts taking requests
        await ptb_app.initialize()
    return ptb_app

async def start(update: Update, context):
    keyboard = []
    for course in COURSES:
        keyboard.append([InlineKeyboardButton(text=f"{course['name']}", web_app=WebAppInfo(url=course['url']))])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Select a course to begin:", reply_markup=reply_markup)

@app.post("/api/webhook")
async def webhook_handler(request: Request):
    bot_instance = await get_ptb_app()
    data = await request.json()
    update = Update.de_json(data, bot_instance.bot)
    
    # Process the update through the library logic
    await bot_instance.process_update(update)
    
    return {"status": "ok"}

@app.get("/")
def index():
    return {"message": "Mindsmith Bot is running!", "token_present": BOT_TOKEN is not None}