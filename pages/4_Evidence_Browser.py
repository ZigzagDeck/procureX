"""Evidence Browser — Source provenance and web verification status."""

import streamlit as st

st.set_page_config(page_title="ProcureX — Evidence Browser", layout="wide")

try:
    from app import apply_custom_css, init_session_state, render_common_sidebar
    apply_custom_css()
    init_session_state()
    render_common_sidebar()
except Exception:
    pass

st.markdown("<h1>Evidence <span class='gradient-text'>Browser</span></h1>", unsafe_allow_html=True)
st.markdown("*Source provenance and verification status for all B2B supplier claims.*")

session = st.session_state.get("research_session")

if not session or not getattr(session, "suppliers", None) or not session.suppliers:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem;">
        <h3>📭 No Evidence Available</h3>
        <p style="color:#94a3b8;">Complete a research session to view supplier evidence and provenance chains.</p>
        <p style="color:#64748b;">Navigate to <strong>Requirement Input</strong> to begin.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Filter active (non-duplicate) suppliers
active_suppliers = [s for s in session.suppliers if s.is_duplicate_of is None]

if not active_suppliers:
    st.info("No active suppliers to display evidence for.")
    st.stop()

# Supplier selector
supplier_names = {s.name: s for s in active_suppliers}
selected_name = st.selectbox("🏢 Select Supplier Candidate:", list(supplier_names.keys()))
supplier = supplier_names[selected_name]

st.markdown("---")

# Supplier Overview Grid
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Type:** {supplier.supplier_type.value.title() if hasattr(supplier.supplier_type, 'value') else supplier.supplier_type}")
with col2:
    st.markdown(f"**GSTIN:** `{supplier.gstin or 'Not available'}`")
with col3:
    st.markdown(f"**Location:** {supplier.city or supplier.address or 'Unknown'}")

st.markdown("<br>", unsafe_allow_html=True)

# Render evidence graph using the components library
try:
    from ui.components.evidence_viewer import render_evidence_viewer
    if supplier.evidence:
        render_evidence_viewer(supplier.evidence)
    else:
        st.info("📭 No structured evidence graph available for this supplier.")
except ImportError:
    st.warning("Evidence viewer component not available.")

# Source URLs registry for transparency
if supplier.source_urls:
    st.markdown("### 🌐 Discovered Source Links")
    for url in supplier.source_urls:
        st.markdown(f"- [{url}]({url})")
