import streamlit as st

st.set_page_config(
    page_title="ProcureX — Autonomous Procurement Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    }

    /* Hide default Streamlit sidebar native page list */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 60%, #090d16 100%);
        color: #f8fafc;
    }
    
    .stSidebar {
        background-color: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 12px 40px -10px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 600;
        font-family: 'Plus Jakarta Sans', sans-serif;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3);
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
        color: white;
    }
    
    .step-badge {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(129, 140, 248, 0.2));
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-block;
        margin-bottom: 8px;
    }

    .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.6);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def render_common_sidebar():
    """Render identical ProcureX sidebar across every single page."""
    st.sidebar.markdown(
        """
        <div style='text-align: center; margin-bottom: 20px; padding-top: 10px;'>
            <h1 style='margin-bottom: 4px; font-size: 2rem;'><span class="gradient-text">ProcureX</span></h1>
            <p style='color: #94a3b8; font-size: 0.85rem; font-weight: 500; margin-top:0;'>Autonomous B2B Procurement Agent</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("### Navigation")
    
    pages = [
        ("App Home", "app.py"),
        ("Requirement Input", "pages/1_Requirement_Input.py"),
        ("Live Screening Status", "pages/2_Live_Screening_Status.py"),
        ("Discovered Suppliers", "pages/3_Discovered_Suppliers.py"),
        ("Evidence Browser", "pages/4_Evidence_Browser.py"),
        ("Economic Trace & Quota Tracker", "pages/5_Economic_Trace.py"),
    ]
    
    for title, path in pages:
        if st.sidebar.button(title, key=f"nav_{path}", use_container_width=True):
            st.switch_page(path)

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='font-size:0.85rem; color:#94a3b8; text-align:center; font-weight:600;'>
            An APEX Creation
        </div>
        """,
        unsafe_allow_html=True
    )

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
    render_common_sidebar()
    
    # Hero Section
    st.markdown("""
        <div style="text-align: center; max-width: 900px; margin: 0 auto 2.5rem auto;">
            <h1 style="font-size: 2.8rem; line-height: 1.2; margin-bottom: 1rem;">
                Autonomous B2B Procurement <br><span class="gradient-text">Research & Intelligence Engine</span>
            </h1>
            <p style="font-size: 1.15rem; color: #94a3b8; line-height: 1.6;">
                ProcureX transforms natural language procurement requests into verified, multi-supplier recommendations. 
                Powered by autonomous live web search, supplier matching, and economic micro-query data verification.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Core Purpose & Capabilities Section
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div class="step-badge">Platform Purpose</div>
            <h3 style="margin-top: 4px;">What ProcureX Solves</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
                B2B procurement in commercial markets is fragmented. 
                ProcureX acts as an <strong>autonomous AI agent</strong> that discovers suppliers across web registries, 
                extracts real product specifications, normalizes pricing, and ranks candidates objectively.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div class="step-badge">Engine Architecture</div>
            <h3 style="margin-top: 4px;">Core Capabilities</h3>
            <ul style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.8; padding-left: 1.2rem; margin-bottom: 0;">
                <li><strong>Natural Language Parsing:</strong> Extracts category, material, quantity, budget, and destination.</li>
                <li><strong>Live Web Screening:</strong> Autonomous real-time search across live web indices.</li>
                <li><strong>Candidate Ranking:</strong> Supplier matching based on available price and MOQ data.</li>
                <li><strong>x402 Micropayment Protocol:</strong> Automated info-buying with real-time USD/INR FX conversion.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<h2 style='text-align: center; margin: 2.5rem 0 1.5rem 0;'>How To Use <span class='gradient-text'>ProcureX</span></h2>", unsafe_allow_html=True)
    
    # 3-Step Interactive Workflow Guide
    s1, s2, s3 = st.columns(3)
    
    with s1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div class="step-badge">Step 1</div>
            <h4>Requirement Input</h4>
            <p style="color: #94a3b8; font-size: 0.85rem;">Enter your exact procurement request in simple English (e.g. 5,000 nitrile gloves under ₹80/pc).</p>
        </div>
        """, unsafe_allow_html=True)
        
    with s2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div class="step-badge">Step 2</div>
            <h4>Live Screening</h4>
            <p style="color: #94a3b8; font-size: 0.85rem;">The AI agent searches live web indices. <strong>Please wait at least 30s–1min for live screening to generate results.</strong></p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div class="step-badge">Step 3</div>
            <h4>Supplier Evaluation</h4>
            <p style="color: #94a3b8; font-size: 0.85rem;">Review discovered suppliers, inspect direct website links, and check unit price and MOQ information.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        if st.button("Start Procurement Research Session", type="primary", use_container_width=True):
            st.switch_page("pages/1_Requirement_Input.py")

if __name__ == "__main__":
    main()
