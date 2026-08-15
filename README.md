# ProcureX: — Autonomous B2B Procurement Intelligence Engine

**ProcureX** is an autonomous AI agent designed to streamline B2B procurement research. It accepts natural language procurement requests, autonomously screens live web search results, normalizes pricing across non-standard units (piece, pair, box), matches technical specifications, and tracks micro-query information buying expenses using an x402 payment protocol simulation.

---

## Key Capabilities & Features

1. **Natural Language Requirement Parsing**:
   - Parses complex commercial procurement prompts into structured attributes: target item, category, material, quantity, max budget per unit, delivery location, and urgency.
   - Normalizes sizing (e.g. `M` -> `Medium`) and product specifications.
   - Supports strategy modes: `Balanced`, `Cost-Optimized`, and `Reliability-First`.

2. **Live Autonomous Web Screening**:
   - Executes real-time search queries against live web indices using DuckDuckGo (`ddgs`) and Google Gemini API for structured extraction.
   - Filters out non-relevant content and isolates potential manufacturer and supplier listings.

3. **Entity Resolution & Candidate Ranking**:
   - Groups discovered listings by supplier identity to prevent duplicate candidate entries.
   - Extracts unit price and Minimum Order Quantity (MOQ) metrics where available.
   - Ranks candidates based on product specification alignment and pricing constraints.

4. **x402 Micropayment Protocol Simulation**:
   - Models HTTP 402 Payment Required micro-transactions for information buying.
   - Integrates a real-time FX conversion engine (cached hourly via `open.er-api.com`) to manage balances in USD and INR.
   - Features a thread-safe local JSON ledger and HMAC-SHA256 JWT payment proof verification.
   - Tracks daily API quota limits with real-time exhaustion percentage metrics.

5. **Clean & Modern UI Design**:
   - Built on Streamlit with dark glassmorphism aesthetic styling.
   - Uses professional typography (*Plus Jakarta Sans* and *Inter*).
   - Uniform sidebar navigation across all application pages.

---

## Tech Stack

- **Framework**: Python 3.14, Streamlit
- **AI & Extraction Engine**: Google GenAI SDK (`google-genai`), Custom Rule Engine
- **Web Search**: DuckDuckGo Search (`ddgs`)
- **Security & Payments**: PyJWT (HMAC-SHA256), `open.er-api.com` FX API
- **Testing Suite**: Pytest

---

## Repository Structure

```procurex/
├── app.py                         # Main Streamlit application entry point & shared navigation sidebar
├── README.md                      # Complete project documentation & setup guide
├── .gitignore                     # Git ignore rules for virtual environments, caches, and credentials
├── requirements.txt               # Application package dependencies
├── agent/                         # Autonomous orchestrator & search execution agent
│   ├── __init__.py
│   └── orchestrator.py            # Manages screening pipelines and progress logs
├── extraction/                    # Natural language parser & extraction pipelines
│   ├── __init__.py
│   ├── provenance.py              # Manages evidence links and sources
│   ├── requirement_parser.py      # Uses Gemini to parse raw English queries
│   └── supplier_extractor.py      # Extracts raw entity structures from web search data
├── intelligence/                  # Scoring & price normalization logic
│   ├── __init__.py
│   └── price_intelligence.py      # Normalizes prices (piece/pair/box) & handles currency conversions
├── models/                        # Core data structures (Requirement, Supplier, Product, Budget)
│   ├── __init__.py
│   ├── budget.py                  # Tracks current session budget metrics
│   ├── evidence.py                # Defines structures for verification evidence
│   ├── product.py                 # Structured representations of products found
│   ├── requirement.py             # Parses procurement parameters
│   ├── scoring.py                 # Scoring schemas for candidate suppliers
│   └── supplier.py                # Deduplicated B2B supplier candidate models
├── pages/                         # Streamlit multi-page interface
│   ├── 1_Requirement_Input.py     # Natural language query input & parsing
│   ├── 2_Live_Screening_Status.py # Real-time agent screening & execution log
│   ├── 3_Discovered_Suppliers.py  # Candidate list with site links, unit price & MOQ
│   ├── 4_Evidence_Browser.py      # Fetched web source URLs registry
│   └── 5_Economic_Trace.py        # Quota tracker, FX engine & x402 payment trace
├── storage/                       # Session state & data persistence
│   ├── __init__.py
│   ├── session.py                 # Handles Streamlit state synchronization
│   └── trace.py                   # Auditing data structures
├── tests/                         # Pytest unit & integration test suite
│   ├── __init__.py
│   ├── test_budget_decisions.py
│   ├── test_e2e.py
│   ├── test_entity_resolver.py
│   ├── test_evidence.py
│   ├── test_fx_engine.py
│   ├── test_prepaid_account.py
│   ├── test_price_normalizer.py
│   ├── test_product_matcher.py
│   ├── test_requirement_parser.py
│   ├── test_scoring.py
│   ├── test_token_signer.py
│   └── test_x402.py
├── ui/                            # Custom UI components
│   ├── __init__.py
│   └── components/
│       ├── __init__.py
│       ├── budget_tracker.py      # Renders real-time financial tracking components
│       ├── evidence_viewer.py     # UI elements for reviewing verified search parameters
│       └── supplier_card.py       # Renders supplier cards with price & MOQ metrics
├── verification/                  # Verification logic (Udyam & GST placeholders)
│   ├── __init__.py
│   ├── gst_verifier.py
│   └── udyam_verifier.py
└── x402/                          # Micropayment protocol, FX engine & JWT token signer
    ├── __init__.py
    ├── account.py                 # Manages prepaid local balances via JSON ledger
    ├── client.py                  # Simulated micropayment network client
    ├── fx_engine.py               # Implements live currency conversions using open.er-api.com
    └── token_signer.py            # Generates HMAC-SHA256 JWT payment tokens
```

---

## Setup & Local Execution

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Installation
Clone the repository and install required dependencies:
```bash
pip install streamlit ddgs google-genai PyJWT fpdf2 pytest
```

### 3. Running Unit & Integration Tests
Verify system functionality with pytest:
```bash
python -m pytest tests/ -v
```

### 4. Running the Application
Launch the Streamlit web server:
```bash
python -m streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## Credits & License

Created as **An APEX Creation**. All rights reserved.
