"""
Base Backend Class für AI Assistant V2
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseAIBackend(ABC):
    """Abstrakte Basis-Klasse für AI Backends"""
    
    def __init__(self):
        self.backend_name = "base"
        self.is_available_cached = None
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if backend is available"""
        pass
    
    @abstractmethod
    def chat(
        self, 
        message: str, 
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_info: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7
    ) -> str:
        """Send chat message and get response"""
        pass
    
    def get_suggestion(self, category: str, current_state: Dict[str, Any]) -> str:
        """Get intelligent suggestion"""
        prompt = self._build_suggestion_prompt(category, current_state)
        return self.chat(prompt, temperature=0.5)
    
    def explain_action(self, action_name: str, action_details: Dict[str, Any]) -> str:
        """Explain what an action does"""
        prompt = f"Erkläre diese Aktion: {action_name}\nDetails: {action_details}"
        return self.chat(prompt, temperature=0.3)
    
    def analyze_error(self, error_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Analyze error and suggest fix"""
        prompt = f"Analysiere diesen Fehler:\n{error_message}\nKontext: {context}"
        return self.chat(prompt, temperature=0.4)
    
    def generate_command(self, task_description: str) -> str:
        """Generate command for task"""
        prompt = f"Generiere einen Befehl für: {task_description}"
        return self.chat(prompt, temperature=0.3)
    
    def _build_suggestion_prompt(self, category: str, current_state: Dict[str, Any]) -> str:
        """Build prompt for suggestions"""
        prompts = {
            'docker': f"Docker-Status: {current_state}. Was empfiehlst du?",
            'deployment': f"Deployment-Status: {current_state}. Welches Profil?",
            'system': f"System-Status: {current_state}. Was prüfen?",
            'backup': f"Backup-Status: {current_state}. Was tun?"
        }
        return prompts.get(category, f"Tipp für: {category}")
    
    def get_backend_name(self) -> str:
        return self.backend_name
    
    def get_info(self) -> Dict[str, Any]:
        return {
            'name': self.backend_name,
            'available': self.is_available(),
            'type': self.__class__.__name__
        }
