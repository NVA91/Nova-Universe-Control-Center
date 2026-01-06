# Semaphore Quickstart: In 10 Minuten zur Web-UI

## 🎯 Ziel

In diesem Guide richten Sie **Ansible Semaphore** ein und führen Ihr erstes Playbook über die Web-UI aus.

## ⏱️ Zeitaufwand

**10-15 Minuten**

## 📋 Voraussetzungen

- ✅ Docker und Docker Compose installiert
- ✅ Unified Ansible Project entpackt
- ✅ Grundlegendes Verständnis von Ansible

## 🚀 Schritt-für-Schritt-Anleitung

### Schritt 1: Setup ausführen (2 Minuten)

```bash
cd unified-ansible-project
make semaphore-setup
```

**Was passiert:**
- Prüft Docker und Docker Compose
- Erstellt `.env.semaphore` (falls nicht vorhanden)
- Generiert sicheres Access Key
- Erstellt SSH-Keys
- Startet Semaphore-Container

**Erwartete Ausgabe:**
```
╔════════════════════════════════════════════════════════════════╗
║  Semaphore erfolgreich gestartet!                             ║
╚════════════════════════════════════════════════════════════════╝

✅ URL: http://localhost:3000
✅ Benutzername: admin
✅ Passwort: changeme
```

### Schritt 2: Anmelden (1 Minute)

1. Öffnen Sie **http://localhost:3000** im Browser
2. Loggen Sie sich ein:
   - **Username**: `admin`
   - **Password**: `changeme` (oder Ihr Passwort aus `.env.semaphore`)

3. **WICHTIG**: Ändern Sie sofort das Passwort!
   - Klicken Sie oben rechts auf **Admin**
   - Wählen Sie **"Edit Profile"**
   - Ändern Sie das Passwort
   - Klicken Sie auf **"Save"**

### Schritt 3: Projekt erstellen (1 Minute)

1. Klicken Sie auf **"New Project"**
2. Geben Sie ein:
   - **Name**: `Unified Ansible Project`
   - **Alert**: Leer lassen (optional)
3. Klicken Sie auf **"Create"**

### Schritt 4: SSH-Key hinzufügen (2 Minuten)

1. Gehen Sie zu **"Key Store"** (linkes Menü)
2. Klicken Sie auf **"New Key"**
3. Konfiguration:
   - **Name**: `Proxmox SSH Key`
   - **Type**: **"SSH Key"**
   - **Private Key**: Fügen Sie Ihren SSH-Key ein

**SSH-Key abrufen:**
```bash
cat .ssh/id_ed25519
```

4. Klicken Sie auf **"Create"**

### Schritt 5: Inventory hinzufügen (2 Minuten)

1. Gehen Sie zu **"Inventory"** (linkes Menü)
2. Klicken Sie auf **"New Inventory"**
3. Konfiguration:
   - **Name**: `Proxmox Production`
   - **Type**: **"File"**
   - **Inventory**: `/ansible/infrastructure/inventory/hosts.yml`
   - **SSH Key**: `Proxmox SSH Key`
   - **Sudo**: Aktivieren (falls benötigt)
   - **Become Method**: `sudo` (falls benötigt)

4. Klicken Sie auf **"Create"**

### Schritt 6: Environment erstellen (1 Minute)

1. Gehen Sie zu **"Environment"** (linkes Menü)
2. Klicken Sie auf **"New Environment"**
3. Konfiguration:
   - **Name**: `Production`
   - **Extra Variables**: Leer lassen (oder JSON-Format)
   - **Environment Variables**:

```json
{
  "ANSIBLE_HOST_KEY_CHECKING": "False",
  "ANSIBLE_FORCE_COLOR": "True"
}
```

4. Klicken Sie auf **"Create"**

### Schritt 7: Task Template erstellen (3 Minuten)

1. Gehen Sie zu **"Task Templates"** (linkes Menü)
2. Klicken Sie auf **"New Template"**
3. Konfiguration:
   - **Name**: `Deploy Standard Profile`
   - **Playbook Filename**: `/ansible/infrastructure/site.yml`
   - **Inventory**: `Proxmox Production`
   - **Repository**: Leer lassen (lokale Playbooks)
   - **Environment**: `Production`
   - **Vault Password**: Leer lassen (oder erstellen)
   - **Extra CLI Arguments**: `-e "@/ansible/infrastructure/config/profile_standard.yml"`
   - **Allow CLI Args in Task**: Aktivieren (optional)

4. Klicken Sie auf **"Create"**

