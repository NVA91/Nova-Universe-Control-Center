# Quickstart - Ansible Test Controller (v2.0)

Starten Sie in 5 Minuten mit dem Ansible Test Controller.

## 1. Voraussetzungen

- Docker installiert: `docker --version`
- Docker Compose installiert: `docker-compose --version`

## 2. Setup

```bash
# Klone oder lade das Projekt herunter
cd ansible_test_controller

# Kopiere die .env-Beispieldatei
cp .env.example .env

# Baue das Docker-Image
make build
```

## 3. Dein erstes Playbook testen

### Option A: Beispiel-Playbook verwenden

Das Projekt enthält ein Beispiel-Playbook in `_examples/hello-world.yml`.

```bash
# Kopiere das Beispiel-Playbook
cp _examples/hello-world.yml site.yml

# Führe es aus
make run
```

### Option B: Eigenes Playbook erstellen

Erstelle eine `site.yml` im Projektverzeichnis:

```yaml
---
- name: Test Playbook
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    - name: Zeige eine Nachricht
      debug:
        msg: "Hallo vom Ansible Test Controller!"
```

Führe es aus:

```bash
make run
```

## 4. Häufige Kommandos

```bash
# Zeige alle verfügbaren Kommandos
make help

# Führe das Playbook aus
make run

# Validiere das Playbook
make lint

# Prüfe die Syntax
make syntax-check

# Öffne eine interaktive Shell
make shell
```

## 5. Nächste Schritte

- **Konfiguration**: Passe die `.env`-Datei an, um SSH-Keys, Vault-Passwörter und andere Einstellungen zu konfigurieren.
- **Troubleshooting**: Wenn Probleme auftreten, schaue in die [TROUBLESHOOT.md](TROUBLESHOOT.md).
- **Erweiterung**: Lese die [README.md](README.md), um zu erfahren, wie du das Projekt erweitern kannst (Rollen, Plugins, etc.).
