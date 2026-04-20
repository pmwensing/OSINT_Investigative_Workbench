from worker.connectors.base import BaseConnector

class ManualImportConnector(BaseConnector):
    name = "manual_import"

    def run(self, target_type: str, target_value: str) -> dict:
        return {
            "connector": self.name,
            "target_type": target_type,
            "target_value": target_value,
            "entities": [
                {"entity_type": "account", "name": target_value, "confidence": 0.95},
            ],
            "observables": [
                {"observable_type": target_type, "value": target_value, "confidence": 0.99},
            ],
            "relationships": [],
            "claims": [
                {"claim_type": "observed_target", "subject": target_value, "value": f"Target {target_value} manually imported.", "confidence": 0.95}
            ],
            "timeline_events": [
                {"title": "Target imported", "description": f"Manual import for {target_value}", "event_type": "import"}
            ],
        }
