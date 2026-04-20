from abc import ABC, abstractmethod

class BaseConnector(ABC):
    name: str

    @abstractmethod
    def run(self, target_type: str, target_value: str) -> dict:
        raise NotImplementedError
