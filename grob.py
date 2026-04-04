import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web
import aiohttp_cors

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8706720051:AAG0-LW48AzHbzGjy0eQzwHpZIjmF_LhpN4"
WEB_APP_URL = "https://eclipsenexus228.github.io/game/"
DB_FILE = "players.json"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

# --- API ДЛЯ ИГРЫ ---
async def get_players(request):
    return web.json_response(list(load_db().values()))

async def update_progress(request):
    data = await request.json()
    user_id = str(data.get("id"))
    change = int(data.get("change", 0))
    
    db = load_db()
    if user_id in db:
        db[user_id]["progress"] = max(0, min(100, db[user_id]["progress"] + change))
        save_db(db)
        return web.json_response({"status": "ok", "new_progress": db[user_id]["progress"]})
    return web.json_response({"status": "error"}, status=404)

# --- БОТ ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    db = load_db()
    uid = str(message.from_user.id)
    if uid not in db:
        db[uid] = {
            "id": uid,
            "name": message.from_user.first_name,
            "nick": f"@{message.from_user.username}" or "incognito",
            "progress": 0
        }
        save_db(db)
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Играть ⚰️", web_app=WebAppInfo(url=WEB_APP_URL)))
    await message.answer("Могила ждет тебя!", reply_markup=builder.as_markup())

# --- ЗАПУСК СЕРВЕРА И БОТА ---
async def main():
    # Создаем веб-приложение для API
    app = web.Application()
    app.router.add_get('/api/players', get_players)
    app.router.add_post('/api/update', update_progress)

    # Разрешаем сайту на GitHub обращаться к твоему компу
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")
    })
    for route in list(app.router.routes()):
        cors.add(route)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080) # Порт 8080
    
    print("API Сервер запущен на порту 8080...")
    asyncio.create_task(site.start())
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())