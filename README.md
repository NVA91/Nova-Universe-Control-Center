# Unified Ansible Project

Ein vereinheitlichtes, modulares Ansible-Repository, das **lokales Testing in Docker** und **Produktions-Deployment auf Proxmox** kombiniert. Dieses Projekt vereint die Stärken eines Docker-basierten Test-Controllers mit einer produktionsreifen Infrastruktur-Automatisierung.

## 🎯 Projektziele

Dieses Repository wurde durch die Zusammenführung zweier spezialisierter Projekte geschaffen:

1. **Ansible Test Controller**: Docker-basierte Testumgebung für isoliertes, reproduzierbares Testing
2. **novachris_home Infrastructure**: Produktionsreife Ansible-Automatisierung für Proxmox-basierte Self-Hosted Cloud

Das Ergebnis ist ein **einheitliches System**, das:
- ✅ Playbooks lokal validiert (ein Befehl: `make test`)
- ✅ Proxmox-Server zuverlässig einrichtet (ein Befehl: `make deploy`)
- ✅ Modular aufgebaut, leicht wartbar und erweiterbar ist

## 📁 Projektstruktur

```
unified-ansible-project/
├── controller/          # 🐳 Docker-basierte Testumgebung
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── entrypoint.sh
│   ├── ansible.cfg     # Test-optimierte Konfiguration
│   └── inventory/      # Lokales Test-Inventory
│
├── infrastructure/      # 🚀 Produktions-Infrastruktur (Proxmox)
│   ├── site.yml        # Haupt-Playbook
│   ├── ansible.cfg     # Produktions-optimierte Konfiguration
│   ├── inventory/      # Produktions-Inventory
│   │   ├── hosts.yml
│   │   ├── group_vars/
│   │   └── host_vars/
│   └── config/         # Deployment-Profile
│       ├── profile_minimal.yml
│       ├── profile_standard.yml
│       ├── profile_full.yml
│       ├── profile_custom.yml
│       └── profile_repair.yml
│
├── shared/             # 🔧 Gemeinsame Ressourcen
│   ├── roles/          # Alle Ansible-Rollen
│   ├── templates/      # Docker-Compose-Templates
│   ├── library/        # Custom Modules
│   └── plugins/        # Lookup/Filter/Callback Plugins
│
├── examples/           # 📚 Beispiel-Playbooks
├── tests/              # 🧪 Test-Playbooks
├── docs/               # 📖 Dokumentation
├── scripts/            # 🛠️ Utility-Skripte
│
├── Makefile           # Vereinheitlichter Einstiegspunkt
├── .env.example       # Umgebungsvariablen-Template
├── .gitignore
└── README.md          # Diese Datei
```

## 🚀 Quickstart

### Voraussetzungen

**Für lokales Testing:**
- Docker & Docker Compose installiert
- WSL2 (für Windows-Benutzer)

**Für Produktions-Deployment:**
- Ansible auf dem Control-Node installiert
- Proxmox VE 9.1 Server
- SSH-Zugriff auf Proxmox-Host

### 1. Repository klonen

```bash
git clone <repository-url>
cd unified-ansible-project
```

### 2. Umgebungsvariablen konfigurieren

```bash
cp .env.example .env
nano .env  # Passe die Werte an deine Umgebung an
```

### 3. Lokales Testing (Docker)

```bash
# Docker-Image bauen
make build

# Syntax-Check und Linting durchführen
make test

# Interaktive Shell im Container öffnen
make shell
```

### 4. Produktions-Deployment (Proxmox)

```bash
# Produktionsumgebung einrichten (SSH-Keys generieren)
make setup-prod

# Inventory anpassen
nano infrastructure/inventory/hosts.yml
nano infrastructure/inventory/group_vars/proxmox_servers.yml

# Standard-Deployment starten
make deploy

# Oder andere Profile verwenden
make deploy-full      # Alle VMs + Apps
make deploy-minimal   # Nur Gateway
make deploy-custom    # Interaktiv
```

## 🎮 Makefile-Kommandos

### Setup & Build

```bash
make build             # Baue Docker-Image für Test-Controller
make clean             # Lösche Container, Images und Caches
```

### Web-UI (Semaphore)

