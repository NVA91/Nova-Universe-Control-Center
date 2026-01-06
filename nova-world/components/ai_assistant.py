"""
🤖 Nova's AI Assistant
Context-Aware AI Chat für DevOps
"""

import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime
from components.secrets_manager import get_secrets_manager
from components.quick_actions import get_quick_actions

class AIAssistant:
    """
    AI Assistant mit Context-Awareness
    Nutzt OpenAI GPT-4 für intelligente Konversationen
    """
    
    def __init__(self):
        secrets = get_secrets_manager()
        self.api_key = secrets.get_openai_key()
        self.model = secrets.get_openai_model()
        
        if not self.api_key:
            raise ValueError("OpenAI API Key fehlt in secrets.toml!")
        
        self.qa = get_quick_actions()
        
        # System Prompt
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """
        Baut System Prompt mit Context
        
        Returns:
            System Prompt String
        """
        return """Du bist Nova, ein KI-Assistent für das Nova-World DevOps Dashboard.

**Deine Rolle:**
- Hilf dem Benutzer bei der Verwaltung von Docker-Containern, Ansible-Deployments und System-Monitoring
- Erkläre Fehler und gib Lösungsvorschläge
- Schlage Quick Actions vor, wenn passend
- Sei präzise, hilfsbereit und professionell

**Verfügbare Quick Actions:**
🐳 Docker:
- docker_start_all - Startet alle gestoppten Container
- docker_stop_all - Stoppt alle Container (GEFÄHRLICH!)
- docker_restart_all - Neustart aller Container
- docker_cleanup - Docker aufräumen
- docker_status - Container-Status prüfen

🚀 Deployments:
- deploy_minimal - Minimal Profile deployen
- deploy_standard - Standard Profile deployen
- deploy_full - Full Profile deployen
- semaphore_status - Deployment-Status prüfen

💻 System:
- health_check - System-Status prüfen
- uptime - System-Laufzeit
- recent_errors - Fehler in Logs suchen

🎯 Composite:
- morning_routine - Startup-Routine (Start Container + Health Check)
- emergency_stop - Notfall-Stop (Stoppt alles)

**Wenn du eine Quick Action vorschlägst:**
Formatiere sie so: `[ACTION: action_name]`
Beispiel: "Ich empfehle dir: [ACTION: health_check]"

**Wichtig:**
- Sei kurz und präzise
- Nutze Emojis sparsam
- Gib konkrete Lösungen
- Frage nach, wenn unklar
"""
    
    def chat(
        self,
        user_message: str,
        chat_history: Optional[List[Dict]] = None,
        system_context: Optional[Dict] = None
    ) -> str:
        """
        Chat mit AI Assistant
        
        Args:
            user_message: Benutzer-Nachricht
            chat_history: Bisherige Chat-History
            system_context: System-Context (CPU, RAM, Docker-Status, etc.)
        
        Returns:
            AI-Antwort
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # Build messages
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add system context if provided
            if system_context:
                context_str = self._format_system_context(system_context)
                messages.append({
                    "role": "system",
                    "content": f"**Aktueller System-Status:**\n{context_str}"
                })
            
            # Add chat history
            if chat_history:
                messages.extend(chat_history)
            
            # Add user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"❌ Fehler beim Chat: {e}"
    
    def _format_system_context(self, context: Dict) -> str:
        """
        Formatiert System-Context für AI
        
        Args:
            context: System-Context Dict
        
        Returns:
            Formatierter Context String
        """
        parts = []
        
        if "cpu" in context:
            parts.append(f"CPU: {context['cpu']}%")
        
        if "ram" in context:
            parts.append(f"RAM: {context['ram']}%")
        
        if "disk" in context:
            parts.append(f"Disk: {context['disk']}%")
        
        if "docker" in context:
            docker = context["docker"]
            parts.append(f"Docker: {docker.get('running', 0)}/{docker.get('total', 0)} Container laufen")
        
        if "semaphore" in context:
            parts.append(f"Semaphore: {context['semaphore']}")
        
        return "\n".join(parts)
    
    def get_system_context(self) -> Dict:
        """
        Holt aktuellen System-Context
        
        Returns:
            System-Context Dict
        """
        try:
            import psutil
            
            # System Metrics
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Docker Status
            docker_status = self.qa.docker_status_check()
            
            # Semaphore Status
            semaphore_status = self.qa.semaphore_status()
            
            return {
                "cpu": cpu,
                "ram": mem.percent,
                "disk": disk.percent,
                "docker": {
                    "running": docker_status.get("running", 0),
                    "total": docker_status.get("total", 0),
                    "stopped": docker_status.get("stopped", 0)
                },
                "semaphore": semaphore_status.get("status", "unknown")
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    def extract_action_suggestions(self, ai_response: str) -> List[str]:
        """
        Extrahiert Action-Vorschläge aus AI-Antwort
        
        Args:
            ai_response: AI-Antwort
        
        Returns:
            Liste von Action-Namen
        """
        import re
        
        # Find [ACTION: action_name] patterns
        pattern = r'\[ACTION:\s*(\w+)\]'
        matches = re.findall(pattern, ai_response)
        
        return matches


# ============================================================================
# Singleton Instance
# ============================================================================

_ai_assistant_instance = None

def get_ai_assistant() -> AIAssistant:
    """
    Gibt Singleton-Instance von AIAssistant zurück
    
    Returns:
        AIAssistant Instance
    """
    global _ai_assistant_instance
    if _ai_assistant_instance is None:
        _ai_assistant_instance = AIAssistant()
    return _ai_assistant_instance
