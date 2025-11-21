import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from config.settings import settings
from config.logging_config import setup_logging
from src.ai.client import AIClient
from src.state.manager import StateManager
from src.filters.content_filter import ContentFilter
from src.bot.commands import BotCommands
from src.bot.handlers import MessageHandler as BotMessageHandler
from src.bot.handlers import error_handler

logger = setup_logging()


async def post_init(application: Application):
    await application.bot.set_my_commands([
        ("start", "Начать работу с ботом"),
        ("help", "Показать справку"),
        ("about", "Информация о боте"),
        ("reset", "Сбросить контекст диалога"),
    ])
    logger.info("Bot commands set successfully")


def main():
    logger.info("Starting Telegram AI Bot...")

    if not settings.telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set")
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    if not settings.openrouter_api_key:
        logger.error("OPENROUTER_API_KEY is not set")
        raise ValueError("OPENROUTER_API_KEY is required")

    ai_client = AIClient()
    state_manager = StateManager()
    content_filter = ContentFilter()

    bot_commands = BotCommands(state_manager)
    message_handler = BotMessageHandler(ai_client, state_manager, content_filter)

    application = Application.builder().token(settings.telegram_bot_token).post_init(post_init).build()

    application.add_handler(CommandHandler("start", bot_commands.start_command))
    application.add_handler(CommandHandler("help", bot_commands.help_command))
    application.add_handler(CommandHandler("about", bot_commands.about_command))
    application.add_handler(CommandHandler("reset", bot_commands.reset_command))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler.start_handle_message)
    )

    application.add_error_handler(error_handler)

    logger.info("Bot handlers registered successfully")
    logger.info(f"Using AI model: {settings.ai_model}")
    logger.info("Bot is running... Press Ctrl+C to stop")

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        raise
