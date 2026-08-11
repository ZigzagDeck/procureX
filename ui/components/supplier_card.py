"""Reusable component to display a Supplier with score as a styled card."""

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
        "unknown": "❓ Unknown",
    }
    return badges.get(supplier_type, "❓ Unknown")


def render_supplier_card(supplier, score=None, rank=None) -> None:
    """Render a supplier as a styled card with ranking and score."""
    rank_display = f"#{rank}" if rank else ""
    score_val = score.total_score if score else 0
    confidence = score.confidence if score else 0

    conf_color = _confidence_color(confidence)

    st.markdown(
        f"""<div style="background: rgba(19,24,54,0.9); border: 1px solid rgba(59,130,246,0.2);
        border-radius: 12px; padding: 1.2rem; margin: 0.5rem 0;
        backdrop-filter: blur(10px);">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:0.8rem;">
            <span style="background:linear-gradient(135deg,#3b82f6,#06b6d4); padding:4px 12px;
            border-radius:20px; font-weight:700; font-size:0.9rem;">{rank_display}</span>
            <span style="font-size:1.15rem; font-weight:600;">{supplier.name}</span>
            <span style="background:rgba(59,130,246,0.15); padding:2px 10px;
            border-radius:12px; font-size:0.8rem;">{_type_badge(supplier.supplier_type.value if hasattr(supplier.supplier_type, 'value') else str(supplier.supplier_type))}</span>
        </div></div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Score", f"{score_val:.1f}/100")
    with col2:
        st.metric("Confidence", f"{confidence*100:.0f}%")
    with col3:
        best_price = None
        if supplier.products:
            prices = [p.normalized_unit_price for p in supplier.products if p.normalized_unit_price]
            best_price = min(prices) if prices else None
        st.metric("Price/piece", f"₹{best_price:.1f}" if best_price else "N/A")
    with col4:
        moqs = [p.moq for p in supplier.products if p.moq] if supplier.products else []
        min_moq = min(moqs) if moqs else None
        st.metric("MOQ", f"{min_moq:,}" if min_moq else "N/A")

    if score and score.dimensions:
        with st.expander("📊 Score Breakdown"):
            for dim in score.dimensions:
                st.progress(
                    min(dim.raw_score, 1.0),
                    text=f"{dim.name}: {dim.weighted_score:.1f}/{dim.weight} — {dim.explanation}",
                )
