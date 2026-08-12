"""Economic Trace — Research budget allocation and x402 payment decisions."""

import streamlit as st
from x402.fx_engine import FXEngine
from x402.account import PrepaidUSDAccount

st.set_page_config(page_title="ProcureX — Economic Trace", page_icon="💰", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>💰 Economic <span class='gradient-text'>Trace</span></h1>", unsafe_allow_html=True)
st.markdown("*Research budget allocation and x402 payment decisions*")

fx_engine = FXEngine()
account = PrepaidUSDAccount()
current_rate = fx_engine.get_rate()

st.info(f"ℹ️ **Live FX Exchange Rate:** 1 USD = ₹{current_rate:.2f} INR (auto-cached 1h)")

session = st.session_state.get("research_session")

if not session:
    col_bal, col_fx = st.columns(2)
    with col_bal:
        st.metric("💳 Account Balance", f"{fx_engine.format_dual(account.get_balance())}")
    with col_fx:
        st.metric("📈 Current FX Rate", f"₹{current_rate:.2f} / USD")

    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem; margin-top:1rem;">
        <h3>📭 No Research Session Active</h3>
        <p style="color:#94a3b8;">Start a research session to track budget and payment decisions.</p>
        <p style="color:#64748b;">Navigate to <strong>Research</strong> to begin.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

budget = session.budget

try:
    from ui.components.budget_tracker import render_budget_tracker
    render_budget_tracker(budget)
except Exception:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Initial Budget", fx_engine.format_dual(budget.initial_budget))
    with col2:
        st.metric("💸 Spent", fx_engine.format_dual(budget.total_spent))
    with col3:
        st.metric("💰 Remaining", fx_engine.format_dual(budget.remaining_budget))
    with col4:
        st.metric("💳 Account Balance", fx_engine.format_dual(account.get_balance()))

st.markdown("---")
st.markdown("### 🔐 x402 Payment Protocol")
st.markdown(f"""
<div class="glass-card">
    <p style="color:#94a3b8;">
    ProcureX uses the <strong>x402 protocol</strong> (HTTP 402 Payment Required) to autonomously 
    pay for specialized intelligence services in fiat USD. The agent evaluates whether the expected value of 
    information exceeds the cost before committing research budget.
    </p>
    <p style="color:#64748b; font-size:0.85rem;">
    Services: <strong>Price Intelligence</strong> ({fx_engine.format_dual(0.002)}) · <strong>Supplier Verification</strong> ({fx_engine.format_dual(0.001)})
    </p>
</div>
""", unsafe_allow_html=True)

if budget.decisions:
    st.markdown("### 🧠 Autonomous Payment Decisions")
    for i, decision in enumerate(budget.decisions):
        icon = "✅" if decision.should_purchase else "⏭️"
        service = decision.service_type.value.replace("_", " ").title()
        action = "Purchased" if decision.should_purchase else "Skipped"
        dual_cost = fx_engine.format_dual(decision.cost)

        st.markdown(
            f"""<div class="glass-card" style="padding:1rem;">
            <strong>{icon} Decision #{i+1}</strong> — {service}<br>
            <span style="color:#94a3b8;">Supplier:</span> {decision.supplier_name or decision.supplier_id}<br>
            <span style="color:#94a3b8;">Action:</span> {action} ({dual_cost})<br>
            <span style="color:#94a3b8;">Reason:</span> {decision.reason}<br>
            {f'<span style="color:#94a3b8;">Expected Value:</span> {decision.expected_value}' if decision.expected_value else ''}
            </div>""",
            unsafe_allow_html=True,
        )
else:
    st.info("No payment decisions made yet. The agent will consider purchasing intelligence services during research.")

if budget.transactions:
    st.markdown("### 💳 Transaction History")
    for tx in budget.transactions:
        status = tx.status.value if hasattr(tx.status, "value") else str(tx.status)
        status_icon = "✅" if status == "completed" else "❌" if status == "failed" else "⏳"
        service = tx.service_type.value.replace("_", " ").title()
        dual_tx_amount = fx_engine.format_dual(tx.amount)
        rate_used = tx.fx_rate if tx.fx_rate > 0 else current_rate

        st.markdown(
            f"""<div class="glass-card" style="padding:1rem; border-left: 3px solid {'#22c55e' if status == 'completed' else '#ef4444' if status == 'failed' else '#eab308'};">
            {status_icon} <strong>{service}</strong> — {dual_tx_amount}<br>
            <span style="color:#94a3b8;">Status:</span> {status.title()} &bull; 
            <span style="color:#94a3b8;">FX Rate Used:</span> 1 USD = ₹{rate_used:.2f} INR<br>
            <span style="color:#94a3b8;">Created:</span> {tx.created_at.strftime('%Y-%m-%d %H:%M:%S') if tx.created_at else 'N/A'}
            {f'<br><span style="color:#94a3b8;">Response:</span> {tx.response_summary}' if tx.response_summary else ''}
            {f'<br><span style="color:#ef4444;">Error:</span> {tx.error_message}' if tx.error_message else ''}
            </div>""",
            unsafe_allow_html=True,
        )
