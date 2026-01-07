"""
Semaphore API Client
Full REST API Integration for Ansible Semaphore
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)


class SemaphoreAPIError(Exception):
    """Base exception for Semaphore API errors"""
    pass


class SemaphoreAPI:
    """
    Semaphore REST API Client
    
    Provides full integration with Ansible Semaphore REST API:
    - Projects management
    - Task templates
    - Job execution and monitoring
    - Live logs streaming
    - Job history
    """
    
    def __init__(
        self,
        base_url: str,
        api_token: str,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize Semaphore API client
        
        Args:
            base_url: Semaphore base URL (e.g., http://localhost:3000)
            api_token: API token from Semaphore user settings
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
        self.timeout = timeout
        self.max_retries = max_retries
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without /api prefix)
            **kwargs: Additional arguments for requests
        
        Returns:
            Response JSON data
        
        Raises:
            SemaphoreAPIError: On API error
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # Handle different status codes
                if response.status_code == 200:
                    return response.json() if response.content else {}
                elif response.status_code == 201:
                    return response.json() if response.content else {}
                elif response.status_code == 204:
                    return {}
                elif response.status_code == 401:
                    raise SemaphoreAPIError("Unauthorized: Invalid API token")
                elif response.status_code == 404:
                    raise SemaphoreAPIError(f"Not found: {endpoint}")
                elif response.status_code >= 500:
                    # Retry on server errors
                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    raise SemaphoreAPIError(f"Server error: {response.status_code}")
                else:
                    error_msg = response.text or f"HTTP {response.status_code}"
                    raise SemaphoreAPIError(f"API error: {error_msg}")
            
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise SemaphoreAPIError("Request timeout")
            
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise SemaphoreAPIError("Connection error: Cannot reach Semaphore")
            
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise SemaphoreAPIError(f"Unexpected error: {str(e)}")
        
        raise SemaphoreAPIError("Max retries exceeded")
    
    # ═══════════════════════════════════════════════════════════
    # HEALTH & INFO
    # ═══════════════════════════════════════════════════════════
    
    def ping(self) -> bool:
        """
        Check if Semaphore is reachable
        
        Returns:
            True if Semaphore is reachable, False otherwise
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/ping",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get Semaphore server info
        
        Returns:
            Server info including version
        """
        return self._request('GET', '/info')
    
    # ═══════════════════════════════════════════════════════════
    # PROJECTS
    # ═══════════════════════════════════════════════════════════
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """
        Get all projects
        
        Returns:
            List of projects
        """
        return self._request('GET', '/projects')
    
    def get_project(self, project_id: int) -> Dict[str, Any]:
        """
        Get project by ID
        
        Args:
            project_id: Project ID
        
        Returns:
            Project details
        """
        return self._request('GET', f'/projects/{project_id}')
    
    # ═══════════════════════════════════════════════════════════
    # TEMPLATES
    # ═══════════════════════════════════════════════════════════
    
    def get_templates(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Get all task templates for a project
        
        Args:
            project_id: Project ID
        
        Returns:
            List of task templates
        """
        return self._request('GET', f'/project/{project_id}/templates')
    
    def get_template(
        self,
        project_id: int,
        template_id: int
    ) -> Dict[str, Any]:
        """
        Get task template by ID
        
        Args:
            project_id: Project ID
            template_id: Template ID
        
        Returns:
            Template details
        """
        return self._request(
            'GET',
            f'/project/{project_id}/templates/{template_id}'
        )
    
    # ═══════════════════════════════════════════════════════════
    # TASKS (JOBS)
    # ═══════════════════════════════════════════════════════════
    
    def run_task(
        self,
        project_id: int,
        template_id: int,
        debug: bool = False,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Run a task (execute template)
        
        Args:
            project_id: Project ID
            template_id: Template ID
            debug: Enable debug mode
            dry_run: Enable dry-run mode (check mode)
        
        Returns:
            Task execution info including task_id
        """
        payload = {
            'template_id': template_id,
            'debug': debug,
            'dry_run': dry_run
        }
        
        return self._request(
            'POST',
            f'/project/{project_id}/tasks',
            json=payload
        )
    
    def get_tasks(
        self,
        project_id: int,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get task history for a project
        
        Args:
            project_id: Project ID
            limit: Maximum number of tasks to return
        
        Returns:
            List of tasks (job history)
        """
        return self._request(
            'GET',
            f'/project/{project_id}/tasks',
            params={'limit': limit}
        )
    
    def get_task(
        self,
        project_id: int,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Get task details by ID
        
        Args:
            project_id: Project ID
            task_id: Task ID
        
        Returns:
            Task details including status
        """
        return self._request(
            'GET',
            f'/project/{project_id}/tasks/{task_id}'
        )
    
    def get_task_output(
        self,
        project_id: int,
        task_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get task output (logs)
        
        Args:
            project_id: Project ID
            task_id: Task ID
        
        Returns:
            List of log entries
        """
        return self._request(
            'GET',
            f'/project/{project_id}/tasks/{task_id}/output'
        )
    
    def stop_task(
        self,
        project_id: int,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Stop a running task
        
        Args:
            project_id: Project ID
            task_id: Task ID
        
        Returns:
            Stop confirmation
        """
        return self._request(
            'POST',
            f'/project/{project_id}/tasks/{task_id}/stop'
        )
    
    # ═══════════════════════════════════════════════════════════
    # HELPER METHODS
    # ═══════════════════════════════════════════════════════════
    
    def wait_for_task(
        self,
        project_id: int,
        task_id: int,
        timeout: int = 600,
        poll_interval: int = 2
    ) -> Dict[str, Any]:
        """
        Wait for task to complete
        
        Args:
            project_id: Project ID
            task_id: Task ID
            timeout: Maximum wait time in seconds
            poll_interval: Polling interval in seconds
        
        Returns:
            Final task status
        
        Raises:
            SemaphoreAPIError: On timeout or error
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            task = self.get_task(project_id, task_id)
            status = task.get('status', '')
            
            if status in ['success', 'error', 'stopped']:
                return task
            
            time.sleep(poll_interval)
        
        raise SemaphoreAPIError(f"Task {task_id} timeout after {timeout}s")
    
    def get_task_status_summary(
        self,
        project_id: int,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Get task status summary
        
        Args:
            project_id: Project ID
            task_id: Task ID
        
        Returns:
            Status summary with human-readable info
        """
        task = self.get_task(project_id, task_id)
        
        status = task.get('status', 'unknown')
        start = task.get('start', '')
        end = task.get('end', '')
        
        # Calculate duration
        duration = None
        if start and end:
            try:
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                duration = (end_dt - start_dt).total_seconds()
            except:
                pass
        
        return {
            'task_id': task_id,
            'status': status,
            'template_id': task.get('template_id'),
            'start': start,
            'end': end,
            'duration_seconds': duration,
            'message': task.get('message', ''),
            'is_running': status == 'running',
            'is_success': status == 'success',
            'is_failed': status == 'error',
            'is_stopped': status == 'stopped'
        }
    
    def get_recent_tasks(
        self,
        project_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent tasks with status summaries
        
        Args:
            project_id: Project ID
            limit: Maximum number of tasks
        
        Returns:
            List of task summaries
        """
        tasks = self.get_tasks(project_id, limit=limit)
        
        summaries = []
        for task in tasks:
            task_id = task.get('id')
            if task_id:
                try:
                    summary = self.get_task_status_summary(project_id, task_id)
                    summaries.append(summary)
                except:
                    # Skip failed tasks
                    pass
        
        return summaries
    
    def stream_task_logs(
        self,
        project_id: int,
        task_id: int,
        follow: bool = True,
        poll_interval: int = 2
    ):
        """
        Stream task logs (generator)
        
        Args:
            project_id: Project ID
            task_id: Task ID
            follow: Follow logs until task completes
            poll_interval: Polling interval in seconds
        
        Yields:
            Log entries
        """
        last_log_id = 0
        
        while True:
            # Get task status
            task = self.get_task(project_id, task_id)
            status = task.get('status', '')
            
            # Get logs
            logs = self.get_task_output(project_id, task_id)
            
            # Yield new logs
            for log in logs:
                log_id = log.get('id', 0)
                if log_id > last_log_id:
                    yield log
                    last_log_id = log_id
            
            # Check if task is done
            if status in ['success', 'error', 'stopped']:
                break
            
            if not follow:
                break
            
            time.sleep(poll_interval)


# ═══════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════

def create_semaphore_client(
    base_url: str = "http://localhost:3000",
    api_token: Optional[str] = None
) -> SemaphoreAPI:
    """
    Create Semaphore API client from config
    
    Args:
        base_url: Semaphore base URL
        api_token: API token (if None, tries to get from secrets)
    
    Returns:
        SemaphoreAPI client
    
    Raises:
        ValueError: If API token is not provided
    """
    if not api_token:
        try:
            import streamlit as st
            api_token = st.secrets.get("semaphore", {}).get("api_token")
        except:
            pass
    
    if not api_token:
        raise ValueError("Semaphore API token required")
    
    return SemaphoreAPI(base_url=base_url, api_token=api_token)


def get_deployment_status(
    client: SemaphoreAPI,
    project_id: int
) -> Dict[str, Any]:
    """
    Get deployment status overview
    
    Args:
        client: SemaphoreAPI client
        project_id: Project ID
    
    Returns:
        Deployment status overview
    """
    try:
        # Get recent tasks
        tasks = client.get_recent_tasks(project_id, limit=10)
        
        # Count by status
        running = sum(1 for t in tasks if t['is_running'])
        success = sum(1 for t in tasks if t['is_success'])
        failed = sum(1 for t in tasks if t['is_failed'])
        
        # Get latest task
        latest = tasks[0] if tasks else None
        
        return {
            'total_tasks': len(tasks),
            'running': running,
            'success': success,
            'failed': failed,
            'latest_task': latest,
            'is_healthy': failed == 0 and running <= 1
        }
    
    except Exception as e:
        return {
            'error': str(e),
            'is_healthy': False
        }
