"""
⚡ Nova's Quick Actions
One-Click Power-Buttons für häufige Tasks
Includes: Docker, Deployment (Semaphore), System, Workflows
"""

import streamlit as st
import subprocess
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import psutil
from components.secrets_manager import get_secrets_manager
from components.semaphore_api import SemaphoreAPI, SemaphoreAPIError, create_semaphore_client

class QuickActions:
    """
    Vordefinierte Actions für häufige Tasks
    One-Click Execution!
    """

    def __init__(self):
        secrets = get_secrets_manager()
        self.semaphore_url = secrets.get_semaphore_url()
        self.semaphore_token = secrets.get_semaphore_token()
        self.semaphore_project_id = secrets.get_semaphore_project_id()
        self.ansible_project_path = secrets.get_ansible_project_path()
        
        # Initialize Semaphore API client
        self.semaphore_client = None
        if self.semaphore_url and self.semaphore_token:
            try:
                self.semaphore_client = create_semaphore_client()
            except Exception as e:
                st.warning(f"Semaphore API nicht verfügbar: {e}")

    # ═══════════════════════════════════════════════════════════
    # 🚀 SEMAPHORE DEPLOYMENT ACTIONS
    # ═══════════════════════════════════════════════════════════

    def deploy_minimal(self) -> Dict[str, Any]:
        """Deploy minimal profile via Semaphore"""
        return self._execute_semaphore_deploy("Deploy Minimal Profile")

    def deploy_standard(self) -> Dict[str, Any]:
        """Deploy standard profile via Semaphore"""
        return self._execute_semaphore_deploy("Deploy Standard Profile")

    def deploy_full(self) -> Dict[str, Any]:
        """Deploy full profile via Semaphore"""
        return self._execute_semaphore_deploy("Deploy Full Profile")

    def _execute_semaphore_deploy(self, template_name: str) -> Dict[str, Any]:
        """Execute deployment via Semaphore API"""
        if not self.semaphore_client:
            return {
                "success": False,
                "message": "❌ Semaphore API nicht konfiguriert",
                "timestamp": datetime.now().isoformat()
            }

        try:
            # Get template
            templates = self.semaphore_client.get_templates(self.semaphore_project_id)
            template = next((t for t in templates if t['name'] == template_name), None)
            
            if not template:
                return {
                    "success": False,
                    "message": f"❌ Template '{template_name}' nicht gefunden",
                    "timestamp": datetime.now().isoformat()
                }

            # Execute task
            task = self.semaphore_client.execute_template(
                self.semaphore_project_id,
                template['id']
            )

            return {
                "success": True,
                "message": f"✅ Deployment gestartet: {template_name}",
                "task_id": task.get('id'),
                "timestamp": datetime.now().isoformat()
            }

        except SemaphoreAPIError as e:
            return {
                "success": False,
                "message": f"❌ Semaphore API Error: {e}",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Fehler: {e}",
                "timestamp": datetime.now().isoformat()
            }

    def get_deployment_status(self) -> Dict[str, Any]:
        """Get current deployment status from Semaphore"""
        if not self.semaphore_client:
            return {"status": "unavailable", "message": "Semaphore API nicht verfügbar"}

        try:
            # Get last 5 tasks
            tasks = self.semaphore_client.get_tasks(
                self.semaphore_project_id,
                limit=5
            )

            if not tasks:
                return {"status": "idle", "message": "Keine aktiven Deployments"}

            # Check if any running
            running = [t for t in tasks if t.get('status') == 'running']
            if running:
                return {
                    "status": "running",
                    "message": f"Deployment läuft: {running[0].get('template_name')}",
                    "task_id": running[0].get('id')
                }

            # Get last completed
            last = tasks[0]
            if last.get('status') == 'success':
                return {
                    "status": "success",
                    "message": f"✅ Letztes Deployment: {last.get('template_name')}",
                    "task_id": last.get('id')
                }
            else:
                return {
                    "status": "failed",
                    "message": f"❌ Letztes Deployment fehlgeschlagen",
                    "task_id": last.get('id')
                }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ═══════════════════════════════════════════════════════════
    # 🐳 DOCKER QUICK ACTIONS
    # ═══════════════════════════════════════════════════════════

    def docker_start_all(self) -> Dict[str, Any]:
        """Start all Docker containers"""
        try:
            result = subprocess.run(
                ["docker", "start", "$(docker ps -aq)"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            return {
                "success": result.returncode == 0,
                "message": "✅ All containers started" if result.returncode == 0 else "❌ Failed to start containers",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def docker_stop_all(self) -> Dict[str, Any]:
        """Stop all Docker containers"""
        try:
            result = subprocess.run(
                ["docker", "stop", "$(docker ps -q)"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            return {
                "success": result.returncode == 0,
                "message": "✅ All containers stopped" if result.returncode == 0 else "❌ Failed to stop containers",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def docker_restart_all(self) -> Dict[str, Any]:
        """Restart all Docker containers"""
        try:
            result = subprocess.run(
                ["docker", "restart", "$(docker ps -q)"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            return {
                "success": result.returncode == 0,
                "message": "✅ All containers restarted" if result.returncode == 0 else "❌ Failed to restart containers",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def docker_cleanup(self) -> Dict[str, Any]:
        """Clean up Docker (unused containers, images, volumes)"""
        try:
            result = subprocess.run(
                ["docker", "system", "prune", "-af", "--volumes"],
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "message": "✅ Docker cleanup complete" if result.returncode == 0 else "❌ Cleanup failed",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    # ═══════════════════════════════════════════════════════════
    # 🔧 SYSTEM QUICK ACTIONS
    # ═══════════════════════════════════════════════════════════

    def system_health_check(self) -> Dict[str, Any]:
        """Quick system health check"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            health = "✅ Healthy"
            if cpu_percent > 80 or memory.percent > 85 or disk.percent > 90:
                health = "⚠️ Warning"
            if cpu_percent > 95 or memory.percent > 95 or disk.percent > 95:
                health = "❌ Critical"
            
            return {
                "success": True,
                "message": health,
                "details": {
                    "cpu": f"{cpu_percent}%",
                    "memory": f"{memory.percent}%",
                    "disk": f"{disk.percent}%"
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def check_errors(self) -> Dict[str, Any]:
        """Check system logs for errors"""
        try:
            # Check Docker logs
            result = subprocess.run(
                ["docker", "ps", "--filter", "health=unhealthy", "--format", "{{.Names}}"],
                capture_output=True,
                text=True
            )
            
            unhealthy = result.stdout.strip().split('
') if result.stdout.strip() else []
            
            if unhealthy and unhealthy[0]:
                return {
                    "success": False,
                    "message": f"⚠️ {len(unhealthy)} unhealthy containers",
                    "details": unhealthy,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": True,
                    "message": "✅ No errors found",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }


# ═══════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════

def get_quick_actions() -> QuickActions:
    """Get Quick Actions instance"""
    if 'quick_actions' not in st.session_state:
        st.session_state.quick_actions = QuickActions()
    return st.session_state.quick_actions


def render_quick_actions_grid():
    """Render Quick Actions Grid in UI"""
    qa = get_quick_actions()
    
    st.subheader("⚡ Quick Actions")
    
    # Deployment Actions
    with st.expander("🚀 Deployment", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Deploy Minimal", use_container_width=True):
                result = qa.deploy_minimal()
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['message'])
        
        with col2:
            if st.button("Deploy Standard", use_container_width=True, type="primary"):
                result = qa.deploy_standard()
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['message'])
        
        with col3:
            if st.button("Deploy Full", use_container_width=True):
                result = qa.deploy_full()
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['message'])
    
    # Docker Actions
    with st.expander("🐳 Docker"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Start All", use_container_width=True):
                result = qa.docker_start_all()
                st.toast(result['message'])
        
        with col2:
            if st.button("Restart All", use_container_width=True):
                result = qa.docker_restart_all()
                st.toast(result['message'])
        
        with col3:
            if st.button("Stop All", use_container_width=True):
                result = qa.docker_stop_all()
                st.toast(result['message'])
        
        with col4:
            if st.button("Cleanup", use_container_width=True):
                result = qa.docker_cleanup()
                st.toast(result['message'])
    
    # System Actions
    with st.expander("🔧 System"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Health Check", use_container_width=True):
                result = qa.system_health_check()
                if result['success']:
                    st.success(result['message'])
                    st.json(result['details'])
                else:
                    st.error(result['message'])
        
        with col2:
            if st.button("Check Errors", use_container_width=True):
                result = qa.check_errors()
                if result['success']:
                    st.success(result['message'])
                else:
                    st.warning(result['message'])
                    if 'details' in result:
                        st.write(result['details'])
