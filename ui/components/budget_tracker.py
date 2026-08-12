"""Reusable component to display research budget status with progress bar."""

import streamlit as st
from x402.fx_engine import FXEngine
from x402.account import PrepaidUSDAccount


def render_budget_tracker(budget) -> None:
    """Render research budget with progress bar, account balance, and transaction list."""
    fx_engine = FXEngine()
    account = PrepaidUSDAccount()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Initial Budget", fx_engine.format_dual(budget.initial_budget))
    with col2:
        st.metric("💸 Spent", fx_engine.format_dual(budget.total_spent))
    with col3:
        st.metric("💰 Remaining", fx_engine.format_dual(budget.remaining_budget))
    with col4:
        st.metric("💳 Account Balance", fx_engine.format_dual(account.get_balance()))

    usage_pct = (budget.total_spent / budget.initial_budget) if budget.initial_budget > 0 else 0
    st.progress(min(usage_pct, 1.0), text=f"Budget used: {usage_pct * 100:.1f}%")

    # Decisions timeline
    if budget.decisions:
        st.markdown("### 🧠 Payment Decisions")
        for decision in budget.decisions:
            icon = "✅" if decision.should_purchase else "⏭️"
            service = decision.service_type.value.replace("_", " ").title()
            dual_cost = fx_engine.format_dual(decision.cost)
            st.markdown(
                f"{icon} **{service}** for *{decision.supplier_name or decision.supplier_id}* "
                f"— {'Purchased' if decision.should_purchase else 'Skipped'} "
                f"({dual_cost}) — {decision.reason}"
            )

    # Transaction details
    if budget.transactions:
        st.markdown("### 💳 Transactions")
        for tx in budget.transactions:
            status = tx.status.value if hasattr(tx.status, "value") else str(tx.status)
            status_icon = "✅" if status == "completed" else "❌" if status == "failed" else "⏳"
            service = tx.service_type.value.replace("_", " ").title()
            dual_amount = fx_engine.format_dual(tx.amount)
            st.markdown(
                f"{status_icon} **{service}** — {dual_amount} — Status: {status}"
            )
            if tx.response_summary:
                st.caption(f"Response: {tx.response_summary}")
            if tx.error_message:
                st.error(f"Error: {tx.error_message}")
