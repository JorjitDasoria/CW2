from flask import request, abort, make_response
from config import db
from models import User, user_schema, users_schema





def get_requester_role():
    
    requester_id = request.headers.get('X-User-ID')
    
    if not requester_id:
        return None

    user = User.query.get(requester_id)
    
    if user and user.role:
        return user.role.role_name.lower()
    
    return None

def read_all():
    users = User.query.all()
    return users_schema.dump(users)

def read_one(user_id):
    user = User.query.get(user_id)
    if user is not None:
        return user_schema.dump(user)
    else:
        abort(404, f"User with ID {user_id} not found")

def create(user_data):
    email = user_data.get("email")
    existing_user = User.query.filter(User.email == email).one_or_none()

    if existing_user is None:
        new_user = user_schema.load(user_data, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"User with email {email} already exists")

def update(user_id, user_data):
    existing_user = User.query.get(user_id)

    if existing_user:
        update_user = user_schema.load(user_data, session=db.session)
        
        existing_user.first_name = update_user.first_name
        existing_user.last_name = update_user.last_name
        existing_user.email = update_user.email
        existing_user.location_id = update_user.location_id
        existing_user.role_id = update_user.role_id
        
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 200
    else:
        abort(404, f"User with ID {user_id} not found")

def delete(user_id):
    existing_user = User.query.get(user_id)

    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"User {user_id} successfully deleted", 204)
    else:
        abort(404, f"User with ID {user_id} not found")