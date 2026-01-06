# Semaphore Konfigurationsanleitung

## Übersicht

Dieses Dokument beschreibt die Konfiguration von **Ansible Semaphore** für das Unified Ansible Project.

## Was ist Semaphore?

**Ansible Semaphore** ist eine moderne, open-source Web-UI für Ansible, die es ermöglicht:
- Playbooks über eine grafische Oberfläche auszuführen
- Inventories zu verwalten
- Job-Historie einzusehen
- Scheduled Tasks zu erstellen
- Multi-User-Zugriff mit Rollen

## Installation

### Voraussetzungen

- Docker und Docker Compose installiert
- Unified Ansible Project entpackt

### Setup

```bash
# 1. In Projektverzeichnis wechseln
cd unified-ansible-project

# 2. Setup-Skript ausführen
./scripts/setup_semaphore.sh
```

Das Skript führt automatisch folgende Schritte aus:
1. Prüft Voraussetzungen (Docker, Docker Compose)
2. Erstellt `.env.semaphore` (falls nicht vorhanden)
3. Generiert sicheres Access Key
4. Erstellt SSH-Keys (falls nicht vorhanden)
5. Startet Semaphore-Container
6. Zeigt Zugriffsinformationen an

### Manuelles Setup

Falls Sie das Setup manuell durchführen möchten:

```bash
# 1. Umgebungsvariablen konfigurieren
cp .env.semaphore .env.semaphore.local
nano .env.semaphore.local

# 2. Docker Compose starten
docker-compose -f docker-compose.semaphore.yml --env-file .env.semaphore.local up -d

# 3. Logs prüfen
docker-compose -f docker-compose.semaphore.yml logs -f
```

## Zugriff

Nach erfolgreichem Setup:

**URL**: http://localhost:3000  
**Benutzername**: admin (oder wie in `.env.semaphore` konfiguriert)  
**Passwort**: changeme (oder wie in `.env.semaphore` konfiguriert)

⚠️ **WICHTIG**: Ändern Sie das Admin-Passwort nach dem ersten Login!

## Erste Schritte in Semaphore

### 1. Projekt erstellen

Nach dem Login:

1. Klicken Sie auf **"New Project"**
2. Geben Sie einen Namen ein: `Unified Ansible Project`
3. Optional: Beschreibung hinzufügen
4. Klicken Sie auf **"Create"**

### 2. Key Store hinzufügen

Für SSH-Zugriff auf Ihre Server:

1. Gehen Sie zu **"Key Store"** im Projekt
2. Klicken Sie auf **"New Key"**
3. Wählen Sie **"SSH Key"**
4. Name: `Proxmox SSH Key`
5. Fügen Sie Ihren privaten SSH-Key ein (`.ssh/id_ed25519`)
6. Optional: Passphrase eingeben
7. Klicken Sie auf **"Create"**

### 3. Repository hinzufügen

Für Git-basierte Playbooks (optional):

1. Gehen Sie zu **"Repositories"**
2. Klicken Sie auf **"New Repository"**
3. Name: `Unified Ansible Playbooks`
4. URL: `https://github.com/IhrUsername/unified-ansible-project.git`
5. Branch: `main`
6. Wählen Sie den SSH-Key (falls privates Repo)
7. Klicken Sie auf **"Create"**

**Alternative**: Lokale Playbooks verwenden (empfohlen)

Semaphore kann auch Playbooks aus dem gemounteten Verzeichnis `/ansible` verwenden.

### 4. Inventory hinzufügen

#### Option A: Statisches Inventory

1. Gehen Sie zu **"Inventory"**
2. Klicken Sie auf **"New Inventory"**
3. Name: `Proxmox Production`
4. Typ: **"Static"**
5. Inventory-Inhalt einfügen:

```yaml
all:
  children:
    proxmox_servers:
      hosts:
        proxmox-host-01:
          ansible_host: 192.168.1.100
          ansible_user: root
          ansible_ssh_private_key_file: /root/.ssh/id_ed25519
```

6. Klicken Sie auf **"Create"**

#### Option B: File Inventory

