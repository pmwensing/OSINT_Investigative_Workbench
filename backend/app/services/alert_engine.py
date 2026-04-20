from app.models.review import Alert


def create_alert(db, investigation_id, alert_type, title, body=None, severity="medium", source_object_type=None, source_object_id=None):
    alert = Alert(
        investigation_id=investigation_id,
        alert_type=alert_type,
        severity=severity,
        title=title,
        body=body,
        source_object_type=source_object_type,
        source_object_id=source_object_id
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
