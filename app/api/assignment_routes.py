from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app.models import User, db, Assignment
from sqlalchemy.sql import func



assignment_routes = Blueprint('assignments', __name__)

# Retrieve all assignments Paginated
# Pagination Example for request: GET /assignments?page=1&per_page=5

@assignment_routes.route('/')
@login_required
def get_assignments():

    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = request.args.get('per_page', 10, type=int)  # Default 10 results per page
    status = request.args.get('status', None)  # Optional status filter
    location_id = request.args.get('location_id', None, type=int)  # Optional location filter
    sort_by = request.args.get('sort_by', 'created_at')  # Default sorting by created_at
    sort_order = request.args.get('sort_order', 'desc')  # Default descending order

    query = Assignment.query

    if current_user.user_type == 'Client':
        query = query.filter_by(client_id=current_user.id)
    elif current_user.user_type == 'Preserver':
        query = query.filter(
            (Assignment.preserver_id == current_user.id) | (Assignment.status == 'Open')
        )
    elif current_user.user_type == 'Admin':
        query = query #Admins get all assignments
    else:
        return jsonify({"error": "Unauthorized"}), 403

    if status:
        query = query.filter_by(status=status)
    if location_id:
        query = query.filter_by(location_id=location_id)

    # Sorting

    if sort_by not in ['created_at', 'updated_at', 'base_price']:
        return jsonify({'error': 'Invalid sor field'}), 400

    order = getattr(Assignment, sort_by)
    if sort_order == 'desc':
        order = order.desc()
    query = query.order_by(order)

    # Pagination
    paginated_results = query.paginate(page=page, per_page=per_page, error_out=False)


    return jsonify({
        'assignments': [assignment.to_dict() for assignment in paginated_results.items],
        'total_pages': paginated_results.pages,
        'current_page': paginated_results.page
    })



# Retrieve Single Assignment By Id
@assignment_routes.route('/<int:assignment_id>')
@login_required
def get_assignment(assignment_id):

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    # Authorization based on user type
    if current_user.user_type == 'Client':
        if assignment.client_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

    elif current_user.user_type == 'Preserver':
        if assignment.preserver_id != current_user.id or (assignment.status not in['Open', 'Completed', 'Paid_out']):
            return jsonify({'error': 'Unauthorized'}), 403

    elif current_user.user_type == 'Admin':
        pass

    else:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(assignment.to_dict()), 200

# Create New Assignment
@assignment_routes.route('/', methods=['POST'])
@login_required
def create_assignment():

    # Preservers cant create an assignment
    if current_user.user_type == 'Preserver':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    new_assignment = Assignment(
        client_id=data['client_id'],
        descriptions=data['description'],
        base_price=data['base_price'],
        location_id=data['location_id'],
        status='Pending'
    )
    db.session.add(new_assignment)
    db.session.commit()
    return jsonify(new_assignment.to_dict())

# Update an Assignment
@assignment_routes.route('/<int:assignment_id>', methods=['PUT'])
@login_required
def update_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    # Ensure the client is only updating their own assignments
    if current_user.user_type == 'Client':
        if assignment.client_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
        assignment.description = request.json.get('description', assignment.description)

        # Once assignment is created, Clients can only cancel assignments, not change to other statuses
        if request.json.get('status') and request.json.get('status')!= 'Cancelled':
            return jsonify({"error": "Unauthorized"}), 403
        assignment.status = request.json.get('status', assignment.status)

    # Ensure the preserver is assigned to the assignment
    elif current_user.user_type == 'Preserver':
        if assignment.preserver_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403

        # Preservers can update status to 'Cancelled' or 'Pending', but not other statuses
        if request.json.get('status') and request.json.get('status') not in ['Cancelled', 'Started', 'Submitted']:
            return jsonify({"error": "Unauthorized"}), 403
        assignment.status = request.json.get('status', assignment.status)

    # Admins have full control
    elif current_user.user_type == 'Admin':
        assignment.description = request.json.get('description', assignment.description)
        assignment.status = request.json.get('status', assignment.status)
        assignment.base_price = request.json.get('base_price', assignment.base_price)

    else:
        return jsonify({'error': 'Unauthorized'}), 403

    # Update the timestamp of the modification
    assignment.updated_at = func.now()

    db.session.commit()
    return jsonify(assignment.to_dict())

