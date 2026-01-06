# Quickstart: Unified Ansible Project

## 🚀 Schnelleinstieg in 5 Minuten

Dieser Guide führt Sie durch die ersten Schritte mit dem vereinheitlichten Ansible-Projekt.

## Voraussetzungen

### Für lokales Testing
- ✅ Docker installiert
- ✅ Docker Compose installiert
- ✅ WSL2 (für Windows-Benutzer)

### Für Produktions-Deployment
- ✅ Ansible auf dem Control-Node
- ✅ Proxmox VE 9.1 Server
- ✅ SSH-Zugriff auf Proxmox-Host

## Schritt 1: Repository entpacken

```bash
# ZIP-Datei entpacken
unzip unified-ansible-project.zip
cd unified-ansible-project

# Verzeichnisstruktur anzeigen
tree -L 2
```

## Schritt 2: Umgebung konfigurieren

```bash
# Umgebungsvariablen kopieren und anpassen
cp .env.example .env
nano .env

# Wichtige Variablen:
# - SSH_USER=ubuntu
# - PROXMOX_HOST=192.168.1.100
# - DEPLOYMENT_PROFILE=standard
```

## Schritt 3: Lokales Testing

### Docker-Image bauen

```bash
make build
```

**Erwartete Ausgabe**:
```
🔨 Baue Docker-Image...
[+] Building 120.5s (12/12) FINISHED
✅ Build abgeschlossen!
```

### Tests durchführen

```bash
# Syntax-Check
make syntax-check

# Linting
make lint

# Alle Tests
make test
```

**Erwartete Ausgabe**:
```
📝 Prüfe Playbook-Syntax...
✅ Syntax-Check erfolgreich!

🔍 Führe ansible-lint aus...
✅ Linting erfolgreich!

✅ Alle Tests erfolgreich!
```

### Interaktive Shell

```bash
make shell

# Im Container:
cd /project
ansible --version
ansible-playbook examples/hello-world.yml
exit
```

## Schritt 4: Produktions-Deployment vorbereiten

### SSH-Keys generieren

```bash
make setup-prod
```

**Erwartete Ausgabe**:
```
🔐 Richte Produktionsumgebung ein...
Generating public/private ed25519 key pair...
✅ Produktionsumgebung eingerichtet!
```

### Inventory anpassen

```bash
# Haupt-Inventory bearbeiten
nano infrastructure/inventory/hosts.yml

# Proxmox-Server-IP eintragen:
proxmox_servers:
  hosts:
    proxmox-host-01:
      ansible_host: 192.168.1.100  # <-- Ihre IP
```

```bash
# VM-Konfiguration anpassen
nano infrastructure/inventory/group_vars/proxmox_servers.yml

# VMs und Apps konfigurieren
```

## Schritt 5: Deployment durchführen

### Dry-Run (empfohlen)

```bash
make deploy-dry-run
```

**Zweck**: Zeigt, was passieren würde, ohne Änderungen vorzunehmen

### Standard-Deployment

```bash
make deploy
```

**Deployed**:
- VMs: vm-gateway, vm-office
- Apps: WireGuard, Traefik, Paperless-ngx, N8N, PostgreSQL

### Andere Profile

```bash
# Minimales Deployment (nur Gateway)
make deploy-minimal

# Vollständiges Deployment (alle VMs + Apps)
make deploy-full

# Interaktives Deployment
make deploy-custom

# Reparatur-Modus
make deploy-repair
```

## Verfügbare Kommandos

### Setup & Build

```bash
make build             # Docker-Image bauen
make clean             # Aufräumen
```

### Testing

```bash
make test              # Alle Tests
make test-playbook     # Spezifisches Playbook testen
make lint              # Linting
make syntax-check      # Syntax-Check
make shell             # Interaktive Shell
```

### Deployment

```bash
make deploy            # Standard-Deployment
make deploy-full       # Vollständiges Deployment
make deploy-minimal    # Minimales Deployment
make deploy-custom     # Interaktives Deployment
make deploy-repair     # Reparatur-Modus
```

### Informationen

