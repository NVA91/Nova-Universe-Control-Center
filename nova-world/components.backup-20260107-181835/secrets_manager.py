"""
🔐 Secrets Manager
Zentralisiertes Secrets-Management für Nova-World
"""

import streamlit as st
from typing import Optional, Dict, Any

class SecretsManager:
    """
    Verwaltet Secrets aus Streamlit Secrets
    Fallback auf Umgebungsvariablen
    """
    
    def __init__(self):
        self.secrets = st.secrets if hasattr(st, 'secrets') else {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Holt einen Secret-Wert
        
        Args:
            key: Secret-Key (z.B. "openai.api_key" oder "openai")
            default: Default-Wert falls nicht gefunden
        
        Returns:
            Secret-Wert oder default
        """
        try:
            # Support für nested keys (z.B. "openai.api_key")
            if "." in key:
                parts = key.split(".")
                value = self.secrets
                for part in parts:
                    value = value.get(part, {})
                return value if value != {} else default
            else:
                return self.secrets.get(key, default)
        except Exception:
            return default
    
    def get_openai_key(self) -> Optional[str]:
        """Holt OpenAI API Key"""
        return self.get("openai.api_key")
    
    def get_openai_model(self) -> str:
        """Holt OpenAI Model (default: gpt-4)"""
        return self.get("openai.model", "gpt-4")
    
    def get_whisper_model(self) -> str:
        """Holt Whisper Model (default: whisper-1)"""
        return self.get("openai.whisper_model", "whisper-1")
    
    def get_semaphore_url(self) -> str:
        """Holt Semaphore URL"""
        return self.get("semaphore.url", "http://localhost:3000")
    
    def get_semaphore_token(self) -> Optional[str]:
        """Holt Semaphore API Token"""
        return self.get("semaphore.api_token")
    
    def get_semaphore_project_id(self) -> int:
        """Holt Semaphore Project ID"""
        return self.get("semaphore.project_id", 1)
    
    def get_ansible_project_path(self) -> str:
        """Holt Ansible Project Path"""
        import os
        from pathlib import Path
        default_path = str(Path(__file__).parent.parent.parent.absolute())
        return self.get("system.ansible_project_path", default_path)
    
    def is_feature_enabled(self, feature: str) -> bool:
        """
        Prüft ob Feature aktiviert ist
        
        Args:
            feature: Feature-Name (z.B. "voice_control_enabled")
        
        Returns:
            True wenn aktiviert, sonst False
        """
        return self.get(f"features.{feature}", False)
    
    def validate_secrets(self) -> Dict[str, bool]:
        """
        Validiert ob alle notwendigen Secrets vorhanden sind
        
        Returns:
            Dict mit Validation-Status
        """
        validations = {
            "openai_key": bool(self.get_openai_key()),
            "semaphore_url": bool(self.get_semaphore_url()),
        }
        return validations
    
    def get_missing_secrets(self) -> list:
        """
        Gibt Liste der fehlenden Secrets zurück
        
        Returns:
            Liste von fehlenden Secret-Namen
        """
        validations = self.validate_secrets()
        return [key for key, valid in validations.items() if not valid]


# ============================================================================
# Singleton Instance
# ============================================================================

_secrets_manager_instance = None

def get_secrets_manager() -> SecretsManager:
    """
    Gibt Singleton-Instance des SecretsManager zurück
    
    Returns:
        SecretsManager Instance
    """
    global _secrets_manager_instance
    if _secrets_manager_instance is None:
        _secrets_manager_instance = SecretsManager()
    return _secrets_manager_instance
