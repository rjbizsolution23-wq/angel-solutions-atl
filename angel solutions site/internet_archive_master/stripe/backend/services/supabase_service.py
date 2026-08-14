"""
Supabase service replaced with local SQLite database for 100% local, self-contained operation.
This mirrors the original SupabaseService interface exactly to serve as a drop-in replacement.
"""
import sqlite3
import uuid
from datetime import datetime
import json
import os
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class SupabaseService:
    """Service for interacting with local SQLite database (drop-in replacement for Supabase)."""
    
    def __init__(self):
        # Resolve db path under backend/db/local_agent.db
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(current_dir)
        self.db_path = os.path.join(backend_dir, "db", "local_agent.db")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database
        self._init_db()
        logger.info(f"Local SQLite database initialized at {self.db_path}")

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    metadata TEXT,
                    created_at TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            """)
            
            # Agent actions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_actions (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    action_type TEXT,
                    stripe_object_type TEXT,
                    stripe_object_id TEXT,
                    request_params TEXT,
                    response_data TEXT,
                    error TEXT,
                    success INTEGER,
                    created_at TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
                )
            """)
            
            # Webhook events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS webhook_events (
                    id TEXT PRIMARY KEY,
                    event_id TEXT UNIQUE,
                    event_type TEXT,
                    event_data TEXT,
                    processed INTEGER DEFAULT 0,
                    processed_at TEXT,
                    created_at TEXT
                )
            """)
            
            # User preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id TEXT PRIMARY KEY,
                    user_id TEXT UNIQUE,
                    stripe_mode TEXT DEFAULT 'test',
                    auto_confirm_actions INTEGER DEFAULT 0,
                    preferences TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            conn.commit()

    # ========== CONVERSATIONS ==========
    
    def create_conversation(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new conversation."""
        conv_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (id, user_id, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (conv_id, user_id, created_at, created_at)
            )
            conn.commit()
        return {
            "id": conv_id,
            "user_id": user_id,
            "created_at": created_at,
            "updated_at": created_at
        }
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get a conversation by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
        return None

    # ========== MESSAGES ==========
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add a message to a conversation."""
        msg_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        metadata_str = json.dumps(metadata or {})
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (id, conversation_id, role, content, metadata, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (msg_id, conversation_id, role, content, metadata_str, created_at)
            )
            conn.commit()
        return {
            "id": msg_id,
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "created_at": created_at
        }
    
    def get_conversation_messages(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get messages for a conversation."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC LIMIT ?",
                (conversation_id, limit)
            )
            rows = cursor.fetchall()
            messages = []
            for r in rows:
                m = dict(r)
                try:
                    m["metadata"] = json.loads(m["metadata"]) if m.get("metadata") else {}
                except Exception:
                    m["metadata"] = {}
                messages.append(m)
            return messages

    # ========== AGENT ACTIONS ==========
    
    def log_agent_action(
        self,
        conversation_id: str,
        action_type: str,
        stripe_object_type: str,
        stripe_object_id: Optional[str] = None,
        request_params: Optional[Dict[str, Any]] = None,
        response_data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        success: bool = True
    ) -> Dict[str, Any]:
        """Log an agent action to audit trail."""
        action_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        params_str = json.dumps(request_params or {})
        resp_str = json.dumps(response_data or {})
        success_int = 1 if success else 0
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO agent_actions 
                   (id, conversation_id, action_type, stripe_object_type, stripe_object_id, request_params, response_data, error, success, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (action_id, conversation_id, action_type, stripe_object_type, stripe_object_id, params_str, resp_str, error, success_int, created_at)
            )
            conn.commit()
        return {
            "id": action_id,
            "conversation_id": conversation_id,
            "action_type": action_type,
            "stripe_object_type": stripe_object_type,
            "stripe_object_id": stripe_object_id,
            "request_params": request_params or {},
            "response_data": response_data or {},
            "error": error,
            "success": success,
            "created_at": created_at
        }
    
    def get_agent_actions(
        self,
        conversation_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get agent actions, optionally filtered by conversation."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if conversation_id:
                cursor.execute(
                    "SELECT * FROM agent_actions WHERE conversation_id = ? ORDER BY created_at DESC LIMIT ?",
                    (conversation_id, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM agent_actions ORDER BY created_at DESC LIMIT ?",
                    (limit,)
                )
            rows = cursor.fetchall()
            actions = []
            for r in rows:
                a = dict(r)
                a["success"] = bool(a["success"])
                try:
                    a["request_params"] = json.loads(a["request_params"]) if a.get("request_params") else {}
                except Exception:
                    a["request_params"] = {}
                try:
                    a["response_data"] = json.loads(a["response_data"]) if a.get("response_data") else {}
                except Exception:
                    a["response_data"] = {}
                actions.append(a)
            return actions

    # ========== WEBHOOK EVENTS ==========
    
    def store_webhook_event(
        self,
        event_id: str,
        event_type: str,
        event_data: Dict[str, Any],
        processed: bool = False
    ) -> Dict[str, Any]:
        """Store a webhook event."""
        uid = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        data_str = json.dumps(event_data)
        proc_int = 1 if processed else 0
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO webhook_events (id, event_id, event_type, event_data, processed, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (uid, event_id, event_type, data_str, proc_int, created_at)
            )
            conn.commit()
        return {
            "id": uid,
            "event_id": event_id,
            "event_type": event_type,
            "event_data": event_data,
            "processed": processed,
            "created_at": created_at
        }
    
    def mark_webhook_processed(self, event_id: str) -> None:
        """Mark a webhook event as processed."""
        processed_at = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE webhook_events SET processed = 1, processed_at = ? WHERE event_id = ?",
                (processed_at, event_id)
            )
            conn.commit()
    
    def get_recent_webhook_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent webhook events."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM webhook_events ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            events = []
            for r in rows:
                e = dict(r)
                e["processed"] = bool(e["processed"])
                try:
                    e["event_data"] = json.loads(e["event_data"]) if e.get("event_data") else {}
                except Exception:
                    e["event_data"] = {}
                events.append(e)
            return events


# Singleton instance
_supabase_service: Optional[SupabaseService] = None


def get_supabase_service() -> SupabaseService:
    """Get or create Supabase service instance."""
    global _supabase_service
    if _supabase_service is None:
        _supabase_service = SupabaseService()
    return _supabase_service
