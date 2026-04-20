from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class ExhibitIndexRow:
    exhibit_id: str
    title: str
    source_id: str
    source_path: str
    category: str
    sha256: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DuplicateGroupRow:
    duplicate_group_id: str
    match_type: str
    member_source_ids: str
    preferred_source_id: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)
