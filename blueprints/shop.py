from flask import Blueprint, render_template, session, request, jsonify
from models import User, Product, Comment, Purchase
from sqlalchemy import func
from exts import db

"""
The following code is used to store the routes related to shop,
such as searchItemByName, isItemMatchSeller, hasNextPage.
"""

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')


# Provide a method for search item by name
@shop_bp.route('/searchItemByName', methods=['GET'])
def search_item_by_name():
    phone = request.args.get('phone')

    # If keyword is not passed in, return an empty string for keyword
    keyword = request.args.get('keyword', '')

    try:
        page_num = int(request.args.get('page_num', 1))
        # check if page_num is less than or equal to 0
        if page_num <= 0:
            page_num = 1
    except (TypeError, ValueError):
        # If there is an error, set page_num to 1
        page_num = 1

    per_page = 10

    # offset means from which one to start, limit means how many to take
    offset = (page_num - 1) * per_page

    # find the user
    user = User.query.filter_by(phone=phone).first()

    query = Product.query

    # if keyword is not empty, filter by keyword
    if keyword:
        # this is actually the search result for buyer and non-login user
        query = query.filter(Product.product_name.like(f"%{keyword}%"))

    # if user is buyer or seller
    if user:
        # if user is seller, only search his/her own products
        if user.user_type == "0":
            query = query.filter_by(seller_phone=phone)
    # if the user is non-login user, limit the page_num to 1
    else:
        if page_num > 1:
            return jsonify([])

    # All products on a certain page
    products = query.limit(per_page).offset(offset).all()

    # ranking from high to low according to average rating
    sorted_products = sorted(products, key=lambda product: calculate_average_rating(product.product_id), reverse=True)

    product_list = []
    for product in sorted_products:
        avg_rating = calculate_average_rating(product.product_id)
        product_list.append({
            "product_name": product.product_name,
            "image_src": product.image_src,
            "rating": avg_rating,
            "price": product.price,
            "product_id": product.product_id
        })

    return jsonify(product_list)


# Provide a method to determine whether the item matches the seller
@shop_bp.route('/isItemMatchSeller', methods=['GET'])
def is_item_match_seller():
    phone = request.args.get('phone')

    # Verify that the product ID exists and is an int type
    try:
        product_id = int(request.args.get('product_id'))
    except(TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    product = Product.query.get(product_id)

    # Verify that the product exists
    if not product:
        return jsonify({"success": False, "message": "Product not found."})

    if product.seller_phone == phone:
        return jsonify({"success": True, "belong":True})
    else:
        return jsonify({"success": True, "belong":False})


# Provide a method to check whether there is a next page
@shop_bp.route('/hasNextPage', methods=['GET'])
def has_next_page():
    phone = request.args.get('phone')
    keyword = request.args.get('keyword', "")

    try:
        page_num = int(request.args.get('page_num', 1))
        # check if page_num is less than or equal to 0
        if page_num <= 0:
            page_num = 1
    except ValueError:
        return jsonify({"has_next": False})

    per_page = 10

    # This offset is different from the offset in searchItemByName,
    # It means how many products are there after the current page
    offset = page_num * per_page

    # find the user
    user = User.query.filter_by(phone=phone).first()

    # If phone is not passed in or the user cannot be found in the database after input
    if not phone or not user:
        return jsonify({"has_next": False})

    query = Product.query

    if keyword:
        query = query.filter(Product.product_name.like(f"%{keyword}%"))

    if user:
        if user.user_type == "0":
            query = query.filter_by(seller_phone=phone)
    # if the user is non-login user, limit the page_num to 1
    else:
        if page_num > 1:

            return jsonify({"has_next": False})

    # offset: from which one to start, limit: how many to take, count: how many in total
    next_page_products_count = (query.limit(per_page).offset(offset)).count()
    boolean = next_page_products_count > 0
    return jsonify({"has_next": boolean})


# Helper function to calculate the average rating of the product
def calculate_average_rating(product_id):
    comments = Comment.query.filter_by(product_id=product_id).all()

    # If there is no comment, return 0.0
    if not comments:
        return 0.0

    total_rating = 0
    for comment in comments:
        total_rating += comment.rating

    average_rating = total_rating / len(comments)
    return average_rating





