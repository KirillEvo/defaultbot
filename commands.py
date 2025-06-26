# Импортируем настройки ID админа из нашего файла config.py
from config import ADMIN_ID

# Простая команда которая отдает приветствие при выполнении /start в самом боте
async def start_command(message, data):
    user = message.from_user
    await data.add_user(user.id, user.username)
    await message.answer("Прииииивеееееет!",)

# Команда для получения списка всех пользователей, но только для админа
async def allusers_command(message, data):
    user_id = message.from_user.id
    admin_id = int(ADMIN_ID)

    if user_id != admin_id:
        await message.answer("❌ У вас нет прав для выполнения этой команды.")
        return

    try:
        users = await data.get_all_users()
        count = len(users)
        await message.answer(f"Количество пользователей: {count}")
    except Exception as e:
        await message.answer("Ошибка при получении списка пользователей.")
        print(f"[ERROR] {e}")