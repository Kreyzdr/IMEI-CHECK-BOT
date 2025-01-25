import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
import requests

from BD import is_user_whitelisted
from sekret.key import TELEGRAM_TOKEN, API_URL, API_TOKEN_SANDBOX

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()



def check_imei_via_api(imei):
    """Проверка IMEI через API"""
    response = requests.post(
        f"{API_URL}/check-imei",
        json={"imei": imei, "token": API_TOKEN_SANDBOX}
    )
    return response.json()



@router.message(Command("start"))
async def start(message: Message):
    """Обработчик команды /start"""
    await message.reply("Добро пожаловать! Отправьте IMEI для проверки.")



@router.message()
async def handle_imei(message: Message):
    """Обработчик текстовых сообщений (IMEI)"""
    user_id = message.from_user.id
    print(f"User ID: {user_id}")# Я это добавил чтобы можно было по быстрому узнать "User ID" и добавить его в белый список

    user_id = message.from_user.id
    imei = message.text.strip()

    # Проверяем пользователя в белом списке
    if not is_user_whitelisted(user_id):
        await message.reply("У вас нет доступа к этому боту.")
        return

    # Проверяем IMEI через API
    imei_info = check_imei_via_api(imei)
    await message.reply(f"Информация по IMEI: {imei_info}")



# Основная функция для запуска бота
async def main():
    # Регистрируем маршруты в диспетчере
    dp.include_router(router)

    # Удаляем вебхуки и запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())