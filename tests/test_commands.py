import pytest
from unittest.mock import AsyncMock, MagicMock
from src.bot.commands import BotCommands


@pytest.mark.asyncio
async def test_start_command(mock_state_manager, sample_user):
    commands = BotCommands(mock_state_manager)

    update = MagicMock()
    update.effective_user = sample_user
    update.effective_user.language_code = "ru"
    update.message.reply_text = AsyncMock()

    context = MagicMock()

    await commands.start_command(update, context)

    mock_state_manager.get_or_create_session.assert_called_once_with(
        telegram_user_id=sample_user.id,
        username=sample_user.username,
        first_name=sample_user.first_name,
        language_code="ru"
    )

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "Привет" in call_args
    assert sample_user.first_name in call_args


@pytest.mark.asyncio
async def test_help_command(mock_state_manager, sample_user):
    commands = BotCommands(mock_state_manager)

    update = MagicMock()
    update.effective_user = sample_user
    update.effective_user.language_code = "ru"
    update.message.reply_text = AsyncMock()

    context = MagicMock()

    mock_state_manager.get_user_language = AsyncMock(return_value="ru")

    await commands.help_command(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "/start" in call_args
    assert "/help" in call_args
    assert "/reset" in call_args


@pytest.mark.asyncio
async def test_about_command(mock_state_manager, sample_user):
    commands = BotCommands(mock_state_manager)

    update = MagicMock()
    update.effective_user = sample_user
    update.effective_user.language_code = "ru"
    update.message.reply_text = AsyncMock()

    context = MagicMock()

    mock_state_manager.get_user_language = AsyncMock(return_value="ru")

    await commands.about_command(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "О боте" in call_args
    assert "DeepSeek" in call_args


@pytest.mark.asyncio
async def test_reset_command(mock_state_manager, sample_user):
    commands = BotCommands(mock_state_manager)

    update = MagicMock()
    update.effective_user = sample_user
    update.effective_user.language_code = "ru"
    update.message.reply_text = AsyncMock()

    context = MagicMock()

    mock_state_manager.get_user_language = AsyncMock(return_value="ru")

    await commands.reset_command(update, context)

    mock_state_manager.reset_conversation.assert_called_once_with(sample_user.id)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "сброшен" in call_args
