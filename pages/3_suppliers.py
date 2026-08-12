"""Discovered Suppliers Page — Clean, elegant B2B supplier candidate list."""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="ProcureX — Discovered Suppliers", page_icon="🏭", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>🏭 Discovered <span class='gradient-text'>Suppliers</span></h1>", unsafe_allow_html=True)
st.markdown("*Autonomous discovery, entity deduplication, and multidimensional capability scoring.*")

session = st.session_state.get("research_session")

if not session or not session.suppliers:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem;">
        <h3>📭 No Suppliers Discovered Yet</h3>
        <p style="color:#94a3b8;">Start a research session to discover, verify, and score suppliers.</p>
        <p style="color:#64748b;">Navigate to <strong>1. Requirement Input</strong> to begin.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

ranked_pairs = session.get_ranked_suppliers()

if not ranked_pairs:
    st.warning("No scored suppliers found.")
    st.stop()

st.markdown(f"### 🎯 Ranked Suppliers ({len(ranked_pairs)} Unique Entities)")

try:
    from ui.components.supplier_card import render_supplier_card
    for rank, (supplier, score) in enumerate(ranked_pairs, start=1):
        render_supplier_card(supplier, score=score, rank=rank)
except Exception as e:
    for rank, (supplier, score) in enumerate(ranked_pairs, start=1):
        st.markdown(f"#### #{rank} {supplier.name} — Score: {score.total_score:.1f}/100")

st.markdown("---")
st.markdown("### 📊 Dimension Score Comparison Across Suppliers")

chart_data = {}
for supplier, score in ranked_pairs:
    dim_scores = {d.name: round(d.weighted_score, 1) for d in score.dimensions}
    chart_data[supplier.name] = dim_scores

df_chart = pd.DataFrame(chart_data).T
st.bar_chart(df_chart, use_container_width=True)
