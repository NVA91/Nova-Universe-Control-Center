#!/usr/bin/env python3
"""
🔐 Nova-World Dashboard Setup
Einmalig ausführen, dann vergessen!
"""

import os
import sys
from pathlib import Path
import secrets as sec

def setup_nova_world():
    """Minimales Setup - nur das Nötigste!"""
    
    print("🪐 Nova-World Dashboard Setup")
    print("=" * 50)
    
    # 1. Check Python Version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ erforderlich!")
        print(f"   Aktuelle Version: {sys.version}")
        sys.exit(1)
    
    print("✅ Python Version OK")
    
    # 2. Install Dependencies
    print("\n📦 Installiere Dependencies...")
    try:
        import streamlit
        print("✅ Streamlit bereits installiert")
    except ImportError:
        print("📦 Installiere Streamlit...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    # 3. Create Directories
    print("\n📁 Erstelle Verzeichnisse...")
    directories = [
        ".streamlit",
        "components",
        "pages",
        ".nova",
        ".nova/credentials",
        "logs",
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Verzeichnisse erstellt")
    
    # 4. Setup Secrets
    secrets_file = Path(".streamlit/secrets.toml")
    
    if not secrets_file.exists():
        print("\n🔐 Erstelle secrets.toml...")
        
        # Generate JWT Secret
        jwt_secret = sec.token_hex(32)
        
        secrets_content = f"""# ============================================================================
# Secrets Configuration - Nova-World Dashboard
# ============================================================================
# WICHTIG: Diese Datei NICHT in Git committen!

[openai]
api_key = "sk-..."  # TODO: Füge deinen OpenAI API Key ein
model = "gpt-4"
whisper_model = "whisper-1"

[semaphore]
url = "http://localhost:3000"
api_token = ""
project_id = 1

[security]
jwt_secret = "{jwt_secret}"
session_timeout = 86400

[passkey]
rp_id = "nova.local"
rp_name = "Nova World"

[system]
ansible_project_path = "{Path.cwd().parent.absolute()}"
docker_socket = "unix:///var/run/docker.sock"

[features]
voice_control_enabled = true
ai_assistant_enabled = true
self_hosted_whisper = false
"""
        
        secrets_file.write_text(secrets_content)
        print("✅ secrets.toml erstellt")
        print("⚠️  WICHTIG: Füge deinen OpenAI API Key in .streamlit/secrets.toml ein!")
    else:
        print("✅ secrets.toml bereits vorhanden")
    
    # 5. Update .gitignore
    print("\n📝 Aktualisiere .gitignore...")
    gitignore = Path("../.gitignore")
    
    lines_to_add = [
        "# Nova-World Dashboard",
        "nova-world/.streamlit/secrets.toml",
        "nova-world/.nova/",
        "nova-world/logs/",
        "nova-world/*.pyc",
        "nova-world/__pycache__/",
    ]
    
    existing = gitignore.read_text() if gitignore.exists() else ""
    
    for line in lines_to_add:
        if line not in existing:
            with open(gitignore, "a") as f:
                f.write(f"\n{line}")
    
    print("✅ .gitignore aktualisiert")
    
    # 6. Create __init__.py files
    print("\n📄 Erstelle __init__.py Dateien...")
    for directory in ["components", "pages"]:
        init_file = Path(directory) / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# Nova-World Dashboard\n")
    
    print("✅ __init__.py Dateien erstellt")
    
    # DONE!
    print("\n" + "=" * 50)
    print("✅ Setup abgeschlossen!")
    print("\n📝 Nächste Schritte:")
    print("1. Füge deinen OpenAI API Key in .streamlit/secrets.toml ein")
    print("2. Optional: Konfiguriere Semaphore URL in secrets.toml")
    print("3. Starte das Dashboard:")
    print("   streamlit run nova_universe.py")
    print("\n🚀 Dashboard wird verfügbar sein auf: http://localhost:8501")
    print("\n💡 Tipp: Siehe README.md für weitere Informationen")

if __name__ == "__main__":
    try:
        setup_nova_world()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fehler beim Setup: {e}")
        sys.exit(1)
