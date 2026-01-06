"""
📊 System Monitoring
Real-time Metrics & Alerts
"""

import streamlit as st
import psutil
from datetime import datetime
import time

st.set_page_config(
    page_title="Monitoring",
    page_icon="📊",
    layout="wide"
)

# ═══════════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════════

col1, col2 = st.columns([5, 1])

with col1:
    st.title("📊 System Monitoring")
    st.caption("Real-time Metrics & Performance")

with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.divider()

# ═══════════════════════════════════════════════════════════
# 📈 SYSTEM METRICS
# ═══════════════════════════════════════════════════════════

st.markdown("### 📈 System Metrics")

try:
    # Get metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💻 CPU Usage",
            f"{cpu_percent}%",
            delta=None
        )
        
        # Progress bar
        if cpu_percent < 70:
            st.progress(cpu_percent / 100, text="🟢 Normal")
        elif cpu_percent < 90:
            st.progress(cpu_percent / 100, text="🟡 High")
        else:
            st.progress(cpu_percent / 100, text="🔴 Critical")
    
    with col2:
        st.metric(
            "🧠 RAM Usage",
            f"{mem.percent}%",
            delta=f"{mem.used / (1024**3):.1f} GB used"
        )
        
        if mem.percent < 70:
            st.progress(mem.percent / 100, text="🟢 Normal")
        elif mem.percent < 90:
            st.progress(mem.percent / 100, text="🟡 High")
        else:
            st.progress(mem.percent / 100, text="🔴 Critical")
    
    with col3:
        st.metric(
            "💾 Disk Usage",
            f"{disk.percent}%",
            delta=f"{disk.free / (1024**3):.1f} GB free"
        )
        
        if disk.percent < 70:
            st.progress(disk.percent / 100, text="🟢 Normal")
        elif disk.percent < 90:
            st.progress(disk.percent / 100, text="🟡 High")
        else:
            st.progress(disk.percent / 100, text="🔴 Critical")
    
    with col4:
        # Network
        net_io = psutil.net_io_counters()
        sent_mb = net_io.bytes_sent / (1024**2)
        recv_mb = net_io.bytes_recv / (1024**2)
        
        st.metric(
            "🌐 Network",
            f"{sent_mb:.1f} MB sent",
            delta=f"{recv_mb:.1f} MB recv"
        )

except Exception as e:
    st.error(f"Fehler beim Laden der Metriken: {e}")

st.divider()

# ═══════════════════════════════════════════════════════════
# 🐳 DOCKER MONITORING
# ═══════════════════════════════════════════════════════════

st.markdown("### 🐳 Docker Container Status")

from components.quick_actions import get_quick_actions

qa = get_quick_actions()

docker_status = qa.docker_status_check()

