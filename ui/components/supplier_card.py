"""Clean, simple supplier candidate card component."""

import streamlit as st
from urllib.parse import urlparse


def render_supplier_card(supplier, score=None, rank=None) -> None:
    """Render a supplier cleanly as a rank-wise list item without score or product description clutter."""
    rank_display = f"#{rank}" if rank else ""

    # Determine site URL / domain
    web_url = supplier.website or (supplier.source_urls[0] if supplier.source_urls else None)
    site_domain = urlparse(web_url).netloc if web_url else "Web Directory"

    st.markdown(
        f"""<div class="glass-card" style="margin-bottom: 1rem; padding: 1.2rem;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom: 0.8rem;">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="background:linear-gradient(135deg,#38bdf8,#818cf8); padding:4px 14px;
                border-radius:20px; font-weight:700; font-size:0.9rem; color:white;">{rank_display}</span>
                <span style="font-size:1.2rem; font-weight:700; color:white;">{supplier.name}</span>
            </div>
            <div>
                {f'<a href="{web_url}" target="_blank" style="background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.3); color:#38bdf8; text-decoration:none; padding:4px 14px; border-radius:12px; font-size:0.85rem; font-weight:600;">🌐 {site_domain}</a>' if web_url else f'<span style="color:#94a3b8; font-size:0.85rem;">🌐 {site_domain}</span>'}
            </div>
        </div></div>""",
        unsafe_allow_html=True,
    )

    # Unit Price and MOQ only if available
    best_price = None
    min_moq = None
    if supplier.products:
        prices = [p.normalized_unit_price for p in supplier.products if p.normalized_unit_price]
        moqs = [p.moq for p in supplier.products if p.moq]
        best_price = min(prices) if prices else None
        min_moq = min(moqs) if moqs else None

    # Render metrics dynamically ONLY for available data
    available_cols = []
    if best_price is not None:
        available_cols.append(("Unit Price", f"₹{best_price:.1f}/pc"))
    if min_moq is not None:
        available_cols.append(("Minimum Order (MOQ)", f"{min_moq:,} units"))

    if available_cols:
        cols = st.columns(len(available_cols))
        for i, (label, val) in enumerate(available_cols):
            cols[i].metric(label, val)

    for product in supplier.products:
        if product.price_correction_note:
            st.info(f"Price correction: {product.price_correction_note}", icon="💳")
