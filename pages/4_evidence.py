"""Evidence Browser — Source provenance and web verification status."""

import streamlit as st

st.set_page_config(page_title="ProcureX — Evidence Browser", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>Evidence <span class='gradient-text'>Browser</span></h1>", unsafe_allow_html=True)
st.markdown("*Source provenance and verification status for all supplier claims.*")

session = st.session_state.get("research_session")

if not session or not getattr(session, "suppliers", None):
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem;">
        <h3>No Evidence Available</h3>
        <p style="color:#94a3b8;">Complete a research session to view supplier evidence and web source provenance.</p>
        <p style="color:#64748b;">Navigate to <strong>Requirement Input</strong> to start.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

active_suppliers = [s for s in session.suppliers if getattr(s, "is_duplicate_of", None) is None]

if not active_suppliers:
    st.info("No active suppliers to display evidence for.")
    st.stop()

supplier_names = {s.name: s for s in active_suppliers}
selected_name = st.selectbox("Select Supplier Candidate:", list(supplier_names.keys()))
supplier = supplier_names[selected_name]

st.markdown("---")

# Supplier Summary Header (Entity Classification REMOVED)
st.markdown(f"""
<div class="glass-card" style="padding: 1rem 1.5rem; margin-bottom: 1.5rem;">
    <h3 style="margin: 0; color: white;">{supplier.name}</h3>
</div>
""", unsafe_allow_html=True)

try:
    from ui.components.evidence_viewer import render_evidence_viewer
    if supplier.evidence:
        render_evidence_viewer(supplier.evidence)
    else:
        st.info("No structured evidence graph recorded for this supplier.")
except Exception as e:
    st.warning("Evidence viewer unavailable.")

if supplier.source_urls:
    st.markdown("### Fetched Web Source URLs")
    for url in supplier.source_urls:
        st.markdown(f"- [{url}]({url})")
