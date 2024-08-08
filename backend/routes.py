from flask import request, jsonify, Response, Flask
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Task
from backend.init import db
from backend.auth import register_auth_routes
from typing import Any, Tuple, Callable, TypeVar, cast
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def typed_jwt_required(func: Callable[P, R]) -> Callable[P, R]:
    """
    A decorator that ensures the route requires a valid JSON Web Token (JWT).

    This function wraps the `jwt_required` decorator from `flask_jwt_extended`,
    preserving the original function's type annotations using `ParamSpec` and `TypeVar`.
    It ensures that the route can only be accessed if a valid JWT is provided.

    Args:
        func (Callable[P, R]): The route handler function that requires JWT validation.

    Returns:
        Callable[P, R]: The route handler function wrapped with JWT validation.
    """
    return cast(Callable[P, R], jwt_required()(func))


def register_routes(app: Flask) -> None:
    @app.route("/")
    def index() -> Response:
        return jsonify({"message": "Welcome to the API"})

    @app.route("/tasks", methods=["GET"])
    @typed_jwt_required
    def get_tasks() -> Response:
        user_identity = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_identity["id"]).all()
        return jsonify([task.serialize() for task in tasks])

    @app.route("/tasks", methods=["POST"])
    @typed_jwt_required
    def create_task() -> Tuple[Response, int]:
        user_identity = get_jwt_identity()
        data = request.get_json()
        new_task = Task(
            title=data["title"],
            description=data["description"],
            user_id=user_identity["id"],
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.serialize()), 201

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    @typed_jwt_required
    def update_task(task_id: int) -> Response:
        task = Task.query.get(task_id)
        data = request.get_json()
        task.title = data["title"]
        task.description = data["description"]
        db.session.commit()
        return jsonify(task.serialize())

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    @typed_jwt_required
    def delete_task(task_id: int) -> Response:
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})

    # Register auth routes
    register_auth_routes(app)
