def format_ai_response(response: str) -> str:
    """
    Форматирует ответ от AI.
    Примечание: разбиение длинных сообщений происходит в handlers.py с помощью split_message()
    """
    if not response:
        return "Извините, не удалось получить ответ."

    response = response.strip()

    return response


def get_error_message(error_type: str = "general") -> str:
    error_messages = {
        "general": "Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже.",
        "ai_error": "Не удалось получить ответ от AI. Проверьте подключение и попробуйте снова.",
        "rate_limit": "Слишком много запросов. Пожалуйста, подождите немного.",
        "invalid_input": "Некорректный ввод. Пожалуйста, проверьте ваше сообщение."
    }
    return error_messages.get(error_type, error_messages["general"])
