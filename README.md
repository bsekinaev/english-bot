# 🎓 English Vocabulary Bot | Бот для изучения английских слов

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-2.x-green.svg)](https://docs.aiogram.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Телеграм-бот с системой интервальных повторений (SRS) для эффективного изучения английской лексики.

## 🌟 Основные возможности

### 📚 Управление словарем
- Добавление слов через бота (`/add слово - перевод`)
- Поддержка мульти-категорий (базовые, работа, путешествия)
- Примеры использования слов в контексте
- Уровни сложности (A1-C2)

### 🔁 Система повторений
- Умные напоминания по алгоритму Лейтнера
- Автоматический расчет интервалов повторений
- Адаптация под успеваемость пользователя

### 📊 Аналитика прогресса
- Статистика по изученным словам
- Графики прогресса (в разработке)
- Экспорт данных в CSV

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.9+
- Telegram bot token от [@BotFather](https://t.me/BotFather)

### Установка
```bash
git clone https://github.com/bsekinaev/english-bot.git
cd english-bot
pip install -r requirements.txt
Настройка
Создайте файл .env:

ini
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id
DATABASE_URL=sqlite:///data/vocabulary.db
Запуск
bash
python src/main.py
🖼 Скриншоты интерфейса
Главное меню	Режим изучения	Статистика
Меню	Обучение	Статистика
🏗 Архитектура проекта
english-bot/
├── data/
│   ├── words.json       # Основной словарь
│   └── vocabulary.db    # База данных SQLite
├── src/
│   ├── handlers/        # Обработчики команд
│   ├── services/        # Бизнес-логика
│   ├── utils/           # Вспомогательные функции
│   ├── config.py        # Конфигурация приложения
│   └── main.py         # Точка входа
├── tests/               # Юнит-тесты
├── .env.example        # Шаблон конфига
└── requirements.txt    # Зависимости
📝 Расширение словаря
Через файл
Отредактируйте data/words.json:

json
{
  "technology": [
    {
      "word": "algorithm",
      "translation": "алгоритм",
      "example": "This sorting algorithm is very efficient",
      "level": "B2"
    }
  ]
}
Через бота
Отправьте команду:

/add algorithm - алгоритм
Пример: This sorting algorithm is very efficient
Уровень: B2
Категория: technology
🤝 Участие в разработке
Мы приветствуем вклад в проект! Вот как вы можете помочь:

Сообщайте об ошибках через Issues

Предлагайте новые функции

Добавляйте слова в словарь

Улучшайте код через Pull Requests

Перед внесением изменений ознакомьтесь с руководством по контрибьютингу.

📜 Лицензия
Проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.

📞 Контакты
По вопросам сотрудничества:
