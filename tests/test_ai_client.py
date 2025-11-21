import pytest
from unittest.mock import AsyncMock, patch, Mock
from src.ai.client import AIClient
from src.utils.exceptions import AIClientError


@pytest.mark.asyncio
async def test_ai_client_successful_response():
    client = AIClient()

    mock_response = AsyncMock()
    mock_response.json = Mock(return_value={
        "choices": [
            {
                "message": {
                    "content": "This is a test response"
                }
            }
        ]
    })
    mock_response.raise_for_status = Mock()

    with patch("httpx.AsyncClient") as mock_http_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_http_client.return_value = mock_client_instance

        response = await client.generate_response(
            messages=[],
            user_message="Test question"
        )

        assert response == "This is a test response"
        mock_client_instance.post.assert_called_once()


@pytest.mark.asyncio
async def test_ai_client_empty_response():
    client = AIClient()

    mock_response = AsyncMock()
    mock_response.json = Mock(return_value={"choices": []})
    mock_response.raise_for_status = Mock()

    with patch("httpx.AsyncClient") as mock_http_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_http_client.return_value = mock_client_instance

        with pytest.raises(AIClientError, match="No response from AI model"):
            await client.generate_response(
                messages=[],
                user_message="Test question"
            )
