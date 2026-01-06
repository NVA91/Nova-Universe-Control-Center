"""
🎨 UI Components
Reusable UI Components für Nova-World Dashboard
"""

import streamlit as st
from typing import Dict, Callable, Optional, List
from components.quick_actions import get_quick_actions

def render_quick_actions_grid():
    """
    Rendert Grid mit Quick Action Buttons
    """
    st.markdown("### ⚡ Quick Actions")
    
    qa = get_quick_actions()
    
    # Docker Actions
    with st.expander("🐳 Docker Control", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("▶️ Start All", use_container_width=True, key="docker_start"):
                with st.spinner("Starte Container..."):
                    result = qa.docker_start_all()
                    if result["success"]:
                        st.success(result["message"])
                        if result.get("started"):
                            st.caption(f"Started: {', '.join(result['started'])}")
                    else:
                        st.error(f"Fehler: {result.get('error')}")
        
        with col2:
            if st.button("⏹️ Stop All", use_container_width=True, key="docker_stop", type="secondary"):
                # Confirmation required!
                if st.session_state.get("confirm_docker_stop"):
                    with st.spinner("Stoppe Container..."):
                        result = qa.docker_stop_all()
                        if result["success"]:
                            st.warning(result["message"])
                        else:
                            st.error(f"Fehler: {result.get('error')}")
                    st.session_state["confirm_docker_stop"] = False
                else:
                    st.warning("⚠️ Gefährliche Aktion! Klicke nochmal zum Bestätigen.")
                    st.session_state["confirm_docker_stop"] = True
        
        with col3:
            if st.button("🔄 Restart All", use_container_width=True, key="docker_restart"):
                with st.spinner("Starte Container neu..."):
                    result = qa.docker_restart_all()
                    if result["success"]:
                        st.info(result["message"])
                    else:
                        st.error(f"Fehler: {result.get('error')}")
        
        with col4:
            if st.button("🧹 Cleanup", use_container_width=True, key="docker_cleanup"):
                with st.spinner("Räume auf..."):
                    result = qa.docker_cleanup()
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(f"Fehler: {result.get('error')}")
    
    # Semaphore Actions
    with st.expander("🚀 Semaphore Deployments"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📦 Deploy Minimal", use_container_width=True, key="deploy_minimal"):
                with st.spinner("Triggere Deployment..."):
                    result = qa.semaphore_deploy_minimal()
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(f"Fehler: {result.get('error')}")
        
        with col2:
            if st.button("📦 Deploy Standard", use_container_width=True, key="deploy_standard"):
                with st.spinner("Triggere Deployment..."):
                    result = qa.semaphore_deploy_standard()
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(f"Fehler: {result.get('error')}")
        
        with col3:
            if st.button("📦 Deploy Full", use_container_width=True, key="deploy_full"):
                with st.spinner("Triggere Deployment..."):
                    result = qa.semaphore_deploy_full()
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(f"Fehler: {result.get('error')}")
    
    # System Actions
    with st.expander("💻 System Operations"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏥 Health Check", use_container_width=True, key="health_check"):
                with st.spinner("Prüfe System..."):
                    result = qa.system_health_quick()
                    if result["success"]:
                        if result["overall"] == "healthy":
                            st.success("✅ System ist gesund!")
                        else:
                            st.warning(f"⚠️ Warnungen: {', '.join(result['warnings'])}")
                        
                        # Show metrics
                        col_cpu, col_ram, col_disk = st.columns(3)
                        with col_cpu:
                            st.metric("CPU", f"{result['cpu']['percent']}%")
                        with col_ram:
                            st.metric("RAM", f"{result['ram']['percent']}%")
                        with col_disk:
                            st.metric("Disk", f"{result['disk']['percent']}%")
                    else:
                        st.error(f"Fehler: {result.get('error')}")
        
        with col2:
            if st.button("📜 Recent Errors", use_container_width=True, key="recent_errors"):
                with st.spinner("Suche Fehler..."):
                    result = qa.logs_recent_errors()
                    if result["success"]:
                        if result["errors_count"] > 0:
                            st.warning(f"⚠️ {result['errors_count']} Fehler gefunden")
                            for error in result["errors"][:3]:
                                st.code(f"[{error['container']}] {error['line']}")
                        else:
                            st.success("✅ Keine Fehler gefunden!")
                    else:
                        st.error(f"Fehler: {result.get('error')}")
        
        with col3:
            if st.button("⏱️ Uptime", use_container_width=True, key="uptime"):
                result = qa.system_uptime()
                if result["success"]:
                    st.info(f"⏱️ Uptime: **{result['uptime_formatted']}**")
                    st.caption(f"Boot: {result['boot_time']}")
                else:
                    st.error(f"Fehler: {result.get('error')}")
    
    # Composite Actions
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌅 Morning Routine", use_container_width=True, type="primary", key="morning_routine"):
            with st.spinner("Führe Morning Routine aus..."):
                result = qa.morning_routine()
                
                if result["success"]:
                    st.success("✅ Morning Routine abgeschlossen!")
                else:
                    st.warning("⚠️ Morning Routine mit Fehlern abgeschlossen")
                
                # Show steps
                for step in result["steps"]:
                    if step["success"]:
                        st.success(f"✅ {step['name']}: {step['message']}")
                    else:
                        st.error(f"❌ {step['name']}: {step['message']}")
    
    with col2:
        if st.button("🚨 Emergency Stop", use_container_width=True, type="secondary", key="emergency_stop"):
            # Double confirmation required!
            if st.session_state.get("confirm_emergency_stop"):
                with st.spinner("Emergency Stop..."):
                    result = qa.emergency_stop()
                    if result["success"]:
                        st.warning(f"⚠️ {result['message']}")
                    else:
                        st.error(f"Fehler: {result.get('error')}")
                st.session_state["confirm_emergency_stop"] = False
            else:
                st.error("🚨 GEFÄHRLICH! Klicke nochmal zum Bestätigen.")
                st.session_state["confirm_emergency_stop"] = True


def render_action_button(
    label: str,
    action: Callable,
    icon: str = "",
    button_type: str = "primary",
    confirmation_required: bool = False,
    key: Optional[str] = None
) -> None:
    """
    Rendert einen Action Button mit optionaler Confirmation
    
    Args:
        label: Button-Label
        action: Callable Action-Funktion
        icon: Icon (Emoji)
        button_type: Button-Typ ("primary", "secondary")
        confirmation_required: Ob Confirmation nötig ist
        key: Unique Key für Button
    """
    button_label = f"{icon} {label}" if icon else label
    
    if st.button(button_label, type=button_type, use_container_width=True, key=key):
        if confirmation_required:
            confirm_key = f"confirm_{key}"
            if st.session_state.get(confirm_key):
                # Execute action
                with st.spinner(f"{label}..."):
                    result = action()
                    _display_action_result(result)
                st.session_state[confirm_key] = False
            else:
                st.warning(f"⚠️ Bestätigung erforderlich! Klicke nochmal.")
                st.session_state[confirm_key] = True
        else:
            # Execute action directly
            with st.spinner(f"{label}..."):
                result = action()
                _display_action_result(result)


def _display_action_result(result: Dict) -> None:
    """
    Zeigt Action-Result an
    
    Args:
        result: Result Dict von Action
    """
    if result.get("success"):
        st.success(result.get("message", "✅ Erfolgreich!"))
        
        # Show additional info
        if "started" in result:
            st.caption(f"Started: {', '.join(result['started'])}")
        if "stopped" in result:
            st.caption(f"Stopped: {', '.join(result['stopped'])}")
        if "restarted" in result:
            st.caption(f"Restarted: {', '.join(result['restarted'])}")
    else:
        st.error(f"❌ Fehler: {result.get('error', 'Unbekannter Fehler')}")


def render_confirmation_dialog(
    title: str,
    message: str,
    on_confirm: Callable,
    on_cancel: Optional[Callable] = None
) -> None:
    """
    Rendert Confirmation Dialog
    
    Args:
        title: Dialog-Titel
        message: Dialog-Nachricht
        on_confirm: Callback bei Bestätigung
        on_cancel: Callback bei Abbruch
    """
    st.warning(f"⚠️ **{title}**")
    st.write(message)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Ja, ausführen", type="primary", use_container_width=True):
            on_confirm()
    
    with col2:
        if st.button("❌ Abbrechen", use_container_width=True):
            if on_cancel:
                on_cancel()
            st.info("Abgebrochen")
