from app.tasks.views import TasksView
from app.tasks.models import Tasks


def register_api_tasks(app):
    """Register routes for tasks."""
    tasks_view = TasksView.as_view('tasks', Tasks)
    app.add_url_rule('/tasks', view_func=tasks_view, methods=['GET', 'POST'])
    app.add_url_rule('/tasks/<int:pk>', view_func=tasks_view, methods=['GET', 'PUT', 'DELETE'])
