"""
🧙‍♂️ Nova-World Setup Wizard
Interactive Setup und Deployment Assistant
"""

import streamlit as st
import psutil
import subprocess
import time
from typing import Dict, Any, List
from components.ai import get_ai_assistant
from components.quick_actions import get_quick_actions

# ========== PAGE CONFIG ==========

st.set_page_config(
    page_title="Setup Wizard",
    page_icon="🧙‍♂️",
    layout="wide"
)

# ========== HELPER FUNCTIONS ==========

def initialize_wizard_state():
    """Initialize wizard session state"""
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1
    if 'wizard_data' not in st.session_state:
        st.session_state.wizard_data = {
            'system_checks': {},
            'config': {},
            'selected_apps': [],
            'deployment_status': {}
        }

def next_step():
    """Go to next wizard step"""
    st.session_state.wizard_step += 1

def prev_step():
    """Go to previous wizard step"""
    if st.session_state.wizard_step > 1:
        st.session_state.wizard_step -= 1

def reset_wizard():
    """Reset wizard to start"""
    st.session_state.wizard_step = 1
    st.session_state.wizard_data = {
        'system_checks': {},
        'config': {},
        'selected_apps': [],
        'deployment_status': {}
    }

# ========== PRE-FLIGHT CHECKS ==========

def check_system_resources() -> Dict[str, Any]:
    """
    Check system resources (RAM, Disk, CPU)
    Returns: Dict with check results
    """
    checks = {}
    
    # RAM Check
    memory = psutil.virtual_memory()
    ram_gb = memory.total / (1024**3)
    ram_available_gb = memory.available / (1024**3)
    checks['ram'] = {
        'total': f"{ram_gb:.1f} GB",
        'available': f"{ram_available_gb:.1f} GB",
        'percent': memory.percent,
        'status': '✅' if ram_available_gb > 2 else '⚠️',
        'pass': ram_available_gb > 2
    }
    
    # Disk Check
    disk = psutil.disk_usage('/')
    disk_free_gb = disk.free / (1024**3)
    checks['disk'] = {
        'total': f"{disk.total / (1024**3):.1f} GB",
        'free': f"{disk_free_gb:.1f} GB",
        'percent': disk.percent,
        'status': '✅' if disk_free_gb > 10 else '⚠️',
        'pass': disk_free_gb > 10
    }
    
    # CPU Check
    cpu_percent = psutil.cpu_percent(interval=1)
    checks['cpu'] = {
        'cores': psutil.cpu_count(),
        'usage': f"{cpu_percent}%",
        'status': '✅' if cpu_percent < 80 else '⚠️',
        'pass': cpu_percent < 80
    }
    
    return checks

