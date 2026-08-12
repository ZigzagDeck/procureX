"""Quota Expense Tracker & Budget Component for ProcureX."""

import streamlit as st
from x402.fx_engine import FXEngine
from x402.account import PrepaidUSDAccount


def render_budget_tracker(budget) -> None:
    """Render research budget with quota tracker, progress bar, account balance, and transactions."""
    fx_engine = FXEngine()
    account = PrepaidUSDAccount()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Initial Session Budget", fx_engine.format_dual(budget.initial_budget))
    with col2:
        st.metric("💸 Micro-Queries Spent", fx_engine.format_dual(budget.total_spent))
    with col3:
        st.metric("💰 Remaining Budget", fx_engine.format_dual(budget.remaining_budget))
    with col4:
        st.metric("💳 Account Balance", fx_engine.format_dual(account.get_balance()))

    usage_pct = (budget.total_spent / budget.initial_budget) if budget.initial_budget > 0 else 0
    st.progress(min(usage_pct, 1.0), text=f"Session Budget Used: {usage_pct * 100:.1f}%")

    if usage_pct >= 0.8:
        st.warning("⚠️ **Budget Warning:** Over 80% of allocated session research budget has been spent on micro-queries.")

    # Decisions timeline
    if budget.decisions:
        st.markdown("### 🧠 Payment Decisions Ledger")
        for decision in budget.decisions:
            icon = "✅" if decision.should_purchase else "⏭️"
            service = decision.service_type.value.replace("_", " ").title()
            dual_cost = fx_engine.format_dual(decision.cost)
            st.markdown(
                f"""<div class="glass-card" style="padding: 0.8rem 1.2rem; margin-bottom: 0.5rem;">
                {icon} <strong>{service}</strong> for <em>{decision.supplier_name or decision.supplier_id}</em> 
                — <strong>{'Purchased' if decision.should_purchase else 'Skipped'}</strong> ({dual_cost})<br>
                <span style="color:#94a3b8; font-size:0.85rem;">Reason: {decision.reason}</span>
                </div>""",
                unsafe_allow_html=True
            )

    # Transaction details
    if budget.transactions:
        st.markdown("### 💳 Cryptographic Transaction Audit Log")
        for tx in budget.transactions:
            status = tx.status.value if hasattr(tx.status, "value") else str(tx.status)
            status_icon = "✅" if status == "completed" else "❌" if status == "failed" else "⏳"
            service = tx.service_type.value.replace("_", " ").title()
            dual_amount = fx_engine.format_dual(tx.amount)
            st.markdown(
                f"""<div class="glass-card" style="padding: 0.8rem 1.2rem; margin-bottom: 0.5rem; border-left: 3px solid {'#22c55e' if status == 'completed' else '#ef4444'};">
                {status_icon} <strong>{service}</strong> — {dual_amount} — Status: <strong>{status.title()}</strong><br>
                {f'<span style="color:#94a3b8; font-size:0.85rem;">Response Payload: {tx.response_summary}</span>' if tx.response_summary else ''}
                </div>""",
                unsafe_allow_html=True
            )
