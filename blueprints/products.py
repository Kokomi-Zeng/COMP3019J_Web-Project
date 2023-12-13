from flask import Blueprint, jsonify, request, render_template
from models import Product, db, Comment, User

"""
The following code is used to store the routes related to product,
such as modifyItem, addItem, deleteItem, itemInfoById.
"""

products_bp = Blueprint('products', __name__, url_prefix='/products')


# Provide modify item method for a seller to modify a product
@products_bp.route('/modifyItem', methods=['GET'])
def modify_item():
    seller_phone = request.args.get('seller_phone')
    product_name = request.args.get('product_name')
    description = request.args.get('description')

    try:
        product_id = int(request.args.get('product_id'))
        price = float(request.args.get('price'))
        storage = int(request.args.get('storage'))

        if price > 100000 or storage > 100000 or len(description) > 1000 or len(product_name)> 100:
            return jsonify({"success": False, "message": "Invalid input. Please ensure message is not too long."})

    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid input. Please ensure valid types for product_id, price, and storage."})

    # Verify if the product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    # Check if the product belongs to the seller
    if product.seller_phone != seller_phone:
        return jsonify({"success": False, "message": "The product does not belong to this seller."})

    # If the status of the user is not active (banned)
    user = User.query.filter_by(phone=seller_phone).first()
    if user.status != 'active':
        return jsonify({"success": False, "message": "User is banned"})

    # Update product information
    product.price = price
    product.storage = storage
    product.product_name = product_name
    product.description = description

    db.session.commit()
    return jsonify({"success": True, "message": "Product updated successfully"})

# Provide modify item storage method for a seller to modify a product's storage



# Provide add item method for a seller to add a product
@products_bp.route('/addItem', methods=['GET'])
def add_item():
    seller_phone = request.args.get('seller_phone')
    product_name = request.args.get('product_name')
    description = request.args.get('description')

    try:
        price = float(request.args.get('price'))
        storage = int(request.args.get('storage'))

        if price > 100000 or storage > 100000 or len(description) > 1000 or len(product_name)> 100:
            return jsonify({"success": False, "message": "Invalid input. Please ensure message is not too long."})

    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid input. Please ensure valid types for price and storage."})

    # If the status of the user is not active (banned)
    user = User.query.filter_by(phone=seller_phone).first()
    if user.status != 'active':
        return jsonify({"success": False, "message": "User is banned"})


    # Create a new product
    product = Product(
        price=price,
        storage=storage,
        product_name=product_name,
        description=description,
        seller_phone=seller_phone
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"success": True, "message": "Product added successfully", "product_id": product.product_id})


# Provide delete item method for a seller to delete a product
@products_bp.route('/deleteItem', methods=['GET'])
def delete_item():
    seller_phone = request.args.get('seller_phone')

    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    # Verify if the product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    # Check if the product belongs to the seller
    if product.seller_phone != seller_phone:
        return jsonify({"success": False, "message": "Unauthorized"})

    # If the status of the user is not active (banned)
    user = User.query.filter_by(phone=seller_phone).first()
    if user.status != 'active':
        return jsonify({"success": False, "message": "User is banned"})

    # Delete the product
    db.session.delete(product)
    db.session.commit()

    return jsonify({"success": True, "message": "Product deleted successfully"})


# Provide a method to get item info by product id
@products_bp.route('/itemInfoById', methods=['GET'])
def item_info_by_id():
    # Check if product_id is an integer
    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    product = Product.query.filter_by(product_id=product_id).first()

    # According to the product_id, check if the product exists
    if not product:
        return jsonify({"success": False, "message": "Product not found."})

    # Calculate the average rating of the product
    avg_rating = calculate_average_rating(product_id)

    return jsonify({
        "image_src": product.image_src,
        "name": product.product_name,
        "price": product.price,
        "average_rating": avg_rating,
        "description": product.description,
        "storage": product.storage
    })


# Helper function to calculate the average rating of a product
def calculate_average_rating(product_id):
    comments = Comment.query.filter_by(product_id=product_id).all()
    # If there is no comment, return 1
    if not comments:
        return 1

    total_rating = 0
    for comment in comments:
        total_rating += comment.rating

    average_rating = total_rating / len(comments)

    # Round to the nearest integer
    average_rating = round(average_rating)
    return average_rating


# Provide a method to administer to reset the image of a product
@products_bp.route('/resetItemImage', methods=['GET'])
def reset_item_image():
    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    product = Product.query.filter_by(product_id=product_id).first()

    # verify if the product exists
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    # Update the image_src of the product
    product.image_src = "https://pinoss.com/kokomi/i/2023/12/07/k7c.png"

    db.session.commit()
    return jsonify({"success": True, "message": "Product image reset successfully"})


# Provide a method to administer to reset the name of a product
@products_bp.route('/resetItemName', methods=['GET'])
def reset_item_name():
    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid Product ID. Please provide a valid integer."})

    product = Product.query.filter_by(product_id=product_id).first()

    # verify if the product exists
    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    # Update the name of the product
    product.product_name = "new product"

    db.session.commit()
    return jsonify({"success": True, "message": "Product name reset successfully"})

@products_bp.route('/getAllProducts', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    result = []
    for product in products:
        # Calculate the average rating of the product
        avg_rating = calculate_average_rating(product.product_id)
        result.append({
            "product_id": product.product_id,
            "seller_phone": product.seller_phone,
            "price": product.price,
            "storage": product.storage,
            "product_name": product.product_name,
            "image_src": product.image_src,
            "description": product.description,
            "rating": avg_rating
        })
    return jsonify(result)



