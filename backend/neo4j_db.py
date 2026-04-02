from neo4j import GraphDatabase

URI = "bolt://neo4j:7687"
USER = "neo4j"
PASSWORD = "123456789"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def get_all_intents():
    query = """
    MATCH (i:Intent)
    OPTIONAL MATCH (a:Answer)-[:BELONG_TO]->(i)
    OPTIONAL MATCH (i)-[:HAS_ENTITY]->(e:Entity)
    WHERE e.name = a.entity
    RETURN i.text AS intent,
           collect({
               entity_name: a.entity,
               entity_text: e.text,
               answer: a.answer
           }) AS entities
    """
    with driver.session(database="test") as session:
        results = session.run(query)
        return [dict(r) for r in results]


def get_all_accounts():
    query = """
    MATCH (a:ADMIN)
    RETURN a AS account
    """
    with driver.session(database="test") as session:
        results = session.run(query)
        return [dict(r["account"]) for r in results]


def update_answer(intent_text, new_answer):
    query = """
    MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {text: $intent_text})
    SET a.answer = $new_answer
    """
    with driver.session(database="test") as session:
        session.run(query, intent_text=intent_text, new_answer=new_answer)
