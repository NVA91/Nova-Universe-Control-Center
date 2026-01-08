# 🎭 Semaphore API Integration Guide

**Full REST API Integration for Nova-World Dashboard**

---

## 📋 Übersicht

Dieses Update fügt **vollständige Semaphore REST API Integration** hinzu für:
- ✅ **Projects Management** - Projekte abrufen und verwalten
- ✅ **Task Templates** - Templates abrufen und ausführen
- ✅ **Job Execution** - Jobs triggern und überwachen
- ✅ **Live Logs** - Echtzeit-Log-Streaming
- ✅ **Job History** - Deployment-Historie anzeigen
- ✅ **Quick Actions** - One-Click-Deployments

---

## 🏗️ Architektur

```
┌─────────────────────────────────────┐
│  Nova-World Dashboard               │
│  (Streamlit)                        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Semaphore API Client               │
│  (semaphore_api.py)                 │
│  - Connection Pooling               │
│  - Retry Logic                      │
│  - Error Handling                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Semaphore REST API                 │
│  (http://localhost:3000/api)        │
│  - Projects                         │
│  - Templates                        │
│  - Tasks                            │
│  - Logs                             │
└─────────────────────────────────────┘
```

---

## 🚀 Installation

### Voraussetzungen

**Semaphore**:
- Semaphore läuft (http://localhost:3000)
- API Token generiert
- Mindestens ein Projekt erstellt

### Schritt 1: API Token generieren

1. Öffne Semaphore: http://localhost:3000
2. Gehe zu **User Settings** → **API Tokens**
3. Klicke **Create Token**
4. Kopiere den Token

### Schritt 2: Konfiguration

Erstelle/erweitere `.streamlit/secrets.toml`:

```toml
[semaphore]
url = "http://localhost:3000"
api_token = "your-api-token-here"
project_id = 1
```

**Wichtig**: `project_id` ist die ID deines Hauptprojekts in Semaphore.

### Schritt 3: Dateien kopieren

```bash
cd /tmp/semaphore-api-update

# API Client
cp nova-world/components/semaphore_api.py \
    ~/unified-ansible-project/nova-world/components/

# Quick Actions Extension
cp nova-world/components/quick_actions_semaphore.py \
    ~/unified-ansible-project/nova-world/components/

# Updated Deploy Page
cp nova-world/pages/03_🚀_Deploy_UPDATED.py \
    ~/unified-ansible-project/nova-world/pages/03_🚀_Deploy.py
```

### Schritt 4: Nova-World neu starten

```bash
cd ~/unified-ansible-project/nova-world
streamlit run nova_universe.py
```

---

## 🧪 Testing

### 1. Connection Test

```python
from components.semaphore_api import create_semaphore_client

client = create_semaphore_client()

# Test connection
if client.ping():
    print("✅ Semaphore is reachable")
else:
    print("❌ Cannot connect to Semaphore")
```

### 2. Get Projects

```python
projects = client.get_projects()
print(f"Found {len(projects)} projects")

for project in projects:
    print(f"- {project['name']} (ID: {project['id']})")
```

### 3. Get Templates

```python
project_id = 1
templates = client.get_templates(project_id)

for template in templates:
    print(f"- {template['name']} (ID: {template['id']})")
```

### 4. Run Task

```python
project_id = 1
template_id = 1

result = client.run_task(project_id, template_id)
task_id = result['id']

print(f"✅ Task {task_id} started")
```

### 5. Get Task Status

```python
task = client.get_task(project_id, task_id)
print(f"Status: {task['status']}")
```

### 6. Get Task Logs

```python
logs = client.get_task_output(project_id, task_id)

for log in logs:
    print(log['output'])
```

---

## 📚 API Reference

### SemaphoreAPI Class

#### Initialization

```python
from components.semaphore_api import SemaphoreAPI

client = SemaphoreAPI(
    base_url="http://localhost:3000",
    api_token="your-token",
    timeout=30,
    max_retries=3
)
```

#### Methods

**Health & Info**:
- `ping()` - Check if Semaphore is reachable
- `get_info()` - Get server info

**Projects**:
- `get_projects()` - Get all projects
- `get_project(project_id)` - Get project by ID

**Templates**:
- `get_templates(project_id)` - Get all templates
- `get_template(project_id, template_id)` - Get template by ID

**Tasks**:
- `run_task(project_id, template_id, debug=False, dry_run=False)` - Run task
- `get_tasks(project_id, limit=50)` - Get task history
- `get_task(project_id, task_id)` - Get task details
- `get_task_output(project_id, task_id)` - Get task logs
- `stop_task(project_id, task_id)` - Stop running task

**Helper Methods**:
- `wait_for_task(project_id, task_id, timeout=600)` - Wait for task completion
- `get_task_status_summary(project_id, task_id)` - Get status summary
- `get_recent_tasks(project_id, limit=10)` - Get recent tasks with summaries
- `stream_task_logs(project_id, task_id, follow=True)` - Stream logs (generator)

---

## 🎯 Features

### 1. Quick Actions Integration

**Semaphore-based Quick Actions**:
- Deploy Minimal
- Deploy Standard
- Deploy Full
- Health Check
- Backup Now
- Update Containers

**Usage in Nova-World**:
```python
from components.quick_actions_semaphore import (
    get_semaphore_actions,
    execute_semaphore_action
)

actions = get_semaphore_actions()
result = execute_semaphore_action(actions[0])
```

### 2. Deploy Page Enhancements

**New Features**:
- ✅ Deployment Status Dashboard
- ✅ Quick Deploy Buttons
- ✅ Template Browser
- ✅ Task History Table
- ✅ Task Details Viewer
- ✅ Live Log Viewer
- ✅ Task Monitoring

**Navigation**:
1. Öffne Nova-World
2. Gehe zu **🚀 Deploy** Page
3. Siehe Deployment-Status
4. Klicke Quick Deploy Buttons
5. Browse Templates
6. View Task History

### 3. Live Monitoring

**Real-time Task Monitoring**:
```python
# Stream logs
for log in client.stream_task_logs(project_id, task_id, follow=True):
    print(log['output'])
```

**In Nova-World**:
1. Gehe zu **🚀 Deploy** Page
2. Scrolle zu **📡 Live Monitoring**
3. Gib Task ID ein
4. Klicke **▶️ Start Monitoring**
5. Siehe Logs in Echtzeit

### 4. Error Handling

**Automatic Retry**:
- Max 3 Retries
- Exponential Backoff (2^attempt seconds)
- Retry on server errors (5xx)
- Retry on timeout
- Retry on connection errors

**Error Types**:
- `SemaphoreAPIError` - Base exception
- Specific error messages for each failure type

---

## 🔧 Konfiguration

### API Client Settings

```python
client = SemaphoreAPI(
    base_url="http://localhost:3000",
    api_token="your-token",
    timeout=30,          # Request timeout in seconds
    max_retries=3        # Maximum retry attempts
)
```

### Secrets Configuration

```toml
[semaphore]
url = "http://localhost:3000"
api_token = "your-api-token-here"
project_id = 1
```

### Environment Variables (Alternative)

```bash
export SEMAPHORE_URL="http://localhost:3000"
export SEMAPHORE_API_TOKEN="your-token"
export SEMAPHORE_PROJECT_ID=1
```

---

## 📊 Use Cases

### Use Case 1: One-Click Deployment

**Scenario**: Deploy standard profile with one click

**Solution**:
1. Öffne Nova-World → **🚀 Deploy**
2. Klicke **Deploy Standard**
3. Bestätige Deployment
4. Siehe Task-Status in Echtzeit

### Use Case 2: Monitor Running Deployment

**Scenario**: Monitor a running deployment

**Solution**:
1. Deployment starten (siehe Use Case 1)
2. Notiere Task ID
3. Gehe zu **📡 Live Monitoring**
4. Gib Task ID ein
5. Klicke **▶️ Start Monitoring**
6. Siehe Logs live

### Use Case 3: Review Deployment History

**Scenario**: Check last 10 deployments

**Solution**:
1. Öffne Nova-World → **🚀 Deploy**
2. Scrolle zu **📜 Task History**
3. Siehe Tabelle mit letzten 10 Tasks
4. Klicke auf Task ID für Details
5. Klicke **📄 Load Logs** für Logs

### Use Case 4: Stop Running Task

**Scenario**: Stop a running task

**Solution**:
1. Öffne Nova-World → **🚀 Deploy**
2. Gehe zu **📜 Task History**
3. Wähle running Task
4. Klicke **⏹️ Stop Task**
5. Task wird gestoppt

### Use Case 5: Programmatic Deployment

**Scenario**: Deploy via Python script

**Solution**:
```python
from components.semaphore_api import create_semaphore_client

client = create_semaphore_client()

# Run deployment
result = client.run_task(
    project_id=1,
    template_id=1,
    debug=False,
    dry_run=False
)

task_id = result['id']
print(f"Task {task_id} started")

# Wait for completion
final_task = client.wait_for_task(
    project_id=1,
    task_id=task_id,
    timeout=600
)

if final_task['status'] == 'success':
    print("✅ Deployment successful")
else:
    print(f"❌ Deployment failed: {final_task.get('message')}")
```

---

## 🐛 Troubleshooting

### Problem: Cannot connect to Semaphore

**Symptom**: `Connection error: Cannot reach Semaphore`

**Lösungen**:
1. Prüfe ob Semaphore läuft:
   ```bash
   curl http://localhost:3000/api/ping
   ```

2. Prüfe URL in secrets.toml:
   ```toml
   [semaphore]
   url = "http://localhost:3000"  # Korrekte URL?
   ```

3. Prüfe Firewall/Network

### Problem: Unauthorized

**Symptom**: `Unauthorized: Invalid API token`

**Lösungen**:
1. Prüfe API Token in secrets.toml
2. Generiere neuen Token in Semaphore
3. Kopiere Token exakt (keine Leerzeichen)

### Problem: Template not found

**Symptom**: `Template 'Deploy Standard' not found`

**Lösungen**:
1. Prüfe Template-Namen in Semaphore
2. Update Template-Namen in Quick Actions:
   ```python
   # quick_actions_semaphore.py
   {
       "template_name": "Your Actual Template Name"
   }
   ```

3. Liste verfügbare Templates:
   ```python
   templates = client.get_templates(project_id)
   for t in templates:
       print(t['name'])
   ```

### Problem: Task timeout

**Symptom**: `Task timeout after 600s`

**Lösungen**:
1. Erhöhe Timeout:
   ```python
   client.wait_for_task(
       project_id=1,
       task_id=task_id,
       timeout=1200  # 20 Minuten
   )
   ```

2. Prüfe Task-Status manuell:
   ```python
   task = client.get_task(project_id, task_id)
   print(task['status'])
   ```

### Problem: Logs not loading

**Symptom**: `No logs available`

**Lösungen**:
1. Warte bis Task startet (Logs erscheinen verzögert)
2. Prüfe Task-Status:
   ```python
   task = client.get_task(project_id, task_id)
   print(task['status'])
   ```

3. Prüfe in Semaphore Web-UI

---

## 💡 Best Practices

### 1. Error Handling

**Always wrap API calls**:
```python
try:
    result = client.run_task(project_id, template_id)
except SemaphoreAPIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

### 2. Connection Pooling

**Reuse client instance**:
```python
# Good
client = create_semaphore_client()
for template_id in [1, 2, 3]:
    client.run_task(project_id, template_id)

# Bad (creates new connection each time)
for template_id in [1, 2, 3]:
    client = create_semaphore_client()
    client.run_task(project_id, template_id)
```

### 3. Timeouts

**Set appropriate timeouts**:
```python
# Short tasks
client = SemaphoreAPI(base_url=url, api_token=token, timeout=30)

# Long tasks
client = SemaphoreAPI(base_url=url, api_token=token, timeout=300)
```

### 4. Polling

**Use appropriate poll intervals**:
```python
# Fast feedback (development)
client.wait_for_task(project_id, task_id, poll_interval=1)

# Normal (production)
client.wait_for_task(project_id, task_id, poll_interval=5)
```

### 5. Log Streaming

**Stream logs for long-running tasks**:
```python
for log in client.stream_task_logs(project_id, task_id, follow=True):
    print(log['output'])
    # Process log in real-time
```

---

## 📈 Performance

### API Response Times

**Typical Response Times**:
- `ping()`: <100ms
- `get_projects()`: 100-200ms
- `get_templates()`: 100-300ms
- `run_task()`: 200-500ms
- `get_task()`: 100-200ms
- `get_task_output()`: 200-500ms (depends on log size)

### Optimization Tips

**1. Cache Projects/Templates**:
```python
# Cache templates (they rarely change)
if 'templates' not in st.session_state:
    st.session_state.templates = client.get_templates(project_id)

templates = st.session_state.templates
```

**2. Batch Requests**:
```python
# Get multiple tasks at once
tasks = client.get_tasks(project_id, limit=50)
```

**3. Use Summaries**:
```python
# Use get_recent_tasks (includes summaries)
tasks = client.get_recent_tasks(project_id, limit=10)

# Instead of
tasks = client.get_tasks(project_id, limit=10)
for task in tasks:
    summary = client.get_task_status_summary(project_id, task['id'])
```

---

## 🔐 Sicherheit

### API Token Security

**Best Practices**:
- ✅ Store in secrets.toml (not in code)
- ✅ Never commit secrets.toml to Git
- ✅ Use environment variables in production
- ✅ Rotate tokens regularly
- ✅ Use separate tokens for dev/prod

### HTTPS

**Production Setup**:
```toml
[semaphore]
url = "https://semaphore.yourdomain.com"  # HTTPS!
api_token = "your-token"
```

### Access Control

**Semaphore User Roles**:
- Owner: Full access
- Manager: Can run tasks
- Task Runner: Can only run tasks
- Guest: Read-only

**Recommendation**: Use Task Runner role for API tokens

---

## 🔮 Roadmap

### v1.1 (Geplant)

- 🔜 Webhook Integration (Semaphore → Nova-World)
- 🔜 Scheduled Deployments
- 🔜 Deployment Approval Workflow
- 🔜 Multi-Project Support

### v1.2 (Zukunft)

- 🔮 Deployment Rollback
- 🔮 Deployment Diff Viewer
- 🔮 Deployment Analytics
- 🔮 Slack/Email Notifications

---

**🎭 Semaphore API Integration ist bereit!**

*Full REST API Control, Live Monitoring, One-Click Deployments.* 🚀
