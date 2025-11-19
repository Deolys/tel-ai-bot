import logging
from better_profanity import profanity
from src.filters.stopwords import ALL_STOPWORDS
from src.utils.exceptions import ContentFilterError

logger = logging.getLogger(__name__)

profanity.load_censor_words()
profanity.add_censor_words(ALL_STOPWORDS)


class ContentFilter:
    def __init__(self):
        self.enabled = True

    def contains_profanity(self, text: str) -> bool:
        try:
            return profanity.contains_profanity(text)
        except Exception as e:
            logger.error(f"Error checking profanity: {e}")
            return False

    def censor_text(self, text: str) -> str:
        try:
            return profanity.censor(text)
        except Exception as e:
            logger.error(f"Error censoring text: {e}")
            return text

    def validate_message(self, text: str) -> tuple[bool, str]:
        if not text or len(text.strip()) == 0:
            return False, "Пустое сообщение не может быть обработано."

        if len(text) > 4000:
            return False, "Сообщение слишком длинное. Максимум 4000 символов."

        if self.contains_profanity(text):
            logger.warning("Profanity detected in message")
            return False, "Ваше сообщение содержит недопустимые выражения. Пожалуйста, используйте корректный язык."

        return True, ""

    def filter_response(self, text: str) -> str:
        if self.contains_profanity(text):
            logger.warning("Profanity detected in AI response, censoring")
            return self.censor_text(text)
        return text
