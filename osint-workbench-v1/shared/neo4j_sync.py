from neo4j import GraphDatabase
from api.core.config import settings

def sync_graph(nodes: list[dict], edges: list[dict]) -> None:
    driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        for node in nodes:
            session.run(
                "MERGE (n:Entity {id: $id}) SET n.label=$label, n.type=$type, n.confidence=$confidence",
                id=node["id"], label=node["label"], type=node["type"], confidence=node.get("confidence", 0.5),
            )
        for edge in edges:
            session.run(
                '''
                MATCH (a:Entity {id: $source}), (b:Entity {id: $target})
                MERGE (a)-[r:RELATED {id: $id}]->(b)
                SET r.label=$label, r.confidence=$confidence
                ''',
                id=edge["id"], source=edge["source"], target=edge["target"], label=edge["label"], confidence=edge.get("confidence", 0.5),
            )
    driver.close()
