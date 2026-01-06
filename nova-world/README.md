# 🪐 Nova-World Dashboard

**Custom Web-UI für Unified Ansible Project**

Nova-World ist ein modernes, Streamlit-basiertes Dashboard für die Verwaltung von Docker-Containern, Ansible-Deployments und System-Monitoring.

---

## ✨ Features

### 🏠 Dashboard
- **System-Übersicht**: CPU, RAM, Disk, Docker-Status
- **Quick Actions**: One-Click-Buttons für häufige Tasks
- **Recent Activity**: Container-Events und Deployment-Status

### ⚡ Quick Actions
- **Docker Control**: Start/Stop/Restart/Cleanup
- **Semaphore Deployments**: Deploy Minimal/Standard/Full
- **System Operations**: Health Check/Logs/Uptime
- **Composite Actions**: Morning Routine, Emergency Stop

### 🎤 Voice Control
- **Whisper STT**: Speech-to-Text mit OpenAI Whisper
- **Intent Recognition**: GPT-4-basierte Command-Erkennung
- **Safety Confirmations**: Bestätigung für gefährliche Aktionen
- **Command History**: Verlauf aller Voice Commands

### 🤖 AI Assistant
- **Context-Aware**: Kennt deinen System-Status
- **Smart Suggestions**: Schlägt passende Quick Actions vor
- **Error Analysis**: Analysiert Logs und gibt Tipps
- **GPT-4 Powered**: Intelligente Konversationen

### 🚀 Deployment Control
- **Profile Management**: Minimal, Standard, Full
- **Semaphore Integration**: Ansible-Deployments triggern
- **Deployment History**: Job-Verlauf (geplant)

### 📊 System Monitoring
- **Real-time Metrics**: CPU, RAM, Disk, Network
- **Docker Monitoring**: Container-Status und Details
- **Alerts & Warnings**: Automatische Warnungen
- **Error Logs**: Fehlersuche in Container-Logs

### 🔧 Docker Management
- **Container List**: Alle Container mit Status
- **Individual Control**: Start/Stop/Restart pro Container
- **Logs Viewer**: Container-Logs anzeigen
- **Bulk Operations**: Alle Container gleichzeitig steuern

---

## 🚀 Quick Start

### 1. Installation

```bash
cd unified-ansible-project/nova-world

# Setup ausführen (einmalig)
python3 setup.py

# Oder manuell:
pip3 install -r requirements.txt
```

### 2. Konfiguration

```bash
# Secrets konfigurieren
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
nano .streamlit/secrets.toml
```

**Wichtig**: Füge deinen OpenAI API Key ein!

```toml
[openai]
api_key = "sk-..."  # Dein OpenAI API Key
```

### 3. Starten

```bash
streamlit run nova_universe.py
```

**Dashboard öffnet sich automatisch auf**: http://localhost:8501

---

## 📋 Voraussetzungen

### System
- **Python**: 3.11+
- **Docker**: Für Container-Management
- **Semaphore**: Optional, für Deployments

### Python Packages
- `streamlit>=1.30.0`
- `audio-recorder-streamlit>=0.0.8`
- `openai>=1.0.0`
- `docker>=7.0.0`
- `requests>=2.31.0`
- `psutil>=5.9.0`
- `plotly>=5.18.0`

Siehe `requirements.txt` für vollständige Liste.

### API Keys
- **OpenAI API Key**: Für Voice Control und AI Assistant
  - Registrierung: https://platform.openai.com/

---

## 🎮 Verwendung

### Dashboard Navigation

**Hauptseiten**:
- 🏠 **Home**: Dashboard-Übersicht
- 🤖 **AI Assistant**: Chat mit AI
- 🚀 **Deploy**: Ansible-Deployments
- 📊 **Monitor**: System-Monitoring
- 🔧 **Docker**: Container-Management
- 🎤 **Voice Control**: Sprachsteuerung

### Quick Actions

**Docker**:
```
▶️ Start All     → Startet alle gestoppten Container
⏹️ Stop All      → Stoppt alle Container (VORSICHT!)
🔄 Restart All   → Neustart aller Container
🧹 Cleanup       → Docker aufräumen
```

**Deployments**:
```
📦 Deploy Minimal   → Minimal Profile
📦 Deploy Standard  → Standard Profile
📦 Deploy Full      → Full Profile
```

**System**:
```
🏥 Health Check     → System-Status prüfen
📜 Recent Errors    → Fehler in Logs suchen
⏱️ Uptime           → System-Laufzeit
```

**Composite**:
```
🌅 Morning Routine  → Startup-Routine (Start + Health Check)
🚨 Emergency Stop   → Notfall-Stop (Stoppt alles)
```

### Voice Commands

**Beispiele**:
```
"Start all"          → Startet alle Container
"Deploy Standard"    → Standard Deployment
"Health Check"       → System-Status prüfen
"Morning Routine"    → Startup-Routine
```

**Verfügbare Commands**:
- Docker: start all, stop all, restart all, cleanup, status
- Deployments: deploy minimal, deploy standard, deploy full
- System: health check, uptime, errors
- Composite: morning routine, emergency stop

### AI Assistant

**Beispiel-Fragen**:
```
"Was läuft gerade auf meinem System?"
"Warum ist mein Container gestoppt?"
"Wie deploye ich das Standard-Profil?"
"Was bedeutet dieser Fehler in den Logs?"
"Führe einen Health Check durch"
```

