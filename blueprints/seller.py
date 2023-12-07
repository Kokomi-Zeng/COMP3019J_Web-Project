from flask import Blueprint, render_template, session, request, jsonify
from werkzeug.security import generate_password_hash
from models import Product, Comment, Buyer, User, Seller
from exts import db

"""
The following code is used to store the routes related to sellers,
such as sellerInfo, getSellerByItemID, getIntroductionByCommentID, modifySellerInfo.
"""
seller_bp = Blueprint('seller', __name__, url_prefix='/seller')


# Provide get sellerInfo method for the front end sellerInfo page
@seller_bp.route('/sellerInfo', methods=['GET'])
def seller_info():
    phone = request.args.get('phone')

    # If phone is not passed in, return an empty string for phone
    if not phone:
        return jsonify({"success": False, "message": "Phone number is required"})

    seller = Seller.query.filter_by(phone=phone).first()

    # If seller is not found, return an empty string for phone
    if not seller:
        return jsonify({"success": False, "message": "Seller not found"})

    return jsonify({
        "phone": seller.phone,
        "name": seller.name,
        "introduction": seller.description,
        "status": seller.user.status
    })


# Provide another get sellerInfo method for use itemID to get sellerInfo
@seller_bp.route('/getSellerByItemID', methods=['GET'])
def get_seller_by_item_id():
    product_id = request.args.get('product_id')

    # Verify that product_id exists and is an int type
    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    product = Product.query.filter_by(product_id=product_id).first()

    # Verify that the product exists
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    seller = product.seller

    # Judge whether the seller exists
    if not seller:
        return jsonify({"success": False, "message": "Seller not found"})

    return jsonify({
        "head": "",
        "name": seller.name,
        "introduction": seller.description,
    })


# Provide a method to modify seller information
@seller_bp.route('/modifySellerInfo', methods=['POST'])
def modify_seller_info():
    phone = request.json.get('phone')
    name = request.json.get('name')
    introduction = request.json.get('introduction')
    password = request.json.get('password')

    # Verify that phone exists
    if not phone:
        return jsonify({"success": False, "message": "Phone number is required"})

    seller = Seller.query.filter_by(phone=phone).first()

    # Determine whether the seller exists
    if not seller:
        return jsonify({"success": False, "message": "Seller not found"})

    # If the status of the user is not active (banned)
    if seller.user.status != 'active':
        return jsonify({"success": False, "message": "User is banned"})

    # Update seller information
    if name:
        seller.name = name
    if introduction:
        seller.description = introduction

    if password:
        # encrypt password
        hashed_password = generate_password_hash(password)
        seller.user.password = hashed_password

    db.session.commit()
    return jsonify({"success": True, "message": "Seller information updated successfully", "phone": seller.phone, "name": seller.name, "introduction": seller.description})
