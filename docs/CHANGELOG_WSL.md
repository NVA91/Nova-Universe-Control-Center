# Changelog - WSL-Optimierung (v2.0)

Dieses Changelog dokumentiert alle Änderungen, die für die Unterstützung von WSL (Windows Subsystem for Linux) und VS Code vorgenommen wurden.

## Version 2.0 - WSL & VS Code Integration

### 🆕 Neue Dateien

#### VS Code Integration
- **`.vscode/settings.json`**: Projekt-spezifische VS Code Einstellungen
  - YAML/Ansible-Konfiguration mit Prettier-Formatter
  - Python-Linting und Formatierung mit Black
  - Shell-Script-Formatierung mit shfmt
  - Ansible-Validierung und Linting
  - Exclude-Muster für Binärdateien und Cache

- **`.vscode/extensions.json`**: Empfohlene VS Code Extensions
  - Ansible, Python, Shell, Docker, Git, Remote Development
  - Linting und Formatierung Tools
  - Markdown und Dokumentation Support

- **`.vscode/launch.json`**: Debug-Konfigurationen
  - Ansible Playbook Debugging
  - Python Debugging
  - Bash/Shell Debugging
  - Compound Configurations

- **`.devcontainer/devcontainer.json`**: Dev Container Konfiguration
  - Docker Compose Integration
  - Automatische Extension-Installation
  - SSH-Key Mounting
  - Umgebungsvariablen für Ansible

#### Windows-kompatible Scripts
- **`ansible-controller.ps1`**: PowerShell Wrapper
  - Alle Makefile-Kommandos von PowerShell aus erreichbar
  - Farbige Ausgabe und Fehlerbehandlung
  - Einfache Verwendung: `.\ansible-controller.ps1 build`

- **`ansible-controller.bat`**: Batch Wrapper
  - Alle Makefile-Kommandos von CMD aus erreichbar
  - Einfache Verwendung: `ansible-controller.bat build`

#### Konfigurationsdateien
- **`.editorconfig`**: Editor-Konfiguration für konsistente Einstellungen
  - Konsistente Line Endings (LF)
  - Konsistente Indentation
  - Charset UTF-8
  - Editor-unabhängig (VS Code, Vim, etc.)

- **`.gitattributes`**: Git-Konfiguration für WSL/Windows
  - Konsistente Line Ending Behandlung
  - Bash-Scripts: LF
  - YAML, Python, Dockerfile: LF
  - Binärdateien korrekt gekennzeichnet

#### Dokumentation
- **`WSL_SETUP.md`**: Detaillierte WSL-Setup-Anleitung
  - Schritt-für-Schritt Anleitung
  - Dev Container Setup
  - PowerShell/CMD Verwendung
  - WSL-spezifisches Troubleshooting

- **`CHANGELOG_WSL.md`**: Dieses Changelog

### 🔄 Geänderte Dateien

- **`README.md`**: 
  - WSL-Setup-Anleitung hinzugefügt
  - Link zu WSL_SETUP.md
  - Hinweis auf Windows-kompatible Scripts

### ✨ Features

#### VS Code Integration
- **Dev Container Support**: Vollständige Entwicklungsumgebung im Container
- **Remote WSL Support**: Nahtlose Integration mit WSL
- **Debugging**: Ansible, Python und Bash Debugging
- **Linting & Formatting**: Automatische Code-Validierung
- **Extensions**: Empfohlene Extensions für schnelle Einrichtung

#### Windows-Kompatibilität
- **PowerShell Wrapper**: Moderne PowerShell-Integration
- **Batch Wrapper**: Klassische CMD-Unterstützung
- **Line Ending Management**: Automatische LF-Konvertierung
- **Path Handling**: Korrekte Pfade für Windows/WSL

#### Editor-Konfiguration
- **`.editorconfig`**: Konsistente Einstellungen für alle Editoren
- **`.gitattributes`**: Konsistente Git-Behandlung
- **VS Code Settings**: Umfassende Projekt-Einstellungen

### 🛠️ Technische Details

#### Line Endings
- Alle Shell-Scripts, YAML, Python und Konfigurationsdateien verwenden LF
- `.gitattributes` stellt sicher, dass Git die Konvertierung korrekt durchführt
- `.editorconfig` stellt sicher, dass Editoren die richtigen Einstellungen verwenden

#### Dev Container
- Basiert auf `docker-compose.yml`
- Automatische Extension-Installation
- SSH-Key Mounting für Git-Operationen
- Umgebungsvariablen für Ansible

#### PowerShell Wrapper
- Vollständige Fehlerbehandlung
- Farbige Ausgabe
- Alle Makefile-Kommandos unterstützt
- Einfache Verwendung von Windows aus

### 📚 Dokumentation

- **WSL_SETUP.md**: Detaillierte Anleitung für WSL-Benutzer
- **README.md**: Aktualisiert mit WSL-Hinweisen
- **TROUBLESHOOT.md**: WSL-spezifische Troubleshooting-Tipps

### 🔐 Sicherheit

- SSH-Keys werden korrekt gemountet
- `.env`-Dateien sind in `.gitignore`
- Vault-Unterstützung bleibt erhalten

### 🚀 Performance

- Line Ending Handling reduziert Git-Konflikte
- Dev Container ermöglicht schnelle Entwicklung
- Caching für Docker-Builds

### 📋 Kompatibilität

- **Windows 10/11**: Vollständig unterstützt
- **WSL2**: Erforderlich für Docker
- **VS Code**: Remote WSL Extension erforderlich
- **Docker Desktop**: Muss für WSL2 konfiguriert sein

### 🔄 Migration

Bestehende Projekte können einfach aktualisiert werden:

1. Kopiere `.editorconfig` und `.gitattributes`
2. Kopiere `.vscode/` und `.devcontainer/` Verzeichnisse
3. Kopiere `ansible-controller.ps1` und `ansible-controller.bat`
4. Aktualisiere `README.md` mit WSL-Hinweisen

### 📝 Hinweise

- Die Änderungen sind vollständig rückwärts-kompatibel
- Bestehende Funktionalität bleibt erhalten
- Alle neuen Features sind optional
- WSL-Benutzer profitieren am meisten von den Änderungen

### 🙏 Danksagungen

Diese WSL-Optimierung wurde durchgeführt, um die Entwicklungserfahrung für Windows-Benutzer zu verbessern, die WSL und VS Code verwenden.
