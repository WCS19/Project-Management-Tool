from backend.init import db
from typing import Dict, Any, Optional


class User(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    tasks = db.relationship("Task", order_by="Task.id", back_populates="user")

    def serialize(self) -> Dict[str, Any]:
        return {"id": self.id, "username": self.username, "email": self.email}


class Task(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))  # Optional[str]
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="tasks")

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
        }
