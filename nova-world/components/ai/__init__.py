"""
AI Assistant V2 - Public API
"""

from .assistant import AIAssistant

__version__ = "2.0.0"
__all__ = ['get_ai_assistant', 'AIAssistant']


def get_ai_assistant(mode: str = "auto") -> AIAssistant:
    """
    Get AI Assistant instance
    
    Args:
        mode: "auto" or "ollama"
    
    Returns:
        AIAssistant instance
    """
    return AIAssistant(mode=mode)