if docker_status.get("success"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🟢 Running", docker_status.get("running", 0))
    
    with col2:
        st.metric("⏹️ Stopped", docker_status.get("stopped", 0))
    
    with col3:
        st.metric("📦 Total", docker_status.get("total", 0))
    
    # Container Details
    containers = docker_status.get("containers", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🟢 Running Containers")
        running = containers.get("running", [])
        
        if running:
            for container in running:
                st.success(f"✅ {container}")
        else:
            st.info("Keine laufenden Container")
    
    with col2:
        st.markdown("#### ⏹️ Stopped Containers")
        stopped = containers.get("stopped", [])
        
        if stopped:
            for container in stopped:
                st.warning(f"⏹️ {container}")
        else:
            st.info("Keine gestoppten Container")

else:
    st.error(f"Fehler: {docker_status.get('error')}")

st.divider()

# ═══════════════════════════════════════════════════════════
# 🚨 ALERTS & WARNINGS
# ═══════════════════════════════════════════════════════════

st.markdown("### 🚨 Alerts & Warnings")

alerts = []

# Check CPU
if cpu_percent > 90:
    alerts.append(("🔴 CRITICAL", f"CPU usage sehr hoch: {cpu_percent}%"))
elif cpu_percent > 70:
    alerts.append(("🟡 WARNING", f"CPU usage hoch: {cpu_percent}%"))

# Check RAM
if mem.percent > 90:
    alerts.append(("🔴 CRITICAL", f"RAM usage sehr hoch: {mem.percent}%"))
elif mem.percent > 70:
    alerts.append(("🟡 WARNING", f"RAM usage hoch: {mem.percent}%"))

# Check Disk
if disk.percent > 90:
    alerts.append(("🔴 CRITICAL", f"Disk usage sehr hoch: {disk.percent}%"))
elif disk.percent > 70:
    alerts.append(("🟡 WARNING", f"Disk usage hoch: {disk.percent}%"))

# Check Stopped Containers
if docker_status.get("success"):
    stopped_count = docker_status.get("stopped", 0)
    if stopped_count > 0:
        alerts.append(("🟡 WARNING", f"{stopped_count} Container gestoppt"))

# Display alerts
if alerts:
    for level, message in alerts:
        if "CRITICAL" in level:
            st.error(f"{level}: {message}")
        else:
            st.warning(f"{level}: {message}")
else:
    st.success("✅ Keine Warnungen - Alles läuft normal!")

st.divider()

# ═══════════════════════════════════════════════════════════
# 📜 RECENT ERRORS
# ═══════════════════════════════════════════════════════════

st.markdown("### 📜 Recent Errors in Logs")

if st.button("🔍 Suche Fehler", use_container_width=False):
    with st.spinner("Durchsuche Logs..."):
        errors_result = qa.logs_recent_errors()
        
        if errors_result.get("success"):
            errors_count = errors_result.get("errors_count", 0)
            
            if errors_count > 0:
                st.warning(f"⚠️ {errors_count} Fehler gefunden")
                
                for error in errors_result.get("errors", [])[:10]:
                    with st.expander(f"🔴 {error['container']}"):
                        st.code(error['line'])
            else:
                st.success("✅ Keine Fehler in den letzten Logs gefunden!")
        else:
            st.error(f"Fehler beim Durchsuchen: {errors_result.get('error')}")

st.divider()

# ═══════════════════════════════════════════════════════════
# ⏱️ SYSTEM INFO
# ═══════════════════════════════════════════════════════════

with st.expander("ℹ️ System Information"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**System:**")
        
        # Uptime
        uptime_result = qa.system_uptime()
        if uptime_result.get("success"):
            st.write(f"⏱️ Uptime: {uptime_result['uptime_formatted']}")
            st.caption(f"Boot: {uptime_result['boot_time']}")
        
        # CPU Info
        cpu_count = psutil.cpu_count()
        st.write(f"💻 CPU Cores: {cpu_count}")
        
        # RAM Info
        mem_total = mem.total / (1024**3)
        st.write(f"🧠 RAM Total: {mem_total:.1f} GB")
    
    with col2:
        st.markdown("**Storage:**")
        
        # Disk Info
        disk_total = disk.total / (1024**3)
        disk_used = disk.used / (1024**3)
        disk_free = disk.free / (1024**3)
        
        st.write(f"💾 Total: {disk_total:.1f} GB")
        st.write(f"📊 Used: {disk_used:.1f} GB")
        st.write(f"📂 Free: {disk_free:.1f} GB")

# ═══════════════════════════════════════════════════════════
# 📱 SIDEBAR
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 📊 Monitoring")
    
    # Auto-refresh option
    auto_refresh = st.checkbox("🔄 Auto-Refresh (30s)")
    
    if auto_refresh:
        st.info("Auto-Refresh aktiv")
        time.sleep(30)
        st.rerun()
    
    st.divider()
    
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("🏥 Health Check", use_container_width=True):
        with st.spinner("Prüfe System..."):
            health = qa.system_health_quick()
            
            if health.get("success"):
                if health["overall"] == "healthy":
                    st.success("✅ System gesund!")
                else:
                    st.warning(f"⚠️ {', '.join(health['warnings'])}")
    
    if st.button("📜 Check Logs", use_container_width=True):
        st.switch_page("pages/04_📊_Monitor.py")
    
    st.divider()
    
    st.markdown("### 🔙 Navigation")
    st.page_link("nova_universe.py", label="🏠 Home")
    st.page_link("pages/01_🏠_Home.py", label="📊 Dashboard")
