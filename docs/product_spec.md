# ProcureX — Product Specification

**Document Version:** 1.0.0  
**Status:** Draft  
**Target Domain:** Indian B2B Procurement (Industrial PPE Focus)  
**Last Updated:** August 2026  

---

## 1. Product Vision

**ProcureX** is an autonomous procurement research agent engineered specifically for Indian B2B procurement. It bridges the gap between natural language sourcing requirements and verified, actionable procurement decisions.

Traditional B2B procurement in India suffers from fragmented supplier data, unverified claims, opaque pricing (GST variance, tier pricing), and inefficient manual vetting. ProcureX automatically discovers real-world suppliers across permitted public directories and B2B platforms, extracts and normalizes supplier/product data, assesses supplier credibility using verifiable evidence, makes autonomous payment decisions for premium intelligence services via x402 micropayments, and generates transparent, fully-cited procurement recommendations.

---

## 2. Target User

ProcureX is designed for professional buyers operating within the Indian industrial ecosystem:

* **Procurement Managers & Purchasing Officers:** Professionals in manufacturing, construction, logistics, and healthcare managing B2B supply chains.
* **Small-to-Medium Enterprise (SME) Business Owners:** Decision-makers seeking reliable industrial supplies without dedicated procurement research teams.
* **Safety & Compliance Officers:** Managers requiring verified certifications (e.g., ISO, CE, BIS/IS standards) for Personal Protective Equipment (PPE).

---

## 3. Core User Flow

The end-to-end user workflow follows seven structured stages:

```
[1. NL Query Input] ➔ [2. Structured Interpretation] ➔ [3. Autonomous Research Execution]
                                                                    │
[6. Provenance & Trace Review]  [5. Ranked Supplier Evaluation]  [4. Live Progress Monitoring]
         │
         ▼
[7. Final Report & Cited Recommendations]
```

1. **Natural Language Input:** The user enters a natural language procurement requirement (e.g., specifying product, quantity, target price, delivery location, deadline, and certifications).
2. **Structured Requirement Interpretation:** ProcureX parses the prompt into a typed schema, highlighting inferred constraints for user review and explicit confirmation.
3. **Autonomous Research Execution:** ProcureX launches multi-source parallel research across permitted B2B directories, public databases, and verification APIs.
4. **Live Progress Monitoring:** The user watches a real-time execution telemetry feed tracking sources consulted, raw suppliers extracted, normalization progress, evidence gathered, and x402 payment transactions.
5. **Ranked Supplier Evaluation:** ProcureX presents a normalized comparison matrix displaying suppliers ranked by a multi-dimensional composite score alongside explicit confidence metrics.
6. **Provenance & Economic Trace Review:** The user inspects evidence trails (URLs, timestamps, raw snippets) and economic traces (budget allocations, paid API calls, x402 transaction ledger).
7. **Final Report Generation:** The user receives a comprehensive, exportable procurement report complete with primary recommendations, alternative options, contradiction highlights, uncertainty disclosures, and inline citations.

---

## 4. MVP Scope

### 4.1 Initial Focus Domain
* **Domain:** Industrial Personal Protective Equipment (PPE) Procurement in India.
* **Primary Core Product:** **Nitrile Industrial Safety Gloves** (chemical resistant, powder-free/powdered, heavy-duty/disposable industrial grade).

### 4.2 Post-MVP Extensibility Path
* Phase 2: Industrial Safety Helmets (IS 2925 / CE standard compliance).
* Phase 3: Industrial Safety Shoes & Footwear (IS 15298 compliant steel-toe footwear).
* Phase 4: General Industrial MRO (Maintenance, Repair, and Operations) categories.

---

## 5. Procurement Requirement Model

Every procurement request is mapped into a strict, validated data model:

```json
{
  "product_category": "Industrial PPE",
  "material": "Nitrile",
  "application": "Chemical Handling / Industrial Safety",
  "size": "Medium",
  "quantity": 5000,
  "maximum_unit_price": 80.0,
  "currency": "INR",
  "destination": "Ghaziabad, Uttar Pradesh",
  "delivery_deadline_days": 10,
  "preferred_supplier_type": "MANUFACTURER",
  "certification_requirements": ["ISO 9001", "CE", "EN 374"],
  "procurement_mode": "BALANCED"
}
```

### 5.1 Field Definitions & Schema Specification

