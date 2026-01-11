# ============================================================================
# Makefile - Unified Ansible Project
# ============================================================================
# Vereinheitlichte Einstiegspunkte für lokales Testing und Produktions-Deployment
# 
# Verwendung:
#   make test              - Lokales Testing im Docker-Container
#   make deploy            - Produktions-Deployment auf Proxmox
#   make help              - Zeige alle verfügbaren Kommandos

.PHONY: help build test deploy clean shell lint syntax-check version info semaphore-setup semaphore-start semaphore-stop semaphore-logs semaphore-backup

# ============================================================================
# Variablen
# ============================================================================

DOCKER_COMPOSE := docker-compose -f controller/docker-compose.yml
PROJECT_NAME := unified-ansible-project
CONTAINER_NAME := ansible-controller

# Playbook-Variablen
PLAYBOOK ?= infrastructure/site.yml
PROFILE ?= standard
ANSIBLE_VERBOSITY ?= 0

# Git-Informationen
GIT_HASH := $(shell git rev-parse --short HEAD 2>/dev/null || echo "local")
BUILD_DATE := $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')

# ============================================================================
# Haupt-Ziele
# ============================================================================

help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║  Unified Ansible Project - Makefile                           ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 SETUP & BUILD"
	@echo "  make build             - Baue Docker-Image für Test-Controller"
	@echo "  make clean             - Lösche Container, Images und Caches"
	@echo ""
	@echo "🧪 TESTING (lokal im Container)"
	@echo "  make test              - Führe alle Tests durch (Syntax + Lint)"
	@echo "  make test-playbook     - Teste spezifisches Playbook"
	@echo "  make lint              - Führe ansible-lint aus"
	@echo "  make syntax-check      - Prüfe Playbook-Syntax"
	@echo "  make shell             - Öffne interaktive Shell im Container"
	@echo ""
	@echo "🚀 DEPLOYMENT (auf Proxmox)"
	@echo "  make deploy            - Standard-Deployment (profile_standard.yml)"
	@echo "  make deploy-full       - Vollständiges Deployment (alle VMs + Apps)"
	@echo "  make deploy-minimal    - Minimales Deployment (nur Gateway)"
	@echo "  make deploy-custom     - Interaktives Deployment"
	@echo "  make deploy-repair     - Reparatur-Modus"
	@echo ""
	@echo "🖥️  WEB-UI (Semaphore)"
	@echo "  make semaphore-setup   - Richte Semaphore Web-UI ein"
	@echo "  make semaphore-start   - Starte Semaphore"
	@echo "  make semaphore-stop    - Stoppe Semaphore"
	@echo "  make semaphore-logs    - Zeige Semaphore-Logs"
	@echo "  make semaphore-backup  - Erstelle Semaphore-Backup"
	@echo ""
	@echo ""
	@echo "ℹ️  INFORMATIONEN"
	@echo "  make info              - Zeige Projekt-Informationen"
	@echo "  make version           - Zeige Versionen"
	@echo "  make inventory         - Zeige Inventory"
	@echo ""
	@echo "📝 VARIABLEN"
	@echo "  PLAYBOOK=<file>        - Anderes Playbook (Standard: infrastructure/site.yml)"
	@echo "  PROFILE=<name>         - Deployment-Profil (Standard: standard)"
	@echo "  ANSIBLE_VERBOSITY=<n>  - Verbosity-Level 0-4 (Standard: 0)"
	@echo ""
	@echo "💡 BEISPIELE"
	@echo "  make build"
	@echo "  make test"
	@echo "  make deploy"
	@echo "  make deploy-full"
	@echo "  make shell"
	@echo ""

# ============================================================================
# Setup & Build
# ============================================================================

build:
	@echo "🔨 Baue Docker-Image..."
	@cd controller && $(DOCKER_COMPOSE) build
	@echo "✅ Build abgeschlossen!"

