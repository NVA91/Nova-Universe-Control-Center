"""
Nova-World Dashboard - AI Assistant
Powered by Ollama (Self-Hosted)
"""

import streamlit as st
import sys
from pathlib import Path
import psutil

# Add components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.ai_assistant_ollama import get_ai_assistant

# ═══════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def get_system_info() -> dict:
    """Get current system information"""
    try:
        return {
            "cpu": round(psutil.cpu_percent(interval=1), 1),
            "memory": round(psutil.virtual_memory().percent, 1),
            "disk": round(psutil.disk_usage('/').percent, 1)
        }
    except:
        return {}

# ═══════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════

st.title("🤖 AI Assistant")
st.markdown("**Nova** - Your Infrastructure AI Helper (Powered by Ollama)")

# Initialize AI Assistant
ai = get_ai_assistant()

# Check availability
if not ai.is_available():
    st.error("❌ Ollama nicht verfügbar!")
    st.info("""
    **Ollama Setup:**
    1. Ollama installieren: `curl -fsSL https://ollama.com/install.sh | sh`
    2. Model herunterladen: `ollama pull llama3:8b`
    3. `[ollama]` in `secrets.toml` aktivieren
    """)
    st.stop()

st.success(f"✅ Ollama verfügbar - Model: {ai.model}")

# ═══════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["💬 Chat", "💡 Suggestions", "ℹ️ Info"])

# ───────────────────────────────────────────────────────────
# TAB 1: CHAT
# ───────────────────────────────────────────────────────────

with tab1:
    st.subheader("Chat with Nova")
    
    # Initialize conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Frage Nova..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Nova denkt nach..."):
                system_info = get_system_info()
                
                response = ai.chat(
                    message=prompt,
                    conversation_history=st.session_state.messages[:-1],
                    system_info=system_info
                )
                
                if response["success"]:
                    st.markdown(response["message"])
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["message"]
                    })
                else:
                    st.error(response["message"])
    
    # Clear chat button
    if st.button("🗑️ Chat löschen"):
        st.session_state.messages = []
        st.rerun()

# ───────────────────────────────────────────────────────────
# TAB 2: INTELLIGENT SUGGESTIONS
# ───────────────────────────────────────────────────────────

with tab2:
    st.subheader("💡 Intelligente Vorschläge")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🐳 Docker")
        if st.button("Docker-Empfehlung", use_container_width=True):
            with st.spinner("Analysiere Docker-Status..."):
                system_info = get_system_info()
                response = ai.get_suggestion("docker", system_info)
                
                if response["success"]:
                    st.success("Empfehlung:")
                    st.markdown(response["message"])
                else:
                    st.error(response["message"])
        
        st.markdown("### 🚀 Deployment")
        if st.button("Deployment-Empfehlung", use_container_width=True):
            with st.spinner("Analysiere System..."):
                system_info = get_system_info()
                response = ai.get_suggestion("deployment", system_info)
                
                if response["success"]:
                    st.success("Empfehlung:")
                    st.markdown(response["message"])
                else:
                    st.error(response["message"])
    
    with col2:
        st.markdown("### 🔧 System")
        if st.button("System-Optimierung", use_container_width=True):
            with st.spinner("Analysiere System-Metriken..."):
                system_info = get_system_info()
                response = ai.get_suggestion("system", system_info)
                
                if response["success"]:
                    st.success("Empfehlung:")
                    st.markdown(response["message"])
                else:
                    st.error(response["message"])
        
        st.markdown("### 💾 Backup")
        if st.button("Backup-Empfehlung", use_container_width=True):
            with st.spinner("Prüfe Backup-Status..."):
                system_info = get_system_info()
                response = ai.get_suggestion("backup", system_info)
                
                if response["success"]:
                    st.success("Empfehlung:")
                    st.markdown(response["message"])
                else:
                    st.error(response["message"])
    
    # Quick Actions Erklärungen
    st.divider()
    st.markdown("### ⚡ Quick Actions Erklärer")
    
    action = st.selectbox(
        "Wähle eine Quick Action:",
        [
            "Deploy Minimal",
            "Deploy Standard",
            "Deploy Full",
            "Docker Start All",
            "Docker Stop All",
            "Docker Cleanup",
            "System Health Check"
        ]
    )
    
    if st.button("🤔 Was macht diese Action?", use_container_width=True):
        with st.spinner("Erkläre Action..."):
            response = ai.explain_action(action)
            
            if response["success"]:
                st.info(response["message"])
            else:
                st.error(response["message"])

# ───────────────────────────────────────────────────────────
# TAB 3: INFO
# ───────────────────────────────────────────────────────────

with tab3:
    st.subheader("ℹ️ AI Assistant Info")
    
    st.markdown(f"""
    ### 🤖 Nova AI Assistant
    
    **Model:** {ai.model}  
    **Engine:** Ollama (Self-Hosted)  
    **Temperature:** {ai.temperature}  
    **API:** {ai.api_url}
    
    ### ✨ Features
    
    - 💬 **Chat Interface** - Stelle Fragen zu deiner Infrastruktur
    - 💡 **Intelligente Vorschläge** - Context-aware Empfehlungen
    - 🎯 **Quick Actions Hilfe** - Erklärt was Actions machen
    - 📊 **System-Kontext** - Nutzt aktuelle System-Metriken
    - 🔒 **100% Lokal** - Keine Cloud, keine Kosten (0€/Monat)
    
    ### 🎯 Use Cases
    
    **Frage Nova:**
    - "Welche Container laufen gerade?"
    - "Soll ich Deploy Standard oder Full wählen?"
    - "Warum ist die CPU so hoch?"
    - "Wie mache ich ein Backup?"
    - "Was macht Docker Cleanup?"
    
    ### 🔧 Configuration
    
    In `.streamlit/secrets.toml`:
    ```toml
    [ollama]
    enabled = true
    api_url = "http://localhost:11434"
    model = "llama3:8b"
    temperature = 0.7
    ```
    """)
    
    # System Info
    st.divider()
    st.markdown("### 📊 Aktuelle System-Info")
    
    system_info = get_system_info()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("CPU", f"{system_info.get('cpu', 0)}%")
    
    with col2:
        st.metric("RAM", f"{system_info.get('memory', 0)}%")
    
    with col3:
        st.metric("Disk", f"{system_info.get('disk', 0)}%")

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    st.divider()
    
    st.markdown("### 🤖 AI Status")
    
    if ai.is_available():
        st.success("✅ Online")
        st.info(f"Model: {ai.model}")
    else:
        st.error("❌ Offline")
    
    st.metric("Messages", len(st.session_state.get("messages", [])))
