"""Reusable component to display a parsed ProcurementRequirement as a styled card."""

import streamlit as st


def render_requirement_card(requirement) -> None:
    """Render a procurement requirement as a professional styled card."""
    st.markdown(
        """<div style="background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.25);
        border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">""",
        unsafe_allow_html=True,
    )
    st.markdown("### 📝 Structured Requirement")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"**🏭 Product:** {requirement.product_category}")
        st.markdown(f"**🧪 Material:** {requirement.material}")
        st.markdown(f"**🛡️ Application:** {requirement.application}")
        if requirement.size:
            st.markdown(f"**📏 Size:** {requirement.size}")

    with col2:
        st.markdown(f"**📦 Quantity:** {requirement.quantity:,}")
        if requirement.maximum_unit_price:
            st.markdown(f"**💰 Max Price:** ₹{requirement.maximum_unit_price}/piece")
        st.markdown(f"**💱 Currency:** {requirement.currency}")

    with col3:
        st.markdown(f"**📍 Destination:** {requirement.destination}")
        if requirement.delivery_deadline:
            st.markdown(f"**📅 Deadline:** {requirement.delivery_deadline}")
        mode_display = requirement.procurement_mode.value.replace("_", " ").title()
        st.markdown(f"**⚙️ Mode:** {mode_display}")
        if requirement.preferred_supplier_type:
            st.markdown(f"**🏢 Preferred:** {requirement.preferred_supplier_type.title()}")

    if requirement.certification_requirements:
        st.markdown(f"**📜 Certifications:** {', '.join(requirement.certification_requirements)}")

    st.markdown("</div>", unsafe_allow_html=True)
