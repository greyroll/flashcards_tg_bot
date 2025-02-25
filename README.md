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
git clone <репозиторий>
cd flashcards_tg_bot
```

#### 2. Создание виртуального окружения и установка зависимостей

```sh
python -m venv .venv
source .venv/bin/activate  # Для macOS/Linux
.venv\Scripts\activate     # Для Windows

pip install -r requirements.txt
```
#### 3. В файле config.py укажите токен телеграм-бота и url сервера
```
BOT_TOKEN = "your_token_here"
BASE_URL = "http://your_url_here"
```
#### 4. Запуск бота
```sh
python main.py
```

Бот взаимодействует с бэкендом через BASE_URL.
