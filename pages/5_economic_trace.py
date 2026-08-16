"""Economic Trace — Quota Expense Tracker & x402 Micropayment Protocol."""

import streamlit as st
from x402.fx_engine import FXEngine
from x402.account import PrepaidUSDAccount

st.set_page_config(page_title="ProcureX — Economic Trace & Quota", layout="wide")

try:
    from app import apply_custom_css, init_session_state, render_common_sidebar
    apply_custom_css()
    init_session_state()
    render_common_sidebar()
except Exception:
    pass

st.markdown("<h1>Economic Trace & <span class='gradient-text'>Quota Tracker</span></h1>", unsafe_allow_html=True)
st.markdown("*Autonomous research budget allocation, live FX conversion, and x402 micropayment quota tracker.*")

if "fx_engine" not in st.session_state:
    st.session_state.fx_engine = FXEngine()
fx_engine = st.session_state.fx_engine

account = PrepaidUSDAccount()
current_rate = fx_engine.get_rate()

st.info(f"Live FX Exchange Rate: 1 USD = ₹{current_rate:.2f} INR (Auto-cached hourly via open.er-api.com)")

# Daily Quota & Balance Overview
st.markdown("### Daily API Quota & Account Balance")

DAILY_QUOTA_MAX_USD = 0.100  # $0.100 daily limit (~50 micro-queries)
balance = account.get_balance()
session = st.session_state.get("research_session")

total_spent = session.budget.total_spent if session else 0.0
quota_remaining = max(0.0, DAILY_QUOTA_MAX_USD - total_spent)
quota_pct = (total_spent / DAILY_QUOTA_MAX_USD) * 100

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Prepaid USD Balance", fx_engine.format_dual(balance))
with c2:
    st.metric("Daily Quota Limit", fx_engine.format_dual(DAILY_QUOTA_MAX_USD))
with c3:
    st.metric("Quota Used Today", fx_engine.format_dual(total_spent))
with c4:
    st.metric("Remaining Quota", fx_engine.format_dual(quota_remaining))

st.progress(min(total_spent / DAILY_QUOTA_MAX_USD, 1.0), text=f"Daily Micro-Query Quota Exhaustion: {quota_pct:.1f}% used")

if quota_pct >= 80:
    st.error("Quota Exhaustion Alert: You have used over 80% of your daily API rate limit. Top up or reset to avoid query throttling.")

top_col1, top_col2 = st.columns([1, 1])
with top_col1:
    if st.button("Top Up Account Balance ($0.050 USD)", type="secondary", use_container_width=True):
        new_bal = account.top_up(0.050)
        st.success(f"Successfully topped up balance! New balance: {fx_engine.format_dual(new_bal)}")
        st.rerun()

with top_col2:
    if st.button("Reset Daily Quota Tracker", type="secondary", use_container_width=True):
        if session:
            session.budget.total_spent = 0.0
            session.budget.remaining_budget = session.budget.initial_budget
        st.success("Daily quota tracker reset successfully!")
        st.rerun()

st.markdown("---")

if session:
    from ui.components.budget_tracker import render_budget_tracker
    render_budget_tracker(session.budget)

# Product Vision Section
st.markdown("### Protocol Transparency & Product Vision")

st.markdown(f"""
<div class="glass-card">
    <h4 style="margin-top:0; color:#38bdf8;">x402 Micropayment Protocol Specifications</h4>
    <p style="color:#cbd5e1; font-size:0.9rem; line-height:1.6;">
        ProcureX implements the x402 protocol (HTTP 402 Payment Required) to give autonomous AI agents financial convenience.
    </p>
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:12px;">
        <div style="background:rgba(15,23,42,0.6); padding:12px; border-radius:8px; border:1px solid rgba(255,255,255,0.05);">
            <strong style="color:white;">Current Architecture State:</strong>
            <ul style="color:#94a3b8; font-size:0.85rem; margin:6px 0 0 0; padding-left:18px;">
                <li>Live FX Engine with 1h rate caching & fallback</li>
                <li>Thread-safe local JSON ledger balance management</li>
                <li>HMAC-SHA256 JWT payment proof signing</li>
                <li>Rule-based information value decision engine</li>
            </ul>
        </div>
        <div style="background:rgba(15,23,42,0.6); padding:12px; border-radius:8px; border:1px solid rgba(255,255,255,0.05);">
            <strong style="color:white;">Product Vision:</strong>
            <ul style="color:#94a3b8; font-size:0.85rem; margin:6px 0 0 0; padding-left:18px;">
                <li>Integration with Stripe / UPI payment rails</li>
                <li>Production GSTIN & Udyam API integrations</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
