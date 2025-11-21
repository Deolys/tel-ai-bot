import logging
from typing import List, Dict, Optional
from datetime import datetime
from config.settings import settings
from src.utils.exceptions import StateManagerError
from src.localization.messages import normalize_language_code

logger = logging.getLogger(__name__)


class StateManager:
    def __init__(self):
        self.sessions: Dict[int, Dict] = {}
        self.messages: Dict[str, List[Dict]] = {}
        self.max_context_messages = settings.max_context_messages
        logger.info("StateManager initialized with in-memory storage")

    async def get_or_create_session(
        self,
        telegram_user_id: int,
        username: str = "",
        first_name: str = "",
        language_code: Optional[str] = None,
    ) -> Dict:
        try:
            if telegram_user_id in self.sessions:
                session = self.sessions[telegram_user_id]

                # Обновляем язык, если он изменился
                if language_code:
                    normalized_lang = normalize_language_code(language_code)
                    if session.get("language") != normalized_lang:
                        session["language"] = normalized_lang
                        logger.info(
                            f"Updated language for user {telegram_user_id} to {normalized_lang}"
                        )

                logger.info(f"Found existing session for user {telegram_user_id}")
                return session

            session_id = f"session_{telegram_user_id}_{datetime.now().timestamp()}"
            normalized_lang = normalize_language_code(language_code)
            new_session = {
                "id": session_id,
                "telegram_user_id": telegram_user_id,
                "username": username,
                "first_name": first_name,
                 "language": normalized_lang,
                "conversation_context": {},
                "created_at": datetime.now().isoformat()
            }

            self.sessions[telegram_user_id] = new_session
            self.messages[session_id] = []

            logger.info(f"Created new session for user {telegram_user_id}")
            return new_session

        except Exception as e:
            logger.error(f"Error getting/creating session: {e}")
            raise StateManagerError(f"Failed to manage session: {str(e)}")

    async def save_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):
        try:
            if session_id not in self.messages:
                self.messages[session_id] = []

            message = {
                "role": role,
                "content": content,
                "created_at": datetime.now().isoformat()
            }

            self.messages[session_id].append(message)
            logger.debug(f"Saved message for session {session_id}")

        except Exception as e:
            logger.error(f"Error saving message: {e}")
            raise StateManagerError(f"Failed to save message: {str(e)}")

    async def get_conversation_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, str]]:
        try:
            if limit is None:
                limit = self.max_context_messages

            if session_id not in self.messages:
                return []
            
            all_messages = self.messages[session_id]
            
            messages = all_messages[-limit:] if limit else all_messages
            
            result = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

            logger.debug(f"Retrieved {len(result)} messages for session {session_id}")
            return result

        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            raise StateManagerError(f"Failed to get history: {str(e)}")

    async def reset_conversation(self, telegram_user_id: int):
        try:
            if telegram_user_id not in self.sessions:
                logger.warning(f"No session found for user {telegram_user_id}")
                return

            session_id = self.sessions[telegram_user_id]["id"]
            
            if session_id in self.messages:
                self.messages[session_id] = []
            
            self.sessions[telegram_user_id]["conversation_context"] = {}

            logger.info(f"Reset conversation for user {telegram_user_id}")

        except Exception as e:
            logger.error(f"Error resetting conversation: {e}")
            raise StateManagerError(f"Failed to reset conversation: {str(e)}")

    async def get_user_language(self, telegram_user_id: int) -> str:
        """
        Возвращает язык пользователя из сессии или язык по умолчанию.
        """
        try:
            session = self.sessions.get(telegram_user_id)
            if session and "language" in session:
                return session["language"]

            return settings.default_language

        except Exception as e:
            logger.error(f"Error getting user language: {e}")
            return settings.default_language

    async def update_session_context(
        self,
        session_id: str,
        context: Dict
    ):
        try:
            for user_id, session in self.sessions.items():
                if session["id"] == session_id:
                    session["conversation_context"] = context
                    logger.debug(f"Updated context for session {session_id}")
                    return
            
            logger.warning(f"Session {session_id} not found for context update")

        except Exception as e:
            logger.error(f"Error updating session context: {e}")
            raise StateManagerError(f"Failed to update context: {str(e)}")
