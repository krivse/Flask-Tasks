from datetime import datetime
from http import HTTPStatus

import pytest
from sqlalchemy import select


@pytest.mark.usefixtures('create_tasks')
class TestTasks:
    """Tests for tasks routes."""
    def test_get_list_tasks(self, client, get_all_tasks):
        """Test get all tasks

        :arg client: Flask test client
        :arg get_all_tasks: fixture to get all tasks."""
        response = client.get('/tasks')
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data) == len(get_all_tasks)

    def test_get_tasks(self, client, get_task):
        """Test get task by id

        :arg client: Flask test client
        :arg get_task: fixture to get task by id."""
        response = client.get('/tasks/1')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['title'] == get_task.title
        assert json_data['description'] == get_task.description
        assert json_data['id'] == get_task.id
        assert datetime.fromisoformat(json_data['created_at']) == get_task.created_at
        assert json_data['updated_at'] == get_task.updated_at

    def test_get_tasks_not_found(self, client):
        """Test get task not found

        :arg client: Flask test client."""
        response = client.get('/tasks/999')
        assert response.status_code == 404
        assert response.get_json() == {'error': 'Task with this id 999 not found'}

    @pytest.mark.parametrize(
        'body, expected_code, expected_message',
        [
            ({'title': 'Test task', 'description': 'Test description'}, HTTPStatus.CREATED, None),
            ({'title': 'Test task', 'description': None}, HTTPStatus.CREATED, None),
            ({'title': None, 'description': 'Test description'}, HTTPStatus.BAD_REQUEST,
             {'error': 'Input should be a valid string: title'}),
            ({'title': 'Test task', 'description': 1}, HTTPStatus.BAD_REQUEST,
             {'error': 'Input should be a valid string: description'}),
            ({'description': 'Test description'}, HTTPStatus.BAD_REQUEST,
             {"error": "Field required: title"}),
            ({}, HTTPStatus.BAD_REQUEST,
             {"error": "Field required: title"}),
            (None, HTTPStatus.UNSUPPORTED_MEDIA_TYPE, None),
        ])
    def test_create_tasks(self, client, body, app, expected_code, expected_message):
        """Test create task

        :arg client: Flask test client
        :arg body: fixture to create task."""
        response = client.post('/tasks', json=body)
        assert response.status_code == expected_code
        json_data = response.get_json()
        if expected_code == HTTPStatus.BAD_REQUEST:
            assert json_data == expected_message
        elif expected_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
            assert json_data is None
        else:
            with app.app_context():
                from app.tasks.models import db, Tasks
                last_task = db.session.execute(select(Tasks).order_by(Tasks.id.desc())).scalar()
            assert json_data['title'] == last_task.title
            assert json_data['description'] == body['description']
            assert json_data['id'] == last_task.id
            assert datetime.fromisoformat(json_data['created_at']) == last_task.created_at
            assert json_data['updated_at'] == last_task.updated_at

    @pytest.mark.parametrize(
        'body, expected_code, expected_message',
        [
            ({'title': 'Test task', 'description': 'Test description'}, HTTPStatus.OK, None),
            ({'title': 'Test task', 'description': None}, HTTPStatus.OK, None),
            ({'description': 'Test description'}, HTTPStatus.OK, None),
            ({'title': 1, 'description': 'Test description'}, HTTPStatus.BAD_REQUEST,
             {'error': 'Input should be a valid string: title'}),
            ({}, HTTPStatus.OK, None),
            (None, HTTPStatus.UNSUPPORTED_MEDIA_TYPE, None),
        ]
    )
    def test_update_tasks(self, client, body, expected_code, app, expected_message):
        """Test update task

        :arg client: Flask test client
        :arg body: fixture to update task
        :arg expected_code: expected status code
        :arg app: fixture to get app."""
        response = client.put('/tasks/1', json=body)
        assert response.status_code == expected_code
        json_data = response.get_json()
        if expected_code == HTTPStatus.BAD_REQUEST:
            assert json_data == expected_message
        elif expected_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
            assert json_data is None
        else:
            with app.app_context():
                from app.tasks.models import db, Tasks
                updated_task = db.session.execute(select(Tasks).filter(Tasks.id == 1)).scalar()
            assert json_data['title'] == updated_task.title
            assert json_data['description'] == updated_task.description
            assert json_data['id'] == updated_task.id
            assert datetime.fromisoformat(json_data['created_at']) == updated_task.created_at
            assert datetime.fromisoformat(json_data['updated_at']) == updated_task.updated_at

    def test_update_tasks_not_found(self, client):
        """Test update task not found

        :arg client: Flask test client."""
        response = client.put('/tasks/999', json={'title': 'Updated task', 'description': 'Updated description'})
        assert response.status_code == 404
        assert response.get_json() == {'error': 'Task with this id 999 not found'}

    def test_delete_tasks(self, client, app):
        """Test delete task

        :arg client: Flask test client
        :arg app: fixture to get app."""
        response = client.delete('/tasks/1')
        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            from app.tasks.models import db, Tasks
            deleted_task = db.session.execute(select(Tasks).filter(Tasks.id == 1)).scalar()
            assert deleted_task is None
            assert response.get_json() == {'message': f'Successfully deleted task: Test task0 with id: 1'}

    def test_delete_tasks_not_found(self, client):
        """Test delete task not found

        :arg client: Flask test client."""
        response = client.delete('/tasks/999')
        assert response.status_code == 404
        assert response.get_json() == {'error': f'Task with this id 999 not found'}
