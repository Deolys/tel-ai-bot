import logging
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)


def log_async_errors(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper


def log_user_interaction(user_id: int, username: str, message: str):
    logger.info(f"User {user_id} (@{username}): {message[:100]}")


def log_bot_response(user_id: int, response: str):
    logger.info(f"Bot response to {user_id}: {response[:100]}")