```bash
make semaphore-setup   # Richte Semaphore Web-UI ein
make semaphore-start   # Starte Semaphore
make semaphore-stop    # Stoppe Semaphore
make semaphore-logs    # Zeige Semaphore-Logs
make semaphore-backup  # Erstelle Semaphore-Backup
```

### Testing (lokal im Container)

```bash
make test              # Führe alle Tests durch (Syntax + Lint)
make test-playbook     # Teste spezifisches Playbook
make lint              # Führe ansible-lint aus
make syntax-check      # Prüfe Playbook-Syntax
make shell             # Öffne interaktive Shell im Container
```

### Deployment (auf Proxmox)

```bash
make deploy            # Standard-Deployment (profile_standard.yml)
make deploy-full       # Vollständiges Deployment (alle VMs + Apps)
make deploy-minimal    # Minimales Deployment (nur Gateway)
make deploy-custom     # Interaktives Deployment
make deploy-repair     # Reparatur-Modus
```

### Informationen

```bash
make info              # Zeige Projekt-Informationen
make version           # Zeige Ansible- und Python-Versionen
make inventory         # Zeige Inventory
make logs              # Zeige Ansible-Logs
```

## 🏗️ Architektur: "The Clean House Strategy"

Die Infrastruktur basiert auf einer klaren Trennung zwischen Hypervisor, Netzwerk und Anwendungen:

- **Proxmox Host**: Reiner Hypervisor ("Vermieter"), stellt nur Ressourcen bereit
- **VPS (optional)**: "Türsteher" und Cache, nimmt Internet-Traffic entgegen
- **3 Spezialisierte VMs**:
  - **vm-gateway**: WireGuard-Tunnel-Endpunkt + Traefik Reverse Proxy
  - **vm-office**: Datenintensive Apps (Paperless-ngx, N8N, PostgreSQL)
  - **vm-ai-lab**: KI-Anwendungen (Whisper, Ollama) mit GPU-Passthrough-Vorbereitung

## 🔧 Features

### Test-Controller Features

- ✅ Isolierte, reproduzierbare Testumgebung
- ✅ Umfassende Linting-Tools (ansible-lint, yamllint, pylint)
- ✅ CI/CD-Integration (GitLab CI, GitHub Actions)
- ✅ Flexible Playbook-Ausführung
- ✅ Secrets-Management über .env-Dateien

### Infrastructure Features

- ✅ Intelligente VM-Provisioning mit Hostname-Korrektur
- ✅ Plugin-System für Apps (über group_vars definiert)
- ✅ Profilbasiertes Deployment (minimal, standard, full, custom, repair)
- ✅ Storage-Architektur (System-Disk + Daten-Disk)
- ✅ Docker-Setup auf VMs
- ✅ Ansible Vault für Secrets
- ✅ Netzwerk-Automatisierung (vmbr0, WireGuard)

## 🖥️ Web-UI mit Semaphore

Das Projekt enthält eine optionale **Web-UI** für grafische Verwaltung:

**Ansible Semaphore** bietet:
- ✅ Playbook-Ausführung über Browser
- ✅ Inventory-Management
- ✅ Job-Historie und Echtzeit-Logs
- ✅ Scheduled Tasks (Cron)
- ✅ Multi-User mit Rollen
- ✅ REST API

**Schnellstart:**
```bash
make semaphore-setup   # Einmalige Einrichtung
# Öffne http://localhost:3000 im Browser
```

**Dokumentation**: [SEMAPHORE_QUICKSTART.md](docs/SEMAPHORE_QUICKSTART.md) | [SEMAPHORE_CONFIG.md](docs/SEMAPHORE_CONFIG.md)

## 📚 Verfügbare Rollen

Das Projekt enthält 9 spezialisierte Ansible-Rollen im `shared/roles/`-Verzeichnis:

1. **system_setup**: Proxmox-Host-Konfiguration (Repositories, Firewall, Netzwerk)
2. **user_management**: Benutzer- und SSH-Verwaltung
3. **storage_setup**: Storage-Architektur (Disk 1 + Disk 2)
4. **provision_guests**: VM-Erstellung aus Cloud-Image-Template
5. **docker_setup**: Docker-Installation auf VMs
6. **app_deployment**: Docker-Compose-basiertes App-Deployment
7. **qa_smoke**: Validierungs- und Test-Aufgaben
8. **installation_classes**: Modulare App-Verwaltung
9. **project_backup**: Backup-Automatisierung

