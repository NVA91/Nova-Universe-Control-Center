"""
🔧 Docker Container Management
Start, Stop, Restart, Logs
"""

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Docker Management",
    page_icon="🔧",
    layout="wide"
)

# ═══════════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════════

st.title("🔧 Docker Container Management")
st.caption("Start, Stop, Restart, Logs")

st.divider()

# ═══════════════════════════════════════════════════════════
# 📊 DOCKER OVERVIEW
# ═══════════════════════════════════════════════════════════

st.markdown("### 📊 Docker Overview")

from components.quick_actions import get_quick_actions

qa = get_quick_actions()

docker_status = qa.docker_status_check()

if docker_status.get("success"):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🟢 Running", docker_status.get("running", 0))
    
    with col2:
        st.metric("⏹️ Stopped", docker_status.get("stopped", 0))
    
    with col3:
        st.metric("📦 Total", docker_status.get("total", 0))
    
    with col4:
        # Health indicator
        running = docker_status.get("running", 0)
        total = docker_status.get("total", 0)
        
        if total == 0:
            st.metric("Status", "⚪ Keine Container")
        elif running == total:
            st.metric("Status", "🟢 Alle laufen")
        elif running > 0:
            st.metric("Status", "🟡 Teilweise")
        else:
            st.metric("Status", "🔴 Alle gestoppt")

else:
    st.error(f"Fehler beim Laden: {docker_status.get('error')}")

st.divider()

# ═══════════════════════════════════════════════════════════
# 🎮 QUICK ACTIONS
# ═══════════════════════════════════════════════════════════

st.markdown("### 🎮 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("▶️ Start All", use_container_width=True, type="primary"):
        with st.spinner("Starte Container..."):
            result = qa.docker_start_all()
            
            if result["success"]:
                st.success(result["message"])
                if result.get("started"):
                    st.caption(f"Started: {', '.join(result['started'])}")
                st.rerun()
            else:
                st.error(f"Fehler: {result.get('error')}")

with col2:
    if st.button("⏹️ Stop All", use_container_width=True, type="secondary"):
        # Confirmation required
        if "confirm_stop_all" not in st.session_state:
            st.session_state.confirm_stop_all = False
        
        if st.session_state.confirm_stop_all:
            with st.spinner("Stoppe Container..."):
                result = qa.docker_stop_all()
                
                if result["success"]:
                    st.warning(result["message"])
                    st.rerun()
                else:
                    st.error(f"Fehler: {result.get('error')}")
            
            st.session_state.confirm_stop_all = False
        else:
            st.warning("⚠️ Gefährlich! Klicke nochmal zum Bestätigen.")
            st.session_state.confirm_stop_all = True

with col3:
    if st.button("🔄 Restart All", use_container_width=True):
        with st.spinner("Starte Container neu..."):
            result = qa.docker_restart_all()
            
            if result["success"]:
                st.info(result["message"])
                st.rerun()
            else:
                st.error(f"Fehler: {result.get('error')}")

with col4:
    if st.button("🧹 Cleanup", use_container_width=True):
        with st.spinner("Räume auf..."):
            result = qa.docker_cleanup()
            
            if result["success"]:
                st.success(result["message"])
                with st.expander("Details"):
                    st.text(result.get("output", ""))
            else:
                st.error(f"Fehler: {result.get('error')}")

st.divider()

# ═══════════════════════════════════════════════════════════
# 📋 CONTAINER LIST
# ═══════════════════════════════════════════════════════════

st.markdown("### 📋 Container List")

if docker_status.get("success"):
    containers = docker_status.get("containers", {})
    
    # Running Containers
    st.markdown("#### 🟢 Running Containers")
    
    running = containers.get("running", [])
    
    if running:
        for container in running:
            with st.expander(f"🟢 {container}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("⏹️ Stop", key=f"stop_{container}", use_container_width=True):
                        import subprocess
                        result = subprocess.run(
                            ["docker", "stop", container],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        
                        if result.returncode == 0:
                            st.success(f"✅ {container} gestoppt")
                            st.rerun()
                        else:
                            st.error(f"Fehler: {result.stderr}")
                
                with col2:
                    if st.button("🔄 Restart", key=f"restart_{container}", use_container_width=True):
                        import subprocess
                        result = subprocess.run(
                            ["docker", "restart", container],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        
                        if result.returncode == 0:
                            st.success(f"✅ {container} neugestartet")
                            st.rerun()
                        else:
                            st.error(f"Fehler: {result.stderr}")
                
                with col3:
                    if st.button("📜 Logs", key=f"logs_{container}", use_container_width=True):
                        import subprocess
                        result = subprocess.run(
                            ["docker", "logs", "--tail", "50", container],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        
                        st.code(result.stdout + result.stderr)
    else:
        st.info("Keine laufenden Container")
    
    st.divider()
    
    # Stopped Containers
    st.markdown("#### ⏹️ Stopped Containers")
    
    stopped = containers.get("stopped", [])
    
    if stopped:
        for container in stopped:
            with st.expander(f"⏹️ {container}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("▶️ Start", key=f"start_{container}", use_container_width=True):
                        import subprocess
                        result = subprocess.run(
                            ["docker", "start", container],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        
                        if result.returncode == 0:
                            st.success(f"✅ {container} gestartet")
                            st.rerun()
                        else:
                            st.error(f"Fehler: {result.stderr}")
                
                with col2:
                    if st.button("📜 Logs", key=f"logs_stopped_{container}", use_container_width=True):
                        import subprocess
                        result = subprocess.run(
                            ["docker", "logs", "--tail", "50", container],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        
                        st.code(result.stdout + result.stderr)
    else:
        st.info("Keine gestoppten Container")

else:
    st.error("Fehler beim Laden der Container-Liste")

st.divider()

# ═══════════════════════════════════════════════════════════
# 💡 DOCKER TIPS
# ═══════════════════════════════════════════════════════════

with st.expander("💡 Docker Tips"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎮 Container Management:**
        - **Start All** → Startet alle gestoppten Container
        - **Stop All** → Stoppt alle laufenden Container (VORSICHT!)
        - **Restart All** → Neustart aller Container
        - **Cleanup** → Entfernt ungenutzte Images/Volumes
        
        **📜 Logs:**
        - Zeigt letzte 50 Zeilen
        - Hilfreich bei Fehlersuche
        - Kombiniert stdout + stderr
        """)
    
    with col2:
        st.markdown("""
        **⚡ Pro Tips:**
        - Regelmäßig **Cleanup** ausführen
        - **Logs** bei Problemen prüfen
        - **Restart** bei hängenden Containern
        - **Stop All** nur im Notfall
        
        **🚨 Wichtig:**
        - Stop All stoppt ALLE Container!
        - Vor Cleanup: Wichtige Daten sichern
        - Bei Fehlern: AI Assistant fragen
        """)

# ═══════════════════════════════════════════════════════════
# 📱 SIDEBAR
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🔧 Docker")
    
    # Quick Status
    if docker_status.get("success"):
        running = docker_status.get("running", 0)
        total = docker_status.get("total", 0)
        
        if total > 0:
            percentage = (running / total) * 100
            st.progress(percentage / 100, text=f"{running}/{total} laufen")
        else:
            st.info("Keine Container")
    
    st.divider()
    
    st.markdown("### 🔄 Refresh")
    
    if st.button("🔄 Aktualisieren", use_container_width=True):
        st.rerun()
    
    st.divider()
    
    st.markdown("### 🔙 Navigation")
    st.page_link("nova_universe.py", label="🏠 Home")
    st.page_link("pages/01_🏠_Home.py", label="📊 Dashboard")
