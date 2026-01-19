
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class AidResource:
    type: str
    quantity: int
    customs_note: str

@dataclass
class DeliveryRoute:
    destination: str
    risk_level: str # 'Safe', 'Borderline', 'High'
    conflicts_present: bool

class HumanitarianLogisticsAdvisor:
    """
    Day 95: Humanitarian Aid Logistics (Safe).
    Optimizes aid delivery while respecting local customs and 
    avoiding conflict zones and 'do-no-harm' violations.
    """
    def __init__(self):
        # Prohibited items by custom or law (Simulated)
        self.prohibited_by_region = {
            "Region_A": ["meat", "alcohol"],
            "Region_B": ["drones", "unencrypted_comms"],
            "Conflict_Zone_X": ["dual_use_tech", "fuel"]
        }

    def validate_aid_package(self, region: str, resources: List[AidResource]) -> List[str]:
        violations = []
        prohibited = self.prohibited_by_region.get(region, [])
        
        for res in resources:
            if res.type.lower() in prohibited:
                violations.append(f"Cultural/Legal Violation: '{res.type}' is prohibited in {region}. Reason: {res.customs_note}")
                
        return violations

    def evaluate_route(self, route: DeliveryRoute) -> Dict[str, Any]:
        risk_warnings = []
        
        if route.conflicts_present:
            risk_warnings.append("ROUTE ALERT: Active conflict detected in the delivery path.")
            
        if route.risk_level == "High":
            risk_warnings.append("DO-NO-HARM WARNING: Delivery to high-risk areas requires manual security audit to prevent aid diversion.")
            
        is_safe = len(risk_warnings) == 0
        return {
            "dest": route.destination,
            "is_safe": is_safe,
            "warnings": risk_warnings,
            "decision": "PROCEED" if is_safe else "DEFER_TO_HUMAN_SECURITY"
        }

    def optimize_aid(self, region: str, resources: List[AidResource], route: DeliveryRoute) -> Dict[str, Any]:
        viols = self.validate_aid_package(region, resources)
        route_eval = self.evaluate_route(route)
        
        overall_safety = (len(viols) == 0) and route_eval["is_safe"]
        
        return {
            "region": region,
            "overall_safety": overall_safety,
            "resource_violations": viols,
            "route_warnings": route_eval["warnings"],
            "status": "APPROVED" if overall_safety else "REVIEW_REQUIRED"
        }
