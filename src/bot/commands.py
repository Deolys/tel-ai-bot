import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.state.manager import StateManager
from src.utils.logger import log_user_interaction
from src.localization.messages import t

logger = logging.getLogger(__name__)


class BotCommands:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_lang = getattr(user, "language_code", None)
        log_user_interaction(user.id, user.username or "", "/start")

        session = await self.state_manager.get_or_create_session(
            telegram_user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            language_code=user_lang,
        )

        lang = session.get("language", user_lang)

        welcome_message = t(lang, "start_welcome",
                            first_name=user.first_name or "")

        await update.message.reply_text(welcome_message)
        logger.info(f"User {user.id} started the bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_lang = getattr(user, "language_code", None)
        log_user_interaction(user.id, user.username or "", "/help")

        lang = await self.state_manager.get_user_language(user.id) or user_lang

        help_text = t(lang, "help_text")

        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_lang = getattr(user, "language_code", None)
        log_user_interaction(user.id, user.username or "", "/about")

        lang = await self.state_manager.get_user_language(user.id) or user_lang

        about_text = t(lang, "about_text")

        await update.message.reply_text(about_text, parse_mode="Markdown")

    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_lang = getattr(user, "language_code", None)
        log_user_interaction(user.id, user.username or "", "/reset")

        try:
            await self.state_manager.reset_conversation(user.id)

            lang = await self.state_manager.get_user_language(user.id) or user_lang
            reset_message = t(lang, "reset_success")

            await update.message.reply_text(reset_message, parse_mode="Markdown")
            logger.info(f"User {user.id} reset conversation")

        except Exception as e:
            logger.error(
                f"Error resetting conversation for user {user.id}: {e}")
            lang = await self.state_manager.get_user_language(user.id) or user_lang
            await update.message.reply_text(t(lang, "reset_error"))
