import asyncio
import aiosqlite
from pathlib import Path

class SqliteUserDataManager:
    def __init__(self, db_file="users.db"):
        self.db_file = Path(db_file)
        self.lock = asyncio.Lock()
        self.initialized = False


    # Этот код представляет собой асинхронный метод _ensure_db_exists, который проверяет и при необходимости создает базу данных SQLite с таблицей users.
    async def _ensure_db_exists(self):
        if self.initialized:
            return
            
        # Использование асинхронного блокировщика для предотвращения race condition (состояния гонки), когда несколько потоков/корутин могут попытаться инициализировать базу одновременно
        async with self.lock:
            if self.initialized:  # Дважды проверьте блокировку
                return
            
            # Подключение к SQLite базе данных с использованием асинхронной библиотеки aiosqlite.
            async with aiosqlite.connect(self.db_file) as db:
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        subscribed BOOLEAN DEFAULT 1,
                        created_at REAL
                    )
                ''')
                await db.commit()
            self.initialized = True
        
    # Этот код представляет собой асинхронный метод add_user, который добавляет пользователя в базу данных SQLite.
    async def add_user(self, user_id, username=None):
        await self._ensure_db_exists()
        async with self.lock:
            async with aiosqlite.connect(self.db_file) as db:
                await db.execute(
                    '''
                    INSERT OR IGNORE INTO users (user_id, username, created_at)
                    VALUES (?, ?, ?)
                    ''',
                    (user_id, username, asyncio.get_event_loop().time())
                )
                # Обновляем имя пользователя, если оно изменилось
                if username is not None:
                    await db.execute(
                        "UPDATE users SET username = ? WHERE user_id = ?",
                        (username, user_id)
                    )
                await db.commit()
    
    # Этот код представляет собой асинхронный метод get_user, который получает информацию о пользователе из базы данных SQLite по его ID.
    async def get_all_users(self):
        await self._ensure_db_exists()
        async with self.lock:
            async with aiosqlite.connect(self.db_file) as db:
                cursor = await db.execute("SELECT * FROM users")
                rows = await cursor.fetchall()
                return {
                    row[0]: {
                        "username": row[1],
                        "subscribed": bool(row[2]),
                        "created_at": row[3]
                    } for row in rows
                }