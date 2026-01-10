# Master Prompt: Nova-Universe-Control-Center

**Zuletzt aktualisiert:** 10. Januar 2026

## 1. Projekt-Vision & Ziel

**Vision:** Eine selbst-gehostete, intelligente private Cloud-Management-Plattform. 

**Ziel:** Die Verwaltung einer Proxmox-Infrastruktur durch eine einfache Web-UI (Nova-World) zu vereinfachen. Die UI dient als Einstiegspunkt, um komplexe Aufgaben (Deployments, Updates) über Ansible (verwaltet durch Semaphore) zu automatisieren. Ein lokaler KI-Assistent (Ollama) soll über die Zeit lernen und Entscheidungen optimieren.

**Kurz gesagt:** Ein performantes, einfaches und mächtiges Control Center für die private Cloud.

## 2. System-Architektur

Das System besteht aus vier Hauptkomponenten, die ineinandergreifen:

| Komponente             | Rolle                                      | Technologie         |
| ---------------------- | ------------------------------------------ | ------------------- |
| **Nova-World UI**      | 🧠 **Gehirn:** Dashboard, Schnellaktionen      | Web App (React/Vue) |
| **Semaphore**          | 💪 **Muskeln:** Führt Ansible-Tasks aus       | Docker Container    |
| **Ansible Playbooks**  | 👐 **Hände:** Führt die eigentliche Arbeit aus | YAML-Skripte        |
| **Proxmox VE**         | 🏠 **Zuhause:** Virtualisierungsplattform      | KVM/QEMU            |

**Workflow:** `Nova-World UI` -> `Semaphore` -> `Ansible` -> `Proxmox`

## 3. Aktueller Sachstand

- ✅ **Nova-World UI** läuft auf dem Proxmox-Host.
- ✅ **Semaphore & PostgreSQL** laufen in Docker-Containern auf Proxmox.
- ✅ **GitHub Repository** (`NVA91/Nova-Universe-Control-Center`) enthält die Nova-World App und die Ansible-Playbooks.
- ✅ **SSH-Key** wurde in Semaphore hochgeladen und dem Repository zugewiesen.
- ✅ **Repository-URL** in Semaphore wurde auf SSH umgestellt (`git@github.com:...`).

## 4. 🔥 Kritisches Problem (BLOCKER)

**Problem:** Semaphore kann keine Verbindung zu GitHub herstellen.

**Fehlermeldung:** `listen unix /tmp/semaphore/ssh-agent-*.sock: socket: permission denied`

**Analyse:**
- Das ist ein **Berechtigungsproblem IM Semaphore-Container**.
- Der `semaphore` User im Container hat nicht die nötigen Rechte, um einen SSH-Agent-Socket im `/tmp/semaphore` Verzeichnis zu erstellen.
- Neustarts und `chmod` haben nicht geholfen. Das Problem liegt tiefer in der Container-Konfiguration oder dem Docker-Image selbst.

**Konsequenz:** Das gesamte System steht still. Ohne eine funktionierende Semaphore-Verbindung können keine Deployments ausgeführt werden.

## 5. 🎯 Nächste Schritte (Roadmap)

**Prio 1: Semaphore Permission-Problem lösen (BLOCKER)**
   - **Hypothese 1:** Das Docker-Image `semaphoreui/semaphore:v2.10.22` hat einen Bug oder ist inkompatibel mit der Proxmox-Umgebung.
   - **Aktion 1:** Recherche nach bekannten Issues mit diesem Image und `permission denied` auf Sockets.
   - **Hypothese 2:** Die Art, wie der Container gestartet wird (via `docker run` oder `docker-compose`), setzt die User-Berechtigungen falsch.
   - **Aktion 2:** `docker-compose.yml` (falls vorhanden) prüfen. Insbesondere die `user` Direktive.
   - **Lösungsidee:** Den Container mit expliziten User-IDs (`-u $(id -u):$(id -g)`) starten oder ein Volume für `/tmp` mit korrekten Rechten mounten.

**Prio 2: Erfolgreiches Deployment**
   - Sobald Prio 1 gelöst ist, die "Standardbereitstellung" in Semaphore erfolgreich ausführen.

**Prio 3: Integration & Weiterentwicklung**
   - Sicherstellen, dass die Nova-World UI wieder Deployments über die Semaphore API anstoßen kann.
   - KI-Assistent weiterentwickeln.

---
*Dieses Dokument dient als zentraler Ankerpunkt, um den Projektfokus zu wahren und die nächsten Schritte klar zu definieren.*
