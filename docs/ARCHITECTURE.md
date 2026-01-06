# Architektur-Dokumentation: Unified Ansible Project

## Übersicht

Das **Unified Ansible Project** ist ein modulares, zweigleisiges Ansible-Repository, das lokales Testing und Produktions-Deployment in einer einzigen, wartbaren Struktur vereint.

## Designprinzipien

### 1. Separation of Concerns

Das Projekt trennt klar zwischen drei Hauptbereichen:

- **controller/**: Isolierte Docker-Testumgebung
- **infrastructure/**: Produktions-Deployment-Logik
- **shared/**: Gemeinsame Ressourcen (Rollen, Templates, Plugins)

Diese Trennung ermöglicht:
- Unabhängige Entwicklung und Testing
- Wiederverwendung von Code
- Klare Verantwortlichkeiten

### 2. DRY (Don't Repeat Yourself)

Alle wiederverwendbaren Komponenten (Rollen, Templates, Plugins) befinden sich im `shared/`-Verzeichnis und werden von beiden Umgebungen referenziert.

### 3. Environment-Aware Configuration

Zwei separate `ansible.cfg`-Dateien ermöglichen umgebungsspezifische Optimierungen:

- **controller/ansible.cfg**: Test-optimiert (schnelle Iterationen, verbose logging)
- **infrastructure/ansible.cfg**: Produktions-optimiert (Performance, Logging)

### 4. Single Entry Point

Das **Makefile** bietet einen einheitlichen Einstiegspunkt für alle Operationen:
- `make test` → Lokales Testing
- `make deploy` → Produktions-Deployment

## Verzeichnisstruktur im Detail

### controller/ - Docker-Testumgebung

```
controller/
├── Dockerfile              # Ubuntu 22.04 + Ansible 2.12.10 + Tools
├── docker-compose.yml      # Orchestrierung
├── entrypoint.sh           # Preflight-Checks
├── ansible.cfg             # Test-Konfiguration
├── inventory/              # Lokales Test-Inventory
│   └── local.yml
├── logs/                   # Container-Logs
└── test.sh                 # Legacy-Test-Script
```

**Zweck**: Isolierte, reproduzierbare Testumgebung für Playbook-Validierung

**Key Features**:
- Ansible-Lint, yamllint, pylint integriert
- Docker-in-Docker-Support (optional)
- Mountet gesamtes Projekt-Root nach `/project`
- Fact-Caching für schnellere Wiederholungen

### infrastructure/ - Produktions-Infrastruktur

```
infrastructure/
├── site.yml                # Haupt-Playbook (7 Plays)
├── ansible.cfg             # Produktions-Konfiguration
├── inventory/              # Produktions-Inventory
│   ├── hosts.yml           # Haupt-Inventory
│   ├── group_vars/
│   │   ├── all.yml
│   │   ├── controllers.yml
│   │   └── proxmox_servers.yml
│   └── host_vars/
│       └── proxmox-host-01.yml
├── config/                 # Deployment-Profile
│   ├── profile_minimal.yml
│   ├── profile_standard.yml
│   ├── profile_full.yml
│   ├── profile_custom.yml
│   └── profile_repair.yml
├── logs/                   # Ansible-Logs
├── setup_prod_env.sh       # SSH-Key-Generierung
└── wizzad.sh               # Legacy-Wizard
```

**Zweck**: Produktionsreife Ansible-Automatisierung für Proxmox-basierte Infrastruktur

**Key Features**:
- Profilbasiertes Deployment
- VM-Provisioning mit Cloud-Images
- Docker-Setup auf VMs
- App-Deployment via Docker Compose
- QA-Smoke-Tests

### shared/ - Gemeinsame Ressourcen

```
shared/
├── roles/                  # Alle Ansible-Rollen
│   ├── system_setup/
│   ├── user_management/
│   ├── storage_setup/
│   ├── provision_guests/
│   ├── docker_setup/
│   ├── app_deployment/
│   ├── qa_smoke/
│   ├── installation_classes/
│   └── project_backup/
├── templates/              # Jinja2-Templates
│   └── docker-compose/     # Docker-Compose-Templates für Apps
│       ├── traefik.yml
│       ├── paperless-ngx.yml
│       ├── n8n.yml
│       ├── postgresql.yml
│       ├── whisper.yml
│       ├── ollama.yml
│       └── wireguard-client.yml
├── library/                # Custom Ansible Modules
├── plugins/                # Ansible Plugins
│   ├── lookup/
│   ├── filter/
│   └── callback/
└── vars/                   # Gemeinsame Variablen
```

**Zweck**: Zentrale Ablage für alle wiederverwendbaren Komponenten

**Key Features**:
- Wird von beiden Umgebungen referenziert (via `roles_path` in ansible.cfg)
- Ermöglicht Code-Wiederverwendung
- Vereinfacht Wartung und Updates

## Datenfluss

### Lokales Testing (make test)

```
┌─────────────┐
│  make test  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  docker-compose (controller/)       │
│  - Baut Image aus Dockerfile        │
│  - Mountet ..:/project              │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Container (Ubuntu 22.04)           │
│  - Lädt controller/ansible.cfg     │
│  - Referenziert ../shared/roles     │
│  - Führt ansible-lint aus           │
│  - Führt syntax-check aus           │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Ergebnis: ✅ oder ❌               │
└─────────────────────────────────────┘
```

### Produktions-Deployment (make deploy)

```
┌──────────────────┐
│  make deploy     │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  ansible-playbook (Host-System)     │
│  - Lädt infrastructure/ansible.cfg  │
│  - Lädt infrastructure/site.yml     │
│  - Lädt Deployment-Profil           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Play 1: Profil-Setup               │
│  - Lädt Profil-Konfiguration        │
│  - Interaktive Abfrage (custom)     │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Play 2: Proxmox Host Vorbereitung  │
│  - system_setup (shared/roles/)     │
│  - user_management                  │
│  - storage_setup                    │
│  - provision_guests                 │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Play 3: Docker Setup auf VMs       │
│  - docker_setup (shared/roles/)     │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Play 4: App Deployment             │
│  - app_deployment (shared/roles/)   │
│  - Nutzt shared/templates/          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Play 5-7: QA, Firewall, Reporting  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Ergebnis: Deployed Infrastructure  │
└─────────────────────────────────────┘
```

## Konfigurationsverwaltung

### ansible.cfg Unterschiede

| Setting | controller/ansible.cfg | infrastructure/ansible.cfg |
|---------|------------------------|----------------------------|
| **roles_path** | `../shared/roles:./roles` | `../shared/roles:roles` |
| **library** | `../shared/library:./library` | `../shared/library` |
| **inventory** | `./inventory` | `inventory/hosts.yml` |
| **forks** | 10 | 5 (default) |
| **retry_files_enabled** | True | False |
| **log_path** | - | `logs/ansible.log` |
| **verbosity** | 0 (konfigurierbar) | - |
| **connection** | local | ssh |

### Umgebungsvariablen

Umgebungsvariablen werden über `.env`-Dateien verwaltet:

- **Root-Level**: `.env` (für Makefile und Docker Compose)
- **Controller**: Wird via `docker-compose.yml` in Container injiziert
- **Infrastructure**: Wird vom Host-System gelesen

## Deployment-Profile

Das Projekt nutzt ein profilbasiertes Deployment-System:

### profile_minimal.yml
- **VMs**: vm-gateway
- **Apps**: wireguard-client, traefik
- **Zweck**: Minimale Infrastruktur für Netzwerk-Gateway

### profile_standard.yml
- **VMs**: vm-gateway, vm-office
- **Apps**: wireguard, traefik, paperless-ngx, n8n, postgresql
- **Zweck**: Standard-Deployment für Office-Anwendungen

### profile_full.yml
- **VMs**: vm-gateway, vm-office, vm-ai-lab
- **Apps**: Alle verfügbaren Apps
- **Zweck**: Vollständiges Deployment inkl. KI-Labor

### profile_custom.yml
- **VMs**: Interaktive Auswahl
- **Apps**: Interaktive Auswahl
- **Zweck**: Flexibles, benutzerdefiniertes Deployment

### profile_repair.yml
- **VMs**: Keine neuen VMs
- **Apps**: Keine neuen Apps
- **Zweck**: Reparatur bestehender Infrastruktur

## Sicherheitsarchitektur

### Secrets-Management

1. **Lokales Testing**: `.env`-Dateien (nicht in Git)
2. **Produktions-Deployment**: Ansible Vault

### SSH-Keys

- Werden von `setup_prod_env.sh` generiert
- Liegen in `.ssh/` (in `.gitignore`)
- Werden in Container gemountet (read-only)

### Firewall

- PVE-Firewall wird am Ende aktiviert (Play 6)
- SSH-Port bleibt offen (Port 22)
- Alle anderen Ports standardmäßig geschlossen

## Erweiterbarkeit

### Neue Rolle hinzufügen

1. Rolle in `shared/roles/` erstellen
2. In Playbook referenzieren
3. Automatisch in beiden Umgebungen verfügbar

### Neue App hinzufügen

1. Docker-Compose-Template in `shared/templates/docker-compose/` erstellen
2. In `infrastructure/inventory/group_vars/proxmox_servers.yml` registrieren
3. In Deployment-Profil aufnehmen

### Neue Tests hinzufügen

1. Test-Playbook in `tests/` erstellen
2. In `Makefile` neues Target hinzufügen
3. Via `make <target>` ausführen

## Performance-Optimierungen

### Fact-Caching

Beide Umgebungen nutzen JSON-basiertes Fact-Caching:
- Cache-Location: `/tmp/ansible_facts`
- Timeout: 3600s (controller), 86400s (infrastructure)

### SSH-Pipelining

Aktiviert in beiden Umgebungen für schnellere Ausführung.

### Parallelisierung

- Controller: 10 Forks (für schnelle Tests)
- Infrastructure: 5 Forks (für stabile Deployments)

## Troubleshooting

### Pfad-Probleme

Wenn Rollen nicht gefunden werden:
1. Prüfe `roles_path` in `ansible.cfg`
2. Stelle sicher, dass relative Pfade korrekt sind
3. Bei Docker: Prüfe Volume-Mounts in `docker-compose.yml`

### Container-Probleme

Wenn Container nicht startet:
1. `make clean` ausführen
2. `make build` neu ausführen
3. Logs prüfen: `docker-compose -f controller/docker-compose.yml logs`

### Deployment-Probleme

Wenn Deployment fehlschlägt:
1. Syntax-Check: `make syntax-check`
2. Inventory prüfen: `make inventory`
3. Verbosity erhöhen: `cd infrastructure && ansible-playbook site.yml -vvv`

## Best Practices

1. **Immer zuerst testen**: `make test` vor `make deploy`
2. **Kleine Änderungen**: Inkrementelle Änderungen statt große Refactorings
3. **Dokumentation**: Jede neue Rolle/App dokumentieren
4. **Versionierung**: Git-Tags für stabile Versionen verwenden
5. **Backups**: Vor Produktions-Deployments Backups erstellen

## Zukunft

Geplante Erweiterungen:
- CI/CD-Pipeline (GitHub Actions, GitLab CI)
- Molecule-Tests für Rollen
- Automatische Dokumentations-Generierung
- Monitoring-Integration (Prometheus, Grafana)
- Backup-Automatisierung
