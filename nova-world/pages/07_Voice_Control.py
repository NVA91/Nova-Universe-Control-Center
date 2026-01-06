"""
🎤 Nova's Voice Control Center
IRON MAN MODE! 🦾
"""

import streamlit as st
import asyncio

st.set_page_config(
    page_title="Voice Control",
    page_icon="🎤",
    layout="wide"
)

# ═══════════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════════

st.title("🎤 Voice Control Center")
st.caption("Sprich mit Nova-World - IRON MAN Mode! 🦾")

# ═══════════════════════════════════════════════════════════
# 📋 INFO
# ═══════════════════════════════════════════════════════════

with st.expander("ℹ️ Wie funktioniert Voice Control?"):
    st.markdown("""
    **Voice Control** ermöglicht dir, Nova-World per Sprache zu steuern!
    
    **So geht's:**
    1. Klicke auf den 🎤 Button unten
    2. Sprich dein Kommando (z.B. "Start all containers")
    3. Warte auf die Bestätigung
    4. Bei gefährlichen Aktionen: Bestätige nochmal
    
    **Beispiel-Kommandos:**
    - 🐳 "Start all" → Startet alle Container
    - 🐳 "Stop all" → Stoppt alle Container (Bestätigung!)
    - 🚀 "Deploy Standard" → Standard Deployment
    - 💻 "Health Check" → System-Status prüfen
    - 🌅 "Morning Routine" → Startup-Routine
    - 🚨 "Emergency Stop" → Notfall-Stop (Bestätigung!)
    
    **Technologie:**
    - 🎤 OpenAI Whisper (Speech-to-Text)
    - 🧠 GPT-4 (Intent Recognition)
    - ⚡ Quick Actions (Execution)
    """)

st.divider()

# ═══════════════════════════════════════════════════════════
# 🎤 VOICE RECORDER
# ═══════════════════════════════════════════════════════════

st.markdown("### 🎤 Voice Command")

# Check if audio-recorder-streamlit is available
try:
    from audio_recorder_streamlit import audio_recorder
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info("**Klick den Button und sprich dein Kommando!**")
        
        # Audio Recorder
        audio_bytes = audio_recorder(
            text="🎤 Klick & Sprich",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="4x",
            pause_threshold=2.0,  # Stop nach 2 Sekunden Stille
        )
    
    with col2:
        # Status Indicator
        if "voice_processing" in st.session_state and st.session_state.voice_processing:
            st.info("🎧 Höre zu...")
        elif "last_command" in st.session_state:
            st.success("✅ Ready")
        else:
            st.info("⏸️ Bereit")
    
    # ═══════════════════════════════════════════════════════════
    # 🧠 VOICE PROCESSING
    # ═══════════════════════════════════════════════════════════
    
    if audio_bytes:
        st.session_state.voice_processing = True
        
        with st.spinner("🧠 Verstehe dein Kommando..."):
            from components.voice_commander import get_voice_commander
            
            vc = get_voice_commander()
            
            # Process Voice Command
            result = asyncio.run(vc.process_voice_command(audio_bytes))
        
        st.session_state.voice_processing = False
        
        # Display Results
        if result["success"]:
            # Show Transcript
            st.success(f"📝 **Du hast gesagt:** {result['transcript']}")
            
            # Show Command Recognition
            st.info(f"🎯 **Erkanntes Kommando:** {result['command']}")
            
            # Check if dangerous command needs confirmation
            if result.get("needs_confirmation"):
                st.warning("⚠️ **WARNUNG:** Dies ist eine gefährliche Aktion!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Ja, ausführen!", type="primary", key="confirm_voice"):
                        with st.spinner("Führe aus..."):
                            exec_result = vc.execute_command(result["command"])
                            
                            if exec_result["success"]:
                                st.success(f"✅ {exec_result['message']}")
                            else:
                                st.error(f"❌ {exec_result.get('error')}")
                
                with col2:
                    if st.button("❌ Abbrechen", key="cancel_voice"):
                        st.info("Abgebrochen")
            
            else:
                # Show execution result
                st.success(f"✅ **Ergebnis:** {result['response']}")
                
                # Show details
                if "action_result" in result:
                    action_result = result["action_result"]
                    
                    with st.expander("🔍 Details"):
                        st.json(action_result)
            
            # Save to history
            if "voice_history" not in st.session_state:
                st.session_state.voice_history = []
            
            st.session_state.voice_history.append({
                "transcript": result["transcript"],
                "command": result["command"],
                "timestamp": st.session_state.get("_timestamp", "now")
            })
        
        else:
            st.error(f"❌ **Fehler:** {result.get('error', 'Unbekannter Fehler')}")
            
            if result.get("transcript"):
                st.caption(f"Transkript: {result['transcript']}")

except ImportError:
    st.error("❌ **audio-recorder-streamlit** nicht installiert!")
    st.info("""
    **Installation erforderlich:**
    ```bash
    pip install audio-recorder-streamlit
    ```
    
    Danach Streamlit neu starten.
    """)

st.divider()

# ═══════════════════════════════════════════════════════════
# 📜 VOICE HISTORY
# ═══════════════════════════════════════════════════════════

st.markdown("### 📜 Voice Command History")

if "voice_history" in st.session_state and st.session_state.voice_history:
    # Show last 10 commands
    for i, cmd in enumerate(reversed(st.session_state.voice_history[-10:])):
        with st.expander(f"🎤 {cmd['transcript']}", expanded=(i == 0)):
            st.write(f"**Kommando:** {cmd['command']}")
            st.caption(f"Zeitpunkt: {cmd.get('timestamp', 'unbekannt')}")
else:
    st.info("Noch keine Voice Commands ausgeführt")

st.divider()

# ═══════════════════════════════════════════════════════════
# 💡 QUICK TIPS
# ═══════════════════════════════════════════════════════════

with st.expander("💡 Voice Command Cheat Sheet"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🐳 Docker Commands:**
        - "Start all" → Alle Container starten
        - "Stop all" → Alle Container stoppen
        - "Restart all" → Alle Container neustarten
        - "Cleanup" → Docker aufräumen
        - "Docker status" → Container-Status
        
        **🚀 Deployment Commands:**
        - "Deploy Minimal" → Minimal Deployment
        - "Deploy Standard" → Standard Deployment
        - "Deploy Full" → Full Deployment
        - "Semaphore Status" → Deployment-Status
        """)
    
    with col2:
        st.markdown("""
        **💻 System Commands:**
        - "Health Check" → System-Status prüfen
        - "Uptime" → System-Laufzeit
        - "Errors" → Fehler in Logs suchen
        
        **🎯 Composite Commands:**
        - "Morning Routine" → Startup-Routine
        - "Emergency Stop" → Notfall-Stop
        
        **💡 Tipps:**
        - Sprich klar und deutlich
        - Warte auf Stille-Erkennung (2 Sek)
        - Bei Fehlern: Nochmal versuchen
        """)

# ═══════════════════════════════════════════════════════════
# 📱 SIDEBAR
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🎤 Voice Control")
    
    st.info("""
    **Status:** 🟢 Aktiv
    
    **Features:**
    - ✅ Whisper STT
    - ✅ Intent Recognition
    - ✅ Quick Actions
    - ✅ Safety Confirmations
    """)
    
    if "voice_history" in st.session_state:
        st.metric("Commands Today", len(st.session_state.voice_history))
    
    st.divider()
    
    st.markdown("### 🔙 Navigation")
    st.page_link("nova_universe.py", label="🏠 Home")
    st.page_link("pages/01_🏠_Home.py", label="📊 Dashboard")
