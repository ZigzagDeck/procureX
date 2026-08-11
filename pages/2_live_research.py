"""Live Research Execution and Status Page."""

import streamlit as st
import asyncio
from agent.orchestrator import ResearchOrchestrator
from storage.session import ResearchPhase

st.set_page_config(page_title="ProcureX — Live Research", page_icon="📡", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>📡 Live <span class='gradient-text'>Research Status</span></h1>", unsafe_allow_html=True)

session = st.session_state.get("research_session")

if not session or not session.requirement:
    st.warning("⚠️ No active research session. Please enter a procurement requirement first.")
    if st.button("Go to Requirement Input"):
        st.switch_page("pages/1_research.py")
    st.stop()

# Run research if not already started/completed
if session.phase == ResearchPhase.NOT_STARTED:
    with st.spinner("Executing autonomous supplier discovery, verification, and scoring pipeline..."):
        orchestrator = ResearchOrchestrator()
        asyncio.run(orchestrator.run_research(session.requirement, session))
        st.success("Research completed!")

# Status metrics header
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Status Phase", session.phase.value.replace("_", " ").title())
c2.metric("Discovered Suppliers", f"{len(session.suppliers)}")
c3.metric("Unique Ranked", f"{len(session.get_ranked_suppliers())}")
c4.metric("Sources Consulted", f"{len(session.sources_consulted)}")
c5.metric("Budget Spent", f"${session.budget.total_spent:.3f}", delta=f"${session.budget.remaining_budget:.3f} left")

st.markdown("---")
st.markdown("### 📜 Autonomous Agent Execution Log")

log_container = st.container(height=400)
with log_container:
    if session.log:
        for entry in session.log:
            ts = entry.timestamp.strftime("%H:%M:%S")
            phase_name = entry.phase.value.replace("_", " ").upper()
            st.markdown(
                f"""<div style="background: rgba(255,255,255,0.02); padding: 8px 12px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #3b82f6;">
                <span style="color: #94a3b8; font-family: monospace; font-size: 0.85em;">[{ts}]</span>
                <span style="background: rgba(59,130,246,0.2); color: #60a5fa; font-size: 0.75em; padding: 2px 6px; border-radius: 4px; font-weight: 600; margin: 0 8px;">{phase_name}</span>
                <span>{entry.message}</span>
                </div>""",
                unsafe_allow_html=True
            )
    else:
        st.info("Log empty.")

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏭 View Suppliers", use_container_width=True):
        st.switch_page("pages/3_suppliers.py")

with col2:
    if st.button("🔗 Browse Evidence & Verification", use_container_width=True):
        st.switch_page("pages/4_evidence.py")

with col3:
    if st.button("📋 Generate Final Executive Report", type="primary", use_container_width=True):
        st.switch_page("pages/6_final_report.py")
