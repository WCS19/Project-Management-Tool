from typing import Any, Dict, Union, Tuple
from flask import request, jsonify, Flask, Response
from flask_jwt_extended import create_access_token
from backend.init import db, bcrypt
from backend.models import User


def register_auth_routes(app: Flask) -> None:
    @app.route("/register", methods=["POST", "OPTIONS"])
    def register() -> Union[Response, Tuple[Response, int]]:
        if request.method == "OPTIONS":
            return Response(status=204)

        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode(
            "utf-8"
        )
        new_user = User(
            username=data["username"], email=data["email"], password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"})

    @app.route("/login", methods=["POST", "OPTIONS"])
    def login() -> Union[Response, Tuple[Response, int]]:
        if request.method == "OPTIONS":
            return Response(status=204)

        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()
        if user and bcrypt.check_password_hash(user.password, data["password"]):
            access_token = create_access_token(
                identity={"id": user.id, "username": user.username, "email": user.email}
            )
            return jsonify({"access_token": access_token})
        else:
            return jsonify({"message": "Invalid credentials"}), 401
