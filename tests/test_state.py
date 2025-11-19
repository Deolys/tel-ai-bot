import pytest
from unittest.mock import MagicMock, patch
from src.state.manager import StateManager


@pytest.fixture
def mock_supabase_client():
    with patch("src.state.manager.create_client") as mock_create:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        yield mock_client


def test_state_manager_initialization(mock_supabase_client):
    manager = StateManager()

    assert manager.supabase is not None
    assert manager.max_context_messages > 0


@pytest.mark.asyncio
async def test_get_or_create_session_existing(mock_supabase_client):
    manager = StateManager()

    existing_session = {
        "id": "test-id",
        "telegram_user_id": 12345,
        "username": "testuser",
        "first_name": "Test"
    }

    mock_response = MagicMock()
    mock_response.data = existing_session
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = mock_response

    result = await manager.get_or_create_session(12345, "testuser", "Test")

    assert result == existing_session


@pytest.mark.asyncio
async def test_save_message(mock_supabase_client):
    manager = StateManager()

    mock_response = MagicMock()
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = mock_response

    await manager.save_message("session-id", "user", "Test message")

    mock_supabase_client.table.assert_called()