1. Typ: **"File"**
2. Path: `/ansible/infrastructure/inventory/hosts.yml`

### 5. Environment erstellen

Für Variablen und Secrets:

1. Gehen Sie zu **"Environment"**
2. Klicken Sie auf **"New Environment"**
3. Name: `Production`
4. JSON-Format:

```json
{
  "ANSIBLE_HOST_KEY_CHECKING": "False",
  "ANSIBLE_FORCE_COLOR": "True"
}
```

5. Optional: Extra Variables hinzufügen
6. Klicken Sie auf **"Create"**

### 6. Task Template erstellen

Für Playbook-Ausführung:

1. Gehen Sie zu **"Task Templates"**
2. Klicken Sie auf **"New Template"**
3. Konfiguration:
   - **Name**: `Deploy Standard Profile`
   - **Playbook Filename**: `/ansible/infrastructure/site.yml`
   - **Inventory**: `Proxmox Production`
   - **Repository**: Leer lassen (lokale Playbooks)
   - **Environment**: `Production`
   - **Vault Password**: Optional
   - **Extra CLI Arguments**: `-e "@/ansible/infrastructure/config/profile_standard.yml"`

4. Klicken Sie auf **"Create"**

### 7. Task ausführen

1. Gehen Sie zu **"Task Templates"**
2. Wählen Sie `Deploy Standard Profile`
3. Klicken Sie auf **"Run"**
4. Optional: Bestätigen Sie die Ausführung
5. Verfolgen Sie die Logs in Echtzeit

## Erweiterte Konfiguration

### Scheduled Tasks

Für automatische Deployments:

1. Öffnen Sie ein Task Template
2. Klicken Sie auf **"Schedules"**
3. Klicken Sie auf **"New Schedule"**
4. Konfiguration:
   - **Cron Expression**: `0 2 * * *` (täglich um 2 Uhr)
   - **Enabled**: Ja
5. Klicken Sie auf **"Create"**

### Benutzer hinzufügen

1. Gehen Sie zu **"Team"** im Projekt
2. Klicken Sie auf **"New User"**
3. Geben Sie Username und Passwort ein
4. Wählen Sie Rolle:
   - **Owner**: Volle Rechte
   - **Manager**: Kann Tasks ausführen und bearbeiten
   - **Task Runner**: Kann nur Tasks ausführen
   - **Guest**: Nur Leserechte
5. Klicken Sie auf **"Create"**

### Notifications

Für Benachrichtigungen bei Task-Fehlern:

1. Gehen Sie zu **"Integrations"**
2. Wählen Sie **"Slack"**, **"Telegram"** oder **"Email"**
3. Konfigurieren Sie Webhook/SMTP
4. Testen Sie die Integration

## Deployment-Profile in Semaphore

Erstellen Sie separate Task Templates für jedes Profil:

### Minimal Profile

```
Name: Deploy Minimal Profile
Playbook: /ansible/infrastructure/site.yml
Extra Args: -e "@/ansible/infrastructure/config/profile_minimal.yml"
```

### Standard Profile

```
Name: Deploy Standard Profile
Playbook: /ansible/infrastructure/site.yml
Extra Args: -e "@/ansible/infrastructure/config/profile_standard.yml"
```

### Full Profile

```
Name: Deploy Full Profile
Playbook: /ansible/infrastructure/site.yml
Extra Args: -e "@/ansible/infrastructure/config/profile_full.yml"
```

### Custom Profile

```
Name: Deploy Custom Profile
Playbook: /ansible/infrastructure/site.yml
Extra Args: -e "@/ansible/infrastructure/config/profile_custom.yml"
Survey: Aktivieren (für interaktive Eingaben)
```

### Repair Profile

```
Name: Repair Infrastructure
Playbook: /ansible/infrastructure/site.yml
Extra Args: -e "@/ansible/infrastructure/config/profile_repair.yml"
```

## Sicherheit

### Best Practices

