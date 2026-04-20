import httpx
from worker.connectors.base import BaseConnector
from api.core.config import settings

class IPInfoConnector(BaseConnector):
    name = "ipinfo"

    def run(self, target_type: str, target_value: str) -> dict:
        if target_type != "ip":
            return {"connector": self.name, "entities": [], "observables": [], "relationships": [], "claims": [], "timeline_events": []}
        headers = {}
        if settings.ipinfo_api_key:
            headers["Authorization"] = f"Bearer {settings.ipinfo_api_key}"
        with httpx.Client(timeout=20) as client:
            resp = client.get(f"https://ipinfo.io/{target_value}/json", headers=headers)
            resp.raise_for_status()
            data = resp.json()

        entities = []
        org = data.get("org")
        if org:
            entities.append({"entity_type": "organization", "name": org, "confidence": 0.8})

        observables = [{"observable_type": "ip", "value": target_value, "confidence": 0.99}]
        if data.get("hostname"):
            observables.append({"observable_type": "hostname", "value": data["hostname"], "confidence": 0.8})
        if data.get("city"):
            observables.append({"observable_type": "city", "value": data["city"], "confidence": 0.6})

        claims = [{"claim_type": "ip_enrichment", "subject": target_value, "value": str(data), "confidence": 0.8}]
        timeline = [{"title": "IP enrichment complete", "description": f"ipinfo lookup for {target_value}", "event_type": "enrichment"}]

        return {
            "connector": self.name,
            "raw": data,
            "entities": entities,
            "observables": observables,
            "relationships": [],
            "claims": claims,
            "timeline_events": timeline,
        }
