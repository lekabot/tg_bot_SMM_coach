# import telebot
# import config
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
#
# file_path = "phone_numbers.txt"
# bot = telebot.TeleBot(config.TOKEN)
#
# last_contact_time = {}
# waiting_for_phone = {}
# current_keyboard = None
#
#
# def check_status_and_send_message():
#     with open(file_path, "r") as file:
#         for line in file:
#             data = line.strip().split()
#             if len(data) >= 3 and data[2] == "1":
#                 username = data[0]
#                 chat_id = get_user_chat_id_by_username(username)
#                 if chat_id:
#                     send_fourth_video(chat_id)
#
#
# def get_user_chat_id_by_username(username):
#     with open(file_path, "r") as file:
#         for line in file:
#             data = line.strip().split()
#             if len(data) >= 2 and data[0] == username:
#                 return int(data[2])
#     return None
#
#
# def update_phone_number_status(username, new_status):
#     updated = False
#     lines = []
#     with open(file_path, "r") as file:
#         for line in file:
#             data = line.strip().split()
#             if len(data) >= 2 and data[0] == username:
#                 line = f"{username} {data[1]} {new_status}\n"
#                 updated = True
#             lines.append(line)
#
#     with open(file_path, "w") as file:
#         file.writelines(lines)
#
#     return updated
#
#
# def send_fourth_video(chat_id):
#     bot.send_message(chat_id, "Наш менеджер связался с тобой и мы "
#                               "подписали тебя на курс СММ за 3 месяца, держи "
#                               "в подарок следующий видеоурок. \nhttps://www.youtube.com/watch?v=O4irXQhgMqg&list=RDpAgnJDJN4VA&index=3&ab_channel=ABKCOVEVO")
#
#
# class MyHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         if event.is_directory:
#             return
#
#         if event.src_path == file_path:
#             check_status_and_send_message()
#
#
# if __name__ == "__main__":
#     observer = Observer()
#     event_handler = MyHandler()
#     observer.schedule(event_handler, path=".", recursive=False)
#     observer.start()
#
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
#
#     bot.polling()
