"""MOQ validation."""
class MOQValidator:
    def validate(self, supplier_moq, requested_quantity):
        if supplier_moq is None: return {'status':'unknown','negotiation_required':False,'explanation':'MOQ not specified','score':0.5}
        if requested_quantity <= 0: return {'status':'invalid','negotiation_required':False,'explanation':'Invalid quantity','score':0.0}
        if supplier_moq <= requested_quantity: return {'status':'pass','negotiation_required':False,'explanation':f'MOQ ({supplier_moq:,}) <= requested ({requested_quantity:,})','score':1.0}
        ratio = requested_quantity / supplier_moq
        return {'status':'flag','negotiation_required':True,'explanation':f'MOQ ({supplier_moq:,}) > requested ({requested_quantity:,}). Negotiation required.','score':max(0.2, ratio)}
