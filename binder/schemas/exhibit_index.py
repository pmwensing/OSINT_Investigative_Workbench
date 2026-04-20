from dataclasses import dataclass, asdict

@dataclass
class ExhibitIndexRow:
    exhibit_id: str
    title: str
    source_path: str
    category: str
    sha256: str

    def to_dict(self):
        return asdict(self)
