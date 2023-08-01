from db import BotDB

async def insert_user(user_id: int) -> None:
    BotDB = BotDB('database.db')
    if (not BotDB.user_exists(user_id)):
        await BotDB().add_user(user_id)
