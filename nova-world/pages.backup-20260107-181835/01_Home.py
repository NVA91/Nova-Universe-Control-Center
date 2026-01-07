"""
🏠 Nova-World Home Dashboard
System Overview & Quick Actions
"""

import streamlit as st
from datetime import datetime
import psutil

st.set_page_config(
    page_title="Home Dashboard",
    page_icon="🏠",
    layout="wide"
)

# ═══════════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════════

col1, col2 = st.columns([5, 1])

with col1:
    st.title("🏠 Nova-World Dashboard")
    st.caption(f"{datetime.now().strftime('%A, %d %B %Y • %H:%M')}")

with col2:
    # Quick Voice Button
    from components.secrets_manager import get_secrets_manager
    secrets = get_secrets_manager()
    
    if secrets.is_feature_enabled("voice_control_enabled"):
        if st.button("🎤", use_container_width=True, type="primary"):
            st.switch_page("pages/🎤_Voice_Control.py")

st.divider()

# ═══════════════════════════════════════════════════════════
# 📊 SYSTEM STATUS CARDS
# ═══════════════════════════════════════════════════════════

st.markdown("### 📊 System Status")

col1, col2, col3, col4 = st.columns(4)

try:
    # CPU
    with col1:
        cpu_percent = psutil.cpu_percent(interval=1)
        delta_color = "normal" if cpu_percent < 70 else "inverse"
        st.metric(
            "💻 CPU",
            f"{cpu_percent}%",
            delta=None,
            delta_color=delta_color
        )
        
        # Status indicator
        if cpu_percent < 70:
            st.success("🟢 Normal")
        elif cpu_percent < 90:
            st.warning("🟡 Hoch")
        else:
            st.error("🔴 Kritisch")
    
    # RAM
    with col2:
        mem = psutil.virtual_memory()
        delta_color = "normal" if mem.percent < 70 else "inverse"
        st.metric(
            "🧠 RAM",
            f"{mem.percent}%",
            delta=f"{mem.used / (1024**3):.1f} GB used",
            delta_color=delta_color
        )
        
        if mem.percent < 70:
            st.success("🟢 Normal")
        elif mem.percent < 90:
            st.warning("🟡 Hoch")
        else:
            st.error("🔴 Kritisch")
    
    # Disk
    with col3:
        disk = psutil.disk_usage('/')
        delta_color = "normal" if disk.percent < 70 else "inverse"
        st.metric(
            "💾 Disk",
            f"{disk.percent}%",
            delta=f"{disk.free / (1024**3):.1f} GB free",
            delta_color=delta_color
        )
        
        if disk.percent < 70:
            st.success("🟢 Normal")
        elif disk.percent < 90:
            st.warning("🟡 Hoch")
        else:
            st.error("🔴 Kritisch")
    
    # Docker
    with col4:
        from components.quick_actions import get_quick_actions
        
        qa = get_quick_actions()
        docker_status = qa.docker_status_check()
        
        if docker_status.get("success"):
            running = docker_status.get("running", 0)
            total = docker_status.get("total", 0)
            
            st.metric(
                "🐳 Docker",
                f"{running}/{total}",
                delta=f"{docker_status.get('stopped', 0)} stopped"
            )
            
            if running == total:
                st.success("🟢 Alle laufen")
            elif running > 0:
                st.warning("🟡 Teilweise")
            else:
                st.error("🔴 Alle gestoppt")
        else:
            st.metric("🐳 Docker", "Error")
            st.error("🔴 Fehler")

except Exception as e:
    st.error(f"Fehler beim Laden der System-Metriken: {e}")

st.divider()

# ═══════════════════════════════════════════════════════════
# ⚡ QUICK ACTIONS
# ═══════════════════════════════════════════════════════════

from components.ui_components import render_quick_actions_grid

render_quick_actions_grid()

st.divider()

# ═══════════════════════════════════════════════════════════
# 📈 RECENT ACTIVITY
# ═══════════════════════════════════════════════════════════

st.markdown("### 📈 Recent Activity")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🐳 Docker Events")
    
    try:
        from components.quick_actions import get_quick_actions
        
        qa = get_quick_actions()
        docker_status = qa.docker_status_check()
        
        if docker_status.get("success"):
            containers = docker_status.get("containers", {})
            running = containers.get("running", [])
            stopped = containers.get("stopped", [])
            
            if running:
                st.success(f"✅ **Running:** {', '.join(running[:5])}")
                if len(running) > 5:
                    st.caption(f"... und {len(running) - 5} weitere")
            
            if stopped:
                st.warning(f"⏹️ **Stopped:** {', '.join(stopped[:5])}")
                if len(stopped) > 5:
                    st.caption(f"... und {len(stopped) - 5} weitere")
            
            if not running and not stopped:
                st.info("Keine Container gefunden")
        else:
            st.error("Fehler beim Laden der Container")
    
    except Exception as e:
        st.error(f"Fehler: {e}")

with col2:
    st.markdown("#### 🚀 Deployment Status")
    
    try:
        from components.quick_actions import get_quick_actions
        
        qa = get_quick_actions()
        semaphore_status = qa.semaphore_status()
        
        if semaphore_status.get("success"):
            st.success(f"✅ Semaphore: **{semaphore_status.get('status')}**")
            st.caption(semaphore_status.get("message"))
        else:
            st.error(f"❌ Semaphore: **{semaphore_status.get('status')}**")
            st.caption(semaphore_status.get("message"))
    
    except Exception as e:
        st.error(f"Fehler: {e}")

st.divider()

# ═══════════════════════════════════════════════════════════
# 💡 QUICK TIPS
# ═══════════════════════════════════════════════════════════

with st.expander("💡 Quick Tips"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🚀 Schnellstart:**
        - Nutze **Quick Actions** für häufige Tasks
        - **Voice Control** für Hands-Free-Steuerung
        - **AI Assistant** für Hilfe und Tipps
        
        **🔧 Wartung:**
        - Regelmäßig **Docker Cleanup** ausführen
        - **Health Check** vor Deployments
        - **Logs** bei Fehlern prüfen
        """)
    
    with col2:
        st.markdown("""
        **⚡ Pro Tips:**
        - **Morning Routine** für schnellen Start
        - **Emergency Stop** bei Problemen
        - **Monitor** für Echtzeit-Überwachung
        
        **🎤 Voice Commands:**
        - "Start all" → Alle Container starten
        - "Health Check" → System prüfen
        - "Deploy Standard" → Deployment
        """)

# ═══════════════════════════════════════════════════════════
# 📱 SIDEBAR
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🏠 Dashboard")
    
    # System Uptime
    try:
        from components.quick_actions import get_quick_actions
        
        qa = get_quick_actions()
        uptime_result = qa.system_uptime()
        
        if uptime_result.get("success"):
            st.info(f"⏱️ **Uptime:**\n{uptime_result['uptime_formatted']}")
    except:
        pass
    
    st.divider()
    
    st.markdown("### 🎮 Quick Navigation")
    st.page_link("pages/02_🤖_AI_Assistant.py", label="🤖 AI Assistant")
    st.page_link("pages/03_🚀_Deploy.py", label="🚀 Deploy")
    st.page_link("pages/04_📊_Monitor.py", label="📊 Monitor")
    st.page_link("pages/06_🔧_Docker.py", label="🔧 Docker")
    
    if secrets.is_feature_enabled("voice_control_enabled"):
        st.page_link("pages/🎤_Voice_Control.py", label="🎤 Voice Control")
    
    st.divider()
    
    st.caption("🪐 Nova-World v1.0")
    st.caption(f"© {datetime.now().year}")
