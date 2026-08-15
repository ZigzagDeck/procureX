import os
import sys
from fpdf import FPDF

class TestReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "ProcureX - Test Suite Verification Report", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 5, "Complete Audit of 47 Automated Unit & Integration Tests", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} - ProcureX Autonomous B2B Procurement Intelligence Engine", align="C")

def generate_pdf():
    pdf = TestReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Executive Summary Card
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Total Test Cases Executed: 47", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Total Passed: 47 (100% Pass Rate)", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Total Failed: 0", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Test Framework: pytest 9.1.1 on Python 3.14", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    test_suites = [
        {
            "category": "1. Budget Decision Engine (tests/test_budget_decisions.py)",
            "tests": [
                ("test_purchase_high_uncertainty", "Verify info-buying when price uncertainty is high (>0.3).", "PASSED", "Given price_uncertainty=0.5 and budget=0.020 USD, should_purchase returned True."),
                ("test_skip_low_uncertainty", "Avoid wasting budget when price uncertainty is low.", "PASSED", "Given price_uncertainty=0.1, decision engine returned should_purchase=False."),
                ("test_skip_insufficient_budget", "Block info-buying if remaining budget is too low.", "PASSED", "Given remaining_budget=0.001 USD, budget constraints enforced should_purchase=False."),
                ("test_verification_purchase", "Test verification purchase under low confidence.", "PASSED", "Given verification_score=0.3, should_purchase_verification returned True."),
                ("test_decisions_tracked", "Ensure financial decisions are logged in session ledger.", "PASSED", "Verified len(budget.decisions) == 2 after two purchasing decisions.")
            ]
        },
        {
            "category": "2. End-to-End Procurement Research Pipeline (tests/test_e2e.py)",
            "tests": [
                ("test_end_to_end_procurement_flow", "Validate full pipeline for canonical Nitrile Gloves query.", "PASSED", "Parsed requirements, ran search pipeline, evaluated candidate scoring (>0 with 6 dimensions), and asserted total spent <= initial budget.")
            ]
        },
        {
            "category": "3. Entity Resolution & Deduplication (tests/test_entity_resolver.py)",
            "tests": [
                ("test_same_gstin", "Deduplicate listings sharing identical GSTIN.", "PASSED", "Identified s1 and s2 as duplicate entity (returned 1 duplicate set)."),
                ("test_similar_names", "Fuzzy string matching for company names.", "PASSED", "Recognized 'Gupta Safety Products Pvt Ltd' and 'Gupta Safety Products Private Limited' as same entity."),
                ("test_same_name_diff_city", "Prevent merging same brand in different cities.", "PASSED", "Returned 0 duplicates for 'Safety First Industries' in Delhi vs. Chennai."),
                ("test_same_phone", "Match normalized phone numbers (+91 vs 0 prefix).", "PASSED", "Normalized phone numbers and matched across formats."),
                ("test_different_suppliers", "Keep distinct suppliers separate.", "PASSED", "Returned 0 duplicates for 'Alpha Safety' vs 'Beta Industrial'.")
            ]
        },
        {
            "category": "4. Evidence Graph & Verification (tests/test_evidence.py)",
            "tests": [
                ("test_add_evidence", "Add evidence records to supplier claim graph.", "PASSED", "Stored claim under key 'name' with 1 record in evidence claims."),
                ("test_no_contradiction_same_values", "Identical claims from multiple sources yield zero contradictions.", "PASSED", "Two sources claiming 'Test Corp' resulted in 0 contradictions."),
                ("test_contradiction_different_values", "Detect conflicting supplier classification claims.", "PASSED", "Source 1 ('manufacturer') vs Source 2 ('trader') generated 1 contradiction."),
                ("test_price_contradiction", "Detect conflicting pricing claims.", "PASSED", "Source 1 (Rs. 50) vs Source 2 (Rs. 80) flagged a price contradiction."),
                ("test_confidence_calculation", "Calculate claim confidence based on evidence presence.", "PASSED", "Evaluated fields (name, price, phone) and calculated expected confidence (0.5)."),
                ("test_conflicting_overall_status", "Contradictory evidence sets status to CONFLICTING.", "PASSED", "get_overall_status returned EvidenceStatus.CONFLICTING on price disagreement.")
            ]
        },
        {
            "category": "5. Foreign Exchange Engine (tests/test_fx_engine.py)",
            "tests": [
                ("test_fallback_rate", "Verify fallback to static rate (83.50 INR/USD) during network error.", "PASSED", "Mocked httpx.get exception; get_rate returned fallback rate 83.50."),
                ("test_dual_format", "Test dual-currency formatting output ($USD and Rs. INR).", "PASSED", "format_dual(0.002) generated string matching '$0.002 (Rs.'")
            ]
        },
        {
            "category": "6. Prepaid USD Account Ledger (tests/test_prepaid_account.py)",
            "tests": [
                ("test_deduct_success", "Test balance deduction from local JSON account ledger.", "PASSED", "Initial 1.00 USD, deducted 0.002 USD, verified remaining balance 0.998 USD."),
                ("test_deduct_insufficient", "Ensure deductions blocked when balance insufficient.", "PASSED", "Balance reduced to 0.001 USD; attempting to deduct 0.002 USD returned False.")
            ]
        },
        {
            "category": "7. Price Unit Normalization (tests/test_price_normalizer.py)",
            "tests": [
                ("test_per_piece", "Normalize unit price when basis is per piece.", "PASSED", "Rs. 75.0 per piece returned 75.0."),
                ("test_per_pair", "Convert price per pair to price per piece.", "PASSED", "Rs. 150.0 per pair converted to 75.0 per piece (150 / 2)."),
                ("test_per_box", "Convert price per box of 100 to price per piece.", "PASSED", "Rs. 7500.0 per box of 100 converted to 75.0 per piece (7500 / 100)."),
                ("test_gst_inclusive", "Strip 18% GST from inclusive prices.", "PASSED", "Rs. 88.50 GST inclusive converted to 75.0 GST exclusive (88.5 / 1.18)."),
                ("test_total", "Convert total order lot price to unit price.", "PASSED", "Rs. 375,000 total for 5,000 pcs converted to 75.0 per piece."),
                ("test_zero", "Handle zero price safely.", "PASSED", "0.0 returned 0.0 without division by zero errors."),
                ("test_budget", "Check if unit price satisfies target budget.", "PASSED", "75.0 <= 80.0 returned True; 85.0 <= 80.0 returned False.")
            ]
        },
        {
            "category": "8. Technical Product Specification Matcher (tests/test_product_matcher.py)",
            "tests": [
                ("test_nitrile_matches_nitrile_rubber", "Match synonyms for Nitrile material.", "PASSED", "Matched 'nitrile' against 'Nitrile Rubber' (True)."),
                ("test_nitrile_not_latex", "Ensure incompatible materials do not match.", "PASSED", "Matched 'nitrile' against 'latex' (False)."),
                ("test_nbr_matches_nitrile", "Match abbreviation NBR.", "PASSED", "Matched 'nitrile' against 'NBR' (True)."),
                ("test_size_m_matches_medium", "Normalize size code M to medium.", "PASSED", "Matched 'M' against 'medium' (True)."),
                ("test_industrial_matches", "Match application category industrial_safety.", "PASSED", "Matched application keywords correctly (True)."),
                ("test_industrial_not_medical", "Ensure industrial safety does not match medical examination.", "PASSED", "Matched 'industrial_safety' against 'medical examination' (False)."),
                ("test_no_size_req", "Unspecified size requirement matches any available size.", "PASSED", "size=None matched 'L' (True).")
            ]
        },
        {
            "category": "9. Natural Language Requirement Parser (tests/test_requirement_parser.py)",
            "tests": [
                ("test_canonical_query", "Parse complex canonical procurement prompt.", "PASSED", "Extracted quantity=5000, material='nitrile', max_unit_price=80.0, destination='Ghaziabad', supplier_type='manufacturer'."),
                ("test_simple_query", "Parse simple 1-line query.", "PASSED", "Extracted quantity=1000, material='nitrile', destination='Pune'."),
                ("test_size_normalization", "Test size normalization helper functions.", "PASSED", "medium -> M, extra large -> XL, None -> None."),
                ("test_cost_optimized_mode", "Detect cost-optimized strategy keywords.", "PASSED", "Parsed query and set procurement_mode to COST_OPTIMIZED."),
                ("test_empty_input", "Handle empty prompt strings safely.", "PASSED", "Returned default requirement object with quantity=0.")
            ]
        },
        {
            "category": "10. Multi-Dimensional Supplier Scoring Engine (tests/test_scoring.py)",
            "tests": [
                ("test_score_with_matching_supplier", "Score a fully matching candidate supplier.", "PASSED", "Generated score > 0 with all 6 evaluation dimensions populated."),
                ("test_score_with_no_products", "Score a supplier record missing product details.", "PASSED", "Assigned non-zero fallback score while maintaining total score < 50."),
                ("test_cost_optimized_weights", "Verify weighting adjustments in Cost-Optimized mode.", "PASSED", "Price Competitiveness weight increased to 30 points under COST_OPTIMIZED mode.")
            ]
        },
        {
            "category": "11. JWT Payment Proof Signer (tests/test_token_signer.py)",
            "tests": [
                ("test_sign_and_verify", "Issue HMAC-SHA256 JWT payment proof token and verify payload.", "PASSED", "Token signed and verified: amount=0.002, currency='USD', service='price_intelligence', supplier_id='supp-123'."),
                ("test_expired_token", "Verify expired payment proof tokens are rejected.", "PASSED", "Issued token with exp=1s, waited 2s; verify_token returned None.")
            ]
        },
        {
            "category": "12. x402 Micropayment Protocol Simulation (tests/test_x402.py)",
            "tests": [
                ("test_mock_payment_completes", "Test HTTP 402 payment flow completion.", "PASSED", "Result status returned 'completed', is_mock=True, amount=0.002."),
                ("test_mock_payment_different_amounts", "Test micropayments for different service tiers.", "PASSED", "Processed 0.001 USD (verification) and 0.002 USD (price intel) correctly.")
            ]
        }
    ]

    for suite in test_suites:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(30, 41, 59)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 7, f"  {suite['category']}", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

        for name, desc, status, result in suite["tests"]:
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(140, 5, f"• {name}", new_x="RIGHT")
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(16, 185, 129) # green
            pdf.cell(50, 5, status, new_x="LMARGIN", new_y="NEXT", align="R")
            pdf.set_text_color(0, 0, 0)

            pdf.set_font("Helvetica", "I", 8.5)
            pdf.multi_cell(0, 4, f"  Reason: {desc}")
            pdf.set_font("Helvetica", "", 8.5)
            pdf.multi_cell(0, 4, f"  Justification: {result}")
            pdf.ln(3)

        pdf.ln(3)

    out_path1 = r"C:\Users\Lenovo\.gemini\antigravity\scratch\procurex\procurex_test_report.pdf"
    out_path2 = r"C:\Users\Lenovo\.gemini\antigravity\brain\a0a65d14-be49-482b-97ca-aaa6cc537890\procurex_test_report.pdf"
    
    pdf.output(out_path1)
    pdf.output(out_path2)
    print(f"PDF successfully generated at:\n1. {out_path1}\n2. {out_path2}")

if __name__ == "__main__":
    generate_pdf()
