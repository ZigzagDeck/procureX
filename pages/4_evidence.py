"""Evidence Browser — Source provenance and verification status for all supplier claims."""

import streamlit as st

st.set_page_config(page_title="ProcureX — Evidence", page_icon="🔗", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>🔗 Evidence <span class='gradient-text'>Browser</span></h1>", unsafe_allow_html=True)
st.markdown("*Source provenance and verification status for all supplier claims*")

session = st.session_state.get("research_session")

if not session or not getattr(session, "suppliers", None):
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem;">
        <h3>📭 No Evidence Available</h3>
        <p style="color:#94a3b8;">Complete a research session to view supplier evidence and provenance chains.</p>
        <p style="color:#64748b;">Navigate to <strong>Research</strong> to start.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

active_suppliers = [s for s in session.suppliers if s.is_duplicate_of is None]

if not active_suppliers:
    st.info("No active suppliers to display evidence for.")
    st.stop()

supplier_names = {s.name: s for s in active_suppliers}
selected_name = st.selectbox("🏢 Select Supplier", list(supplier_names.keys()))
supplier = supplier_names[selected_name]

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Type:** {supplier.supplier_type.value.title() if hasattr(supplier.supplier_type, 'value') else supplier.supplier_type}")
with col2:
    st.markdown(f"**GSTIN:** {supplier.gstin or 'Not available'}")
with col3:
    st.markdown(f"**Location:** {supplier.city or supplier.address or 'Unknown'}")

try:
    from ui.components.evidence_viewer import render_evidence_viewer
    if supplier.evidence:
        render_evidence_viewer(supplier.evidence)
    else:
        st.info("📭 No structured evidence graph available for this supplier.")
except Exception:
    st.warning("Evidence viewer component not available.")

if supplier.source_urls:
    st.markdown("### 🌐 Source URLs")
    for url in supplier.source_urls:
        st.markdown(f"- [{url}]({url})")

if supplier.claims:
    st.markdown("### 📢 Self-Reported Claims")
    for claim in supplier.claims:
        st.markdown(f"- 🟡 {claim} *(unverified)*")

if supplier.certifications:
    st.markdown("### 📜 Certifications")
    for cert in supplier.certifications:
        st.markdown(f"- {cert}")
