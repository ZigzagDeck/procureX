"""Product matching against procurement requirements."""
class ProductMatcher:
    MATERIAL_ALIASES = {'nitrile': ['nitrile','nitrile rubber','nbr'], 'latex': ['latex','natural rubber','nr'], 'vinyl': ['vinyl','pvc','polyvinyl chloride']}
    SIZE_NORMALIZE = {'extra small':'XS','xs':'XS','small':'S','s':'S','medium':'M','med':'M','m':'M','large':'L','l':'L','extra large':'XL','xl':'XL','extra extra large':'XXL','xxl':'XXL'}
    APPLICATION_GROUPS = {'industrial_safety': ['industrial','safety','industrial use','heavy duty','industrial safety','construction','manufacturing'], 'medical': ['medical','examination','clinical','hospital','surgical'], 'food': ['food','food handling','food processing','food grade']}
    def match_material(self, required, product_material):
        req, prod = required.lower().strip(), product_material.lower().strip()
        if not req or not prod: return (False, 'Material information missing')
        if req == prod: return (True, f'Material match: {req}')
        for canonical, aliases in self.MATERIAL_ALIASES.items():
            if (req in aliases or req == canonical) and (prod in aliases or prod == canonical): return (True, f'Material match: {prod} is {canonical}')
        return (False, f"Material mismatch: required '{req}', found '{prod}'")
    def match_application(self, required, product_application):
        req, prod = required.lower().strip(), product_application.lower().strip()
        if not req or not prod: return (False, 'Application information missing')
        if req == prod: return (True, f'Application match: {req}')
        for group, terms in self.APPLICATION_GROUPS.items():
            if (req in terms or req == group) and (prod in terms or prod == group): return (True, f"Application match: both in '{group}'")
        return (False, f"Application mismatch: required '{req}', found '{prod}'")
    def match_size(self, required, product_size):
        if not required: return (True, 'No size requirement specified')
        rn = self.SIZE_NORMALIZE.get(required.lower().strip(), required.upper().strip())
        pn = self.SIZE_NORMALIZE.get(product_size.lower().strip(), product_size.upper().strip()) if product_size else ''
        if not pn: return (False, 'Product size not specified')
        if rn == pn: return (True, f'Size match: {rn}')
        return (False, f"Size mismatch: required '{rn}', found '{pn}'")
    def match_product(self, requirement, product):
        mm, me = self.match_material(requirement.material, product.material)
        am, ae = self.match_application(requirement.application, product.application)
        sm, se = self.match_size(requirement.size, product.size)
        return {'match': mm and am and sm, 'material_match': mm, 'application_match': am, 'size_match': sm, 'explanations': [me, ae, se]}
