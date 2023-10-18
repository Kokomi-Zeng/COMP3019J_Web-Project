from flask import Blueprint, jsonify, request, render_template
from models import Product, db, Comment

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def products():
    return render_template('products.html')

@products_bp.route('/modifyItem', methods=['GET'])
def modify_item():
    seller_phone = request.args.get('seller_phone')
    image_src = request.args.get('image_src')
    product_name = request.args.get('product_name')
    description = request.args.get('description')

    try:
        product_id = int(request.args.get('product_id'))
        price = float(request.args.get('price'))
        storage = int(request.args.get('storage'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. Please ensure valid types for product_id, price, and storage."}), 400

    # 验证商品是否存在
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # 检查商品是否属于该卖家
    if product.seller_phone != seller_phone:
        return jsonify({"message": "Unauthorized"}), 403

    # 更改商品信息
    product.price = price
    product.image_src = image_src
    product.storage = storage
    product.product_name = product_name
    product.description = description

    # 弄到数据库中
    db.session.commit()

    # 状态码200表示服务器已成功处理了请求
    return jsonify({"message": "Product updated successfully"}), 200

@products_bp.route('/addItem', methods=['GET'])
def add_item():
    seller_phone = request.args.get('seller_phone')
    image_src = request.args.get('image_src')
    product_name = request.args.get('product_name')
    description = request.args.get('description')

    try:
        price = float(request.args.get('price'))
        storage = int(request.args.get('storage'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. Please ensure valid types for price and storage."}), 400

    # 创建新的商品
    product = Product(
        price=price,
        image_src=image_src,
        storage=storage,
        product_name=product_name,
        description=description,
        seller_phone=seller_phone
    )

    # 将商品添加到数据库
    db.session.add(product)
    db.session.commit()

    # 状态码201表示请求成功并且服务器创建了新的资源
    return jsonify({"message": "Product added successfully"}), 201


@products_bp.route('/deleteItem', methods=['GET'])
def delete_item():
    seller_phone = request.args.get('seller_phone')

    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid Product ID. Please provide a valid integer."}), 400

    # 验证商品是否存在
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # 检查商品是否属于该卖家
    if product.seller_phone != seller_phone:
        return jsonify({"message": "Unauthorized"}), 403

    # 删除商品
    db.session.delete(product)
    db.session.commit()

    # 状态码200表示服务器已成功处理了请求
    return jsonify({"message": "Product deleted successfully"}), 200


@products_bp.route('/itemInfoById', methods=['GET'])
def item_info_by_id():
    # product_id是否为int类型
    try:
        product_id = int(request.args.get('product_id'))
    except (TypeError, ValueError):
        # return jsonify({"error": "Invalid Product ID. Please provide a valid integer."}), 400
        return jsonify([])

    product = Product.query.filter_by(product_id=product_id).first()

    # 根据product_id查询到的商品是否存在
    if not product:
        # return jsonify({"error": "Product not found"}), 404
        return jsonify([])
    avg_rating = calculate_average_rating(product_id)

    return jsonify({
        "image_src": product.image_src,
        "name": product.product_name,
        "price": product.price,
        "average_rating": avg_rating,
        "storage": product.storage
    }), 200


# 辅助函数来计算商品的平均rating
def calculate_average_rating(product_id):
    comments = Comment.query.filter_by(product_id=product_id).all()
    # 如果没有评论，直接0.0分
    if not comments:
        return 0.0

    total_rating = 0
    for comment in comments:
        total_rating += comment.rating

    average_rating = total_rating / len(comments)
    return average_rating



