from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tasks(db.Model):
    """Tasks model for working with tasks requests."""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