### Schritt 8: Erstes Playbook ausführen (2 Minuten)

1. Gehen Sie zu **"Task Templates"**
2. Wählen Sie `Deploy Standard Profile`
3. Klicken Sie auf **"Run"**
4. Optional: Bestätigen Sie die Ausführung
5. **Verfolgen Sie die Logs in Echtzeit!** 🎉

**Erwartete Ausgabe:**
- Echtzeit-Logs des Playbook-Laufs
- Farbige Ausgabe
- Status-Updates
- Erfolgs- oder Fehlermeldungen

## ✅ Fertig!

Sie haben jetzt:
- ✅ Semaphore installiert und konfiguriert
- ✅ Projekt, Inventory und Keys eingerichtet
- ✅ Ihr erstes Playbook über die Web-UI ausgeführt

## 🎯 Nächste Schritte

### Weitere Task Templates erstellen

Erstellen Sie Templates für andere Profile:

**Minimal Profile:**
```
Name: Deploy Minimal Profile
Playbook: /ansible/infrastructure/site.yml
Extra Args: -e "@/ansible/infrastructure/config/profile_minimal.yml"
```

**Full Profile:**
```
Name: Deploy Full Profile
Playbook: /ansible/infrastructure/site.yml
Extra Args: -e "@/ansible/infrastructure/config/profile_full.yml"
```

**Custom Profile:**
```
Name: Deploy Custom Profile
Playbook: /ansible/infrastructure/site.yml
Extra Args: -e "@/ansible/infrastructure/config/profile_custom.yml"
```

### Scheduled Tasks einrichten

1. Öffnen Sie ein Task Template
2. Klicken Sie auf **"Schedules"**
3. Klicken Sie auf **"New Schedule"**
4. Cron Expression: `0 2 * * *` (täglich um 2 Uhr)
5. Klicken Sie auf **"Create"**

### Benutzer hinzufügen

1. Gehen Sie zu **"Team"**
2. Klicken Sie auf **"New User"**
3. Geben Sie Username und Passwort ein
4. Wählen Sie Rolle (Owner, Manager, Task Runner, Guest)
5. Klicken Sie auf **"Create"**

## 🛠️ Nützliche Kommandos

```bash
# Semaphore starten
make semaphore-start

# Semaphore stoppen
make semaphore-stop

# Logs anzeigen
make semaphore-logs

# Backup erstellen
make semaphore-backup

# Semaphore neu starten
docker-compose -f docker-compose.semaphore.yml restart
```

## 🔍 Troubleshooting

### Problem: Semaphore startet nicht

**Lösung:**
```bash
# Logs prüfen
make semaphore-logs

# Container-Status prüfen
docker-compose -f docker-compose.semaphore.yml ps

# Neu starten
make semaphore-stop
make semaphore-start
```

### Problem: SSH-Verbindung schlägt fehl

**Lösung:**
1. Prüfen Sie SSH-Key in Key Store
2. Testen Sie SSH-Verbindung manuell:
   ```bash
   ssh -i .ssh/id_ed25519 user@proxmox-host
   ```
3. Prüfen Sie `ansible_user` im Inventory

### Problem: Playbook nicht gefunden

**Lösung:**
1. Prüfen Sie Pfad in Task Template (muss mit `/ansible` beginnen)
2. Prüfen Sie Volume-Mount:
   ```bash
   docker-compose -f docker-compose.semaphore.yml exec semaphore ls -la /ansible
   ```

## 📚 Weiterführende Dokumentation

- **Vollständige Konfiguration**: [SEMAPHORE_CONFIG.md](SEMAPHORE_CONFIG.md)
- **Architektur**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Testing**: [TESTING.md](TESTING.md)
- **Troubleshooting**: [TROUBLESHOOT.md](TROUBLESHOOT.md)

## 💡 Tipps

1. **Dry-Run**: Verwenden Sie `--check` in Extra Args für Dry-Runs
2. **Verbosity**: Fügen Sie `-vvv` für detaillierte Logs hinzu
3. **Tags**: Nutzen Sie `--tags` für selektive Ausführung
4. **Limit**: Verwenden Sie `--limit` für spezifische Hosts
5. **Notifications**: Richten Sie Slack/Email-Benachrichtigungen ein

---

**Viel Erfolg mit Semaphore! 🚀**

Bei Fragen: Siehe [SEMAPHORE_CONFIG.md](SEMAPHORE_CONFIG.md) oder [TROUBLESHOOT.md](TROUBLESHOOT.md)
