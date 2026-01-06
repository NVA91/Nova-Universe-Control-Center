"""
🎤 Nova's Voice Commander
Whisper STT → Intent Recognition → Quick Actions Execution
IRON MAN MODE! 🦾
"""

import streamlit as st
from typing import Dict, Optional, Tuple
import re
from components.quick_actions import get_quick_actions
from components.whisper_integration import transcribe_audio
from components.secrets_manager import get_secrets_manager

class VoiceCommander:
    """
    Voice Command Processing für Nova-World
    Whisper → Parse Intent → Execute Action
    """
    
    def __init__(self):
        self.qa = get_quick_actions()
        
        # OpenAI für Intent Recognition
        secrets = get_secrets_manager()
        self.api_key = secrets.get_openai_key()
        self.model = secrets.get_openai_model()
        
        # Command Patterns (für schnelle Regex-Matching)
        self.quick_patterns = self._build_quick_patterns()
        
        # Dangerous commands (require confirmation)
        self.dangerous_commands = [
            "docker_stop_all",
            "emergency_stop"
        ]
    
    def _build_quick_patterns(self) -> Dict[str, Tuple[str, callable]]:
        """
        Baut Pattern-Dictionary für häufige Commands
        Format: {pattern: (command_name, action_function)}
        """
        return {
            # Docker Commands
            r"start.*all|starte.*alle|alles.*starten": 
                ("docker_start_all", self.qa.docker_start_all),
            
            r"stop.*all|stoppe.*alle|alles.*stoppen":
                ("docker_stop_all", self.qa.docker_stop_all),
            
            r"restart.*all|neustart.*alle|alle.*neustarten":
                ("docker_restart_all", self.qa.docker_restart_all),
            
            r"cleanup|aufräumen|docker.*clean":
                ("docker_cleanup", self.qa.docker_cleanup),
            
            r"docker.*status|container.*status":
                ("docker_status", self.qa.docker_status_check),
            
            # Semaphore Deployments
            r"deploy.*minimal|minimal.*deploy":
                ("deploy_minimal", self.qa.semaphore_deploy_minimal),
            
            r"deploy.*standard|standard.*deploy":
                ("deploy_standard", self.qa.semaphore_deploy_standard),
            
            r"deploy.*full|full.*deploy|alles.*deployen":
                ("deploy_full", self.qa.semaphore_deploy_full),
            
            r"semaphore.*status|deployment.*status":
                ("semaphore_status", self.qa.semaphore_status),
            
            # System Commands
            r"health.*check|system.*check|gesundheit":
                ("health_check", self.qa.system_health_quick),
            
            r"uptime|laufzeit":
                ("uptime", self.qa.system_uptime),
            
            r"errors|fehler|logs":
                ("recent_errors", self.qa.logs_recent_errors),
            
            # Composite Commands
            r"morning.*routine|morgen.*routine|startup":
                ("morning_routine", self.qa.morning_routine),
            
            r"emergency.*stop|notfall.*stop":
                ("emergency_stop", self.qa.emergency_stop),
        }
    
    async def process_voice_command(self, audio_bytes: bytes) -> Dict:
        """
        Verarbeitet Voice Command
        
        Args:
            audio_bytes: Audio-Daten vom Recorder
        
        Returns:
            Result Dict mit transcript, command, response
        """
        try:
            # Step 1: Transcribe Audio
            transcript = transcribe_audio(audio_bytes)
            
            if not transcript:
                return {
                    "success": False,
                    "error": "Transkription fehlgeschlagen",
                    "transcript": None,
                    "command": None
                }
            
            # Step 2: Parse Intent
            command_name, action_func = self._parse_intent(transcript)
            
            if not command_name:
                return {
                    "success": False,
                    "error": "Kommando nicht erkannt",
                    "transcript": transcript,
                    "command": None,
                    "response": f"Ich verstehe '{transcript}' nicht. Versuche es nochmal."
                }
            
            # Step 3: Check if confirmation needed
            if self.needs_confirmation(command_name):
                return {
                    "success": True,
                    "transcript": transcript,
                    "command": command_name,
                    "needs_confirmation": True,
                    "response": f"Kommando '{command_name}' erkannt. Bestätigung erforderlich!"
                }
            
            # Step 4: Execute Action
            result = action_func()
            
            return {
                "success": result.get("success", False),
                "transcript": transcript,
                "command": command_name,
                "action_result": result,
                "response": result.get("message", "Ausgeführt!")
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "transcript": None,
                "command": None
            }
    
    def _parse_intent(self, transcript: str) -> Tuple[Optional[str], Optional[callable]]:
        """
        Parsed Intent aus Transcript
        
        Args:
            transcript: Transkribierter Text
        
        Returns:
            (command_name, action_function) oder (None, None)
        """
        transcript_lower = transcript.lower()
        
        # Try quick pattern matching first
        for pattern, (command_name, action_func) in self.quick_patterns.items():
            if re.search(pattern, transcript_lower):
                return command_name, action_func
        
        # Fallback: Use OpenAI for intent recognition
        try:
            command_name, action_func = self._parse_intent_with_ai(transcript)
            if command_name:
                return command_name, action_func
        except Exception as e:
            st.warning(f"AI Intent Recognition fehlgeschlagen: {e}")
        
        return None, None
    
    def _parse_intent_with_ai(self, transcript: str) -> Tuple[Optional[str], Optional[callable]]:
        """
        Verwendet OpenAI für Intent Recognition
        
        Args:
            transcript: Transkribierter Text
        
        Returns:
            (command_name, action_function) oder (None, None)
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # Build prompt
            available_commands = list(self.quick_patterns.values())
            command_list = "\n".join([f"- {cmd[0]}" for cmd in available_commands])
            
            prompt = f"""Du bist ein Voice Command Parser für ein DevOps Dashboard.

