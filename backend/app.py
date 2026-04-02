from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j_db import get_all_intents, update_answer, get_all_accounts, driver

app = Flask(__name__)
CORS(app)


@app.route("/api/intents", methods=["GET"])
def intents():
    return jsonify(get_all_intents())


@app.route("/api/update", methods=["POST"])
def update():
    data = request.json
    print("data", data)
    query = """
    MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {text:$intent})
    WHERE $entity IS NULL OR a.entity = $entity
    SET a.answer = $answer
    """
    print("query", query)
    with driver.session(database="test") as session:
        for item in data["entities"]:
            session.run(
                query,
                intent=data["intent"],
                entity=item.get("entity") or item.get("entity_name"),
                answer=item["answer"],
            )

    return {"status": "success"}


@app.route("/api/accounts", methods=["GET"])
def accounts():
    return jsonify(get_all_accounts())


# -------- LOGIN --------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    query = """
    MATCH (a:ADMIN {username:$username, password:$password})
    RETURN a.username AS user
    """

    with driver.session(database="test") as session:
        result = session.run(query, username=username, password=password)
        record = result.single()

        if record:
            return jsonify({"status": "success", "user": record["user"]})
        else:
            return jsonify({"status": "fail"}), 401


if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
