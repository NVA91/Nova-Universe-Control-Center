"""
UI Components für Nova World Dashboard
Optimiert für stabiles Layout
"""

import streamlit as st
from typing import Dict, Any
from components.quick_actions import get_quick_actions

def apply_layout_fixes():
    """
    Wendet CSS-Fixes für stabiles Layout an
    """
    st.markdown("""
        <style>
        /* ==================== SIDEBAR FIX ==================== */
        [data-testid="stSidebar"] {
            min-width: 280px !important;
            max-width: 280px !important;
            width: 280px !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            width: 280px !important;
        }
        
        /* ==================== MAIN CONTENT ==================== */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-top: 1rem !important;
        }
        
        /* ==================== BUTTON LAYOUT ==================== */
        .stButton button {
            width: 100% !important;
            min-height: 100px !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            text-align: center !important;
            font-size: 1.1rem !important;
            padding: 1rem !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        }
        
        /* ==================== GRID LAYOUT ==================== */
        div[data-testid="column"] {
            padding: 0.5rem !important;
            min-width: 0 !important;
        }
        
        /* ==================== TEXT OVERFLOW FIX ==================== */
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            max-width: 100% !important;
        }
        
        /* ==================== CARD STYLING ==================== */
        .action-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* ==================== METRICS FIX ==================== */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        /* ==================== RESPONSIVE BREAKPOINTS ==================== */
        @media (max-width: 1400px) {
            .main .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
        }
        
        @media (max-width: 1200px) {
            [data-testid="stSidebar"] {
                min-width: 250px !important;
                max-width: 250px !important;
            }
        }
        
        /* ==================== SCROLLBAR STYLING ==================== */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)


def render_quick_actions_grid():
    """
    Rendert Quick Actions Grid mit optimiertem Layout
    """
    apply_layout_fixes()
    
    qa = get_quick_actions()
    
    st.markdown("## ⚡ Quick Actions")
    st.markdown("---")
    
    # ==================== ROW 1: DEPLOYMENT & DOCKER ====================
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Deployment")
        
        if st.button("🎯 Minimal", key="deploy_min", use_container_width=True, help="Deploy Minimal Profile"):
            with st.spinner("Deploying Minimal..."):
                result = qa.deploy_minimal()
                if result['success']:
                    st.success(result['message'])
                    st.toast("✅ Minimal deployed!", icon="🚀")
                else:
                    st.error(result['message'])
        
        if st.button("⭐ Standard", key="deploy_std", use_container_width=True, help="Deploy Standard Profile"):
            with st.spinner("Deploying Standard..."):
                result = qa.deploy_standard()
                if result['success']:
                    st.success(result['message'])
                    st.toast("✅ Standard deployed!", icon="⭐")
                else:
                    st.error(result['message'])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("### 🐳 Docker")
        
        if st.button("▶️ Start All", key="docker_start", use_container_width=True, help="Start all containers"):
            with st.spinner("Starting containers..."):
                result = qa.docker_start_all()
                if result['success']:
                    st.success(result['message'])
                    st.toast("✅ Containers started!", icon="🐳")
                else:
                    st.error(result['message'])
        
        if st.button("🔄 Restart All", key="docker_restart", use_container_width=True, help="Restart all containers"):
            with st.spinner("Restarting containers..."):
                result = qa.docker_restart_all()
                if result['success']:
                    st.success(result['message'])
                    st.toast("✅ Containers restarted!", icon="🔄")
                else:
                    st.error(result['message'])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("### 🔧 System")
        
        if st.button("🏥 Health Check", key="health_check", use_container_width=True, help="Check system health"):
            with st.spinner("Checking system health..."):
                result = qa.system_health_check()
                if result['success']:
                    st.success(result['message'])
                    with st.expander("📊 Details"):
                        details = result.get('details', {})
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("CPU", details.get('cpu', {}).get('usage', 'N/A'))
                        with col_b:
                            st.metric("Memory", details.get('memory', {}).get('usage', 'N/A'))
                        with col_c:
                            st.metric("Disk", details.get('disk', {}).get('usage', 'N/A'))
                else:
                    st.error(result['message'])
        
        if st.button("🔍 Check Errors", key="check_errors", use_container_width=True, help="Check for system errors"):
            with st.spinner("Checking for errors..."):
                result = qa.check_errors()
                if result['success']:
                    if result.get('details', {}).get('unhealthy', []):
                        st.warning(result['message'])
                        with st.expander("⚠️ Errors"):
                            for error in result['details']['unhealthy']:
                                st.code(error)
                    else:
                        st.success(result['message'])
                else:
                    st.error(result['message'])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Status")
        
        if st.button("🚀 Deploy Status", key="deploy_status", use_container_width=True, help="Check deployment status"):
            with st.spinner("Fetching deployment status..."):
                result = qa.get_deployment_status()
                if result['success']:
                    st.info(result['message'])
                else:
                    st.warning(result['message'])
        
        if st.button("🐳 Docker Status", key="docker_status", use_container_width=True, help="Check Docker status"):
            with st.spinner("Fetching Docker status..."):
                result = qa.docker_status_check()
                if result['success']:
                    st.info(result['message'])
                    details = result.get('details', {})
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Running", details.get('running', 0))
                    with col_b:
                        st.metric("Total", details.get('total', 0))
                else:
                    st.error(result['message'])
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_system_metrics():
    """
    Rendert System-Metriken mit optimiertem Layout
    """
    apply_layout_fixes()
    
    qa = get_quick_actions()
    
    # System Health Check für Metriken
    health = qa.system_health_check()
    
    if health['success']:
        details = health.get('details', {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cpu = details.get('cpu', {})
            cpu_usage = cpu.get('usage', 'N/A')
            cpu_status = cpu.get('status', '❓')
            st.metric(
                label="🖥️ CPU",
                value=cpu_usage,
                delta=cpu_status,
                delta_color="normal" if "✅" in cpu_status else "off"
            )
        
        with col2:
            mem = details.get('memory', {})
            mem_usage = mem.get('usage', 'N/A')
            mem_status = mem.get('status', '❓')
            st.metric(
                label="💾 Memory",
                value=mem_usage,
                delta=mem_status,
                delta_color="normal" if "✅" in mem_status else "off"
            )
        
        with col3:
            disk = details.get('disk', {})
            disk_usage = disk.get('usage', 'N/A')
            disk_status = disk.get('status', '❓')
            st.metric(
                label="💿 Disk",
                value=disk_usage,
                delta=disk_status,
                delta_color="normal" if "✅" in disk_status else "off"
            )
    else:
        st.error("Fehler beim Laden der System-Metriken")


def render_sidebar_status():
    """
    Rendert Sidebar-Status
    """
    with st.sidebar:
        st.markdown("### 📊 System Status")
        
        qa = get_quick_actions()
        health = qa.system_health_check()
        
        if health['success']:
            details = health.get('details', {})
            
            # CPU
            cpu_usage = details.get('cpu', {}).get('usage', 'N/A')
            st.metric("CPU", cpu_usage)
            
            # Memory
            mem_usage = details.get('memory', {}).get('usage', 'N/A')
            st.metric("RAM", mem_usage)
            
            # Disk
            disk_usage = details.get('disk', {}).get('usage', 'N/A')
            st.metric("Disk", disk_usage)
        
        st.markdown("---")
