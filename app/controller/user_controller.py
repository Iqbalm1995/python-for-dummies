from flask import Blueprint, jsonify, request
from ..model.user_model import User
from ..model.response_model import ResponseModel
from database import db
from sqlalchemy import or_
import urllib.parse  # Import urllib.parse for URL decoding
from ..helper.exception_handle import ExceptionHandle
from ..helper.constants import RC_SUCCESS, RC_BAD_REQUEST, RC_NOT_FOUND, RC_ERROR, RM_SUCCESS, RM_BAD_REQUEST, RM_NOT_FOUND, RM_ERROR

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/api/users', methods=['GET'])
def get_users():
    try:
        # Get the 'username', 'full_name', 'page', and 'limit' parameters from the query string
        search = urllib.parse.unquote(request.args.get('search', ''))  # Decode and provide default
        username = urllib.parse.unquote(request.args.get('username', ''))  # Decode and provide default
        full_name = urllib.parse.unquote(request.args.get('full_name', ''))  # Decode and provide default
        page = int(request.args.get('page', 1))  # Default to page 1 if not provided
        limit = int(request.args.get('limit', 10))  # Default to limit 10 if not provided

        # Calculate the offset based on the page and limit
        offset = (page - 1) * limit

        # Initialize the base query
        query = User.query

        # If 'username' parameter is provided, filter the query by username
        # if username:
        #     query = query.filter(User.username == username)

        # Create a list to hold filter conditions
        filter_conditions = []

        # Check if 'username' parameter is provided and add a partial match filter
        if username:
            filter_conditions.append(User.username.ilike(f'%{username}%'))

        # Check if 'full_name' parameter is provided and add a partial match filter
        if full_name:
            filter_conditions.append(User.full_name.ilike(f'%{full_name}%'))

        # Combine filter conditions with OR clauses
        if filter_conditions:
            query = query.filter(or_(*filter_conditions))

        # Create a list to hold filter conditions
        filter_conditions_global = []

        # Coba custom exception
        if search == 'iqbal':
            raise ExceptionHandle("Coba exception", 400)

        if search:
            filter_conditions_global.append(User.username.ilike(f'%{search}%'))
            filter_conditions_global.append(User.full_name.ilike(f'%{search}%'))

        # Combine filter conditions with OR clauses
        if filter_conditions_global:
            query = query.filter(or_(*filter_conditions_global))

        # Create a clone of the query for counting total records
        count_query = query.statement.with_only_columns(db.func.count()).order_by(None)

        # Execute the count query to get the total count
        total_count = db.session.execute(count_query).scalar()

        # Add pagination and order by created_at descending to the query
        query = query.order_by(User.created_at.desc()).offset(offset).limit(limit)

        # Execute the query
        users = query.all()

        user_list = []

        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'created_at': user.created_at.isoformat(),
                'created_by': user.created_by
            }
            user_list.append(user_data)

        # Create the custom response object
        response = ResponseModel(
            status_code=RC_SUCCESS,
            message=RM_SUCCESS,
            count=len(user_list),
            count_total=total_count,
            data=user_list
        )

        return jsonify(response.to_dict()), RC_SUCCESS
    
    except ExceptionHandle as e:

        # Create the custom response object
        responseError = ResponseModel(
            status_code=RC_BAD_REQUEST,
            message=str(e),
            count=0,
            count_total=0,
            data=None  # Set data to None for error response
        )

        # Handle the custom exception with a custom error response
        return jsonify(responseError.to_dict()), RC_BAD_REQUEST

    except Exception as e:

        # Create the custom response object
        responseError = ResponseModel(
            status_code=RC_ERROR,
            message=str(e),
            count=0,
            count_total=0,
            data=None  # Set data to None for error response
        )

        return jsonify(responseError.to_dict()), RC_ERROR
