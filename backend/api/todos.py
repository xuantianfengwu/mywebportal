from flask import Blueprint, request

todos_bp = Blueprint('todos', __name__)

from ..service.todos_service import TodosService

@todos_bp.route('/task')
def get_todos_task():
    tasks = TodosService().get_all_tasks()
    resp = {'code': 200,
            'message': 'get task success!',
            'data': tasks}
    return resp