| Field Name | Type | Enum / Allowed Values | Validation Rules / Description |
| :--- | :--- | :--- | :--- |
| `product_category` | String | `Industrial PPE`, `Safety Footwear`, `Head Protection` | Required. Base category. |
| `material` | String | `Nitrile`, `Latex`, `Neoprene`, `Polyurethane` | Material filter for gloves/PPE. |
| `application` | String | `Industrial Safety`, `Chemical Handling`, `Cleanroom` | Target usage context. |
| `size` | String | `Small`, `Medium`, `Large`, `Extra Large` | Sizing requirement. |
| `quantity` | Integer | $> 0$ | Total units required. |
| `maximum_unit_price`| Float | $> 0.0$ | Upper cap per unit in specified currency. |
| `currency` | String | `INR` | Default: `INR`. |
| `destination` | String | Valid Indian City/PIN/District | Target delivery location. |
| `delivery_deadline` | Integer | $> 0$ (Days) | Maximum permissible delivery timeframe. |
| `preferred_supplier_type`| Enum | `MANUFACTURER`, `DISTRIBUTOR`, `WHOLESALER`, `TRADER`, `ANY` | Preferred supplier classification. |
| `certification_requirements`| Array[String]| `ISO 9001`, `CE`, `EN 374`, `BIS`, `FDA` | Standard compliance flags. |
| `procurement_mode` | Enum | `COST_OPTIMIZED`, `BALANCED`, `RELIABILITY_FIRST` | Weighing profile for scoring engine. |

---

## 6. Example Query Benchmark

```text
"Find 5,000 medium-sized nitrile industrial safety gloves under ₹80 per piece, preferably from manufacturers, deliverable to Ghaziabad within 10 days. Find the top 3 suppliers and assess their credibility."
```

---

## 7. Streamlit UI Architecture & Pages

