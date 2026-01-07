"""
🤖 Nova's AI Assistant
Context-Aware DevOps Assistant
"""

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ═══════════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════════

st.title("🤖 Nova AI Assistant")
st.caption("Dein intelligenter DevOps-Helfer")

# ═══════════════════════════════════════════════════════════
# 📋 INFO
# ═══════════════════════════════════════════════════════════

with st.expander("ℹ️ Was kann der AI Assistant?"):
    st.markdown("""
    **Nova AI Assistant** ist dein intelligenter Helfer für DevOps-Tasks!
    
    **Features:**
    - 🧠 **Context-Aware**: Kennt deinen System-Status
    - 💡 **Smart Suggestions**: Schlägt passende Quick Actions vor
    - 🔍 **Error Analysis**: Analysiert Logs und gibt Tipps
    - 📚 **Knowledge Base**: Weiß über Docker, Ansible, Semaphore Bescheid
    
    **Beispiel-Fragen:**
    - "Was läuft gerade auf meinem System?"
    - "Warum ist mein Container gestoppt?"
    - "Wie deploye ich das Standard-Profil?"
    - "Was bedeutet dieser Fehler in den Logs?"
    - "Führe einen Health Check durch"
    
    **Technologie:**
    - 🤖 OpenAI GPT-4
    - 🎯 Quick Actions Integration
    - 📊 System-Context-Awareness
    """)

st.divider()

# ═══════════════════════════════════════════════════════════
# 💬 CHAT INTERFACE
# ═══════════════════════════════════════════════════════════

# Initialize chat history
if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = []

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = [
        {
            "role": "assistant",
            "content": "👋 Hi! Ich bin Nova, dein AI Assistant. Wie kann ich dir helfen?"
        }
    ]

# Display chat messages
for message in st.session_state.ai_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Frag mich was..."):
    # Add user message
    st.session_state.ai_messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Denke nach..."):
            from components.ai_assistant import get_ai_assistant
            
            ai = get_ai_assistant()
            
            # Get system context
            system_context = ai.get_system_context()
            
            # Chat with AI
            response = ai.chat(
                user_message=prompt,
                chat_history=st.session_state.ai_chat_history[-10:],  # Last 10 messages
                system_context=system_context
            )
            
            st.markdown(response)
            
            # Check for action suggestions
            actions = ai.extract_action_suggestions(response)
            
            if actions:
                st.divider()
                st.markdown("**💡 Vorgeschlagene Actions:**")
                
                for action in actions:
                    if st.button(f"▶️ {action}", key=f"action_{action}"):
                        from components.quick_actions import get_quick_actions
                        
                        qa = get_quick_actions()
                        
                        # Execute action
                        with st.spinner(f"Führe {action} aus..."):
                            # Map action name to function
                            action_func = getattr(qa, action, None)
                            
                            if action_func:
                                result = action_func()
                                
                                if result.get("success"):
                                    st.success(result.get("message", "✅ Erfolgreich!"))
                                else:
                                    st.error(f"❌ {result.get('error')}")
                            else:
                                st.error(f"Action '{action}' nicht gefunden")
    
    # Add assistant message
    st.session_state.ai_messages.append({"role": "assistant", "content": response})
    
    # Update chat history for API
    st.session_state.ai_chat_history.append({"role": "user", "content": prompt})
    st.session_state.ai_chat_history.append({"role": "assistant", "content": response})

st.divider()

# ═══════════════════════════════════════════════════════════
# 📊 SYSTEM CONTEXT (Sidebar)
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 📊 System Context")
    
    try:
        from components.ai_assistant import get_ai_assistant
        
        ai = get_ai_assistant()
        context = ai.get_system_context()
        
        if "error" not in context:
            # CPU
            cpu_color = "🟢" if context["cpu"] < 70 else "🟡" if context["cpu"] < 90 else "🔴"
            st.metric("CPU", f"{context['cpu']}%", delta=None)
            
            # RAM
            ram_color = "🟢" if context["ram"] < 70 else "🟡" if context["ram"] < 90 else "🔴"
            st.metric("RAM", f"{context['ram']}%", delta=None)
            
            # Disk
            disk_color = "🟢" if context["disk"] < 70 else "🟡" if context["disk"] < 90 else "🔴"
            st.metric("Disk", f"{context['disk']}%", delta=None)
            
            st.divider()
            
            # Docker
            docker = context.get("docker", {})
            st.metric(
                "🐳 Docker",
                f"{docker.get('running', 0)}/{docker.get('total', 0)}",
                delta=f"{docker.get('stopped', 0)} stopped"
            )
            
            # Semaphore
            semaphore_status = context.get("semaphore", "unknown")
            status_emoji = "🟢" if semaphore_status == "online" else "🔴"
            st.metric("🚀 Semaphore", f"{status_emoji} {semaphore_status}")
        
        else:
            st.error(f"Fehler: {context['error']}")
    
    except Exception as e:
        st.error(f"Context-Fehler: {e}")
    
    st.divider()
    
    st.markdown("### 🤖 AI Info")
    st.caption("Model: GPT-4")
    st.caption("Context: System-Aware")
    
    if st.session_state.ai_messages:
        st.metric("Messages", len(st.session_state.ai_messages))
    
    st.divider()
    
    # Clear Chat
    if st.button("🗑️ Chat löschen", use_container_width=True):
        st.session_state.ai_messages = [
            {
                "role": "assistant",
                "content": "👋 Chat wurde gelöscht. Wie kann ich dir helfen?"
            }
        ]
        st.session_state.ai_chat_history = []
        st.rerun()
    
    st.divider()
    
    st.markdown("### 🔙 Navigation")
    st.page_link("nova_universe.py", label="🏠 Home")
    st.page_link("pages/01_🏠_Home.py", label="📊 Dashboard")

# ═══════════════════════════════════════════════════════════
# 💡 QUICK EXAMPLES
# ═══════════════════════════════════════════════════════════

with st.expander("💡 Beispiel-Fragen"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 System & Status:**
        - "Was läuft gerade?"
        - "Wie ist der System-Status?"
        - "Zeige mir die Container"
        - "Gibt es Fehler in den Logs?"
        
        **🐳 Docker:**
        - "Starte alle Container"
        - "Warum ist Container X gestoppt?"
        - "Räume Docker auf"
        - "Restart alle Container"
        """)
    
    with col2:
        st.markdown("""
        **🚀 Deployments:**
        - "Deploye das Standard-Profil"
        - "Was ist der Deployment-Status?"
        - "Wie deploye ich minimal?"
        
        **💡 Hilfe:**
        - "Was kann ich hier machen?"
        - "Erkläre mir Quick Actions"
        - "Was bedeutet dieser Fehler?"
        - "Gib mir Tipps für Optimierung"
        """)
