"""Procurement Requirement Input Page."""

import streamlit as st
from datetime import datetime
from extraction.requirement_parser import parse_requirement
from storage.session import ResearchSession, ResearchPhase
from models.budget import ResearchBudget

st.set_page_config(page_title="ProcureX — Requirement", page_icon="📝", layout="wide")

try:
    from app import apply_custom_css, init_session_state
    apply_custom_css()
    init_session_state()
except Exception:
    pass

st.markdown("<h1>📝 Procurement <span class='gradient-text'>Requirement</span></h1>", unsafe_allow_html=True)
st.markdown("*Describe your procurement needs in natural language for AI parsing and autonomous research.*")

CANONICAL_QUERY = (
    "Find 5,000 medium-sized nitrile industrial safety gloves under ₹80 per piece, "
    "preferably from manufacturers, deliverable to Ghaziabad within 10 days. "
    "Find the top 3 suppliers and assess their credibility."
)

query_input = st.text_area(
    "Natural Language Procurement Query:",
    value=st.session_state.get("raw_query", CANONICAL_QUERY),
    height=120,
    help="Enter your exact requirement including quantity, specs, budget, destination, and deadline."
)

col_a, col_b = st.columns([1, 1])
with col_a:
    procurement_mode = st.selectbox(
        "Procurement Mode:",
        options=["balanced", "cost_optimized", "reliability_first"],
        format_func=lambda x: x.replace("_", " ").title(),
        help="Balanced balances price and quality; Cost-Optimized prioritizes lowest unit price; Reliability-First prioritizes verified manufacturers."
    )
with col_b:
    budget_val = st.number_input(
        "Research Budget (USD):",
        min_value=0.005,
        max_value=0.100,
        value=0.020,
        step=0.005,
        format="%.3f",
        help="Autonomous budget for querying paid price intelligence and supplier verification services via x402."
    )

if st.button("🔍 Parse & Validate Requirement", type="primary", use_container_width=True):
    with st.spinner("Parsing requirement using Gemini LLM / Rule-based NLP..."):
        requirement = parse_requirement(query_input)
        # Override mode if selected in UI
        from models.requirement import ProcurementMode
        if procurement_mode == "cost_optimized":
            requirement.procurement_mode = ProcurementMode.COST_OPTIMIZED
        elif procurement_mode == "reliability_first":
            requirement.procurement_mode = ProcurementMode.RELIABILITY_FIRST

        st.session_state.parsed_requirement = requirement
        st.session_state.raw_query = query_input
        st.success("Requirement parsed successfully!")

if "parsed_requirement" in st.session_state and st.session_state.parsed_requirement:
    req = st.session_state.parsed_requirement

    st.markdown("---")
    st.markdown("### 📋 Parsed Specification Summary")

    try:
        from ui.components.requirement_card import render_requirement_card
        render_requirement_card(req)
    except Exception:
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Product:** {req.product_category}")
        c1.markdown(f"**Material:** {req.material}")
        c2.markdown(f"**Quantity:** {req.quantity:,}")
        c2.markdown(f"**Max Unit Price:** ₹{req.maximum_unit_price}/piece")
        c3.markdown(f"**Destination:** {req.destination}")
        c3.markdown(f"**Mode:** {req.procurement_mode.value}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Start Autonomous Agent Research", type="primary", use_container_width=True):
        # Create session
        session = ResearchSession(
            requirement=req,
            budget=ResearchBudget(initial_budget=budget_val, remaining_budget=budget_val)
        )
        st.session_state.research_session = session
        st.session_state.research_active = True
        st.switch_page("pages/2_live_research.py")
