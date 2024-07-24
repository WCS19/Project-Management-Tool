from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Task
from backend.init import db
from backend.auth import register_auth_routes

def register_routes(app):

    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to the API'})

    @app.route('/tasks', methods=['GET'])
    @jwt_required()
    def get_tasks():
        user_identity = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_identity['id']).all()
        return jsonify([task.serialize() for task in tasks])

    @app.route('/tasks', methods=['POST'])
    @jwt_required()
    def create_task():
        user_identity = get_jwt_identity()
        data = request.get_json()
        new_task = Task(title=data['title'], description=data['description'], user_id=user_identity['id'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.serialize()), 201

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    @jwt_required()
    def update_task(task_id):
        task = Task.query.get(task_id)
        data = request.get_json()
        task.title = data['title']
        task.description = data['description']
        db.session.commit()
        return jsonify(task.serialize())

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(task_id):
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})

    # Register auth routes
    register_auth_routes(app)