1. **Passwort ändern**: Ändern Sie das Admin-Passwort sofort nach dem ersten Login
2. **HTTPS verwenden**: In Produktion Reverse Proxy (Traefik, Nginx) mit SSL
3. **Firewall**: Beschränken Sie Zugriff auf Port 3000
4. **SSH-Keys**: Verwenden Sie separate SSH-Keys für Semaphore
5. **Vault**: Nutzen Sie Ansible Vault für Secrets
6. **Backups**: Sichern Sie die PostgreSQL-Datenbank regelmäßig

### HTTPS mit Traefik

Falls Sie Traefik verwenden:

```yaml
# In docker-compose.semaphore.yml
services:
  semaphore:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.semaphore.rule=Host(`semaphore.example.com`)"
      - "traefik.http.routers.semaphore.entrypoints=websecure"
      - "traefik.http.routers.semaphore.tls.certresolver=letsencrypt"
      - "traefik.http.services.semaphore.loadbalancer.server.port=3000"
```

## Wartung

### Logs anzeigen

```bash
docker-compose -f docker-compose.semaphore.yml logs -f
```

### Semaphore stoppen

```bash
docker-compose -f docker-compose.semaphore.yml down
```

### Semaphore neustarten

```bash
docker-compose -f docker-compose.semaphore.yml restart
```

### Backup erstellen

```bash
# Datenbank-Backup
docker-compose -f docker-compose.semaphore.yml exec semaphore-db \
  pg_dump -U semaphore semaphore > semaphore_backup_$(date +%Y%m%d).sql

# Konfiguration sichern
docker-compose -f docker-compose.semaphore.yml exec semaphore \
  tar czf /tmp/semaphore-config.tar.gz /etc/semaphore
docker cp semaphore:/tmp/semaphore-config.tar.gz ./
```

### Backup wiederherstellen

```bash
# Datenbank wiederherstellen
cat semaphore_backup_20260103.sql | \
  docker-compose -f docker-compose.semaphore.yml exec -T semaphore-db \
  psql -U semaphore semaphore
```

### Update

```bash
# Images aktualisieren
docker-compose -f docker-compose.semaphore.yml pull

# Container neu starten
docker-compose -f docker-compose.semaphore.yml up -d
```

## Troubleshooting

### Problem: Semaphore startet nicht

**Lösung**:
```bash
# Logs prüfen
docker-compose -f docker-compose.semaphore.yml logs

# Container-Status prüfen
docker-compose -f docker-compose.semaphore.yml ps

# Datenbank-Verbindung testen
docker-compose -f docker-compose.semaphore.yml exec semaphore-db \
  psql -U semaphore -c "SELECT 1"
```

### Problem: SSH-Verbindung schlägt fehl

**Lösung**:
1. Prüfen Sie SSH-Key in Key Store
2. Testen Sie SSH-Verbindung manuell:
   ```bash
   docker-compose -f docker-compose.semaphore.yml exec semaphore \
     ssh -i /root/.ssh/id_ed25519 user@host
   ```
3. Prüfen Sie `ansible_user` im Inventory

### Problem: Playbook nicht gefunden

**Lösung**:
1. Prüfen Sie Volume-Mount in `docker-compose.semaphore.yml`
2. Stellen Sie sicher, dass Pfad mit `/ansible` beginnt
3. Prüfen Sie Berechtigungen:
   ```bash
   docker-compose -f docker-compose.semaphore.yml exec semaphore ls -la /ansible
   ```

### Problem: Vault-Passwort funktioniert nicht

**Lösung**:
1. Erstellen Sie Vault Password in Semaphore
2. Verknüpfen Sie es mit dem Task Template
3. Oder verwenden Sie `--vault-password-file` in Extra Args

## Weiterführende Ressourcen

- **Semaphore Dokumentation**: https://docs.semaphoreui.com/
- **GitHub**: https://github.com/ansible-semaphore/semaphore
- **Community**: https://github.com/ansible-semaphore/semaphore/discussions

## Support

Bei Problemen:
1. Konsultieren Sie diese Dokumentation
2. Prüfen Sie Semaphore-Logs
3. Siehe `TROUBLESHOOT.md` im Hauptverzeichnis
4. Öffnen Sie ein Issue auf GitHub
