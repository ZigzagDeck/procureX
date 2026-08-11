# ProcureX — x402 Integration Specification

## Overview
x402 is an open-source protocol that enables machine-to-machine payments using HTTP 402 (Payment Required). ProcureX uses x402 to enable the autonomous procurement agent to pay for specialized intelligence services when the expected value exceeds the cost.

## Scope
x402 is ONLY used for:
1. **Price Intelligence Service** — Market price analysis for specific products
2. **Supplier Verification Service** — Enhanced supplier credibility verification

x402 is NOT used for:
- Internal computation
- Basic web searches
- Data extraction
- Scoring calculations
- Geographic analysis

## Architecture

### Client Side (Agent)
Location: `x402/`
- Uses official `x402` Python SDK (`pip install x402[httpx]`)
- Handles the 402 challenge-response payment flow
- Signs payment payloads with configured wallet
- Tracks spending against research budget

### Server Side (Intelligence Services)
Location: `services/`
- FastAPI endpoints protected by x402 middleware
- `POST /v1/price-intelligence`
- `POST /v1/supplier-verification`
- Returns structured JSON responses

## Payment Flow
1. Agent requests intelligence service endpoint
2. Server returns HTTP 402 with payment requirements (amount, asset, recipient)
3. Agent evaluates autonomous payment policy
4. If approved: Agent signs payment payload using x402 SDK
5. Agent retries request with payment header
6. Server verifies payment and delivers intelligence
7. Transaction recorded in research trace

## Budget Model

### Configuration
```python
class ResearchBudget:
    initial_budget: float = 0.020  # $0.020 USD
    remaining_budget: float
    total_spent: float = 0.0
    transactions: list[PaymentTransaction]
```

### Service Costs (Configurable Defaults)
| Service | Default Cost | Configurable Via |
|---|---|---|
| Price Intelligence | $0.002 | `PROCUREX_PRICE_INTEL_COST` env var |
| Supplier Verification | $0.001 | `PROCUREX_SUPPLIER_VERIFY_COST` env var |

## Autonomous Payment Policy
The agent MUST evaluate before every purchase:

```
IF information_is_necessary
   AND candidate_is_finalist (top-ranked or close)
   AND expected_value > service_cost
   AND remaining_budget >= service_cost
THEN purchase
ELSE skip (record decision in trace)
```

### Decision Criteria

#### Price Intelligence
- Trigger: Price uncertainty is HIGH (>20% spread across sources OR single source only)
- Candidate: Supplier is in top N ranked candidates
- Budget: `remaining_budget >= price_intelligence_cost`

#### Supplier Verification
- Trigger: Business verification score is LOW (<50%) for a finalist
- Candidate: Supplier is in top N ranked candidates
- Budget: `remaining_budget >= supplier_verification_cost`

## Service Contracts

### POST /v1/price-intelligence
**Request:**
```json
{
  "product_category": "nitrile_gloves",
  "material": "nitrile",
  "application": "industrial_safety",
  "size": "M",
  "quantity": 5000,
  "region": "NCR"
}
```

**Response:**
```json
{
  "market_price_range": {"min": 45.0, "max": 95.0, "median": 68.0, "currency": "INR"},
  "price_trend": "stable",
  "data_sources_count": 12,
  "confidence": 0.82,
  "generated_at": "2026-08-10T12:00:00Z"
}
```

### POST /v1/supplier-verification
**Request:**
```json
{
  "supplier_name": "ABC Safety Products Pvt Ltd",
  "gstin": "09AAACR5678K1ZH",
  "address": "Plot 45, Industrial Area, Noida",
  "claimed_type": "MANUFACTURER"
}
```

**Response:**
```json
{
  "gstin_status": "ACTIVE",
  "registered_name": "ABC SAFETY PRODUCTS PRIVATE LIMITED",
  "business_type": "Private Limited Company",
  "registration_date": "2018-07-01",
  "principal_place": "Noida, Uttar Pradesh",
  "msme_registered": true,
  "msme_category": "Small",
  "verification_confidence": 0.88,
  "verified_at": "2026-08-10T12:00:00Z"
}
```

## Development Mode
- Environment variable: `PROCUREX_X402_MODE=mock|live`
- Mock mode: Services return realistic structured data without actual payment
- Mock mode: Payment flow is simulated (402 → sign → 200)
- Mock data MUST be clearly labeled as mock in provenance
- Mock mode MUST NOT contaminate production research results

## Wallet Configuration
```
PROCUREX_WALLET_PRIVATE_KEY=<env var, never in code>
PROCUREX_X402_NETWORK=base-sepolia  # testnet for MVP
PROCUREX_FACILITATOR_URL=<x402 facilitator endpoint>
PROCUREX_X402_MODE=mock  # or 'live'
```

## Economic Trace (UI Display)
The Economic Trace page must show:
- Starting research budget
- For each service considered: service name, supplier, decision (purchase/skip), reason
- For each purchase: amount, transaction status, response summary
- Total spent
- Remaining budget
