# 🎤 Voice Commands Cheat Sheet

**Nova-World Voice Control - Alle verfügbaren Commands**

---

## 🐳 Docker Commands

### Container starten
```
"Start all"
"Starte alle"
"Alles starten"
```
→ Startet alle gestoppten Container

### Container stoppen
```
"Stop all"
"Stoppe alle"
"Alles stoppen"
```
→ Stoppt alle laufenden Container  
⚠️ **GEFÄHRLICH** - Bestätigung erforderlich!

### Container neustarten
```
"Restart all"
"Neustart alle"
"Alle neustarten"
```
→ Restart aller laufenden Container

### Docker aufräumen
```
"Cleanup"
"Aufräumen"
"Docker clean"
```
→ Entfernt ungenutzte Images, Container, Volumes

### Docker Status
```
"Docker status"
"Container status"
```
→ Zeigt Status aller Container

---

## 🚀 Deployment Commands

### Minimal Deployment
```
"Deploy minimal"
"Minimal deploy"
```
→ Triggert Minimal Profile Deployment

### Standard Deployment
```
"Deploy standard"
"Standard deploy"
```
→ Triggert Standard Profile Deployment

### Full Deployment
```
"Deploy full"
"Full deploy"
"Alles deployen"
```
→ Triggert Full Profile Deployment

### Deployment Status
```
"Semaphore status"
"Deployment status"
```
→ Zeigt Semaphore-Status

---

## 💻 System Commands

### Health Check
```
"Health check"
"System check"
"Gesundheit"
```
→ Prüft System-Status (CPU, RAM, Disk, Docker)

### System Uptime
```
"Uptime"
"Laufzeit"
```
→ Zeigt System-Laufzeit

### Fehler suchen
```
"Errors"
"Fehler"
"Logs"
```
→ Sucht nach Fehlern in Container-Logs

---

## 🎯 Composite Commands

### Morning Routine
```
"Morning routine"
"Morgen routine"
"Startup"
```
→ Automatisierte Startup-Sequenz:
1. Start alle Container
2. Health Check
3. Semaphore Status

### Emergency Stop
```
"Emergency stop"
"Notfall stop"
```
→ Notfall-Shutdown (stoppt alle Container)  
⚠️ **GEFÄHRLICH** - Bestätigung erforderlich!

---

## 💡 Tipps für Voice Commands

### ✅ Best Practices

**Klar und deutlich sprechen**:
- Nicht zu schnell
- Nicht zu leise
- Keine Hintergrundgeräusche

**Kurze Commands bevorzugen**:
- ✅ "Start all" statt "Starte bitte alle Container"
- ✅ "Health check" statt "Führe einen System Health Check durch"

**Warten auf Stille-Erkennung**:
- Nach Command 2 Sekunden warten
- Recorder stoppt automatisch

**Bei Fehlern**:
- Nochmal versuchen
- Andere Formulierung nutzen
- AI Assistant fragen

### 🎯 Command-Varianten

**Deutsch & Englisch funktionieren**:
- "Start all" = "Starte alle"
- "Health check" = "Gesundheit"
- "Deploy" = "Deployen"

**Flexible Formulierungen**:
- "Start all" = "Starte alle" = "Alles starten"
- "Stop all" = "Stoppe alle" = "Alles stoppen"

### ⚠️ Gefährliche Commands

**Erfordern Bestätigung**:
- Stop all
- Emergency stop

**Workflow**:
1. Sprich Command
2. Warte auf Erkennung
3. Bestätige mit Button
4. Command wird ausgeführt

---

## 🔍 Command Recognition

### Pattern Matching (Schnell)

**Regex-basiert** für häufige Commands:
- "start.*all" → docker_start_all
- "health.*check" → health_check
- "deploy.*standard" → deploy_standard

### AI Intent Recognition (Fallback)

**GPT-4-basiert** für komplexe Commands:
- "Kannst du bitte alle Container starten?" → docker_start_all
- "Ich möchte das Standard-Profil deployen" → deploy_standard

---

## 📊 Command History

**Alle Voice Commands werden gespeichert**:
- Transcript (was du gesagt hast)
- Erkanntes Kommando
- Zeitpunkt
- Ergebnis

**Zugriff**:
- Voice Control Page → Command History
- Letzte 10 Commands werden angezeigt

---

## 🚨 Troubleshooting

### Command wird nicht erkannt

**Problem**: "Ich verstehe ... nicht"

**Lösungen**:
1. Andere Formulierung versuchen
2. Kürzer formulieren
3. Aus Cheat Sheet kopieren
4. AI Assistant fragen

### Audio-Aufnahme funktioniert nicht

**Problem**: Kein Audio-Recorder sichtbar

**Lösung**:
```bash
pip install audio-recorder-streamlit
streamlit run nova_universe.py
```

### Whisper Fehler

**Problem**: "Whisper Fehler: ..."

**Lösungen**:
1. OpenAI API Key prüfen (`.streamlit/secrets.toml`)
2. Internet-Verbindung prüfen
3. API-Limit erreicht? (OpenAI Dashboard prüfen)

---

## 🎓 Beispiel-Session

```
👤 User: "Start all"
🎤 Nova: "Du hast gesagt: Start all"
🎯 Nova: "Erkanntes Kommando: docker_start_all"
✅ Nova: "3 Container gestartet"

👤 User: "Health check"
🎤 Nova: "Du hast gesagt: Health check"
🎯 Nova: "Erkanntes Kommando: health_check"
✅ Nova: "System ist gesund! CPU: 45%, RAM: 62%, Disk: 58%"

👤 User: "Deploy standard"
🎤 Nova: "Du hast gesagt: Deploy standard"
🎯 Nova: "Erkanntes Kommando: deploy_standard"
✅ Nova: "Deployment 'Deploy Standard Profile' würde getriggert"
```

---

## 📚 Weitere Ressourcen

- **README.md**: Vollständige Dokumentation
- **AI Assistant**: Frag Nova bei Fragen!
- **Dashboard**: Alle Actions auch per Button verfügbar

---

**🎤 Happy Voice Commanding!**

*"JARVIS, start all containers!" 🦾*
