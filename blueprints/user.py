from flask import Blueprint, render_template, session, request, jsonify
from werkzeug.security import generate_password_hash
from models import Product, Comment, Buyer, User, Seller
from exts import db

"""
The following code is used to store the routes related to users,
such as resetUserName, resetUserImage, resetUserIntroduction.
"""

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Provide a method for administer to reset the user's name
@user_bp.route('/resetUserName', methods=['GET'])
def reset_user_name():
    phone = request.args.get('phone')

    # verify if the phone number is provided
    if not phone:
        return jsonify({"success": False, "message": "Phone number is required"})

    user = User.query.filter_by(phone=phone).first()

    # Verify that the user exists
    if not user:
        return jsonify({"success": False, "message": "User not found"})

    # reset username according to user type
    if user.user_type == '1':  # buyer
        buyer = Buyer.query.filter_by(phone=phone).first()
        if buyer:
            buyer.name = "new buyer"
    elif user.user_type == '0':  # seller
        seller = Seller.query.filter_by(phone=phone).first()
        if seller:
            seller.name = "new seller"

    db.session.commit()
    return jsonify({"success": True, "message": "Username reset successfully"})

# Provide a method for administer to reset the user's image
@user_bp.route('/resetUserImage', methods=['GET'])
def reset_user_image():
    phone = request.args.get('phone')

    # verify if the phone number is provided
    if not phone:
        return jsonify({"success": False, "message": "Phone number is required"})

    user = User.query.filter_by(phone=phone).first()

    # Verify that the user exists
    if not user:
        return jsonify({"success": False, "message": "User not found"})

    # reset the user's image
    user.image_src = "https://pinoss.com/kokomi/i/2023/10/20/default_image.jpg"

    db.session.commit()
    return jsonify({"success": True, "message": "Image reset successfully"})

# Provide a method for administer to reset the user's introduction
@user_bp.route('/resetUserIntroduction', methods=['GET'])
def reset_user_introduction():
    phone = request.args.get('phone')

    # verify if the phone number is provided
    if not phone:
        return jsonify({"success": False, "message": "Phone number is required"})

    user = User.query.filter_by(phone=phone).first()

    # Verify that the user exists
    if not user:
        return jsonify({"success": False, "message": "User not found"})

    # reset the user's introduction
    user.description = ""

    db.session.commit()
    return jsonify({"success": True, "message": "Introduction reset successfully"})

@user_bp.route('/switchMode', methods=['GET'])
def light_mode():
    mode = session.get('mode')
    if not mode:
        session['mode'] = True
        print(session['mode'])
        return jsonify({"mode": True})
    else:
        session['mode'] = not mode
        print(session['mode'])
        return jsonify({"mode": not mode})


@user_bp.route('/getMode', methods=['GET'])
def get_mode():
    mode = session.get('mode')
    if mode is None:
        session['mode'] = True
        print(mode)
        return jsonify({"mode": True})
    else:
        print(mode)
        return jsonify({"mode": mode})