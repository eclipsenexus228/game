import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Твой токен (лучше держать его в секрете!)
TOKEN = "8706720051:AAG0-LW48AzHbzGjy0eQzwHpZIjmF_LhpN4"

# Твоя ПРАВИЛЬНАЯ ссылка (без /groby/index.html)
WEB_APP_URL = "https://eclipsenexus228.github.io/game/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Играть в Могилу ⚰️", 
        web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    await message.answer(
        f"Привет! Нажми кнопку ниже, чтобы открыть игру.",
        reply_markup=builder.as_markup()
    )

async def main():
    print("Бот запущен...")
    # Удаляем вебхуки, чтобы бот точно отвечал на твои команды
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")