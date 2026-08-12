"""Discovered Suppliers Page — Clean B2B supplier candidate list."""

import streamlit as st

st.set_page_config(page_title="ProcureX — Discovered Suppliers", layout="wide")

try:
    from app import apply_custom_css, init_session_state, render_common_sidebar
    apply_custom_css()
    init_session_state()
    render_common_sidebar()
except Exception:
    pass

st.markdown("<h1>Discovered <span class='gradient-text'>Suppliers</span></h1>", unsafe_allow_html=True)
st.markdown("*Autonomous discovery and entity deduplication across live web sources.*")

session = st.session_state.get("research_session")

if not session or not session.suppliers:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem;">
        <h3>No Suppliers Discovered Yet</h3>
        <p style="color:#94a3b8;">Start a research session to discover and verify suppliers.</p>
        <p style="color:#64748b;">Navigate to <strong>Requirement Input</strong> to begin.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

ranked_pairs = session.get_ranked_suppliers()

if not ranked_pairs:
    st.warning("No candidate suppliers found.")
    st.stop()

st.markdown(f"### Candidate Suppliers ({len(ranked_pairs)} Unique Entities)")

try:
    from ui.components.supplier_card import render_supplier_card
    for rank, (supplier, score) in enumerate(ranked_pairs, start=1):
        render_supplier_card(supplier, rank=rank)
except Exception as e:
    for rank, (supplier, score) in enumerate(ranked_pairs, start=1):
        st.markdown(f"#### #{rank} {supplier.name}")