```bash
make info              # Projekt-Informationen
make version           # Versionen anzeigen
make inventory         # Inventory anzeigen
make logs              # Logs anzeigen
make help              # Alle Kommandos
```

## Typische Workflows

### Workflow 1: Entwicklung und Testing

```bash
# 1. Änderungen vornehmen
nano shared/roles/my_role/tasks/main.yml

# 2. Syntax prüfen
make syntax-check

# 3. Linting durchführen
make lint

# 4. Im Container testen
make shell
cd /project
ansible-playbook examples/with-roles.yml
exit

# 5. Committen
git add .
git commit -m "Add new role"
```

### Workflow 2: Produktions-Deployment

```bash
# 1. Tests durchführen
make test

# 2. Inventory prüfen
make inventory

# 3. Dry-Run
make deploy-dry-run

# 4. Deployment
make deploy

# 5. Logs prüfen
make logs
```

### Workflow 3: Neue App hinzufügen

```bash
# 1. Docker-Compose-Template erstellen
nano shared/templates/docker-compose/my-app.yml

# 2. In Inventory registrieren
nano infrastructure/inventory/group_vars/proxmox_servers.yml

# 3. In Profil aufnehmen
nano infrastructure/config/profile_standard.yml

# 4. Testen
make test

# 5. Deployen
make deploy
```

## Troubleshooting

### Problem: "Role not found"

**Lösung**:
```bash
# Prüfe roles_path
grep roles_path controller/ansible.cfg
grep roles_path infrastructure/ansible.cfg

# Prüfe, ob Rolle existiert
ls -la shared/roles/
```

### Problem: "Docker-Image build failed"

**Lösung**:
```bash
# Alte Images löschen
make clean

# Neu bauen
make build

# Logs prüfen
docker-compose -f controller/docker-compose.yml logs
```

### Problem: "SSH connection failed"

**Lösung**:
```bash
# SSH-Verbindung manuell testen
ssh -i .ssh/id_ed25519 user@proxmox-host

# SSH-Key auf Proxmox-Host kopieren
ssh-copy-id -i .ssh/id_ed25519.pub user@proxmox-host
```

### Problem: "Playbook syntax error"

**Lösung**:
```bash
# Syntax detailliert prüfen
cd infrastructure
ansible-playbook site.yml --syntax-check -vvv

# YAML-Syntax prüfen
make shell
yamllint infrastructure/site.yml
```

## Nächste Schritte

Nach dem Quickstart:

1. **Dokumentation lesen**:
   - [README.md](README.md) - Vollständige Übersicht
   - [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architektur-Details
   - [TESTING.md](docs/TESTING.md) - Testing-Guide

2. **Beispiele erkunden**:
   ```bash
   ls examples/
   cat examples/hello-world.yml
   ```

3. **Rollen anpassen**:
   ```bash
   ls shared/roles/
   cat shared/roles/docker_setup/tasks/main.yml
   ```

4. **Apps konfigurieren**:
   ```bash
   ls shared/templates/docker-compose/
   cat shared/templates/docker-compose/traefik.yml
   ```

## Hilfe und Support

- **Dokumentation**: `docs/` Verzeichnis
- **Troubleshooting**: [TROUBLESHOOT.md](docs/TROUBLESHOOT.md)
- **WSL-Setup**: [WSL_SETUP.md](docs/WSL_SETUP.md)
- **Sicherheit**: [SECURITY.md](docs/SECURITY.md)

## Checkliste

- [ ] Repository entpackt
- [ ] `.env` konfiguriert
- [ ] Docker-Image gebaut (`make build`)
- [ ] Tests durchgeführt (`make test`)
- [ ] SSH-Keys generiert (`make setup-prod`)
- [ ] Inventory angepasst
- [ ] Dry-Run durchgeführt (`make deploy-dry-run`)
- [ ] Deployment erfolgreich (`make deploy`)
- [ ] Services geprüft

---

**Viel Erfolg! 🚀**

Bei Fragen: Siehe [TROUBLESHOOT.md](docs/TROUBLESHOOT.md)
