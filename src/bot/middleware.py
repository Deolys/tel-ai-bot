import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.filters.content_filter import ContentFilter
from src.localization.messages import t

logger = logging.getLogger(__name__)


class MessageMiddleware:
    def __init__(self, content_filter: ContentFilter):
        self.content_filter = content_filter

    async def process_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> tuple[bool, str]:
        user = update.effective_user
        user_lang = getattr(user, "language_code", None) if user else None

        if not update.message or not update.message.text:
            return False, t(user_lang, "no_text_message")

        text = update.message.text

        is_valid, error_message = self.content_filter.validate_message(text, lang=user_lang)

        if not is_valid:
            logger.warning(
                f"Message validation failed for user {update.effective_user.id}: {error_message}"
            )
            return False, error_message

        return True, text
