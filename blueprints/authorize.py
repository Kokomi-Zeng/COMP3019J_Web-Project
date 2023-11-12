from flask import Blueprint, render_template, request,redirect,jsonify
from flask import session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db
from models import User, Seller, Buyer

"""
This following code is used to store the routes related to authorization,
such as login and  register.
"""

"""
Create a blueprint object, 
the first: the name of the blueprint, 
the second: __name__ represents the current module,
the third: url_prefix represents the prefix, all the routes in here will add this prefix
"""
bp = Blueprint("authorize", __name__, url_prefix="/authorize")

# Provide login method for the front end login page
@bp.route("/login", methods=["POST"])
def login():

    phone = request.json.get('phone')
    password = request.json.get('password')

    if len(phone) > 15:
        return jsonify({"success": False, "message": "Invalid phone number."})
    user = User.query.filter_by(phone=phone).first()
    if user and check_password_hash(user.password, password):
        if user.user_type == 2:
            return jsonify({"success": True, "message": "Login successful", "isAdmin": True})
        else:

            # Passing data to the session
            session['phone'] = user.phone
            session['type'] = user.user_type
            return jsonify({"success": True, "message": "Login successful", "isAdmin": False})
    else:
        return jsonify({"success": False, "message": "Incorrect phone or password."})

# Provide logout method for the front end logout page
@bp.route("/register", methods=["POST"])
def register():

    phone = request.json.get('phone')
    password = request.json.get('password')
    user_type = request.json.get('user_type')

    if len(phone) > 15:
        return jsonify({"success": False, "message": "Invalid phone number."})

    # Verify that the phone number has been registered
    if User.query.filter_by(phone=phone).first():
        return jsonify({"success": False, "message": "Phone number already registered."})

    # Verify user_type, 1 means buyer, 0 means seller
    if user_type not in ['0', '1']:
        return jsonify({"success": False, "message": "Invalid user type."})

    # Create a new user, encrypted the password, and add it to the database
    user = User(phone=phone, password=generate_password_hash(password), user_type=user_type, image_src="https://pinoss.com/kokomi/i/2023/10/20/default_image.jpg", status="active")
    db.session.add(user)

    if user_type == '0':
        seller = Seller(phone=phone, name="new seller", description="")
        db.session.add(seller)

    if user_type == '1':
        buyer = Buyer(phone=phone, name="new buyer", description="", balance=0)
        db.session.add(buyer)

    db.session.commit()
    return jsonify({"success": True, "message": "Registration successful"})





