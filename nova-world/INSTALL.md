# 🎭 Semaphore API Integration - Installation

**Update-Paket für Unified Ansible Project**

---

## 📦 Was ist enthalten?

Dieses Update fügt **vollständige Semaphore REST API Integration** hinzu:
- Full REST API Client
- Quick Actions mit Semaphore-Jobs
- Enhanced Deploy Page
- Live Task Monitoring
- Job History Viewer

---

## 🚀 Schnell-Installation (5 Minuten)

### 1. Paket entpacken

```bash
unzip semaphore-api-integration-v1.0.zip -d /tmp/semaphore-api-update
```

### 2. Semaphore API Token generieren

1. Öffne Semaphore: http://localhost:3000
2. Login mit deinem Account
3. Gehe zu **User Settings** (Profil-Icon oben rechts)
4. Klicke **API Tokens**
5. Klicke **Create Token**
6. Gib einen Namen ein (z.B. "Nova-World")
7. Klicke **Create**
8. **Kopiere den Token** (wird nur einmal angezeigt!)

### 3. Konfiguration

Erstelle/erweitere `~/unified-ansible-project/nova-world/.streamlit/secrets.toml`:

```toml
[semaphore]
url = "http://localhost:3000"
api_token = "DEIN-API-TOKEN-HIER"
project_id = 1
```

**Wichtig**: 
- Ersetze `DEIN-API-TOKEN-HIER` mit dem kopierten Token
- `project_id` ist die ID deines Hauptprojekts (meist 1)

### 4. Dateien kopieren

```bash
cd /tmp/semaphore-api-update

# API Client
cp nova-world/components/semaphore_api.py \
    ~/unified-ansible-project/nova-world/components/

# Quick Actions Extension
cp nova-world/components/quick_actions_semaphore.py \
    ~/unified-ansible-project/nova-world/components/

# Updated Deploy Page
cp nova-world/pages/03_🚀_Deploy_UPDATED.py \
    ~/unified-ansible-project/nova-world/pages/03_🚀_Deploy.py
```

### 5. Nova-World neu starten

```bash
cd ~/unified-ansible-project/nova-world

# Stoppe laufende Instanz (Ctrl+C)

# Starte neu
streamlit run nova_universe.py
```

### 6. Verifizieren

1. Öffne Nova-World: http://localhost:8501
2. Gehe zu **🚀 Deploy** Page
3. Siehe **📊 Deployment Status** (sollte Daten zeigen)
4. Teste **⚡ Quick Deploy** Button

---

## ✅ Testen

### Test 1: Connection

```bash
cd ~/unified-ansible-project/nova-world

python3 << EOF
from components.semaphore_api import create_semaphore_client

client = create_semaphore_client()

if client.ping():
    print("✅ Semaphore is reachable")
else:
    print("❌ Cannot connect to Semaphore")
EOF
```

**Erwartete Ausgabe**: `✅ Semaphore is reachable`

### Test 2: Get Projects

```bash
python3 << EOF
from components.semaphore_api import create_semaphore_client

client = create_semaphore_client()
projects = client.get_projects()

print(f"Found {len(projects)} projects:")
for p in projects:
    print(f"  - {p['name']} (ID: {p['id']})")
EOF
```

### Test 3: Get Templates

```bash
python3 << EOF
from components.semaphore_api import create_semaphore_client

client = create_semaphore_client()
templates = client.get_templates(1)  # Project ID 1

print(f"Found {len(templates)} templates:")
for t in templates:
    print(f"  - {t['name']} (ID: {t['id']})")
EOF
```

### Test 4: Nova-World UI

1. Öffne http://localhost:8501
2. Gehe zu **🚀 Deploy**
3. Prüfe **📊 Deployment Status** (zeigt Metriken)
4. Prüfe **⚡ Quick Deploy** (zeigt Buttons)
5. Prüfe **📋 Task Templates** (zeigt Templates)
6. Prüfe **📜 Task History** (zeigt Historie)

---

## 🐛 Troubleshooting

### Problem: "Semaphore API not configured"

**Lösung**:
1. Prüfe `secrets.toml`:
   ```bash
   cat ~/unified-ansible-project/nova-world/.streamlit/secrets.toml
   ```

2. Stelle sicher, dass `[semaphore]` Sektion existiert
3. Stelle sicher, dass `api_token` gesetzt ist

### Problem: "Cannot connect to Semaphore"

**Lösung**:
1. Prüfe ob Semaphore läuft:
   ```bash
   curl http://localhost:3000/api/ping
   ```

2. Prüfe URL in secrets.toml:
   ```toml
   [semaphore]
   url = "http://localhost:3000"  # Korrekt?
   ```

3. Prüfe Docker:
   ```bash
   docker ps | grep semaphore
   ```

### Problem: "Unauthorized: Invalid API token"

**Lösung**:
1. Generiere neuen Token in Semaphore
2. Kopiere Token exakt (keine Leerzeichen)
3. Update secrets.toml
4. Restart Nova-World

### Problem: "Template not found"

**Lösung**:
1. Liste verfügbare Templates:
   ```bash
   python3 << EOF
   from components.semaphore_api import create_semaphore_client
   client = create_semaphore_client()
   templates = client.get_templates(1)
   for t in templates:
       print(t['name'])
   EOF
   ```

2. Update Template-Namen in `quick_actions_semaphore.py`:
   ```python
   {
       "template_name": "Dein Actual Template Name"
   }
   ```

---

## 📚 Dokumentation

Vollständige Dokumentation:
- `docs/SEMAPHORE_API_GUIDE.md` - API Guide
- `CHANGELOG.md` - Änderungen

---

## 🔄 Deinstallation

```bash
# Entferne Dateien
rm ~/unified-ansible-project/nova-world/components/semaphore_api.py
rm ~/unified-ansible-project/nova-world/components/quick_actions_semaphore.py

# Restore alte Deploy Page (falls Backup existiert)
# cp ~/unified-ansible-project/nova-world/pages/03_🚀_Deploy.py.backup \
#    ~/unified-ansible-project/nova-world/pages/03_🚀_Deploy.py

# Entferne Semaphore-Config aus secrets.toml
# (manuell editieren)
```

---

## 💡 Nächste Schritte

Nach erfolgreicher Installation:

1. **Explore Deploy Page**:
   - Deployment Status Dashboard
   - Quick Deploy Buttons
   - Task History
   - Live Monitoring

2. **Create Task Templates** in Semaphore:
   - Deploy Minimal Profile
   - Deploy Standard Profile
   - Deploy Full Profile
   - Health Check
   - Backup

3. **Test Deployments**:
   - Klicke Quick Deploy Button
   - Verfolge Task-Status
   - Siehe Logs

4. **Automate Workflows**:
   - Morning Routine mit Semaphore
   - Scheduled Deployments
   - Backup Automation

---

**🎭 Installation abgeschlossen!**

*Full REST API Control für Ihre Deployments!* 🚀
