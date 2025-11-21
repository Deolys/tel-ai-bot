from src.localization.messages import t


def format_ai_response(response: str, lang: str | None = None) -> str:
    """
    Форматирует ответ от AI.
    Примечание: разбиение длинных сообщений происходит в handlers.py с помощью split_message()
    """
    if not response:
        return t(lang, "ai_no_response")

    response = response.strip()

    return response


def get_error_message(error_type: str = "general", lang: str | None = None) -> str:
    key_map = {
        "general": "error_general",
        "ai_error": "error_ai",
        "rate_limit": "error_rate_limit",
        "invalid_input": "error_invalid_input",
    }
    key = key_map.get(error_type, "error_general")
    return t(lang, key)
