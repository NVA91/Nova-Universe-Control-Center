#!/bin/bash

# ============================================================================
# entrypoint.sh - Ansible Test Controller Entrypoint (v2.0)
# ============================================================================
# Refaktoriert für bessere Fehlerbehandlung, Preflight-Checks und
# einheitliche Einstiegspunkte. Keine Funktionsverluste.

set -euo pipefail

# ============================================================================
# SECTION 1: Konfiguration und Konstanten
# ============================================================================

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="${PROJECT_DIR:-/project}"
readonly ANSIBLE_VERBOSITY="${ANSIBLE_VERBOSITY:-0}"
readonly PLAYBOOK_NAMES=("site.yml" "playbook.yml" "main.yml")

# Exit-Codes
readonly EXIT_SUCCESS=0
readonly EXIT_MISSING_DEPS=1
readonly EXIT_INVALID_PROJECT=2
readonly EXIT_PLAYBOOK_ERROR=3
readonly EXIT_CONFIG_ERROR=4

# ============================================================================
# SECTION 2: Farben und Formatierung
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging-Funktionen
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[✗]${NC} $1" >&2
}

log_section() {
    echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# ============================================================================
# SECTION 3: Hilfsfunktionen
# ============================================================================

# Prüfe ob ein Kommando existiert
command_exists() {
    command -v "$1" &> /dev/null
}

# Prüfe ob eine Datei existiert
file_exists() {
    [[ -f "$1" ]]
}

# Prüfe ob ein Verzeichnis existiert
dir_exists() {
    [[ -d "$1" ]]
}

# Finde das erste existierende Playbook
find_playbook() {
    for playbook in "${PLAYBOOK_NAMES[@]}"; do
        if file_exists "$PROJECT_DIR/$playbook"; then
            echo "$playbook"
            return $EXIT_SUCCESS
        fi
    done
    return 1
}

# Zeige Fehler und beende
die() {
    local exit_code="${2:-$EXIT_INVALID_PROJECT}"
    log_error "$1"
    exit "$exit_code"
}

# ============================================================================
# SECTION 4: Preflight-Checks
# ============================================================================

check_dependencies() {
    log_section "Prüfe Abhängigkeiten"
    
    local missing_deps=0
    
    # Prüfe Ansible
    if ! command_exists ansible-playbook; then
        log_error "ansible-playbook nicht gefunden"
        missing_deps=$((missing_deps + 1))
    else
        local ansible_version
        ansible_version=$(ansible-playbook --version | head -1)
        log_success "Ansible: $ansible_version"
    fi
    
    # Prüfe Python
    if ! command_exists python3; then
        log_error "python3 nicht gefunden"
        missing_deps=$((missing_deps + 1))
    else
        local python_version
        python_version=$(python3 --version)
        log_success "Python: $python_version"
    fi
    
    # Prüfe SSH (optional, aber empfohlen)
    if ! command_exists ssh; then
        log_warning "ssh nicht gefunden (optional)"
    else
        log_success "SSH: verfügbar"
    fi
    
    # Prüfe ansible-lint (optional)
    if ! command_exists ansible-lint; then
        log_warning "ansible-lint nicht gefunden (optional)"
    else
        log_success "ansible-lint: verfügbar"
    fi
    
    if [[ $missing_deps -gt 0 ]]; then
        die "Erforderliche Abhängigkeiten fehlen ($missing_deps)" "$EXIT_MISSING_DEPS"
    fi
}

check_project_structure() {
    log_section "Validiere Projektstruktur"
    
    # Prüfe ob Projekt-Verzeichnis existiert
    if ! dir_exists "$PROJECT_DIR"; then
        die "Projekt-Verzeichnis nicht gefunden: $PROJECT_DIR" "$EXIT_INVALID_PROJECT"
    fi
    log_success "Projekt-Verzeichnis: $PROJECT_DIR"
    
    # Prüfe auf Playbook
    if ! find_playbook > /dev/null 2>&1; then
        log_warning "Kein Playbook gefunden (site.yml, playbook.yml, main.yml)"
        PLAYBOOK_FOUND=false
    else
        PLAYBOOK_FOUND=true
        PLAYBOOK=$(find_playbook)
        log_success "Playbook gefunden: $PLAYBOOK"
    fi
    
    # Prüfe auf Inventory (optional, aber empfohlen)
    if dir_exists "$PROJECT_DIR/inventory" || file_exists "$PROJECT_DIR/inventory"; then
        log_success "Inventory: gefunden"
        INVENTORY_FOUND=true
    else
        log_warning "Inventory nicht gefunden (optional)"
        INVENTORY_FOUND=false
    fi
    
    # Prüfe auf Rollen (optional)
    if dir_exists "$PROJECT_DIR/roles"; then
        local role_count
        role_count=$(find "$PROJECT_DIR/roles" -maxdepth 1 -type d ! -name "roles" | wc -l)
        if [[ $role_count -gt 0 ]]; then
            log_success "Rollen: $role_count gefunden"
        else
            log_warning "Rollen-Verzeichnis leer"
        fi
    fi
    
    # Prüfe auf .env (optional, aber empfohlen)
    if file_exists "$PROJECT_DIR/.env"; then
        log_success ".env: gefunden"
        ENV_FOUND=true
    else
        log_warning ".env nicht gefunden (optional)"
        ENV_FOUND=false
    fi
}

check_ansible_config() {
    log_section "Prüfe Ansible-Konfiguration"
    
    # Prüfe ob ansible.cfg existiert
    if file_exists "$PROJECT_DIR/ansible.cfg"; then
        log_success "ansible.cfg: gefunden"
    elif file_exists "/etc/ansible/ansible.cfg"; then
        log_success "ansible.cfg: Standard-Konfiguration"
    else
        log_warning "ansible.cfg nicht gefunden (verwendet Defaults)"
    fi
    
    # Zeige Ansible-Konfiguration
    log_info "Ansible-Umgebung:"
    echo -e "  - Host Key Checking: ${ANSIBLE_HOST_KEY_CHECKING:-False}"
    echo -e "  - Inventory: ${ANSIBLE_INVENTORY:-./inventory}"
    echo -e "  - Roles Path: ${ANSIBLE_ROLES_PATH:-./roles}"
    echo -e "  - Verbosity: $ANSIBLE_VERBOSITY"
}

# ============================================================================
# SECTION 5: Hauptlogik
# ============================================================================

main() {
    # Führe Preflight-Checks durch
    check_dependencies
    check_project_structure
    check_ansible_config
    
    # Verarbeite Kommandos
    if [[ $# -gt 0 ]]; then
        # Explizites Kommando übergeben
        log_section "Führe Kommando aus"
        log_info "Kommando: $*"
        exec "$@"
    elif [[ "$PLAYBOOK_FOUND" == true ]]; then
        # Playbook gefunden - führe es aus
        log_section "Führe Playbook aus: $PLAYBOOK"
        
        # Bestimme Inventory-Pfad
        local inventory_arg
        if [[ "$INVENTORY_FOUND" == true ]]; then
            inventory_arg="-i $PROJECT_DIR/inventory"
        else
            log_warning "Verwende localhost als Inventory"
            inventory_arg="-i localhost,"
        fi
        
        # Baue Verbosity-Flags
        local verbosity_flags=""
        for ((i = 0; i < ANSIBLE_VERBOSITY; i++)); do
            verbosity_flags="${verbosity_flags}v"
        done
        if [[ -n "$verbosity_flags" ]]; then
            verbosity_flags="-${verbosity_flags}"
        fi
        
        # Führe Playbook aus
        cd "$PROJECT_DIR"
        exec ansible-playbook "$PLAYBOOK" $inventory_arg $verbosity_flags "$@"
    else
        # Kein Playbook gefunden - zeige Hilfe
        log_section "Keine Playbooks gefunden"
        show_help
        exit $EXIT_INVALID_PROJECT
    fi
}

show_help() {
    cat <<EOF

${CYAN}Verfügbare Kommandos:${NC}

  # Zeige Ansible-Version
  docker-compose run --rm ansible-controller ansible --version

  # Validiere Playbook-Syntax
  docker-compose run --rm ansible-controller ansible-playbook site.yml --syntax-check

  # Führe Playbook im Dry-Run aus
  docker-compose run --rm ansible-controller ansible-playbook site.yml --check

  # Führe Playbook mit Verbose-Output aus
  docker-compose run --rm ansible-controller ansible-playbook site.yml -v

  # Öffne eine interaktive Shell
  docker-compose run --rm ansible-controller bash

  # Verwende Makefile-Kommandos
  make help
  make run
  make lint
  make syntax-check

${CYAN}Weitere Informationen:${NC}
  - README.md: Umfassende Dokumentation
  - QUICKSTART.md: Schnelleinstieg
  - TROUBLESHOOT.md: Häufige Probleme und Lösungen

EOF
}

# ============================================================================
# SECTION 6: Fehlerbehandlung
# ============================================================================

trap 'log_error "Script abgebrochen"; exit $EXIT_INVALID_PROJECT' INT TERM

# ============================================================================
# SECTION 7: Script-Start
# ============================================================================

main "$@"
