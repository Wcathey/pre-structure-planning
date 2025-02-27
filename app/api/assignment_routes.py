from flask import Blueprint
from flask_login import login_required
from app.models import Assignment

assignment_routes = Blueprint('assignments', __name__)


@assignment_routes.route('/')
@login_required
def assignments():
    """
    Query for all assignments and returns them in a list of assignment dictionaries
    """
    assignments = Assignment.query.all()
    return {'assignments': [assignment.to_dict() for assignment in assignments]}


@assignment_routes.route('/<int:id>')
@login_required
def assignment(id):
    """
    Query for an assignment by id and returns that assignment in a dictionary
    """
    assignment = Assignment.query.get(id)
    return assignment.to_dict()
