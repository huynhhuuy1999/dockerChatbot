from flask import Blueprint, request, jsonify
from utils.security import hash_password, check_password
from neo4j_db import get_all_accounts, driver

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/api/accounts", methods=["GET"])
def accounts():
    return jsonify(get_all_accounts())


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    query = """
    MATCH (a:ADMIN {username:$username})
    RETURN a.password AS password
    """

    with driver.session(database="test") as session:

        resultUser = session.run(query, username=username)
        recordUser = resultUser.single()
        check = check_password(password, recordUser["password"])

        if check:
            return jsonify({"status": "success", "user": recordUser["password"]})
        else:
            return jsonify({"status": "fail"}), 401


@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    newPassword = hash_password(password).decode("utf-8")
    queryCheck = """
    MATCH (a:ADMIN {username:$username})
    RETURN a.username AS user
    """

    query = """
    MATCH (u:USERS)
    MERGE (u)-[:HAS_USER]->(a:ADMIN {username:$username, password:$password})
    RETURN a.username AS user, a.password AS password
    """

    with driver.session(database="test") as session:
        resultCheck = session.run(queryCheck, username=username)
        recordCheck = resultCheck.single()
        if recordCheck:
            return (
                jsonify({"status": "fail", "message": "Username already exists"}),
                400,
            )

        result = session.run(query, username=username, password=newPassword)
        record = result.single()

        if record:
            return jsonify({"status": "success", "user": record["user"]})
        else:
            return jsonify({"status": "fail"}), 401


@auth_bp.route("/api/update_account", methods=["POST"])
def update_account():
    data = request.json
    username = data.get("username")
    new_UserName = data.get("newUserName")
    new_password = data.get("password")
    isUpdatePassword = data.get("isUpdatePassword")
    if not new_password:
        return jsonify({"status": "fail", "message": "Password is required"}), 400
    if isUpdatePassword == True:
        hashed_password = hash_password(new_password).decode("utf-8")
    elif isUpdatePassword == False:
        hashed_password = new_password

    query = """
    MATCH (a:ADMIN {username:$username})
    SET a.password = $password, a.username = $new_UserName
    RETURN a.username AS user
    """

    with driver.session(database="test") as session:
        result = session.run(
            query,
            username=username,
            password=hashed_password,
            new_UserName=new_UserName,
        )
        record = result.single()

        if record:
            return jsonify({"status": "success", "user": record["user"]})
        else:
            return jsonify({"status": "fail"}), 401
