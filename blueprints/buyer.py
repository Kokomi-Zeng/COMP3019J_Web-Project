from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from exts import db
from models import Product, Comment, Buyer, User, Purchase

"""
The following code is used to store the routes related to buyer,
such as buyerInfo, charge, buyItem, buyerItem, modifyBuyerInfo.
"""

buyer_bp = Blueprint('buyer', __name__, url_prefix='/buyer')


# Provide get buyerInfo method for the front end buyerInfo page
@buyer_bp.route('/buyerInfo', methods=['GET'])
def buyer_info():
    phone = request.args.get('phone')

    # If phone is not passed in, return an empty string for phone
    if not phone:
        phone = ""

    buyer = Buyer.query.filter_by(phone=phone).first()

    # If buyer is not found, return an empty string for phone
    if not buyer:
        phone = ""

    # If phone is empty, return an empty string for name and introduction
    if phone == "":
        return jsonify({
            "phone": "",
            "name": "",
            "introduction": "",
        })
    # If phone is not empty, return the buyer's name, introduction and phone
    else:
        return jsonify({
            "phone": buyer.phone,
            "name": buyer.name,
            "introduction": buyer.description,
            "status": buyer.user.status
        })


# Provide charge method for a buyer to charge money
@buyer_bp.route('/charge', methods=['GET'])
def charge():
    phone = request.args.get('phone')
    try:
        charge_num = float(request.args.get('charge_num'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid charge amount."})
    # password = request.args.get('password')

    #  find the user
    user = User.query.filter_by(phone=phone).first()

    # If the user is not found or the password is incorrect
    # if not user or not check_password_hash(user.password, password):

    if not user:
        # return jsonify({"success": False, "message": "Can't find user or password incorrect"})
        return jsonify({"success": False, "message": "Can't find user"})

    # If the user is not a buyer
    buyer = Buyer.query.filter_by(phone=phone).first()
    if not buyer:
        return jsonify({"success": False, "message": "The user is not buyer"})

    # If the charge amount is less than 10
    if charge_num < 10:
        return jsonify({"success": False, "message": "The minimum charge amount is 10"})

    # If the status of the user is not active (banned)
    if user.status != 'active':
        return jsonify({"success": False, "message": "User is banned"})

    buyer.balance += charge_num
    db.session.commit()

    return jsonify({"success": True, "message": "Charge successfully"})


# Provide a method for what a buyer has bought
@buyer_bp.route('/buyerItem', methods=['GET'])
def get_buyer_items():
    phone = request.args.get('phone')
    buyer = Buyer.query.filter_by(phone=phone).first()

    # If the buyer is not found, return an empty list
    if not buyer:
        return jsonify([])

    purchased_items = []
    for purchase in buyer.purchases:
        purchased_items.append({
            'product_name': purchase.product.product_name,
            'total_price': purchase.purchase_price,
            'image_src': purchase.image_src_at_time_of_purchase,
            # convert datetime object to string
            'purchase_time': purchase.purchase_time.strftime('%Y-%m-%d %H:%M:%S'),
            'purchase_quantity': purchase.purchase_number
        })

    return jsonify(purchased_items)

@buyer_bp.route('/getAllBuyerItem', methods=['GET'])
def get_all_buyer_items():
    purchased_items = []
    for purchase in Purchase.query.all():
        buyer_name = Buyer.query.filter_by(phone=purchase.buyer_phone).first().name
        product_name = Product.query.filter_by(product_id=purchase.product_id).first().product_name
        purchased_items.append({
            'purchase_id': purchase.purchase_id,
            'product_id': purchase.product_id,
            'product_name': product_name,
            'buyer_name': buyer_name,
            'purchase_quantity': purchase.purchase_number,
            'total_price': purchase.purchase_price,
            'image_src': purchase.image_src_at_time_of_purchase,
            # convert datetime object to string
            'purchase_time': purchase.purchase_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(purchased_items)


# Provide a method for a buyer to buy an item
@buyer_bp.route('/buyItem', methods=['GET'])
def buy_item():
    try:
        product_id = int(request.args.get('product_id'))
        # get the quantity of the product, if not specified, default to 1
        quantity = int(request.args.get('quantity', 1))
    # If the product_id or quantity is not an integer
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid product ID or quantity."})

    phone = request.args.get('phone')
    buyer = Buyer.query.filter_by(phone=phone).first()
    product = Product.query.filter_by(product_id=product_id).first()

    # Judge whether the buyer or product exists
    if not buyer or not product:
        return jsonify({"success": False, "message": "Buyer or product not found"})

    # Judge whether the product is in stock
    if product.storage < quantity:
        return jsonify({"success": False, "message": "Not enough stock"})

    total_price = product.price * quantity

    # Judge whether the buyer has enough money
    if buyer.balance < total_price:
        return jsonify({"success": False, "message": "Insufficient funds"})

    # If the status of the user is not active (banned)
    if buyer.user.status != 'active':
        return jsonify({"success": False, "message": "User is banned"})

    # balance decrease, storage decrease, new purchase added to the database
    buyer.balance -= total_price
    product.storage -= quantity

    new_purchase = Purchase(
        product_id=product.product_id,
        buyer_phone=buyer.phone,
        purchase_number=quantity,
        purchase_price=total_price,
        purchase_time=datetime.now(),
        image_src_at_time_of_purchase=product.image_src
    )

    db.session.add(new_purchase)
    db.session.commit()

    return jsonify({"success": True, "message": "You buy successful!!!"})


# Provide a method for a buyer to know his/her balance
@buyer_bp.route('/getMoney', methods=['GET'])
def get_money():
    phone = request.args.get('phone')

    # validate whether phone exists
    if not phone:
        return jsonify({"success": False, "message": "phone number is required"})

    buyer = Buyer.query.filter_by(phone=phone).first()

    # validate whether buyer exists
    if not buyer:
        return jsonify({"success": False, "message": "buyer not found"})

    return jsonify({"success": True, "phone": phone, "money": buyer.balance})


# Provide a method for a buyer to modify his/her information
@buyer_bp.route('/modifyBuyerInfo', methods=['POST'])
def modify_buyer_info():
    phone = request.json.get('phone')
    name = request.json.get('name')
    introduction = request.json.get('introduction')
    password = request.json.get('password')

    # validate whether phone exists
    if not phone:
        return jsonify({"success": False, "message": "Phone number is required"})

    buyer = Buyer.query.filter_by(phone=phone).first()
    if not buyer:
        return jsonify({"success": False, "message": "Buyer not found"})

    # If the status of the user is not active (banned)
    if buyer.user.status != 'active':
        return jsonify({"success": False, "message": "User is banned"})

    # update information
    if name:
        buyer.name = name
    if introduction:
        buyer.description = introduction
    if password and password != "":
        # encrypt password
        hashed_password = generate_password_hash(password)
        buyer.user.password = hashed_password

    db.session.commit()
    return jsonify({"success": True, "message": "Buyer information updated successfully", "phone": buyer.phone, "name": buyer.name, "introduction": buyer.description})