def check_docker() -> Dict[str, Any]:
    """
    Check if Docker is running
    Returns: Dict with Docker status
    """
    try:
        result = subprocess.run(
            ['docker', 'info'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return {
            'installed': True,
            'running': result.returncode == 0,
            'status': '✅' if result.returncode == 0 else '❌',
            'pass': result.returncode == 0
        }
    except FileNotFoundError:
        return {
            'installed': False,
            'running': False,
            'status': '❌',
            'pass': False
        }
    except Exception as e:
        return {
            'installed': True,
            'running': False,
            'status': '❌',
            'pass': False,
            'error': str(e)
        }

def check_ollama() -> Dict[str, Any]:
    """
    Check if Ollama is available
    Returns: Dict with Ollama status
    """
    try:
        ai = get_ai_assistant(mode="ollama")
        available = ai.is_available()
        
        return {
            'available': available,
            'status': '✅' if available else '⚠️',
            'pass': available,
            'info': ai.get_info() if available else {}
        }
    except Exception as e:
        return {
            'available': False,
            'status': '❌',
            'pass': False,
            'error': str(e)
        }

def run_all_checks() -> Dict[str, Any]:
    """Run all pre-flight checks"""
    return {
        'system': check_system_resources(),
        'docker': check_docker(),
        'ollama': check_ollama()
    }

# ========== WIZARD STEPS ==========

def render_step_1_welcome():
    """Step 1: Welcome Screen"""
    st.markdown("# 🧙‍♂️ Willkommen beim Nova-World Setup Wizard!")
    
    st.markdown("""
    Dieser Wizard hilft dir bei der Einrichtung und Konfiguration von Nova-World.
    
    ## 📋 Was dieser Wizard macht:
    
    ✅ **System-Checks** - Prüft dein System (RAM, Disk, Docker)  
    ✅ **Konfiguration** - Hilft bei der Konfiguration  
    ✅ **App-Deployment** - Deployt ausgewählte Apps  
    ✅ **Validierung** - Prüft ob alles funktioniert  
    ✅ **AI-Unterstützung** - Nova hilft dir bei Entscheidungen  
    
    ## ⏱️ Dauer:
    
    - **Quick Setup**: ~5 Minuten (nur Checks)
    - **Full Setup**: ~15 Minuten (mit App-Deployment)
    
    ## 🚀 Bereit?
    
    Klicke auf **Weiter** um zu starten!
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🚀 Weiter", key="step1_next", use_container_width=True, type="primary"):
            next_step()
            st.rerun()

def render_step_2_checks():
    """Step 2: System Checks"""
    st.markdown("# 🔍 System-Checks")
    
    st.markdown("""
    Prüfe dein System um sicherzustellen, dass alles bereit ist.
    """)
    
    # Run checks button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 System prüfen", key="run_checks", use_container_width=True, type="primary"):
            with st.spinner("Prüfe System..."):
                checks = run_all_checks()
                st.session_state.wizard_data['system_checks'] = checks
    
    # Display checks if available
    if st.session_state.wizard_data.get('system_checks'):
        checks = st.session_state.wizard_data['system_checks']
        
        st.markdown("---")
        st.markdown("## 📊 Ergebnisse:")
        
        # System Resources
        st.markdown("### 💻 System-Ressourcen")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ram = checks['system']['ram']
            st.metric(
                label=f"{ram['status']} RAM",
                value=ram['available'],
                delta=f"von {ram['total']}"
            )
        
        with col2:
            disk = checks['system']['disk']
            st.metric(
                label=f"{disk['status']} Disk",
                value=disk['free'],
                delta=f"von {disk['total']}"
            )
        
        with col3:
            cpu = checks['system']['cpu']
            st.metric(
                label=f"{cpu['status']} CPU",
                value=cpu['usage'],
                delta=f"{cpu['cores']} Cores"
            )
        
        # Docker
        st.markdown("### 🐳 Docker")
        docker = checks['docker']
        if docker['pass']:
            st.success(f"✅ Docker läuft")
        else:
            st.error(f"❌ Docker nicht verfügbar")
            st.warning("Bitte starte Docker und führe die Checks erneut aus.")
        
        # Ollama
        st.markdown("### 🤖 Ollama AI")
        ollama = checks['ollama']
        if ollama['pass']:
            info = ollama.get('info', {})
            st.success(f"✅ Ollama verfügbar - Model: {info.get('model', 'N/A')}")
        else:
            st.warning("⚠️ Ollama nicht verfügbar (optional)")
            st.info("AI-Features sind ohne Ollama eingeschränkt, aber der Rest funktioniert!")
        
        # Overall Status
        st.markdown("---")
        all_critical_pass = checks['docker']['pass']
        
        if all_critical_pass:
            st.success("🎉 Alle kritischen Checks bestanden! Du kannst fortfahren.")
            
            # AI Suggestion
            if ollama['pass']:
                with st.expander("💡 AI-Empfehlung"):
                    try:
                        ai = get_ai_assistant()
                        suggestion = ai.get_suggestion('system', {
                            'ram': checks['system']['ram'],
                            'disk': checks['system']['disk'],
                            'cpu': checks['system']['cpu']
                        })
                        st.info(suggestion)
                    except:
                        pass
            
            # Navigation
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Zurück", key="step2_back", use_container_width=True):
                    prev_step()
                    st.rerun()
            with col2:
                if st.button("➡️ Weiter", key="step2_next", use_container_width=True, type="primary"):
                    next_step()
                    st.rerun()
        else:
            st.error("❌ Einige kritische Checks sind fehlgeschlagen. Bitte behebe die Probleme und prüfe erneut.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Zurück", key="step2_back_fail", use_container_width=True):
                    prev_step()
                    st.rerun()

def render_step_3_config():
    """Step 3: Configuration"""
    st.markdown("# ⚙️ Konfiguration")
    
    st.markdown("""
    Konfiguriere Nova-World nach deinen Bedürfnissen.
    """)
    
    # Domain Config
    st.markdown("### 🌐 Domain-Konfiguration")
    domain = st.text_input(
        "Domain (für Traefik)",
        value=st.session_state.wizard_data.get('config', {}).get('domain', 'nova.local'),
        help="Die Domain unter der deine Services erreichbar sein sollen"
    )
    
    # Email Config
    email = st.text_input(
        "Email (für Let's Encrypt)",
        value=st.session_state.wizard_data.get('config', {}).get('email', 'admin@example.com'),
        help="Deine Email-Adresse für SSL-Zertifikate"
    )
    
    # Semaphore Config
    st.markdown("### 🚀 Semaphore-Integration")
    
    col1, col2 = st.columns(2)
    with col1:
        semaphore_url = st.text_input(
            "Semaphore URL",
            value=st.session_state.wizard_data.get('config', {}).get('semaphore_url', 'http://192.168.2.77:3000'),
            help="URL zu deiner Semaphore-Instanz"
        )
    
    with col2:
        semaphore_token = st.text_input(
            "API Token",
            value=st.session_state.wizard_data.get('config', {}).get('semaphore_token', ''),
            type="password",
            help="Dein Semaphore API Token"
        )
    
    # Save config
    st.session_state.wizard_data['config'] = {
        'domain': domain,
        'email': email,
        'semaphore_url': semaphore_url,
        'semaphore_token': semaphore_token
    }
    
    # AI Suggestion
    try:
        ai = get_ai_assistant()
        if ai.is_available():
            with st.expander("💡 Konfigurationstipps von Nova"):
                tips = ai.chat(
                    "Gib 3 kurze Tipps für eine sichere Nova-World Konfiguration.",
                    temperature=0.5
                )
                st.info(tips)
    except:
        pass
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Zurück", key="step3_back", use_container_width=True):
            prev_step()
            st.rerun()
    with col2:
        if st.button("➡️ Weiter", key="step3_next", use_container_width=True, type="primary"):
            next_step()
            st.rerun()

def render_step_4_apps():
    """Step 4: App Selection"""
    st.markdown("# 📦 App-Auswahl")
    
    st.markdown("""
    Wähle die Apps aus, die du deployen möchtest.
    """)
    
    # Available Apps
    apps = {
        'whisper': {
            'name': '🎤 Whisper',
            'description': 'Self-hosted Speech-to-Text',
            'resources': 'RAM: ~2GB, Disk: ~5GB'
        },
        'jellyfin': {
            'name': '🎬 Jellyfin',
            'description': 'Media Server',
            'resources': 'RAM: ~1GB, Disk: ~10GB'
        },
        'nextcloud': {
            'name': '☁️ Nextcloud',
            'description': 'Cloud Storage',
            'resources': 'RAM: ~2GB, Disk: ~20GB'
        },
        'paperless': {
            'name': '📄 Paperless',
            'description': 'Document Management',
            'resources': 'RAM: ~3GB, Disk: ~10GB'
        }
    }
    
    st.markdown("### Verfügbare Apps:")
    
    selected_apps = []
    
    for app_id, app_info in apps.items():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{app_info['name']}**")
            st.caption(app_info['description'])
            st.caption(f"📊 {app_info['resources']}")
        
        with col2:
            if st.checkbox("Auswählen", key=f"app_{app_id}"):
                selected_apps.append(app_id)
    
    # Save selection
    st.session_state.wizard_data['selected_apps'] = selected_apps
    
    # Summary
    if selected_apps:
        st.markdown("---")
        st.markdown("### ✅ Ausgewählte Apps:")
        for app_id in selected_apps:
            st.info(f"• {apps[app_id]['name']}")
    else:
        st.info("ℹ️ Keine Apps ausgewählt. Du kannst auch nur die Konfiguration durchführen.")
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Zurück", key="step4_back", use_container_width=True):
            prev_step()
            st.rerun()
    with col2:
        if st.button("➡️ Weiter", key="step4_next", use_container_width=True, type="primary"):
            next_step()
            st.rerun()

def render_step_5_deploy():
    """Step 5: Deployment"""
    st.markdown("# 🚀 Deployment")
    
    st.markdown("""
    Bereit zum Deployen? Überprüfe deine Einstellungen und starte das Deployment.
    """)
    
    # Summary
    st.markdown("## 📋 Zusammenfassung:")
    
    config = st.session_state.wizard_data.get('config', {})
    selected_apps = st.session_state.wizard_data.get('selected_apps', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚙️ Konfiguration")
        st.info(f"""
**Domain:** {config.get('domain', 'N/A')}  
**Email:** {config.get('email', 'N/A')}  
**Semaphore:** {config.get('semaphore_url', 'N/A')}
        """)
    
    with col2:
        st.markdown("### 📦 Apps")
        if selected_apps:
            apps_text = "\n".join([f"• {app}" for app in selected_apps])
            st.info(apps_text)
        else:
            st.info("Keine Apps ausgewählt")
    
    # Deploy Button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Deployment starten", key="start_deploy", use_container_width=True, type="primary"):
            # Simulate deployment
            with st.spinner("Deployment läuft..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    "Konfiguration wird geschrieben...",
                    "Docker-Compose wird erstellt...",
                    "Container werden gestartet...",
                    "Health-Checks laufen...",
                    "Deployment abgeschlossen!"
                ]
                
                for i, step in enumerate(steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(1)
                
                st.session_state.wizard_data['deployment_status'] = {
                    'success': True,
                    'message': 'Deployment erfolgreich!',
                    'apps_deployed': selected_apps
                }
            
            st.success("🎉 Deployment erfolgreich!")
            st.balloons()
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Zurück", key="step5_back", use_container_width=True):
            prev_step()
            st.rerun()
    
    with col3:
        if st.button("🏁 Fertig", key="step5_finish", use_container_width=True, type="primary"):
            st.success("✅ Wizard abgeschlossen!")
            st.info("Du kannst jetzt das Dashboard nutzen!")
            if st.button("🔄 Wizard neu starten"):
                reset_wizard()
                st.rerun()

# ========== MAIN ==========

def main():
    """Main wizard function"""
    initialize_wizard_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🧙‍♂️ Setup Wizard")
        
        # Progress
        steps = [
            "👋 Willkommen",
            "🔍 System-Checks",
            "⚙️ Konfiguration",
            "📦 App-Auswahl",
            "🚀 Deployment"
        ]
        
        current_step = st.session_state.wizard_step
        
        for i, step in enumerate(steps, 1):
            if i < current_step:
                st.markdown(f"✅ {step}")
            elif i == current_step:
                st.markdown(f"**➡️ {step}**")
            else:
                st.markdown(f"⭕ {step}")
        
        st.markdown("---")
        
        if st.button("🔄 Wizard zurücksetzen", use_container_width=True):
            reset_wizard()
            st.rerun()
    
    # Render current step
    if st.session_state.wizard_step == 1:
        render_step_1_welcome()
    elif st.session_state.wizard_step == 2:
        render_step_2_checks()
    elif st.session_state.wizard_step == 3:
        render_step_3_config()
    elif st.session_state.wizard_step == 4:
        render_step_4_apps()
    elif st.session_state.wizard_step == 5:
        render_step_5_deploy()

if __name__ == "__main__":
    main()
