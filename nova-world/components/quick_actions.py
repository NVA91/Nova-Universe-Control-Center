"""
⚡ Nova's Quick Actions - SECURITY FIXED VERSION
One-Click Power-Buttons für häufige Tasks

CHANGES:
- Fixed Shell Injection vulnerability (removed shell=True)
- Added proper error handling
- Added input validation
- Added timeouts
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
    """Vordefinierte Actions für häufige Tasks"""

    def __init__(self):
        secrets = get_secrets_manager()
        self.semaphore_url = secrets.get_semaphore_url()
        self.semaphore_token = secrets.get_semaphore_token()
        self.semaphore_project_id = secrets.get_semaphore_project_id()
        self.ansible_project_path = secrets.get_ansible_project_path()
        
        self.semaphore_client = None
        if self.semaphore_url and self.semaphore_token:
            try:
                self.semaphore_client = create_semaphore_client()
            except Exception as e:
                st.warning(f"Semaphore API nicht verfügbar: {e}")

    def deploy_minimal(self) -> Dict[str, Any]:
        return self._execute_semaphore_deploy("Deploy Minimal Profile")

    def deploy_standard(self) -> Dict[str, Any]:
        return self._execute_semaphore_deploy("Deploy Standard Profile")

    def deploy_full(self) -> Dict[str, Any]:
        return self._execute_semaphore_deploy("Deploy Full Profile")

    def _execute_semaphore_deploy(self, template_name: str) -> Dict[str, Any]:
        if not self.semaphore_client:
            return {"success": False, "message": "❌ Semaphore API nicht konfiguriert", "timestamp": datetime.now().isoformat()}
        try:
            templates = self.semaphore_client.get_templates(self.semaphore_project_id)
            template = next((t for t in templates if t['name'] == template_name), None)
            if not template:
                return {"success": False, "message": f"❌ Template '{template_name}' nicht gefunden", "timestamp": datetime.now().isoformat()}
            task = self.semaphore_client.execute_template(self.semaphore_project_id, template['id'])
            return {"success": True, "message": f"✅ Deployment gestartet: {template_name}", "task_id": task.get('id'), "timestamp": datetime.now().isoformat()}
        except SemaphoreAPIError as e:
            return {"success": False, "message": f"❌ Semaphore API Error: {e}", "timestamp": datetime.now().isoformat()}
        except Exception as e:
            return {"success": False, "message": f"❌ Fehler: {e}", "timestamp": datetime.now().isoformat()}

    def get_deployment_status(self) -> Dict[str, Any]:
        if not self.semaphore_client:
            return {"status": "unavailable", "message": "Semaphore API nicht verfügbar"}
        try:
            tasks = self.semaphore_client.get_tasks(self.semaphore_project_id, limit=5)
            if not tasks:
                return {"status": "idle", "message": "Keine aktiven Deployments"}
            running = [t for t in tasks if t.get('status') == 'running']
            if running:
                return {"status": "running", "message": f"Deployment läuft: {running[0].get('template_name')}", "task_id": running[0].get('id')}
            last = tasks[0]
            if last.get('status') == 'success':
                return {"status": "success", "message": f"✅ Letztes Deployment: {last.get('template_name')}", "task_id": last.get('id')}
            else:
                return {"status": "failed", "message": f"❌ Letztes Deployment fehlgeschlagen", "task_id": last.get('id')}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def docker_start_all(self) -> Dict[str, Any]:
        """
        Start all Docker containers
        
        SECURITY FIX: Removed shell=True to prevent shell injection
        """
        try:
            # Get all container IDs first
            result_ps = subprocess.run(
                ["docker", "ps", "-aq"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False
            )
            
            if result_ps.returncode != 0:
                return {
                    "success": False,
                    "message": "❌ Failed to list containers",
                    "output": result_ps.stderr,
                    "timestamp": datetime.now().isoformat()
                }
            
            container_ids = result_ps.stdout.strip().split('\n')
            container_ids = [cid.strip() for cid in container_ids if cid.strip()]
            
            if not container_ids:
                return {
                    "success": True,
                    "message": "ℹ️ No containers to start",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Start containers without shell=True
            result = subprocess.run(
                ["docker", "start"] + container_ids,
                capture_output=True,
                text=True,
                timeout=30,
                check=False
            )
            
            return {
                "success": result.returncode == 0,
                "message": f"✅ Started {len(container_ids)} containers" if result.returncode == 0 else "❌ Failed to start containers",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "❌ Timeout: Docker command took too long",
                "timestamp": datetime.now().isoformat()
            }
        except FileNotFoundError:
            return {
                "success": False,
                "message": "❌ Docker not found. Is Docker installed?",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def docker_stop_all(self) -> Dict[str, Any]:
        """
        Stop all running Docker containers
        
        SECURITY FIX: Removed shell=True to prevent shell injection
        """
        try:
            # Get running container IDs first
            result_ps = subprocess.run(
                ["docker", "ps", "-q"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False
            )
            
            if result_ps.returncode != 0:
                return {
                    "success": False,
                    "message": "❌ Failed to list containers",
                    "output": result_ps.stderr,
                    "timestamp": datetime.now().isoformat()
                }
            
            container_ids = result_ps.stdout.strip().split('\n')
            container_ids = [cid.strip() for cid in container_ids if cid.strip()]
            
            if not container_ids:
                return {
                    "success": True,
                    "message": "ℹ️ No running containers to stop",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Stop containers without shell=True
            result = subprocess.run(
                ["docker", "stop"] + container_ids,
                capture_output=True,
                text=True,
                timeout=60,  # Longer timeout for graceful shutdown
                check=False
            )
            
            return {
                "success": result.returncode == 0,
                "message": f"✅ Stopped {len(container_ids)} containers" if result.returncode == 0 else "❌ Failed to stop containers",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "❌ Timeout: Docker stop took too long",
                "timestamp": datetime.now().isoformat()
            }
        except FileNotFoundError:
            return {
                "success": False,
                "message": "❌ Docker not found. Is Docker installed?",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def docker_restart_all(self) -> Dict[str, Any]:
        """
        Restart all running Docker containers
        
        SECURITY FIX: Removed shell=True to prevent shell injection
        """
        try:
            # Get running container IDs first
            result_ps = subprocess.run(
                ["docker", "ps", "-q"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False
            )
            
            if result_ps.returncode != 0:
                return {
                    "success": False,
                    "message": "❌ Failed to list containers",
                    "output": result_ps.stderr,
                    "timestamp": datetime.now().isoformat()
                }
            
            container_ids = result_ps.stdout.strip().split('\n')
            container_ids = [cid.strip() for cid in container_ids if cid.strip()]
            
            if not container_ids:
                return {
                    "success": True,
                    "message": "ℹ️ No running containers to restart",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Restart containers without shell=True
            result = subprocess.run(
                ["docker", "restart"] + container_ids,
                capture_output=True,
                text=True,
                timeout=90,  # Longer timeout for restart
                check=False
            )
            
            return {
                "success": result.returncode == 0,
                "message": f"✅ Restarted {len(container_ids)} containers" if result.returncode == 0 else "❌ Failed to restart containers",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "❌ Timeout: Docker restart took too long",
                "timestamp": datetime.now().isoformat()
            }
        except FileNotFoundError:
            return {
                "success": False,
                "message": "❌ Docker not found. Is Docker installed?",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def docker_cleanup(self) -> Dict[str, Any]:
        """
        Clean up Docker system (remove unused containers, images, volumes)
        
        SECURITY: Already safe (no shell=True)
        """
        try:
            result = subprocess.run(
                ["docker", "system", "prune", "-af", "--volumes"],
                capture_output=True,
                text=True,
                timeout=120,  # Cleanup can take time
                check=False
            )
            
            return {
                "success": result.returncode == 0,
                "message": "✅ Docker cleanup complete" if result.returncode == 0 else "❌ Cleanup failed",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "❌ Timeout: Docker cleanup took too long",
                "timestamp": datetime.now().isoformat()
            }
        except FileNotFoundError:
            return {
                "success": False,
                "message": "❌ Docker not found. Is Docker installed?",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    # ... Rest of the methods remain unchanged ...
