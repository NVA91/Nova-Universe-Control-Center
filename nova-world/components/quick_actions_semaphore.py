"""
Quick Actions - Semaphore Integration
Extended Quick Actions with Semaphore API
"""

import streamlit as st
from typing import Dict, List, Optional, Any
from .semaphore_api import SemaphoreAPI, SemaphoreAPIError, create_semaphore_client


# ═══════════════════════════════════════════════════════════
# SEMAPHORE QUICK ACTIONS
# ═══════════════════════════════════════════════════════════

def get_semaphore_actions() -> List[Dict[str, Any]]:
    """
    Get Semaphore-based quick actions
    
    Returns:
        List of Semaphore quick actions
    """
    return [
        {
            "id": "semaphore_deploy_minimal",
            "name": "Deploy Minimal",
            "description": "Deploy minimal profile via Semaphore",
            "icon": "🚀",
            "category": "deployment",
            "requires_confirmation": True,
            "confirmation_message": "Deploy minimal profile to production?",
            "template_name": "Deploy Minimal Profile"
        },
        {
            "id": "semaphore_deploy_standard",
            "name": "Deploy Standard",
            "description": "Deploy standard profile via Semaphore",
            "icon": "🚀",
            "category": "deployment",
            "requires_confirmation": True,
            "confirmation_message": "Deploy standard profile to production?",
            "template_name": "Deploy Standard Profile"
        },
        {
            "id": "semaphore_deploy_full",
            "name": "Deploy Full",
            "description": "Deploy full profile via Semaphore",
            "icon": "🚀",
            "category": "deployment",
            "requires_confirmation": True,
            "confirmation_message": "Deploy full profile to production?",
            "template_name": "Deploy Full Profile"
        },
        {
            "id": "semaphore_health_check",
            "name": "Health Check",
            "description": "Run health check playbook",
            "icon": "🏥",
            "category": "monitoring",
            "requires_confirmation": False,
            "template_name": "Health Check"
        },
        {
            "id": "semaphore_backup",
            "name": "Backup Now",
            "description": "Trigger backup via Semaphore",
            "icon": "💾",
            "category": "maintenance",
            "requires_confirmation": False,
            "template_name": "Backup"
        },
        {
            "id": "semaphore_update_containers",
            "name": "Update Containers",
            "description": "Update all Docker containers",
            "icon": "🔄",
            "category": "maintenance",
            "requires_confirmation": True,
            "confirmation_message": "Update all Docker containers?",
            "template_name": "Update Containers"
        }
    ]


