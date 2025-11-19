import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.filters.content_filter import ContentFilter

logger = logging.getLogger(__name__)


class MessageMiddleware:
    def __init__(self, content_filter: ContentFilter):
        self.content_filter = content_filter

    async def process_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> tuple[bool, str]:
        if not update.message or not update.message.text:
            return False, "Нет текстового сообщения для обработки."

        text = update.message.text

        is_valid, error_message = self.content_filter.validate_message(text)

        if not is_valid:
            logger.warning(
                f"Message validation failed for user {update.effective_user.id}: {error_message}"
            )
            return False, error_message

        return True, text