#Delete an Assignment
@assignment_routes.route('/<int:assignment_id>', methods=['DELETE'])
@login_required
def delete_assignment(assignment_id):

    # Only Admins can delete an assignment
    if current_user.user_type != 'Admin':
        return jsonify({'error': "Unauthorized"}), 403

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"message": "Assignment deleted successfully"})

#Assign Preserver to Assignment
@assignment_routes.route('/<int:assignment_id>/assign', methods=['PATCH'])
@login_required
def assign_preserver(assignment_id):
    # Only Admins can assign a preserver to an assignment
    if current_user.user_type != 'Admin':
        return jsonify({'error': "Unauthorized"}), 403

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    data = request.json
    preserver_id = data.get('preserver_id')
    status = data.get('status')
    if not preserver_id:
        return jsonify({"error": "Preserver ID is required"}), 400

    #Assignment funded by client changes status to open, refer to payment model
    #Preserver assigned only if status is open
    elif status != 'Open':
        return jsonify({'error': 'Assignment pending funding status from client'})

    assignment.preserver_id = preserver_id
    assignment.status = 'Assigned'
    assignment.updated_at = func.now()

    db.session.commit()
    return jsonify(assignment.to_dict())

#Mark Assignment as Completed, continue to pay out
#This is different than cancelled assignments
@assignment_routes.route('/<int:assignment_id>/complete', methods=['PATCH'])
@login_required
def complete_assignment(assignment_id):

    # Only Admins can mark assignments Completed
    if current_user.user_type != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    if assignment.status != 'Submitted':
        return jsonify({"error": "Assignment must be submitted from preserver before completion"}), 400

    assignment.status = "Completed"
    assignment.updated_at = func.now()

    db.session.commit()
    return jsonify(assignment.to_dict())

#Cancel an Assignment
@assignment_routes.route('/<int:assignment_id>/cancel', methods=['PATCH'])
@login_required
def cancel_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404
    if assignment.status == 'Completed':
        return jsonify({"error": "Cannot cancel a completed assignment"}), 400
    if assignment.status == 'Paid_Out':
        return jsonify({"error": "Cannot cancel a paid out assignment"}), 400

    assignment.status = 'Cancelled'
    assignment.updated_at = func.now()

    db.session.commit()
    return jsonify(assignment.to_dict())

#Filtering Routes | Searching Routes | ***ADMIN USE ONLY***

#Retrieve Assignment by Status
@assignment_routes.route('/status/<string:status>')
@login_required
def get_assignments_by_status(status):
    if current_user.user_type != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403
    assignments = Assignment.query.filter_by(status=status).all()
    return jsonify([assignment.to_dict() for assignment in assignments])

#Retrieve Assignment for a Specific User (Client or Preserver)
# For getting assignments for logged in user use get_assignments
@assignment_routes.route('/user/<int:user_id>')
@login_required
def get_user_assignments(user_id):
    if current_user.user_type != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403
    assignments = Assignment.query.filter(
        (Assignment.client_id == user_id) | (Assignment.preserver_id == user_id)
    ).all()
    return jsonify([assignment.to_dict() for assignment in assignments])

#Search Assignments by Keyword in Description
@assignment_routes.route('/search')
@login_required
def search_assignments():
    if current_user.user_type != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403
    keyword = request.args.get('q', '')
    assignments = Assignment.query.filter(Assignment.description.ilike(f'%{keyword}%')).all()
    return jsonify([assignment.to_dict() for assignment in assignments])
