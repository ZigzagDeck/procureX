# ProcureX — Domain Rules

## Overview
Deterministic business rules for Indian B2B PPE procurement. These rules are hard-coded into the system. Supplier data, prices, and rankings are NEVER hard-coded.

## Product Matching Rules

### Material Matching
- User-specified material (e.g., 'nitrile') must match product material
- Acceptable variations: 'nitrile', 'nitrile rubber', 'NBR'
- Reject: latex if nitrile specified, vinyl if nitrile specified
- Case-insensitive matching

### Application Matching
- 'industrial safety' matches: 'industrial', 'safety', 'industrial use', 'heavy duty'
- Does NOT match: 'medical examination', 'food handling' (unless explicitly acceptable)

### Size Matching
- Standard sizes: XS, S, M, L, XL, XXL
- Normalize: 'medium' → 'M', 'large' → 'L', 'extra large' → 'XL'
- If user specifies size, product must match or be flagged as mismatch

## Quantity Rules

### MOQ Validation
- If supplier MOQ ≤ requested quantity → PASS
- If supplier MOQ > requested quantity → FLAG as 'requires negotiation'
- Never silently ignore MOQ exceeding requested quantity

## Price Normalization Rules

### Unit Price Conversion
All prices must be normalized to: **INR per piece (₹/piece)**

| Source Format | Conversion Rule |
|---|---|
| Per piece | Direct use |
| Per pair | Divide by 2 |
| Per box (N pieces) | Divide by N |
| Per carton (N pieces) | Divide by N |
| Total for Q quantity | Divide by Q |

### GST Handling
- GST rate for safety gloves: 18% (HSN 4015)
- NEVER silently mix GST-inclusive and GST-exclusive prices
- All comparisons must use the same tax basis
- If tax status unknown, mark as UNKNOWN and flag
- Store: price_value, price_basis (inclusive/exclusive/unknown), normalized_unit_price

### Currency
- Primary: INR (₹)
- If price in USD/other, convert using current exchange rate and flag conversion

## Supplier Classification Rules

| Classification | Criteria |
|---|---|
| MANUFACTURER | Independently verified production facility OR government registration as manufacturer |
| DISTRIBUTOR | Claims to distribute products from known manufacturers |
| WHOLESALER | Sells in bulk without manufacturing |
| TRADER | Intermediary, buys and resells |
| UNKNOWN | Insufficient information to classify |

### Important Rules
- A marketplace listing claiming 'manufacturer' is classified as CLAIMED, not MANUFACTURER
- Only upgrade to MANUFACTURER with corroborating evidence (GST registration type, factory verification, Udyam registration)
- Distributor/Wholesaler/Trader distinctions may be ambiguous — use best available evidence

## Evidence Status Rules

| Status | Definition | Upgrade Condition |
|---|---|---|
| UNKNOWN | No information | Any source found |
| CLAIMED | Single source, self-reported | - |
| DOCUMENTED | Found in official/authoritative source | Independent source confirms |
| CORROBORATED | Multiple independent sources agree | Government/official verification |
| VERIFIED | Government or legal verification obtained | - |
| CONFLICTING | Sources disagree | Requires manual review |

### Evidence Rules
- Never auto-upgrade from CLAIMED to VERIFIED
- CORROBORATED requires at least 2 independent sources
- CONFLICTING takes precedence over any other status when contradictions exist
- Timestamp all evidence; older evidence has lower weight

## Scoring Rules (BALANCED mode)

| Dimension | Weight | Scoring Method |
|---|---|---|
| Product Fit | 25 | Material match (10), Application match (8), Size match (7) |
| Price Competitiveness | 20 | Normalized unit price vs. user max price. Lower = better |
| Business Verification | 20 | Evidence quality of business identity (GSTIN, Udyam, etc.) |
| Delivery Feasibility | 15 | Distance-based estimate vs. deadline. Achievable = full score |
| MOQ Compatibility | 10 | MOQ ≤ quantity = full score. MOQ > quantity = partial |
| Evidence Quality | 10 | Overall evidence status distribution across all claims |

### Mode Adjustments
| Mode | Product Fit | Price | Verification | Delivery | MOQ | Evidence |
|---|---|---|---|---|---|---|
| COST_OPTIMIZED | 20 | 30 | 15 | 15 | 10 | 10 |
| BALANCED | 25 | 20 | 20 | 15 | 10 | 10 |
| RELIABILITY_FIRST | 20 | 15 | 30 | 15 | 10 | 10 |

## Confidence Calculation
Confidence is separate from score. It measures completeness and consistency of evidence.

Confidence = (fields_with_evidence / total_scored_fields) × consistency_factor

- consistency_factor = 1.0 if no contradictions, 0.7 if contradictions exist
- A supplier can have Score=91 but Confidence=68% if evidence is sparse

## Contradiction Rules
Detect and surface:
- Price discrepancy: marketplace price ≠ website price (>10% difference)
- Type mismatch: claims manufacturer but evidence suggests trader
- Address mismatch: registered address ≠ operational address
- Certification conflict: claims ISO but no ISO record found
- Temporal conflict: old price vs recent price (>30 days)
