from flask import Blueprint, render_template, request,redirect,jsonify
from flask import session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db
from models import User, Seller, Buyer

# Create a blueprint object, the first: the name of the blueprint, the second; __name__ represents the current module,
# the third: url_prefix represents the prefix, all the routes in here will add this prefix
bp = Blueprint("authorize", __name__, url_prefix="/authorize")

@bp.route("/login", methods=["POST"])
def login():

    phone = request.json.get('phone')
    password = request.json.get('password')

    if len(phone) > 15:
        # return jsonify(success=False, message="Invalid phone number.")
        return jsonify({"success": False, "message": "Invalid phone number."})
    user = User.query.filter_by(phone=phone).first()
    if user and check_password_hash(user.password, password):
        session['phone'] = user.phone
        session['type'] = user.user_type
        # return jsonify(success=True, message="Login successful")
        return jsonify({"success": True, "message": "Login successful"})
    else:
        # return jsonify(success=False, message="Incorrect phone or password.")
        return jsonify({"success": False, "message": "Incorrect phone or password."})


@bp.route("/register", methods=["POST"])
def register():

    phone = request.json.get('phone')
    password = request.json.get('password')
    user_type = request.json.get('user_type')

    if len(phone) > 15:
        # return jsonify(success=False, message="Invalid phone number.")
        return jsonify({"success": False, "message": "Invalid phone number."})
    # 验证手机号是否已经被注册
    if User.query.filter_by(phone=phone).first():
        # return jsonify(success=False, message="Phone number already registered.")
        return jsonify({"success": False, "message": "Phone number already registered."})
    # 验证user_type, 1表示买家，0表示卖家
    if user_type not in ['0', '1']:
        # return jsonify(success=False, message="Invalid user type.")
        return jsonify({"success": False, "message": "Invalid user type."})
    user = User(phone=phone, password=generate_password_hash(password), user_type=user_type)
    db.session.add(user)

    if user_type == '0':
        seller = Seller(phone=phone, name="new seller", description="")
        db.session.add(seller)

    if user_type == '1':
        buyer = Buyer(phone=phone, name="new buyer", description="", balance=0)
        db.session.add(buyer)

    db.session.commit()
    # return jsonify(success=True, message="Registration successful")
    return jsonify({"success": True, "message": "Registration successful"})





