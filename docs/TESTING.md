# Testing-Guide: Unified Ansible Project

## Übersicht

Dieses Dokument beschreibt alle Testing-Methoden und -Strategien für das Unified Ansible Project. Das Projekt unterstützt **lokales Testing im Docker-Container** sowie **Produktions-Testing auf Proxmox**.

## Testing-Philosophie

### Prinzipien

1. **Test First**: Immer zuerst lokal testen, bevor auf Produktion deployt wird
2. **Fail Fast**: Fehler früh erkennen (Syntax → Lint → Integration)
3. **Isolation**: Tests beeinflussen sich nicht gegenseitig
4. **Reproduzierbarkeit**: Jeder Test liefert bei gleichen Bedingungen gleiche Ergebnisse

### Testing-Pyramide

```
        ┌─────────────────┐
        │  Produktions-   │
        │  Deployment     │  ← Manuell, selten
        └─────────────────┘
       ┌───────────────────┐
       │  Integration      │
       │  Tests            │  ← Mit Mock-Inventory
       └───────────────────┘
      ┌─────────────────────┐
      │  Linting &          │
      │  Syntax-Checks      │  ← Automatisiert, häufig
      └─────────────────────┘
```

## Lokales Testing (Docker)

### Setup

```bash
# 1. Docker-Image bauen
make build

# 2. Umgebungsvariablen konfigurieren
cp .env.example .env
nano .env
```

### Basis-Tests

#### 1. Syntax-Check

Prüft die YAML-Syntax und Ansible-Struktur:

```bash
make syntax-check
```

**Was wird geprüft:**
- YAML-Syntax
- Ansible-Playbook-Struktur
- Variable-Definitionen
- Task-Syntax

**Erwartetes Ergebnis:**
```
✅ Syntax-Check erfolgreich!
```

#### 2. Linting

Prüft Best Practices und Code-Qualität:

```bash
make lint
```

**Was wird geprüft:**
- Ansible-Best-Practices (ansible-lint)
- YAML-Formatierung (yamllint)
- Deprecated Features
- Sicherheits-Checks

**Erwartetes Ergebnis:**
```
✅ Linting erfolgreich (oder Warnungen, die ignoriert werden können)
```

#### 3. Vollständiger Test

Führt alle Tests durch:

```bash
make test
```

**Umfasst:**
- Syntax-Check
- Linting
- Variable-Validierung

### Erweiterte Tests

#### Spezifisches Playbook testen

```bash
make test-playbook PLAYBOOK=examples/hello-world.yml
```

#### Interaktive Shell

Für manuelle Tests im Container:

```bash
make shell

# Im Container:
cd /project
ansible-playbook examples/hello-world.yml
ansible-playbook infrastructure/site.yml --syntax-check
ansible-lint infrastructure/site.yml
```

#### Dry-Run

Simuliert Deployment ohne Änderungen:

```bash
# Im Container
make shell
cd /project/infrastructure
ansible-playbook site.yml -e "@config/profile_standard.yml" --check
```

## Testbarkeit-Matrix

### Vollständig testbar im Container

| Komponente | Testmethode | Kommando |
|------------|-------------|----------|
| **Syntax** | ansible-playbook --syntax-check | `make syntax-check` |
| **Linting** | ansible-lint | `make lint` |
| **YAML** | yamllint | Im Container |
| **Variablen** | ansible-playbook --check | Im Container |
| **Templates** | Jinja2-Rendering | Im Container |

### Teilweise testbar im Container

| Komponente | Was testbar? | Was nicht testbar? |
|------------|--------------|-------------------|
| **docker_setup** | Syntax, Variablen | Echte Docker-Installation |
| **app_deployment** | Template-Rendering | Echte Container-Starts |
| **user_management** | Syntax, Logik | Echte User-Erstellung |

### Nicht testbar im Container

| Komponente | Grund | Alternative |
|------------|-------|-------------|
| **provision_guests** | Benötigt Proxmox-API | Staging-Umgebung |
| **storage_setup** | Benötigt echte Disks | Staging-Umgebung |
| **system_setup** | Benötigt Proxmox-Host | Staging-Umgebung |

## Test-Playbooks

### Beispiel-Playbooks

Im `examples/`-Verzeichnis befinden sich Test-Playbooks:

#### hello-world.yml

```bash
make shell
cd /project
ansible-playbook examples/hello-world.yml
```

**Zweck**: Grundlegende Ansible-Funktionalität testen

#### with-roles.yml

```bash
make shell
cd /project
ansible-playbook examples/with-roles.yml
```

**Zweck**: Rollen-Integration testen

#### simulate_proxmox.yml

```bash
make shell
cd /project
ansible-playbook examples/simulate_proxmox.yml
```

**Zweck**: Proxmox-ähnliche Operationen simulieren

### Eigene Test-Playbooks erstellen

```yaml
# tests/my-test.yml
---
- name: Test My Feature
  hosts: localhost
  gather_facts: false
  
  tasks:
    - name: Test Variable Definition
      ansible.builtin.debug:
        msg: "Variable test: {{ my_var | default('not defined') }}"
    
    - name: Test Role Inclusion
      ansible.builtin.include_role:
        name: my_role
      when: false  # Skip actual execution
```

