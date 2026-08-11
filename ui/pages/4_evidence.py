"""Evidence Browser — Source provenance and verification status for all supplier claims."""

import streamlit as st

st.set_page_config(page_title="ProcureX — Evidence", page_icon="🔗", layout="wide")

# --- CSS (consistent with app.py) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0a0e27; }
.glass-card {
    background: rgba(255,255,255,0.05); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1); border-radius: 12px;
    padding: 24px; margin-bottom: 24px;
}
.gradient-text {
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔗 Evidence Browser")
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

# Filter active (non-duplicate) suppliers
active_suppliers = [s for s in session.suppliers if s.is_duplicate_of is None]

if not active_suppliers:
    st.info("No active suppliers to display evidence for.")
    st.stop()

supplier_names = {s.name: s for s in active_suppliers}
selected_name = st.selectbox("🏢 Select Supplier", list(supplier_names.keys()))
supplier = supplier_names[selected_name]

st.markdown("---")

# Supplier overview
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Type:** {supplier.supplier_type.value.title() if hasattr(supplier.supplier_type, 'value') else supplier.supplier_type}")
with col2:
    st.markdown(f"**GSTIN:** {supplier.gstin or 'Not available'}")
with col3:
    st.markdown(f"**Location:** {supplier.city or supplier.address or 'Unknown'}")

# Evidence graph
try:
    from ui.components.evidence_viewer import render_evidence_viewer
    if supplier.evidence:
        render_evidence_viewer(supplier.evidence)
    else:
        st.info("📭 No structured evidence graph available for this supplier.")
except ImportError:
    st.warning("Evidence viewer component not available.")

# Source URLs
if supplier.source_urls:
    st.markdown("### 🌐 Source URLs")
    for url in supplier.source_urls:
        st.markdown(f"- [{url}]({url})")

# Self-reported claims
if supplier.claims:
    st.markdown("### 📢 Self-Reported Claims")
    for claim in supplier.claims:
        st.markdown(f"- 🟡 {claim} *(unverified)*")

# Certifications
if supplier.certifications:
    st.markdown("### 📜 Certifications")
    for cert in supplier.certifications:
        st.markdown(f"- {cert}")
