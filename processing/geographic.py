"""Geographic analysis and delivery feasibility."""
import httpx
from models.geographic import Coordinates, RouteEstimate, DeliveryFeasibility

class GeographicAnalyzer:
    async def geocode(self, address):
        if not address: return None
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get('https://nominatim.openstreetmap.org/search',
                    params={'q': address + ', India', 'format': 'json', 'limit': 1},
                    headers={'User-Agent': 'ProcureX/1.0'}, timeout=10)
                data = resp.json()
                if data: return Coordinates(latitude=float(data[0]['lat']), longitude=float(data[0]['lon']), source='nominatim', confidence=0.7)
        except Exception: pass
        return None
    async def estimate_route(self, origin, dest):
        try:
            url = f'http://router.project-osrm.org/route/v1/driving/{origin.longitude},{origin.latitude};{dest.longitude},{dest.latitude}'
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params={'overview': 'false'}, timeout=10)
                data = resp.json()
                if data.get('routes'):
                    r = data['routes'][0]
                    return RouteEstimate(origin=origin, destination=dest, distance_km=round(r['distance']/1000,1), estimated_duration_hours=round(r['duration']/3600,1), route_source='osrm')
        except Exception: pass
        return None
    async def assess_delivery(self, supplier, destination_address, deadline_days=None):
        sloc = await self.geocode(supplier.city or supplier.address or '')
        dloc = await self.geocode(destination_address)
        route = None
        if sloc and dloc: route = await self.estimate_route(sloc, dloc)
        feasible, explanation = None, 'Unable to assess delivery feasibility'
        if route and deadline_days:
            transit = max(1, int(route.estimated_duration_hours / 8))
            feasible = transit <= deadline_days
            explanation = f'Estimated {transit} transit days vs {deadline_days} day deadline'
        return DeliveryFeasibility(supplier_id=supplier.id, supplier_location=sloc, destination=dloc, route=route, deadline_days=deadline_days, is_feasible=feasible, feasibility_explanation=explanation)
