import pytest
from sqlalchemy import select

from app.main import create_app
from app.tasks.models import db, Tasks


@pytest.fixture()
def app():
    """Flask test app"""
    # Create and configure the app for testing
    app = create_app(mode_test=True)
    # Settings for dev and testing environment
    app.config['TESTING'] = True
    yield app
    with app.app_context():
        db.session.close()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Flask test client"""
    return app.test_client()


@pytest.fixture()
def create_tasks(app):
    """Create tasks."""
    with app.app_context():
        for task in range(5):
            db.session.add(Tasks(title=f'Test task{task}', description=f'Test description{task}'))
        db.session.commit()


@pytest.fixture()
def get_task(app):
    """Get task by id."""
    with app.app_context():
        return db.session.get(Tasks, 1)


@pytest.fixture()
def get_all_tasks(app):
    """Get all tasks."""
    with app.app_context():
        return db.session.execute(select(Tasks)).fetchall()


@pytest.fixture()
def get_last_task(app):
    """Get last task."""
    with app.app_context():
        return db.session.execute(select(Tasks).order_by(Tasks.id.desc())).fetchone()