```bash
make shell
cd /project
ansible-playbook tests/my-test.yml --syntax-check
```

## CI/CD-Integration

### GitHub Actions

Beispiel `.github/workflows/test.yml`:

```yaml
name: Ansible Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker Image
        run: make build
      
      - name: Run Tests
        run: make test
      
      - name: Upload Logs
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: ansible-logs
          path: controller/logs/
```

### GitLab CI

Beispiel `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - deploy

test:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  script:
    - make build
    - make test
  only:
    - merge_requests
    - main

deploy:
  stage: deploy
  script:
    - make deploy
  only:
    - main
  when: manual
```

## Staging-Umgebung

Für Tests, die nicht im Container möglich sind, empfiehlt sich eine Staging-Umgebung.

### Setup

1. **Separates Proxmox-System** oder **separate VMs** für Staging
2. **Eigenes Inventory**: `infrastructure/inventory/staging.yml`
3. **Staging-Profil**: `infrastructure/config/profile_staging.yml`

### Staging-Deployment

```bash
# Staging-Inventory verwenden
cd infrastructure
ansible-playbook site.yml -i inventory/staging.yml -e "@config/profile_staging.yml"
```

## Debugging

### Verbosity-Level

```bash
# Level 1: Basis-Informationen
cd infrastructure
ansible-playbook site.yml -v

# Level 2: Mehr Details
ansible-playbook site.yml -vv

# Level 3: Debug-Informationen
ansible-playbook site.yml -vvv

# Level 4: Alle Verbindungs-Details
ansible-playbook site.yml -vvvv
```

### Logs analysieren

```bash
# Echtzeit-Logs
make logs

# Logs durchsuchen
grep ERROR infrastructure/logs/ansible.log
grep FAILED infrastructure/logs/ansible.log
```

### Einzelne Tasks testen

```bash
make shell

# Im Container
cd /project/infrastructure
ansible-playbook site.yml --start-at-task="Task Name"
ansible-playbook site.yml --tags="docker_setup"
ansible-playbook site.yml --skip-tags="proxmox_only"
```

## Test-Checkliste

### Vor jedem Commit

- [ ] `make syntax-check` erfolgreich
- [ ] `make lint` erfolgreich (oder Warnungen dokumentiert)
- [ ] Neue Rollen/Tasks dokumentiert
- [ ] `.gitignore` aktualisiert (falls neue Dateien)

### Vor jedem Deployment

- [ ] `make test` erfolgreich
- [ ] Inventory geprüft (`make inventory`)
- [ ] Backup erstellt
- [ ] Dry-Run durchgeführt (`make deploy-dry-run`)
- [ ] Deployment-Profil korrekt ausgewählt

### Nach jedem Deployment

- [ ] Logs geprüft (`make logs`)
- [ ] Services geprüft (SSH, Docker, Apps)
- [ ] QA-Smoke-Tests erfolgreich
- [ ] Dokumentation aktualisiert

## Häufige Test-Fehler

### 1. "Role not found"

**Problem**: Ansible findet Rolle nicht

**Lösung**:
```bash
# Prüfe roles_path in ansible.cfg
grep roles_path controller/ansible.cfg
grep roles_path infrastructure/ansible.cfg

# Prüfe, ob Rolle existiert
ls -la shared/roles/
```

### 2. "Syntax Error in YAML"

**Problem**: YAML-Formatierung falsch

**Lösung**:
```bash
# Verwende yamllint
make shell
yamllint infrastructure/site.yml

# Prüfe Einrückung (2 Spaces, keine Tabs)
```

### 3. "Variable not defined"

**Problem**: Variable nicht gesetzt

**Lösung**:
```bash
# Prüfe Variable-Definitionen
grep -r "my_var" infrastructure/inventory/

# Verwende default-Filter
{{ my_var | default('fallback_value') }}
```

### 4. "Connection timeout"

**Problem**: SSH-Verbindung schlägt fehl

**Lösung**:
```bash
# Prüfe SSH-Verbindung manuell
ssh -i .ssh/id_rsa user@host

# Erhöhe Timeout in ansible.cfg
timeout = 30
```

## Performance-Testing

### Zeitmessung

```bash
# Mit Ansible-Timer
cd infrastructure
ANSIBLE_CALLBACK_WHITELIST=timer ansible-playbook site.yml

# Mit time-Kommando
time ansible-playbook site.yml
```

### Profiling

```bash
# Mit profile_tasks-Plugin
cd infrastructure
ANSIBLE_CALLBACK_WHITELIST=profile_tasks ansible-playbook site.yml
```

## Best Practices

1. **Kleine Änderungen**: Teste jede Änderung einzeln
2. **Frequent Testing**: Teste oft, nicht nur vor Commits
3. **Dokumentiere Fehler**: Halte häufige Fehler in TROUBLESHOOT.md fest
4. **Automatisiere**: Nutze CI/CD für automatische Tests
5. **Staging First**: Teste kritische Änderungen zuerst in Staging

## Weiterführende Ressourcen

- [Ansible Testing Strategies](https://docs.ansible.com/ansible/latest/reference_appendices/test_strategies.html)
- [Molecule Testing Framework](https://molecule.readthedocs.io/)
- [ansible-lint Documentation](https://ansible-lint.readthedocs.io/)
