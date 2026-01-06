"""
🪐 Nova-World Control Center
Main Dashboard Application
"""

import streamlit as st
from datetime import datetime
from components.secrets_manager import get_secrets_manager

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Nova World",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Main Container */
    .main {
        padding-top: 2rem;
    }
    
    /* Header */
    h1 {
        color: #3498db;
        font-weight: 700;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
    
    /* Success/Warning/Error boxes */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SECRETS VALIDATION
# ============================================================================

secrets_manager = get_secrets_manager()
missing_secrets = secrets_manager.get_missing_secrets()

if missing_secrets:
    st.warning("⚠️ Einige Secrets fehlen!")
    st.info("""
    **Setup erforderlich:**
    1. Öffne `.streamlit/secrets.toml`
    2. Füge fehlende Secrets hinzu:
    """)
    for secret in missing_secrets:
        st.code(f"- {secret}")
    st.info("Siehe `.streamlit/secrets.toml.example` für Beispiele")
    st.stop()

# ============================================================================
# HEADER
# ============================================================================

col1, col2 = st.columns([5, 1])

with col1:
    st.title("🪐 Nova World Control Center")
    st.caption(f"Welcome to Nova-World • {datetime.now().strftime('%A, %d %B %Y • %H:%M')}")

with col2:
    # Quick Voice Button (wenn Voice Control aktiviert)
    if secrets_manager.is_feature_enabled("voice_control_enabled"):
        if st.button("🎤 Voice", use_container_width=True, type="primary"):
            st.switch_page("pages/07_Voice_Control.py")

st.divider()

# ============================================================================
# WELCOME MESSAGE
# ============================================================================

st.markdown("### 👋 Willkommen im Nova-World Dashboard")

st.info("""
**Nova-World** ist dein zentrales Control Center für das Unified Ansible Project.

**Features:**
- 🏠 **Dashboard**: System-Übersicht und Quick Actions
- 🤖 **AI Assistant**: Intelligenter Chat-Assistent
- 🚀 **Deploy**: Ansible-Deployment-Kontrolle
- 📊 **Monitor**: System-Monitoring und Metriken
- 🔧 **Docker**: Container-Management
- 🎤 **Voice Control**: Sprachsteuerung (optional)
""")

# ============================================================================
# QUICK START
# ============================================================================

st.markdown("### 🚀 Quick Start")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/01_Home.py")
    st.caption("System-Übersicht")

with col2:
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/02_AI_Assistant.py")
    st.caption("Chat mit AI")

with col3:
    if st.button("🚀 Deploy", use_container_width=True):
        st.switch_page("pages/03_Deploy.py")
    st.caption("Ansible Deployments")

st.divider()

# ============================================================================
# SYSTEM STATUS (Quick Overview)
# ============================================================================

st.markdown("### 📊 System Status")

try:
    import psutil
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cpu_percent = psutil.cpu_percent(interval=1)
        delta_color = "normal" if cpu_percent < 70 else "inverse"
        st.metric(
            "💻 CPU",
            f"{cpu_percent}%",
            delta=None,
            delta_color=delta_color
        )
    
    with col2:
        mem = psutil.virtual_memory()
        delta_color = "normal" if mem.percent < 70 else "inverse"
        st.metric(
            "🧠 RAM",
            f"{mem.percent}%",
            delta=f"{mem.used / (1024**3):.1f} GB used",
            delta_color=delta_color
        )
    
    with col3:
        disk = psutil.disk_usage('/')
        delta_color = "normal" if disk.percent < 70 else "inverse"
        st.metric(
            "💾 Disk",
            f"{disk.percent}%",
            delta=f"{disk.free / (1024**3):.1f} GB free",
            delta_color=delta_color
        )

except ImportError:
    st.warning("⚠️ psutil nicht installiert. Führe `pip install psutil` aus.")

st.divider()

# ============================================================================
# QUICK TIPS
# ============================================================================

with st.expander("💡 Quick Tips & Shortcuts"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Navigation:**
        - 🏠 Home → Dashboard-Übersicht
        - 🤖 AI Assistant → Chat mit AI
        - 🚀 Deploy → Ansible-Deployments
        - 📊 Monitor → System-Monitoring
        - 🔧 Docker → Container-Management
        - 🎤 Voice Control → Sprachsteuerung
        """)
    
    with col2:
        st.markdown("""
        **Pro Tips:**
        - Nutze Quick Actions für häufige Tasks
        - Voice Control für schnelle Befehle
        - AI Assistant für Hilfe und Tipps
        - Monitor für System-Überwachung
        - Regelmäßige Backups nicht vergessen!
        """)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🎮 Navigation")
    
    st.page_link("pages/01_Home.py", label="🏠 Home Dashboard")
    st.page_link("pages/02_AI_Assistant.py", label="🤖 AI Assistant")
    st.page_link("pages/03_Deploy.py", label="🚀 Deployment")
    st.page_link("pages/04_Monitor.py", label="📊 Monitoring")
    st.page_link("pages/06_Docker.py", label="🔧 Docker Control")
    
    if secrets_manager.is_feature_enabled("voice_control_enabled"):
        st.page_link("pages/07_Voice_Control.py", label="🎤 Voice Control")
    
    st.divider()
    
    st.markdown("### ℹ️ Info")
    st.caption("Nova World v1.0")
    st.caption("🔐 Secured")
    
    if secrets_manager.is_feature_enabled("voice_control_enabled"):
        st.caption("🎤 Voice Enabled")
    
    if secrets_manager.is_feature_enabled("ai_assistant_enabled"):
        st.caption("🤖 AI Enabled")
    
    st.divider()
    
    st.caption(f"© {datetime.now().year} Nova-World")
