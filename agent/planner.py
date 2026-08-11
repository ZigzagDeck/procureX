"""Research planner - generates search queries from requirements."""
class ResearchPlanner:
    def generate_search_queries(self, requirement):
        base = f"{requirement.material} {requirement.product_category.replace('_', ' ')}"
        queries = [f"{base} manufacturer India", f"{base} supplier {requirement.destination}", f"{base} wholesale price India"]
        if requirement.preferred_supplier_type:
            queries.append(f"{base} {requirement.preferred_supplier_type} India")
        queries.append(f"{base} IndiaMART")
        return queries
