"""
⚡ Nova's Quick Actions
One-Click Power-Buttons für häufige Tasks
"""

import streamlit as st
import subprocess
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import psutil
from components.secrets_manager import get_secrets_manager

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
    
    # ═══════════════════════════════════════════════════════════
    # 🐳 DOCKER QUICK ACTIONS
    # ═══════════════════════════════════════════════════════════
    
    def docker_start_all(self) -> Dict:
        """Startet alle gestoppten Container"""
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--filter", "status=exited", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {"success": False, "error": result.stderr}
            
            stopped_containers = result.stdout.strip().split('\n')
            stopped_containers = [c for c in stopped_containers if c]  # Remove empty
            
            if not stopped_containers:
                return {
                    "success": True,
                    "message": "Keine gestoppten Container gefunden",
                    "started": []
                }
            
            # Start all
            started = []
            for container in stopped_containers:
                start_result = subprocess.run(
                    ["docker", "start", container],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if start_result.returncode == 0:
                    started.append(container)
            
            return {
                "success": True,
                "message": f"{len(started)} Container gestartet",
                "started": started
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def docker_stop_all(self) -> Dict:
        """Stoppt alle laufenden Container (GEFÄHRLICH!)"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {"success": False, "error": result.stderr}
            
            running_containers = result.stdout.strip().split('\n')
            running_containers = [c for c in running_containers if c]
            
            if not running_containers:
                return {
                    "success": True,
                    "message": "Keine laufenden Container",
                    "stopped": []
                }
            
            # Stop all
            stopped = []
            for container in running_containers:
                stop_result = subprocess.run(
                    ["docker", "stop", container],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if stop_result.returncode == 0:
                    stopped.append(container)
            
            return {
                "success": True,
                "message": f"{len(stopped)} Container gestoppt",
                "stopped": stopped
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def docker_restart_all(self) -> Dict:
        """Restart aller laufenden Container"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            running_containers = result.stdout.strip().split('\n')
            running_containers = [c for c in running_containers if c]
            
            restarted = []
            for container in running_containers:
                restart_result = subprocess.run(
                    ["docker", "restart", container],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if restart_result.returncode == 0:
                    restarted.append(container)
            
            return {
                "success": True,
                "message": f"{len(restarted)} Container neugestartet",
                "restarted": restarted
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def docker_cleanup(self) -> Dict:
        """Räumt auf: dangling images, stopped containers, unused volumes"""
        try:
            # Prune system
            result = subprocess.run(
                ["docker", "system", "prune", "-f"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "message": "Docker cleanup durchgeführt",
                "output": result.stdout
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def docker_status_check(self) -> Dict:
        """Quick Status Check aller Container"""
        try:
            # Running containers
            running_result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # All containers
            all_result = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Stopped containers
            stopped_result = subprocess.run(
                ["docker", "ps", "-a", "--filter", "status=exited", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            running = [c for c in running_result.stdout.strip().split('\n') if c]
            all_containers = [c for c in all_result.stdout.strip().split('\n') if c]
            stopped = [c for c in stopped_result.stdout.strip().split('\n') if c]
            
            return {
                "success": True,
                "running": len(running),
                "total": len(all_containers),
                "stopped": len(stopped),
                "containers": {
                    "running": running,
                    "stopped": stopped
                }
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ═══════════════════════════════════════════════════════════
    # 🚀 SEMAPHORE QUICK ACTIONS
    # ═══════════════════════════════════════════════════════════
    
    def semaphore_deploy_minimal(self) -> Dict:
        """Triggert Minimal Profile Deployment"""
        return self._semaphore_trigger_task("Deploy Minimal Profile")
    
    def semaphore_deploy_standard(self) -> Dict:
        """Triggert Standard Profile Deployment"""
        return self._semaphore_trigger_task("Deploy Standard Profile")
    
    def semaphore_deploy_full(self) -> Dict:
        """Triggert Full Profile Deployment"""
        return self._semaphore_trigger_task("Deploy Full Profile")
    
    def semaphore_status(self) -> Dict:
        """Holt Semaphore Status"""
        try:
            response = requests.get(
                f"{self.semaphore_url}/api/ping",
                timeout=5
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "status": "online",
                    "message": "Semaphore ist erreichbar"
                }
            else:
                return {
                    "success": False,
                    "status": "error",
                    "message": f"HTTP {response.status_code}"
                }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "status": "offline",
                "message": "Semaphore nicht erreichbar"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _semaphore_trigger_task(self, task_name: str) -> Dict:
        """
        Interner Helper: Triggert Semaphore Task
        
        Args:
            task_name: Name des Task Templates
        
        Returns:
            Result Dict
        """
        try:
            # Check if Semaphore is reachable
            status = self.semaphore_status()
            if not status.get("success"):
                return {
                    "success": False,
                    "error": "Semaphore nicht erreichbar",
                    "details": status
                }
            
            # TODO: Implement actual Semaphore API call
            # For now, return mock response
            return {
                "success": True,
                "message": f"Deployment '{task_name}' würde getriggert",
                "task": task_name,
                "note": "API-Integration noch nicht implementiert"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ═══════════════════════════════════════════════════════════
    # 💻 SYSTEM QUICK ACTIONS
    # ═══════════════════════════════════════════════════════════
    
    def system_health_quick(self) -> Dict:
        """Quick System Health Check"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Determine overall health
            warnings = []
            if cpu > 80:
                warnings.append("CPU usage high")
            if mem.percent > 80:
                warnings.append("RAM usage high")
            if disk.percent > 80:
                warnings.append("Disk usage high")
            
            overall = "healthy" if not warnings else "warning"
            
            return {
                "success": True,
                "overall": overall,
                "warnings": warnings,
                "cpu": {
                    "percent": cpu,
                    "status": "🟢 OK" if cpu < 70 else "🟡 High" if cpu < 90 else "🔴 Critical"
                },
                "ram": {
                    "percent": mem.percent,
                    "used_gb": round(mem.used / (1024**3), 1),
                    "total_gb": round(mem.total / (1024**3), 1),
                    "status": "🟢 OK" if mem.percent < 70 else "🟡 High" if mem.percent < 90 else "🔴 Critical"
                },
                "disk": {
                    "percent": disk.percent,
                    "free_gb": round(disk.free / (1024**3), 1),
                    "total_gb": round(disk.total / (1024**3), 1),
                    "status": "🟢 OK" if disk.percent < 70 else "🟡 High" if disk.percent < 90 else "🔴 Critical"
                }
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def system_uptime(self) -> Dict:
        """System Uptime"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = datetime.now().timestamp() - boot_time
            
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            uptime_formatted = f"{days}d {hours}h {minutes}m"
            
            return {
                "success": True,
                "uptime_seconds": uptime_seconds,
                "uptime_formatted": uptime_formatted,
                "boot_time": datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def logs_recent_errors(self) -> Dict:
        """Sucht nach recent errors in Docker logs"""
        try:
            # Get running containers
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            containers = [c for c in result.stdout.strip().split('\n') if c]
            
            errors = []
            for container in containers[:5]:  # Limit to 5 containers
                # Get last 50 lines of logs
                logs_result = subprocess.run(
                    ["docker", "logs", "--tail", "50", container],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                # Search for error keywords
                for line in logs_result.stderr.split('\n'):
                    if any(keyword in line.lower() for keyword in ['error', 'fatal', 'exception', 'failed']):
                        errors.append({
                            "container": container,
                            "line": line.strip()
                        })
            
            return {
                "success": True,
                "errors_count": len(errors),
                "errors": errors[:10]  # Limit to 10 errors
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ═══════════════════════════════════════════════════════════
    # 🎯 COMPOSITE ACTIONS (Multi-Step)
    # ═══════════════════════════════════════════════════════════
    
    def morning_routine(self) -> Dict:
        """Morning Startup Routine"""
        results = {
            "success": True,
            "steps": []
        }
        
        # Step 1: Start all containers
        docker_start = self.docker_start_all()
        results["steps"].append({
            "name": "Start Docker Containers",
            "success": docker_start.get("success"),
            "message": docker_start.get("message")
        })
        
        # Step 2: Health Check
        health = self.system_health_quick()
        results["steps"].append({
            "name": "System Health Check",
            "success": health.get("success"),
            "message": f"Overall: {health.get('overall', 'unknown')}"
        })
        
        # Step 3: Check Semaphore
        semaphore = self.semaphore_status()
        results["steps"].append({
            "name": "Semaphore Status",
            "success": semaphore.get("success"),
            "message": semaphore.get("message")
        })
        
        # Overall success
        results["success"] = all(step["success"] for step in results["steps"])
        results["message"] = "Morning Routine abgeschlossen!"
        
        return results
    
    def emergency_stop(self) -> Dict:
        """Emergency Stop - Stoppt alle Container"""
        return self.docker_stop_all()


# ============================================================================
# Singleton Instance
# ============================================================================

_quick_actions_instance = None

def get_quick_actions() -> QuickActions:
    """
    Gibt Singleton-Instance von QuickActions zurück
    
    Returns:
        QuickActions Instance
    """
    global _quick_actions_instance
    if _quick_actions_instance is None:
        _quick_actions_instance = QuickActions()
    return _quick_actions_instance
