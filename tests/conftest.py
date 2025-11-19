import pytest
from unittest.mock import AsyncMock, MagicMock
from src.ai.client import AIClient
from src.state.manager import StateManager
from src.filters.content_filter import ContentFilter


@pytest.fixture
def mock_ai_client():
    client = AsyncMock(spec=AIClient)
    client.generate_response = AsyncMock(return_value="Test AI response")
    return client


@pytest.fixture
def mock_state_manager():
    manager = AsyncMock(spec=StateManager)
    manager.get_or_create_session = AsyncMock(return_value={
        "id": "test-session-id",
        "telegram_user_id": 12345,
        "username": "testuser",
        "first_name": "Test",
        "conversation_context": {},
    })
    manager.get_conversation_history = AsyncMock(return_value=[])
    manager.save_message = AsyncMock()
    manager.reset_conversation = AsyncMock()
    return manager


@pytest.fixture
def content_filter():
    return ContentFilter()


@pytest.fixture
def sample_user():
    user = MagicMock()
    user.id = 12345
    user.username = "testuser"
    user.first_name = "Test"
    return user


@pytest.fixture
def sample_message():
    message = MagicMock()
    message.text = "Hello, bot!"
    return message
