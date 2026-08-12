"""Final Recommendation Report — Evidence-backed procurement summary."""

import streamlit as st
from datetime import datetime, timezone

st.set_page_config(page_title="ProcureX — Final Report", page_icon="📋", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>📋 Final Recommendation <span class='gradient-text'>Report</span></h1>", unsafe_allow_html=True)
st.markdown("*Evidence-backed procurement recommendation with complete audit transparency.*")

session = st.session_state.get("research_session")

if not session or not getattr(session, "scores", None) or not session.scores:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem;">
        <h3>📭 Report Not Ready</h3>
        <p style="color:#94a3b8;">Complete a full research session to generate the procurement recommendation report.</p>
        <p style="color:#64748b;">Navigate to <strong>1. Requirement Input</strong> to begin.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

ranked = session.get_ranked_suppliers()

if not ranked:
    st.warning("No ranked suppliers available for report generation.")
    st.stop()

# Executive Summary
st.markdown("### 📊 Executive Summary")
requirement = session.requirement

st.markdown(f"""
<div class="glass-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
        <span style="color:#94a3b8; font-size:0.85rem;">Session Generated: {session.created_at.strftime('%B %d, %Y %H:%M UTC') if session.created_at else 'N/A'}</span>
        <span style="background:rgba(56,189,248,0.15); color:#38bdf8; padding:3px 12px; border-radius:12px; font-size:0.8rem; font-weight:600;">
            Mode: {requirement.procurement_mode.value.replace('_', ' ').title() if requirement else 'Balanced'}
        </span>
    </div>
    <p style="font-size:1.05rem; margin-bottom:1rem;"><strong style="color:white;">Requirement Prompt:</strong> "{requirement.raw_query if requirement else 'N/A'}"</p>
    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px;">
        <div><span style="color:#94a3b8; font-size:0.85rem;">Suppliers Evaluated</span><br><strong style="font-size:1.2rem; color:white;">{len(session.suppliers)}</strong></div>
        <div><span style="color:#94a3b8; font-size:0.85rem;">Unique Candidates</span><br><strong style="font-size:1.2rem; color:white;">{len(ranked)}</strong></div>
        <div><span style="color:#94a3b8; font-size:0.85rem;">Sources Consulted</span><br><strong style="font-size:1.2rem; color:white;">{len(session.sources_consulted)}</strong></div>
        <div><span style="color:#94a3b8; font-size:0.85rem;">Research Cost</span><br><strong style="font-size:1.2rem; color:#38bdf8;">${session.budget.total_spent:.3f} USD</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Recommendation
st.markdown("### 🏆 Primary Supplier Recommendation")
top_supplier, top_score = ranked[0]

best_price = None
best_moq = None
if top_supplier.products:
    prices = [p.normalized_unit_price for p in top_supplier.products if p.normalized_unit_price]
    moqs = [p.moq for p in top_supplier.products if p.moq]
    best_price = min(prices) if prices else None
    best_moq = min(moqs) if moqs else None

conf_color = "#22c55e" if top_score.confidence >= 0.8 else "#eab308" if top_score.confidence >= 0.5 else "#ef4444"
s_type = top_supplier.supplier_type.value if hasattr(top_supplier.supplier_type, "value") else str(top_supplier.supplier_type)

st.markdown(f"""
<div class="glass-card" style="background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(129,140,248,0.08)); border: 1px solid rgba(56,189,248,0.3);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <h3 style="margin:0; font-size:1.4rem;">🥇 {top_supplier.name}</h3>
        <span style="background:#0284c7; color:white; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.85rem;">Top Candidate</span>
    </div>
    <div style="display:flex; gap:2rem; flex-wrap:wrap; margin-top:8px;">
        <div><span style="color:#94a3b8; font-size:0.85rem;">Match Score</span><br><strong style="font-size:1.6rem; color:#38bdf8;">{top_score.total_score:.1f}</strong><span style="color:#64748b;">/100</span></div>
        <div><span style="color:#94a3b8; font-size:0.85rem;">Confidence Level</span><br><strong style="font-size:1.6rem; color:{conf_color};">{top_score.confidence*100:.0f}%</strong></div>
        <div><span style="color:#94a3b8; font-size:0.85rem;">Unit Price</span><br><strong style="font-size:1.6rem; color:white;">{'₹' + f'{best_price:.1f}' if best_price else 'N/A'}</strong></div>
        <div><span style="color:#94a3b8; font-size:0.85rem;">MOQ</span><br><strong style="font-size:1.6rem; color:white;">{f'{best_moq:,} pcs' if best_moq else 'N/A'}</strong></div>
        <div><span style="color:#94a3b8; font-size:0.85rem;">Entity Type</span><br><strong style="font-size:1.2rem; color:white;">{s_type.title()}</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)

if top_score.dimensions:
    with st.expander("📊 View Top Recommendation Dimension Breakdown"):
        for dim in top_score.dimensions:
            st.progress(min(dim.raw_score, 1.0), text=f"{dim.name}: {dim.weighted_score:.1f}/{dim.weight}")

if len(ranked) > 1:
    st.markdown("### 🔄 Alternative Options Benchmark")
    for i, (supplier, score) in enumerate(ranked[1:], start=2):
        price = None
        moq = None
        if supplier.products:
            prices = [p.normalized_unit_price for p in supplier.products if p.normalized_unit_price]
            moqs = [p.moq for p in supplier.products if p.moq]
            price = min(prices) if prices else None
            moq = min(moqs) if moqs else None

        conf_c = "#22c55e" if score.confidence >= 0.8 else "#eab308" if score.confidence >= 0.5 else "#ef4444"
        alt_type = supplier.supplier_type.value if hasattr(supplier.supplier_type, "value") else str(supplier.supplier_type)

        st.markdown(f"""
        <div class="glass-card" style="padding: 1rem 1.2rem; margin-bottom: 0.8rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0;">#{i} {supplier.name}</h4>
                <div>
                    <span style="color:#94a3b8; font-size:0.85rem;">Score:</span> <strong style="color:#38bdf8;">{score.total_score:.1f}/100</strong> &bull;
                    <span style="color:#94a3b8; font-size:0.85rem;">Confidence:</span> <strong style="color:{conf_c};">{score.confidence*100:.0f}%</strong>
                </div>
            </div>
            <div style="margin-top:6px; font-size:0.9rem; color:#cbd5e1;">
                Unit Price: <strong>{'₹' + f'{price:.1f}' if price else 'N/A'}</strong> &bull;
                MOQ: <strong>{f'{moq:,} pcs' if moq else 'N/A'}</strong> &bull;
                Type: <strong>{alt_type.title()}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

report_text = f"""# ProcureX Autonomous Procurement Recommendation Report
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

## Requirement Prompt
{requirement.raw_query if requirement else 'N/A'}

## Primary Recommendation
{top_supplier.name}
- Match Score: {top_score.total_score:.1f}/100
- Confidence Level: {top_score.confidence*100:.0f}%
- Unit Price: {'₹' + f'{best_price:.1f}' if best_price else 'N/A'}
- Minimum Order Quantity: {f'{best_moq:,}' if best_moq else 'N/A'}
- Entity Type: {s_type.title()}

## Alternatives
"""
for i, (s, sc) in enumerate(ranked[1:], start=2):
    report_text += f"\n#{i} {s.name} — Score: {sc.total_score:.1f}/100, Confidence: {sc.confidence*100:.0f}%"

report_text += f"""

## Research Audit Summary
- Initial Budget Allocated: ${session.budget.initial_budget:.3f} USD
- Micro-Query Cost Spent: ${session.budget.total_spent:.3f} USD
- Remaining Session Balance: ${session.budget.remaining_budget:.3f} USD

---
Generated by ProcureX Autonomous B2B Procurement Intelligence Agent
"""

st.download_button(
    label="📥 Download Executive Procurement Report (.md)",
    data=report_text,
    file_name=f"procurex_recommendation_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')}.md",
    mime="text/markdown",
    use_container_width=True
)
