import hashlib
from app.models.freeze import FreezeSnapshot, AuditEvent


def compute_manifest_hash(db, investigation_id):
    # simple hash over key tables (expand later)
    data = f"investigation:{investigation_id}"
    return hashlib.sha256(data.encode()).hexdigest()


def freeze_investigation(db, investigation_id):
    manifest_hash = compute_manifest_hash(db, investigation_id)

    snapshot = FreezeSnapshot(
        investigation_id=investigation_id,
        manifest_hash=manifest_hash,
        audit_log=f"Freeze created with hash {manifest_hash}"
    )
    db.add(snapshot)

    audit = AuditEvent(
        investigation_id=investigation_id,
        event_type="freeze",
        details=f"Investigation frozen with hash {manifest_hash}"
    )
    db.add(audit)

    db.commit()
    db.refresh(snapshot)
    return snapshot


def log_event(db, investigation_id, event_type, details=None, object_type=None, object_id=None):
    audit = AuditEvent(
        investigation_id=investigation_id,
        event_type=event_type,
        object_type=object_type,
        object_id=object_id,
        details=details
    )
    db.add(audit)
    db.commit()
    return audit
