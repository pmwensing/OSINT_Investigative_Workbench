import httpx
from worker.connectors.base import BaseConnector
from api.core.config import settings

class ShodanConnector(BaseConnector):
    name = "shodan"

    def run(self, target_type: str, target_value: str) -> dict:
        if target_type != "ip":
            return {"connector": self.name, "entities": [], "observables": [], "relationships": [], "claims": [], "timeline_events": []}
        if not settings.shodan_api_key:
            raise RuntimeError("SHODAN_API_KEY not set")
        with httpx.Client(timeout=30) as client:
            resp = client.get(
                f"https://api.shodan.io/shodan/host/{target_value}",
                params={"key": settings.shodan_api_key},
            )
            resp.raise_for_status()
            data = resp.json()

        entities = []
        if data.get("org"):
            entities.append({"entity_type": "organization", "name": data["org"], "confidence": 0.85})

        observables = [{"observable_type": "ip", "value": target_value, "confidence": 0.99}]
        for host in data.get("hostnames", [])[:5]:
            observables.append({"observable_type": "hostname", "value": host, "confidence": 0.8})

        claims = [{"claim_type": "shodan_host_data", "subject": target_value, "value": str(data), "confidence": 0.8}]
        timeline = [{"title": "Shodan enrichment complete", "description": f"shodan lookup for {target_value}", "event_type": "enrichment"}]

        return {
            "connector": self.name,
            "raw": data,
            "entities": entities,
            "observables": observables,
            "relationships": [],
            "claims": claims,
            "timeline_events": timeline,
        }
