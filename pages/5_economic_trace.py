"""Economic Trace — Research budget allocation and x402 payment decisions."""

import streamlit as st

st.set_page_config(page_title="ProcureX — Economic Trace", page_icon="💰", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>💰 Economic <span class='gradient-text'>Trace</span></h1>", unsafe_allow_html=True)
st.markdown("*Research budget allocation and x402 payment decisions*")

session = st.session_state.get("research_session")

if not session:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem;">
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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Initial Budget", f"${budget.initial_budget:.3f}")
    with col2:
        st.metric("💸 Spent", f"${budget.total_spent:.3f}")
    with col3:
        st.metric("💰 Remaining", f"${budget.remaining_budget:.3f}")

st.markdown("---")
st.markdown("### 🔐 x402 Payment Protocol")
st.markdown("""
<div class="glass-card">
    <p style="color:#94a3b8;">
    ProcureX uses the <strong>x402 protocol</strong> (HTTP 402 Payment Required) to autonomously 
    pay for specialized intelligence services. The agent evaluates whether the expected value of 
    information exceeds the cost before committing research budget.
    </p>
    <p style="color:#64748b; font-size:0.85rem;">
    Active Service: <strong>Price Intelligence</strong> ($0.002)
    </p>
</div>
""", unsafe_allow_html=True)

if budget.decisions:
    st.markdown("### 🧠 Autonomous Payment Decisions")
    for i, decision in enumerate(budget.decisions):
        icon = "✅" if decision.should_purchase else "⏭️"
        service = decision.service_type.value.replace("_", " ").title()
        action = "Purchased" if decision.should_purchase else "Skipped"

        st.markdown(
            f"""<div class="glass-card" style="padding:1rem;">
            <strong>{icon} Decision #{i+1}</strong> — {service}<br>
            <span style="color:#94a3b8;">Supplier:</span> {decision.supplier_name or decision.supplier_id}<br>
            <span style="color:#94a3b8;">Action:</span> {action} (${decision.cost:.3f})<br>
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

        st.markdown(
            f"""<div class="glass-card" style="padding:1rem; border-left: 3px solid {'#22c55e' if status == 'completed' else '#ef4444' if status == 'failed' else '#eab308'};">
            {status_icon} <strong>{service}</strong> — ${tx.amount:.3f} {tx.currency}<br>
            <span style="color:#94a3b8;">Status:</span> {status.title()}<br>
            <span style="color:#94a3b8;">Created:</span> {tx.created_at.strftime('%Y-%m-%d %H:%M:%S') if tx.created_at else 'N/A'}
            {f'<br><span style="color:#94a3b8;">Response:</span> {tx.response_summary}' if tx.response_summary else ''}
            {f'<br><span style="color:#ef4444;">Error:</span> {tx.error_message}' if tx.error_message else ''}
            </div>""",
            unsafe_allow_html=True,
        )
