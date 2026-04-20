import hashlib
from app.models.provenance import ProvenanceRecord, ClaimCitation


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def create_provenance(db, investigation_id, artifact_id=None, record_type="artifact", content="", locator=None, notes=None, derived_from_id=None):
    h = hash_content(content or "")

    record = ProvenanceRecord(
        investigation_id=investigation_id,
        artifact_id=artifact_id,
        record_type=record_type,
        locator=locator,
        content_hash=h,
        notes=notes,
        derived_from_id=derived_from_id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def cite_claim(db, claim_id, artifact_id=None, provenance_id=None, locator=None, excerpt=None, justification=None):
    citation = ClaimCitation(
        claim_id=claim_id,
        artifact_id=artifact_id,
        provenance_id=provenance_id,
        locator=locator,
        excerpt=excerpt,
        justification=justification,
    )
    db.add(citation)
    db.commit()
    db.refresh(citation)
    return citation
