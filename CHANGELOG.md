# Changelog – Nova-Universe Control Center

Alle notablen Änderungen dieses Projekts werden in dieser Datei dokumentiert.

Format basiert auf [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- GitHub Actions CI Workflows (Ansible + Python Lint)
- Status Dashboard für Komponenten-Reifegrad
- Konsolidierte Getting-Started-Dokumentation
- 2-Phasen-Roadmap für Stabilisierung & Onboarding

### Changed
- PROJECT_CONTEXT aktualisiert (Semaphore Blocker → Gelöst)
- Repo-Cleanup: Backup-Artefakte archiviert
- Nova-World: Phase 5 Completion (Live Semaphore Integration)
- **YubiKey 2FA: Status → Complete (5/5)** 🗝️

### Fixed
- Shell Injection in Quick Actions (Commit d11b12f5)

---

## [1.0.0-beta.2] – 2026-01-11

### Added
- 🗝️ **YubiKey 2FA Integration – COMPLETE**
  - Hardware security key support
  - Dual-factor authentication for CLI & Web
  - Vault integration for key management
  - Emergency recovery codes
  - Full test coverage + documentation

### Changed
- Phase 5 Completion: All critical blockers resolved
- Infrastructure fully automated with Ansible
- Semaphore integration fully functional

---

## [1.0.0-beta.1] – 2026-01-10

### Added
- Initial unified repository (merge of Test-Controller + novachris_home)
- Nova-World UI with Streamlit dashboard
- Semaphore integration (REST API)
- 11 Ansible Roles (system_setup, docker_setup, app_deployment, etc.)
- Makefile-basierte Automation
- Comprehensive documentation (16 docs)

### Features
- Ansible Vault for Secrets Management
- Docker-based Test Environment
- Multi-Profile Deployment (minimal, standard, full, repair, custom)
- AI Assistant (Ollama integration)
- Quick Actions (Docker, System, Deployment)

---
