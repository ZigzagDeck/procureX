"""Live Screening Execution and Status Page."""

import streamlit as st
import asyncio
from agent.orchestrator import ResearchOrchestrator
from storage.session import ResearchPhase

st.set_page_config(page_title="ProcureX — Live Screening Status", layout="wide")

try:
    from app import apply_custom_css, init_session_state, render_common_sidebar
    apply_custom_css()
    init_session_state()
    render_common_sidebar()
except Exception:
    pass

st.markdown("<h1>Live Screening <span class='gradient-text'>Status</span></h1>", unsafe_allow_html=True)
st.markdown("*Live web screening and autonomous supplier discovery pipeline. Please wait 30s–1min for screening to complete.*")

session = st.session_state.get("research_session")

if not session or not session.requirement:
    st.warning("No active research session. Please enter a procurement requirement first.")
    if st.button("Go to Requirement Input"):
        st.switch_page("pages/1_Requirement_Input.py")
    st.stop()

# Run research if not already started/completed
if session.phase == ResearchPhase.NOT_STARTED:
    with st.spinner("Executing autonomous live screening and supplier discovery pipeline (30s-1min)..."):
        orchestrator = ResearchOrchestrator()
        asyncio.run(orchestrator.run_research(session.requirement, session))
        st.success("Live screening completed!")

# Status metrics header
c1, c2, c3 = st.columns(3)
c1.metric("Status Phase", session.phase.value.replace("_", " ").title())
c2.metric("Discovered Suppliers", f"{len(session.suppliers)}")
c3.metric("Unique Candidates", f"{len(session.get_ranked_suppliers())}")

st.markdown("---")
st.markdown("### Autonomous Agent Execution Log")

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
col1, col2 = st.columns(2)

with col1:
    if st.button("View Discovered Suppliers", use_container_width=True):
        st.switch_page("pages/3_Discovered_Suppliers.py")

with col2:
    if st.button("Browse Evidence Verification", type="primary", use_container_width=True):
        st.switch_page("pages/4_Evidence_Browser.py")
