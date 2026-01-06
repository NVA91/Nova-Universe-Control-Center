# Extensions - Ansible Test Controller (v2.0)

Dieses Dokument beschreibt, wie du den Ansible Test Controller erweitern und anpassen kannst.

## 🔌 Extension Points

### 1. Alternative Playbooks

Der Controller sucht standardmäßig nach `site.yml`, `playbook.yml` und `main.yml`. Du kannst ein anderes Playbook angeben:

```bash
# Über Makefile
make run PLAYBOOK=my-playbook.yml

# Über docker-compose
docker-compose run --rm ansible-controller ansible-playbook my-playbook.yml
```

### 2. Rollen

Lege deine Rollen im `roles/`-Verzeichnis ab:

```
roles/
├── common/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   │   └── main.yml
│   ├── vars/
│   │   └── main.yml
│   ├── defaults/
│   │   └── main.yml
│   └── README.md
└── webserver/
    └── ...
```

Verwende sie in deinem Playbook:

```yaml
---
- name: My Playbook
  hosts: localhost
  roles:
    - common
    - webserver
```

### 3. Collections

Installiere Ansible Collections über eine `requirements.yml`:

```yaml
---
collections:
  - name: community.general
    version: ">=1.0.0"
  - name: ansible.posix
    version: ">=1.1.0"
```

Installiere sie vor dem Playbook:

```bash
docker-compose run --rm ansible-controller ansible-galaxy collection install -r requirements.yml
```

### 4. Custom Plugins

#### Library (Custom Modules)

Lege Custom Modules im `library/`-Verzeichnis ab:

```
library/
├── my_module.py
└── my_module.py.j2
```

Verwende sie im Playbook:

```yaml
- name: Use custom module
  my_module:
    param1: value1
    param2: value2
```

#### Lookup Plugins

Lege Lookup Plugins im `lookup_plugins/`-Verzeichnis ab:

```
lookup_plugins/
├── my_lookup.py
└── ...
```

Verwende sie im Playbook:

```yaml
- name: Use custom lookup
  debug:
    msg: "{{ lookup('my_lookup', 'param') }}"
```

#### Filter Plugins

Lege Filter Plugins im `filter_plugins/`-Verzeichnis ab:

```
filter_plugins/
├── my_filter.py
└── ...
```

Verwende sie im Playbook:

```yaml
- name: Use custom filter
  debug:
    msg: "{{ 'hello' | my_filter }}"
```

### 5. Gruppenvariablen und Host-Variablen

Organisiere deine Variablen in `group_vars/` und `host_vars/`:

```
group_vars/
├── all.yml
├── webservers.yml
└── databases.yml

host_vars/
├── web1.example.com.yml
└── db1.example.com.yml
```

### 6. Templates

Lege Jinja2-Templates im `templates/`-Verzeichnis ab:

```
templates/
├── nginx.conf.j2
├── app.config.j2
└── ...
```

Verwende sie im Playbook:

```yaml
- name: Deploy config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
```

### 7. Files

Lege statische Dateien im `files/`-Verzeichnis ab:

```
files/
├── app.jar
├── config.xml
└── ...
```

Verwende sie im Playbook:

```yaml
- name: Copy file
  copy:
    src: app.jar
    dest: /opt/app/app.jar
```

## 🛠️ Dockerfile anpassen

Du kannst das Dockerfile anpassen, um zusätzliche Tools zu installieren:

```dockerfile
# Füge nach der Ansible-Installation hinzu
RUN pip3 install --no-cache-dir \
    my-custom-package \
    another-package
```

Baue das Image neu:

```bash
make build
```

## 🔐 Vault-Integration

Verwende Ansible Vault für sensitive Daten:

```bash
# Erstelle eine neue Vault-Datei
docker-compose run --rm ansible-controller ansible-vault create group_vars/all/vault.yml

# Bearbeite eine Vault-Datei
docker-compose run --rm ansible-controller ansible-vault edit group_vars/all/vault.yml

# Führe Playbook mit Vault aus
docker-compose run --rm ansible-controller ansible-playbook site.yml
```

Konfiguriere die Vault-Passwort-Datei in der `.env`:

```bash
ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass
```

## 📦 Beispiele

Im `_examples/`-Verzeichnis findest du Vorlagen für:

- `hello-world.yml`: Einfaches Beispiel-Playbook
- `with-roles.yml`: Playbook mit Rollen
- `inventory.yml`: Inventory-Beispiel

## 🚀 CI/CD Integration

Integriere den Controller in deine CI/CD-Pipeline:

### GitLab CI

```yaml
stages:
  - test

test_ansible:
  stage: test
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - docker-compose build
    - docker-compose run --rm ansible-controller make test
```

### GitHub Actions

```yaml
name: Ansible Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          make build
          make test
```

## 📚 Weitere Ressourcen

- [Ansible Dokumentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Ansible Collections](https://galaxy.ansible.com/)