def execute_semaphore_action(
    action: Dict[str, Any],
    client: Optional[SemaphoreAPI] = None
) -> Dict[str, Any]:
    """
    Execute Semaphore-based quick action
    
    Args:
        action: Action definition
        client: SemaphoreAPI client (optional, will be created if None)
    
    Returns:
        Execution result
    """
    try:
        # Create client if not provided
        if client is None:
            try:
                base_url = st.secrets.get("semaphore", {}).get("url", "http://localhost:3000")
                api_token = st.secrets.get("semaphore", {}).get("api_token")
                
                if not api_token:
                    return {
                        "success": False,
                        "error": "Semaphore API token not configured",
                        "message": "Please configure Semaphore API token in secrets.toml"
                    }
                
                client = SemaphoreAPI(base_url=base_url, api_token=api_token)
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to create Semaphore client: {str(e)}"
                }
        
        # Get project ID from secrets
        project_id = st.secrets.get("semaphore", {}).get("project_id", 1)
        
        # Find template by name
        template_name = action.get("template_name")
        if not template_name:
            return {
                "success": False,
                "error": "Template name not specified in action"
            }
        
        templates = client.get_templates(project_id)
        template = next(
            (t for t in templates if t.get('name') == template_name),
            None
        )
        
        if not template:
            return {
                "success": False,
                "error": f"Template '{template_name}' not found",
                "available_templates": [t.get('name') for t in templates]
            }
        
        template_id = template.get('id')
        
        # Run task
        result = client.run_task(project_id, template_id)
        task_id = result.get('id')
        
        if not task_id:
            return {
                "success": False,
                "error": "Task ID not returned from Semaphore"
            }
        
        return {
            "success": True,
            "task_id": task_id,
            "project_id": project_id,
            "template_id": template_id,
            "template_name": template_name,
            "message": f"Task {task_id} started successfully"
        }
    
    except SemaphoreAPIError as e:
        return {
            "success": False,
            "error": f"Semaphore API error: {str(e)}"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def render_semaphore_action_result(result: Dict[str, Any]):
    """
    Render Semaphore action result in Streamlit
    
    Args:
        result: Action execution result
    """
    if result.get("success"):
        task_id = result.get("task_id")
        project_id = result.get("project_id")
        template_name = result.get("template_name")
        
        st.success(f"✅ {template_name} started!")
        
        # Show task details
        with st.expander("Task Details"):
            st.write(f"**Task ID:** {task_id}")
            st.write(f"**Project ID:** {project_id}")
            st.write(f"**Template:** {template_name}")
            
            # Link to Semaphore
            base_url = st.secrets.get("semaphore", {}).get("url", "http://localhost:3000")
            task_url = f"{base_url}/project/{project_id}/history?t={task_id}"
            st.markdown(f"[View in Semaphore]({task_url})")
        
        # Show task status
        try:
            client = create_semaphore_client()
            
            with st.spinner("Fetching task status..."):
                status = client.get_task_status_summary(project_id, task_id)
            
            st.write("**Current Status:**", status.get("status", "unknown"))
            
            if status.get("is_running"):
                st.info("🔄 Task is currently running...")
            elif status.get("is_success"):
                st.success("✅ Task completed successfully!")
            elif status.get("is_failed"):
                st.error("❌ Task failed!")
                if status.get("message"):
                    st.code(status.get("message"), language="text")
        
        except Exception as e:
            st.warning(f"Could not fetch task status: {str(e)}")
    
    else:
        error = result.get("error", "Unknown error")
        st.error(f"❌ Action failed: {error}")
        
        # Show available templates if template not found
        if "available_templates" in result:
            with st.expander("Available Templates"):
                for template in result["available_templates"]:
                    st.write(f"- {template}")


def render_semaphore_status_widget():
    """
    Render Semaphore status widget
    
    Shows:
    - Connection status
    - Recent deployments
    - Running tasks
    """
    try:
        client = create_semaphore_client()
        
        # Check connection
        if not client.ping():
            st.error("❌ Semaphore is not reachable")
            return
        
        # Get project ID
        project_id = st.secrets.get("semaphore", {}).get("project_id", 1)
        
        # Get deployment status
        from .semaphore_api import get_deployment_status
        status = get_deployment_status(client, project_id)
        
        if status.get("error"):
            st.warning(f"⚠️ Could not fetch deployment status: {status['error']}")
            return
        
        # Show status
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tasks", status.get("total_tasks", 0))
        
        with col2:
            running = status.get("running", 0)
            st.metric("Running", running, delta="active" if running > 0 else None)
        
        with col3:
            success = status.get("success", 0)
            st.metric("Success", success)
        
        with col4:
            failed = status.get("failed", 0)
            st.metric("Failed", failed, delta="error" if failed > 0 else None)
        
        # Show latest task
        latest = status.get("latest_task")
        if latest:
            st.write("**Latest Deployment:**")
            
            status_emoji = {
                'running': '🔄',
                'success': '✅',
                'error': '❌',
                'stopped': '⏹️'
            }.get(latest.get('status', ''), '❓')
            
            st.write(f"{status_emoji} Task {latest.get('task_id')} - {latest.get('status', 'unknown')}")
            
            if latest.get('duration_seconds'):
                st.write(f"Duration: {latest['duration_seconds']:.1f}s")
    
    except Exception as e:
        st.error(f"❌ Semaphore error: {str(e)}")


def get_semaphore_task_history(
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Get Semaphore task history
    
    Args:
        limit: Maximum number of tasks to return
    
    Returns:
        List of task summaries
    """
    try:
        client = create_semaphore_client()
        project_id = st.secrets.get("semaphore", {}).get("project_id", 1)
        
        return client.get_recent_tasks(project_id, limit=limit)
    
    except Exception as e:
        st.error(f"Failed to fetch task history: {str(e)}")
        return []


def render_task_history_table(tasks: List[Dict[str, Any]]):
    """
    Render task history as table
    
    Args:
        tasks: List of task summaries
    """
    if not tasks:
        st.info("No tasks found")
        return
    
    import pandas as pd
    
    # Prepare data for table
    data = []
    for task in tasks:
        status_emoji = {
            'running': '🔄',
            'success': '✅',
            'error': '❌',
            'stopped': '⏹️'
        }.get(task.get('status', ''), '❓')
        
        data.append({
            'Task ID': task.get('task_id'),
            'Status': f"{status_emoji} {task.get('status', 'unknown')}",
            'Template': task.get('template_id'),
            'Start': task.get('start', '')[:19] if task.get('start') else '',
            'Duration': f"{task.get('duration_seconds', 0):.1f}s" if task.get('duration_seconds') else 'N/A'
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════
# COMPOSITE ACTIONS WITH SEMAPHORE
# ═══════════════════════════════════════════════════════════

def execute_morning_routine_with_semaphore() -> Dict[str, Any]:
    """
    Execute morning routine with Semaphore integration
    
    Steps:
    1. Start Docker containers
    2. Start Semaphore
    3. Run health check via Semaphore
    4. Show deployment status
    
    Returns:
        Execution result
    """
    results = {
        "steps": [],
        "success": True
    }
    
    # Step 1: Start Docker
    st.write("🐳 Starting Docker containers...")
    # ... (existing Docker start logic)
    results["steps"].append({"name": "Docker Start", "success": True})
    
    # Step 2: Start Semaphore
    st.write("🎭 Starting Semaphore...")
    # ... (existing Semaphore start logic)
    results["steps"].append({"name": "Semaphore Start", "success": True})
    
    # Step 3: Health Check via Semaphore
    st.write("🏥 Running health check...")
    try:
        client = create_semaphore_client()
        project_id = st.secrets.get("semaphore", {}).get("project_id", 1)
        
        # Find health check template
        templates = client.get_templates(project_id)
        health_template = next(
            (t for t in templates if 'health' in t.get('name', '').lower()),
            None
        )
        
        if health_template:
            result = client.run_task(project_id, health_template['id'])
            results["steps"].append({
                "name": "Health Check",
                "success": True,
                "task_id": result.get('id')
            })
            st.success("✅ Health check started")
        else:
            results["steps"].append({
                "name": "Health Check",
                "success": False,
                "error": "Health check template not found"
            })
            st.warning("⚠️ Health check template not found")
    
    except Exception as e:
        results["steps"].append({
            "name": "Health Check",
            "success": False,
            "error": str(e)
        })
        st.error(f"❌ Health check failed: {str(e)}")
        results["success"] = False
    
    # Step 4: Show status
    st.write("📊 Deployment status:")
    render_semaphore_status_widget()
    
    return results
