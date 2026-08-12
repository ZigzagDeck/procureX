"""Main research pipeline orchestrator."""
from storage.session import ResearchSession, ResearchPhase
from acquisition.web_search import WebSearchSource
from extraction.supplier_extractor import SupplierExtractor
from processing.price_normalizer import PriceNormalizer
from processing.entity_resolver import EntityResolver
from processing.product_matcher import ProductMatcher
from processing.scoring import ScoringEngine
from processing.geographic import GeographicAnalyzer
from verification.evidence_collector import EvidenceCollector
from agent.budget_manager import BudgetManager
from agent.planner import ResearchPlanner
from x402.client import X402Client
from models.budget import ServiceType, PaymentStatus
from datetime import date

class ResearchOrchestrator:
    def __init__(self):
        self.search_source = WebSearchSource()
        self.extractor = SupplierExtractor()
        self.price_normalizer = PriceNormalizer()
        self.entity_resolver = EntityResolver()
        self.product_matcher = ProductMatcher()
        self.scoring_engine = ScoringEngine()
        self.geo_analyzer = GeographicAnalyzer()
        self.evidence_collector = EvidenceCollector()
        self.planner = ResearchPlanner()

    async def run_research(self, requirement, session):
        try:
            session.phase = ResearchPhase.SEARCHING
            session.add_log(ResearchPhase.SEARCHING, 'Starting supplier search...')
            queries = self.planner.generate_search_queries(requirement)
            all_results = []
            for q in queries:
                try:
                    results = await self.search_source.search(q, max_results=5)
                    all_results.extend(results)
                    session.sources_consulted.append(q)
                    session.add_log(ResearchPhase.SEARCHING, f'Query "{q}": {len(results)} results')
                except Exception as e:
                    session.add_log(ResearchPhase.SEARCHING, f'Search error: {e}')

            session.phase = ResearchPhase.EXTRACTING
            session.add_log(ResearchPhase.EXTRACTING, f'Extracting suppliers from {len(all_results)} results...')
            for result in all_results:
                try:
                    if not result.url: continue
                    fetched = await self.search_source.fetch(result.url)
                    if fetched.content:
                        prod_label = requirement.product_category.replace('_', ' ').title()
                        suppliers = self.extractor.extract_from_text(fetched.content, result.url, 'web_search', product_name=prod_label)
                        session.suppliers.extend(suppliers)
                        session.add_log(ResearchPhase.EXTRACTING, f'{result.url}: {len(suppliers)} suppliers')
                except Exception as e:
                    session.add_log(ResearchPhase.EXTRACTING, f'Extraction error: {e}')

            session.phase = ResearchPhase.NORMALIZING
            for s in session.suppliers:
                for p in s.products:
                    if p.price_value and not p.normalized_unit_price:
                        p.normalized_unit_price = self.price_normalizer.normalize_unit_price(p.price_value, p.price_basis, p.tax_status)
            session.add_log(ResearchPhase.NORMALIZING, 'Price normalization complete')

            session.phase = ResearchPhase.DEDUPLICATING
            dupes = self.entity_resolver.find_duplicates(session.suppliers)
            for id1, id2 in dupes:
                s1 = next((s for s in session.suppliers if s.id == id1), None)
                s2 = next((s for s in session.suppliers if s.id == id2), None)
                if s1 and s2: self.entity_resolver.merge_suppliers(s1, s2)
            active = [s for s in session.suppliers if not s.is_duplicate_of]
            session.add_log(ResearchPhase.DEDUPLICATING, f'{len(dupes)} duplicates merged. {len(active)} unique.')

            session.phase = ResearchPhase.VERIFYING
            for s in active:
                try:
                    s.evidence = await self.evidence_collector.collect_evidence(s)
                except Exception as e:
                    session.add_log(ResearchPhase.VERIFYING, f'Verification error for {s.name}: {e}')
            session.add_log(ResearchPhase.VERIFYING, 'Evidence collection complete')

            session.phase = ResearchPhase.GEO_ANALYZING
            deliveries = {}
            if requirement.destination:
                deadline_days = None
                if requirement.delivery_deadline:
                    deadline_days = (requirement.delivery_deadline - date.today()).days
                for s in active[:5]:
                    try:
                        d = await self.geo_analyzer.assess_delivery(s, requirement.destination, deadline_days)
                        deliveries[s.id] = d
                    except Exception: pass
            session.add_log(ResearchPhase.GEO_ANALYZING, f'Geographic analysis for {len(deliveries)} suppliers')

            session.phase = ResearchPhase.SCORING
            budget_mgr = BudgetManager(session.budget)
            x402_client = X402Client()
            
            for s in active:
                score = self.scoring_engine.score_supplier(s, requirement, delivery=deliveries.get(s.id), evidence_graph=s.evidence)
                
                # Check for Price Intelligence Information Gap on top candidates
                if score.total_score >= 45:
                    price_uncert = 0.3 if not s.products or not s.products[0].normalized_unit_price else 0.1
                    intel_decision = budget_mgr.should_purchase_price_intel(s, score, price_uncertainty=price_uncert)
                    
                    if intel_decision.should_purchase:
                        request_data = {
                            'product_category': requirement.product_category,
                            'material': requirement.material,
                            'quantity': requirement.quantity,
                            'region': requirement.destination
                        }
                        intel_data, tx = await x402_client.call_service(
                            ServiceType.PRICE_INTELLIGENCE, request_data, intel_decision
                        )
                        session.budget.record_purchase(tx)
                        if tx.status == PaymentStatus.COMPLETED and intel_data:
                            session.add_log(ResearchPhase.SCORING, f"Paid x402 Intel for {s.name}: ${intel_decision.cost}")
                            
                session.scores.append(score)
                
            session.scores.sort(key=lambda x: x.total_score, reverse=True)
            session.add_log(ResearchPhase.SCORING, f'Scored {len(session.scores)} suppliers with budget auditing complete.')

            session.phase = ResearchPhase.COMPLETED
            session.add_log(ResearchPhase.COMPLETED, 'Research complete!')
        except Exception as e:
            session.phase = ResearchPhase.FAILED
            session.error_message = str(e)
            session.add_log(ResearchPhase.FAILED, f'Research failed: {e}')
