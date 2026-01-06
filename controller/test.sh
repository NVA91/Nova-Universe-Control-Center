#!/bin/bash

# ============================================================================
# test.sh - Ansible Test Controller Test-Suite (v2.0)
# ============================================================================
# Führt eine Reihe von Tests durch, um die Funktionsfähigkeit des
# Ansible Test Controllers zu überprüfen.

set -euo pipefail

# ============================================================================
# Konfiguration
# ============================================================================

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="${SCRIPT_DIR}"

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test-Zähler
TESTS_PASSED=0
TESTS_FAILED=0

# ============================================================================
# Hilfsfunktionen
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

log_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# ============================================================================
# Tests
# ============================================================================

test_docker_installed() {
    log_section "Test 1: Docker Installation"
    
    if command -v docker &> /dev/null; then
        local version
        version=$(docker --version)
        log_success "Docker installiert: $version"
    else
        log_error "Docker nicht installiert"
    fi
}

test_docker_compose_installed() {
    log_section "Test 2: Docker Compose Installation"
    
    if command -v docker-compose &> /dev/null; then
        local version
        version=$(docker-compose --version)
        log_success "Docker Compose installiert: $version"
    else
        log_error "Docker Compose nicht installiert"
    fi
}

test_project_structure() {
    log_section "Test 3: Projektstruktur"
    
    # Prüfe wichtige Dateien
    local files=(
        "Dockerfile"
        "docker-compose.yml"
        "entrypoint.sh"
        "ansible.cfg"
        ".env.example"
        "Makefile"
        "README.md"
        "QUICKSTART.md"
        "TROUBLESHOOT.md"
    )
    
    for file in "${files[@]}"; do
        if [[ -f "$PROJECT_DIR/$file" ]]; then
            log_success "Datei vorhanden: $file"
        else
            log_error "Datei fehlt: $file"
        fi
    done
}

test_dockerfile() {
    log_section "Test 4: Dockerfile Validierung"
    
    if docker build -t ansible-controller:test . > /dev/null 2>&1; then
        log_success "Dockerfile erfolgreich gebaut"
        docker rmi ansible-controller:test > /dev/null 2>&1 || true
    else
        log_error "Dockerfile Build fehlgeschlagen"
    fi
}

test_makefile() {
    log_section "Test 5: Makefile Validierung"
    
    if make help > /dev/null 2>&1; then
        log_success "Makefile funktioniert"
    else
        log_error "Makefile fehlgeschlagen"
    fi
}

test_entrypoint() {
    log_section "Test 6: entrypoint.sh Validierung"
    
    if [[ -x "$PROJECT_DIR/entrypoint.sh" ]]; then
        log_success "entrypoint.sh ist ausführbar"
    else
        log_error "entrypoint.sh ist nicht ausführbar"
    fi
}

test_env_example() {
    log_section "Test 7: .env.example Validierung"
    
    if [[ -f "$PROJECT_DIR/.env.example" ]]; then
        local var_count
        var_count=$(grep -c "^[A-Z_]*=" "$PROJECT_DIR/.env.example" || true)
        log_success ".env.example enthält $var_count Variablen"
    else
        log_error ".env.example nicht gefunden"
    fi
}

# ============================================================================
# Zusammenfassung
# ============================================================================

print_summary() {
    log_section "Test-Zusammenfassung"
    
    local total=$((TESTS_PASSED + TESTS_FAILED))
    echo "Gesamt Tests: $total"
    echo -e "Bestanden: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Fehlgeschlagen: ${RED}$TESTS_FAILED${NC}"
    echo ""
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ Alle Tests bestanden!${NC}"
        return 0
    else
        echo -e "${RED}✗ Einige Tests fehlgeschlagen!${NC}"
        return 1
    fi
}

# ============================================================================
# Hauptprogramm
# ============================================================================

main() {
    log_section "Ansible Test Controller - Test-Suite"
    
    test_docker_installed
    test_docker_compose_installed
    test_project_structure
    test_dockerfile
    test_makefile
    test_entrypoint
    test_env_example
    
    print_summary
}

main "$@"
