from flask import Blueprint, render_template, session, request, jsonify
from werkzeug.security import generate_password_hash
from models import Product, Comment, Buyer, User, Seller, Purchase
from exts import db

"""
The following code is used to store the routes related to administer,
such ?????????????????????????????????????????????????????????
"""
administer_bp = Blueprint('administer', __name__, url_prefix='/administer')

@administer_bp.route('/deleteUser', methods=['GET'])
def delete_user():
    phone = request.args.get('phone')

    # verify if the phone number is provided
    if not phone:
        return jsonify({"success": False, "message": "Phone number is required"})

    user = User.query.filter_by(phone=phone).first()

    # Verify that the user exists
    if not user:
        return jsonify({"success": False, "message": "User not found"})

    # delete all data associated with the user
    if user.user_type == '1':  # buyer
        # delete all comments and purchases made by the buyer
        Comment.query.filter_by(commenter_phone=phone).delete()
        Purchase.query.filter_by(buyer_phone=phone).delete()
        Buyer.query.filter_by(phone=phone).delete()
    elif user.user_type == '0':  # seller
        # first delete all products and their related comments and purchase records
        products = Product.query.filter_by(seller_phone=phone).all()
        for product in products:
            Comment.query.filter_by(product_id=product.product_id).delete()
            Purchase.query.filter_by(product_id=product.product_id).delete()
        # then delete all products and seller
        Product.query.filter_by(seller_phone=phone).delete()
        Seller.query.filter_by(phone=phone).delete()

    # finally delete the user itself
    User.query.filter_by(phone=phone).delete()

    db.session.commit()
    return jsonify({"success": True, "message": "User deleted successfully"})

@administer_bp.route('/updateBuyerAccount', methods=['GET'])
def update_buyer_account():
    phone = request.args.get('phone')
    amount = request.args.get('amount')

    # Validate that phone and amount are provided
    if not phone or amount is None:
        return jsonify({"success": False, "message": "Phone number and amount are required", "amount": amount})

    try:
        # Convert amount to float
        amount = float(amount)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid amount. Please provide a valid number.", "amount": amount})

    # Find the buyer by phone number
    buyer = Buyer.query.filter_by(phone=phone).first()

    # Check if the buyer exists
    if not buyer:
        return jsonify({"success": False, "message": "Buyer not found", "amount": amount})

    # Set the buyer's account balance to the provided amount
    buyer.balance = amount

    db.session.commit()
    return jsonify({"success": True, "message": "Buyer account updated successfully", "amount": buyer.balance})

@administer_bp.route('/deleteItem', methods=['GET'])
def delete_item():
    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    # Delete related comments and purchases
    Comment.query.filter_by(product_id=product_id).delete()
    Purchase.query.filter_by(product_id=product_id).delete()

    # Finally, delete the product itself
    db.session.delete(product)

    db.session.commit()
    return jsonify({"success": True, "message": "Product deleted successfully"})

@administer_bp.route('/deleteComment', methods=['GET'])
def delete_comment():
    try:
        comment_id = int(request.args.get('comment_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Comment ID. Please provide a valid integer."})

    # Check if the comment exists
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"success": False, "message": "Comment not found"})

    # Delete the comment
    db.session.delete(comment)

    db.session.commit()
    return jsonify({"success": True, "message": "Comment deleted successfully"})

@administer_bp.route('/deleteBuyerItem', methods=['GET'])
def delete_buyer_item():
    try:
        purchase_id = int(request.args.get('purchase_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Purchase ID. Please provide a valid integer."})

    # Check if the purchase record exists
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"success": False, "message": "Purchase record not found"})

    # Delete the purchase record
    db.session.delete(purchase)

    db.session.commit()
    return jsonify({"success": True, "message": "Purchase record deleted successfully"})

@administer_bp.route('/banUser', methods=['GET'])
def ban_user():
    admin_phone = request.args.get('admin_phone')
    user_phone = request.args.get('user_phone')

    # 验证管理员电话号码和用户电话号码是否提供
    if not admin_phone or not user_phone:
        return jsonify({"success": False, "message": "Admin and user phone numbers are required"})

    # 验证操作者是否为管理员
    admin = User.query.filter_by(phone=admin_phone).first()
    if not admin or admin.user_type != '2':
        return jsonify({"success": False, "message": "Operation not permitted. Admin privileges required."})

    # 查找要操作的用户
    user = User.query.filter_by(phone=user_phone).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"})

    # 根据用户当前状态切换禁止状态
    if user.status == 'banned':
        user.status = 'active'
        message = "User has been unbanned successfully"
    else:
        user.status = 'banned'
        message = "User has been banned successfully"

    db.session.commit()
    return jsonify({"success": True, "message": message})
