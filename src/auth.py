from flask import Blueprint



auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.route("/login", methods=["POST", 'GET'])
def login():
    return {"message":"Hello there"}


@auth.route(rule="/register", methods=["POST", "GET"])
def register():
    return {"message": "Hello World!"}


@auth.get("/me")
def me():
    return {"message": "Hello World!"}