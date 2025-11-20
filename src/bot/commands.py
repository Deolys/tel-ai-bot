import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.state.manager import StateManager
from src.utils.logger import log_user_interaction

logger = logging.getLogger(__name__)


class BotCommands:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        log_user_interaction(user.id, user.username or "", "/start")

        await self.state_manager.get_or_create_session(
            telegram_user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or ""
        )

        welcome_message = (
            f"👋 Привет, {user.first_name}!\n\n"
            "Я AI ассистент, работающий на базе DeepSeek. "
            "Я могу помочь тебе с вопросами, поддержать беседу и просто пообщаться.\n\n"
            "Просто напиши мне что-нибудь, и я отвечу!\n\n"
            "Используй /help для списка доступных команд."
        )

        await update.message.reply_text(welcome_message)
        logger.info(f"User {user.id} started the bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        log_user_interaction(user.id, user.username or "", "/help")

        help_text = (
            "📚 *Доступные команды:*\n\n"
            "/start - Начать работу с ботом\n"
            "/help - Показать это сообщение\n"
            "/about - Информация о боте\n"
            "/reset - Сбросить контекст диалога\n\n"
            "Просто отправь мне сообщение, и я отвечу!"
        )

        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        log_user_interaction(user.id, user.username or "", "/about")

        about_text = (
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
            "• DeepSeek AI (OpenRouter)\n"
            "Версия: 1.0.0"
        )

        await update.message.reply_text(about_text, parse_mode="Markdown")

    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        log_user_interaction(user.id, user.username or "", "/reset")

        try:
            await self.state_manager.reset_conversation(user.id)

            reset_message = (
                "🔄 *Контекст диалога сброшен*\n\n"
                "Все предыдущие сообщения удалены. "
                "Можем начать новую беседу!"
            )

            await update.message.reply_text(reset_message, parse_mode="Markdown")
            logger.info(f"User {user.id} reset conversation")

        except Exception as e:
            logger.error(f"Error resetting conversation for user {user.id}: {e}")
            await update.message.reply_text(
                "Произошла ошибка при сбросе контекста. Попробуйте позже."
            )
