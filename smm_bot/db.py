import sqlite3

class BotDB:

    def __init__(self, db_file) -> None:
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.connection.commit()
    
    def add_phone_number(self, user_id, phone_number):
        self.cursor.execute("UPDATE users SET phone_number = ? WHERE user_id = ?", (phone_number, user_id))
        self.conn.commit()

    def buy_lesson(self, user_id, lesson_id):
        try:
            self.cursor.execute("INSERT INTO purchases (user_id, lesson_id) VALUES (?, ?)", (user_id, lesson_id))
            self.conn.commit()
            print("Покупка успешно добавлена в базу данных.")
        except sqlite3.IntegrityError:
            print("Покупка уже существует для данного пользователя и урока.")

    def is_purchased(self, user_id, lesson_id):
        result = self.cursor.execute("SELECT `id` FROM `purchases` WHERE `user_id` = ? AND `lesson_id` = ?", (user_id, lesson_id))
        return bool(len(result.fetchall()))
    
    def close(self):
        self.connection.close()