clean:
	@echo "🧹 Räume auf..."
	@cd controller && $(DOCKER_COMPOSE) down -v
	@docker rmi $(PROJECT_NAME):latest 2>/dev/null || true
	@rm -rf controller/logs/* infrastructure/logs/* 2>/dev/null || true
	@echo "✅ Aufgeräumt!"

# ============================================================================
# Testing (lokal im Container)
# ============================================================================

test: lint syntax-check
	@echo ""
	@echo "✅ Alle Tests erfolgreich!"

test-playbook:
	@echo "🧪 Teste Playbook: $(PLAYBOOK)"
	@$(DOCKER_COMPOSE) run --rm $(CONTAINER_NAME) \
		ansible-playbook /project/$(PLAYBOOK) --syntax-check
	@echo "✅ Playbook-Test erfolgreich!"

lint:
	@echo "🔍 Führe ansible-lint aus..."
	@$(DOCKER_COMPOSE) run --rm $(CONTAINER_NAME) \
		ansible-lint /project/infrastructure/site.yml || true

syntax-check:
	@$(DOCKER_COMPOSE) run --rm $(CONTAINER_NAME) \
		ansible-playbook /project/infrastructure/site.yml --syntax-check
	@echo "✅ Syntax-Check erfolgreich!"

shell:
	@echo "🐚 Öffne interaktive Shell im Container..."
	@cd controller && $(DOCKER_COMPOSE) run --rm -it $(CONTAINER_NAME) bash

# ============================================================================
# Deployment (auf Proxmox)
# ============================================================================

deploy:
	@echo "🚀 Starte Standard-Deployment..."
	@cd infrastructure && ansible-playbook site.yml -e "@config/profile_standard.yml"
	@echo "✅ Deployment abgeschlossen!"

deploy-full:
	@echo "🚀 Starte vollständiges Deployment (alle VMs + Apps)..."
	@cd infrastructure && ansible-playbook site.yml -e "@config/profile_full.yml"
	@echo "✅ Deployment abgeschlossen!"

deploy-minimal:
	@echo "🚀 Starte minimales Deployment..."
	@cd infrastructure && ansible-playbook site.yml -e "@config/profile_minimal.yml"
	@echo "✅ Deployment abgeschlossen!"

deploy-custom:
	@echo "🚀 Starte interaktives Deployment..."
	@cd infrastructure && ansible-playbook site.yml -e "@config/profile_custom.yml"
	@echo "✅ Deployment abgeschlossen!"

deploy-repair:
	@echo "🔧 Starte Reparatur-Modus..."
	@cd infrastructure && ansible-playbook site.yml -e "@config/profile_repair.yml"
	@echo "✅ Reparatur abgeschlossen!"

# ============================================================================
# Erweiterte Deployment-Optionen
# ============================================================================

deploy-dry-run:
	@echo "🔍 Führe Deployment im Dry-Run aus..."
	@cd infrastructure && ansible-playbook site.yml -e "@config/profile_$(PROFILE).yml" --check

deploy-verbose:
	@echo "🔊 Führe Deployment mit Verbose-Output aus..."
	@cd infrastructure && ansible-playbook site.yml -e "@config/profile_$(PROFILE).yml" -vvv

# ============================================================================
# Informationen
# ============================================================================

info:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║  Unified Ansible Project - Informationen                      ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📂 Projekt-Struktur:"
	@echo "   controller/         - Docker-basierte Testumgebung"
	@echo "   infrastructure/     - Produktions-Infrastruktur (Proxmox)"
	@echo "   shared/             - Gemeinsame Rollen, Templates, Plugins"
	@echo "   examples/           - Beispiel-Playbooks"
	@echo "   tests/              - Test-Playbooks"
	@echo "   docs/               - Dokumentation"
	@echo ""
	@echo "🔧 Build-Informationen:"
	@echo "   Git Hash:    $(GIT_HASH)"
	@echo "   Build Date:  $(BUILD_DATE)"
	@echo ""
	@echo "📚 Dokumentation:"
	@echo "   README:              docs/README_INFRASTRUCTURE.md"
	@echo "   Quickstart:          docs/QUICKSTART.md"
	@echo "   Architektur:         docs/IMPLEMENTATION_GUIDE.md"
	@echo "   Troubleshooting:     docs/TROUBLESHOOT.md"
	@echo ""

version:
	@echo "📦 Versionen:"
	@echo ""
	@cd controller && $(DOCKER_COMPOSE) run --rm $(CONTAINER_NAME) ansible --version
	@echo ""
	@cd controller && $(DOCKER_COMPOSE) run --rm $(CONTAINER_NAME) python3 --version

inventory:
	@echo "📋 Zeige Inventory..."
	@cd infrastructure && ansible-inventory -i inventory/hosts.yml --list

# ============================================================================
# Utility-Kommandos
# ============================================================================

setup-prod:
	@echo "🔐 Richte Produktionsumgebung ein..."
	@bash scripts/setup_prod_env.sh
	@echo "✅ Produktionsumgebung eingerichtet!"

logs:
	@echo "📜 Zeige Logs..."
	@tail -f infrastructure/logs/ansible.log

# ============================================================================
# Semaphore Web-UI
# ============================================================================

semaphore-setup:
	@echo "🖥️  Richte Semaphore Web-UI ein..."
	@bash scripts/setup_semaphore.sh
	@echo "✅ Semaphore eingerichtet!"

semaphore-start:
	@echo "▶️  Starte Semaphore..."
	@docker-compose -f docker-compose.semaphore.yml --env-file .env.semaphore up -d
	@echo "✅ Semaphore gestartet: http://localhost:3000"

semaphore-stop:
	@echo "⏹️  Stoppe Semaphore..."
	@docker-compose -f docker-compose.semaphore.yml down
	@echo "✅ Semaphore gestoppt!"

semaphore-logs:
	@echo "📜 Zeige Semaphore-Logs..."
	@docker-compose -f docker-compose.semaphore.yml logs -f

semaphore-restart:
	@echo "🔄 Starte Semaphore neu..."
	@docker-compose -f docker-compose.semaphore.yml restart
	@echo "✅ Semaphore neu gestartet!"

semaphore-backup:
	@echo "💾 Erstelle Semaphore-Backup..."
	@mkdir -p backups
	@docker-compose -f docker-compose.semaphore.yml exec -T semaphore-db \
		pg_dump -U semaphore semaphore > backups/semaphore_backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup erstellt: backups/semaphore_backup_$$(date +%Y%m%d_%H%M%S).sql"

semaphore-restore:
	@echo "📥 Stelle Semaphore-Backup wieder her..."
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "❌ Fehler: BACKUP_FILE nicht gesetzt. Verwendung: make semaphore-restore BACKUP_FILE=backups/semaphore_backup_20260103.sql"; \
		exit 1; \
	fi
	@cat $(BACKUP_FILE) | docker-compose -f docker-compose.semaphore.yml exec -T semaphore-db \
		psql -U semaphore semaphore
	@echo "✅ Backup wiederhergestellt!"

# ============================================================================
# Standardziel
# ============================================================================

.DEFAULT_GOAL := help
