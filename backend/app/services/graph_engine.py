from collections import defaultdict, deque
from app.models.entity import Entity, Relationship


def build_graph_payload(db, investigation_id):
    entities = db.query(Entity).filter(Entity.investigation_id == investigation_id).all()
    relationships = db.query(Relationship).all()

    entity_ids = {e.id for e in entities}
    filtered_relationships = [
        r for r in relationships
        if r.source_entity_id in entity_ids and r.target_entity_id in entity_ids
    ]

    nodes = [
        {
            "id": str(e.id),
            "label": e.value,
            "entity_type": e.entity_type,
        }
        for e in entities
    ]

    edges = [
        {
            "id": str(r.id),
            "source": str(r.source_entity_id),
            "target": str(r.target_entity_id),
            "relationship_type": r.relationship_type,
        }
        for r in filtered_relationships
    ]

    return {"nodes": nodes, "edges": edges}


def build_adjacency(db, investigation_id):
    graph = build_graph_payload(db, investigation_id)
    adj = defaultdict(set)
    for edge in graph["edges"]:
        adj[edge["source"]].add(edge["target"])
        adj[edge["target"]].add(edge["source"])
    return graph, adj


def get_neighbors(db, investigation_id, entity_id):
    graph, adj = build_adjacency(db, investigation_id)
    node_map = {n["id"]: n for n in graph["nodes"]}
    neighbor_ids = sorted(adj.get(entity_id, set()))
    return {
        "entity": node_map.get(entity_id),
        "neighbors": [node_map[nid] for nid in neighbor_ids if nid in node_map],
    }


def shortest_path(db, investigation_id, source_id, target_id):
    graph, adj = build_adjacency(db, investigation_id)
    node_map = {n["id"]: n for n in graph["nodes"]}

    if source_id not in node_map or target_id not in node_map:
        return {"path": []}

    queue = deque([[source_id]])
    seen = {source_id}

    while queue:
        path = queue.popleft()
        current = path[-1]
        if current == target_id:
            return {
                "path": [node_map[nid] for nid in path]
            }
        for nxt in sorted(adj.get(current, set())):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(path + [nxt])

    return {"path": []}
