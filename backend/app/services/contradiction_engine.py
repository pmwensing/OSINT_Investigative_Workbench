from app.models.entity import Claim
from app.models.contradiction import Contradiction


def detect_simple_contradictions(db, investigation_id):
    claims = db.query(Claim).all()
    created = []

    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            a = claims[i]
            b = claims[j]

            if a.entity_id != b.entity_id:
                continue

            if a.claim_type != b.claim_type:
                continue

            if a.value != b.value:
                c = Contradiction(
                    investigation_id=investigation_id,
                    claim_a_id=a.id,
                    claim_b_id=b.id,
                    rule="value_mismatch",
                    summary=f"Conflicting values: '{a.value}' vs '{b.value}'",
                    severity="medium"
                )
                db.add(c)
                created.append(c)

    db.commit()
    return created
