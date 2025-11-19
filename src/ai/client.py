import logging
import httpx
from typing import List, Dict
from config.settings import settings
from src.ai.prompts import format_conversation_history
from src.utils.exceptions import AIClientError

logger = logging.getLogger(__name__)


class AIClient:
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.model = settings.ai_model
        self.max_tokens = settings.ai_max_tokens
        self.temperature = settings.ai_temperature
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        user_message: str
    ) -> str:
        try:
            messages.append({"role": "user", "content": user_message})

            formatted_messages = format_conversation_history(messages)

            logger.info(f"Sending request to AI model: {self.model}")

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": formatted_messages,
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature,
                    }
                )

                response.raise_for_status()
                data = response.json()

                if "choices" not in data or len(data["choices"]) == 0:
                    raise AIClientError("No response from AI model")

                ai_response = data["choices"][0]["message"]["content"]
                logger.info("Successfully received AI response")

                return ai_response

        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {e}")
            raise AIClientError("Request timeout. Please try again.")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 429:
                raise AIClientError("Rate limit exceeded. Please wait.")
            raise AIClientError(f"AI service error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Unexpected error in AI client: {e}")
            raise AIClientError(f"Failed to generate response: {str(e)}")
