# Telegram AI Bot with DeepSeek

Telegram бот с интеграцией AI агента (DeepSeek через OpenRouter), управлением контекстом диалога и фильтрацией контента.

## Возможности

- Диалог с AI агентом (DeepSeek)
- Хранение контекста диалога в Supabase
- Базовые команды: /start, /help, /about, /reset
- Фильтрация нецензурного контента
- Обработка ошибок и логирование
- Тесты с pytest

## Установка

### Предварительные требования

1. Python 3.11+
2. Telegram Bot Token (получить через [@BotFather](https://t.me/botfather))
3. OpenRouter API ключ (получить на [openrouter.ai](https://openrouter.ai))
4. Supabase проект (для хранения контекста)

### Локальная установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate  # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Скопируйте `.env.example` в `.env` и заполните:
   ```bash
   cp .env.example .env
   ```

5. Примените миграции базы данных (автоматически при первом запуске)

6. Запустите бота:
   ```bash
   python main.py
   ```

### Docker установка

1. Скопируйте `.env.example` в `.env` и заполните
2. Запустите через Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Тестирование

Запуск всех тестов:
```bash
pytest
```

Запуск с покрытием кода:
```bash
pytest --cov=src --cov-report=html
```

## Структура проекта

```
telegram-ai-bot/
├── config/           # Конфигурация и настройки
├── src/
│   ├── bot/         # Обработчики Telegram
│   ├── ai/          # Интеграция с AI
│   ├── state/       # Управление состоянием
│   ├── filters/     # Фильтрация контента
│   └── utils/       # Утилиты
├── tests/           # Тесты
└── main.py          # Точка входа
```

## Команды бота

- `/start` - Начать диалог
- `/help` - Справка по командам
- `/about` - О боте
- `/reset` - Сбросить контекст диалога

## Лицензия

MIT
