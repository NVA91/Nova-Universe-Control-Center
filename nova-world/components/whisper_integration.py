"""
🎤 Whisper Integration
Speech-to-Text mit OpenAI Whisper
"""

import streamlit as st
from typing import Optional
from io import BytesIO
from components.secrets_manager import get_secrets_manager

class WhisperIntegration:
    """
    Whisper STT Integration
    Unterstützt OpenAI API und Self-Hosted
    """
    
    def __init__(self):
        secrets = get_secrets_manager()
        self.api_key = secrets.get_openai_key()
        self.model = secrets.get_whisper_model()
        self.self_hosted = secrets.is_feature_enabled("self_hosted_whisper")
        
        if not self.self_hosted and not self.api_key:
            raise ValueError("OpenAI API Key fehlt in secrets.toml!")
    
    def transcribe_audio(self, audio_bytes: bytes) -> Optional[str]:
        """
        Transkribiert Audio zu Text
        
        Args:
            audio_bytes: Audio-Daten (WAV, MP3, etc.)
        
        Returns:
            Transkribierter Text oder None bei Fehler
        """
        try:
            if self.self_hosted:
                return self._transcribe_self_hosted(audio_bytes)
            else:
                return self._transcribe_openai(audio_bytes)
        
        except Exception as e:
            st.error(f"Whisper Fehler: {e}")
            return None
    
    def _transcribe_openai(self, audio_bytes: bytes) -> Optional[str]:
        """
        Transkribiert via OpenAI API
        
        Args:
            audio_bytes: Audio-Daten
        
        Returns:
            Transkribierter Text
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # Create BytesIO object
            audio_file = BytesIO(audio_bytes)
            audio_file.name = "audio.wav"
            
            # Transcribe
            transcript = client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                language="de"  # Deutsch
            )
            
            return transcript.text
        
        except Exception as e:
            raise Exception(f"OpenAI Whisper Fehler: {e}")
    
    def _transcribe_self_hosted(self, audio_bytes: bytes) -> Optional[str]:
        """
        Transkribiert via Self-Hosted Whisper
        
        Args:
            audio_bytes: Audio-Daten
        
        Returns:
            Transkribierter Text
        """
        # TODO: Implement self-hosted Whisper
        # This would call a local Whisper server (e.g., on vm-ai-lab)
        raise NotImplementedError("Self-Hosted Whisper noch nicht implementiert")


# ============================================================================
# Singleton Instance
# ============================================================================

_whisper_instance = None

def get_whisper_integration() -> WhisperIntegration:
    """
    Gibt Singleton-Instance von WhisperIntegration zurück
    
    Returns:
        WhisperIntegration Instance
    """
    global _whisper_instance
    if _whisper_instance is None:
        _whisper_instance = WhisperIntegration()
    return _whisper_instance


def transcribe_audio(audio_bytes: bytes) -> Optional[str]:
    """
    Convenience Function: Transkribiert Audio
    
    Args:
        audio_bytes: Audio-Daten
    
    Returns:
        Transkribierter Text
    """
    whisper = get_whisper_integration()
    return whisper.transcribe_audio(audio_bytes)
