"""Final Report — Evidence-backed procurement recommendation with full transparency."""

import streamlit as st
from datetime import datetime, timezone

st.set_page_config(page_title="ProcureX — Final Report", page_icon="📋", layout="wide")

# --- CSS ---
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
.recommendation-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(6,182,212,0.1));
    border: 1px solid rgba(59,130,246,0.3); border-radius: 12px;
    padding: 24px; margin: 16px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 📋 Final Procurement Report")
st.markdown("*Evidence-backed procurement recommendation with full transparency*")

session = st.session_state.get("research_session")

if not session or not getattr(session, "scores", None) or not session.scores:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem;">
        <h3>📭 Report Not Ready</h3>
        <p style="color:#94a3b8;">Complete a full research session to generate the procurement report.</p>
        <p style="color:#64748b;">Navigate to <strong>Research</strong> to begin.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Get ranked suppliers
ranked = session.get_ranked_suppliers()

if not ranked:
    st.warning("No ranked suppliers available for report generation.")
    st.stop()

# --- Executive Summary ---
st.markdown("## 📊 Executive Summary")
requirement = session.requirement

st.markdown(f"""
<div class="glass-card">
    <p style="color:#94a3b8; font-size:0.9rem;">Research conducted on {session.created_at.strftime('%B %d, %Y') if session.created_at else 'N/A'}</p>
    <p><strong>Requirement:</strong> {requirement.raw_query if requirement else 'N/A'}</p>
    <p><strong>Suppliers Discovered:</strong> {len(session.suppliers)} &bull;
    <strong>After Deduplication:</strong> {len([s for s in session.suppliers if s.is_duplicate_of is None])} &bull;
    <strong>Ranked:</strong> {len(ranked)}</p>
    <p><strong>Sources Consulted:</strong> {len(session.sources_consulted)}</p>
    <p><strong>Research Budget:</strong> ${session.budget.initial_budget:.3f} &bull;
    <strong>Spent:</strong> ${session.budget.total_spent:.3f} &bull;
    <strong>Remaining:</strong> ${session.budget.remaining_budget:.3f}</p>
</div>
""", unsafe_allow_html=True)

# --- Top Recommendation ---
st.markdown("## 🏆 Top Recommendation")
top_supplier, top_score = ranked[0]

best_price = None
best_moq = None
if top_supplier.products:
    prices = [p.normalized_unit_price for p in top_supplier.products if p.normalized_unit_price]
    moqs = [p.moq for p in top_supplier.products if p.moq]
    best_price = min(prices) if prices else None
    best_moq = min(moqs) if moqs else None

conf_color = "#22c55e" if top_score.confidence >= 0.8 else "#eab308" if top_score.confidence >= 0.5 else "#ef4444"

