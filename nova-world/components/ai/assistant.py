"""
Unified AI Assistant
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from .ollama_backend import OllamaBackend


class AIAssistant:
    """Unified AI Assistant"""
    
    def __init__(self, mode: str = "auto"):
        self.mode = mode
        self.backend = None
        self._initialize_backend()
    
    def _initialize_backend(self):
        """Initialize backend"""
        if self.mode in ["ollama", "auto"]:
            self.backend = OllamaBackend()
            if not self.backend.is_available():
                st.warning(f"⚠️ Ollama nicht verfügbar auf {self.backend.api_url}")
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
    
    def is_available(self) -> bool:
        return self.backend is not None and self.backend.is_available()
    
    def chat(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None,
             system_info: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> str:
        if not self.backend:
            return "❌ Kein AI Backend verfügbar"
        return self.backend.chat(message, conversation_history, system_info, temperature)
    
    def get_suggestion(self, category: str, current_state: Dict[str, Any]) -> str:
        if not self.backend:
            return "❌ Kein AI Backend verfügbar"
        return self.backend.get_suggestion(category, current_state)
    
    def explain_action(self, action_name: str, action_details: Dict[str, Any]) -> str:
        if not self.backend:
            return "❌ Kein AI Backend verfügbar"
        return self.backend.explain_action(action_name, action_details)
    
    def analyze_error(self, error_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self.backend:
            return "❌ Kein AI Backend verfügbar"
        return self.backend.analyze_error(error_message, context)
    
    def generate_command(self, task_description: str) -> str:
        if not self.backend:
            return "❌ Kein AI Backend verfügbar"
        return self.backend.generate_command(task_description)
    
    def get_backend_name(self) -> str:
        return self.backend.get_backend_name() if self.backend else "none"
    
    def get_info(self) -> Dict[str, Any]:
        if not self.backend:
            return {'available': False, 'backend': 'none', 'mode': self.mode}
        info = self.backend.get_info()
        info['mode'] = self.mode
        return info
