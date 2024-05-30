from http import HTTPStatus

from flask import jsonify, views, request
from pydantic_core import ValidationError
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.tasks.models import db
from app.tasks.schemas import TasksSchema, TasksResponseSchema as TResponseS, TaskUpdateSchema
from flask_pydantic import validate


class TasksView(views.MethodView):
    """Tasks view for handling tasks requests."""
    def __init__(self, model):
        self.model = model

    def _get_task(self, pk: int):
        """Get task by id.

        :arg pk: id of task

        :returns Task model: returned instance of task and status code."""
        return db.session.get(self.model, pk)

    @validate(on_success_status=HTTPStatus.CREATED)
    def post(self):
        """Create task.

        :returns Task model: created task and status code."""
        try:
            # Get body from request for validation and creation
            body = TasksSchema(**request.get_json())
            # Exclude unset fields for creation task
            task = self.model(**body.model_dump(exclude_unset=True))
            db.session.add(task)
            db.session.commit()
            return TResponseS.model_validate(task)
        except ValidationError as e:
            message = f'{str(e.errors()[0]["msg"])}: {str(e.errors()[0]["loc"][0])}'
            return jsonify(error=message), HTTPStatus.BAD_REQUEST

    @validate()
    def get(self, pk: int | None = None):
        """Get task by id or all tasks.

        :arg pk: id of task to get or None

        :returns Task model: task or all tasks and status code."""
        try:
            if pk is None:
                tasks = self.model.query.all()
                return jsonify([TResponseS.model_validate(task).model_dump() for task in tasks])
            else:
                task = self._get_task(pk)
                if task is None:
                    return jsonify({'error': f'Task with this id {pk} not found'}), HTTPStatus.NOT_FOUND
                return TResponseS.model_validate(task)
        except AttributeError:
            return jsonify({'error': f'Task with this id {pk} not found'}), HTTPStatus.NOT_FOUND

    @validate()
    def put(self, pk: int):
        """Put task by id.

        :arg pk: id of task to update

        :returns Task model: updated task and status code."""
        try:
            # If task not found, returns 404
            task = self._get_task(pk)
            # Get body from request for validation and update
            body = TaskUpdateSchema(**request.get_json())
            # Exclude unset fields for update task
            task.query.update(body.model_dump(exclude_unset=True))
            db.session.commit()
            return TResponseS.model_validate(task)
        except AttributeError:
            return jsonify({'error': f'Task with this id {pk} not found'}), HTTPStatus.NOT_FOUND
        except ValidationError as e:
            message = f'{str(e.errors()[0]["msg"])}: {str(e.errors()[0]["loc"][0])}'
            return jsonify(error=message), HTTPStatus.BAD_REQUEST

    @validate()
    def delete(self, pk: int):
        """Delete task by id.

        :arg pk: id of task
        :returns: success message and status code."""
        try:
            task = self._get_task(pk)
            db.session.delete(task)
            db.session.commit()
            # Returns status 200 for output with a success message, instead of 204
            return jsonify(message=f'Successfully deleted task: {task.title} with id: {pk}')
        except UnmappedInstanceError:
            return jsonify({'error': f'Task with this id {pk} not found'}), HTTPStatus.NOT_FOUND