Verfügbare Kommandos:
{command_list}

Benutzer sagt: "{transcript}"

Welches Kommando meint der Benutzer? Antworte NUR mit dem Kommando-Namen (z.B. "docker_start_all") oder "unknown" wenn unklar.
"""
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Du bist ein Command Parser. Antworte nur mit dem Kommando-Namen."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.0
            )
            
            command_name = response.choices[0].message.content.strip().lower()
            
            # Find matching action
            for pattern, (cmd_name, action_func) in self.quick_patterns.items():
                if cmd_name.lower() == command_name:
                    return cmd_name, action_func
            
            return None, None
        
        except Exception as e:
            raise Exception(f"AI Intent Recognition Fehler: {e}")
    
    def needs_confirmation(self, command_name: str) -> bool:
        """
        Prüft ob Kommando Bestätigung benötigt
        
        Args:
            command_name: Name des Kommandos
        
        Returns:
            True wenn Bestätigung nötig
        """
        return command_name in self.dangerous_commands
    
    def execute_command(self, command_name: str) -> Dict:
        """
        Führt Kommando direkt aus (nach Bestätigung)
        
        Args:
            command_name: Name des Kommandos
        
        Returns:
            Result Dict
        """
        # Find action function
        for pattern, (cmd_name, action_func) in self.quick_patterns.items():
            if cmd_name == command_name:
                return action_func()
        
        return {
            "success": False,
            "error": f"Kommando '{command_name}' nicht gefunden"
        }


# ============================================================================
# Singleton Instance
# ============================================================================

_voice_commander_instance = None

def get_voice_commander() -> VoiceCommander:
    """
    Gibt Singleton-Instance von VoiceCommander zurück
    
    Returns:
        VoiceCommander Instance
    """
    global _voice_commander_instance
    if _voice_commander_instance is None:
        _voice_commander_instance = VoiceCommander()
    return _voice_commander_instance
