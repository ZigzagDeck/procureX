"""Parse natural language procurement requirements into structured ProcurementRequirement."""
import re
import json
import os
from datetime import datetime, date, timedelta
from typing import Optional
from models.requirement import ProcurementRequirement, ProcurementMode

SIZE_MAP = {
    'extra small': 'XS', 'xs': 'XS', 'small': 'S', 's': 'S',
    'medium': 'M', 'med': 'M', 'm': 'M', 'large': 'L', 'l': 'L',
    'extra large': 'XL', 'xl': 'XL',
    'extra extra large': 'XXL', 'xxl': 'XXL', '2xl': 'XXL',
}
MATERIAL_MAP = {
    'nitrile rubber': 'nitrile', 'nbr': 'nitrile', 'nitrile': 'nitrile',
    'latex': 'latex', 'natural rubber': 'latex',
    'vinyl': 'vinyl', 'pvc': 'vinyl',
}

def parse_requirement(query: str) -> ProcurementRequirement:
    api_key = os.environ.get('GOOGLE_API_KEY', '')
    if api_key:
        try:
            data = _parse_with_llm(query, api_key)
            if data:
                return _validate_requirement(data, query)
        except Exception:
            pass
    data = _parse_with_rules(query)
    return _validate_requirement(data, query)

def _parse_with_llm(query: str, api_key: str) -> Optional[dict]:
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f'Extract procurement fields from: "{query}". Return JSON with: product_category, material, application, size, quantity, maximum_unit_price, currency, destination, delivery_days, preferred_supplier_type, certification_requirements, procurement_mode'
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        text = response.text.strip()
        if '```json' in text: text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text: text = text.split('```')[1].split('```')[0].strip()
        return json.loads(text)
    except Exception:
        return None

def _parse_with_rules(query: str) -> dict:
    q = query.lower()
        # Extract item category dynamically from search query
    cat_fallback = 'general_supplies'
    words = [w for w in q.split() if w not in ['find', 'need', 'require', 'order', 'buy', 'purchase', 'get', 'under', 'for', 'in', 'with']]
    if words:
        cat_fallback = '_'.join(words[:2])
        
    data = {
        'product_category': cat_fallback, 'material': '', 'application': 'industrial_safety',
        'size': None, 'quantity': 0, 'maximum_unit_price': None, 'currency': 'INR',
        'destination': '', 'delivery_days': None, 'preferred_supplier_type': None,
        'certification_requirements': [], 'procurement_mode': 'balanced',
    }
    for alias, canonical in MATERIAL_MAP.items():
        if alias in q:
            data['material'] = canonical
            break
    size_phrases = [
        ('extra extra large', 'XXL'), ('extra large', 'XL'), ('extra small', 'XS'),
        ('medium-sized', 'M'), ('medium sized', 'M'), ('medium', 'M'),
        ('small', 'S'), ('large', 'L'), ('xxl', 'XXL'), ('xl', 'XL'), ('xs', 'XS'),
    ]
    for phrase, size in size_phrases:
        if phrase in q:
            data['size'] = size
            break
    for pattern in [r'(\d{1,3}(?:,\d{3})+)\s*(?:pieces?|pcs?|pairs?|units?|nos?|gloves?)',
                    r'(\d+)\s*(?:pieces?|pcs?|pairs?|units?|nos?|gloves?)',
                    r'(?:find|need|require|order|buy|purchase|get)\s+(\d{1,3}(?:,\d{3})+)',
                    r'(?:find|need|require|order|buy|purchase|get)\s+(\d+)']:
        match = re.search(pattern, q)
        if match:
            data['quantity'] = int(match.group(1).replace(',', ''))
            break
    for pattern in [r'(?:under|below|max|maximum|budget|upto|up\s*to|within|less\s*than)\s*[\u20b9rs\.inr\s]*(\d+(?:\.\d+)?)',
                    r'[\u20b9rs\.inr\s]*(\d+(?:\.\d+)?)\s*(?:per\s*piece|/\s*piece|/\s*pc|per\s*unit|each)']:
        match = re.search(pattern, q)
        if match:
            data['maximum_unit_price'] = float(match.group(1))
            break
    for city in ['ghaziabad','delhi','mumbai','pune','bangalore','bengaluru','hyderabad','chennai','kolkata','noida','gurugram','ahmedabad','jaipur','lucknow','kanpur','indore','surat','nagpur','coimbatore','faridabad','ludhiana','agra','patna']:
        if city in q:
            data['destination'] = city.title()
            break
    dm = re.search(r'(?:within|in)\s+(\d+)\s*(?:days?|business\s*days?)', q)
    if dm: data['delivery_days'] = int(dm.group(1))
    if 'manufacturer' in q: data['preferred_supplier_type'] = 'manufacturer'
    elif 'distributor' in q: data['preferred_supplier_type'] = 'distributor'
    elif 'wholesaler' in q: data['preferred_supplier_type'] = 'wholesaler'
    if any(w in q for w in ['cheapest','lowest price','cost optimized','cheap']): data['procurement_mode'] = 'cost_optimized'
    elif any(w in q for w in ['reliable','trusted','verified','reliability']): data['procurement_mode'] = 'reliability_first'
    if 'glove' in q: data['product_category'] = 'safety_gloves'
    elif 'helmet' in q: data['product_category'] = 'safety_helmets'
    if 'medical' in q or 'examination' in q: data['application'] = 'medical'
    elif 'food' in q: data['application'] = 'food_handling'
    return data

def _normalize_size(size_str: str) -> Optional[str]:
    if not size_str: return None
    return SIZE_MAP.get(size_str.lower().strip(), size_str.upper().strip())

def _validate_requirement(data: dict, raw_query: str) -> ProcurementRequirement:
    size = data.get('size')
    if size: size = _normalize_size(size)
    material = data.get('material', '').lower().strip()
    material = MATERIAL_MAP.get(material, material)
    delivery_deadline = None
    dd = data.get('delivery_days')
    if dd and isinstance(dd, int): delivery_deadline = date.today() + timedelta(days=dd)
    mode_str = data.get('procurement_mode', 'balanced').lower()
    mode = ProcurementMode.BALANCED
    if mode_str == 'cost_optimized': mode = ProcurementMode.COST_OPTIMIZED
    elif mode_str == 'reliability_first': mode = ProcurementMode.RELIABILITY_FIRST
    return ProcurementRequirement(
        product_category=data.get('product_category', 'safety_gloves'),
        material=material or 'unknown', application=data.get('application', 'industrial_safety'),
        size=size, quantity=max(int(data.get('quantity', 0)), 0),
        maximum_unit_price=data.get('maximum_unit_price'), currency=data.get('currency', 'INR'),
        destination=data.get('destination', ''), delivery_deadline=delivery_deadline,
        preferred_supplier_type=data.get('preferred_supplier_type'),
        certification_requirements=data.get('certification_requirements', []),
        procurement_mode=mode, raw_query=raw_query, parsed_at=datetime.utcnow(),
    )
