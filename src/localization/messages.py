import logging
from typing import Dict

from config.settings import settings

logger = logging.getLogger(__name__)


def normalize_language_code(lang_code: str | None) -> str:
    """
    Нормализует язык к поддерживаемому значению ("ru" или "en").
    При None или неизвестном языке возвращает язык по умолчанию.
    """
    if not lang_code:
        return getattr(settings, "default_language", "ru")

    code = lang_code.lower()

    if code.startswith("ru"):
        return "ru"
    if code.startswith("en"):
        return "en"

    # Если язык неизвестен — используем язык по умолчанию (обычно "ru" или "en")
    return getattr(settings, "default_language", "ru")


TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "ru": {
        # Общие / ошибки
        "no_text_message": "Нет текстового сообщения для обработки.",
        "empty_message": "Пустое сообщение не может быть обработано.",
        "message_too_long": "Сообщение слишком длинное. Максимум 4000 символов.",
        "message_has_profanity": (
            "Ваше сообщение содержит недопустимые выражения. "
            "Пожалуйста, используйте корректный язык."
        ),
        "ai_no_response": "Извините, не удалось получить ответ.",
        "error_general": (
            "Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже."
        ),
        "error_ai": (
            "Не удалось получить ответ от AI. Проверьте подключение и попробуйте снова."
        ),
        "error_rate_limit": "Слишком много запросов. Пожалуйста, подождите немного.",
        "error_invalid_input": "Некорректный ввод. Пожалуйста, проверьте ваше сообщение.",
        "unexpected_error": "Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.",

        # Команды
        "start_welcome": (
            "👋 Привет, {first_name}!\n\n"
            "Я AI ассистент, работающий на базе DeepSeek. "
            "Я могу помочь тебе с вопросами, поддержать беседу и просто пообщаться.\n\n"
            "Просто напиши мне что-нибудь, и я отвечу!\n\n"
            "Используй /help для списка доступных команд."
        ),
        "help_text": (
            "📚 *Доступные команды:*\n\n"
            "/start - Начать работу с ботом\n"
            "/help - Показать это сообщение\n"
            "/about - Информация о боте\n"
            "/reset - Сбросить контекст диалога\n\n"
            "Просто отправь мне сообщение, и я отвечу!"
        ),
        "about_text": (
            "🤖 *О боте*\n\n"
            "Я умный Telegram бот с интеграцией AI агента DeepSeek через OpenRouter.\n\n"
            "*Возможности:*\n"
            "• Естественный диалог на русском и английском\n"
            "• Сохранение контекста беседы\n"
            "• Фильтрация нецензурного контента\n"
            "• Обработка ошибок и устойчивая работа\n\n"
            "*Технологии:*\n"
            "• Python 3.11+\n"
            "• python-telegram-bot\n"
            "• DeepSeek AI (OpenRouter)\n\n"
            "Версия: 1.0.0"
        ),
        "reset_success": (
            "🔄 *Контекст диалога сброшен*\n\n"
            "Все предыдущие сообщения удалены. "
            "Можем начать новую беседу!"
        ),
        "reset_error": "Произошла ошибка при сбросе контекста. Попробуйте позже.",
    },
    "en": {
        # Common / errors
        "no_text_message": "There is no text message to process.",
        "empty_message": "An empty message cannot be processed.",
        "message_too_long": "The message is too long. Maximum is 4000 characters.",
        "message_has_profanity": (
            "Your message contains inappropriate language. "
            "Please use respectful wording."
        ),
        "ai_no_response": "Sorry, I couldn't get a response.",
        "error_general": (
            "Sorry, an error occurred while processing your request. Please try again later."
        ),
        "error_ai": (
            "Failed to get a response from the AI. Please check the connection and try again."
        ),
        "error_rate_limit": "Too many requests. Please wait a bit.",
        "error_invalid_input": "Invalid input. Please check your message.",
        "unexpected_error": "An unexpected error occurred. Please try again later.",

        # Commands
        "start_welcome": (
            "👋 Hi, {first_name}!\n\n"
            "I'm an AI assistant powered by DeepSeek. "
            "I can help you with questions, keep up a conversation, or just chat.\n\n"
            "Just send me a message and I'll reply!\n\n"
            "Use /help to see the list of available commands."
        ),
        "help_text": (
            "📚 *Available commands:*\n\n"
            "/start - Start working with the bot\n"
            "/help - Show this message\n"
            "/about - Information about the bot\n"
            "/reset - Reset conversation context\n\n"
            "Just send me a message and I'll reply!"
        ),
        "about_text": (
            "🤖 *About the bot*\n\n"
            "I'm a smart Telegram bot with a DeepSeek AI agent integrated via OpenRouter.\n\n"
            "*Capabilities:*\n"
            "• Natural conversation in Russian and English\n"
            "• Conversation context saving\n"
            "• Profanity filtering\n"
            "• Error handling and stable work\n\n"
            "*Tech stack:*\n"
            "• Python 3.11+\n"
            "• python-telegram-bot\n"
            "• DeepSeek AI (OpenRouter)\n\n"
            "Version: 1.0.0"
        ),
        "reset_success": (
            "🔄 *Conversation context has been reset*\n\n"
            "All previous messages were cleared. "
            "We can start a new conversation!"
        ),
        "reset_error": "An error occurred while resetting the context. Please try again later.",
    },
}


def t(lang: str | None, key: str, **kwargs) -> str:
    """
    Возвращает локализованную строку по ключу и языку.
    lang может быть как 'ru'/'en', так и Telegram language_code ('ru', 'ru-RU', 'en', 'en-US').
    """
    normalized = normalize_language_code(lang)
    messages = TRANSLATIONS.get(normalized) or TRANSLATIONS.get(
        getattr(settings, "default_language", "ru"), {}
    )

    text = messages.get(key)
    if text is None:
        # Пытаемся взять из английского как запасной вариант
        text = TRANSLATIONS.get("en", {}).get(key, key)
        logger.warning(
            f"Missing translation for key '{key}' in language '{normalized}'")

    try:
        return text.format(**kwargs)
    except Exception:
        # Если форматирование не удалось — возвращаем как есть
        return text
