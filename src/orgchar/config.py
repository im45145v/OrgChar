"""
Configuration module for OrgChar RAG chatbot.
"""

import os
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _strip_wrapping_quotes(value: str) -> str:
    """Strip matching wrapping quotes often copied into .env values."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1].strip()
    return value


def _get_streamlit_secret(key: str) -> Optional[Any]:
    """Fetch a secret from Streamlit, supporting flat and [orgchar] TOML layouts."""
    try:
        import streamlit as st
        secrets = st.secrets
    except Exception:
        return None

    try:
        if key in secrets:
            return secrets[key]

        namespace = secrets.get("orgchar")
        if namespace and key in namespace:
            return namespace[key]
    except Exception:
        return None

    return None


def _get_setting(key: str, default: Optional[Any] = None) -> Any:
    """Read config from Streamlit secrets first, then env, then default."""
    secret_value = _get_streamlit_secret(key)
    if secret_value is not None and str(secret_value).strip() != "":
        return _strip_wrapping_quotes(str(secret_value))

    env_value = os.getenv(key)
    if env_value is not None and str(env_value).strip() != "":
        return _strip_wrapping_quotes(str(env_value))

    return default


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

class Config:
    """Configuration class for OrgChar application."""
    
    # API Keys
    OPENAI_API_KEY = _get_setting("OPENAI_API_KEY")
    DISCORD_BOT_TOKEN = _get_setting("DISCORD_BOT_TOKEN")
    DISCORD_GUILD_ID = _get_setting("DISCORD_GUILD_ID")
    
    # Paths
    KNOWLEDGE_BASE_PATH = Path(_get_setting("KNOWLEDGE_BASE_PATH", "./knowledge_base"))
    VECTOR_DB_PATH = Path(_get_setting("VECTOR_DB_PATH", "./vector_db"))
    
    # Document processing
    CHUNK_SIZE = _to_int(_get_setting("CHUNK_SIZE", 1000), 1000)
    CHUNK_OVERLAP = _to_int(_get_setting("CHUNK_OVERLAP", 200), 200)
    
    # Model configuration
    EMBEDDING_MODEL = _get_setting("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    LLM_MODEL = _get_setting("LLM_MODEL", "gpt-4o-mini")
    TEMPERATURE = _to_float(_get_setting("TEMPERATURE", 0.3), 0.3)
    USE_LOCAL_FALLBACK = _to_bool(_get_setting("USE_LOCAL_FALLBACK", True), True)
    LOCAL_LLM_MODEL = _get_setting("LOCAL_LLM_MODEL", "google/flan-t5-base")
    LOCAL_MAX_NEW_TOKENS = _to_int(_get_setting("LOCAL_MAX_NEW_TOKENS", 512), 512)
    
    # Streamlit configuration
    STREAMLIT_PAGE_TITLE = "OrgChar - Organizational Behavior Chatbot"
    STREAMLIT_PAGE_ICON = "🏢"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        cls.KNOWLEDGE_BASE_PATH.mkdir(parents=True, exist_ok=True)
        cls.VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)