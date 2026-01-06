# Troubleshooting - Ansible Test Controller (v2.0)

Dieses Dokument listet häufige Probleme und deren Lösungen auf.

## 1. Docker & Docker Compose

### Fehler: `docker-compose: command not found`

**Lösung**: Stelle sicher, dass Docker Compose installiert ist. Folge der [offiziellen Anleitung](https://docs.docker.com/compose/install/).

### Fehler: `permission denied while trying to connect to the Docker daemon socket`

**Lösung**: Füge deinen Benutzer zur `docker`-Gruppe hinzu:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Fehler: `no space left on device`

**Lösung**: Räume ungenutzte Docker-Ressourcen auf:

```bash
docker system prune -a
```

## 2. Ansible & Playbooks

### Fehler: `ERROR! the playbook: site.yml could not be found`

**Lösung**: Stelle sicher, dass eine `site.yml`, `playbook.yml` oder `main.yml` im Projektverzeichnis existiert. Du kannst auch ein anderes Playbook angeben:

```bash
make run PLAYBOOK=my-playbook.yml
```

### Fehler: `Failed to connect to the host via ssh: Permission denied`

**Lösung**: Überprüfe deine SSH-Konfiguration:

1. **SSH-Keys**: Stelle sicher, dass deine SSH-Keys im `.ssh/`-Verzeichnis liegen und in der `.env`-Datei korrekt konfiguriert sind (`SSH_KEY_PATH`).
2. **Berechtigungen**: Setze die richtigen Berechtigungen für deine SSH-Keys:
   ```bash
   chmod 600 .ssh/id_rsa
   chmod 644 .ssh/id_rsa.pub
   ```
3. **SSH-Benutzer**: Überprüfe den `SSH_USER` in der `.env`-Datei.

### Fehler: `ERROR! Decryption failed`

**Lösung**: Überprüfe deine Ansible-Vault-Konfiguration:

1. **Vault-Passwort**: Stelle sicher, dass die `ANSIBLE_VAULT_PASSWORD_FILE` in der `.env`-Datei auf die richtige Passwort-Datei zeigt.
2. **Passwort-Datei**: Überprüfe, ob die Passwort-Datei das korrekte Passwort enthält.

## 3. Makefile

### Fehler: `make: *** No rule to make target 'run'. Stop.`

**Lösung**: Stelle sicher, dass du dich im richtigen Verzeichnis befindest und eine `Makefile` existiert.

## 4. Debugging

### Verbose-Output

Führe das Playbook mit Verbose-Output aus, um mehr Informationen zu erhalten:

```bash
make run ANSIBLE_VERBOSITY=2
```

### Interaktive Shell

Öffne eine interaktive Shell im Container, um die Umgebung zu untersuchen:

```bash
make shell
```

### Logs

Zeige die Logs des Containers an:

```bash
make logs
```

## 5. Weitere Hilfe

Wenn du weitere Hilfe benötigst, öffne bitte ein [Issue](https://github.com/your-repo/ansible-test-controller/issues) mit einer detaillierten Beschreibung des Problems.
