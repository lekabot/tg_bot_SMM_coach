import bot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

file_path = "phone_numbers.txt"

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        if event.src_path == "phone_numbers.txt":  # Замените на путь к вашему текстовому файлу
            with open(event.src_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 3 and parts[2] == "0":
                        bot.send_fourth_video(parts[0])


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path="/path/to/your",
                      recursive=False)  # Замените на каталог, в котором находится ваш текстовый файл
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def get_user_chat_id_by_username(username):
    with open("phone_numbers.txt", "r") as file:
        for line in file:
            data = line.strip().split()
            if len(data) == 3 and data[0] == username:
                return int(data[2])
    return None
