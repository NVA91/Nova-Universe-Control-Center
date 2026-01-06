#!/bin/bash
# ============================================================================
# Semaphore Setup Script
# ============================================================================
# Dieses Skript richtet Ansible Semaphore Web-UI ein
# ============================================================================

set -e

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktionen
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  Semaphore Setup - Unified Ansible Project                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
}

# Hauptskript
main() {
    print_header
    
    # 1. Prüfe Voraussetzungen
    print_info "Prüfe Voraussetzungen..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker ist nicht installiert!"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose ist nicht installiert!"
        exit 1
    fi
    
    print_success "Docker und Docker Compose sind installiert"
    
    # 2. Prüfe .env.semaphore
    if [ ! -f ".env.semaphore" ]; then
        print_error ".env.semaphore nicht gefunden!"
        print_info "Erstelle .env.semaphore aus Vorlage..."
        
        if [ -f ".env.semaphore.example" ]; then
            cp .env.semaphore.example .env.semaphore
            print_success ".env.semaphore erstellt"
        else
            print_error "Keine Vorlage gefunden!"
            exit 1
        fi
    fi
    
    # 3. Lade Umgebungsvariablen
    print_info "Lade Umgebungsvariablen..."
    source .env.semaphore
    
    # 4. Generiere sicheres Access Key (falls nicht gesetzt)
    if [ "$SEMAPHORE_ACCESS_KEY" == "your-secret-encryption-key-change-me-32chars" ]; then
        print_warning "Generiere sicheres Access Key..."
        NEW_KEY=$(openssl rand -hex 16)
        sed -i "s/SEMAPHORE_ACCESS_KEY=.*/SEMAPHORE_ACCESS_KEY=$NEW_KEY/" .env.semaphore
        print_success "Neues Access Key generiert"
    fi
    
    # 5. Erstelle notwendige Verzeichnisse
    print_info "Erstelle Verzeichnisse..."
    mkdir -p shared/templates/docker-compose
    mkdir -p .ssh
    print_success "Verzeichnisse erstellt"
    
    # 6. Prüfe SSH-Keys
    if [ ! -f ".ssh/id_ed25519" ]; then
        print_warning "SSH-Key nicht gefunden. Generiere neuen Key..."
        ssh-keygen -t ed25519 -f .ssh/id_ed25519 -N "" -C "semaphore@unified-ansible"
        print_success "SSH-Key generiert: .ssh/id_ed25519"
    else
        print_success "SSH-Key vorhanden"
    fi
    
    # 7. Setze Berechtigungen
    print_info "Setze Berechtigungen..."
    chmod 600 .ssh/id_ed25519 2>/dev/null || true
    chmod 644 .ssh/id_ed25519.pub 2>/dev/null || true
    print_success "Berechtigungen gesetzt"
    
    # 8. Erstelle docker-compose.yml für Semaphore
    print_info "Erstelle docker-compose.yml..."
    
    if [ ! -f "docker-compose.semaphore.yml" ]; then
        cp shared/templates/docker-compose/semaphore.yml docker-compose.semaphore.yml
        print_success "docker-compose.semaphore.yml erstellt"
    else
        print_warning "docker-compose.semaphore.yml existiert bereits"
    fi
    
    # 9. Starte Semaphore
    print_info "Starte Semaphore..."
    docker-compose -f docker-compose.semaphore.yml --env-file .env.semaphore up -d
    
    # 10. Warte auf Semaphore
    print_info "Warte auf Semaphore-Start (max. 60 Sekunden)..."
    
    COUNTER=0
    MAX_WAIT=60
    
    while [ $COUNTER -lt $MAX_WAIT ]; do
        if docker-compose -f docker-compose.semaphore.yml ps | grep -q "Up"; then
            if curl -s http://localhost:${SEMAPHORE_PORT:-3000}/api/ping > /dev/null 2>&1; then
                print_success "Semaphore ist bereit!"
                break
            fi
        fi
        
        sleep 2
        COUNTER=$((COUNTER + 2))
        echo -n "."
    done
    
    echo ""
    
    if [ $COUNTER -ge $MAX_WAIT ]; then
        print_warning "Timeout erreicht. Prüfe Logs mit: docker-compose -f docker-compose.semaphore.yml logs"
    fi
    
    # 11. Zeige Zugriffsinformationen
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  Semaphore erfolgreich gestartet!                             ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    print_success "URL: http://localhost:${SEMAPHORE_PORT:-3000}"
    print_success "Benutzername: ${SEMAPHORE_ADMIN_USER:-admin}"
    print_success "Passwort: ${SEMAPHORE_ADMIN_PASSWORD:-changeme}"
    echo ""
    print_warning "WICHTIG: Ändere das Admin-Passwort nach dem ersten Login!"
    echo ""
    print_info "Nächste Schritte:"
    echo "  1. Öffne http://localhost:${SEMAPHORE_PORT:-3000} im Browser"
    echo "  2. Logge dich mit den obigen Credentials ein"
    echo "  3. Erstelle ein neues Projekt"
    echo "  4. Füge dein Inventory hinzu"
    echo "  5. Erstelle Task Templates für deine Playbooks"
    echo ""
    print_info "Logs anzeigen: docker-compose -f docker-compose.semaphore.yml logs -f"
    print_info "Stoppen: docker-compose -f docker-compose.semaphore.yml down"
    echo ""
}

# Skript ausführen
main "$@"