## 🧪 Testbarkeit-Matrix

| Komponente | Im Container testbar? | Hinweise |
|------------|----------------------|----------|
| **Syntax-Check** | ✅ Ja | Vollständig testbar |
| **Linting** | ✅ Ja | ansible-lint, yamllint |
| **Variable-Check** | ✅ Ja | Mit Mock-Inventory |
| **Rollen (docker_setup)** | ✅ Ja | Mit Docker-in-Docker |
| **Rollen (app_deployment)** | ✅ Ja | Mit Mock-Templates |
| **VM-Provisioning** | ❌ Nein | Benötigt echten Proxmox-Server |
| **Proxmox-API-Aufrufe** | ❌ Nein | Benötigt echten Proxmox-Server |

## 🔐 Secrets-Management

### Für lokales Testing

Verwende `.env`-Dateien (bereits in `.gitignore`):

```bash
cp .env.example .env
nano .env
```

### Für Produktions-Deployment

Verwende **Ansible Vault** für sensible Daten:

```bash
# Vault-Passwort-Datei erstellen
echo "your-secure-password" > .vault_pass
chmod 600 .vault_pass

# Secrets verschlüsseln
ansible-vault encrypt infrastructure/inventory/group_vars/all/vault.yml

# Playbook mit Vault ausführen
cd infrastructure
ansible-playbook site.yml --vault-password-file ../.vault_pass
```

## 📖 Dokumentation

Ausführliche Dokumentation findest du im `docs/`-Verzeichnis:

- **[README_INFRASTRUCTURE.md](docs/README_INFRASTRUCTURE.md)**: Infrastruktur-Details
- **[README_CONTROLLER.md](docs/README_CONTROLLER.md)**: Test-Controller-Details
- **[QUICKSTART.md](docs/QUICKSTART.md)**: Schnelleinstieg
- **[IMPLEMENTATION_GUIDE.md](docs/IMPLEMENTATION_GUIDE.md)**: Implementierungsanleitung
- **[TROUBLESHOOT.md](docs/TROUBLESHOOT.md)**: Fehlerbehebung
- **[WSL_SETUP.md](docs/WSL_SETUP.md)**: WSL-Einrichtung für Windows
- **[SECURITY.md](docs/SECURITY.md)**: Sicherheits-Best-Practices

## 🛠️ Entwicklung

### Neue Rolle hinzufügen

```bash
# Rolle im shared-Verzeichnis erstellen
cd shared/roles
ansible-galaxy init my_new_role

# Rolle wird automatisch von beiden Umgebungen erkannt
```

### Neue App hinzufügen

1. Docker-Compose-Template erstellen: `shared/templates/docker-compose/my-app.yml`
2. App in Inventory registrieren: `infrastructure/inventory/group_vars/proxmox_servers.yml`
3. Deployment-Profil aktualisieren: `infrastructure/config/profile_*.yml`

### Lokales Testing neuer Playbooks

```bash
# Playbook in examples/ erstellen
nano examples/my-test.yml

# Im Container testen
make shell
cd /project
ansible-playbook examples/my-test.yml --syntax-check
```

## 🤝 Contributing

Beiträge sind willkommen! Bitte beachte:

1. Teste alle Änderungen lokal mit `make test`
2. Dokumentiere neue Features in `docs/`
3. Halte die Trennung zwischen `controller/`, `infrastructure/` und `shared/` ein
4. Keine sensiblen Daten in Git committen

Siehe [CONTRIBUTING.md](docs/CONTRIBUTING.md) für Details.

## 📜 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 🙏 Danksagungen

Dieses Projekt vereint:
- **Ansible Test Controller v2.0**: Docker-basierte Testumgebung
- **novachris_home**: Produktionsreife Proxmox-Infrastruktur

## 📞 Support

Bei Fragen oder Problemen:
1. Siehe [TROUBLESHOOT.md](docs/TROUBLESHOOT.md)
2. Öffne ein Issue auf GitHub
3. Konsultiere die ausführliche Dokumentation in `docs/`

---

**Viel Erfolg mit deiner Ansible-Automatisierung! 🚀**
