"""Routes for user authentication."""
from flask import current_app as app
from flask import redirect, request, url_for, jsonify, Blueprint, session
from flask_login import current_user, login_user, confirm_login, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.local import LocalProxy

from . import login_manager, mongo

from .user import User

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

Users = mongo.db.users


@auth_bp.route("/signup", methods=["GET"],)
def signup(username, password):

    existing_user = Users.find_one(username)
    print("Existing Users:", existing_user)
    if existing_user is None:
        user = User(username, generate_password_hash(password))
        result = user.createMongoUser(Users)
    
    return 'Username already exist', 401



@auth_bp.route("/login", methods=["GET"], )
def login():

    username = request.args['username']
    password = request.args['password']
    user = User(username, password)

    if current_user.is_authenticated: # type: ignore
        confirm_login()
        return jsonify({'username': username}), 201

    if check_password_hash(pwhash=user.password, password=password):
        login_user(user, remember=True)
        return jsonify({'username': user.username}), 201
    return unauthorized()



@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    logout_user()
    print("Logout success")
    return jsonify({}), 201



@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        user = "5"
        if user is not None:
            userObject = User("root", "password")
            return userObject
    return None


@login_manager.unauthorized_handler
def unauthorized():
    return '', 401 