---

## 🔐 Sicherheit

### Secrets Management

**Secrets werden gespeichert in**: `.streamlit/secrets.toml`

**Wichtig**:
- Diese Datei ist in `.gitignore`
- NIEMALS in Git committen!
- Nur lokale Verwendung

### Confirmation Flows

**Gefährliche Aktionen** erfordern Bestätigung:
- Docker Stop All
- Emergency Stop
- Container-Löschung (geplant)

### API Keys

**OpenAI API Key**:
- Wird nur für Voice Control und AI Assistant verwendet
- Keine Speicherung außerhalb von `secrets.toml`
- Übertragung über HTTPS

---

## 🛠️ Entwicklung

### Projektstruktur

```
nova-world/
├── nova_universe.py           # Main App
├── components/
│   ├── quick_actions.py       # Quick Actions System
│   ├── voice_commander.py     # Voice Command Processing
│   ├── whisper_integration.py # Whisper STT
│   ├── ai_assistant.py        # AI Chat Assistant
│   ├── secrets_manager.py     # Secrets Management
│   └── ui_components.py       # UI Components
├── pages/
│   ├── 01_🏠_Home.py          # Dashboard Home
│   ├── 02_🤖_AI_Assistant.py  # AI Chat
│   ├── 03_🚀_Deploy.py        # Deployment Control
│   ├── 04_📊_Monitor.py       # System Monitoring
│   ├── 06_🔧_Docker.py        # Docker Management
│   └── 🎤_Voice_Control.py    # Voice Control Center
├── .streamlit/
│   ├── config.toml            # Streamlit Config
│   └── secrets.toml           # API Keys (gitignored)
├── requirements.txt           # Python Dependencies
├── setup.py                   # Setup Script
└── README.md                  # Diese Datei
```

### Komponenten erweitern

**Neue Quick Action hinzufügen**:

1. In `components/quick_actions.py`:
```python
def my_new_action(self) -> Dict:
    """Beschreibung"""
    try:
        # Implementation
        return {"success": True, "message": "Erfolgreich!"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

2. In `components/ui_components.py`:
```python
if st.button("🎯 My Action", ...):
    result = qa.my_new_action()
    _display_action_result(result)
```

3. In `components/voice_commander.py`:
```python
r"my.*action|neue.*aktion":
    ("my_new_action", self.qa.my_new_action),
```

---

## 📊 Monitoring

### System Metrics

**Überwacht**:
- CPU Usage (%)
- RAM Usage (%)
- Disk Usage (%)
- Network I/O
- Docker Container Status

**Alerts**:
- 🟢 Normal: < 70%
- 🟡 Warning: 70-90%
- 🔴 Critical: > 90%

### Docker Monitoring

**Überwacht**:
- Running Containers
- Stopped Containers
- Container Logs
- Recent Errors

---

## 🐛 Troubleshooting

### Dashboard startet nicht

**Problem**: `streamlit: command not found`

**Lösung**:
```bash
pip3 install streamlit
# Oder
python3 -m pip install streamlit
```

### Voice Control funktioniert nicht

**Problem**: `audio-recorder-streamlit` nicht installiert

**Lösung**:
```bash
pip3 install audio-recorder-streamlit
```

**Problem**: OpenAI API Key fehlt

**Lösung**:
```bash
nano .streamlit/secrets.toml
# Füge api_key hinzu
```

### Docker-Befehle funktionieren nicht

**Problem**: Docker nicht installiert oder nicht gestartet

**Lösung**:
```bash
# Docker starten
sudo systemctl start docker

# Docker-Status prüfen
docker ps
```

### Semaphore nicht erreichbar

**Problem**: Semaphore läuft nicht

**Lösung**:
```bash
cd unified-ansible-project
make semaphore-start
```

---

## 🔮 Roadmap

### Geplante Features

**Phase 1** (Aktuell):
- ✅ Quick Actions System
- ✅ Voice Control
- ✅ AI Assistant
- ✅ Dashboard Pages

**Phase 2** (Nächste):
- 🔜 Self-Hosted Whisper (auf vm-ai-lab)
- 🔜 Text-to-Speech (Voice Output)
- 🔜 Semaphore API vollständige Integration
- 🔜 Deployment-Historie

**Phase 3** (Zukunft):
- 🔮 Passkey Authentication (YubiKey, Face ID)
- 🔮 Multi-User Support
- 🔮 Notifications (Slack, Email, Push)
- 🔮 Grafana Integration
- 🔮 Backup Automation

---

## 📚 Ressourcen

### Dokumentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Docker SDK Docs](https://docker-py.readthedocs.io/)

### Support
- **Issues**: GitHub Issues (wenn Repository öffentlich)
- **Fragen**: AI Assistant im Dashboard nutzen!

---

## 📄 Lizenz

Siehe Haupt-Repository für Lizenz-Informationen.

---

## 🙏 Credits

**Entwickelt mit**:
- Streamlit
- OpenAI (Whisper, GPT-4)
- Docker SDK
- psutil

**Inspiriert von**:
- Iron Man's JARVIS 🦾
- DevOps Best Practices
- KISS-Prinzip

---

**🪐 Nova-World - Your DevOps Command Center**

*Built with ❤️ for efficient DevOps workflows*
