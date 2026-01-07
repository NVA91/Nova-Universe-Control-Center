"""
AI Assistant - Ollama Integration
Local AI Assistant for Infrastructure Management
"""

import streamlit as st
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class AIAssistantOllama:
    """AI Assistant powered by Ollama"""
    
    def __init__(self):
        """Initialize Ollama AI Assistant"""
        ollama_config = st.secrets.get("ollama", {})
        self.enabled = ollama_config.get("enabled", False)
        self.api_url = ollama_config.get("api_url", "http://localhost:11434")
        self.model = ollama_config.get("model", "llama3:8b")
        self.temperature = ollama_config.get("temperature", 0.7)
        
        self.system_context = "Du bist Nova, ein KI-Assistent für Infrastructure Management. Antworte auf Deutsch, präzise und hilfreich."
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        if not self.enabled:
            return False
        try:
            response = requests.get(f"{self.api_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def chat(self, message: str, conversation_history: Optional[List[Dict]] = None, system_info: Optional[Dict] = None) -> Dict[str, Any]:
        """Chat with AI Assistant"""
        if not self.is_available():
            return {"success": False, "message": "❌ Ollama nicht verfügbar"}
        
        try:
            context = self._build_context(system_info)
            messages = [{"role": "system", "content": self.system_context + context}]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": message})
            
            response = requests.post(
                f"{self.api_url}/api/chat",
                json={"model": self.model, "messages": messages, "stream": False, "options": {"temperature": self.temperature}},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {"success": True, "message": data.get("message", {}).get("content", ""), "model": self.model, "timestamp": datetime.now().isoformat()}
            else:
                return {"success": False, "message": f"❌ API Error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "message": f"❌ Fehler: {str(e)}"}
    
    def _build_context(self, system_info: Optional[Dict] = None) -> str:
        """Build system context"""
        if not system_info:
            return ""
        parts = []
        if "cpu" in system_info:
            parts.append(f"CPU: {system_info['cpu']}%")
        if "memory" in system_info:
            parts.append(f"RAM: {system_info['memory']}%")
        if "disk" in system_info:
            parts.append(f"Disk: {system_info['disk']}%")
        return "\n\nSystem-Status:\n" + "\n".join(parts) if parts else ""
    
    def get_suggestion(self, category: str, current_state: Optional[Dict] = None) -> Dict[str, Any]:
        """Get intelligent suggestion"""
        prompts = {
            "docker": "Analysiere den Docker-Status und gib eine Empfehlung.",
            "deployment": "Welches Deployment-Profil empfiehlst du?",
            "system": "Analysiere die System-Metriken und gib Optimierungs-Vorschläge.",
            "backup": "Wann sollte das nächste Backup durchgeführt werden?"
        }
        return self.chat(prompts.get(category, "Gib eine Empfehlung."), system_info=current_state)
    
    def explain_action(self, action_name: str) -> Dict[str, Any]:
        """Explain what a Quick Action does"""
        return self.chat(f"Erkläre kurz was die Quick Action '{action_name}' macht.")

def get_ai_assistant() -> AIAssistantOllama:
    """Get AI Assistant instance"""
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistantOllama()
    return st.session_state.ai_assistant