st.markdown(f"""
<div class="recommendation-card">
    <h3 style="margin-top:0;">🥇 {top_supplier.name}</h3>
    <div style="display:flex; gap:2rem; flex-wrap:wrap;">
        <div><span style="color:#94a3b8;">Score</span><br><strong style="font-size:1.5rem;">{top_score.total_score:.1f}</strong>/100</div>
        <div><span style="color:#94a3b8;">Confidence</span><br><strong style="font-size:1.5rem; color:{conf_color};">{top_score.confidence*100:.0f}%</strong></div>
        <div><span style="color:#94a3b8;">Price/piece</span><br><strong style="font-size:1.5rem;">{'₹' + f'{best_price:.1f}' if best_price else 'N/A'}</strong></div>
        <div><span style="color:#94a3b8;">MOQ</span><br><strong style="font-size:1.5rem;">{f'{best_moq:,}' if best_moq else 'N/A'}</strong></div>
        <div><span style="color:#94a3b8;">Type</span><br><strong>{top_supplier.supplier_type.value.title() if hasattr(top_supplier.supplier_type, 'value') else top_supplier.supplier_type}</strong></div>
        <div><span style="color:#94a3b8;">Location</span><br><strong>{top_supplier.city or top_supplier.state or 'Unknown'}</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Score breakdown for top supplier
if top_score.dimensions:
    with st.expander("📊 Score Breakdown for Top Recommendation"):
        for dim in top_score.dimensions:
            st.progress(min(dim.raw_score, 1.0), text=f"{dim.name}: {dim.weighted_score:.1f}/{dim.weight}")

# --- Alternatives ---
if len(ranked) > 1:
    st.markdown("## 🔄 Alternatives")
    for i, (supplier, score) in enumerate(ranked[1:], start=2):
        price = None
        moq = None
        if supplier.products:
            prices = [p.normalized_unit_price for p in supplier.products if p.normalized_unit_price]
            moqs = [p.moq for p in supplier.products if p.moq]
            price = min(prices) if prices else None
            moq = min(moqs) if moqs else None

        conf_c = "#22c55e" if score.confidence >= 0.8 else "#eab308" if score.confidence >= 0.5 else "#ef4444"

        st.markdown(f"""
        <div class="glass-card">
            <h4>#{i} {supplier.name}</h4>
            <span style="color:#94a3b8;">Score:</span> <strong>{score.total_score:.1f}/100</strong> &bull;
            <span style="color:#94a3b8;">Confidence:</span> <strong style="color:{conf_c};">{score.confidence*100:.0f}%</strong> &bull;
            <span style="color:#94a3b8;">Price:</span> <strong>{'₹' + f'{price:.1f}' if price else 'N/A'}</strong> &bull;
            <span style="color:#94a3b8;">MOQ:</span> <strong>{f'{moq:,}' if moq else 'N/A'}</strong> &bull;
            <span style="color:#94a3b8;">Type:</span> {supplier.supplier_type.value.title() if hasattr(supplier.supplier_type, 'value') else supplier.supplier_type} &bull;
            <span style="color:#94a3b8;">Location:</span> {supplier.city or 'Unknown'}
        </div>
        """, unsafe_allow_html=True)

# --- Uncertainties & Information Gaps ---
st.markdown("## ⚠️ Uncertainties & Information Gaps")
uncertainties = []

for supplier, score in ranked:
    if score.confidence < 0.5:
        uncertainties.append(f"**{supplier.name}**: Low confidence ({score.confidence*100:.0f}%) — insufficient evidence")
    if supplier.supplier_type_evidence.value in ("unknown", "claimed") if hasattr(supplier.supplier_type_evidence, "value") else True:
        uncertainties.append(f"**{supplier.name}**: Supplier type is {supplier.supplier_type_evidence.value if hasattr(supplier.supplier_type_evidence, 'value') else 'unverified'}")
    if not supplier.gstin:
        uncertainties.append(f"**{supplier.name}**: GSTIN not available — business identity unverified")
    if supplier.evidence and supplier.evidence.contradictions:
        for c in supplier.evidence.contradictions:
            uncertainties.append(f"**{supplier.name}**: Contradiction in {c.field_name} — {c.description}")

if uncertainties:
    for u in uncertainties:
        st.markdown(f"- ⚠️ {u}")
else:
    st.success("No major uncertainties detected.")

# --- Download Report ---
st.markdown("---")
report_text = f"""# ProcureX Procurement Report
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

## Requirement
{requirement.raw_query if requirement else 'N/A'}

## Top Recommendation
{top_supplier.name}
- Score: {top_score.total_score:.1f}/100
- Confidence: {top_score.confidence*100:.0f}%
- Price/piece: {'₹' + f'{best_price:.1f}' if best_price else 'N/A'}
- MOQ: {f'{best_moq:,}' if best_moq else 'N/A'}
- Type: {top_supplier.supplier_type.value.title() if hasattr(top_supplier.supplier_type, 'value') else top_supplier.supplier_type}
- Location: {top_supplier.city or 'Unknown'}

## Alternatives
"""
for i, (s, sc) in enumerate(ranked[1:], start=2):
    report_text += f"\n#{i} {s.name} — Score: {sc.total_score:.1f}, Confidence: {sc.confidence*100:.0f}%"

report_text += f"""

## Budget
- Initial: ${session.budget.initial_budget:.3f}
- Spent: ${session.budget.total_spent:.3f}
- Remaining: ${session.budget.remaining_budget:.3f}

## Disclaimer
This report is based on automated research and should be independently verified.
Route estimates do not represent supplier delivery commitments.
Evidence quality varies — check confidence scores and evidence status for each claim.
"""

st.download_button(
    label="📥 Download Report (Markdown)",
    data=report_text,
    file_name=f"procurex_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')}.md",
    mime="text/markdown",
)
