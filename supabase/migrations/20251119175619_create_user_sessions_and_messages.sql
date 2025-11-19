/*
  # Telegram Bot User Sessions and Messages Schema

  1. New Tables
    - `user_sessions`
      - `id` (uuid, primary key) - Unique session identifier
      - `telegram_user_id` (bigint, unique) - Telegram user ID
      - `username` (text) - Telegram username
      - `first_name` (text) - User's first name
      - `conversation_context` (jsonb) - Stored conversation context
      - `created_at` (timestamptz) - Session creation time
      - `updated_at` (timestamptz) - Last update time
      
    - `chat_messages`
      - `id` (uuid, primary key) - Unique message identifier
      - `session_id` (uuid, foreign key) - Reference to user_sessions
      - `role` (text) - Message role (user/assistant)
      - `content` (text) - Message content
      - `created_at` (timestamptz) - Message creation time
      
  2. Security
    - Enable RLS on both tables
    - Add policies for authenticated bot service access
    - Add indexes for performance optimization
    
  3. Important Notes
    - Messages are linked to sessions via foreign key
    - Automatic timestamp updates via triggers
    - JSONB for flexible context storage
*/

CREATE TABLE IF NOT EXISTS user_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  telegram_user_id bigint UNIQUE NOT NULL,
  username text DEFAULT '',
  first_name text DEFAULT '',
  conversation_context jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chat_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id uuid NOT NULL REFERENCES user_sessions(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('user', 'assistant')),
  content text NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_user_sessions_telegram_id ON user_sessions(telegram_user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at DESC);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname = 'update_user_sessions_updated_at'
  ) THEN
    CREATE TRIGGER update_user_sessions_updated_at
      BEFORE UPDATE ON user_sessions
      FOR EACH ROW
      EXECUTE FUNCTION update_updated_at_column();
  END IF;
END $$;

ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role can manage user sessions"
  ON user_sessions
  FOR ALL
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Service role can manage chat messages"
  ON chat_messages
  FOR ALL
  TO authenticated
  USING (true)
  WITH CHECK (true);
