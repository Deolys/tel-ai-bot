import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.ai.client import AIClient
from src.ai.response_formatter import format_ai_response, get_error_message
from src.state.manager import StateManager
from src.filters.content_filter import ContentFilter
from src.bot.middleware import MessageMiddleware
from src.utils.logger import log_user_interaction, log_bot_response
from src.utils.exceptions import AIClientError, StateManagerError
from src.utils.message_splitter import split_message
from src.localization.messages import t

logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(
        self,
        ai_client: AIClient,
        state_manager: StateManager,
        content_filter: ContentFilter
    ):
        self.ai_client = ai_client
        self.state_manager = state_manager
        self.content_filter = content_filter
        self.middleware = MessageMiddleware(content_filter)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user

        user_lang = getattr(user, "language_code", None) if user else None

        is_valid, result = await self.middleware.process_message(update, context)

        if not is_valid:
            await update.message.reply_text(result)
            return

        user_message = result
        log_user_interaction(user.id, user.username or "", user_message)

        try:
            await update.message.chat.send_action("typing")

            session = await self.state_manager.get_or_create_session(
                telegram_user_id=user.id,
                username=user.username or "",
                first_name=user.first_name or "",
                language_code=user_lang,
            )

            lang = session.get("language", user_lang)

            conversation_history = await self.state_manager.get_conversation_history(
                session["id"]
            )

            ai_response = await self.ai_client.generate_response(
                messages=conversation_history,
                user_message=user_message
            )

            filtered_response = self.content_filter.filter_response(ai_response)
            formatted_response = format_ai_response(filtered_response, lang=lang)

            await self.state_manager.save_message(
                session_id=session["id"],
                role="user",
                content=user_message
            )

            await self.state_manager.save_message(
                session_id=session["id"],
                role="assistant",
                content=formatted_response
            )

            message_parts = split_message(formatted_response)
            for part in message_parts:
                await update.message.reply_text(part)
            
            log_bot_response(user.id, formatted_response)

        except AIClientError as e:
            logger.error(f"AI client error for user {user.id}: {e}")
            error_msg = get_error_message("ai_error", lang=user_lang)
            await update.message.reply_text(error_msg)

        except StateManagerError as e:
            logger.error(f"State manager error for user {user.id}: {e}")
            error_msg = get_error_message("general", lang=user_lang)
            await update.message.reply_text(error_msg)

        except Exception as e:
            logger.error(f"Unexpected error handling message for user {user.id}: {e}")
            error_msg = get_error_message("general", lang=user_lang)
            await update.message.reply_text(error_msg)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)

    if update and update.effective_message:
        user = update.effective_user
        user_lang = getattr(user, "language_code", None) if user else None
        await update.effective_message.reply_text(
            t(user_lang, "unexpected_error")
        )
