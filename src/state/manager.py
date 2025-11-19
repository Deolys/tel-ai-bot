import logging
from typing import List, Dict, Optional
from supabase import create_client, Client
from config.settings import settings
from src.utils.exceptions import StateManagerError

logger = logging.getLogger(__name__)


class StateManager:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        self.max_context_messages = settings.max_context_messages

    async def get_or_create_session(
        self,
        telegram_user_id: int,
        username: str = "",
        first_name: str = ""
    ) -> Dict:
        try:
            response = self.supabase.table("user_sessions").select("*").eq(
                "telegram_user_id", telegram_user_id
            ).maybe_single().execute()

            if response.data:
                logger.info(f"Found existing session for user {telegram_user_id}")
                return response.data

            new_session = self.supabase.table("user_sessions").insert({
                "telegram_user_id": telegram_user_id,
                "username": username,
                "first_name": first_name,
                "conversation_context": {}
            }).execute()

            logger.info(f"Created new session for user {telegram_user_id}")
            return new_session.data[0]

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
            self.supabase.table("chat_messages").insert({
                "session_id": session_id,
                "role": role,
                "content": content
            }).execute()

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

            response = self.supabase.table("chat_messages").select(
                "role, content"
            ).eq(
                "session_id", session_id
            ).order(
                "created_at", desc=True
            ).limit(limit).execute()

            messages = list(reversed(response.data))

            logger.debug(f"Retrieved {len(messages)} messages for session {session_id}")
            return messages

        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            raise StateManagerError(f"Failed to get history: {str(e)}")

    async def reset_conversation(self, telegram_user_id: int):
        try:
            session_response = self.supabase.table("user_sessions").select("id").eq(
                "telegram_user_id", telegram_user_id
            ).maybe_single().execute()

            if not session_response.data:
                logger.warning(f"No session found for user {telegram_user_id}")
                return

            session_id = session_response.data["id"]

            self.supabase.table("chat_messages").delete().eq(
                "session_id", session_id
            ).execute()

            self.supabase.table("user_sessions").update({
                "conversation_context": {}
            }).eq("id", session_id).execute()

            logger.info(f"Reset conversation for user {telegram_user_id}")

        except Exception as e:
            logger.error(f"Error resetting conversation: {e}")
            raise StateManagerError(f"Failed to reset conversation: {str(e)}")

    async def update_session_context(
        self,
        session_id: str,
        context: Dict
    ):
        try:
            self.supabase.table("user_sessions").update({
                "conversation_context": context
            }).eq("id", session_id).execute()

            logger.debug(f"Updated context for session {session_id}")

        except Exception as e:
            logger.error(f"Error updating session context: {e}")
            raise StateManagerError(f"Failed to update context: {str(e)}")