The user interface is structured into six dedicated, intuitive navigation pages:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PROCUREX STREAMLIT UI                           │
├──────────────┬──────────────┬─────────────┬───────────┬──────────────┬─┴───────────┐
│ 1. Input     │ 2. Live      │ 3. Supplier │ 4. Evidence│ 5. Economic │ 6. Final    │
│    Research  │    Research  │    Matrix   │    Trace  │    Trace     │    Report   │
└──────────────┴──────────────┴─────────────┴───────────┴──────────────┴─────────────┘
```

### 1. Research Input Page
* Interactive prompt box for natural language entry.
* One-click "Parse Requirement" trigger.
* Interactive form preview displaying the extracted `ProcurementRequirementModel` with editable overrides.
* Procurement mode selector (`COST_OPTIMIZED`, `BALANCED`, `RELIABILITY_FIRST`).

### 2. Live Research Page
* Real-time execution status bar and telemetry console.
* Live counters: Permitted Sources Polled, Suppliers Discovered, Claims Extracted, Verification Checks Completed.
* Active log stream showing agent reasoning, x402 budget consumption, and service API hits.

### 3. Suppliers Page
* Sortable, filterable comparison matrix of discovered suppliers.
* High-level summary metrics: Composite Score (0-100), Confidence Score (0-100%), Normalized Price (INR/piece), Distance/ETD.
* Supplier categorization badges (`Manufacturer`, `Distributor`, etc.).
* Deep-dive breakdown of individual category scores (Product Fit, Price, Verification, Logistics, MOQ, Evidence).

### 4. Evidence Page
* Full evidence provenance table detailing every factual claim made about a supplier.
* Direct source links, retrieval timestamps, raw text snippets, and document hashes.
* Visual contradiction indicators highlighting discrepancies between multiple sources (e.g., price mismatch across directories).

### 5. Economic Trace Page
* Transparent breakdown of research budget allocation (e.g., initial budget ₹50 / $0.60 USD).
* Itemized transaction ledger of x402 payments executed for paid intelligence endpoints (e.g., GSTIN verification, credit score check, premium director lookup).
* Return on Investment (ROI) metric showing estimated savings vs. research cost.

### 6. Final Report Page
* Formatted executive summary with top 3 recommended suppliers.
* Comprehensive risk analysis, delivery schedule projections, and recommended procurement strategy.
* Export capabilities: One-click export to PDF, CSV, and Markdown.

---

## 8. Key Features & Functional System Modules

### 8.1 Natural Language Requirement Parsing
* Parses complex user queries into structured JSON via deterministic LLM prompt templates and Pydantic validation models.
* Fallback heuristics ensure missing fields are populated with sensible defaults (e.g., default currency = `INR`, procurement_mode = `BALANCED`).

### 8.2 Real Supplier Discovery (Permitted Sources)
* Queries permitted public registries, government B2B listings, and accessible web sources.
* Strict compliance with site policies and standard rate-limiting.

### 8.3 Price Normalization Engine
* Standardizes disparate pricing structures into a single metric: **INR per piece (GST inclusive)**.
* Handles conversions: Per box/carton to per piece, per pair to per piece, GST addition/exclusion (18% standard rate applied when omitted).

### 8.4 Supplier Classification Engine
* Categorizes entities into: `Manufacturer`, `Distributor`, `Wholesaler`, `Trader`, or `Unknown`.
* Based on GST active business activities, manufacturing unit declarations, plant locations, and import/export code (IEC) presence.

### 8.5 Evidence-Backed Claims & Provenance Tracking
* No ungrounded assertions: Every data point (MOQ, lead time, price, certification) must point to at least one valid `EvidenceRecord`.

### 8.6 Geographic & Logistics Analysis
* Calculates straight-line and estimated road transit distances from supplier origin city/state to destination (`Ghaziabad, UP`).
* Estimates lead times based on distance tiers and transport modes in India.

### 8.7 Deterministic Scoring Engine
Composite Score $S \in [0, 100]$ is computed using a weighted sum across six dimensions:

$$\text{Composite Score} = w_1 S_{\text{fit}} + w_2 S_{\text{price}} + w_3 S_{\text{verif}} + w_4 S_{\text{deliv}} + w_5 S_{\text{moq}} + w_6 S_{\text{evid}}$$

#### Base Category Weights (Balanced Mode):
* **Product Fit ($S_{\text{fit}}$):** 25 points — Material, size, and application matching.
* **Price Score ($S_{\text{price}}$):** 20 points — Relative position against target unit price.
* **Verification Score ($S_{\text{verif}}$):** 20 points — Active GSTIN, business age, IEC status, physical address confirmation.
* **Delivery & Geo Score ($S_{\text{deliv}}$):** 15 points — Lead time compatibility with deadline.
* **MOQ Score ($S_{\text{moq}}$):** 10 points — Alignment of supplier Minimum Order Quantity with required quantity.
* **Evidence Quality Score ($S_{\text{evid}}$):** 10 points — Multi-source verification ratio and recency.

```
Total Base Weight = 25 + 20 + 20 + 15 + 10 + 10 = 100 Points
```

### 8.8 Separate Score vs. Confidence Metrics
* **Score:** Evaluates *how well* the supplier matches the user's requirements.
* **Confidence:** Evaluates *how reliable* the data behind the score is (based on data completeness, source reliability, and age of evidence). High score with low confidence signals a high-potential but unverified supplier.

### 8.9 Autonomous x402 Payment Engine
* ProcureX operates with an autonomous budget for data enrichment.
* Evaluates cost-vs-value before spending micropayments (x402 protocol) on premium paid intelligence services (e.g., deep GST verification, credit checks).
* Automatically logs every transaction in the Economic Trace ledger.

### 8.10 Contradiction & Uncertainty Management
* Detects conflicting data points (e.g., Directory A lists MOQ as 1,000; Directory B lists MOQ as 5,000).
* Highlights contradictions explicitly in the UI and reduces confidence scores accordingly rather than averaging or guessing.

### 8.11 Graceful Degradation
* If a primary data source times out or fails, the research pipeline continues using secondary sources, marking affected fields as `UNVERIFIED` without crashing.

---

## 9. Definition of Done (MVP)

The MVP is complete when the following scenario executes end-to-end flawlessly:

1. Input natural language query for Nitrile Gloves (Ghaziabad destination, 5,000 units, ₹80 target price).
2. Requirement correctly parsed into structured JSON model.
3. System discovers at least 5 real Indian suppliers from permitted public sources.
4. Data extracted, normalized (INR/piece), deduplicated, and filtered.
5. Verification checks executed (GSTIN/address validation) with x402 payment decisions evaluated and logged.
6. Geographic transit times to Ghaziabad computed.
7. Suppliers scored and ranked deterministically.
8. Output rendered across Streamlit UI pages with zero fabricated data and full evidence citations.

---

## 10. Non-Goals (MVP Scope Boundaries)

To maintain sharp focus, ProcureX explicitly excludes the following features from the MVP scope:

* **Not a B2B Marketplace:** ProcureX does not host sellers or process product transactions.
* **Not an SRM (Supplier Relationship Management) Suite:** Does not provide contract management or vendor onboarding workflows.
* **Not an Order Execution System:** Does not issue Purchase Orders (POs) or execute physical procurement orders.
* **No Unrestricted Domain Generalization:** Scope is strictly bounded to Industrial PPE (Nitrile Gloves baseline).
* **No Aggressive / Unlawful Scraping:** ProcureX strictly adheres to web standards, public APIs, and permitted data sources.
