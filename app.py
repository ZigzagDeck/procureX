import streamlit as st

st.set_page_config(
    page_title="ProcureX — Autonomous Procurement Research",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0a0e27;
        color: #ffffff;
    }
    
    .stSidebar {
        background-color: rgba(10, 14, 39, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 40px rgba(6, 182, 212, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: opacity 0.3s;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        color: white;
    }
    
    .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 1px #3b82f6;
    }

    .nav-btn {
        display: block;
        width: 100%;
        padding: 10px 14px;
        margin-bottom: 8px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #cbd5e1;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
    }
    .nav-btn:hover {
        background: rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
        color: white;
    }
    
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    if "research_active" not in st.session_state:
        st.session_state.research_active = False
    if "requirement" not in st.session_state:
        st.session_state.requirement = None
    if "budget" not in st.session_state:
        st.session_state.budget = 1000.0
    if "spent" not in st.session_state:
        st.session_state.spent = 0.0
    if "suppliers" not in st.session_state:
        st.session_state.suppliers = []
    if "evidence" not in st.session_state:
        st.session_state.evidence = {}
    if "transactions" not in st.session_state:
        st.session_state.transactions = []
    if "progress_log" not in st.session_state:
        st.session_state.progress_log = []

def main():
    apply_custom_css()
    init_session_state()

    # Sidebar Header
    st.sidebar.markdown(
        """
        <div style='text-align: center; margin-bottom: 20px;'>
            <h1 style='margin-bottom: 0;'><span class="gradient-text">ProcureX</span></h1>
            <p style='color: #a0aec0; font-size: 0.85rem;'>Autonomous B2B Procurement Agent</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Custom Navigation Buttons in Sidebar
    st.sidebar.markdown("### 📌 Navigation")
    
    pages = [
        ("📝 Requirement Input", "pages/1_research.py"),
        ("📡 Live Research Status", "pages/2_live_research.py"),
        ("🏭 Discovered Suppliers", "pages/3_suppliers.py"),
        ("🔗 Evidence Browser", "pages/4_evidence.py"),
        ("💰 Economic Trace", "pages/5_economic_trace.py"),
        ("📋 Final Report", "pages/6_final_report.py"),
    ]
    
    for title, path in pages:
        if st.sidebar.button(title, key=f"nav_{path}", use_container_width=True):
            st.switch_page(path)

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='font-size:0.8rem; color:#64748b; text-align:center;'>ProcureX v1.0 MVP &bull; x402 Protocol</div>",
        unsafe_allow_html=True
    )
    
    # Home Page Content
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Welcome to <span class='gradient-text'>ProcureX</span></h1>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <p style="font-size: 1.2rem; color: #cbd5e1; margin-bottom: 2rem;">
                Autonomous B2B procurement research agent for Indian B2B markets. 
                Parses complex natural-language requirements, discovers & deduplicates suppliers, 
                verifies business credentials, and makes economic information-buying decisions using x402.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="text-align: center;">🔍 Discovery</h3>
            <p style="color: #94a3b8; text-align: center;">Autonomous search across multiple web sources and directories with rate-limited fetching.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="text-align: center;">✅ Verification</h3>
            <p style="color: #94a3b8; text-align: center;">Cross-referencing claims against GSTIN records, evidence graphs, and flagging price discrepancies.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3 style="text-align: center;">📊 Scoring & x402</h3>
            <p style="color: #94a3b8; text-align: center;">Deterministic 6-dimension scoring and x402 HTTP 402 micro-payment information allocation.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀 Start Procurement Research Now", type="primary", use_container_width=True):
            st.switch_page("pages/1_research.py")

if __name__ == "__main__":
    main()
