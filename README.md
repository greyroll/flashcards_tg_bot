## Flashcards Telegram Bot

Этот бот помогает изучать английские слова, используя карточки, подобные Anki.

### 📌 Функции
- Выбор колоды слов
- Запуск сессии изучения слов
- Переключение между сторонами карточки (вопрос-ответ)
- Отметка изученных слов
- Завершение сессии с отображением статистики

### 🚀 Установка и запуск
#### 1. Клонирование репозитория
```sh
git clone https://github.com/greyroll/flashcards_tg_bot.git
```
#### 2. Настройка окружения (.env)
Создайте файл `.env` в корне проекта и укажите:
```
BOT_TOKEN = "your_token_here"
BASE_URL = "http://your_url_here"
```
#### 3. Установка зависимостей

```sh
pip install -r requirements.txt
```
#### 4. Запуск бота
```sh
python main.py
```

Бот взаимодействует с бэкендом через BACKEND_URL.

бэкенд: [flashcards_back](https://github.com/greyroll/flashcards_back)
