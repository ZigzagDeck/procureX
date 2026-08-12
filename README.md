# ProcureX — Autonomous B2B Procurement Intelligence Engine

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

```
procurex/
├── app.py                         # Main Streamlit application entry point & shared navigation sidebar
├── agent/                         # Autonomous orchestrator & search execution agent
│   └── orchestrator.py
├── extraction/                    # Natural language parser & Gemini extraction pipelines
│   └── requirement_parser.py
├── models/                        # Core data models (Requirement, Supplier, Product, Budget)
│   ├── requirement.py
│   ├── supplier.py
│   ├── product.py
│   └── budget.py
├── pages/                         # Streamlit multi-page interface
│   ├── 1_Requirement_Input.py     # Natural language query input & parsing
│   ├── 2_Live_Screening_Status.py # Real-time agent screening & execution log
│   ├── 3_Discovered_Suppliers.py  # Candidate list with site links, unit price & MOQ
│   ├── 4_Evidence_Browser.py     # Fetched web source URLs registry
│   └── 5_Economic_Trace.py        # Quota tracker, FX engine & x402 payment trace
├── storage/                       # Session state & data persistence
│   └── session.py
├── tests/                         # Pytest unit & integration test suite (47 tests)
├── ui/                            # Custom UI components (Supplier card, Budget tracker)
│   └── components/
└── x402/                          # Micropayment protocol, FX engine & JWT token signer
    ├── account.py
    ├── fx_engine.py
    └── token_signer.py
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
