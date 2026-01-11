# Docker Services Role

Manages containerized services for the Local AI Office Stack.

## Services
- **Semaphore** – Ansible UI & Automation
- **PostgreSQL** – Database backend
- **Traefik** – Self-Signed HTTPS Proxy

## Usage
ansible-playbook infrastructure/playbooks/deploy-proxmox-stack.yml --tags docker
