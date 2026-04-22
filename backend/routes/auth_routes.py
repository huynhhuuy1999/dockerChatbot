from flask import Blueprint, request, jsonify
from utils.security import hash_password, check_password
from neo4j_db import get_all_accounts, driver
from utils.response import response_success, response_error
from neo4j.exceptions import ConstraintError
from utils.constants import STATUS

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
    try:
        with driver.session(database="test") as session:

            resultUser = session.run(query, username=username)
            recordUser = resultUser.single()
            check = check_password(password, recordUser["password"])

            if check:
                return response_success(user=recordUser["password"])
            else:
                return response_error(
                    error="Sai mật khẩu", status_code=STATUS["UNAUTHORIZED"]
                )
    except:
        return response_error(error="Lỗi đăng nhập", status_code=STATUS["UNAUTHORIZED"])


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
            return response_error(
                error="Username đã tồn tại", status_code=STATUS["BAD_REQUEST"]
            )

        result = session.run(query, username=username, password=newPassword)
        record = result.single()

        if record:
            return response_success(user=record["user"])
        else:
            return response_error(
                error="Đăng ký thất bại", status_code=STATUS["BAD_REQUEST"]
            )


@auth_bp.route("/api/update_account", methods=["POST"])
def update_account():
    data = request.json
    username = data.get("username")
    new_UserName = data.get("newUserName")
    new_password = data.get("password")
    isUpdatePassword = data.get("isUpdatePassword")
    if not new_password:
        return response_error(
            error="Mật khẩu không được trống", status_code=STATUS["BAD_REQUEST"]
        )
    if isUpdatePassword == True:
        hashed_password = hash_password(new_password).decode("utf-8")
    elif isUpdatePassword == False:
        hashed_password = new_password

    query = """
    MATCH (a:ADMIN {username:$username})
    SET a.password = $password, a.username = $new_UserName
    RETURN a.username AS user
    """
    try:
        with driver.session(database="test") as session:
            result = session.run(
                query,
                username=username,
                password=hashed_password,
                new_UserName=new_UserName,
            )
            record = result.single()

            if record:
                return response_success(user=record["user"])
            else:
                return response_error(
                    error="Cập nhật tài khoản thất bại",
                    status_code=STATUS["BAD_REQUEST"],
                )
    except ConstraintError:
        return response_error(
            error="Username đã tồn tại", status_code=STATUS["BAD_REQUEST"]
        )
