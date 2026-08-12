"""Procurement Requirement Input Page."""

import streamlit as st
from datetime import datetime
from extraction.requirement_parser import parse_requirement
from storage.session import ResearchSession
from models.budget import ResearchBudget
from models.requirement import ProcurementMode

st.set_page_config(page_title="ProcureX — Requirement Input", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>Requirement <span class='gradient-text'>Input</span></h1>", unsafe_allow_html=True)
st.markdown("*Describe your procurement needs in natural language for AI parsing and autonomous research.*")

CANONICAL_QUERY = (
    "Find 5,000 medium-sized nitrile industrial safety gloves under ₹80 per piece, "
    "preferably from manufacturers, deliverable to Ghaziabad within 10 days. "
    "Find the top 3 suppliers and assess their credibility."
)

st.markdown("""
<div class="glass-card" style="padding: 1.2rem; margin-bottom: 1.5rem;">
    <h4 style="margin-top: 0; font-size: 1rem; color: #38bdf8;">Example Requirement Prompt</h4>
    <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0;">
        Include quantity, product specs, target budget per unit, destination, and supplier preference if available.
    </p>
</div>
""", unsafe_allow_html=True)

query_input = st.text_area(
    "Natural Language Procurement Query:",
    value=st.session_state.get("raw_query", CANONICAL_QUERY),
    height=110,
    help="Enter your exact requirement."
)

col_a, col_b = st.columns([1, 1])
with col_a:
    procurement_mode = st.selectbox(
        "Procurement Mode Strategy:",
        options=["balanced", "cost_optimized", "reliability_first"],
        format_func=lambda x: x.replace("_", " ").title(),
        help="Balanced: equal weight; Cost-Optimized: prioritizes lowest price; Reliability-First: prioritizes verified suppliers."
    )
with col_b:
    budget_val = st.number_input(
        "Autonomous Micro-Query Budget (USD):",
        min_value=0.005,
        max_value=0.100,
        value=0.020,
        step=0.005,
        format="%.3f",
        help="Research budget allocated for information buying."
    )

if st.button("Parse & Validate Requirement Specification", type="primary", use_container_width=True):
    with st.spinner("Analyzing prompt with extraction pipeline..."):
        requirement = parse_requirement(query_input)
        if procurement_mode == "cost_optimized":
            requirement.procurement_mode = ProcurementMode.COST_OPTIMIZED
        elif procurement_mode == "reliability_first":
            requirement.procurement_mode = ProcurementMode.RELIABILITY_FIRST

        st.session_state.parsed_requirement = requirement
        st.session_state.raw_query = query_input
        st.success("Requirement specification parsed successfully!")

if "parsed_requirement" in st.session_state and st.session_state.parsed_requirement:
    req = st.session_state.parsed_requirement
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Launch Autonomous Research Agent", type="primary", use_container_width=True):
        session = ResearchSession(
            requirement=req,
            budget=ResearchBudget(initial_budget=budget_val, remaining_budget=budget_val)
        )
        st.session_state.research_session = session
        st.session_state.research_active = True
        st.switch_page("pages/2_Live_Screening_Status.py")
