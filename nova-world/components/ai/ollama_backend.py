"""
Ollama Backend für AI Assistant V2
"""

import requests
import streamlit as st
from typing import Dict, List, Any, Optional
from .base_backend import BaseAIBackend


class OllamaBackend(BaseAIBackend):
    """Ollama Backend (Self-hosted LLM)"""
    
    def __init__(self, api_url: str = "http://localhost:11434", model: str = "llama3:8b", timeout: int = 30):
        super().__init__()
        self.backend_name = "ollama"
        self.api_url = api_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        
        # Load from secrets
        try:
            ollama_config = st.secrets.get("ollama", {})
            if ollama_config.get("enabled", True):
                self.api_url = ollama_config.get("api_url", self.api_url).rstrip('/')
                self.model = ollama_config.get("model", self.model)
        except:
            pass
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        if self.is_available_cached is not None:
            return self.is_available_cached
        
        try:
            response = requests.get(f"{self.api_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                model_names = [m.get('name', '') for m in models]
                is_available = any(self.model in name for name in model_names)
                self.is_available_cached = is_available
                return is_available
            return False
        except:
            self.is_available_cached = False
            return False
    
    def chat(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None,
             system_info: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> str:
        """Send chat message"""
        try:
            system_context = self._build_system_context(system_info)
            messages = []
            
            if system_context:
                messages.append({"role": "system", "content": system_context})
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": message})
            
            response = requests.post(
                f"{self.api_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": temperature}
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get('message', {}).get('content', 'Keine Antwort.')
            return f"Fehler: API returned {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "⏱️ Timeout: Ollama antwortet nicht."
        except requests.exceptions.ConnectionError:
            return f"🔌 Verbindungsfehler: {self.api_url}"
        except Exception as e:
            return f"❌ Fehler: {str(e)}"
    
    def _build_system_context(self, system_info: Optional[Dict[str, Any]] = None) -> str:
        """Build system context"""
        context = [
            "Du bist Nova, der AI-Assistent für Nova-World.",
            "Antworte auf Deutsch, präzise und hilfreich."
        ]
        
        if system_info:
            context.append("\n📊 System-Status:")
            if 'cpu' in system_info:
                context.append(f"- CPU: {system_info['cpu']}")
            if 'memory' in system_info:
                context.append(f"- Memory: {system_info['memory']}")
            if 'disk' in system_info:
                context.append(f"- Disk: {system_info['disk']}")
        
        return "\n".join(context)
    
    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({'api_url': self.api_url, 'model': self.model})
        return info
