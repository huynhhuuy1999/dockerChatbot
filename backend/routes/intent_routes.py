from flask import Blueprint, request, jsonify
from neo4j_db import get_all_intents, driver
from utils.response import response_success

# Khởi tạo Blueprint
intent_bp = Blueprint("intent_bp", __name__)


@intent_bp.route("/api/intents", methods=["GET"])
def intents():
    return jsonify(get_all_intents())


@intent_bp.route("/api/update", methods=["POST"])
def update():
    data = request.json
    print("data", data)
    query = """
    MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {text:$intent})
    WHERE $entity IS NULL OR a.entity = $entity
    SET a.answer = $answer
    """

    with driver.session(database="test") as session:
        for item in data["entities"]:
            session.run(
                query,
                intent=data["intent"],
                entity=item.get("entity") or item.get("entity_name"),
                answer=item["answer"],
            )

    return response_success()
