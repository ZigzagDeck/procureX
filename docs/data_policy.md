# ProcureX — Data Access Policy

## Core Principle
The system must NOT use fabricated supplier data as its primary research result. All supplier information must originate from real external sources wherever technically and legally permissible.

## Source Hierarchy (Priority Order)

1. **Official Government Sources**
   - GST Portal
   - Udyam/MSME Registry
   - GeM (Government e-Marketplace)

2. **Supplier-Owned Sources**
   - Official company websites
   - Direct contact information published by the supplier

3. **Established Marketplaces**
   - IndiaMART
   - TradeIndia
   - Alibaba India
   - JustDial B2B

4. **Other Reputable Public Sources**
   - Industry directories
   - Trade association listings
   - Reputable news articles and press releases

---

## Access Rules

### MUST Respect
- **robots.txt Directives**: Honor crawl-delay and user-agent rules specified in `robots.txt`.
- **Terms of Service**: Comply with terms of service for all queried external platforms.
- **Rate Limits**: Enforce a minimum 2-second delay between consecutive requests to the same domain.
- **Authentication Boundaries**: Never bypass login walls, paywalls, or gated forms.
- **API Restrictions & Quotas**: Observe rate limits, key constraints, and usage quotas.
- **Personal Data Protection Laws**: Comply strictly with applicable legislation, including the Digital Personal Data Protection (DPDP) Act 2023.

### MUST NOT
- Build or deploy aggressive, evasive, or distributed scraping systems.
- Bypass CAPTCHAs, anti-bot mechanisms, or IP-blocking controls.
- Use unauthorized, leaked, or stolen credentials.
- Store personal data beyond the active research session lifecycle.
- Fabricate supplier identities, product prices, user reviews, or compliance certifications.

---

## Source Adapter Interface

Every data source in ProcureX must be accessed strictly through the `ResearchSource` abstraction:

```python
class ResearchSource(ABC):
    @abstractmethod
    def search(self, query: str) -> list[ResultReference]:
        """Search the source for matching entries and return reference objects."""
        pass

    @abstractmethod
    def fetch(self, reference: ResultReference) -> RawContent:
        """Fetch raw content for a specific search reference."""
        pass

    @abstractmethod
    def extract(self, content: RawContent) -> StructuredSupplierData:
        """Extract structured supplier data and provenance from raw content."""
        pass
```

> [!IMPORTANT]
> **Pluggable Source Stub Rule**: If a source does not provide legitimate, compliant automated access, developers MUST create a pluggable source interface (stub) returning mock/not-available responses rather than bypassing security or legal restrictions.

---

## Permitted Sources for MVP

| Source | Type | Access Method | Notes |
|---|---|---|---|
| **Google Search** | Web Search | SerpAPI / Official Search API | Used to discover supplier websites and public marketplace listings |
| **IndiaMART** | Marketplace | Web search results (public listings only) | No direct public API; use search engine results to locate public product pages |
| **TradeIndia** | Marketplace | Public product pages | Crawled respecting `robots.txt` and ToS |
| **Company Websites** | Direct | HTTP GET | Directly fetched respecting domain `robots.txt` |
| **GST Portal** | Government | Third-party API (sandbox/mock for MVP) | Verified for GSTIN validation and status |
| **Udyam Portal** | Government | Third-party API (sandbox/mock for MVP) | Verified for MSME classification and registration details |
| **Google Maps / Nominatim** | Geocoding | REST API | Geolocation coordinates and distance calculation |

---

## Raw Data Retention

For every acquired document or web page, the system must retain:

- **Source Identifier**: Unique ID of the source adapter (e.g., `indiamart_search`, `gst_api`)
- **URL**: Complete target URL retrieved
- **Retrieval Timestamp**: ISO 8601 UTC timestamp (e.g., `2026-08-10T17:50:32Z`)
- **Raw Content**: Exact HTTP response payload (where permitted by ToS and privacy policies)
- **Content Hash**: Cryptographic hash (SHA-256) of raw content for immutability verification
- **Extraction Metadata**: Parser version, processing latency, and execution flags

*Rule: Never discard raw provenance after structured field extraction.*

---

## Provenance Requirements

Every extracted field in the domain model must carry explicit provenance metadata:

```json
{
  "field_name": "gstin_status",
  "value": "ACTIVE",
  "source": "gst_portal_adapter",
  "url": "https://api.gst.gov.in/v1/search/27AAAAA0000A1Z5",
  "retrieved_at": "2026-08-10T17:50:32Z",
  "confidence": 1.0,
  "evidence_status": "VERIFIED"
}
```

### Supported `evidence_status` Enum Values:
1. `CLAIMED`: Asserted by supplier on their own website/listing without independent confirmation.
2. `DOCUMENTED`: Supported by official document uploads or web artifacts.
3. `CORROBORATED`: Confirmed independently by multiple non-government public sources.
4. `VERIFIED`: Formally verified against an authoritative government or primary register (e.g., GST portal).
5. `CONFLICTING`: Discrepancy observed across different sources.
6. `UNKNOWN`: Insufficient evidence or unverified field.

---

## Failure Handling

The system must continue operation gracefully under external failure conditions:

- **HTTP Errors (4xx, 5xx)**: Log failure, flag source as unavailable for the session, and continue with remaining sources.
- **Parsing / Extraction Failures**: Record partial extraction result with non-parsed fields set to `UNKNOWN`.
- **Incomplete Supplier Info**: Mark missing attributes as `UNAVAILABLE` rather than inferring or hallucinating values.
- **Geocoding Unavailable**: Fall back to state/city level proximity estimation.
- **Government Verification Down**: Set verification status to `UNCHECKED` or `NOT_VERIFIED` with detailed failure log.
- **Rate Limit Exceeded**: Trigger exponential backoff; if persistent, skip source without throwing unhandled exceptions.

> [!CAUTION]
> Under no circumstances should error recovery logic fill missing or failed fields with fabricated default values. Use `UNKNOWN`, `UNAVAILABLE`, or `NOT_VERIFIED`.

---

## Mock Data Policy

- **Clear Separation**: Mock/development data must be strictly segregated from production/real research data pipelines.
- **Explicit Labeling**: All mock sources must return `source: "MOCK"` and `evidence_status: "UNKNOWN"` in provenance.
- **Contamination Prevention**: Production research runs must explicitly disable mock adapters via environment configuration (`ALLOW_MOCK_SOURCES=False`).
- **Test Fixtures**: Development and CI unit tests must use deterministic synthetic fixtures mirroring real data schemas.

---

## Security

- **Secret Management**: All API keys, tokens, and database passwords must be loaded strictly via environment variables or Streamlit secrets (`.streamlit/secrets.toml`).
- **No Source Code Secrets**: No hardcoded API keys, passwords, or personal access tokens in code repositories or documentation.
- **Version Control Controls**: Git repositories must ignore `.env`, `secrets.toml`, and raw data dumps via `.gitignore`.
- **Safe Degradation**: Missing API credentials must result in graceful degradation (disabling that specific adapter with a user notification) rather than application crashes.
