
-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    phone_number TEXT UNIQUE,
    verified BOOLEAN NOT NULL DEFAULT 0
);

-- Таблица видеоуроков
CREATE TABLE IF NOT EXISTS video_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT,
    price DECIMAL NOT NULL
);

-- Таблица покупок
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lesson_id INTEGER NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES video_lessons (id)
);

INSERT INTO video_lessons (title, link, price) VALUES ('Урок 1', 'https://www.youtube.com/watch?v=ZmrC1QyQZWk&list=PLA7tIFWESalzcP80GYV-uoHqzphPKJ9S-&ab_channel=AntonSaburov', 0.0);
INSERT INTO video_lessons (title, link, price) VALUES ('Урок 2', 'https://www.youtube.com/watch?v=ApBySvo7ZuY&list=PLA7tIFWESalzcP80GYV-uoHqzphPKJ9S-&index=2&ab_channel=AntonSaburov', 0.0);
INSERT INTO video_lessons (title, link, price) VALUES ('Урок 3', 'https://www.youtube.com/watch?v=FiazmLa5R_k&list=PLA7tIFWESalzcP80GYV-uoHqzphPKJ9S-&index=3&ab_channel=AntonSaburov', 0.0);
INSERT INTO video_lessons (title, link, price) VALUES ('Урок 4', 'https://www.youtube.com/watch?v=BUHCsr8Alks&list=PLA7tIFWESalzcP80GYV-uoHqzphPKJ9S-&index=4&ab_channel=AntonSaburov', 100.0);
INSERT INTO video_lessons (title, link, price) VALUES ('Урок 5', 'https://www.youtube.com/watch?v=B5F0ivikWRY&list=PLA7tIFWESalzcP80GYV-uoHqzphPKJ9S-&index=5&ab_channel=AntonSaburov', 150.0);
INSERT INTO video_lessons (title, link, price) VALUES ('Урок 6', 'https://www.youtube.com/watch?v=OiUjlCKrIFo&list=PLA7tIFWESalzcP80GYV-uoHqzphPKJ9S-&index=6&ab_channel=AntonSaburov', 200.0);
INSERT INTO video_lessons (title, link, price) VALUES ('Урок 7', 'https://www.youtube.com/watch?v=ZSUtpA0XKGs&list=PLA7tIFWESalzcP80GYV-uoHqzphPKJ9S-&index=7&ab_channel=AntonSaburov', 250.0);
