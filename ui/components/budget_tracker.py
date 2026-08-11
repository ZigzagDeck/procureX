"""Reusable component to display research budget status with progress bar."""

import streamlit as st


def render_budget_tracker(budget) -> None:
    """Render research budget with progress bar and transaction list."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Initial Budget", f"${budget.initial_budget:.3f}")
    with col2:
        st.metric("💸 Spent", f"${budget.total_spent:.3f}")
    with col3:
        st.metric("💰 Remaining", f"${budget.remaining_budget:.3f}")

    usage_pct = (budget.total_spent / budget.initial_budget) if budget.initial_budget > 0 else 0
    st.progress(min(usage_pct, 1.0), text=f"Budget used: {usage_pct * 100:.1f}%")

    # Decisions timeline
    if budget.decisions:
        st.markdown("### 🧠 Payment Decisions")
        for decision in budget.decisions:
            icon = "✅" if decision.should_purchase else "⏭️"
            service = decision.service_type.value.replace("_", " ").title()
            st.markdown(
                f"{icon} **{service}** for *{decision.supplier_name or decision.supplier_id}* "
                f"— {'Purchased' if decision.should_purchase else 'Skipped'} "
                f"(${decision.cost:.3f}) — {decision.reason}"
            )

    # Transaction details
    if budget.transactions:
        st.markdown("### 💳 Transactions")
        for tx in budget.transactions:
            status = tx.status.value if hasattr(tx.status, "value") else str(tx.status)
            status_icon = "✅" if status == "completed" else "❌" if status == "failed" else "⏳"
            service = tx.service_type.value.replace("_", " ").title()
            st.markdown(
                f"{status_icon} **{service}** — ${tx.amount:.3f} — Status: {status}"
            )
            if tx.response_summary:
                st.caption(f"Response: {tx.response_summary}")
            if tx.error_message:
                st.error(f"Error: {tx.error_message}")
