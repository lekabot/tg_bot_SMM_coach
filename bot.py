import telebot
import config
import threading
import time
import re
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

file_path = "phone_numbers.txt"
bot = telebot.TeleBot(config.TOKEN)

last_contact_time = {}
waiting_for_phone = {}
current_keyboard = None


def check_10_seconds(user_id):
    current_time = time.time()
    if user_id not in last_contact_time:
        last_contact_time[user_id] = current_time
        return True
    else:
        elapsed_time = current_time - last_contact_time[user_id]
        if elapsed_time >= 10:
            return True
        else:
            return False


def get_video_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Посмотреть первое видео еще раз"))
    return keyboard


def send_second_video_message(chat_id):
    global current_keyboard
    if current_keyboard is None:
        current_keyboard = get_video_keyboard()
    current_keyboard.add(KeyboardButton("Посмотреть второе видео еще раз"))
    bot.send_message(chat_id,
                     "Привет! Вот еще один обучающий ролик специально для тебя! \nhttps://www.youtube.com/watch?v=pAgnJDJN4VA&ab_channel=acdcVEVO",
                     reply_markup=current_keyboard)


def send_third_message(chat_id, user_id):
    bot.send_message(chat_id,
                     "Привет, начинающий СММщик! Для продолжения нашего обучения приглашаю тебя присоединиться к нашему курсу \"СММ за 3 месяца\"\n"
                     "Напиши свой телефон по форме +7 (900) 999 99-99 и наш менеджер с тобой свяжется!")
    waiting_for_phone[user_id] = True


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Приветствую тебя, ученик СММ!")
    bot.send_message(message.chat.id, "Добро пожаловать в мир Социального Медиа Маркетинга!")
    current_keyboard = get_video_keyboard()
    bot.send_message(message.chat.id,
                     "Для начала, посмотри это обучающее видео: \nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley")
    bot.send_message(message.chat.id, "Готов к увлекательному обучению? Поехали!", reply_markup=current_keyboard)
    threading.Timer(10, schedule_second_video_message, args=(message.from_user.id,)).start()


def schedule_second_video_message(user_id):
    if check_10_seconds(user_id):
        send_second_video_message(user_id)
        last_contact_time[user_id] = time.time()
        threading.Timer(10, send_third_message, args=(user_id, user_id)).start()


@bot.message_handler(func=lambda message: message.text == "Посмотреть первое видео еще раз")
def send_first_video_again(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley")


@bot.message_handler(func=lambda message: message.text == "Посмотреть второе видео еще раз")
def send_second_video_again(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "\nhttps://www.youtube.com/watch?v=pAgnJDJN4VA&ab_channel=acdcVEVO")


@bot.message_handler(func=lambda message: message.text == "Изменить номер телефона")
def handle_change_phone_request(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите новый номер телефона:")
    bot.register_next_step_handler(message, handle_change_phone)


def handle_change_phone(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    phone_number = message.text.strip()

    if not validate_phone_number(phone_number):
        bot.send_message(chat_id, "Неправильный формат телефонного номера. Попробуй еще раз.")
        return

    username = message.from_user.username or "Unknown"
    if update_phone_number_in_database(username, phone_number):
        bot.send_message(chat_id, "Ваш номер телефона был обновлен.")
    else:
        bot.send_message(chat_id, "Это ваш старый номер телефона.")


def update_phone_number_in_database(username, new_phone_number):
    updated = False
    lines = []
    with open("phone_numbers.txt", "r") as file:
        for line in file:
            data = line.strip().split()
            if len(data) >= 2 and data[0] == username:
                old_phone_number = data[1]
                if old_phone_number == new_phone_number:
                    return False  # Номер не изменился, не требуется обновление
                updated = True
                line = f"{username} {new_phone_number} 0\n"  # Обновляем номер телефона
            lines.append(line)

    # Если пользователь не найден, добавляем его в конец файла
    if not updated:
        lines.append(f"{username} {new_phone_number} 0\n")

    with open("phone_numbers.txt", "w") as file:
        file.writelines(lines)

    return True


@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    user_id = message.from_user.id
    if user_id in waiting_for_phone and waiting_for_phone[user_id]:
        phone_number = message.text.strip()
        if validate_phone_number(phone_number):
            if not phone_number_in_database(phone_number):
                username = message.from_user.username or "Unknown"
                save_phone_number_to_file(username, phone_number)
                if current_keyboard is None:
                    send_second_video_message(message.chat.id)
                current_keyboard.add(KeyboardButton("Изменить номер телефона"))
                bot.send_message(message.chat.id,
                                 "Твой номер телефона был добавлен в базу данных. Ожидай, пока наш менеджер с тобой свяжется!",
                                 reply_markup=current_keyboard)
                waiting_for_phone[user_id] = True
                waiting_for_phone.pop(user_id)
            else:
                if current_keyboard is None:
                    send_second_video_message(message.chat.id)
                current_keyboard.add(KeyboardButton("Изменить номер телефона"))
                bot.send_message(message.chat.id,
                                 "Твой номер телефона уже есть в нашей базе данных. Мы обязательно с тобой свяжемся.",
                                 reply_markup=current_keyboard)
        else:
            bot.send_message(message.chat.id, "Неправильный формат телефонного номера. Попробуй еще раз.")
    else:
        bot.send_message(message.chat.id, "Приходи за вторым обучающим видео завтра!")


def validate_phone_number(phone_number):
    pattern = r'^(\+7)\d{10}$'
    return bool(re.match(pattern, phone_number))


def phone_number_in_database(phone_number):
    with open("phone_numbers.txt", "r") as file:
        for line in file:
            data = line.strip().split()
            if len(data) >= 2 and data[1] == phone_number:
                return True
    return False


def save_phone_number_to_file(username, phone_number):
    with open("phone_numbers.txt", "a") as file:
        file.write(f"{username} {phone_number} 0\n")


def send_fourth_video(chat_id):
    bot.send_message(chat_id, "Наш менеджер связался с тобой и мы "
                              "подписали тебя на курс СММ за 3 месяца, держи "
                              "в подарок следующий видеоурок. \nhttps://www.youtube.com/watch?v=O4irXQhgMqg&list=RDpAgnJDJN4VA&index=3&ab_channel=ABKCOVEVO")




bot.polling()
