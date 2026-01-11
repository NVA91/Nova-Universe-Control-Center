# ============================================================================
# Dockerfile - Ansible Test Controller (v2.1 - mit Collections)
# ============================================================================
# Basis-Image: Ubuntu 22.04 LTS
# Enthält: Ansible, Python3, SSH-Tools, Linting-Tools, Galaxy Collections
#
# Build: docker-compose build --no-cache
# Run: docker-compose run --rm ansible-controller

ARG UBUNTU_VERSION=22.04
FROM ubuntu:${UBUNTU_VERSION}

# ============================================================================
# Metadaten
# ============================================================================

LABEL maintainer="Ansible Test Controller"
LABEL description="Docker-basierter Ansible-Test-Controller für lokale Entwicklung und CI/CD"
LABEL version="2.1"

# ============================================================================
# Build-Argumente
# ============================================================================

ARG ANSIBLE_VERSION=2.16.3
ARG PYTHON_VERSION=3

# ============================================================================
# Umgebungsvariablen
# ============================================================================

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ANSIBLE_FORCE_COLOR=1 \
    ANSIBLE_HOST_KEY_CHECKING=False \
    ANSIBLE_INVENTORY=./inventory \
    ANSIBLE_ROLES_PATH=./roles \
    ANSIBLE_LIBRARY=./library \
    ANSIBLE_LOOKUP_PLUGINS=./lookup_plugins \
    ANSIBLE_FORKS=5 \
    ANSIBLE_TIMEOUT=10

# ============================================================================
# SECTION 1: Basis-Pakete und Abhängigkeiten
# ============================================================================

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Basis-Tools
    curl \
    wget \
    git \
    vim \
    nano \
    less \
    \
    # Python und Ansible
    python${PYTHON_VERSION} \
    python3-pip \
    python${PYTHON_VERSION}-dev \
    python${PYTHON_VERSION}-venv \
    \
    # SSH und Verbindungs-Tools
    openssh-client \
    sshpass \
    \
    # Build-Tools (für Python-Pakete)
    build-essential \
    libssl-dev \
    libffi-dev \
    \
    # Netzwerk-Tools
    iputils-ping \
    dnsutils \
    \
    # Utilities
    jq \
    sudo \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ============================================================================
# SECTION 2: Ansible Core und Python-Tools installieren
# ============================================================================

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir \
    # Ansible Core
    ansible-core==${ANSIBLE_VERSION} \
    \
    # Ansible Collections und Tools
    ansible-lint \
    yamllint \
    \
    # Python-Abhängigkeiten für Ansible
    jinja2 \
    pyyaml \
    paramiko \
    cryptography \
    requests \
    netaddr \
    \
    # Zusätzliche Tools
    molecule \
    molecule-docker \
    pytest \
    testinfra \
    \
    # Linting und Validierung
    pylint \
    flake8 \
    black

# ============================================================================
# SECTION 2.5: Ansible Galaxy Collections (NEU & WICHTIG!)
# ============================================================================
# Hier installieren wir die fehlenden Module wie ansible.posix (sysctl)
# und community.docker (für Container-Handling).

RUN ansible-galaxy collection install \
    ansible.posix \
    community.general \
    community.docker \
    community.crypto

# ============================================================================
# SECTION 3: Ansible-Verzeichnisse erstellen
# ============================================================================

RUN mkdir -p /project \
    && mkdir -p /project/roles \
    && mkdir -p /project/inventory \
    && mkdir -p /project/library \
    && mkdir -p /project/lookup_plugins \
    && mkdir -p /project/filter_plugins \
    && mkdir -p /project/group_vars \
    && mkdir -p /project/host_vars \
    && mkdir -p /project/templates \
    && mkdir -p /project/files \
    && mkdir -p /project/vars \
    && mkdir -p /project/logs

# ============================================================================
# SECTION 4: Entrypoint-Script kopieren und konfigurieren
# ============================================================================

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# ============================================================================
# SECTION 5: Ansible-Konfiguration kopieren
# ============================================================================

COPY ansible.cfg /etc/ansible/ansible.cfg

# ============================================================================
# SECTION 6: Health-Check (optional)
# ============================================================================

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ansible-playbook --version > /dev/null 2>&1 || exit 1

# ============================================================================
# SECTION 7: Workdir und Entrypoint
# ============================================================================

WORKDIR /project

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["ansible-playbook", "--version"]