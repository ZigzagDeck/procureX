"""Clean, professional supplier card component for ProcureX."""

import streamlit as st


def _confidence_color(confidence: float) -> str:
    if confidence >= 0.8:
        return "#22c55e"  # green
    elif confidence >= 0.5:
        return "#eab308"  # yellow
    return "#ef4444"  # red


def _type_badge(supplier_type: str) -> str:
    badges = {
        "manufacturer": "🏭 Manufacturer",
        "distributor": "🔄 Distributor",
        "wholesaler": "📦 Wholesaler",
        "trader": "🔁 Trader",
        "unknown": "🏢 Supplier Entity",
    }
    return badges.get(supplier_type, "🏢 Supplier Entity")


def render_supplier_card(supplier, score=None, rank=None) -> None:
    """Render a supplier cleanly as a styled card with ranking and score."""
    rank_display = f"#{rank}" if rank else ""
    score_val = score.total_score if score else 0
    confidence = score.confidence if score else 0
    conf_color = _confidence_color(confidence)

    s_type = supplier.supplier_type.value if hasattr(supplier.supplier_type, "value") else str(supplier.supplier_type)

    st.markdown(
        f"""<div class="glass-card" style="margin-bottom: 1rem; padding: 1.2rem;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom: 1rem;">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="background:linear-gradient(135deg,#38bdf8,#818cf8); padding:4px 14px;
                border-radius:20px; font-weight:700; font-size:0.9rem; color:white;">{rank_display}</span>
                <span style="font-size:1.2rem; font-weight:700; color:white;">{supplier.name}</span>
                <span style="background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.25); color:#38bdf8; padding:3px 12px;
                border-radius:12px; font-size:0.8rem; font-weight:600;">{_type_badge(s_type)}</span>
            </div>
            <div>
                <span style="color:#94a3b8; font-size:0.85rem; margin-right:6px;">Match Score</span>
                <span style="font-size:1.3rem; font-weight:800; color:#38bdf8;">{score_val:.1f}</span>
                <span style="color:#64748b; font-size:0.9rem;">/100</span>
            </div>
        </div></div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{score_val:.1f}/100")
    with col2:
        st.metric("Confidence", f"{confidence*100:.0f}%")
    with col3:
        best_price = None
        if supplier.products:
            prices = [p.normalized_unit_price for p in supplier.products if p.normalized_unit_price]
            best_price = min(prices) if prices else None
        st.metric("Unit Price", f"₹{best_price:.1f}/pc" if best_price else "N/A")
    with col4:
        moqs = [p.moq for p in supplier.products if p.moq] if supplier.products else []
        min_moq = min(moqs) if moqs else None
        st.metric("Minimum Order (MOQ)", f"{min_moq:,} units" if min_moq else "N/A")

    if score and score.dimensions:
        with st.expander("📊 View Multi-Dimension Scoring Breakdown"):
            for dim in score.dimensions:
                st.progress(
                    min(dim.raw_score, 1.0),
                    text=f"{dim.name}: {dim.weighted_score:.1f}/{dim.weight} — {dim.explanation if dim.explanation else 'Evaluated against requirement criteria'}",
                )
