"""
Layout-Optimierung für render_quick_actions_grid()
"""

def get_responsive_columns():
    """
    Responsive Column-Layout basierend auf Viewport
    """
    import streamlit as st
    
    # Viewport-Info (via Custom Component später)
    # Für jetzt: Fixed aber sauber
    
    return {
        'desktop': [1, 1, 1, 1],  # 4 Spalten
        'tablet': [1, 1],          # 2 Spalten
        'mobile': [1]              # 1 Spalte
    }

def render_quick_actions_grid_optimized():
    """
    Optimierte Version mit Fixed Layout
    """
    import streamlit as st
    from components.quick_actions import get_quick_actions
    
    st.markdown("""
        <style>
        /* Sidebar Width Fix */
        [data-testid="stSidebar"] {
            min-width: 250px !important;
            max-width: 250px !important;
            width: 250px !important;
        }
        
        /* Main Content Responsive */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        /* Card Layout Fix */
        .stButton button {
            width: 100% !important;
            min-height: 80px !important;
            white-space: normal !important;
            word-wrap: break-word !important;
        }
        
        /* Grid Gap */
        div[data-testid="column"] {
            padding: 0.5rem !important;
        }
        
        /* Prevent Text Overflow */
        .stMarkdown {
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    qa = get_quick_actions()
    
    # Grid mit festen Spalten (4 Columns)
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown("### 🚀 Deployment")
        if st.button("🚀 Minimal Deploy", key="deploy_min", use_container_width=True):
            with st.spinner("Deploying Minimal..."):
                result = qa.deploy_minimal()
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['message'])
    
    with col2:
        st.markdown("### 🐳 Docker")
        if st.button("▶️ Start All", key="docker_start", use_container_width=True):
            with st.spinner("Starting containers..."):
                result = qa.docker_start_all()
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['message'])
    
    with col3:
        st.markdown("### 🔧 System")
        if st.button("🏥 Health Check", key="health_check", use_container_width=True):
            with st.spinner("Checking system..."):
                result = qa.system_health_check()
                if result['success']:
                    st.success(result['message'])
                    with st.expander("Details"):
                        st.json(result.get('details', {}))
                else:
                    st.error(result['message'])
    
    with col4:
        st.markdown("### 📊 Status")
        if st.button("📊 Deployment Status", key="deploy_status", use_container_width=True):
            with st.spinner("Fetching status..."):
                result = qa.get_deployment_status()
                if result['success']:
                    st.info(result['message'])
                else:
                    st.warning(result['message'])

