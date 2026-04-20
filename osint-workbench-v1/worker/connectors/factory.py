from worker.connectors.manual_import import ManualImportConnector
from worker.connectors.ipinfo import IPInfoConnector
from worker.connectors.shodan import ShodanConnector

CONNECTORS = {
    "manual_import": ManualImportConnector,
    "ipinfo": IPInfoConnector,
    "shodan": ShodanConnector,
}

def get_connector(name: str):
    try:
        return CONNECTORS[name]()
    except KeyError as exc:
        raise ValueError(f"Unsupported connector: {name}") from exc
