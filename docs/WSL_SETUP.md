# WSL Setup - Ansible Test Controller (v2.0)

Diese Anleitung beschreibt die Einrichtung des Ansible Test Controllers unter WSL (Windows Subsystem for Linux) mit VS Code.

## 1. Voraussetzungen

- **Windows 10/11**: Aktuelle Version mit aktiviertem WSL2.
- **WSL2**: Installiert und konfiguriert. [Anleitung](https://docs.microsoft.com/de-de/windows/wsl/install)
- **Docker Desktop**: Installiert und für WSL2 konfiguriert. [Anleitung](https://docs.docker.com/desktop/windows/wsl/)
- **VS Code**: Installiert mit der "Remote - WSL"-Extension. [Anleitung](https://code.visualstudio.com/docs/remote/wsl)

## 2. Setup

### Schritt 1: Projekt in WSL klonen

Öffne eine WSL-Shell (z.B. Ubuntu) und klone das Projekt:

```bash
git clone https://github.com/your-repo/ansible-test-controller.git
cd ansible-test-controller
```

### Schritt 2: Projekt in VS Code öffnen

Öffne das Projekt in VS Code über die WSL-Shell:

```bash
code .
```

VS Code wird das Projekt im WSL-Kontext öffnen. Es wird empfohlen, die empfohlenen Extensions zu installieren.

### Schritt 3: Dev Container starten

VS Code wird automatisch erkennen, dass eine Dev-Container-Konfiguration vorhanden ist. Klicke auf "Reopen in Container", um die Entwicklungsumgebung zu starten.

Alternativ kannst du die Command Palette öffnen (`Ctrl+Shift+P`) und "Remote-Containers: Reopen in Container" auswählen.

### Schritt 4: Konfiguration

Kopiere die `.env.example`-Datei zu `.env` und passe die Werte an:

```bash
cp .env.example .env
```

### Schritt 5: Build und Test

Öffne ein neues Terminal in VS Code (`Ctrl+Shift+` `) und führe die folgenden Kommandos aus:

```bash
# Baue das Docker-Image
make build

# Führe die Tests aus
make test

# Führe das Beispiel-Playbook aus
make run
```

## 3. Windows PowerShell / CMD

Du kannst das Projekt auch direkt von Windows PowerShell oder CMD aus steuern.

### PowerShell

```powershell
# Baue das Image
.\ansible-controller.ps1 build

# Führe das Playbook aus
.\ansible-controller.ps1 run
```

### CMD

```batch
# Baue das Image
ansible-controller.bat build

# Führe das Playbook aus
ansible-controller.bat run
```

## 4. Troubleshooting

### Fehler: `docker-compose: command not found`

**Lösung**: Stelle sicher, dass Docker Desktop installiert und für WSL2 konfiguriert ist. Überprüfe die Einstellungen in Docker Desktop -> Settings -> Resources -> WSL Integration.

### Fehler: `permission denied while trying to connect to the Docker daemon socket`

**Lösung**: Stelle sicher, dass dein WSL-Benutzer zur `docker`-Gruppe gehört. Führe `sudo usermod -aG docker $USER` in der WSL-Shell aus und starte die Shell neu.

### Fehler: `Line endings`

**Lösung**: Das Projekt enthält `.editorconfig` und `.gitattributes`, um konsistente Line Endings sicherzustellen. Wenn du Probleme hast, überprüfe die Einstellungen in VS Code (`files.eol`).

### Fehler: `Cannot find module '...'.`

**Lösung**: Stelle sicher, dass du dich im Dev Container befindest, wenn du Ansible-Kommandos ausführst. Das Terminal in VS Code sollte "Dev Container: Ansible Test Controller" anzeigen.

## 5. Empfohlene VS Code Einstellungen

Das Projekt enthält eine `.vscode/settings.json`-Datei mit empfohlenen Einstellungen. Es wird empfohlen, diese zu verwenden, um eine konsistente Entwicklungserfahrung zu gewährleisten.

## 6. Weitere Hilfe

Wenn du weitere Hilfe benötigst, schaue in die [TROUBLESHOOT.md](TROUBLESHOOT.md) oder öffne ein [Issue](https://github.com/your-repo/ansible-test-controller/issues).
